"""Verify that every (repository, ref, path) referenced by published content exists.

The resolver is injected: CI can use the GitHub API or a link checker; local
runs can use GitResolver, which only reads local clones (no fetch, no writes).
"""

import subprocess
from collections.abc import Callable
from pathlib import Path

from .issues import Issue, error, warning
from .loader import Site
from .models import RepoMaterial, Repository

# resolver(repo_id, ref, path) -> True (exists) | False (missing) | None (cannot verify)
Resolver = Callable[[str, str, str], bool | None]


def _materials(doc):
    found = list(doc.meta.materials)
    for task in getattr(doc.meta, "tasks", {}).values():
        found += task.materials
    return found


def referenced_repositories(site: Site) -> list[Repository]:
    """Registered repositories that task sets or guides refer to (any status), in registry order."""
    used = {
        m.repository
        for doc in site.docs
        if doc.kind in ("task_set", "guide") and doc.meta is not None
        for m in _materials(doc)
        if isinstance(m, RepoMaterial)
    }
    return [repo for repo_id, repo in site.repositories.items() if repo_id in used]


def check_materials(site: Site, resolver: Resolver) -> list[Issue]:
    issues: list[Issue] = []
    for doc in site.docs:
        if doc.kind not in ("task_set", "guide") or doc.meta is None:
            continue
        for m in _materials(doc):
            if not isinstance(m, RepoMaterial) or m.repository not in site.repositories:
                continue
            ref = m.ref or site.repositories[m.repository].default_branch
            path = (m.path or "").rstrip("/")
            found = resolver(m.repository, ref, path)
            target = f"{m.repository}@{ref}:{path or '/'}"
            if found is None:
                issues.append(warning("material-unverified", doc.rel, f"{target} could not be checked"))
            elif not found:
                issues.append(error("material-missing", doc.rel, f"{target} does not exist"))
    return issues


class GitResolver:
    """Read-only lookups in local clones found under the given roots.

    Branches are resolved through the local remote-tracking ref (origin/<branch>),
    never the working tree, because local checkouts may differ from origin/main.
    Remote-tracking refs are only as fresh as the last fetch.
    """

    def __init__(self, roots: list[Path]):
        self.roots = [Path(r).expanduser() for r in roots]

    def _clone(self, repo_id: str) -> Path | None:
        for root in self.roots:
            candidate = root / repo_id
            if (candidate / ".git").exists():
                return candidate
        return None

    def _git(self, clone: Path, *args: str) -> bool:
        proc = subprocess.run(["git", "-C", str(clone), *args], capture_output=True, text=True)
        return proc.returncode == 0

    def _commitish(self, clone: Path, ref: str) -> str | None:
        for candidate in (f"refs/tags/{ref}", f"refs/remotes/origin/{ref}"):
            if self._git(clone, "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"):
                return candidate
        return None

    def __call__(self, repo_id: str, ref: str, path: str) -> bool | None:
        clone = self._clone(repo_id)
        if clone is None:
            return None
        commitish = self._commitish(clone, ref)
        if commitish is None:
            return False
        if not path:
            return True
        return self._git(clone, "cat-file", "-e", f"{commitish}:{path}")
