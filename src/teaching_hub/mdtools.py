"""Minimal Markdown structure helpers: sections and task headings outside code fences."""

import re
from dataclasses import dataclass

import yaml

FENCE_RE = re.compile(r"^\s*(```|~~~)")
TASK_HEADING_RE = re.compile(r"^###\s+(?P<title>.+?)\s*\{#(?P<id>[^}\s]+)\}\s*$")


class FrontMatterError(ValueError):
    pass


def split_front_matter(text: str) -> tuple[dict | None, str]:
    """Return (front matter mapping or None, body)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        raise FrontMatterError("front matter is not closed with '---'")
    raw = text[4:end]
    rest = text[end + 4 :]
    body = rest[1:] if rest.startswith("\n") else rest
    data = yaml.safe_load(raw) if raw.strip() else {}
    if not isinstance(data, dict):
        raise FrontMatterError("front matter must be a mapping")
    return data, body


def code_mask(lines: list[str]) -> list[bool]:
    """True for lines inside (or delimiting) fenced code blocks."""
    mask: list[bool] = []
    fence: str | None = None
    for line in lines:
        match = FENCE_RE.match(line)
        if fence is None and match:
            fence = match.group(1)
            mask.append(True)
        elif fence is not None:
            mask.append(True)
            if line.strip().startswith(fence):
                fence = None
        else:
            mask.append(False)
    return mask


def find_section(lines: list[str], heading: str) -> tuple[int, int] | None:
    """Index range [start, end) of a level-2 section (heading line included)."""
    mask = code_mask(lines)
    start = None
    for i, line in enumerate(lines):
        if mask[i] or not line.startswith("## "):
            continue
        if start is None and line[3:].strip() == heading:
            start = i
        elif start is not None:
            return start, i
    return (start, len(lines)) if start is not None else None


@dataclass(frozen=True)
class TaskHeading:
    line: int
    title: str
    id: str | None


def task_headings(lines: list[str], section: tuple[int, int]) -> list[TaskHeading]:
    mask = code_mask(lines)
    found: list[TaskHeading] = []
    for i in range(section[0] + 1, section[1]):
        line = lines[i]
        if mask[i] or not line.startswith("### "):
            continue
        match = TASK_HEADING_RE.match(line)
        if match:
            found.append(TaskHeading(i, match.group("title"), match.group("id")))
        else:
            found.append(TaskHeading(i, line[4:].strip(), None))
    return found


_INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1", re.S)
_LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
_REFERENCE_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s.*)?$", re.M)
_AUTOLINK_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9+.-]*:[^>\s]+)>")
_HTML_URL_RE = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)


def link_targets(body: str) -> list[str]:
    """Targets of links and images (Markdown and raw HTML), ignoring code blocks and code spans."""
    lines = body.splitlines()
    mask = code_mask(lines)
    text = "\n".join("" if in_code else line for line, in_code in zip(lines, mask))
    text = _INLINE_CODE_RE.sub("", text)
    targets: list[str] = []
    for pattern in (_LINK_RE, _REFERENCE_RE, _AUTOLINK_RE, _HTML_URL_RE):
        targets += pattern.findall(text)
    return targets
