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
