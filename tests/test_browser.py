"""Keyboard and assistive-technology behaviour of the navigation, in a real browser.

Opt-in: set TEACHING_HUB_CHROME to a Chrome or Chromium binary (Node.js 22+ must be on PATH), e.g.
TEACHING_HUB_CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" uv run pytest tests/test_browser.py
Without it the tests are skipped, so the suite and CI do not depend on a browser.
"""

import functools
import http.server
import json
import os
import shutil
import subprocess
import threading
from pathlib import Path

import pytest

from teaching_hub.loader import load_site
from teaching_hub.render import build_site

CHROME = os.environ.get("TEACHING_HUB_CHROME")
SCRIPT = Path(__file__).parent / "browser" / "navigation.mjs"
SEARCH_SCRIPT = Path(__file__).parent / "browser" / "search.mjs"
pytestmark = [
    pytest.mark.renderer,
    pytest.mark.browser,
    pytest.mark.skipif(not (CHROME and shutil.which("node")), reason="set TEACHING_HUB_CHROME and install Node.js"),
]


@pytest.fixture
def served(tmp_path):
    def serve(site_dir: Path) -> str:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site_dir))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        servers.append(server)
        return f"http://127.0.0.1:{server.server_address[1]}"
    servers: list = []
    yield serve
    for server in servers:
        server.shutdown()


