from pathlib import Path

from conftest import write
from teaching_hub.check import check_anchor_aliases, check_artifact, check_repository_links, check_tracked_paths
from teaching_hub.models import AnchorAlias

PAGE = '<html lang="pl"><body>{}</body></html>'


def make_site(tmp_path: Path, pages: dict[str, str]) -> Path:
    site = tmp_path / "_site"
    write(site / "404.html", PAGE.format("404"))
    for rel, body in pages.items():
        write(site / rel, PAGE.format(body) if rel.endswith(".html") else body)
    return site


def codes(issues) -> list[str]:
    return sorted(i.code for i in issues)


def test_consistent_site_has_no_issues(tmp_path):
    site = make_site(tmp_path, {
        "index.html": '<a href="/courses/">c</a> <a href="/courses/a/#t1">t</a>',
        "courses/index.html": '<a href="a/">a</a> <a href="../">home</a> <a href="https://github.com/x">gh</a>',
        "courses/a/index.html": '<h3 id="t1">T</h3> <a href="#t1">self</a> <a href="/licensing/">lic</a>',
        "licensing/index.html": "lic",
    })
    assert codes(check_artifact(site)) == []


def test_link_to_missing_page_is_reported(tmp_path):
    site = make_site(tmp_path, {"index.html": '<a href="/courses/missing/">x</a>'})
    assert codes(check_artifact(site)) == ["broken-link"]


def test_relative_link_is_resolved_from_the_page_directory(tmp_path):
    site = make_site(tmp_path, {
        "courses/a/index.html": '<a href="../b/">b</a>',
        "courses/b/index.html": "b",
        "courses/c/index.html": '<a href="b/">wrong: resolves to /courses/c/b/</a>',
    })
    issues = check_artifact(site)
    assert [(i.code, i.path) for i in issues] == [("broken-link", "courses/c/index.html")]


def test_link_to_missing_anchor_is_reported(tmp_path):
    site = make_site(tmp_path, {
        "index.html": '<a href="/a/#nope">x</a> <a href="#also-nope">y</a>',
        "a/index.html": '<h2 id="yes">y</h2>',
    })
    assert codes(check_artifact(site)) == ["broken-anchor", "broken-anchor"]


def test_resources_loaded_from_third_parties_are_reported(tmp_path):
    site = make_site(tmp_path, {
        "index.html": (
            '<link rel="canonical" href="https://michalmaj.github.io/">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">'
            '<script src="https://cdn.example.org/x.js"></script>'
            '<a href="https://docs.example.org/">a plain outbound link is fine</a>'
        ),
        "assets/style.css": "@import url(https://fonts.example.org/a.css); body{background:url(/assets/x.png)}",
    })
    issues = check_artifact(site)
    assert codes(issues) == ["external-request", "external-request", "external-request"]


def test_course_pages_must_not_link_to_the_employer_space(tmp_path):
    site = make_site(tmp_path, {
        "for-employers/index.html": "e",
        "en/for-employers/index.html": "e",
        "courses/index.html": '<a href="/for-employers/">x</a>',
        "en/courses/index.html": '<a href="/en/for-employers/">x</a>',
        "index.html": '<a href="/for-employers/">home may link to every space</a>',
    })
    issues = [i for i in check_artifact(site, disabled_spaces=()) if i.code == "cross-space-link"]
    assert sorted(i.path for i in issues) == ["courses/index.html", "en/courses/index.html"]


def test_output_of_a_disabled_space_is_reported(tmp_path):
    site = make_site(tmp_path, {"for-employers/index.html": "e"})
    assert "disabled-space-output" in codes(check_artifact(site, disabled_spaces=("for-employers",)))


def test_forbidden_text_anywhere_in_the_artifact_is_reported(tmp_path):
    site = make_site(tmp_path, {"courses/search.json": '{"items":[{"text":"Szkicowetestowesłowo"}]}'})
    issues = check_artifact(site, forbidden=["Szkicowetestowesłowo"])
    assert [(i.code, i.path) for i in issues] == [("forbidden-text", "courses/search.json")]


def test_forbidden_text_is_found_in_json_with_escaped_unicode(tmp_path):
    # MkDocs Material writes search_index.json with \uXXXX escapes ("ł" -> "ł").
    site = make_site(tmp_path, {"courses/search/search_index.json": '{"docs":[{"text":"Szkicowetestowes\\u0142owo"}]}'})
    issues = check_artifact(site, forbidden=["Szkicowetestowesłowo"])
    assert [(i.code, i.path) for i in issues] == [("forbidden-text", "courses/search/search_index.json")]


