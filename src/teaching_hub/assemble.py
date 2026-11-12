"""Turn a validated Site into one renderer input per (language, space).

Output per build: <out>/<lang>/<space>/docs/ (plain Markdown) and mkdocs.yml.
Only published/archived material is written; drafts only in local preview.
"""

import copy
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import markup as m
from .i18n import t
from .loader import Doc, Site
from .mdtools import find_section, task_headings
from .models import LANGS, ExternalMaterial, RepoMaterial
from .urls import (
    doc_url,
    lang_prefix,
    space_has_content,
    space_root,
    task_set_url,
    visible_courses,
)


class PreviewNotAllowed(RuntimeError):
    """Raised when draft preview is requested in CI."""


@dataclass(frozen=True)
class Build:
    lang: str
    space: str
    prefix: str  # public URL path of the build root, e.g. "/en/courses/"
    root: Path  # <out>/<lang>/<space>

    @property
    def config_path(self) -> Path:
        return self.root / "mkdocs.yml"

    @property
    def site_dir(self) -> Path:
        return self.root / "site"


# ---------------------------------------------------------------- helpers


def _other(lang: str) -> str:
    return next(other for other in LANGS if other != lang)


def _in_build(doc: Doc, include_drafts: bool) -> bool:
    return doc.status in ("published", "archived") or (include_drafts and doc.draft)


def _listed(doc: Doc, include_drafts: bool) -> bool:
    return doc.status == "published" or (include_drafts and doc.draft)


def _lang_badge(site: Site, lang: str, material_lang: str) -> str:
    return m.lang_badge(t(site, lang, f"lang_{material_lang}"), t(site, lang, "material_language"))


def _maturity_badge(site: Site, lang: str, repo) -> str | None:
    key = f"maturity_{repo.maturity}"
    return m.badge(m.esc(t(site, lang, key)), "status") if key in site.i18n[lang] else None


def _material_line(site: Site, lang: str, material) -> str:
    if isinstance(material, ExternalMaterial):
        return f"- [{material.label}]({material.url}) " + m.meta([_lang_badge(site, lang, material.lang)])
    repo = site.repositories[material.repository]
    ref = material.ref or repo.default_branch
    if material.path:
        kind = "tree" if material.path.endswith("/") else "blob"
        url = f"{repo.url}/{kind}/{ref}/{material.path.rstrip('/')}"
    else:
        url = repo.url if material.ref is None else f"{repo.url}/tree/{ref}"
    parts = [f'<span class="th-material__repo">{m.esc(repo.name)}</span>']
    if ref != repo.default_branch:
        parts.append(m.badge(f"{m.esc(t(site, lang, 'ref'))} `{ref}`", "ref"))
    parts.append(_maturity_badge(site, lang, repo))
    parts.append(_lang_badge(site, lang, material.lang))
    return f"- [{material.label}]({url}) " + m.meta(parts)


def _material_block(site: Site, lang: str, materials, css_class: str = "th-materials", label: str | None = None) -> list[str]:
    lines = [_material_line(site, lang, item) for item in materials]
    if label:
        lines = [f'<p class="th-label">{m.esc(label)}</p>', "", *lines]
    return m.block(css_class, lines)


def _switch(site: Site, lang: str, url: str | None, include_drafts: bool) -> str | None:
    """Link to the other-language version (or the other home page)."""
    other = _other(lang)
    if url is not None:
        return f"[{t(site, lang, 'other_language')}]({url}){{ lang={other} .th-lang-switch }}"
    if space_has_content(site, "home", other):
        return f"[{t(site, lang, 'other_language_home')}]({space_root(other, '')}){{ lang={other} .th-lang-switch }}"
    return None


def _crumbs(site: Site, lang: str, links: list[str]) -> str:
    return m.breadcrumbs(t(site, lang, "breadcrumb"), links)


def _front(search_exclude: bool, hide: tuple[str, ...] = ()) -> str:
    return m.front_matter(search_exclude, hide)


def _set_title(site: Site, lang: str, doc: Doc) -> str:
    return f"{t(site, lang, 'task_set')} {doc.position} · {doc.meta.title}"


# ---------------------------------------------------------------- pages


