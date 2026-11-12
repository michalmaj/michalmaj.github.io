import shutil
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "sample"


@pytest.fixture
def sample(tmp_path: Path) -> Path:
    """A writable copy of the placeholder sample site with the real renderer config."""
    root = tmp_path / "site"
    shutil.copytree(FIXTURE, root)
    shutil.copytree(REPO / "renderer", root / "renderer")
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
