"""Visibility rules for courses and spaces, and the public URLs they produce."""

from .loader import Doc, Site
from .models import LANGS


def lang_prefix(lang: str) -> str:
    return "" if lang == "pl" else f"/{lang}"


def space_root(lang: str, space_path: str) -> str:
    return f"{lang_prefix(lang)}/{space_path}/" if space_path else f"{lang_prefix(lang)}/"


def _in_build(doc: Doc, include_drafts: bool) -> bool:
    return doc.status in ("published", "archived") or (include_drafts and doc.draft)


def visible_courses(site: Site, lang: str, include_drafts: bool = False) -> list[str]:
    """Course ids visible in `lang`, in catalog order."""
    visible = []
    for course in site.courses.values():
        if not course.name.get(lang):
            continue
        has_description = bool(course.summary.get(lang)) or site.find("course_index", lang, course.id) is not None
        has_material = any(
            d.status == "published" or (include_drafts and d.draft)
            for kind in ("task_set", "guide")
            for d in site.by_kind(kind, lang, course.id)
        )
        if has_description or has_material:
            visible.append(course)
    visible.sort(key=lambda c: (c.order is None, c.order or 0))
    return [c.id for c in visible]


def space_enabled(site: Site, space: str) -> bool:
    cfg = site.spaces.get(space)
    return bool(cfg and cfg.enabled)


def space_has_content(site: Site, space: str, lang: str, include_drafts: bool = False) -> bool:
    """A space is built and linked only when it has approved public content (§8.1)."""
    if not space_enabled(site, space):
        return False
    if space == "home":
        return site.find("home", lang) is not None
    if space == "courses":
        return bool(visible_courses(site, lang, include_drafts))
    return False


def task_set_url(lang: str, course_id: str, slug: str) -> str:
    return f"{lang_prefix(lang)}/courses/{course_id}/task-sets/{slug}/"


def guide_url(lang: str, course_id: str, slug: str) -> str:
    return f"{lang_prefix(lang)}/courses/{course_id}/guides/{slug}/"


def doc_url(doc: Doc) -> str | None:
    if doc.kind == "task_set":
        return task_set_url(doc.lang, doc.course_id, doc.slug)
    if doc.kind == "guide":
        return guide_url(doc.lang, doc.course_id, doc.slug)
    return None


def public_urls(site: Site) -> list[str]:
    """Every URL the public build produces (published and archived pages)."""
    urls: list[str] = []
    for lang in LANGS:
        if space_has_content(site, "home", lang):
            urls.append(space_root(lang, ""))
            if site.find("licensing", lang):
                urls.append(f"{lang_prefix(lang)}/licensing/")
        if space_has_content(site, "courses", lang):
            urls.append(space_root(lang, "courses"))
            if site.find("how_to_use", lang):
                urls.append(f"{lang_prefix(lang)}/courses/how-to-use/")
            for course_id in visible_courses(site, lang):
                urls.append(f"{lang_prefix(lang)}/courses/{course_id}/")
                for kind in ("task_set", "guide"):
                    for doc in site.by_kind(kind, lang, course_id):
                        if _in_build(doc, include_drafts=False):
                            urls.append(doc_url(doc))
    return urls
