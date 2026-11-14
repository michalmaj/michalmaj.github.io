"""Data model of the site. Independent of any renderer."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LANGS: tuple[str, ...] = ("pl", "en")
Lang = Literal["pl", "en"]
Maturity = Literal["not_assessed", "in_development", "stable", "maintenance", "archived"]
Status = Literal["published", "archived"]

# SPDX identifiers accepted in repository and third-party entries.
# Extend deliberately when a new license is actually encountered.
SPDX_ALLOWED = frozenset(
    {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0"}
)

# Course ids become URL segments under /courses/; these collide with pipeline
# pages or renderer output directories.
RESERVED_COURSE_IDS = frozenset({"how-to-use", "assets", "search", "stylesheets", "javascripts", "404"})
# Top-level URL segments owned by the site.
RESERVED_TOP_LEVEL = frozenset({"courses", "for-employers", "en", "licensing", "assets", "search"})


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Localized(Strict):
    pl: str | None = None
    en: str | None = None

    def get(self, lang: str) -> str | None:
        return getattr(self, lang)


class Course(Strict):
    id: str
    name: Localized
    summary: Localized = Localized()
    order: int | None = None


class Licenses(Strict):
    code: str | None = None
    content: str | None = None


class Repository(Strict):
    id: str
    name: str
    url: str = Field(pattern=r"^https://github\.com/[^/\s]+/[^/\s]+$")
    default_branch: str
    maturity: Maturity = "not_assessed"
    description: Localized = Localized()
    technologies: list[str] = []
    content_languages: list[Lang] = []
    licenses: Licenses | None = None
    documentation_url: str | None = None
    demo_url: str | None = None


class RepoMaterial(Strict):
    repository: str
    path: str | None = None
    ref: str | None = None
    lang: Lang
    label: str


class ExternalMaterial(Strict):
    url: str = Field(pattern=r"^https://\S+$")
    lang: Lang
    label: str


Material = RepoMaterial | ExternalMaterial


class TaskMeta(Strict):
    optional: bool = False
    materials: list[Material] = []


class TaskSetMeta(Strict):
    title: str
    summary: str | None = None
    status: Status
    estimated_duration_minutes: int | None = Field(default=None, gt=0)
    requires: list[str] = []
    materials: list[Material] = []
    tasks: dict[str, TaskMeta] = {}
    replaced_by: str | None = None


class GuideMeta(Strict):
    title: str
    summary: str | None = None
    status: Status
    order: int | None = None
    materials: list[Material] = []


class ThirdPartyItem(Strict):
    kind: Literal["asset", "excerpt"]
    path: str | None = None
    used_in: str | None = None
    title: str
    author: str
    source_url: str
    license: str
    changes: str | None = None


class AnchorAlias(Strict):
    """A published heading anchor that changed: `anchor` keeps leading to the heading `target`."""

    page: str  # public URL of the page, e.g. /licensing/
    anchor: str
    target: str


class SpaceConfig(Strict):
    enabled: bool
    path: str
    site_name_key: str | None = None
    footer_key: str | None = None