def test_missing_root_404_page_is_reported(tmp_path):
    site = make_site(tmp_path, {"index.html": "x"})
    (site / "404.html").unlink()
    assert codes(check_artifact(site)) == ["missing-404"]


def test_private_files_in_the_artifact_are_reported(tmp_path):
    site = make_site(tmp_path, {
        "index.html": "ok",
        "ARCHITECTURE.md": "x",
        "assets/notes.private.md": "x",
        "courses/CLAUDE.md": "x",
        "courses/drafts/pl/x.md": "x",
    })
    flagged = sorted(i.path for i in check_artifact(site) if i.code == "private-file-published")
    assert flagged == ["ARCHITECTURE.md", "assets/notes.private.md", "courses/CLAUDE.md", "courses/drafts/pl/x.md"]


def test_private_files_must_not_be_tracked():
    tracked = [
        "README.md",
        "ARCHITECTURE.md",
        "drafts/pl/courses/x/task-sets/01-y.md",
        ".claude/settings.json",
        "docs/CLAUDE.md",
        "notes.private.md",
        "content/pl/home/index.md",
    ]
    flagged = sorted(i.path for i in check_tracked_paths(tracked))
    assert flagged == [".claude/settings.json", "ARCHITECTURE.md", "docs/CLAUDE.md",
                       "drafts/pl/courses/x/task-sets/01-y.md", "notes.private.md"]


# ---------------------------------------------------------------- links to the site's own repository

SITE_REPO = "https://github.com/michalmaj/michalmaj.github.io"


def test_links_to_files_of_the_site_repository_must_exist_in_the_source(tmp_path):
    # e.g. the licensing page links LICENSE and LICENSE-CONTENT.md on GitHub: the published link only
    # works if the deployed commit contains the file, so the file must be in the source being built.
    source = tmp_path / "source"
    write(source / "LICENSE", "MIT\n")
    write(source / "docs/notes/a.md", "x\n")
    site = make_site(tmp_path, {"licensing/index.html": "".join([
        f'<a href="{SITE_REPO}/blob/main/LICENSE">ok</a>',
        f'<a href="{SITE_REPO}/blob/main/LICENSE#L3">ok with fragment</a>',
        f'<a href="{SITE_REPO}/tree/main/docs/notes">ok directory</a>',
        f'<a href="{SITE_REPO}/blob/main/LICENSE-CONTENT.MD">typo</a>',
        f'<a href="{SITE_REPO}/tree/main/missing">missing directory</a>',
        f'<a href="{SITE_REPO}/blob/main/docs/notes">directory linked as a file</a>',
        f'<a href="{SITE_REPO}/issues">not a file</a>',
        '<a href="https://github.com/michalmaj/other-repository/blob/main/NOPE">another repository</a>',
    ])})
    issues = check_repository_links(site, SITE_REPO, source)
    assert {i.code for i in issues} == {"broken-repository-link"}
    assert sorted(i.message.split(" ")[0] for i in issues) == [
        "blob/main/LICENSE-CONTENT.MD", "blob/main/docs/notes", "tree/main/missing",
    ]


def test_repository_links_to_other_branches_are_not_checked_against_the_source(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    site = make_site(tmp_path, {"index.html": f'<a href="{SITE_REPO}/blob/gh-pages/x.txt">x</a>'})
    assert check_repository_links(site, SITE_REPO, source) == []


def test_repository_links_are_case_sensitive_like_github(tmp_path):
    # macOS and Windows file systems ignore case; GitHub does not.
    source = tmp_path / "source"
    write(source / "LICENSE-CONTENT.md", "x\n")
    site = make_site(tmp_path, {"licensing/index.html": f'<a href="{SITE_REPO}/blob/main/LICENSE-CONTENT.MD">x</a>'})
    assert [i.code for i in check_repository_links(site, SITE_REPO, source)] == ["broken-repository-link"]


def test_anchor_alias_needs_both_anchors_on_its_page(tmp_path):
    site = tmp_path / "_site"
    write(site / "index.html", '<h1 id="new"><span id="old" class="th-anchor-alias"></span>Tytuł</h1>')
    write(site / "licensing/index.html", '<h2 id="new2">Tytuł</h2>')
    aliases = [
        AnchorAlias(page="/", anchor="old", target="new"),
        AnchorAlias(page="/licensing/", anchor="old2", target="new2"),
        AnchorAlias(page="/gone/", anchor="a", target="b"),
    ]
    issues = check_anchor_aliases(site, aliases)
    assert sorted((i.code, i.path) for i in issues) == [("broken-anchor-alias", "/gone/"), ("broken-anchor-alias", "/licensing/")]