def _task_set_page(site: Site, doc: Doc, include_drafts: bool) -> str:
    lang, meta = doc.lang, doc.meta
    course = site.courses[doc.course_id]
    other = _other(lang)
    twin = site.find("task_set", other, doc.course_id, doc.slug)
    twin_url = task_set_url(other, doc.course_id, doc.slug) if twin and _listed(twin, False) else None

    crumbs = _crumbs(site, lang, [f"[{t(site, lang, 'nav_catalog')}](../../index.md)", f"[{course.name.get(lang)}](../index.md)"])
    switch = _switch(site, lang, twin_url, include_drafts)
    header = [m.page_marker("task-set"), "", *m.pagebar(crumbs, switch), f"# {_set_title(site, lang, doc)}", ""]
    if doc.draft:
        header += [f'!!! danger "{t(site, lang, "draft_title")}"', f"    {t(site, lang, 'draft_text')}", ""]
    if meta.status == "archived":
        text = t(site, lang, "archived_text")
        if meta.replaced_by:
            text += f" [{t(site, lang, 'replaced_by')}]({meta.replaced_by}.md)"
        header += [f'!!! warning "{t(site, lang, "archived_title")}"', f"    {text}", ""]
    facts = []
    if meta.estimated_duration_minutes:
        facts.append(f"{t(site, lang, 'duration')}: {meta.estimated_duration_minutes} {t(site, lang, 'minutes')}")
    if meta.requires:
        siblings = {d.slug: d for d in site.by_kind("task_set", lang, doc.course_id)}
        links = ", ".join(f"[{_set_title(site, lang, siblings[s])}]({s}.md)" for s in meta.requires)
        facts.append(f"{t(site, lang, 'requires')}: {links}")
    if facts:
        header += [*m.paragraph(" · ".join(facts), "th-meta"), ""]

    lines = doc.body.splitlines()
    tasks_heading = t(site, lang, "section_tasks")
    materials_heading = t(site, lang, "section_materials")
    section = find_section(lines, tasks_heading)
    insert_before: dict[int, list[str]] = {}
    insert_after: dict[int, list[str]] = {}
    replace: dict[int, str] = {}
    for number, task in enumerate(task_headings(lines, section), start=1):
        task_meta = meta.tasks.get(task.id)
        title = f"{t(site, lang, 'task')} {number}. {task.title}"
        if task_meta and task_meta.optional:
            title += " " + m.optional_badge(t(site, lang, "optional"))
        replace[task.line] = f"### {title} {{#{task.id}}}"
        if task_meta and task_meta.materials:
            insert_after[task.line] = [
                "",
                *_material_block(site, lang, task_meta.materials, "th-materials th-materials--task", materials_heading),
            ]

    if meta.materials:
        block = _material_block(site, lang, meta.materials)
        existing = find_section(lines, materials_heading)
        if existing is not None:
            insert_after[existing[0]] = ["", *block]
        else:
            insert_before[section[0]] = [f"## {materials_heading}", "", *block, ""]

    body: list[str] = []
    for i, line in enumerate(lines):
        body.extend(insert_before.get(i, []))
        body.append(replace.get(i, line))
        body.extend(insert_after.get(i, []))
    return _front(meta.status == "archived") + "\n".join(header + body).rstrip() + "\n"


def _guide_page(site: Site, doc: Doc, include_drafts: bool) -> str:
    lang = doc.lang
    course = site.courses[doc.course_id]
    other = _other(lang)
    twin = site.find("guide", other, doc.course_id, doc.slug)
    twin_url = doc_url(twin) if twin and _listed(twin, False) else None
    crumbs = _crumbs(site, lang, [f"[{t(site, lang, 'nav_catalog')}](../../index.md)", f"[{course.name.get(lang)}](../index.md)"])
    switch = _switch(site, lang, twin_url, include_drafts)
    out = [m.page_marker("guide"), "", *m.pagebar(crumbs, switch), f"# {doc.meta.title}", ""]
    if doc.draft:
        out += [f'!!! danger "{t(site, lang, "draft_title")}"', f"    {t(site, lang, 'draft_text')}", ""]
    if doc.meta.status == "archived":
        out += [f'!!! warning "{t(site, lang, "archived_title")}"', f"    {t(site, lang, 'archived_text')}", ""]
    if doc.meta.materials:
        out += [f"## {t(site, lang, 'section_materials')}", "", *_material_block(site, lang, doc.meta.materials), ""]
    out.append(doc.body.strip())
    return _front(doc.meta.status == "archived") + "\n".join(out).rstrip() + "\n"


