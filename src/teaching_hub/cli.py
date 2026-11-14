"""Command line: teaching-hub <command> [options]."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from .assemble import PreviewNotAllowed
from .check import (
    check_anchor_aliases,
    check_artifact,
    check_pages_present,
    check_repository_links,
    check_site_urls,
    check_sitemap,
    check_tracked_paths,
    draft_markers,
)
from .loader import load_site
from .materials import GitResolver, check_materials, referenced_repositories
from .production import FIXTURE_MARKERS, has_production_content, is_test_fixture, production_status
from .render import RenderError, build_site
from .urls import public_urls
from .validate import check_registered_urls, validate


def _report(issues) -> int:
    for issue in issues:
        print(issue)
    errors = sum(1 for i in issues if i.level == "error")
    warnings = len(issues) - errors
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def _cmd_validate(args) -> int:
    return _report(validate(load_site(Path(args.source), drafts=args.drafts, config_dir=Path(args.config_dir))))


def _production_checks(site, site_dir: Path) -> tuple[list[str], list]:
    """Extra forbidden strings and issues for a production artifact."""
    issues = check_site_urls(site_dir, site.settings["site_url"])
    issues += check_sitemap(site_dir, site.settings["site_url"], public_urls(site))
    issues += check_registered_urls(site)
    if site.settings.get("repository_url"):
        issues += check_repository_links(site_dir, site.settings["repository_url"], site.root)
    return list(FIXTURE_MARKERS), issues


def _cmd_build(args) -> int:
    if args.production:
        if is_test_fixture(Path(args.source)):
            print(f"refused: a production build cannot use the test fixture ({args.source})")
            return 1
        if args.drafts is not None:
            print("refused: a production build never includes drafts")
            return 1
    site = load_site(Path(args.source), drafts=args.drafts, config_dir=Path(args.config_dir))
    issues = validate(site)
    if _report(issues):
        return 1
    try:
        results = build_site(site, Path(args.build_dir), Path(args.site_dir), args.renderer, include_drafts=args.drafts is not None)
    except (RenderError, PreviewNotAllowed) as exc:
        print(exc)
        return 1
    for r in results:
        print(f"built {r.build.prefix:<14} with {args.renderer} in {r.seconds:.2f}s")
    # Outside a draft preview, the draft banner must never reach the artifact.
    forbidden = [] if args.drafts is not None else draft_markers(site)
    site_dir = Path(args.site_dir)
    issues = check_pages_present(site_dir, public_urls(site)) + check_anchor_aliases(site_dir, site.anchor_aliases)
    if args.production:
        extra, url_issues = _production_checks(site, site_dir)
        forbidden += extra
        issues += url_issues
    return _report(check_artifact(site_dir, forbidden=forbidden) + issues)


def _cmd_check(args) -> int:
    forbidden = [line.strip() for line in Path(args.forbid).read_text(encoding="utf-8").splitlines() if line.strip()] if args.forbid else []
    site_dir = Path(args.site_dir)
    issues = []
    if args.production and args.source is None:
        print("refused: --production needs --source (site URL and draft markers come from the source)")
        return 1
    if args.source is not None:
        site = load_site(Path(args.source), config_dir=Path(args.config_dir))
        forbidden += draft_markers(site)
        issues += check_pages_present(site_dir, public_urls(site)) + check_anchor_aliases(site_dir, site.anchor_aliases)
        if args.production:
            extra, url_issues = _production_checks(site, site_dir)
            forbidden += extra
            issues += url_issues
    return _report(check_artifact(site_dir, forbidden=forbidden) + issues)


def _cmd_production_status(args) -> int:
    status = production_status(Path(args.source))
    content = has_production_content(Path(args.source))
    print(("ready: " if status.ready else "error: " if status.error else "not ready: ") + status.reason)
    print("production content: " + ("found" if content else "none yet"))
    if os.environ.get("GITHUB_ACTIONS") and (status.error or status.reason.startswith("unpublished")):
        level = "error" if status.error else "warning"
        print(f"::{level} title=Publication state::{status.reason}")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            # ready: the launch gate (deploy). content: anything CI must validate and build.
            out.write(f"ready={'true' if status.ready else 'false'}\ncontent={'true' if content else 'false'}\n")
    return 1 if status.error else 0


def _cmd_check_tracked(args) -> int:
    if args.from_file:
        paths = Path(args.from_file).read_text(encoding="utf-8").splitlines()
    else:
        paths = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    return _report(check_tracked_paths(paths))


def _cmd_check_materials(args) -> int:
    site = load_site(Path(args.source), config_dir=Path(args.config_dir))
    return _report(check_materials(site, GitResolver([Path(r) for r in args.repos_root])))


def _cmd_repositories(args) -> int:
    site = load_site(Path(args.source), config_dir=Path(args.config_dir))
    for repo in referenced_repositories(site):
        print(f"{repo.id} {repo.url}")
    return 0


def _cmd_urls(args) -> int:
    urls = public_urls(load_site(Path(args.source), config_dir=Path(args.config_dir)))
    if args.write:
        target = Path(args.source) / "data/published-urls.txt"
        target.write_text("\n".join(urls) + "\n", encoding="utf-8")
        print(f"wrote {len(urls)} URL(s) to {target}")
    else:
        print("\n".join(urls))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="teaching-hub")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="validate data/ and content/")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--drafts", type=Path, help="private drafts directory (local preview only)")
    p.set_defaults(func=_cmd_validate)

    p = sub.add_parser("build", help="validate, assemble, render and check")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--renderer", choices=["zensical", "material"], default="zensical")
    p.add_argument("--build-dir", default="build")
    p.add_argument("--site-dir", default="_site")
    p.add_argument("--drafts", type=Path, help="include private drafts (local preview only; refused in CI)")
    p.add_argument("--production", action="store_true",
                   help="publishable build: refuses the test fixture and drafts; adds production artifact checks")
    p.set_defaults(func=_cmd_build)

    p = sub.add_parser("check", help="check a composed artifact")
    p.add_argument("--site-dir", default="_site")
    p.add_argument("--forbid", help="file with strings that must not appear in the artifact")
    p.add_argument("--source", help="site source; its draft banner texts must not appear in the artifact")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--production", action="store_true", help="also apply the production artifact checks")
    p.set_defaults(func=_cmd_check)

    p = sub.add_parser("production-status", help="report whether approved production content exists (launch gate)")
    p.add_argument("--source", default=".")
    p.add_argument("--github-output", help="append ready=true|false to this file (GitHub Actions step output)")
    p.set_defaults(func=_cmd_production_status)

    p = sub.add_parser("check-tracked", help="fail if private files are tracked by Git")
    p.add_argument("--from-file", help="read the path list from a file instead of git ls-files")
    p.set_defaults(func=_cmd_check_tracked)

    p = sub.add_parser("check-materials", help="verify repository/ref/path of materials in local clones (read-only)")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--repos-root", action="append", required=True)
    p.set_defaults(func=_cmd_check_materials)

    p = sub.add_parser("repositories", help="list repositories referenced by materials: '<id> <url>' per line")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.set_defaults(func=_cmd_repositories)

    p = sub.add_parser("urls", help="list public URLs or write data/published-urls.txt")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=_cmd_urls)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
