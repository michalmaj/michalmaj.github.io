"""Run a renderer for each build and compose one artifact."""

import html
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from .assemble import Build, assemble
from .i18n import t
from .loader import Site
from .urls import space_has_content

_BIN = Path(sys.executable).parent


class RenderError(RuntimeError):
    """A renderer build failed (in strict mode every warning is a failure)."""


@dataclass(frozen=True)
class RenderResult:
    build: Build
    seconds: float
    output: str


def _command(renderer: str, config: Path) -> list[str]:
    if renderer == "zensical":
        return [str(_BIN / "zensical"), "build", "--strict", "--clean", "-f", str(config)]
    if renderer == "material":
        return [str(_BIN / "mkdocs"), "build", "--strict", "-f", str(config)]
    raise ValueError(f"unknown renderer {renderer!r}")


def render(builds: list[Build], renderer: str) -> list[RenderResult]:
    results = []
    for build in builds:
        start = time.perf_counter()
        proc = subprocess.run(_command(renderer, build.config_path), capture_output=True, text=True)
        seconds = time.perf_counter() - start
        output = proc.stdout + proc.stderr
        if proc.returncode != 0:
            raise RenderError(f"{renderer} failed for {build.prefix}:\n{output[-4000:]}")
        results.append(RenderResult(build, seconds, output))
    return results


def not_found_page(site: Site, icon: str | None = None) -> str:
    sections = []
    for lang in ("pl", "en"):
        home = "/" if lang == "pl" or not space_has_content(site, "home", "en") else "/en/"
        attr = "" if lang == "pl" else ' lang="en"'
        sections.append(
            f"<section{attr}><h1>{html.escape(t(site, lang, 'not_found_title'))}</h1>"
            f"<p>{html.escape(t(site, lang, 'not_found_text'))}</p>"
            f'<p><a href="{home}">{html.escape(t(site, lang, "nav_home"))}</a></p></section>'
        )
    style = (
        "body{font-family:system-ui,sans-serif;max-width:40rem;margin:3rem auto;padding:0 1rem;"
        "line-height:1.5;color:#1a1a1a;background:#fff}a{color:#0b57d0}"
        "@media (prefers-color-scheme:dark){body{color:#e6e6e6;background:#121212}a{color:#8ab4f8}}"
    )
    return (
        '<!doctype html>\n<html lang="pl">\n<head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>404</title>{f'<link rel="icon" href="{html.escape(icon)}">' if icon else ''}"
        f"<style>{style}</style></head>\n<body><main>\n"
        + "\n".join(sections)
        + "\n</main></body>\n</html>\n"
    )


# Search index of a build: Zensical writes search.json with "items", MkDocs Material
# search/search_index.json with "docs". Each entry's "location" is relative to the build root.
SEARCH_INDEXES = (("search.json", "items"), ("search/search_index.json", "docs"))


def search_groups(site: Site, builds) -> list[list[str]]:
    """Build prefixes that share one search index: same language and same search group of the space."""
    groups: dict[tuple[str, str], list[str]] = {}
    for build in builds:
        space = site.spaces.get(build.space)
        group = (space.search_group if space else None) or f"space:{build.space}"
        groups.setdefault((build.lang, group), []).append(build.prefix)
    return list(groups.values())


def relocate(location: str, source: str, target: str) -> str:
    """A search entry `location` of the build at `source`, relative to the build at `target`."""
    path, hash_, fragment = location.partition("#")
    absolute = source + path
    parts = [p for p in absolute.split("/") if p]
    base = [p for p in target.split("/") if p]
    common = 0
    while common < min(len(parts), len(base)) and parts[common] == base[common]:
        common += 1
    relative = [".."] * (len(base) - common) + parts[common:]
    out = "/".join(relative) + ("/" if relative and absolute.endswith("/") else "")
    return out + hash_ + fragment


def _read_index(site_dir: Path, prefix: str) -> tuple[Path, str, dict] | None:
    for rel, key in SEARCH_INDEXES:
        path = site_dir / prefix.strip("/") / rel
        if path.is_file():
            return path, key, json.loads(path.read_text(encoding="utf-8"))
    return None


def _merge_search_indexes(site: Site, builds: list[Build], site_dir: Path) -> None:
    """Each build's search index also lists the entries of the other builds of its group.

    Only entries the renderer wrote are merged, so pages it left out (drafts, archived pages
    excluded from search) stay out. Each page or section appears once per index.
    """
    for group in search_groups(site, builds):
        indexes = {prefix: index for prefix in group if (index := _read_index(site_dir, prefix))}
        own = {prefix: list(data[key]) for prefix, (_, key, data) in indexes.items()}
        for prefix, (path, key, data) in indexes.items():
            seen: set[str] = set()
            merged = []
            for source in [prefix, *(p for p in group if p != prefix and p in own)]:
                for entry in own[source]:
                    absolute = relocate(entry["location"], source, "/")
                    if absolute in seen:
                        continue
                    seen.add(absolute)
                    location = entry["location"] if source == prefix else relocate(entry["location"], source, prefix)
                    merged.append({**entry, "location": location})
            data[key] = merged
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


_URL_ENTRY = re.compile(r"<url>.*?</url>", re.S)
FAVICON = "assets/images/favicon.png"


def _merge_sitemaps(site: Site, builds: list[Build], site_dir: Path) -> None:
    """One sitemap for the whole site at the root, named in robots.txt.

    Every build writes its own sitemap.xml (and Material a .gz copy); search engines look for
    /sitemap.xml, so the entries of all builds are merged there and the per-build files removed.
    """
    entries: list[str] = []
    for build in sorted(builds, key=lambda b: len(b.prefix)):
        path = site_dir / build.prefix.strip("/") / "sitemap.xml"
        if path.is_file():
            entries += [entry.strip() for entry in _URL_ENTRY.findall(path.read_text(encoding="utf-8"))]
    for path in [*site_dir.rglob("sitemap.xml"), *site_dir.rglob("sitemap.xml.gz")]:
        path.unlink()
    (site_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  {entry}\n" for entry in entries) + "</urlset>\n", encoding="utf-8")
    site_url = site.settings["site_url"].rstrip("/") + "/"
    (site_dir / "robots.txt").write_text(f"User-agent: *\nDisallow:\n\nSitemap: {site_url}sitemap.xml\n", encoding="utf-8")


def compose(site: Site, builds: list[Build], site_dir: Path) -> None:
    site_dir = Path(site_dir)
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    for build in sorted(builds, key=lambda b: len(b.prefix)):
        target = site_dir / build.prefix.strip("/")
        shutil.copytree(build.site_dir, target, dirs_exist_ok=True)
        if build.prefix.strip("/"):
            (target / "404.html").unlink(missing_ok=True)  # GitHub Pages serves only /404.html
    _merge_sitemaps(site, builds, site_dir)
    _merge_search_indexes(site, builds, site_dir)
    # An absolute icon URL keeps the 404 page self-contained at any depth of a missing path.
    icon = urlsplit(site.settings["site_url"]).path.rstrip("/") + "/" + FAVICON if (site_dir / FAVICON).is_file() else None
    (site_dir / "404.html").write_text(not_found_page(site, icon), encoding="utf-8")


def build_site(
    site: Site, build_dir: Path, site_dir: Path, renderer: str = "zensical", include_drafts: bool = False
) -> list[RenderResult]:
    build_dir = Path(build_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    builds = assemble(site, build_dir, include_drafts=include_drafts)
    results = render(builds, renderer)
    compose(site, builds, site_dir)
    return results