def _used_repositories(site: Site, docs: list[Doc]) -> list[str]:
    seen: list[str] = []
    for doc in docs:
        materials = list(doc.meta.materials)
        for task in getattr(doc.meta, "tasks", {}).values():
            materials += task.materials
        for item in materials:
            if isinstance(item, RepoMaterial) and item.repository not in seen:
                seen.append(item.repository)
    return seen


def _course_page(site: Site, lang: str, course_id: str, include_drafts: bool) -> str:
    course = site.courses[course_id]
    other = _other(lang)
    twin_url = f"{lang_prefix(other)}/courses/{course_id}/" if course_id in visible_courses(site, other) else None
    switch = _switch(site, lang, twin_url, include_drafts)
    crumbs = _crumbs(site, lang, [f"[{t(site, lang, 'nav_catalog')}](../index.md)"])
    out = [m.page_marker("course"), "", *m.pagebar(crumbs, switch), f"# {course.name.get(lang)}", ""]
    if course.summary.get(lang):
        out += [*m.paragraph(course.summary.get(lang), "th-lead"), ""]
    index = site.find("course_index", lang, course_id)
    if index is not None and index.body.strip():
        out += [index.body.strip(), ""]

    sets = sorted((d for d in site.by_kind("task_set", lang, course_id) if _listed(d, include_drafts)), key=lambda d: d.position)
    if sets:
        cards: list[str] = []
        for doc in sets:
            facts = []
            if doc.meta.estimated_duration_minutes:
                facts.append(f"{doc.meta.estimated_duration_minutes} {t(site, lang, 'minutes')}")
            count = len(task_headings(doc.body.splitlines(), find_section(doc.body.splitlines(), t(site, lang, "section_tasks"))))
            facts.append(f"{t(site, lang, 'tasks_count')}: {count}")
            card = [
                f'<p class="th-eyebrow">{m.esc(t(site, lang, "task_set"))} {doc.position}</p>',
                "",
                f"### [{doc.meta.title}](task-sets/{doc.slug}.md)",
                "",
            ]
            if doc.meta.summary:
                card += [doc.meta.summary, ""]
            card.append(f'<p class="th-card__meta">{m.esc(" · ".join(facts))}</p>')
            cards += [*m.block("th-card th-card--set", card), ""]
        out += [f"## {t(site, lang, 'task_sets')}", "", *m.block("th-cards th-cards--sets", cards), ""]
    guides = sorted((d for d in site.by_kind("guide", lang, course_id) if _listed(d, include_drafts)), key=lambda d: (d.meta.order is None, d.meta.order or 0, d.slug))
    if guides:
        cards = []
        for d in guides:
            card = [f"### [{d.meta.title}](guides/{d.slug}.md)", ""]
            if d.meta.summary:
                card.append(d.meta.summary)
            cards += [*m.block("th-card th-card--guide", card), ""]
        out += [f"## {t(site, lang, 'guides')}", "", *m.block("th-cards th-cards--guides", cards), ""]
    repos = _used_repositories(site, sets + guides)
    if repos:
        lines = []
        for repo_id in repos:
            repo = site.repositories[repo_id]
            parts = [_lang_badge(site, lang, code) for code in repo.content_languages]
            parts.append(_maturity_badge(site, lang, repo))
            lines.append(f"- [{repo.name}]({repo.url}) " + m.meta(parts))
        out += [f"## {t(site, lang, 'used_materials')}", "", *m.block("th-repos", lines), ""]
    return "\n".join(out).rstrip() + "\n"


