"""Load data/, content/ and renderer/ into a Site. Load problems become Issues."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ValidationError

from .issues import Issue, error
from .mdtools import FrontMatterError, split_front_matter
from .models import (
    LANGS,
    SLUG_RE,
    AnchorAlias,
    Course,
    GuideMeta,
    Repository,
    SpaceConfig,
    TaskSetMeta,
    ThirdPartyItem,
)

DocKind = Literal[
    "home", "licensing", "catalog_index", "how_to_use", "repositories_index", "course_index", "task_set", "guide",
    "employers",
]

_LANG = "(?P<lang>" + "|".join(LANGS) + ")"
_PATTERNS: list[tuple[DocKind, re.Pattern[str]]] = [
    ("home", re.compile(rf"^{_LANG}/home/index\.md$")),
    ("licensing", re.compile(rf"^{_LANG}/home/licensing\.md$")),
    ("catalog_index", re.compile(rf"^{_LANG}/courses/index\.md$")),
    ("how_to_use", re.compile(rf"^{_LANG}/courses/how-to-use\.md$")),
    ("repositories_index", re.compile(rf"^{_LANG}/courses/repositories\.md$")),
    ("course_index", re.compile(rf"^{_LANG}/courses/(?P<course>[^/]+)/index\.md$")),
    ("task_set", re.compile(rf"^{_LANG}/courses/(?P<course>[^/]+)/task-sets/(?P<name>[^/]+)\.md$")),
    ("guide", re.compile(rf"^{_LANG}/courses/(?P<course>[^/]+)/guides/(?P<name>[^/]+)\.md$")),
    ("employers", re.compile(rf"^{_LANG}/for-employers/.+$")),
]
_TASK_SET_NAME = re.compile(r"^(?P<pos>\d{2})-(?P<slug>.+)$")
_IGNORED_FILES = {".DS_Store"}


@dataclass
class Doc:
    kind: DocKind
    lang: str
    rel: str
    body: str
    course_id: str | None = None
    slug: str | None = None
    position: int | None = None
    meta: TaskSetMeta | GuideMeta | None = None
    draft: bool = False

    @property
    def status(self) -> str:
        if self.draft:
            return "draft"
        return self.meta.status if self.meta is not None else "published"


@dataclass
class Site:
    root: Path
    config_dir: Path
    settings: dict
    spaces: dict[str, SpaceConfig]
    courses: dict[str, Course]
    repositories: dict[str, Repository]
    i18n: dict[str, dict[str, str]]
    third_party: list[ThirdPartyItem]
    docs: list[Doc]
    url_registry: list[str] | None
    issues: list[Issue] = field(default_factory=list)
    anchor_aliases: list[AnchorAlias] = field(default_factory=list)

    def by_kind(self, kind: DocKind, lang: str | None = None, course: str | None = None) -> list[Doc]:
        return [
            d
            for d in self.docs
            if d.kind == kind and (lang is None or d.lang == lang) and (course is None or d.course_id == course)
        ]

    def find(self, kind: DocKind, lang: str, course: str | None = None, slug: str | None = None) -> Doc | None:
        for d in self.by_kind(kind, lang, course):
            if slug is None or d.slug == slug:
                return d
        return None


def _read_yaml(path: Path, rel: str, issues: list[Issue], default):
    if not path.exists():
        return default
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        issues.append(error("schema", rel, f"invalid YAML: {exc}"))
        return default
    return default if data is None else data


def _model_list(items, model: type[BaseModel], rel: str, issues: list[Issue]) -> list:
    out = []
    if not isinstance(items, list):
        issues.append(error("schema", rel, "expected a list"))
        return out
    for n, item in enumerate(items):
        try:
            out.append(model.model_validate(item))
        except ValidationError as exc:
            issues.append(error("schema", f"{rel}[{n}]", _short(exc)))
    return out


def _short(exc: ValidationError) -> str:
    return "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()[:3])


def _by_id(items: list, rel: str, issues: list[Issue]) -> dict:
    out: dict = {}
    for item in items:
        if item.id in out:
            issues.append(error("duplicate-id", rel, f"duplicate id {item.id!r}"))
        out[item.id] = item
    return out


def _load_doc(path: Path, content_root: Path, root: Path, issues: list[Issue], draft: bool) -> Doc | None:
    rel_content = path.relative_to(content_root).as_posix()
    rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
    for kind, pattern in _PATTERNS:
        match = pattern.match(rel_content)
        if match:
            break
    else:
        issues.append(error("unexpected-file", rel, "file does not match any content location"))
        return None

    groups = match.groupdict()
    doc = Doc(kind=kind, lang=groups["lang"], rel=rel, body="", course_id=groups.get("course"), draft=draft)
    if kind == "employers":
        return doc

    try:
        front, body = split_front_matter(path.read_text(encoding="utf-8"))
    except (FrontMatterError, yaml.YAMLError) as exc:
        issues.append(error("schema", rel, str(exc)))
        return None
    doc.body = body

    if kind in ("task_set", "guide"):
        name = groups["name"]
        if kind == "task_set":
            named = _TASK_SET_NAME.match(name)
            if not named:
                issues.append(error("bad-slug", rel, "task set file must be named NN-<slug>.md"))
                return None
            doc.position, doc.slug = int(named.group("pos")), named.group("slug")
        else:
            doc.slug = name
        if not SLUG_RE.match(doc.slug):
            issues.append(error("bad-slug", rel, f"slug {doc.slug!r} must be lowercase ASCII with hyphens"))
            return None
        front = front or {}
        if front.get("status") == "draft" and not draft:
            issues.append(error("draft-in-content", rel, "drafts belong to the private drafts directory"))
            return None
        if draft:
            front = {**front, "status": front.get("status", "published")}
        model = TaskSetMeta if kind == "task_set" else GuideMeta
        try:
            doc.meta = model.model_validate(front)
        except ValidationError as exc:
            issues.append(error("schema", rel, _short(exc)))
            return None
    elif front is not None:
        issues.append(error("schema", rel, "this page takes Markdown only, without front matter"))
    return doc


def _load_content(content_root: Path, root: Path, issues: list[Issue], draft: bool) -> list[Doc]:
    docs = []
    if not content_root.exists():
        return docs
    for path in sorted(p for p in content_root.rglob("*") if p.is_file()):
        if path.name in _IGNORED_FILES:
            continue
        doc = _load_doc(path, content_root, root, issues, draft)
        if doc is not None:
            docs.append(doc)
    return docs


REQUIRED_SPACES = ("home", "courses", "for-employers")
# Published heading anchors that changed, kept as aliases (slugs.py).
ANCHOR_ALIASES = "data/anchor-aliases.yml"


def load_site(root: Path, drafts: Path | None = None, config_dir: Path | None = None) -> Site:
    """Load a site source tree.

    `drafts` (private, local preview only) overlays content/.
    `config_dir` holds renderer/pipeline configuration; defaults to <root>/renderer.
    """
    root = Path(root)
    config_dir = Path(config_dir) if config_dir is not None else root / "renderer"
    issues: list[Issue] = []

    for required in ("site.yml", "base.yml"):
        if not (config_dir / required).is_file():
            issues.append(error("missing-config", str(config_dir / required), "renderer configuration file is missing"))
    settings = _read_yaml(config_dir / "site.yml", "renderer/site.yml", issues, {})
    spaces: dict[str, SpaceConfig] = {}
    for path in sorted((config_dir / "spaces").glob("*.yml")):
        rel = f"renderer/spaces/{path.name}"
        try:
            spaces[path.stem] = SpaceConfig.model_validate(_read_yaml(path, rel, issues, {}))
        except ValidationError as exc:
            issues.append(error("schema", rel, _short(exc)))
    for name in REQUIRED_SPACES:
        if name not in spaces:
            issues.append(error("missing-config", f"renderer/spaces/{name}.yml", "space configuration is missing"))

    courses_raw = _read_yaml(root / "data/courses.yml", "data/courses.yml", issues, {}).get("courses", [])
    courses = _by_id(_model_list(courses_raw, Course, "data/courses.yml", issues), "data/courses.yml", issues)
    repos_raw = _read_yaml(root / "data/repositories.yml", "data/repositories.yml", issues, {}).get(
        "repositories", []
    )
    repositories = _by_id(
        _model_list(repos_raw, Repository, "data/repositories.yml", issues), "data/repositories.yml", issues
    )
    i18n = {lang: _read_yaml(root / f"data/i18n/{lang}.yml", f"data/i18n/{lang}.yml", issues, {}) for lang in LANGS}
    tp_raw = _read_yaml(root / "data/third-party.yml", "data/third-party.yml", issues, {}).get("items", [])
    third_party = _model_list(tp_raw, ThirdPartyItem, "data/third-party.yml", issues)

    aliases_raw = _read_yaml(root / ANCHOR_ALIASES, ANCHOR_ALIASES, issues, {}).get("aliases", [])
    anchor_aliases = _model_list(aliases_raw, AnchorAlias, ANCHOR_ALIASES, issues)

    registry_path = root / "data/published-urls.txt"
    registry = None
    if registry_path.exists():
        lines = registry_path.read_text(encoding="utf-8").splitlines()
        registry = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    docs = _load_content(root / "content", root, issues, draft=False)
    if drafts is not None:
        overlay = _load_content(Path(drafts), Path(drafts).parent, issues, draft=True)
        replaced = {(d.kind, d.lang, d.course_id, d.slug) for d in overlay}
        docs = [d for d in docs if (d.kind, d.lang, d.course_id, d.slug) not in replaced] + overlay

    return Site(root, config_dir, settings, spaces, courses, repositories, i18n, third_party, docs, registry, issues,
                anchor_aliases)
