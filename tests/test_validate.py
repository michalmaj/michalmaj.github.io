from pathlib import Path

from conftest import error_codes, replace_in, warning_codes, write
from teaching_hub.loader import load_site
from teaching_hub.validate import validate

ALPHA_PL = "content/pl/courses/sample-course-a/task-sets/01-alpha.md"
ALPHA_EN = "content/en/courses/sample-course-a/task-sets/01-alpha.md"
BETA_PL = "content/pl/courses/sample-course-a/task-sets/02-beta.md"

MINIMAL_SET = """---
title: "x"
status: published
---

## Zadania

### Zadanie {#t1}

Tekst.
"""


def run(root: Path):
    return validate(load_site(root))


def test_sample_site_is_valid(sample):
    # Catches false positives, e.g. a heading inside a code block parsed as a task.
    issues = run(sample)
    assert error_codes(issues) == set()
    assert warning_codes(issues) == set()


def test_unknown_front_matter_key_is_rejected(sample):
    replace_in(sample / ALPHA_PL, "status: published", "status: published\ncolour: red")
    assert "schema" in error_codes(run(sample))


def test_draft_status_is_not_allowed_in_content(sample):
    replace_in(sample / ALPHA_PL, "status: published", "status: draft")
    assert "draft-in-content" in error_codes(run(sample))


def test_task_set_of_unknown_course_is_rejected(sample):
    write(sample / "content/pl/courses/no-such-course/task-sets/01-x.md", MINIMAL_SET)
    assert "unknown-course" in error_codes(run(sample))


def test_slug_must_be_lowercase_ascii(sample):
    write(sample / "content/pl/courses/sample-course-a/task-sets/03-Zadania_Ł.md", MINIMAL_SET)
    assert "bad-slug" in error_codes(run(sample))


def test_slug_is_unique_within_course_and_language(sample):
    write(sample / "content/pl/courses/sample-course-a/task-sets/03-alpha.md", MINIMAL_SET)
    assert "duplicate-slug" in error_codes(run(sample))


def test_position_is_unique_within_course_and_language(sample):
    write(sample / "content/pl/courses/sample-course-a/task-sets/01-gamma.md", MINIMAL_SET)
    assert "duplicate-position" in error_codes(run(sample))


def test_same_slug_in_other_language_is_a_translation_not_a_duplicate(sample):
    # 01-alpha.md exists in pl and en; that must not be reported.
    assert "duplicate-slug" not in error_codes(run(sample))


def test_unknown_repository_is_rejected(sample):
    replace_in(sample / ALPHA_PL, "repository: deep-learning", "repository: no-such-repo")
    assert "unknown-repository" in error_codes(run(sample))


def test_requires_must_point_to_existing_set(sample):
    replace_in(sample / ALPHA_PL, "status: published", "status: published\nrequires: [ghost]")
    assert "unknown-reference" in error_codes(run(sample))


def test_replaced_by_only_on_archived_set(sample):
    replace_in(sample / ALPHA_PL, "status: published", "status: published\nreplaced_by: beta")
    assert "replaced-by-not-archived" in error_codes(run(sample))


def test_replaced_by_must_point_to_existing_set(sample):
    replace_in(sample / BETA_PL, "replaced_by: alpha", "replaced_by: ghost")
    assert "unknown-reference" in error_codes(run(sample))


def test_tasks_section_is_required(sample):
    replace_in(sample / ALPHA_PL, "## Zadania", "## Coś innego")
    assert "missing-tasks-section" in error_codes(run(sample))


def test_tasks_section_heading_follows_page_language(sample):
    # A Polish heading in an English page is not the English tasks section.
    replace_in(sample / ALPHA_EN, "## Tasks", "## Zadania")
    assert "missing-tasks-section" in error_codes(run(sample))


def test_task_heading_needs_explicit_id(sample):
    replace_in(sample / ALPHA_PL, "zadania drugiego {#a2}", "zadania drugiego")
    assert "task-without-id" in error_codes(run(sample))


