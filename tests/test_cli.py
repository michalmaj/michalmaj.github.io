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


def test_check_tracked_flags_private_files(tmp_path, capsys):
    listing = tmp_path / "tracked.txt"
    listing.write_text("README.md\nARCHITECTURE.md\n", encoding="utf-8")
    assert main(["check-tracked", "--from-file", str(listing)]) == 1
    assert "ARCHITECTURE.md" in capsys.readouterr().out
