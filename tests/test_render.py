import json
from html.parser import HTMLParser
import re
from pathlib import Path

import pytest

from conftest import write
from teaching_hub.check import check_anchor_aliases, check_artifact, check_sitemap
from teaching_hub.loader import load_site
from teaching_hub.render import RenderError, build_site
from teaching_hub.urls import public_urls

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
    assert "<script" not in html and "stylesheet" not in html  # works at any depth
    icons = re.findall(r'<link rel="icon" href="([^"]+)"', html)
    assert icons == ["/assets/images/favicon.png"]  # absolute, so it also works at any depth
    assert (site_dir / icons[0].lstrip("/")).is_file()


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


@pytest.mark.parametrize("renderer", RENDERERS)
def test_heading_ids_keep_polish_letters_and_published_anchors_still_lead_to_them(sample, tmp_path, renderer):
    write(sample / "data/anchor-aliases.yml", "aliases:\n  - {page: /, anchor: strona-gowna, target: strona-glowna}\n")
    site = load_site(sample)
    site_dir = tmp_path / "_site"
    build_site(site, tmp_path / "build", site_dir, renderer=renderer)
    html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert re.search(r'<h1 id="strona-glowna"[^>]*><span id="strona-gowna" class="th-anchor-alias"></span>Strona główna', html)
    assert check_anchor_aliases(site_dir, site.anchor_aliases) == []
    index = build_index(site_dir, "")
    assert "strona-glowna" in index and "th-anchor-alias" not in index and "strona-gowna" not in index


@pytest.mark.parametrize("renderer", RENDERERS)
def test_one_sitemap_lists_the_whole_site_and_robots_txt_points_to_it(sample, tmp_path, renderer):
    site = load_site(sample)
    site_dir = tmp_path / "_site"
    build_site(site, tmp_path / "build", site_dir, renderer=renderer)
    assert sorted(p.relative_to(site_dir).as_posix() for p in site_dir.rglob("sitemap*")) == ["sitemap.xml"]
    locs = re.findall(r"<loc>([^<]+)</loc>", (site_dir / "sitemap.xml").read_text(encoding="utf-8"))
    assert sorted(locs) == sorted("https://michalmaj.github.io" + u for u in public_urls(site))
    assert "Sitemap: https://michalmaj.github.io/sitemap.xml" in (site_dir / "robots.txt").read_text(encoding="utf-8").splitlines()
    assert check_sitemap(site_dir, site.settings["site_url"], public_urls(site)) == []


@pytest.mark.parametrize("renderer", RENDERERS)
def test_only_the_root_404_page_is_published(sample, tmp_path, renderer):
    # GitHub Pages serves /404.html for every missing path; the builds' own 404 pages are never used.
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    assert sorted(p.relative_to(site_dir).as_posix() for p in site_dir.rglob("404.html")) == ["404.html"]


class _Navigation(HTMLParser):
    """Section toggles of the theme: <label for="__nav_N">, its checkbox and the list it controls."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.toggles: list[dict] = []
        self.checkboxes: set[str] = set()
        self.labelled_navs: set[str] = set()
        self.scripts: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "label" and "md-nav__link" in (a.get("class") or "").split() and (a.get("for") or "").startswith("__nav_"):
            self.toggles.append(a)
        elif tag == "input" and a.get("type") == "checkbox" and a.get("id"):
            self.checkboxes.add(a["id"])
        elif tag == "nav" and a.get("aria-labelledby"):
            self.labelled_navs.add(a["aria-labelledby"])
        elif tag == "script" and a.get("src"):
            self.scripts.append(a["src"])


@pytest.mark.parametrize("renderer", RENDERERS)
def test_navigation_script_finds_the_section_toggles_it_makes_accessible(sample, tmp_path, renderer):
    # navigation.js relies on this markup; a theme upgrade that changes it must fail here.
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    page = _Navigation()
    page.feed((site_dir / "courses/sample-course-a/index.html").read_text(encoding="utf-8"))
    assert any(src.endswith("javascripts/teaching-hub/navigation.js") for src in page.scripts)
    assert page.toggles, "no section toggle in the navigation"
    for toggle in page.toggles:
        assert toggle["for"] in page.checkboxes
        assert toggle.get("id") in page.labelled_navs
