"""Production publishing: the launch gate and guards against publishing test data."""

from dataclasses import dataclass
from pathlib import Path

# The site is published only once approved production content exists; the Polish home page is the switch.
HOME_PAGE = "content/pl/home/index.md"
# Public URLs of the published site. "/" in it means the site has been launched.
URL_REGISTRY = "data/published-urls.txt"

# Identifiers that exist only in the placeholder test fixture. They must never reach the published site,
# even if fixture files are copied out of tests/.
FIXTURE_MARKERS = ("sample-course-", "[EN placeholder]")


# Production content: pages, course and repository data, the URL registry and site assets.
# Code, renderer configuration and interface strings (data/i18n/) alone are not content.
CONTENT_DIRS = ("content", "assets")
CONTENT_FILES = ("data/courses.yml", "data/repositories.yml", "data/third-party.yml", "data/published-urls.txt", "data/anchor-aliases.yml")
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


@dataclass(frozen=True)
class PublicationStatus:
    ready: bool  # deploy
    error: bool  # inconsistent publication state: stop, never skip quietly
    reason: str


def read_url_registry(root: Path) -> list[str] | None:
    path = Path(root) / URL_REGISTRY
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def production_status(root: Path) -> PublicationStatus:
    """Whether the repository holds approved production content to publish.

    The home page opens the launch gate; the URL registry records that the site has been published.
    Losing the home page of a published site is an error, not a skipped deployment: the last
    deployment would stay online while every check is green. Unpublishing is a conscious change that
    also removes the home page from the registry.
    """
    root = Path(root)
    home = (root / HOME_PAGE).is_file()
    registry = read_url_registry(root)
    launched = registry is not None and "/" in registry
    if home and launched:
        return PublicationStatus(True, False, "approved production content found")
    if home:
        return PublicationStatus(False, True, (
            f"{HOME_PAGE} exists, but {URL_REGISTRY} does not record the home page '/'; "
            "record the public URLs with `teaching-hub urls --write` and commit the file before publishing"))
    if launched:
        return PublicationStatus(False, True, (
            f"the published home page {HOME_PAGE} is missing while {URL_REGISTRY} still lists '/'; "
            f"restore the page, or unpublish on purpose: remove the home page and its URLs from {URL_REGISTRY} "
            "in the same change and disable GitHub Pages in the repository settings"))
    if registry is not None:
        return PublicationStatus(False, False, (
            f"unpublished: {URL_REGISTRY} does not list the home page '/', so nothing will be deployed; "
            "a previous deployment stays online until GitHub Pages is disabled in the repository settings"))
    return PublicationStatus(False, False, f"no approved production content yet ({HOME_PAGE} is missing); nothing will be deployed")


def is_test_fixture(source: Path) -> bool:
    parts = Path(source).resolve().parts
    return any(parts[i : i + 2] == ("tests", "fixtures") for i in range(len(parts) - 1))
