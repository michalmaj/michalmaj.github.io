from conftest import replace_in
from teaching_hub.cli import main

ALPHA_PL = "content/pl/courses/sample-course-a/task-sets/01-alpha.md"


def test_validate_exit_code_reflects_errors(sample):
    assert main(["validate", "--source", str(sample)]) == 0
    replace_in(sample / ALPHA_PL, "status: published", "status: draft")
    assert main(["validate", "--source", str(sample)]) == 1


def test_build_stops_before_rendering_when_validation_fails(sample, tmp_path):
    replace_in(sample / ALPHA_PL, "## Zadania", "## Inne")
    site_dir = tmp_path / "_site"
    code = main(["build", "--source", str(sample), "--build-dir", str(tmp_path / "b"), "--site-dir", str(site_dir)])
    assert code == 1
    assert not site_dir.exists()


def test_build_reads_renderer_config_separately_from_the_content_source(tmp_path):
    # The fixture itself has no renderer/; the site's renderer/ is passed explicitly.
    import shutil

    from conftest import FIXTURE, REPO

    source = tmp_path / "content-only"
    shutil.copytree(FIXTURE, source)
    site_dir = tmp_path / "_site"
    code = main(["build", "--source", str(source), "--config-dir", str(REPO / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(site_dir)])
    assert code == 0
    assert (site_dir / "courses/sample-course-a/task-sets/alpha/index.html").is_file()


DRAFT_MARKER_PL = "Podgląd lokalny. Ta strona nie jest publikowana."  # draft_text in data/i18n/pl.yml


def test_build_fails_when_a_draft_marker_reaches_the_artifact(sample, tmp_path):
    guide = sample / "content/pl/courses/sample-course-a/guides/guidelines.md"
    guide.write_text(guide.read_text(encoding="utf-8") + f"\n{DRAFT_MARKER_PL}\n", encoding="utf-8")
    code = main(["build", "--source", str(sample), "--config-dir", str(sample / "renderer"),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1


def test_check_command_uses_draft_markers_from_the_source(sample, tmp_path):
    site_dir = tmp_path / "_site"
    args = ["--source", str(sample), "--config-dir", str(sample / "renderer")]
    assert main(["build", *args, "--build-dir", str(tmp_path / "b"), "--site-dir", str(site_dir)]) == 0
    assert main(["check", "--site-dir", str(site_dir), *args]) == 0
    page = site_dir / "courses/index.html"
    page.write_text(page.read_text(encoding="utf-8") + DRAFT_MARKER_PL, encoding="utf-8")
    assert main(["check", "--site-dir", str(site_dir), *args]) == 1


def test_draft_preview_in_ci_fails_cleanly(sample, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    drafts = tmp_path / "drafts"
    drafts.mkdir()
    code = main(["build", "--source", str(sample), "--config-dir", str(sample / "renderer"), "--drafts", str(drafts),
                 "--build-dir", str(tmp_path / "b"), "--site-dir", str(tmp_path / "_site")])
    assert code == 1
    assert "refused in CI" in capsys.readouterr().out
    assert not (tmp_path / "_site").exists()


def test_check_reports_public_pages_missing_from_the_artifact(sample, tmp_path, capsys):
    site_dir = tmp_path / "_site"
    args = ["--source", str(sample), "--config-dir", str(sample / "renderer")]
    assert main(["build", *args, "--build-dir", str(tmp_path / "b"), "--site-dir", str(site_dir)]) == 0
    (site_dir / "en/courses/sample-course-a/task-sets/alpha/index.html").unlink()
    assert main(["check", "--site-dir", str(site_dir), *args]) == 1
    out = capsys.readouterr().out
    assert "[missing-page] /en/courses/sample-course-a/task-sets/alpha/" in out


def test_check_tracked_flags_private_files(tmp_path, capsys):
    listing = tmp_path / "tracked.txt"
    listing.write_text("README.md\nARCHITECTURE.md\n", encoding="utf-8")
    assert main(["check-tracked", "--from-file", str(listing)]) == 1
    assert "ARCHITECTURE.md" in capsys.readouterr().out


def test_repositories_command_lists_only_repositories_referenced_by_materials(sample, capsys):
    # CI clones exactly these to check that every repository/ref/path in the content exists.
    registry = sample / "data/repositories.yml"
    registry.write_text(
        registry.read_text(encoding="utf-8")
        + "  - id: unused-repository\n    name: Unused\n"
        + "    url: https://github.com/michalmaj/unused-repository\n    default_branch: main\n",
        encoding="utf-8",
    )
    assert main(["repositories", "--source", str(sample), "--config-dir", str(sample / "renderer")]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "software-engineering-in-practice https://github.com/michalmaj/software-engineering-in-practice",
        "mechatronic-systems-programming https://github.com/michalmaj/mechatronic-systems-programming",
        "deep-learning https://github.com/michalmaj/deep-learning",
        "python-dev-setup-for-beginners https://github.com/michalmaj/python-dev-setup-for-beginners",
    ]
