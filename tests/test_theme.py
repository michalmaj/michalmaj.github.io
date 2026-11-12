"""Design tokens: both colour schemes must meet WCAG 2.2 AA contrast.

Contrast is computed here with the WCAG relative-luminance formula, independently of the stylesheet.
"""

import re
from pathlib import Path

import pytest

THEME = Path(__file__).resolve().parent.parent / "renderer" / "theme"

# (foreground token, background token, minimum ratio)
# 4.5:1 text (WCAG 1.4.3), 3:1 UI component boundaries and focus indicators (WCAG 1.4.11).
PAIRS = [
    ("--th-text", "--th-bg", 4.5),
    ("--th-text", "--th-surface", 4.5),
    ("--th-text-muted", "--th-bg", 4.5),
    ("--th-text-muted", "--th-surface", 4.5),
    ("--th-accent", "--th-bg", 4.5),
    ("--th-accent", "--th-surface", 4.5),
    ("--th-accent-strong", "--th-surface", 4.5),
    ("--th-on-accent", "--th-accent", 4.5),
    ("--th-accent-on-soft", "--th-accent-soft", 4.5),
    ("--th-badge-fg", "--th-badge-bg", 4.5),
    ("--th-optional-fg", "--th-optional-bg", 4.5),
    ("--th-archived-fg", "--th-archived-bg", 4.5),
    ("--th-draft-fg", "--th-draft-bg", 4.5),
    ("--th-code-fg", "--th-code-bg", 4.5),
    ("--th-code-comment", "--th-code-bg", 4.5),
    ("--th-code-keyword", "--th-code-bg", 4.5),
    ("--th-code-string", "--th-code-bg", 4.5),
    ("--th-code-number", "--th-code-bg", 4.5),
    ("--th-code-function", "--th-code-bg", 4.5),
    ("--th-code-operator", "--th-code-bg", 4.5),
    ("--th-border-strong", "--th-bg", 3.0),
    ("--th-border-strong", "--th-surface", 3.0),
    ("--th-focus", "--th-bg", 3.0),
    ("--th-focus", "--th-surface", 3.0),
]

SCHEMES = {"light": '[data-md-color-scheme="default"]', "dark": '[data-md-color-scheme="slate"]'}


def tokens(scheme: str) -> dict[str, str]:
    css = (THEME / "tokens.css").read_text(encoding="utf-8")
    selector = re.escape(SCHEMES[scheme])
    block = re.search(selector + r"[^{]*\{(?P<body>[^}]*)\}", css)
    assert block, f"no token block for {scheme}"
    return dict(re.findall(r"(--th-[a-z0-9-]+)\s*:\s*([^;]+);", block.group("body")))


def luminance(hex_color: str) -> float:
    value = hex_color.strip().lstrip("#")
    assert re.fullmatch(r"[0-9a-fA-F]{6}", value), f"tokens must be #rrggbb, got {hex_color!r}"
    channels = [int(value[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_contrast_helper_matches_known_values():
    assert round(contrast("#000000", "#ffffff"), 1) == 21.0
    assert round(contrast("#767676", "#ffffff"), 2) == 4.54  # the classic AA grey


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize("fg,bg,minimum", PAIRS)
def test_token_pair_meets_wcag_aa(scheme, fg, bg, minimum):
    values = tokens(scheme)
    ratio = contrast(values[fg], values[bg])
    assert ratio >= minimum, f"{scheme}: {fg} on {bg} is {ratio:.2f}:1, needs {minimum}:1"


def test_both_schemes_define_the_same_tokens():
    assert set(tokens("light")) == set(tokens("dark"))


def test_theme_stylesheets_load_nothing_from_other_hosts():
    for path in THEME.glob("*.css"):
        css = path.read_text(encoding="utf-8")
        assert not re.search(r"@import|url\(\s*['\"]?(https?:)?//", css), path.name
