"""The maintainer guide must describe the system as it is: commands, files, issue codes and keys exist."""

import re

from conftest import REPO

GUIDE = REPO / "docs" / "adding-content.md"
SOURCE = "\n".join(p.read_text(encoding="utf-8") for p in (REPO / "src" / "teaching_hub").glob("*.py"))


def guide() -> str:
    return GUIDE.read_text(encoding="utf-8")


def test_every_command_in_the_guide_exists():
    commands = set(re.findall(r"teaching-hub ([a-z][a-z-]+)", guide()))
    defined = set(re.findall(r'sub\.add_parser\("([a-z-]+)"', SOURCE))
    assert commands and commands <= defined, commands - defined


def test_every_repository_path_in_the_guide_exists():
    # Items (a line with its indented continuation) that call a file optional describe files a site may not have yet.
    items = [item for item in re.split(r"\n(?=\S)", guide()) if "optional" not in item]
    paths = {p for p in re.findall(r"`((?:data|renderer|src|tests|content|docs|assets)/[^`\s<>…]*|\.gitignore)`", "\n".join(items))
             if "<" not in p and "*" not in p and not p.startswith(("content/", "assets/"))}
    missing = sorted(p for p in paths if not (REPO / p.rstrip("/")).exists())
    assert paths and not missing, missing


def test_every_issue_code_in_the_guide_is_reported_by_the_pipeline():
    codes = set(re.findall(r"\(`([a-z]+(?:-[a-z]+)+)`\)", guide()))
    unknown = sorted(c for c in codes if f'"{c}"' not in SOURCE)
    assert codes and not unknown, unknown


def test_interface_string_keys_in_the_guide_exist():
    keys = set(re.findall(r"`(section_[a-z]+)`", guide()))
    pl = (REPO / "data/i18n/pl.yml").read_text(encoding="utf-8")
    assert keys and all(re.search(rf"^{k}:", pl, re.M) for k in keys), keys


def test_readme_links_the_guide():
    assert "docs/adding-content.md" in (REPO / "README.md").read_text(encoding="utf-8")
