"""Production publishing guards: launch gate, no test fixture, no drafts, correct site URLs."""

import shutil
from pathlib import Path

import pytest

from conftest import FIXTURE, REPO, make_production_like, write
from teaching_hub.check import check_site_urls
from teaching_hub.cli import main
from teaching_hub.production import has_production_content, production_status

PAGE = '<html><head><link rel="canonical" href="{}"></head><body>x</body></html>'


def repo_without_content(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    shutil.copytree(REPO / "renderer", root / "renderer")
    return root


# ---------------------------------------------------------------- launch gate


HOME = "content/pl/home/index.md"
REGISTRY = "data/published-urls.txt"


def test_not_ready_without_an_approved_home_page(tmp_path):
    status = production_status(repo_without_content(tmp_path))
    assert (status.ready, status.error) == (False, False)
    assert "content/pl/home/index.md" in status.reason


def test_ready_once_the_polish_home_page_exists_and_is_registered(tmp_path):
    root = repo_without_content(tmp_path)
    write(root / HOME, "# Home\n")
    write(root / REGISTRY, "/\n/courses/\n")
    status = production_status(root)
    assert (status.ready, status.error) == (True, False)
    assert status.reason == "approved production content found"


def test_launch_requires_the_home_page_in_the_url_registry(tmp_path, capsys):
    # The registry arms the guard below: without "/" in it, losing the home page could go unnoticed.
    root = repo_without_content(tmp_path)
    write(root / HOME, "# Home\n")
    for registry in (None, "/courses/\n"):
        if registry is not None:
            write(root / REGISTRY, registry)
        status = production_status(root)
        assert (status.ready, status.error) == (False, True)
        assert main(["production-status", "--source", str(root)]) == 1
        assert "teaching-hub urls --write" in capsys.readouterr().out


def test_removing_the_home_page_of_a_published_site_is_an_error(tmp_path, capsys):
    # Not a quiet "deployment skipped": the last deployment would stay online with green checks.
    root = repo_without_content(tmp_path)
    write(root / REGISTRY, "/\n/licensing/\n/courses/\n")
    status = production_status(root)
    assert (status.ready, status.error) == (False, True)
    output = tmp_path / "github-output"
    assert main(["production-status", "--source", str(root), "--github-output", str(output)]) == 1
    out = capsys.readouterr().out
    assert "content/pl/home/index.md" in out and "data/published-urls.txt" in out
    assert output.read_text(encoding="utf-8") == "ready=false\ncontent=true\n"


def test_unpublishing_on_purpose_is_reported_explicitly(tmp_path, capsys):
    # The conscious way: remove the home page and its URLs from the registry in the same change.
    root = repo_without_content(tmp_path)
    write(root / REGISTRY, "/courses/\n")
    status = production_status(root)
    assert (status.ready, status.error) == (False, False)
    assert "unpublished" in status.reason and "GitHub Pages" in status.reason
    assert main(["production-status", "--source", str(root)]) == 0
    assert "unpublished" in capsys.readouterr().out


def test_status_command_writes_the_gate_for_github_actions(tmp_path):
    root = repo_without_content(tmp_path)
    output = tmp_path / "github-output"
    assert main(["production-status", "--source", str(root), "--github-output", str(output)]) == 0
    assert output.read_text(encoding="utf-8") == "ready=false\ncontent=false\n"
    write(root / HOME, "# Home\n")
    write(root / REGISTRY, "/\n")
    output.write_text("", encoding="utf-8")
    assert main(["production-status", "--source", str(root), "--github-output", str(output)]) == 0
    assert output.read_text(encoding="utf-8") == "ready=true\ncontent=true\n"


def test_content_without_a_home_page_is_reported_but_does_not_open_the_launch_gate(tmp_path, capsys):
    # CI must check such content even though nothing would be deployed yet.
    root = repo_without_content(tmp_path)
    write(root / "data/courses.yml", "courses: []\n")
    output = tmp_path / "github-output"
    assert main(["production-status", "--source", str(root), "--github-output", str(output)]) == 0
    assert output.read_text(encoding="utf-8") == "ready=false\ncontent=true\n"
    assert "production content: found" in capsys.readouterr().out


# ---------------------------------------------------------------- production content (CI checks)


def test_code_and_interface_strings_alone_are_not_production_content(tmp_path):
    # The state of main before the first publication: renderer configuration and data/i18n only.
    root = repo_without_content(tmp_path)
    shutil.copytree(REPO / "data/i18n", root / "data/i18n")
    write(root / "content/.DS_Store", "")
    assert has_production_content(root) is False


@pytest.mark.parametrize(
    "path",
    [
        "content/pl/home/index.md",
        "content/pl/courses/some-course/task-sets/01-first.md",
        "data/courses.yml",
        "data/repositories.yml",
        "data/third-party.yml",
        "data/published-urls.txt",
        "assets/diagram.svg",
    ],
)
def test_any_page_course_data_or_asset_is_production_content(tmp_path, path):
    root = repo_without_content(tmp_path)
    write(root / path, "x\n")
    assert has_production_content(root) is True


# ---------------------------------------------------------------- production build guards


def test_production_build_refuses_the_test_fixture(tmp_path, capsys):
    code = main(["build", "--production", "--source", str(FIXTURE), "--config-dir", str(REPO / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1
    assert "test fixture" in capsys.readouterr().out
    assert not (tmp_path / "_site").exists()


def test_production_build_refuses_drafts(sample, tmp_path, capsys):
    drafts = tmp_path / "drafts"
    drafts.mkdir()
    code = main(["build", "--production", "--source", str(sample), "--config-dir", str(sample / "renderer"),
                 "--drafts", str(drafts), "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1
    assert "drafts" in capsys.readouterr().out


def test_production_build_rejects_placeholder_content_copied_out_of_the_fixture(sample, tmp_path, capsys):
    # A copy of the fixture outside tests/ passes validation but must still never be published.
    code = main(["build", "--production", "--source", str(sample), "--config-dir", str(sample / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1
    assert "[forbidden-text]" in capsys.readouterr().out


# ---------------------------------------------------------------- site URLs


def test_canonical_and_sitemap_urls_must_use_the_site_url(tmp_path):
    site = tmp_path / "_site"
    write(site / "index.html", PAGE.format("https://michalmaj.github.io/"))
    write(site / "courses/index.html", PAGE.format("https://michalmaj.github.io/courses/"))
    write(site / "en/index.html", PAGE.format("http://127.0.0.1:8000/en/"))
    write(site / "sitemap.xml", "<urlset><url><loc>https://michalmaj.github.io/</loc></url></urlset>")
    write(site / "courses/sitemap.xml", "<urlset><url><loc>https://example.org/courses/</loc></url></urlset>")
    issues = check_site_urls(site, "https://michalmaj.github.io/")
    assert sorted((i.code, i.path) for i in issues) == [
        ("wrong-site-url", "courses/sitemap.xml"),
        ("wrong-site-url", "en/index.html"),
    ]


def test_production_checks_accept_a_real_artifact_once_fixture_identifiers_are_gone(sample, tmp_path):
    # Guards against false positives: canonical links, sitemaps, pages and links of a real Zensical
    # build must pass the production checks. Identifiers are renamed only inside this temporary copy.
    make_production_like(sample)
    assert main(["urls", "--source", str(sample), "--config-dir", str(sample / "renderer"), "--write"]) == 0
    code = main(["build", "--production", "--source", str(sample), "--config-dir", str(sample / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 0
    assert main(["check", "--production", "--site-dir", str(tmp_path / "_site"),
                 "--source", str(sample), "--config-dir", str(sample / "renderer")]) == 0


def test_production_build_requires_every_public_url_in_the_registry(sample, tmp_path, capsys):
    # A page that is not registered could later disappear without the url-removed check noticing.
    make_production_like(sample)
    args = ["--source", str(sample), "--config-dir", str(sample / "renderer")]
    assert main(["urls", *args, "--write"]) == 0
    registry = sample / REGISTRY
    lines = registry.read_text(encoding="utf-8").splitlines()
    registry.write_text("\n".join(u for u in lines if u != "/courses/demo-course-a/task-sets/alpha/") + "\n", encoding="utf-8")
    capsys.readouterr()
    code = main(["build", "--production", *args, "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1
    out = capsys.readouterr().out
    assert "[url-not-registered] /courses/demo-course-a/task-sets/alpha/" in out
    assert "teaching-hub urls --write" in out


def test_production_build_checks_links_to_files_of_the_site_repository(sample, tmp_path, capsys):
    make_production_like(sample)
    args = ["--source", str(sample), "--config-dir", str(sample / "renderer")]
    write(sample / "LICENSE", "MIT\n")
    licensing = sample / "content/pl/home/licensing.md"
    licensing.write_text(
        licensing.read_text(encoding="utf-8")
        + "\n[MIT](https://github.com/michalmaj/michalmaj.github.io/blob/main/LICENSE)"
        + " · [CC BY](https://github.com/michalmaj/michalmaj.github.io/blob/main/LICENSE-CONTENT.md)\n",
        encoding="utf-8",
    )
    assert main(["urls", *args, "--write"]) == 0
    capsys.readouterr()
    site_dir = tmp_path / "_site"
    assert main(["build", "--production", *args, "--build-dir", str(tmp_path / "b"), "--site-dir", str(site_dir)]) == 1
    out = capsys.readouterr().out
    assert "[broken-repository-link]" in out and "LICENSE-CONTENT.md" in out and "blob/main/LICENSE " not in out
    write(sample / "LICENSE-CONTENT.md", "# Teaching Content License\n")
    assert main(["check", "--production", "--site-dir", str(site_dir), *args]) == 0
