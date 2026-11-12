"""Presentation markup written into generated Markdown.

Only CSS hooks and accessible structure (classes, landmarks, visually hidden text).
No content, no selection logic: callers decide what is shown, these helpers decide how.
"""

import html


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def page_marker(kind: str) -> str:
    """Hidden element naming the page type, used by the stylesheet to scope page-specific rules."""
    return f'<div class="th-page" data-th-page="{kind}" hidden></div>'


def front_matter(search_exclude: bool = False, hide: tuple[str, ...] = ()) -> str:
    lines = []
    if search_exclude:
        lines += ["search:", "  exclude: true"]
    if hide:
        lines += ["hide:", *(f"  - {item}" for item in hide)]
    return "---\n" + "\n".join(lines) + "\n---\n\n" if lines else ""


def block(css_class: str, lines: list[str]) -> list[str]:
    """A <div> whose content is still Markdown (md_in_html)."""
    return [f'<div class="{css_class}" markdown>', "", *lines, "", "</div>"]


def breadcrumbs(label: str, links: list[str]) -> str:
    separator = ' <span class="th-breadcrumbs__sep" aria-hidden="true">/</span> '
    return f'<nav class="th-breadcrumbs" aria-label="{esc(label)}" markdown="span">{separator.join(links)}</nav>'


def pagebar(crumbs: str | None, switch: str | None) -> list[str]:
    inner: list[str] = []
    if crumbs:
        inner += [crumbs, ""]
    if switch:
        inner.append(switch)
    return [*block("th-pagebar", inner), ""] if inner else []


def badge(text: str, variant: str) -> str:
    # `text` may contain inline Markdown code (e.g. a Git ref in backticks); it is not escaped twice.
    return f'<span class="th-badge th-badge--{variant}">{text}</span>'


def lang_badge(code_label: str, sr_label: str) -> str:
    return f'<span class="th-badge th-badge--lang"><span class="th-sr">{esc(sr_label)}: </span>{esc(code_label)}</span>'


def optional_badge(label: str) -> str:
    # Parentheses are visually hidden so that screen readers and the table of contents read "(label)".
    return (
        '<span class="th-badge th-badge--optional"><span class="th-sr">(</span>'
        f'{esc(label)}<span class="th-sr">)</span></span>'
    )


def meta(parts: list[str]) -> str:
    return '<span class="th-material__meta">' + " ".join(p for p in parts if p) + "</span>"


def paragraph(text: str, css_class: str) -> list[str]:
    """A Markdown paragraph with a class (attr_list block syntax)."""
    return [text, f"{{ .{css_class} }}"]
