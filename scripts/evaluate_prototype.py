"""Compare Zensical and MkDocs Material on the sample fixture (build, search, checks, parity).

Usage: uv run python scripts/evaluate_prototype.py [--out results.json]
Builds only placeholder fixture content into a temporary directory; publishes nothing.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from teaching_hub.assemble import assemble
from teaching_hub.check import check_artifact
from teaching_hub.loader import load_site
from teaching_hub.render import RenderError, build_site, render

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests/fixtures/sample"
DRAFT_WORD = "Szkicowetestowesłowo"
ARCHIVE_WORD = "Zarchiwizowanetestowesłowo"
DRAFT = f"""---
title: "Szkic zastępczy"
---

## Zadania

### Zadanie szkicu {{#d1}}

{DRAFT_WORD}
"""


def source(tmp: Path, name: str) -> Path:
    root = tmp / name
    shutil.copytree(FIXTURE, root)
    shutil.copytree(REPO / "renderer", root / "renderer")
    return root


def drafts_dir(tmp: Path) -> Path:
    d = tmp / "private-drafts" / "drafts"
    path = d / "pl/courses/sample-course-a/task-sets/05-draft-x.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(DRAFT, encoding="utf-8")
    return d


def digest(site_dir: Path) -> dict[str, str]:
    return {
        p.relative_to(site_dir).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(site_dir.rglob("*"))
        if p.is_file()
    }


def pages(site_dir: Path) -> list[str]:
    return sorted(
        p.relative_to(site_dir).as_posix()
        for p in site_dir.rglob("index.html")
        if "/assets/" not in p.as_posix()
    )


def search_indexes(site_dir: Path) -> dict:
    out = {}
    for path in sorted(list(site_dir.rglob("search.json")) + list(site_dir.rglob("search_index.json"))):
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data.get("items") or data.get("docs") or []
        decoded = json.dumps(data, ensure_ascii=False)
        out[path.relative_to(site_dir).as_posix()] = {
            "lang": (data.get("config") or {}).get("lang"),
            "entries": len(items),
            "contains_archived_word": ARCHIVE_WORD in decoded,
            "contains_draft_word": DRAFT_WORD in decoded,
            "contains_other_language_text": ("Placeholder topic alpha" in decoded) if not path.as_posix().count("/en/") else ("Temat zastępczy alfa" in decoded),
        }
    return out


def a11y_hints(site_dir: Path) -> dict:
    page = (site_dir / "courses/sample-course-a/task-sets/alpha/index.html").read_text(encoding="utf-8")
    css = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in site_dir.glob("courses/assets/stylesheets/**/*.css"))
    html_langs = {}
    for prefix in ("", "courses/", "en/", "en/courses/"):
        html = (site_dir / prefix / "index.html").read_text(encoding="utf-8")
        match = re.search(r"<html[^>]*\blang=\"([^\"]+)\"", html)
        html_langs[prefix or "/"] = match.group(1) if match else None
    return {
        "html_lang": html_langs,
        "viewport_meta": 'name="viewport"' in page,
        "skip_link": "md-skip" in page,
        # Both themes style focus via a .focus-visible class (polyfill pattern) rather than :focus-visible.
        "focus_styles_in_css": "focus-visible" in css,
        "lang_attribute_on_switch_link": 'lang="en"' in page,
    }


def remote_hosts_in_js(site_dir: Path) -> list[str]:
    hosts = set()
    for path in site_dir.rglob("*.js"):
        hosts.update(re.findall(r"https://([a-z0-9.-]+\.[a-z]{2,})", path.read_text(encoding="utf-8", errors="replace")))
    return sorted(hosts)


def strict_negative(tmp: Path, renderer: str, broken: str) -> dict:
    root = source(tmp, f"neg-{renderer}-{broken.count('#')}")
    guide = root / "content/pl/courses/sample-course-a/guides/guidelines.md"
    guide.write_text(guide.read_text(encoding="utf-8") + f"\n[x]({broken})\n", encoding="utf-8")
    try:
        build_site(load_site(root), tmp / f"nb-{renderer}", tmp / f"ns-{renderer}", renderer=renderer)
    except RenderError as exc:
        text = str(exc)
        return {"renderer_failed": True, "python_traceback_in_output": "Traceback" in text}
    leftover = check_artifact(tmp / f"ns-{renderer}")
    return {"renderer_failed": False, "pipeline_artifact_check": sorted({i.code for i in leftover})}


def evaluate_renderer(tmp: Path, renderer: str) -> dict:
    site_dir = tmp / f"site-{renderer}"
    start = time.perf_counter()
    results = build_site(load_site(source(tmp, f"src-{renderer}")), tmp / f"build-{renderer}", site_dir, renderer=renderer)
    total = time.perf_counter() - start

    second = tmp / f"site-{renderer}-2"
    build_site(load_site(source(tmp, f"src-{renderer}-2")), tmp / f"build-{renderer}-2", second, renderer=renderer)
    first_digest, second_digest = digest(site_dir), digest(second)
    differing = sorted(k for k in first_digest.keys() | second_digest.keys() if first_digest.get(k) != second_digest.get(k))

    issues = check_artifact(site_dir, forbidden=[DRAFT_WORD, "Szkic zastępczy"])
    return {
        "builds": [{"prefix": r.build.prefix, "seconds": round(r.seconds, 3)} for r in results],
        "total_seconds_including_assemble": round(total, 3),
        "artifact_files": len(first_digest),
        "artifact_bytes": sum(p.stat().st_size for p in site_dir.rglob("*") if p.is_file()),
        "artifact_issues": [str(i) for i in issues],
        "pages": pages(site_dir),
        "search_indexes": search_indexes(site_dir),
        "a11y_hints": a11y_hints(site_dir),
        "remote_hosts_mentioned_in_js": remote_hosts_in_js(site_dir),
        "deterministic": not differing,
        "differing_files_between_two_builds": differing[:20],
        "strict_broken_page": strict_negative(tmp, renderer, "../task-sets/ghost.md"),
        "strict_broken_anchor": strict_negative(tmp, renderer, "../task-sets/alpha.md#ghost-anchor"),
    }


def evaluate_preview(tmp: Path) -> dict:
    root = source(tmp, "src-preview")
    drafts = drafts_dir(tmp)
    site_dir = tmp / "site-preview"
    build_site(load_site(root, drafts=drafts), tmp / "build-preview", site_dir, renderer="zensical", include_drafts=True)
    page = site_dir / "courses/sample-course-a/task-sets/draft-x/index.html"
    env = {**os.environ, "GITHUB_ACTIONS": "true"}
    refused = subprocess.run(
        [sys.executable, "-m", "teaching_hub.cli", "build", "--source", str(root), "--drafts", str(drafts),
         "--build-dir", str(tmp / "b-ci"), "--site-dir", str(tmp / "s-ci")],
        capture_output=True, text=True, env=env,
    )
    normal = tmp / "site-normal"
    build_site(load_site(root), tmp / "build-normal", normal, renderer="zensical")
    return {
        "draft_page_in_preview": page.is_file(),
        "draft_banner_in_preview": page.is_file() and "SZKIC" in page.read_text(encoding="utf-8"),
        "preview_refused_with_GITHUB_ACTIONS": refused.returncode != 0 and "PreviewNotAllowed" in (refused.stdout + refused.stderr),
        "draft_absent_from_normal_build": check_artifact(normal, forbidden=[DRAFT_WORD, "Szkic zastępczy"]) == [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="teaching-hub-eval-") as tmp_name:
        tmp = Path(tmp_name)
        results = {name: evaluate_renderer(tmp, name) for name in ("zensical", "material")}
        results["preview"] = evaluate_preview(tmp)
        z, m = set(results["zensical"]["pages"]), set(results["material"]["pages"])
        results["page_parity"] = {"only_zensical": sorted(z - m), "only_material": sorted(m - z)}
    text = json.dumps(results, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
