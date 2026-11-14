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


def check_pages_present(site_dir: Path, urls) -> list[Issue]:
    """Every public URL of the source must exist in the composed artifact."""
    return [
        error("missing-page", url, "public page is missing from the artifact")
        for url in urls
        if _target_file(Path(site_dir), url) is None
    ]


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



class _Canonical(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and (a.get("rel") or "").lower() == "canonical" and a.get("href"):
            self.urls.append(a["href"])


_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


def check_site_urls(site_dir: Path, site_url: str) -> list[Issue]:
    """Canonical links and sitemap entries must point to the production domain."""
    site_dir = Path(site_dir)
    issues: list[Issue] = []
    for path in sorted(site_dir.rglob("*")):
        if path.suffix == ".html":
            parser = _Canonical()
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
            urls = parser.urls
        elif path.name == "sitemap.xml":
            urls = _LOC_RE.findall(path.read_text(encoding="utf-8", errors="replace"))
        else:
            continue
        wrong = [u for u in urls if not u.startswith(site_url)]
        if wrong:
            rel = path.relative_to(site_dir).as_posix()
            issues.append(error("wrong-site-url", rel, f"{len(wrong)} URL(s) outside {site_url}, e.g. {wrong[0]}"))
    return issues


def _exists_exactly(root: Path, rel: str, directory: bool) -> bool:
    """Like Path.exists, but case-sensitive on every filesystem (GitHub URLs are case-sensitive)."""
    current = Path(root)
    for part in [p for p in rel.split("/") if p]:
        if not current.is_dir() or part not in {child.name for child in current.iterdir()}:
            return False
        current = current / part
    return current.is_dir() if directory else current.is_file()


def check_repository_links(site_dir: Path, repository_url: str, source_root: Path, branch: str = "main") -> list[Issue]:
    """Links to files of the site's own repository on GitHub must point to files in the source.

    The site is deployed from the same commit as its source, so `<repository>/blob/<branch>/<path>`
    (and `tree/` for directories) works after publication only if `<path>` exists in that source.
    """
    site_dir = Path(site_dir)
    base = urlsplit(repository_url.rstrip("/") + "/")
    pattern = re.compile(rf"^{re.escape(base.path)}(blob|tree)/{re.escape(branch)}/(.+?)/?$")
    issues: list[Issue] = []
    for path in sorted(site_dir.rglob("*.html")):
        parser = _Page()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        rel = path.relative_to(site_dir).as_posix()
        for href in parser.links:
            parts = urlsplit(href)
            if (parts.scheme, parts.netloc) != (base.scheme, base.netloc):
                continue
            match = pattern.match(parts.path)
            if not match:
                continue
            kind, target = match.group(1), unquote(match.group(2))
            if not _exists_exactly(source_root, target, directory=kind == "tree"):
                issues.append(error("broken-repository-link", rel, f"{kind}/{branch}/{target} does not exist in the source ({href})"))
    return issues


def check_anchor_aliases(site_dir: Path, aliases) -> list[Issue]:
    """Each published anchor that changed must still exist on its page, next to its target heading."""
    site_dir = Path(site_dir)
    issues: list[Issue] = []
    for alias in aliases:
        target = _target_file(site_dir, alias.page)
        ids: set[str] = set()
        if target is not None:
            page = _Page()
            page.feed(target.read_text(encoding="utf-8", errors="replace"))
            ids = page.ids
        missing = [a for a in (alias.anchor, alias.target) if a not in ids]
        if missing:
            issues.append(error("broken-anchor-alias", alias.page,
                                f"#{alias.anchor} → #{alias.target}: {', '.join('#' + m for m in missing)} not on the page "
                                "(see data/anchor-aliases.yml)"))
    return issues


def check_sitemap(site_dir: Path, site_url: str, urls) -> list[Issue]:
    """One sitemap at the root lists exactly the public pages, and robots.txt names it."""
    site_dir = Path(site_dir)
    site_url = site_url.rstrip("/") + "/"
    issues: list[Issue] = []
    root = site_dir / "sitemap.xml"
    for path in sorted([*site_dir.rglob("sitemap*.xml"), *site_dir.rglob("sitemap*.xml.gz")]):
        if path != root:
            rel = path.relative_to(site_dir).as_posix()
            issues.append(error("sitemap", rel, f"only /sitemap.xml may exist; {rel} is a second sitemap"))
    if not root.is_file():
        issues.append(error("sitemap", "sitemap.xml", "the site has no /sitemap.xml"))
    else:
        locs = _LOC_RE.findall(root.read_text(encoding="utf-8", errors="replace"))
        expected = {site_url.rstrip("/") + url for url in urls}
        for loc in sorted(set(locs) - expected):
            issues.append(error("sitemap", "sitemap.xml", f"lists {loc}, which is not a public page"))
        for loc in sorted(expected - set(locs)):
            issues.append(error("sitemap", "sitemap.xml", f"public page {loc} is missing"))
        for loc in sorted({loc for loc in locs if locs.count(loc) > 1}):
            issues.append(error("sitemap", "sitemap.xml", f"lists {loc} more than once"))
    robots = site_dir / "robots.txt"
    line = f"Sitemap: {site_url}sitemap.xml"
    if not robots.is_file() or line not in robots.read_text(encoding="utf-8", errors="replace").splitlines():
        issues.append(error("sitemap", "robots.txt", f"robots.txt must contain the line {line!r}"))
    return issues


_SEARCH_INDEXES = (("search.json", "items"), ("search/search_index.json", "docs"))


def _absolute(location: str, prefix: str) -> str:
    """Site path of a search entry location of the build at `prefix`."""
    path, hash_, fragment = location.partition("#")
    parts: list[str] = []
    for part in (prefix + path).split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part not in ("", "."):
            parts.append(part)
    url = "/" + "/".join(parts) + ("/" if parts and (prefix + path).endswith("/") else "")
    return url + hash_ + fragment


def check_search_indexes(site_dir: Path, groups: list[list[str]]) -> list[Issue]:
    """Builds that share a search index (same language and audience) list the same existing pages once.

    `groups` holds the build prefixes of every search group, e.g. [["/", "/courses/"], ["/en/", ...]].
    """
    site_dir = Path(site_dir)
    issues: list[Issue] = []
    prefixes = sorted({p for group in groups for p in group}, key=len, reverse=True)
    owner = lambda url: next((p for p in prefixes if url.startswith(p)), None)  # noqa: E731
    pages_cache: dict[Path, set[str]] = {}
    for group in groups:
        listed: dict[str, set[str]] = {}
        for prefix in group:
            found = next(((site_dir / prefix.strip("/") / rel, key) for rel, key in _SEARCH_INDEXES
                          if (site_dir / prefix.strip("/") / rel).is_file()), None)
            if found is None:
                continue
            path, key = found
            rel = path.relative_to(site_dir).as_posix()
            entries = [_absolute(e["location"], prefix) for e in json.loads(path.read_text(encoding="utf-8"))[key]]
            for url in sorted({u for u in entries if entries.count(u) > 1}):
                issues.append(error("search-index", rel, f"lists {url} twice"))
            for url in sorted(set(entries)):
                page, _, fragment = url.partition("#")
                if owner(page) not in group:
                    issues.append(error("search-index", rel, f"lists {url}, outside its language and audience"))
                    continue
                target = _target_file(site_dir, page)
                if target is None:
                    issues.append(error("search-index", rel, f"lists {url}: no such page"))
                    continue
                if fragment:
                    if target not in pages_cache:
                        parser = _Page()
                        parser.feed(target.read_text(encoding="utf-8", errors="replace"))
                        pages_cache[target] = parser.ids
                    if unquote(fragment) not in pages_cache[target]:
                        issues.append(error("search-index", rel, f"lists {url}: no element with that id"))
            listed[prefix] = {u.partition("#")[0] for u in entries}
        every = set().union(*listed.values()) if listed else set()
        for prefix, pages in listed.items():
            for page in sorted(every - pages):
                issues.append(error("search-index", prefix, f"the search index of {prefix} does not list {page}"))
    return issues