def test_task_metadata_must_match_a_heading(sample):
    replace_in(sample / ALPHA_PL, "  a3:\n    optional: true", "  zz:\n    optional: true")
    assert "task-meta-without-heading" in error_codes(run(sample))


def test_task_id_is_unique_within_set(sample):
    replace_in(sample / ALPHA_PL, "zadania drugiego {#a2}", "zadania drugiego {#a1}")
    assert "duplicate-task-id" in error_codes(run(sample))


def test_local_filesystem_paths_are_rejected(sample):
    replace_in(sample / ALPHA_PL, "Tekst zastępczy celu.", "Zobacz ../python/deep-learning/README.md")
    assert "local-path" in error_codes(run(sample))


def test_repository_maturity_defaults_to_not_assessed(sample):
    replace_in(sample / "data/repositories.yml", "    maturity: not_assessed\n    technologies: [Markdown]", "    technologies: [Markdown]")
    site = load_site(sample)
    assert site.repositories["python-dev-setup-for-beginners"].maturity == "not_assessed"


def test_unknown_maturity_value_is_rejected(sample):
    replace_in(sample / "data/repositories.yml", "maturity: in_development", "maturity: beta")
    assert "schema" in error_codes(run(sample))


def test_unknown_license_identifier_is_rejected(sample):
    replace_in(sample / "data/repositories.yml", "content: CC-BY-SA-4.0}", "content: CC-BY-SA}")
    assert "bad-license" in error_codes(run(sample))


def test_interface_string_missing_in_one_language(sample):
    replace_in(sample / "data/i18n/en.yml", 'task: "Task"\n', "")
    assert "i18n-missing-key" in error_codes(run(sample))


def test_third_party_file_needs_registry_entry(sample):
    write(sample / "assets/third-party/diagram.svg", "<svg/>")
    assert "third-party-unregistered" in error_codes(run(sample))


def test_third_party_excerpt_must_point_to_existing_page(sample):
    write(
        sample / "data/third-party.yml",
        "items:\n"
        "  - kind: excerpt\n"
        "    used_in: content/pl/courses/sample-course-a/task-sets/09-ghost.md\n"
        "    title: t\n    author: a\n    source_url: https://example.org\n    license: CC-BY-4.0\n",
    )
    assert "third-party-missing-target" in error_codes(run(sample))


def test_differing_task_ids_between_translations_is_a_warning(sample):
    replace_in(sample / ALPHA_EN, "optional task {#a3}", "optional task {#a9}")
    issues = run(sample)
    assert "translation-task-mismatch" in warning_codes(issues)
    assert error_codes(issues) == set()


def test_course_id_cannot_be_a_reserved_name(sample):
    replace_in(sample / "data/courses.yml", "id: sample-course-c", "id: how-to-use")
    assert "reserved-name" in error_codes(run(sample))


def test_unexpected_file_in_content_is_rejected(sample):
    write(sample / "content/pl/random-page.md", "# x\n")
    assert "unexpected-file" in error_codes(run(sample))


def test_unsupported_language_directory_is_rejected(sample):
    write(sample / "content/de/home/index.md", "# x\n")
    assert "unexpected-file" in error_codes(run(sample))


def test_content_in_disabled_employer_space_is_reported(sample):
    write(sample / "content/en/for-employers/index.md", "# x\n")
    assert "space-disabled" in warning_codes(run(sample))


def test_missing_renderer_configuration_is_an_error(sample):
    # Without space configuration nothing would be built; that must not pass silently.
    import shutil

    shutil.rmtree(sample / "renderer")
    assert "missing-config" in error_codes(run(sample))


def test_published_url_cannot_disappear(sample):
    write(
        sample / "data/published-urls.txt",
        "/courses/sample-course-a/task-sets/alpha/\n/courses/sample-course-a/task-sets/gone/\n",
    )
    issues = run(sample)
    removed = [i for i in issues if i.code == "url-removed"]
    assert [i.path for i in removed] == ["/courses/sample-course-a/task-sets/gone/"]