def _catalog_page(site: Site, lang: str, include_drafts: bool) -> str:
    other = _other(lang)
    twin_url = space_root(other, "courses") if space_has_content(site, "courses", other) else None
    switch = _switch(site, lang, twin_url, include_drafts)
    out = [m.page_marker("catalog"), "", *m.pagebar(None, switch), f"# {t(site, lang, 'nav_catalog')}", ""]
    index = site.find("catalog_index", lang)
    if index is not None and index.body.strip():
        out += [index.body.strip(), ""]
    cards: list[str] = []
    for course_id in visible_courses(site, lang, include_drafts):
        course = site.courses[course_id]
        count = sum(1 for d in site.by_kind("task_set", lang, course_id) if _listed(d, include_drafts))
        card = [f"## [{course.name.get(lang)}]({course_id}/index.md)", ""]
        if course.summary.get(lang):
            card += [course.summary.get(lang), ""]
        card.append(f'<p class="th-card__meta">{m.esc(t(site, lang, "course_sets_count"))}: {count}</p>')
        cards += [*m.block("th-card", card), ""]
    out += m.block("th-cards", cards)
    return _front(False, hide=("toc",)) + "\n".join(out).rstrip() + "\n"


def _home_page(site: Site, lang: str, include_drafts: bool) -> str:
    doc = site.find("home", lang)
    other = _other(lang)
    twin_url = space_root(other, "") if space_has_content(site, "home", other) else None
    switch = _switch(site, lang, twin_url, include_drafts)
    out = [m.page_marker("home"), "", *m.pagebar(None, switch), doc.body.strip(), ""]
    cards: list[str] = []
    if space_has_content(site, "courses", lang, include_drafts):
        card = [f"## [{t(site, lang, 'space_courses')}]({space_root(lang, 'courses')})", "", t(site, lang, "space_courses_description")]
        cards += [*m.block("th-card th-card--space", card), ""]
    if cards:
        out += m.block("th-cards th-cards--spaces", cards)
    return _front(False, hide=("navigation", "toc")) + "\n".join(out).rstrip() + "\n"


def _licensing_page(site: Site, lang: str) -> str:
    doc = site.find("licensing", lang)
    out = [m.page_marker("licensing"), "", doc.body.strip(), "", f"## {t(site, lang, 'licensing_third_party')}", ""]
    if site.third_party:
        for item in site.third_party:
            out.append(f"- {item.title} — {item.author} · [{item.source_url}]({item.source_url}) · {item.license}")
    else:
        out.append(t(site, lang, "none"))
    out += ["", f"## {t(site, lang, 'licensing_repositories')}", ""]
    published = [d for d in site.docs if d.kind in ("task_set", "guide") and d.status == "published"]
    repos = _used_repositories(site, published)
    if repos:
        out += [f"| | {t(site, lang, 'licensing_code')} | {t(site, lang, 'licensing_content')} |", "|---|---|---|"]
        for repo_id in repos:
            repo = site.repositories[repo_id]
            lic = repo.licenses
            out.append(f"| [{repo.name}]({repo.url}) | {(lic and lic.code) or '—'} | {(lic and lic.content) or '—'} |")
    else:
        out.append(t(site, lang, "none"))
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- builds


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


THEME_CSS = ("tokens.css", "theme.css")
THEME_URL = "stylesheets/teaching-hub"


def _copy_theme(site: Site, space: str, docs: Path) -> list[str]:
    """Copy the shared stylesheets (and an optional space-specific one) into a build; return extra CSS."""
    source = site.config_dir / "theme"
    names = [*THEME_CSS]
    if (source / f"space-{space}.css").is_file():
        names.append(f"space-{space}.css")
    target = docs / THEME_URL
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        if (source / name).is_file():
            shutil.copyfile(source / name, target / name)
    return [f"{THEME_URL}/{name}" for name in names[len(THEME_CSS):]]


def _palette(site: Site, lang: str) -> list[dict]:
    """Native colour scheme toggle: system → light → dark → system."""
    custom = {"primary": "custom", "accent": "custom"}
    return [
        {"media": "(prefers-color-scheme)", **custom,
         "toggle": {"icon": "material/brightness-auto", "name": t(site, lang, "theme_to_light")}},
        {"media": "(prefers-color-scheme: light)", "scheme": "default", **custom,
         "toggle": {"icon": "material/brightness-7", "name": t(site, lang, "theme_to_dark")}},
        {"media": "(prefers-color-scheme: dark)", "scheme": "slate", **custom,
         "toggle": {"icon": "material/brightness-4", "name": t(site, lang, "theme_to_auto")}},
    ]


