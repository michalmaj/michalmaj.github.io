"""Production publishing: the launch gate and guards against publishing test data."""

from pathlib import Path

# The site is published only once approved production content exists; the Polish home page is the switch.
HOME_PAGE = "content/pl/home/index.md"

# Identifiers that exist only in the placeholder test fixture. They must never reach the published site,
# even if fixture files are copied out of tests/.
FIXTURE_MARKERS = ("sample-course-", "[EN placeholder]")


def production_status(root: Path) -> tuple[bool, str]:
    """(ready, reason): whether the repository holds approved production content to publish."""
    if (Path(root) / HOME_PAGE).is_file():
        return True, "approved production content found"
    return False, f"no approved production content yet ({HOME_PAGE} is missing); nothing will be deployed"


def is_test_fixture(source: Path) -> bool:
    parts = Path(source).resolve().parts
    return any(parts[i : i + 2] == ("tests", "fixtures") for i in range(len(parts) - 1))
