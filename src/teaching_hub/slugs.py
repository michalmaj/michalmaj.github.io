"""Heading ids (anchors) for Polish text, and aliases for published anchors that changed.

Python-Markdown's default slugify drops letters that have no ASCII base under Unicode
decomposition. For Polish that is only "ł": "Materiały" became "materiay". `slugify` maps
"ł" to "l" first; every other heading id stays exactly as before. Both renderers use it
through the toc extension (`slugify: !!python/name:teaching_hub.slugs.slugify`).

Anchors are public links. When a published heading id changes, data/anchor-aliases.yml keeps
the old id: `add_anchor_aliases` puts it on an empty element at the start of the heading, so
old links still land on the heading while its text, table of contents and search entry stay
as they are.
"""

import re
from collections.abc import Iterable, Mapping

from markdown.extensions.toc import slugify as _markdown_slugify
from markdown.extensions.toc import unique

ALIAS_CLASS = "th-anchor-alias"
_TRANSLITERATION = str.maketrans({"ł": "l", "Ł": "L"})

_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_HEADING = re.compile(r"^( {0,3}#{1,6}[ \t]+)(.*?)[ \t]*$")
_ATTR_LIST = re.compile(r"[ \t]*\{:?([^}]*)\}$")
_EXPLICIT_ID = re.compile(r"(?:^|\s)#([\w-]+)")
_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_TAG = re.compile(r"<[^>]+>")


def slugify(value: str, separator: str) -> str:
    return _markdown_slugify(value.translate(_TRANSLITERATION), separator)


def _plain(text: str) -> str:
    """Heading text as the toc extension sees it: without link targets, tags and emphasis marks."""
    text = _TAG.sub("", _LINK.sub(r"\1", text))
    return text.replace("`", "").replace("**", "").replace("__", "").replace("*", "")


def heading_ids(markdown: str) -> list[tuple[int, str, str]]:
    """(line number, heading prefix, id) of each ATX heading, outside front matter and code blocks."""
    lines = markdown.split("\n")
    start = lines.index("---", 1) + 1 if lines[0] == "---" and "---" in lines[1:] else 0
    ids: set[str] = set()
    out = []
    fence: str | None = None
    for number in range(start, len(lines)):
        line = lines[number]
        opening = _FENCE.match(line)
        if fence is not None:
            if opening and opening.group(1)[0] == fence:
                fence = None
            continue
        if opening:
            fence = opening.group(1)[0]
            continue
        heading = _HEADING.match(line)
        if not heading:
            continue
        prefix, content = heading.groups()
        attrs = _ATTR_LIST.search(content)
        explicit = _EXPLICIT_ID.search(attrs.group(1)) if attrs else None
        if explicit:
            ids.add(explicit.group(1))
            out.append((number, prefix, explicit.group(1)))
        else:
            out.append((number, prefix, unique(slugify(_plain(content[: attrs.start()] if attrs else content), "-"), ids)))
    return out


def add_anchor_aliases(markdown: str, aliases: Mapping[str, Iterable[str]]) -> str:
    """Put each alias (old anchor) on the heading whose id is its target."""
    lines = markdown.split("\n")
    for number, prefix, heading_id in heading_ids(markdown):
        spans = "".join(f'<span id="{anchor}" class="{ALIAS_CLASS}"></span>' for anchor in aliases.get(heading_id, ()))
        if spans:
            lines[number] = prefix + spans + lines[number][len(prefix):]
    return "\n".join(lines)