def _config(site: Site, lang: str, space: str, nav: list, not_in_nav: list[str], extra_css: list[str] = ()) -> dict:
    base = yaml.safe_load((site.config_dir / "base.yml").read_text(encoding="utf-8")) or {}
    cfg = copy.deepcopy(base)
    cfg["extra_css"] = [*cfg.get("extra_css", []), *extra_css]
    space_cfg = site.spaces[space]
    licensing_lang = lang if site.find("licensing", lang) and space_has_content(site, "home", lang) else "pl"
    licensing_url = f"{lang_prefix(licensing_lang)}/licensing/"
    cfg.update(
        site_name=t(site, lang, space_cfg.site_name_key),
        site_url=site.settings["site_url"].rstrip("/") + space_root(lang, space_cfg.path),
        docs_dir="docs",
        site_dir="site",
        nav=nav,
    )
    cfg.setdefault("theme", {})["language"] = lang
    cfg["theme"]["palette"] = _palette(site, lang)
    if space_cfg.footer_key:
        cfg["copyright"] = t(site, lang, space_cfg.footer_key).format(licensing_url=licensing_url)
    if not_in_nav:
        cfg["not_in_nav"] = "\n".join(not_in_nav) + "\n"
    return cfg


def _home_build(site: Site, lang: str, root: Path, include_drafts: bool) -> list:
    docs = root / "docs"
    _write(docs / "index.md", _home_page(site, lang, include_drafts))
    nav = [{t(site, lang, "nav_home"): "index.md"}]
    if site.find("licensing", lang):
        _write(docs / "licensing.md", _licensing_page(site, lang))
        nav.append({t(site, lang, "nav_licensing"): "licensing.md"})
    return nav


def _courses_build(site: Site, lang: str, root: Path, include_drafts: bool) -> tuple[list, list[str]]:
    docs = root / "docs"
    _write(docs / "index.md", _catalog_page(site, lang, include_drafts))
    nav: list = [{t(site, lang, "nav_catalog"): "index.md"}]
    how_to = site.find("how_to_use", lang)
    if how_to is not None:
        _write(docs / "how-to-use.md", how_to.body)
        nav.append({t(site, lang, "nav_how_to_use"): "how-to-use.md"})
    hidden: list[str] = []
    for course_id in visible_courses(site, lang, include_drafts):
        course = site.courses[course_id]
        _write(docs / course_id / "index.md", _course_page(site, lang, course_id, include_drafts))
        entries: list = [{course.name.get(lang): f"{course_id}/index.md"}]
        for doc in sorted(site.by_kind("task_set", lang, course_id), key=lambda d: d.position):
            if not _in_build(doc, include_drafts):
                continue
            rel = f"{course_id}/task-sets/{doc.slug}.md"
            _write(docs / rel, _task_set_page(site, doc, include_drafts))
            if _listed(doc, include_drafts):
                entries.append({_set_title(site, lang, doc): rel})
            else:
                hidden.append(f"/{rel}")
        for doc in sorted(site.by_kind("guide", lang, course_id), key=lambda d: (d.meta.order is None, d.meta.order or 0, d.slug)):
            if not _in_build(doc, include_drafts):
                continue
            rel = f"{course_id}/guides/{doc.slug}.md"
            _write(docs / rel, _guide_page(site, doc, include_drafts))
            if _listed(doc, include_drafts):
                entries.append({doc.meta.title: rel})
            else:
                hidden.append(f"/{rel}")
        nav.append({course.name.get(lang): entries})
    return nav, hidden


def assemble(site: Site, out_dir: Path, include_drafts: bool = False) -> list[Build]:
    if include_drafts and (os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")):
        raise PreviewNotAllowed("draft preview is a local-only mode and is refused in CI")
    out_dir = Path(out_dir)
    builds: list[Build] = []
    for lang in LANGS:
        for space in ("home", "courses"):
            if not space_has_content(site, space, lang, include_drafts):
                continue
            root = out_dir / lang / space
            if space == "home":
                nav, hidden = _home_build(site, lang, root, include_drafts), []
            else:
                nav, hidden = _courses_build(site, lang, root, include_drafts)
            extra_css = _copy_theme(site, space, root / "docs")
            cfg = _config(site, lang, space, nav, hidden, extra_css)
            _write(root / "mkdocs.yml", yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False))
            builds.append(Build(lang, space, space_root(lang, site.spaces[space].path), root))
    return builds
