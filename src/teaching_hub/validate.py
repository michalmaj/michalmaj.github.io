"""Content and data validation rules. Renderer-independent."""

import re

from .i18n import REQUIRED_KEYS
from .issues import Issue, error, warning
from .loader import Doc, Site
from .mdtools import find_section, link_targets, task_headings
from .models import LANGS, RESERVED_COURSE_IDS, RESERVED_TOP_LEVEL, SLUG_RE, SPDX_ALLOWED, RepoMaterial
from .urls import public_urls

# Applied to link and image targets only, never to instruction text or code: a lab may well tell
# students to open http://localhost:8000 or to work in /home/student, but the published site must not
# link to files on the author's machine, to sibling repositories in the workspace, or to local services.
LOCAL_TARGET_RE = re.compile(
    r"^(?:file:|/Users/|/home/|[A-Za-z]:[\\/]|\\\\)"
    r"|(?:^|/)\.\./(?:python|cpp)/"
    r"|^[a-z][a-z0-9+.-]*://(?:localhost|127\.0\.0\.1|\[::1\])(?::\d+)?(?:/|$)",
    re.I,
)


def _outside_repository(path: str) -> bool:
    """A material path must be relative and stay inside its repository."""
    return (
        path.startswith(("/", "\\"))
        or re.match(r"^[A-Za-z]:", path) is not None
        or ".." in re.split(r"[\\/]", path)
        or path.lower().startswith("file:")
    )


def validate(site: Site) -> list[Issue]:
    issues = list(site.issues)
    issues += _check_courses(site)
    issues += _check_repositories(site)
    issues += _check_i18n(site)
    issues += _check_third_party(site)
    issues += _check_docs(site)
    issues += _check_translations(site)
    issues += _check_url_registry(site)
    return issues


def _check_courses(site: Site) -> list[Issue]:
    out = []
    for course in site.courses.values():
        if not SLUG_RE.match(course.id):
            out.append(error("bad-slug", "data/courses.yml", f"course id {course.id!r}"))
        if course.id in RESERVED_COURSE_IDS:
            out.append(error("reserved-name", "data/courses.yml", f"course id {course.id!r} is reserved"))
        if not course.name.pl:
            out.append(error("schema", "data/courses.yml", f"course {course.id!r} needs a Polish name"))
    return out


def _check_repositories(site: Site) -> list[Issue]:
    out = []
    for repo in site.repositories.values():
        if repo.id in RESERVED_TOP_LEVEL:
            out.append(error("reserved-name", "data/repositories.yml", f"repository {repo.id!r} collides with a site path"))
        for spdx in (repo.licenses.code, repo.licenses.content) if repo.licenses else ():
            if spdx is not None and spdx not in SPDX_ALLOWED:
                out.append(error("bad-license", "data/repositories.yml", f"{repo.id}: unknown SPDX id {spdx!r}"))
    return out


def _check_i18n(site: Site) -> list[Issue]:
    out = []
    for lang in LANGS:
        keys = set(site.i18n.get(lang) or {})
        for key in sorted(REQUIRED_KEYS - keys):
            out.append(error("i18n-missing-key", f"data/i18n/{lang}.yml", f"missing key {key!r}"))
    pl, en = set(site.i18n.get("pl") or {}), set(site.i18n.get("en") or {})
    for key in sorted(pl ^ en):
        lang = "en" if key in pl else "pl"
        out.append(error("i18n-missing-key", f"data/i18n/{lang}.yml", f"missing key {key!r}"))
    return out


def _check_third_party(site: Site) -> list[Issue]:
    out = []
    registered = {item.path for item in site.third_party if item.kind == "asset"}
    tp_dir = site.root / "assets/third-party"
    if tp_dir.exists():
        for path in sorted(p for p in tp_dir.rglob("*") if p.is_file() and p.name != ".DS_Store"):
            rel = path.relative_to(site.root).as_posix()
            if rel not in registered:
                out.append(error("third-party-unregistered", rel, "no entry in data/third-party.yml"))
    for item in site.third_party:
        target = item.path if item.kind == "asset" else item.used_in
        if not target or not (site.root / target).is_file():
            out.append(error("third-party-missing-target", "data/third-party.yml", f"{item.kind} target {target!r} not found"))
        if item.license not in SPDX_ALLOWED:
            out.append(warning("third-party-license", "data/third-party.yml", f"{item.title}: license {item.license!r} is not an SPDX id from the allowlist"))
    return out


def _materials(doc: Doc) -> list:
    if doc.meta is None:
        return []
    found = list(doc.meta.materials)
    for task in getattr(doc.meta, "tasks", {}).values():
        found += task.materials
    return found


