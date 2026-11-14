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
