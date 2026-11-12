from pathlib import Path

import pytest
import yaml

from conftest import write
from teaching_hub.assemble import PreviewNotAllowed, assemble
from teaching_hub.loader import load_site

ALPHA_EN = "content/en/courses/sample-course-a/task-sets/01-alpha.md"


def build(root: Path, tmp_path: Path, drafts: Path | None = None, include_drafts: bool = False):
    out = tmp_path / "build"
    builds = assemble(load_site(root, drafts=drafts), out, include_drafts=include_drafts)
    return out, {(b.lang, b.space): b for b in builds}


def page(out: Path, lang: str, space: str, rel: str) -> str:
    return (out / lang / space / "docs" / rel).read_text(encoding="utf-8")


def config(out: Path, lang: str, space: str) -> dict:
    return yaml.safe_load((out / lang / space / "mkdocs.yml").read_text(encoding="utf-8"))


def all_generated_text(out: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in out.rglob("*") if p.is_file())


def test_only_enabled_spaces_with_content_are_built(sample, tmp_path):
    out, builds = build(sample, tmp_path)
    assert set(builds) == {("pl", "home"), ("pl", "courses"), ("en", "home"), ("en", "courses")}
    assert not any(out.rglob("for-employers*"))


def test_english_course_space_is_skipped_without_a_visible_course(sample, tmp_path):
    (sample / ALPHA_EN).unlink()
    out, builds = build(sample, tmp_path)
    assert ("en", "courses") not in builds
    assert "/en/courses/" not in page(out, "en", "home", "index.md")


def test_home_links_only_to_spaces_with_content(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    home = page(out, "pl", "home", "index.md")
    assert "](/courses/)" in home
    assert "for-employers" not in all_generated_text(out)


def test_invisible_course_gets_no_page(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    catalog = page(out, "pl", "courses", "index.md")
    assert "sample-course-b/index.md" in catalog
    assert "sample-course-c" not in catalog
    assert not (out / "pl/courses/docs/sample-course-c").exists()


def test_catalog_lists_courses_in_catalog_order(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    catalog = page(out, "pl", "courses", "index.md")
    assert catalog.index("sample-course-a/index.md") < catalog.index("sample-course-b/index.md")


def test_task_set_page_is_numbered_and_keeps_task_anchors(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    assert "# Zestaw 1 · Temat zastępczy alfa" in alpha
    assert "### Zadanie 1. Tytuł zastępczy zadania pierwszego {#a1}" in alpha
    assert "### Zadanie 2. Tytuł zastępczy zadania drugiego {#a2}" in alpha
    assert "### Zadanie 3. Tytuł zastępczy zadania dodatkowego (opcjonalne) {#a3}" in alpha
    assert "### To nie jest zadanie, tylko blok kodu" in alpha  # code block untouched


def _line_with(text: str, needle: str) -> str:
    lines = [line for line in text.splitlines() if needle in line]
    assert len(lines) == 1, f"expected one line with {needle!r}, got {lines}"
    return lines[0]


def test_task_materials_are_rendered_below_their_task(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    setup = "https://github.com/michalmaj/python-dev-setup-for-beginners/blob/main/docs/00_start_here.md"
    assert alpha.index("{#a2}") < alpha.index(setup) < alpha.index("{#a3}")
    assert _line_with(alpha, setup).endswith("· EN")


def test_material_with_tag_links_to_tree_and_shows_the_ref(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    line = _line_with(alpha, "https://github.com/michalmaj/mechatronic-systems-programming/tree/module-01-start/src)")
    assert "`module-01-start`" in line


def test_maturity_is_shown_only_when_assessed_as_notable(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    assert "w rozbudowie" in _line_with(alpha, "deep-learning/blob/main/lectures/01_intro/lecture.md")
    assert "w rozbudowie" not in _line_with(alpha, "software-engineering-in-practice/blob/main/START-HERE.pl.md")


def test_set_materials_section_is_inserted_before_tasks(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    start_here = "software-engineering-in-practice/blob/main/START-HERE.pl.md"
    assert alpha.index("## Materiały") < alpha.index(start_here) < alpha.index("## Zadania")


def test_archived_set_keeps_its_page_but_leaves_nav_lists_and_search(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    beta = page(out, "pl", "courses", "sample-course-a/task-sets/beta.md")
    assert beta.startswith("---\nsearch:\n  exclude: true\n---\n")
    assert '!!! warning "Zarchiwizowane"' in beta
    assert "](alpha.md)" in beta  # replaced_by link
    cfg = config(out, "pl", "courses")
    assert "sample-course-a/task-sets/beta.md" not in yaml.safe_dump(cfg["nav"])
    assert "/sample-course-a/task-sets/beta.md" in cfg["not_in_nav"]
    assert "task-sets/beta.md" not in page(out, "pl", "courses", "sample-course-a/index.md")


def test_language_switch_points_to_translation_or_other_home(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    assert "](/en/courses/sample-course-a/task-sets/alpha/)" in alpha
    guide = page(out, "pl", "courses", "sample-course-a/guides/guidelines.md")
    assert "](/en/)" in guide
    alpha_en = page(out, "en", "courses", "sample-course-a/task-sets/alpha.md")
    assert "](/courses/sample-course-a/task-sets/alpha/)" in alpha_en


def test_footer_links_to_licensing_page_of_the_same_language(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    assert 'href="/licensing/"' in config(out, "pl", "courses")["copyright"]
    assert 'href="/en/licensing/"' in config(out, "en", "courses")["copyright"]


def test_generated_config_targets_the_build_prefix(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    cfg = config(out, "en", "courses")
    assert cfg["site_url"] == "https://michalmaj.github.io/en/courses/"
    assert cfg["theme"]["language"] == "en"
    assert cfg["theme"]["font"] is False
    assert config(out, "pl", "home")["site_url"] == "https://michalmaj.github.io/"


def test_course_page_lists_repositories_used_by_published_material(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    course = page(out, "pl", "courses", "sample-course-a/index.md")
    assert "## Wykorzystywane materiały" in course
    for name in ("Software Engineering in Practice", "Deep Learning", "Python Dev Setup for Beginners"):
        assert f"[{name}](" in course


def test_licensing_page_lists_licenses_of_linked_repositories(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    licensing = page(out, "pl", "home", "licensing.md")
    assert "| [Deep Learning](https://github.com/michalmaj/deep-learning) | MIT | CC-BY-SA-4.0 |" in licensing
    assert "## Materiały osób trzecich" in licensing


DRAFT = """---
title: "Szkic zastępczy"
---

## Zadania

### Zadanie szkicu {#d1}

Szkicowetestowesłowo.
"""


def test_drafts_are_absent_unless_previewed(sample, tmp_path):
    drafts = tmp_path / "private" / "drafts"
    write(drafts / "pl/courses/sample-course-a/task-sets/05-draft-x.md", DRAFT)
    out, _ = build(sample, tmp_path)
    assert "Szkicowetestowesłowo" not in all_generated_text(out)

    out_preview, _ = build(sample, tmp_path / "preview", drafts=drafts, include_drafts=True)
    draft_page = page(out_preview, "pl", "courses", "sample-course-a/task-sets/draft-x.md")
    assert '!!! danger "SZKIC"' in draft_page


def test_preview_is_refused_in_ci(sample, tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    with pytest.raises(PreviewNotAllowed):
        build(sample, tmp_path, include_drafts=True)