def _check_docs(site: Site) -> list[Issue]:
    out = []
    seen_slug: dict[tuple, str] = {}
    seen_pos: dict[tuple, str] = {}
    for doc in site.docs:
        if doc.kind == "employers":
            if not (site.spaces.get("for-employers") and site.spaces["for-employers"].enabled):
                out.append(warning("space-disabled", doc.rel, "the for-employers space is reserved and disabled; file ignored"))
            continue
        if doc.course_id is not None and doc.course_id not in site.courses:
            out.append(error("unknown-course", doc.rel, f"course {doc.course_id!r} is not in data/courses.yml"))
        local = [target for target in link_targets(doc.body) if LOCAL_TARGET_RE.search(target)]
        if local:
            out.append(error("local-path", doc.rel, f"link to a local path or service: {local[0]}"))
        for material in _materials(doc):
            if isinstance(material, RepoMaterial):
                if material.repository not in site.repositories:
                    out.append(error("unknown-repository", doc.rel, f"repository {material.repository!r} is not registered"))
                if material.path and _outside_repository(material.path):
                    out.append(error("local-path", doc.rel, f"material path {material.path!r} leaves the repository"))
            elif LOCAL_TARGET_RE.search(material.url):
                out.append(error("local-path", doc.rel, f"material URL {material.url!r} points to a local service"))
        if doc.kind in ("task_set", "guide"):
            key = (doc.kind, doc.lang, doc.course_id, doc.slug)
            if key in seen_slug:
                out.append(error("duplicate-slug", doc.rel, f"slug {doc.slug!r} already used by {seen_slug[key]}"))
            seen_slug[key] = doc.rel
        if doc.kind == "task_set":
            pos_key = (doc.lang, doc.course_id, doc.position)
            if pos_key in seen_pos:
                out.append(error("duplicate-position", doc.rel, f"position {doc.position:02d} already used by {seen_pos[pos_key]}"))
            seen_pos[pos_key] = doc.rel
            out += _check_task_set(site, doc)
    return out


def _check_task_set(site: Site, doc: Doc) -> list[Issue]:
    out = []
    meta = doc.meta
    siblings = {d.slug: d for d in site.by_kind("task_set", doc.lang, doc.course_id)}
    for slug in meta.requires:
        if slug not in siblings:
            out.append(error("unknown-reference", doc.rel, f"requires {slug!r}: no such task set"))
    if meta.replaced_by is not None:
        if meta.status != "archived":
            out.append(error("replaced-by-not-archived", doc.rel, "replaced_by is only allowed on archived sets"))
        if meta.replaced_by not in siblings:
            out.append(error("unknown-reference", doc.rel, f"replaced_by {meta.replaced_by!r}: no such task set"))

    lines = doc.body.splitlines()
    heading = (site.i18n.get(doc.lang) or {}).get("section_tasks", "")
    section = find_section(lines, heading) if heading else None
    if section is None:
        out.append(error("missing-tasks-section", doc.rel, f"no '## {heading}' section"))
        return out
    ids: list[str] = []
    for task in task_headings(lines, section):
        if task.id is None:
            out.append(error("task-without-id", doc.rel, f"task heading {task.title!r} needs {{#id}}"))
            continue
        if not SLUG_RE.match(task.id):
            out.append(error("bad-slug", doc.rel, f"task id {task.id!r}"))
        if task.id in ids:
            out.append(error("duplicate-task-id", doc.rel, f"task id {task.id!r} repeats"))
        ids.append(task.id)
    if not ids:
        out.append(error("missing-tasks-section", doc.rel, "the tasks section has no tasks"))
    for task_id in meta.tasks:
        if task_id not in ids:
            out.append(error("task-meta-without-heading", doc.rel, f"tasks.{task_id} has no matching heading"))
    return out


def task_ids(site: Site, doc: Doc) -> set[str]:
    lines = doc.body.splitlines()
    heading = (site.i18n.get(doc.lang) or {}).get("section_tasks", "")
    section = find_section(lines, heading) if heading else None
    return {t.id for t in task_headings(lines, section) if t.id} if section else set()


def _check_translations(site: Site) -> list[Issue]:
    out = []
    pl_sets = {(d.course_id, d.slug): d for d in site.by_kind("task_set", "pl")}
    for doc in site.by_kind("task_set", "en"):
        twin = pl_sets.get((doc.course_id, doc.slug))
        if twin is not None and task_ids(site, twin) != task_ids(site, doc):
            out.append(warning("translation-task-mismatch", doc.rel, "task ids differ from the Polish version"))
    return out


def _check_url_registry(site: Site) -> list[Issue]:
    if site.url_registry is None:
        return []
    current = set(public_urls(site))
    return [
        error("url-removed", url, "published URL is no longer produced and has no redirect")
        for url in site.url_registry
        if url not in current
    ]
