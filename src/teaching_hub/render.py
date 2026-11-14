"""Run a renderer for each build and compose one artifact."""

import html
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
