"""Course visibility: published material of a course that cannot be shown must be reported."""

from conftest import error_codes, write
from test_validate import MINIMAL_SET, run




def test_published_material_of_a_course_without_description_is_reported(sample):
    # Course C has a name but no description: its published task set would silently disappear.
    write(sample / "content/pl/courses/sample-course-c/task-sets/01-first.md", MINIMAL_SET)
    issues = run(sample)
    assert "course-not-visible" in error_codes(issues)
    assert [i.path for i in issues if i.code == "course-not-visible"] == [
        "content/pl/courses/sample-course-c/task-sets/01-first.md"
    ]


def test_published_material_needs_the_course_name_in_its_language(sample):
    # Course B has no English name, so an English guide could not be published.
    write(sample / "content/en/courses/sample-course-b/guides/overview.md", "---\ntitle: x\nstatus: published\n---\n\nText.\n")
    assert "course-not-visible" in error_codes(run(sample))


def test_complete_courses_raise_no_visibility_error(sample):
    assert "course-not-visible" not in error_codes(run(sample))