@pytest.mark.parametrize("renderer", ["zensical", "material"])
def test_section_toggle_is_a_named_button_whose_state_follows_the_keyboard(sample, tmp_path, served, renderer):
    site_dir = tmp_path / "_site"
    build_site(load_site(sample), tmp_path / "build", site_dir, renderer=renderer)
    base = served(site_dir)
    proc = subprocess.run(["node", str(SCRIPT), f"{base}/courses/sample-course-a/", CHROME, str(tmp_path / "profile")],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    for view in ("desktop", "phone"):
        r = result[view]
        initial = r["initial"]
        assert initial["role"] == "button" and initial["focusable"], (view, initial)
        assert initial["name"] == "Podsekcje: Przedmiot przykładowy A", (view, initial)
        assert initial["listName"] == initial["name"], (view, initial)  # the list it controls is named too
        assert initial["expanded"] is True and initial["checked"] is True, (view, initial)
        # Space and Enter both toggle; the state seen by assistive technologies follows; Space does not scroll.
        for step, expected in (("afterSpace", False), ("afterSecondSpace", True), ("afterEnter", False)):
            s = r[step]
            assert s["checked"] is expected and s["expanded"] is expected and s["focused"], (view, step, s)
        assert r["afterSpace"]["scrollY"] == initial["scrollY"], (view, r["afterSpace"])
    drawer = result["phone"]["drawerBefore"]
    assert drawer["focused"] and drawer["role"] == "button" and drawer["name"], drawer
    assert drawer["expanded"] == "false" and drawer["checked"] is False, drawer
    assert result["phone"]["drawerAfterEnter"] == {"expanded": "true", "checked": True}, result["phone"]["drawerAfterEnter"]
    assert result["phone"]["drawerAfterSpace"] == {"expanded": "false", "checked": False}, result["phone"]["drawerAfterSpace"]


def search(base: str, tmp_path: Path, queries: list[dict]) -> dict:
    proc = subprocess.run(["node", str(SEARCH_SCRIPT), base, CHROME, str(tmp_path / "profile-search"), json.dumps(queries)],
                          capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_search_finds_the_whole_language_from_any_page_by_keyboard(sample, tmp_path, served):
    # Zensical's search dialog (the deployed renderer); the indexes of both renderers are tested in test_render.py.
    drafts = tmp_path / "drafts"
    (drafts / "pl/courses/sample-course-a/task-sets").mkdir(parents=True)
    (drafts / "pl/courses/sample-course-a/task-sets/09-draft.md").write_text(
        '---\ntitle: "Szkic"\nstatus: published\n---\n\n## Zadania\n\n### Zadanie {#d1}\n\nSzkicowetestowesłowo.\n',
        encoding="utf-8")
    site_dir = tmp_path / "_site"
    build_site(load_site(sample, drafts=drafts), tmp_path / "build", site_dir, renderer="zensical")
    base = served(site_dir)
    result = search(base, tmp_path, [
        {"page": "/", "query": "Temat zastępczy alfa"},  # a task set of the course space, from the home page
        {"page": "/courses/", "query": "Tytuł zastępczy zadania pierwszego"},  # a task, from the catalogue
        {"page": "/courses/sample-course-a/", "query": "Tekst zastępczy strony licencji"},  # /licensing/, from a course
        {"page": "/en/", "query": "Temat zastępczy alfa"},  # Polish text is not in the English index
        {"page": "/", "query": "Szkicowetestowesłowo"},  # drafts are never indexed
    ])
    for view in ("desktop", "phone"):
        home, catalogue, course, english, draft = result[view]
        for r in (home, catalogue, course):
            assert r["focused"] and r["results"], (view, r)
            assert len(r["results"]) == len(set(r["results"])), (view, r)  # no duplicates
            assert r["opened"] == r["results"][r["selected"]], (view, r)  # Enter opens the selected result
        assert all(u.startswith("/courses/sample-course-a/") for u in home["results"]), (view, home["results"])
        assert "/courses/sample-course-a/task-sets/alpha/" in home["results"], (view, home["results"])
        assert "/courses/sample-course-a/task-sets/alpha/#a1" in catalogue["results"], (view, catalogue)
        assert course["results"][0].startswith("/licensing/"), (view, course)
        assert english["results"] == [] or all(u.startswith("/en/") for u in english["results"]), (view, english)
        assert draft["results"] == [], (view, draft)


def test_closed_navigation_drawer_is_out_of_the_keyboard_and_screen_reader_path(sample, tmp_path, served):
    for renderer in ("zensical", "material"):
        site_dir = tmp_path / renderer / "_site"
        build_site(load_site(sample), tmp_path / renderer / "build", site_dir, renderer=renderer)
        base = served(site_dir)
        proc = subprocess.run(["node", str(SCRIPT), f"{base}/courses/sample-course-a/", CHROME, str(tmp_path / renderer / "profile")],
                              capture_output=True, text=True, timeout=180)
        assert proc.returncode == 0, proc.stderr
        drawer = json.loads(proc.stdout)["drawer"]
        for view in ("phone", "tablet"):
            d = drawer[view]
            # Closed: inert, reported as collapsed, and Tab never lands in it or off screen.
            assert d["closed"]["open"] is False and d["closed"]["inert"] and d["closed"]["expanded"] == "false", (renderer, view, d["closed"])
            assert not any(stop["inDrawer"] for stop in d["closedStops"]), (renderer, view, d["closedStops"])
            assert all(stop["onScreen"] for stop in d["closedStops"]), (renderer, view, [s for s in d["closedStops"] if not s["onScreen"]])
            # Enter opens it; its links are then reachable with Tab, on screen.
            assert d["openedWithEnter"]["open"] and not d["openedWithEnter"]["inert"], (renderer, view, d["openedWithEnter"])
            assert d["openedWithEnter"]["expanded"] == "true", (renderer, view, d["openedWithEnter"])
            assert any(s["focusInDrawer"] and s["focusOnScreen"] for s in d["openStops"]), (renderer, view, d["openStops"])
            # Escape closes it and focus, which was in the drawer, returns to the button that opened it.
            assert d["focusBeforeEscape"]["focusInDrawer"], (renderer, view, d["focusBeforeEscape"])
            after = d["afterEscape"]
            assert not after["open"] and after["inert"] and after["expanded"] == "false" and after["focusOnButton"], (renderer, view, after)
            # Space opens and closes it as well, focus staying on the button.
            assert d["openedWithSpace"]["open"] and not d["openedWithSpace"]["inert"], (renderer, view, d["openedWithSpace"])
            closed = d["closedWithSpace"]
            assert not closed["open"] and closed["inert"] and closed["focusOnButton"], (renderer, view, closed)
        # Wide screens: the sidebar is a column of the page, reachable and never inert.
        assert drawer["resizedToDesktop"]["inert"] is False, (renderer, drawer["resizedToDesktop"])
        assert drawer["desktop"]["state"]["inert"] is False, (renderer, drawer["desktop"])
        assert any(stop["inDrawer"] and stop["onScreen"] for stop in drawer["desktop"]["stops"]), (renderer, drawer["desktop"])
