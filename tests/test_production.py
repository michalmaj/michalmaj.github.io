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


def test_not_ready_without_an_approved_home_page(tmp_path):
    ready, reason = production_status(repo_without_content(tmp_path))
    assert ready is False
    assert "content/pl/home/index.md" in reason


def test_ready_once_the_polish_home_page_exists(tmp_path):
    root = repo_without_content(tmp_path)
    write(root / "content/pl/home/index.md", "# Home\n")
    assert production_status(root) == (True, "approved production content found")


def test_status_command_writes_the_gate_for_github_actions(tmp_path):
    root = repo_without_content(tmp_path)
    output = tmp_path / "github-output"
    assert main(["production-status", "--source", str(root), "--github-output", str(output)]) == 0
    assert output.read_text(encoding="utf-8") == "ready=false\ncontent=false\n"
    write(root / "content/pl/home/index.md", "# Home\n")
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
    code = main(["build", "--production", "--source", str(sample), "--config-dir", str(sample / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 0
    assert main(["check", "--production", "--site-dir", str(tmp_path / "_site"),
                 "--source", str(sample), "--config-dir", str(sample / "renderer")]) == 0
