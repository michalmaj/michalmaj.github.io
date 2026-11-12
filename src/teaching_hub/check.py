"""Checks on the composed artifact (_site/) and on tracked files. Renderer-independent."""

import fnmatch
import json
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from .issues import Issue, error

# Elements whose URL attribute makes the browser load a resource.
_LOADING_LINK_RELS = {"stylesheet", "preload", "preconnect", "dns-prefetch", "icon", "modulepreload", "manifest", "prefetch"}
_SRC_TAGS = {"script", "img", "iframe", "source", "video", "audio", "embed"}
_CSS_REMOTE_RE = re.compile(r"""(?:@import\s+(?:url\()?|url\()\s*['"]?(https?:)?//""", re.I)
_TEXT_SUFFIXES = {".html", ".json", ".xml", ".js", ".css", ".txt"}

PRIVATE_PATTERNS = (
    "ARCHITECTURE.md",
    "drafts/*",
    "CLAUDE.md",
    "*/CLAUDE.md",
    "AGENTS.md",
    "*/AGENTS.md",
    ".claude/*",
    ".superpowers/*",
    "*.private.md",
)


class _Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []  # navigations and internal resource references
        self.remote_loads: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("id", "name"):
            if a.get(key):
                self.ids.add(a[key])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "link" and a.get("href"):
            rels = set((a.get("rel") or "").lower().split())
            if rels & _LOADING_LINK_RELS:
                (self.remote_loads if _is_remote(a["href"]) else self.links).append(a["href"])
        elif tag in _SRC_TAGS and a.get("src"):
            (self.remote_loads if _is_remote(a["src"]) else self.links).append(a["src"])


def _is_remote(url: str) -> bool:
    return url.startswith(("http://", "https://", "//"))


def _page_url(site_dir: Path, path: Path) -> PurePosixPath:
    rel = PurePosixPath(path.relative_to(site_dir).as_posix())
    return PurePosixPath("/") / (rel.parent if rel.name == "index.html" else rel)


def _target_file(site_dir: Path, url_path: str) -> Path | None:
    rel = url_path.lstrip("/")
    candidates = [site_dir / rel / "index.html"] if url_path.endswith("/") or rel == "" else [
        site_dir / rel, site_dir / rel / "index.html", site_dir / f"{rel}.html"
    ]
    return next((c for c in candidates if c.is_file()), None)


def _space(url_path: str) -> str:
    parts = [p for p in url_path.split("/") if p]
    if parts and parts[0] == "en":
        parts = parts[1:]
    return parts[0] if parts and parts[0] in ("courses", "for-employers") else "home"


def check_artifact(site_dir: Path, forbidden=(), disabled_spaces=("for-employers",)) -> list[Issue]:
    site_dir = Path(site_dir)
    issues: list[Issue] = []
    if not (site_dir / "404.html").is_file():
        issues.append(error("missing-404", "404.html", "GitHub Pages serves /404.html for every missing path"))
    for space in disabled_spaces:
        for prefix in (space, f"en/{space}"):
            if (site_dir / prefix).exists():
                issues.append(error("disabled-space-output", prefix, f"the {space} space is disabled"))

    pages: dict[Path, _Page] = {}
    for path in sorted(site_dir.rglob("*.html")):
        parser = _Page()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        pages[path] = parser

    for path, page in pages.items():
        rel = path.relative_to(site_dir).as_posix()
        here = _page_url(site_dir, path)
        page_space = _space(str(here))
        for url in page.remote_loads:
            issues.append(error("external-request", rel, f"loads a third-party resource: {url}"))
        for href in page.links:
            if _is_remote(href) or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            parts = urlsplit(href)
            if parts.path:
                base = here if str(here).endswith("/") or path.name == "index.html" else here.parent
                joined = PurePosixPath(unquote(parts.path)) if parts.path.startswith("/") else base / unquote(parts.path)
                target_path = _normalize(joined, keep_slash=parts.path.endswith("/"))
                target = _target_file(site_dir, target_path)
                if target is None:
                    issues.append(error("broken-link", rel, f"{href} → {target_path} does not exist"))
                    continue
                target_space = _space(target_path)
                if page_space != "home" and target_space not in ("home", page_space):
                    issues.append(error("cross-space-link", rel, f"{href} links the {page_space} space to {target_space}"))
            else:
                target = path
            if parts.fragment and target.suffix == ".html":
                target_page = pages.get(target)
                if target_page is not None and unquote(parts.fragment) not in target_page.ids:
                    issues.append(error("broken-anchor", rel, f"{href}: no element with id {parts.fragment!r}"))

    for path in sorted(p for p in site_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(site_dir).as_posix()
        if _is_private_artifact_path(rel):
            issues.append(error("private-file-published", rel, "private material must never be part of the published site"))
        if path.suffix == ".css" and _CSS_REMOTE_RE.search(path.read_text(encoding="utf-8", errors="replace")):
            issues.append(error("external-request", rel, "stylesheet imports a remote resource"))
        if forbidden and path.suffix in _TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            for needle in forbidden:
                # JSON writers may escape non-ASCII characters ("ł" -> "ł").
                escaped = json.dumps(needle)[1:-1]
                if needle in text or escaped in text:
                    issues.append(error("forbidden-text", rel, f"contains {needle!r}"))
    return issues


def _normalize(path: PurePosixPath, keep_slash: bool) -> str:
    parts: list[str] = []
    for part in path.parts:
        if part in ("/", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    out = "/" + "/".join(parts)
    return out + "/" if keep_slash and out != "/" else out


_PRIVATE_NAMES = {"ARCHITECTURE.md", "CLAUDE.md", "AGENTS.md"}
_PRIVATE_DIRS = {"drafts", ".claude", ".superpowers"}


def _is_private_artifact_path(rel: str) -> bool:
    parts = rel.split("/")
    return parts[-1] in _PRIVATE_NAMES or parts[-1].endswith(".private.md") or bool(_PRIVATE_DIRS & set(parts[:-1]))


def draft_markers(site) -> list[str]:
    """Texts of the draft banner; they may appear only in a local draft preview."""
    return [text for text in (site.i18n.get(lang, {}).get("draft_text") for lang in ("pl", "en")) if text]


def check_tracked_paths(paths) -> list[Issue]:
    """Flag private files (local documentation, drafts, tool configuration) among tracked paths."""
    return [
        error("private-file-tracked", p, "private material must not be tracked in the public repository")
        for p in paths
        if any(fnmatch.fnmatch(p, pattern) for pattern in PRIVATE_PATTERNS)
    ]
