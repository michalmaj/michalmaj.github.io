"""Interface strings live in data/i18n/<lang>.yml."""

from .loader import Site

# Keys the pipeline reads. Every key must exist in every language file.
REQUIRED_KEYS = frozenset(
    {
        "site_name_home", "site_name_courses", "space_courses", "nav_home", "nav_licensing",
        "nav_catalog", "nav_how_to_use", "task_set", "task", "task_sets", "tasks_count", "guides",
        "used_materials", "course_sets_count", "optional", "duration", "minutes", "requires", "ref",
        "archived_title", "archived_text", "replaced_by", "draft_title", "draft_text",
        "other_language", "other_language_home", "maturity_in_development", "maturity_archived",
        "lang_pl", "lang_en", "footer_courses", "footer_home", "licensing_third_party",
        "licensing_repositories", "licensing_repository", "licensing_code", "licensing_content", "none",
        "not_found_title", "not_found_text", "section_materials", "section_tasks",
        "breadcrumb", "material_language", "theme_to_light", "theme_to_dark", "theme_to_auto",
        "space_courses_description",
    }
)


def t(site: Site, lang: str, key: str) -> str:
    return site.i18n[lang][key]
