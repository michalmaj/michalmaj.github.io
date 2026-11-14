"""Verify that every (repository, ref, path) referenced by published content exists.

Two kinds of references are checked: materials in the front matter of task sets and guides, and
links in the text of any page to a file, directory or ref (tag or branch) of a registered
repository, e.g. `<repository>/tree/module-01-start` or `<repository>/blob/main/README.md`.

The resolver is injected: CI can use the GitHub API or a link checker; local
runs can use GitResolver, which only reads local clones (no fetch, no writes).
"""

import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .issues import Issue, error, warning
from .loader import Site
from .mdtools import link_targets
from .models import RepoMaterial, Repository

# resolver(repo_id, ref, path) -> True (exists) | False (missing) | None (cannot verify)
Resolver = Callable[[str, str, str], bool | None]


def _materials(doc):
    found = list(doc.meta.materials)
    for task in getattr(doc.meta, "tasks", {}).values():
        found += task.materials
    return found


_REF_PATH = re.compile(r"^/(?:tree|blob)/([^/]+)(?:/(.*))?$")


def _repository_links(site: Site, doc) -> list[tuple[str, str, str, str]]:
    """(repository id, ref, path, link) for links in a page's text into a registered repository.

    The repository itself, `/tree/<ref>[/<path>]` and `/blob/<ref>/<path>` are checked; other
    GitHub pages (issues, releases, …) cannot be read from a clone and are left out. A ref is one
    path segment (tags and branches without "/").
    """
    out = []
    if doc.kind == "employers":
        return out
    for link in link_targets(doc.body):
        parts = urlsplit(link)
        for repo in site.repositories.values():
            base = urlsplit(repo.url)
            if (parts.scheme, parts.netloc) != (base.scheme, base.netloc):
                continue
            if parts.path.rstrip("/") == base.path.rstrip("/"):
                out.append((repo.id, repo.default_branch, "", link))
            elif parts.path.startswith(base.path.rstrip("/") + "/"):
                match = _REF_PATH.match(parts.path[len(base.path.rstrip("/")):])
                if match:
                    out.append((repo.id, match.group(1), unquote(match.group(2) or "").rstrip("/"), link))
    return out


def referenced_repositories(site: Site) -> list[Repository]:
    """Registered repositories that materials or links in page text refer to, in registry order."""
    used = {
        m.repository
        for doc in site.docs
        if doc.kind in ("task_set", "guide") and doc.meta is not None
        for m in _materials(doc)
        if isinstance(m, RepoMaterial)
    }
    used |= {repo_id for doc in site.docs for repo_id, _, _, _ in _repository_links(site, doc)}
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
    for doc in site.docs:
        for repo_id, ref, path, link in _repository_links(site, doc):
            found = resolver(repo_id, ref, path)
            target = f"{repo_id}@{ref}:{path or '/'}"
            if found is None:
                issues.append(warning("repository-link-unverified", doc.rel, f"{target} could not be checked ({link})"))
            elif not found:
                issues.append(error("repository-link-missing", doc.rel, f"{target} does not exist ({link})"))
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
