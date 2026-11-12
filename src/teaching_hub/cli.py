"""Command line: teaching-hub <command> [options]."""

import argparse
import subprocess
import sys
from pathlib import Path

from .check import check_artifact, check_tracked_paths
from .loader import load_site
from .materials import GitResolver, check_materials
from .render import RenderError, build_site
from .urls import public_urls
from .validate import validate


def _report(issues) -> int:
    for issue in issues:
        print(issue)
    errors = sum(1 for i in issues if i.level == "error")
    warnings = len(issues) - errors
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def _cmd_validate(args) -> int:
    return _report(validate(load_site(Path(args.source), drafts=args.drafts, config_dir=Path(args.config_dir))))


def _cmd_build(args) -> int:
    site = load_site(Path(args.source), drafts=args.drafts, config_dir=Path(args.config_dir))
    issues = validate(site)
    if _report(issues):
        return 1
    try:
        results = build_site(site, Path(args.build_dir), Path(args.site_dir), args.renderer, include_drafts=args.drafts is not None)
    except RenderError as exc:
        print(exc)
        return 1
    for r in results:
        print(f"built {r.build.prefix:<14} with {args.renderer} in {r.seconds:.2f}s")
    return _report(check_artifact(Path(args.site_dir)))


def _cmd_check(args) -> int:
    forbidden = [line.strip() for line in Path(args.forbid).read_text(encoding="utf-8").splitlines() if line.strip()] if args.forbid else []
    return _report(check_artifact(Path(args.site_dir), forbidden=forbidden))


def _cmd_check_tracked(args) -> int:
    if args.from_file:
        paths = Path(args.from_file).read_text(encoding="utf-8").splitlines()
    else:
        paths = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    return _report(check_tracked_paths(paths))


def _cmd_check_materials(args) -> int:
    site = load_site(Path(args.source), config_dir=Path(args.config_dir))
    return _report(check_materials(site, GitResolver([Path(r) for r in args.repos_root])))


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
    p.set_defaults(func=_cmd_build)

    p = sub.add_parser("check", help="check a composed artifact")
    p.add_argument("--site-dir", default="_site")
    p.add_argument("--forbid", help="file with strings that must not appear in the artifact")
    p.set_defaults(func=_cmd_check)

    p = sub.add_parser("check-tracked", help="fail if private files are tracked by Git")
    p.add_argument("--from-file", help="read the path list from a file instead of git ls-files")
    p.set_defaults(func=_cmd_check_tracked)

    p = sub.add_parser("check-materials", help="verify repository/ref/path of materials in local clones (read-only)")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--repos-root", action="append", required=True)
    p.set_defaults(func=_cmd_check_materials)

    p = sub.add_parser("urls", help="list public URLs or write data/published-urls.txt")
    p.add_argument("--source", default=".")
    p.add_argument("--config-dir", default="renderer", help="renderer configuration (default: ./renderer)")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=_cmd_urls)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
