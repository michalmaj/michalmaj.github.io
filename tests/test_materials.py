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
