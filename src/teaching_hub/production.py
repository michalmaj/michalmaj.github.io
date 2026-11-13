"""Production publishing: the launch gate and guards against publishing test data."""

from pathlib import Path

# The site is published only once approved production content exists; the Polish home page is the switch.
HOME_PAGE = "content/pl/home/index.md"

# Identifiers that exist only in the placeholder test fixture. They must never reach the published site,
# even if fixture files are copied out of tests/.
FIXTURE_MARKERS = ("sample-course-", "[EN placeholder]")


# Production content: pages, course and repository data, the URL registry and site assets.
# Code, renderer configuration and interface strings (data/i18n/) alone are not content.
CONTENT_DIRS = ("content", "assets")
CONTENT_FILES = ("data/courses.yml", "data/repositories.yml", "data/third-party.yml", "data/published-urls.txt")
_IGNORED = {".DS_Store"}


def has_production_content(root: Path) -> bool:
    """Whether the repository holds production content that CI must validate and build.

    Independent of the launch gate: content without a home page is not deployed, but it is checked.
    """
    root = Path(root)
    if any((root / name).is_file() for name in CONTENT_FILES):
        return True
    return any(
        path.is_file() and path.name not in _IGNORED
        for directory in CONTENT_DIRS
        for path in (root / directory).rglob("*")
    )


def production_status(root: Path) -> tuple[bool, str]:
    """(ready, reason): whether the repository holds approved production content to publish."""
    if (Path(root) / HOME_PAGE).is_file():
        return True, "approved production content found"
    return False, f"no approved production content yet ({HOME_PAGE} is missing); nothing will be deployed"


def is_test_fixture(source: Path) -> bool:
    parts = Path(source).resolve().parts
    return any(parts[i : i + 2] == ("tests", "fixtures") for i in range(len(parts) - 1))
