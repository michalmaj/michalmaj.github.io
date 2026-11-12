import json
import re
from pathlib import Path

import pytest

from conftest import write
from teaching_hub.check import check_artifact
from teaching_hub.loader import load_site
from teaching_hub.render import RenderError, build_site

pytestmark = pytest.mark.renderer
RENDERERS = ["zensical", "material"]


def _decoded(path: Path) -> str:
    # Decode JSON so \uXXXX escapes (used by Material) compare as real characters.
    return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)


def search_text(site_dir: Path) -> str:
    """Concatenated, decoded text of every search index file in the artifact."""
    files = list(site_dir.rglob("search.json")) + list(site_dir.rglob("search_index.json"))
    assert files, "no search index produced"
    return "\n".join(_decoded(f) for f in files)


@pytest.mark.parametrize("renderer", RENDERERS)
def test_full_build_composes_four_builds_without_artifact_issues(sample, tmp_path, renderer):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    for page in ("index.html", "licensing/index.html", "courses/index.html", "en/index.html",
                 "en/courses/index.html", "courses/sample-course-a/task-sets/alpha/index.html",
                 "en/courses/sample-course-a/task-sets/alpha/index.html"):
        assert (site_dir / page).is_file(), page
    assert check_artifact(site_dir) == []


@pytest.mark.parametrize("renderer", RENDERERS)
def test_task_anchors_survive_rendering(sample, tmp_path, renderer):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    html = (site_dir / "courses/sample-course-a/task-sets/alpha/index.html").read_text(encoding="utf-8")
    for task_id in ("a1", "a2", "a3"):
        assert re.search(rf'<h3 id="{task_id}"', html), task_id


@pytest.mark.parametrize("renderer", RENDERERS)
def test_archived_page_is_published_but_not_searchable(sample, tmp_path, renderer):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    assert (site_dir / "courses/sample-course-a/task-sets/beta/index.html").is_file()
    assert "Zarchiwizowanetestowesłowo" not in search_text(site_dir)


def build_index(site_dir: Path, prefix: str) -> str:
    """Search index of one build: Zensical writes search.json, Material search/search_index.json."""
    for rel in ("search.json", "search/search_index.json"):
        path = site_dir / prefix / rel
        if path.is_file():
            return _decoded(path)
    raise AssertionError(f"no search index under {prefix}")


@pytest.mark.parametrize("renderer", RENDERERS)
def test_search_indexes_are_separate_per_build(sample, tmp_path, renderer):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    text = build_index(site_dir, "courses")
    assert "Temat zastępczy alfa" in text
    assert "Placeholder topic alpha" not in text  # English build has its own index
    assert "Tekst zastępczy strony licencji" not in text  # home space has its own index


def test_root_404_is_bilingual_and_self_contained(sample, tmp_path):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer="zensical")
    html = (site_dir / "404.html").read_text(encoding="utf-8")
    assert "Nie znaleziono strony" in html and "Page not found" in html
    assert 'href="/en/"' in html
    assert "<link" not in html and "<script" not in html  # works at any depth


def test_broken_internal_link_fails_the_build(sample, tmp_path):
    page = sample / "content/pl/courses/sample-course-a/guides/guidelines.md"
    page.write_text(page.read_text(encoding="utf-8") + "\n[x](../task-sets/ghost.md)\n", encoding="utf-8")
    with pytest.raises(RenderError):
        build_site(load_site(sample), tmp_path / "build", tmp_path / "_site", renderer="zensical")


@pytest.mark.parametrize("renderer", RENDERERS)
def test_colour_scheme_preference_is_stored_in_one_scope_for_all_builds(sample, tmp_path, renderer):
    # The theme stores the visitor's colour scheme under a key prefixed with its storage scope.
    # One scope for every build (/, /courses/, /en/, /en/courses/) means one shared preference.
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    scopes = {}
    for prefix in ("", "courses/", "en/", "en/courses/"):
        html = (site_dir / prefix / "index.html").read_text(encoding="utf-8")
        match = re.search(r'__md_scope=new URL\("([^"]*)"', html)
        assert match, f"no storage scope in /{prefix}"
        scopes[f"/{prefix}"] = match.group(1)
    assert scopes == {"/": "/", "/courses/": "/", "/en/": "/", "/en/courses/": "/"}
