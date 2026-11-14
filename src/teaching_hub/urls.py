"""Visibility rules for courses and spaces, and the public URLs they produce."""

from .loader import Doc, Site
from .models import LANGS


def lang_prefix(lang: str) -> str:
    return "" if lang == "pl" else f"/{lang}"


def space_root(lang: str, space_path: str) -> str:
    return f"{lang_prefix(lang)}/{space_path}/" if space_path else f"{lang_prefix(lang)}/"


def _in_build(doc: Doc, include_drafts: bool) -> bool:
    return doc.status in ("published", "archived") or (include_drafts and doc.draft)


def has_description(site: Site, course, lang: str) -> bool:
    """An approved description: a summary in data/courses.yml or a non-empty course index page."""
    index = site.find("course_index", lang, course.id)
    return bool(course.summary.get(lang)) or (index is not None and bool(index.body.strip()))


def has_published_material(site: Site, course_id: str, lang: str, include_drafts: bool = False) -> bool:
    return any(
        d.status == "published" or (include_drafts and d.draft)
        for kind in ("task_set", "guide")
        for d in site.by_kind(kind, lang, course_id)
    )


def visible_courses(site: Site, lang: str, include_drafts: bool = False) -> list[str]:
    """Course ids visible in `lang`, in catalog order.

    A course is published in a language only when it has a name, a description and at least one
    published task set or guide in that language: no empty course pages.
    """
    visible = [
        course
        for course in site.courses.values()
        if course.name.get(lang)
        and has_description(site, course, lang)
        and has_published_material(site, course.id, lang, include_drafts)
    ]
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


def has_repository_catalog(site: Site, lang: str) -> bool:
    """The repository catalog exists in a language with its page text and at least one registered repository."""
    return bool(site.repositories) and site.find("repositories_index", lang) is not None


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
            if has_repository_catalog(site, lang):
                urls.append(f"{lang_prefix(lang)}/courses/repositories/")
            for course_id in visible_courses(site, lang):
                urls.append(f"{lang_prefix(lang)}/courses/{course_id}/")
                for kind in ("task_set", "guide"):
                    for doc in site.by_kind(kind, lang, course_id):
                        if _in_build(doc, include_drafts=False):
                            urls.append(doc_url(doc))
    return urls
