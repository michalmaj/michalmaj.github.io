import re
from pathlib import Path

import pytest
import yaml

from conftest import replace_in, write
from teaching_hub.assemble import PreviewNotAllowed, assemble
from teaching_hub.loader import load_site

ALPHA_EN = "content/en/courses/sample-course-a/task-sets/01-alpha.md"


def build(root: Path, tmp_path: Path, drafts: Path | None = None, include_drafts: bool = False):
    out = tmp_path / "build"
    builds = assemble(load_site(root, drafts=drafts), out, include_drafts=include_drafts)
    return out, {(b.lang, b.space): b for b in builds}


def page(out: Path, lang: str, space: str, rel: str) -> str:
    return (out / lang / space / "docs" / rel).read_text(encoding="utf-8")


class _ConfigLoader(yaml.SafeLoader):
    """Reads renderer configs: `!!python/name:` values become their dotted names."""


_ConfigLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", lambda loader, suffix, node: f"python:{suffix}")


def config(out: Path, lang: str, space: str) -> dict:
    return yaml.load((out / lang / space / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_ConfigLoader)


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
    assert "### Zadanie 3. Tytuł zastępczy zadania dodatkowego " + OPTIONAL_BADGE + " {#a3}" in alpha
    assert "### To nie jest zadanie, tylko blok kodu" in alpha  # code block untouched


# The parentheses are visually hidden; screen readers and the table of contents read "(opcjonalne)".
OPTIONAL_BADGE = '<span class="th-badge th-badge--optional"><span class="th-sr">(</span>opcjonalne<span class="th-sr">)</span></span>'
LANG_BADGE_EN = '<span class="th-badge th-badge--lang"><span class="th-sr">Język materiału: </span>EN</span>'


def _line_with(text: str, needle: str) -> str:
    lines = [line for line in text.splitlines() if needle in line]
    assert len(lines) == 1, f"expected one line with {needle!r}, got {lines}"
    return lines[0]


def test_task_materials_are_rendered_below_their_task(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    setup = "https://github.com/michalmaj/python-dev-setup-for-beginners/blob/main/docs/00_start_here.md"
    assert alpha.index("{#a2}") < alpha.index(setup) < alpha.index("{#a3}")
    assert LANG_BADGE_EN in _line_with(alpha, setup)


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
    assert re.search(r"^## (<span [^>]*></span>)?Materiały osób trzecich$", licensing, re.M)


def test_licensing_table_names_every_column(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    assert "| Repozytorium | Kod | Treści |" in page(out, "pl", "home", "licensing.md")
    assert "| Repository | Code | Content |" in page(out, "en", "home", "licensing.md")


# ---------------------------------------------------------------- heading anchors


def test_every_build_makes_heading_ids_with_the_site_slugify(sample, tmp_path):
    out, builds = build(sample, tmp_path)
    for lang, space in builds:
        toc = [e["toc"] for e in config(out, lang, space)["markdown_extensions"] if isinstance(e, dict) and "toc" in e]
        assert toc == [{"permalink": True, "slugify": "python:teaching_hub.slugs.slugify"}], (lang, space)


ALIASES = """aliases:
  - page: /
    anchor: strona-gowna
    target: strona-glowna
  - page: /licensing/
    anchor: materiay-osob-trzecich
    target: materialy-osob-trzecich
  - page: /courses/sample-course-a/
    anchor: wykorzystywane-materiay
    target: wykorzystywane-materialy
"""
ALIAS = '<span id="{}" class="th-anchor-alias"></span>'


def test_published_anchors_that_changed_stay_on_their_headings(sample, tmp_path):
    write(sample / "data/anchor-aliases.yml", ALIASES)
    out, _ = build(sample, tmp_path)
    assert "# " + ALIAS.format("strona-gowna") + "Strona główna" in page(out, "pl", "home", "index.md")
    assert "## " + ALIAS.format("materiay-osob-trzecich") + "Materiały osób trzecich" in page(out, "pl", "home", "licensing.md")
    assert "## " + ALIAS.format("wykorzystywane-materiay") + "Wykorzystywane materiały" in page(
        out, "pl", "courses", "sample-course-a/index.md")
    assert "th-anchor-alias" not in page(out, "en", "home", "index.md")


def test_headings_get_no_aliases_without_the_alias_registry(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    assert "th-anchor-alias" not in all_generated_text(out)


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


@pytest.mark.parametrize("variable", ["CI", "GITHUB_ACTIONS"])
def test_preview_is_refused_in_ci(sample, tmp_path, monkeypatch, variable):
    monkeypatch.setenv(variable, "true")
    with pytest.raises(PreviewNotAllowed):
        build(sample, tmp_path, include_drafts=True)


# ---------------------------------------------------------------- presentation hooks (CSS classes only)


@pytest.mark.parametrize(
    "lang,space,rel,kind",
    [
        ("pl", "home", "index.md", "home"),
        ("pl", "home", "licensing.md", "licensing"),
        ("pl", "courses", "index.md", "catalog"),
        ("pl", "courses", "sample-course-a/index.md", "course"),
        ("pl", "courses", "sample-course-a/task-sets/alpha.md", "task-set"),
        ("pl", "courses", "sample-course-a/guides/guidelines.md", "guide"),
    ],
)
def test_every_generated_page_carries_its_page_type(sample, tmp_path, lang, space, rel, kind):
    out, _ = build(sample, tmp_path)
    assert f'<div class="th-page" data-th-page="{kind}" hidden></div>' in page(out, lang, space, rel)


def test_catalog_renders_each_visible_course_as_a_card(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    catalog = page(out, "pl", "courses", "index.md")
    assert '<div class="th-cards" markdown>' in catalog
    assert '<div class="th-card" markdown>\n\n## [Przedmiot przykładowy A](sample-course-a/index.md)' in catalog
    assert catalog.count('<div class="th-card" markdown>') == 2


def test_course_page_renders_task_sets_as_cards_with_their_number(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    course = page(out, "pl", "courses", "sample-course-a/index.md")
    card = course[course.index('<div class="th-card th-card--set" markdown>'):]
    assert '<p class="th-eyebrow">Zestaw 1</p>' in card
    assert "### [Temat zastępczy alfa](task-sets/alpha.md)" in card


def test_breadcrumbs_are_a_labelled_navigation_landmark_above_the_title(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    alpha = page(out, "pl", "courses", "sample-course-a/task-sets/alpha.md")
    nav = '<nav class="th-breadcrumbs" aria-label="Ścieżka nawigacji" markdown="span">'
    assert nav in alpha
    assert alpha.index(nav) < alpha.index("# Zestaw 1 · Temat zastępczy alfa")


def test_home_space_entries_are_cards_linking_to_the_space(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    home = page(out, "pl", "home", "index.md")
    assert '<div class="th-card th-card--space" markdown>' in home
    assert "## [Dla studentów](/courses/)" in home


def test_theme_stylesheets_are_copied_into_every_build_and_linked(sample, tmp_path):
    out, builds = build(sample, tmp_path)
    for lang, space in builds:
        docs = out / lang / space / "docs" / "stylesheets" / "teaching-hub"
        assert (docs / "tokens.css").is_file() and (docs / "theme.css").is_file()
        assert config(out, lang, space)["extra_css"][:2] == [
            "stylesheets/teaching-hub/tokens.css",
            "stylesheets/teaching-hub/theme.css",
        ]


def test_space_specific_stylesheet_is_linked_only_in_that_space(sample, tmp_path):
    (sample / "renderer/theme/space-courses.css").write_text(":root { --th-accent: #000000; }\n", encoding="utf-8")
    out, _ = build(sample, tmp_path)
    assert "stylesheets/teaching-hub/space-courses.css" in config(out, "pl", "courses")["extra_css"]
    assert "stylesheets/teaching-hub/space-courses.css" not in config(out, "pl", "home")["extra_css"]


def test_colour_scheme_toggle_is_labelled_in_the_page_language(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    for lang, expected in (("pl", "Przełącz na jasny motyw"), ("en", "Switch to light theme")):
        palette = config(out, lang, "courses")["theme"]["palette"]
        assert [entry.get("scheme") for entry in palette] == [None, "default", "slate"]
        assert palette[0]["toggle"]["name"] == expected


# ---------------------------------------------------------------- course visibility: name + description + published material


def test_course_with_a_description_but_no_published_material_is_not_published(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    assert "sample-course-d" not in page(out, "pl", "courses", "index.md")
    assert not (out / "pl/courses/docs/sample-course-d").exists()


def test_a_published_guide_is_enough_material(sample, tmp_path):
    out, _ = build(sample, tmp_path)
    assert "sample-course-b/index.md" in page(out, "pl", "courses", "index.md")
    assert (out / "pl/courses/docs/sample-course-b/guides/overview.md").is_file()


def test_course_needs_a_description_in_each_language(sample, tmp_path):
    replace_in(sample / "data/courses.yml", '      en: "Placeholder description of course A."\n', "")
    out, builds = build(sample, tmp_path)
    assert ("en", "courses") not in builds  # no English course is complete any more
    assert "/en/courses/" not in page(out, "en", "home", "index.md")
