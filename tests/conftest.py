import shutil
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "sample"


@pytest.fixture(autouse=True)
def _outside_ci(monkeypatch):
    """Run every test as a local run; tests that need CI set the variables themselves."""
    for name in ("CI", "GITHUB_ACTIONS"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def sample(tmp_path: Path) -> Path:
    """A writable copy of the placeholder sample site with the real renderer config."""
    root = tmp_path / "site"
    shutil.copytree(FIXTURE, root)
    shutil.copytree(REPO / "renderer", root / "renderer")
    return root


def make_production_like(root: Path) -> Path:
    """Rename the fixture's placeholder identifiers inside a temporary copy.

    Production builds refuse the fixture's markers, so tests of the production path need content
    without them. Only the copy under tmp_path is changed; nothing here is real course content.
    """
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".yml"):
            text = path.read_text(encoding="utf-8")
            # The English fixture name "Sample course A" would also yield the heading id "sample-course-a".
            text = text.replace("sample-course-", "demo-course-").replace("[EN placeholder] Sample course", "Demo course")
            path.write_text(text, encoding="utf-8")
    for directory in sorted(root.rglob("sample-course-*"), reverse=True):
        directory.rename(directory.with_name(directory.name.replace("sample-course-", "demo-course-")))
    return root


def error_codes(issues) -> set[str]:
    return {i.code for i in issues if i.level == "error"}


def warning_codes(issues) -> set[str]:
    return {i.code for i in issues if i.level == "warning"}


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture text not found in {path}: {old!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
