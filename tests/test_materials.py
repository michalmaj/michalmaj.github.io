from conftest import error_codes, warning_codes
from teaching_hub.loader import load_site
from teaching_hub.materials import check_materials


class FakeResolver:
    """Records lookups; answers from a fixed table. None = repository not available."""

    def __init__(self, missing=(), unavailable=()):
        self.missing = set(missing)
        self.unavailable = set(unavailable)
        self.calls: list[tuple[str, str, str]] = []

    def __call__(self, repo_id: str, ref: str, path: str):
        self.calls.append((repo_id, ref, path))
        if repo_id in self.unavailable:
            return None
        return (repo_id, ref, path) not in self.missing


def test_all_sample_materials_resolve(sample):
    assert check_materials(load_site(sample), FakeResolver()) == []


def test_missing_path_at_ref_is_an_error(sample):
    resolver = FakeResolver(missing={("mechatronic-systems-programming", "module-01-start", "src")})
    issues = check_materials(load_site(sample), resolver)
    assert error_codes(issues) == {"material-missing"}
    assert [i.path for i in issues] == ["content/pl/courses/sample-course-a/task-sets/01-alpha.md"]


def test_default_branch_is_used_when_ref_is_omitted(sample):
    resolver = FakeResolver()
    check_materials(load_site(sample), resolver)
    assert ("software-engineering-in-practice", "main", "START-HERE.pl.md") in resolver.calls
    assert ("mechatronic-systems-programming", "module-01-start", "src") in resolver.calls


def test_unavailable_repository_is_a_warning_not_an_error(sample):
    issues = check_materials(load_site(sample), FakeResolver(unavailable={"deep-learning"}))
    assert warning_codes(issues) == {"material-unverified"}
    assert error_codes(issues) == set()


# ---------------------------------------------------------------- links in page text


from conftest import write  # noqa: E402
from teaching_hub.materials import referenced_repositories  # noqa: E402

MECH = "https://github.com/michalmaj/mechatronic-systems-programming"
LINKED_TEXT = f"""Tekst.

| Moduł | Dokumentacja | Kod |
|---|---|---|
| 0 | [dokumentacja]({MECH}/tree/main/course/module_00_tooling) | brak tagu |
| 1 | [dokumentacja]({MECH}/tree/main/course/module_01_control_basics) | [`module-01-start`]({MECH}/tree/module-01-start) |

[README]({MECH}/blob/main/README.md#szybki-start) · [repozytorium]({MECH}) · [zgłoszenia]({MECH}/issues)
· [inne repozytorium](https://github.com/someone/elsewhere/tree/main/x)
"""


def test_links_in_page_text_to_registered_repositories_are_checked(sample):
    write(sample / "content/pl/courses/sample-course-a/index.md", LINKED_TEXT)
    resolver = FakeResolver()
    assert check_materials(load_site(sample), resolver) == []
    for call in (("mechatronic-systems-programming", "main", "course/module_00_tooling"),
                 ("mechatronic-systems-programming", "main", "course/module_01_control_basics"),
                 ("mechatronic-systems-programming", "module-01-start", ""),
                 ("mechatronic-systems-programming", "main", "README.md"),
                 ("mechatronic-systems-programming", "main", "")):
        assert call in resolver.calls, call
    assert not any(repo == "elsewhere" or path == "issues" for repo, _, path in resolver.calls)


def test_a_missing_path_or_tag_linked_in_page_text_is_an_error(sample):
    write(sample / "content/pl/courses/sample-course-a/index.md", LINKED_TEXT)
    resolver = FakeResolver(missing={("mechatronic-systems-programming", "module-01-start", "")})
    issues = check_materials(load_site(sample), resolver)
    assert error_codes(issues) == {"repository-link-missing"}
    assert [i.path for i in issues] == ["content/pl/courses/sample-course-a/index.md"]
    assert "module-01-start" in issues[0].message


def test_a_repository_linked_only_in_page_text_is_cloned_for_the_check(sample):
    text = f"[DL](https://github.com/michalmaj/deep-learning/tree/main/lectures)\n"
    write(sample / "content/pl/courses/sample-course-b/index.md", text)
    write(sample / "content/pl/courses/sample-course-a/task-sets/01-alpha.md",
          (sample / "content/pl/courses/sample-course-a/task-sets/01-alpha.md").read_text(encoding="utf-8")
          .replace("repository: deep-learning", "repository: python-dev-setup-for-beginners"))
    site = load_site(sample)
    assert "deep-learning" in [repo.id for repo in referenced_repositories(site)]
    issues = check_materials(site, FakeResolver(unavailable={"deep-learning"}))
    assert warning_codes(issues) == {"repository-link-unverified"}


# ---------------------------------------------------------------- solutions and reference answers

import re  # noqa: E402

from conftest import REPO, replace_in  # noqa: E402
from teaching_hub.mdtools import link_targets  # noqa: E402

# Source repositories keep solutions, model answers and rubrics in public. The site sends students
# to the instructions and never links those files or tags directly.
ANSWERS = re.compile(r"solution|exemplar|rubric", re.I)
ALPHA = "content/pl/courses/sample-course-a/task-sets/01-alpha.md"


def answer_links(root) -> list[tuple[str, str]]:
    """(page, target) for each material or link in page text that leads to a solution or a reference answer."""
    found = []
    for doc in load_site(root).docs:
        targets = link_targets(doc.body)
        if doc.meta is not None:
            materials = list(getattr(doc.meta, "materials", []))
            for task in getattr(doc.meta, "tasks", {}).values():
                materials += task.materials
            for m in materials:
                targets += [v for v in (getattr(m, "path", None), getattr(m, "ref", None), getattr(m, "url", None)) if v]
        found += [(doc.rel, target) for target in targets if ANSWERS.search(target)]
    return found


def test_published_content_links_no_solutions_or_reference_answers():
    assert answer_links(REPO) == []


def test_a_material_or_a_link_leading_to_an_answer_is_noticed(sample):
    rubric = "https://github.com/michalmaj/data-science-casebook/blob/main/ASSESSMENT_RUBRIC.pl.md"
    assert answer_links(sample) == []
    replace_in(sample / ALPHA, "path: labs/01-workstation/README.pl.md", "path: labs/01-workstation/solution.py")
    replace_in(sample / ALPHA, "ref: module-01-start", "ref: module-01-solution")
    replace_in(sample / ALPHA, "Tekst zastępczy czynności. Zobacz", f"[Rubryka]({rubric}). Zobacz")
    assert sorted(answer_links(sample)) == [
        (ALPHA, rubric), (ALPHA, "labs/01-workstation/solution.py"), (ALPHA, "module-01-solution"),
    ]
