"""GitHub Actions workflows: what runs for pull requests, and what can never deploy.

The production-content job of ci.yml is also executed here, step by step, against temporary
repositories: valid content must pass, every kind of broken production content must fail, and a
repository without production content (the state of main before the first publication) must pass.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from conftest import FIXTURE, REPO, make_production_like, replace_in, write

WORKFLOWS = REPO / ".github" / "workflows"
FULL_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
DEPLOY_ACTIONS = ("actions/deploy-pages", "actions/upload-pages-artifact", "actions/configure-pages")


def workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def triggers(wf: dict) -> dict:
    # YAML 1.1 reads the bare key `on` as the boolean True.
    return wf.get("on", wf.get(True))


def steps(job: dict) -> list[dict]:
    return job["steps"]


def step(job: dict, name: str) -> dict:
    found = [s for s in steps(job) if s.get("name") == name]
    assert len(found) == 1, f"expected one step named {name!r}"
    return found[0]


CI = workflow("ci.yml")
PRODUCTION = CI["jobs"]["production"]


# ---------------------------------------------------------------- structure


def test_ci_runs_for_pull_requests_and_main():
    on = triggers(CI)
    assert "pull_request" in on
    assert on["push"]["branches"] == ["main"]


def test_ci_can_never_deploy():
    assert CI["permissions"] == {"contents": "read"}
    for name, job in CI["jobs"].items():
        assert "environment" not in job, name
        for scope, level in (job.get("permissions") or {}).items():
            assert level in ("read", "none"), f"{name}: {scope}: {level}"
        for s in steps(job):
            assert not str(s.get("uses", "")).startswith(DEPLOY_ACTIONS), f"{name}: {s.get('name')}"


@pytest.mark.parametrize("name", ["ci.yml", "pages.yml"])
def test_every_action_is_pinned_to_a_full_commit_sha(name):
    for job_name, job in workflow(name)["jobs"].items():
        for s in steps(job):
            if "uses" in s:
                assert FULL_SHA.match(s["uses"]), f"{name}: {job_name}: {s['uses']}"


def test_fixture_checks_stay_in_place():
    assert CI["env"]["SITE_SOURCE"] == "tests/fixtures/sample"
    assert any(s.get("run") == "uv run pytest" for s in steps(CI["jobs"]["tests"]))
    build = " ".join(s.get("run", "") for s in steps(CI["jobs"]["build"]))
    for command in ("check-tracked", 'validate --source "$SITE_SOURCE"', "--renderer zensical", "--renderer material"):
        assert command in build


def test_production_job_validates_the_repository_unconditionally():
    validate = step(PRODUCTION, "Validate repository data and content")
    assert "if" not in validate
    assert validate["run"] == "uv run teaching-hub validate --source ."


def test_production_job_builds_and_checks_only_when_production_content_exists():
    status = step(PRODUCTION, "Look for production content")
    assert status["id"] == "status"
    assert "production-status --source . --github-output" in status["run"]
    gated = [s for s in steps(PRODUCTION) if re.search(r"teaching-hub (build|check) ", s.get("run", ""))]
    assert len(gated) >= 3
    for s in gated:
        assert s["if"] == "steps.status.outputs.content == 'true'", s["name"]
        assert "--production" in s["run"] and "--source ." in s["run"]
    renderers = " ".join(s["run"] for s in gated)
    assert "--renderer zensical" in renderers and "--renderer material" in renderers
    assert "check-materials --source ." in step(PRODUCTION, "Check repository materials")["run"]


def test_production_job_offers_the_built_site_for_manual_qa():
    upload = step(PRODUCTION, "Upload production site for manual QA")
    assert upload["uses"].startswith("actions/upload-artifact@")
    assert upload["if"] == "steps.status.outputs.content == 'true'"
    assert upload["with"]["if-no-files-found"] == "error"


def test_pages_workflow_never_runs_for_pull_requests():
    on = triggers(workflow("pages.yml"))
    assert set(on) == {"push", "workflow_dispatch"}
    assert on["push"]["branches"] == ["main"]


# ---------------------------------------------------------------- the production job, executed

_CONDITION = re.compile(r"^steps\.(\w+)\.outputs\.(\w+) (==|!=) '([^']*)'$")
CLI = f'"{sys.executable}" -m teaching_hub.cli'
# Steps that need the network (cloning the linked repositories); covered by the materials tests.
NETWORK_STEPS = {"Check repository materials"}


def run_production_job(root: Path, tmp_path: Path) -> tuple[bool, str]:
    """Run the `run:` steps of the production job like Actions would; return (passed, log)."""
    outputs: dict[str, dict[str, str]] = {}
    log: list[str] = []
    runner_temp = tmp_path / "runner-temp"
    runner_temp.mkdir(exist_ok=True)
    for n, s in enumerate(steps(PRODUCTION)):
        if "run" not in s or s["name"] in NETWORK_STEPS or s["run"].startswith("uv sync"):
            continue
        condition = s.get("if")
        if condition:
            match = _CONDITION.match(condition)
            assert match, f"the simulator cannot evaluate {condition!r}"
            step_id, key, operator, expected = match.groups()
            if (outputs.get(step_id, {}).get(key) == expected) != (operator == "=="):
                continue
        script = s["run"].replace("uv run teaching-hub", CLI)
        assert "uv run" not in script, f"unsupported command in {s['name']!r}"
        output = tmp_path / f"github-output-{n}"
        output.write_text("", encoding="utf-8")
        env = {**os.environ, "GITHUB_OUTPUT": str(output), "GITHUB_STEP_SUMMARY": str(tmp_path / "summary.md"),
               "RUNNER_TEMP": str(runner_temp)}
        proc = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
                              cwd=root, env=env, capture_output=True, text=True)
        log.append(f"--- {s['name']} (exit {proc.returncode})\n{proc.stdout}{proc.stderr}")
        if "id" in s:
            lines = output.read_text(encoding="utf-8").splitlines()
            outputs[s["id"]] = dict(line.split("=", 1) for line in lines if "=" in line)
        if proc.returncode != 0:
            return False, "\n".join(log)
    return True, "\n".join(log)


@pytest.fixture
def production_repo(tmp_path: Path) -> Path:
    """A repository with production-like content: the fixture with its placeholder identifiers renamed."""
    root = tmp_path / "repo"
    shutil.copytree(FIXTURE, root)
    shutil.copytree(REPO / "renderer", root / "renderer")
    return make_production_like(root)


ALPHA = "content/pl/courses/demo-course-a/task-sets/01-alpha.md"


def _append(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def _broken_page_link(root):
    _append(root, ALPHA, "\nZobacz [opis](missing-page.md).\n")


def _broken_anchor(root):
    _append(root, ALPHA, "\nZobacz [zadanie](#no-such-task).\n")


def _missing_image(root):
    _append(root, ALPHA, "\n![Schemat](diagram.png)\n")


def _removed_published_url(root):
    write(root / "data/published-urls.txt", "/\n/courses/demo-course-a/task-sets/removed-set/\n")


def _draft_in_content(root):
    replace_in(root / ALPHA, "status: published", "status: draft")


def _link_to_a_local_file(root):
    _append(root, ALPHA, "\nZobacz [notatki](file:///Users/someone/notes.md).\n")


def _fixture_identifier(root):
    _append(root, ALPHA, "\nsample-course-a\n")


def _course_without_description(root):
    replace_in(root / "data/courses.yml", '      pl: "Opis zastępczy przedmiotu A."\n', "")
    (root / "content/pl/courses/demo-course-a/index.md").unlink()


def _unknown_repository(root):
    replace_in(root / ALPHA, "repository: python-dev-setup-for-beginners", "repository: no-such-repository")


# case -> (how the content is broken, evidence in the log: any of these). Broken links and anchors are
# reported by the renderer's strict mode first; the artifact check reports them if a renderer does not.
BROKEN = {
    "broken page link": (_broken_page_link, ("page does not exist", "[broken-link]")),
    "broken anchor": (_broken_anchor, ("anchor does not exist", "[broken-anchor]")),
    "missing image": (_missing_image, ("diagram.png",)),
    "removed published URL": (_removed_published_url, ("[url-removed]",)),
    "draft in content": (_draft_in_content, ("[draft-in-content]",)),
    "link to a local file": (_link_to_a_local_file, ("[local-path]",)),
    "placeholder identifier": (_fixture_identifier, ("[forbidden-text]",)),
    "course without description": (_course_without_description, ("[course-not-visible]",)),
    "unknown repository": (_unknown_repository, ("[unknown-repository]",)),
}


@pytest.mark.renderer
def test_valid_production_content_passes_and_is_uploaded(production_repo, tmp_path):
    passed, log = run_production_job(production_repo, tmp_path)
    assert passed, log
    upload = step(PRODUCTION, "Upload production site for manual QA")["with"]["path"].rstrip("/")
    assert (production_repo / upload / "index.html").is_file()
    assert (production_repo / upload / "courses/demo-course-a/task-sets/alpha/index.html").is_file()


@pytest.mark.renderer
@pytest.mark.parametrize("case", sorted(BROKEN))
def test_broken_production_content_fails_the_pull_request(production_repo, tmp_path, case):
    break_content, evidence = BROKEN[case]
    break_content(production_repo)
    passed, log = run_production_job(production_repo, tmp_path)
    assert not passed, log
    assert any(e in log for e in evidence), log


def test_main_without_production_content_is_a_valid_transitional_state(tmp_path):
    root = tmp_path / "repo"
    shutil.copytree(REPO / "renderer", root / "renderer")
    shutil.copytree(REPO / "data/i18n", root / "data/i18n")
    passed, log = run_production_job(root, tmp_path)
    assert passed, log
    assert "No production content" in log
    assert not any(root.glob("_site*"))
