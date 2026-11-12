"""Run a renderer for each build and compose one artifact."""

import html
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

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


def not_found_page(site: Site) -> str:
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
        f"<title>404</title><style>{style}</style></head>\n<body><main>\n"
        + "\n".join(sections)
        + "\n</main></body>\n</html>\n"
    )


def compose(site: Site, builds: list[Build], site_dir: Path) -> None:
    site_dir = Path(site_dir)
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)
    for build in sorted(builds, key=lambda b: len(b.prefix)):
        shutil.copytree(build.site_dir, site_dir / build.prefix.strip("/"), dirs_exist_ok=True)
    (site_dir / "404.html").write_text(not_found_page(site), encoding="utf-8")


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
