"""Shared visual system for the Cosmochrony video series (Manim 0.20).

Drop this file into each ``video/`` directory next to the scene script so the
``from cosmochrony_style import *`` line resolves.

Design language (mirrors the approved HTML preview):
  * Typography    -> Computer Modern.  Prose uses the ``CMU Serif`` / ``CMU
                     Typewriter Text`` Pango families; every equation and symbol
                     uses ``MathTex`` (LaTeX Computer Modern).  Install the
                     ``cm-unicode`` fonts and a LaTeX distribution.
  * Palette       -> chalkboard-dark stage, cyan = distinction / quantum,
                     violet = the one / geometry, and green/amber/coral reserved
                     strictly for the epistemic status proved / conditional / open.
  * Motion        -> one idea per beat; graphics of *existing* theories appear as
                     a single unit; prose types on letter-by-letter; keyword
                     lists appear word-by-word; a beat of stillness sits before
                     each em-dash clause.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    AddTextLetterByLetter,
    Arrow,
    Circle,
    Dot,
    DOWN,
    Ellipse,
    FadeIn,
    FunctionGraph,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    ORIGIN,
    RIGHT,
    Text,
    UP,
    VGroup,
    config,
)

# ----------------------------------------------------------------------------- palette
BACKGROUND = "#080A10"
FOREGROUND = "#F2F4F8"
MUTED = "#8A97AD"
STRUCTURE = "#46587A"
CYAN = "#63E0E6"      # distinction / quantum
VIOLET = "#A08BFF"    # the one / geometry
CORAL = "#FF7E82"     # forces / open
GREEN = "#62D6A0"     # proved
AMBER = "#F2C862"     # conditional

FONT_SERIF = "CMU Serif"
FONT_MONO = "CMU Typewriter Text"

# Resolve to a Computer Modern family if installed, otherwise fall back to the
# best available SERIF (never a sans). Install `cm-unicode` to get true Computer
# Modern; on many TeX installs "Latin Modern Roman" is present as a system font.
try:
    import manimpango
    _AVAILABLE = set(manimpango.list_fonts())
except Exception:  # pragma: no cover - manimpango is always present with manim
    _AVAILABLE = set()


def _pick(candidates):
    for name in candidates:
        if name in _AVAILABLE:
            return name
    return candidates[-1]


FONT_SERIF = _pick([
    "CMU Serif", "Latin Modern Roman", "CMU Classical Serif",
    "TeX Gyre Termes", "Nimbus Roman", "Liberation Serif", "DejaVu Serif",
])
FONT_MONO = _pick([
    "CMU Typewriter Text", "Latin Modern Mono", "TeX Gyre Cursor",
    "DejaVu Sans Mono", "Liberation Mono",
])

config.background_color = BACKGROUND


# ----------------------------------------------------------------------------- text
def serif(text: str, size: float = 40, color: str = FOREGROUND, italic: bool = False,
          bold: bool = False) -> Text:
    return Text(
        text,
        font=FONT_SERIF,
        font_size=size,
        color=color,
        slant="ITALIC" if italic else "NORMAL",
        weight="BOLD" if bold else "NORMAL",
    )


def kicker(text: str, size: float = 22, color: str = CYAN, tracking: str = "\u2009") -> Text:
    """A small, lightly letter-spaced monospace section label."""
    return Text(
        tracking.join(text.upper()),       # gentle tracking with thin spaces
        font=FONT_MONO,
        font_size=size,
        color=color,
    )


# ----------------------------------------------------------------------------- timing helpers
def type_on(scene, mobject, run_time: float = 1.0, lag: float = None) -> None:
    """Reveal a Text LEFT-TO-RIGHT: each glyph fades in with a small rightward
    slide (matches the HTML preview's left-to-right fade — NOT a typewriter)."""
    glyphs = list(mobject.submobjects) if mobject.submobjects else [mobject]
    if lag is None:
        lag = min(0.85, 1.6 / max(1, len(glyphs)))
    scene.play(
        LaggedStart(*[FadeIn(g, shift=0.09 * RIGHT) for g in glyphs], lag_ratio=lag),
        run_time=run_time,
    )


def type_sentence(scene, text: str, size: float, color: str = FOREGROUND,
                  italic: bool = False, run_time: float = 1.4, em_pause: float = 0.6,
                  **move):
    """Type a sentence, pausing before an em-dash clause.

    Returns the finished VGroup so the caller can fade it out later.
    """
    parts = [p.strip() for p in text.split("—")]
    group = VGroup()
    for index, part in enumerate(parts):
        prefix = "— " if index else ""
        line = serif(prefix + part, size=size, color=color, italic=italic)
        group.add(line)
    group.arrange(RIGHT, buff=0.22)
    if move:
        group.move_to(move.get("center", ORIGIN))
    per = run_time / max(1, len(parts))
    for index, line in enumerate(group):
        if index:
            scene.wait(em_pause)
        type_on(scene, line, run_time=per)
    return group


def reveal_words(scene, words, size: float, color: str = MUTED, sep: str = "·",
                 per_word: float = 0.32):
    """Reveal a keyword list one token at a time with a small wait between."""
    tokens = []
    for index, word in enumerate(words):
        if index:
            tokens.append(serif(sep, size=size, color=STRUCTURE))
        tokens.append(serif(word, size=size, color=color))
    row = VGroup(*tokens).arrange(RIGHT, buff=0.24)
    for token in row:
        scene.play(FadeIn(token, shift=0.12 * UP), run_time=per_word)
    return row


# ----------------------------------------------------------------------------- theory vignettes
def _wave(color: str) -> VGroup:
    axes = VGroup(
        Line(1.35 * LEFT, 1.35 * RIGHT, color=STRUCTURE, stroke_width=1.6),
        Line(0.9 * DOWN, 0.9 * UP, color=STRUCTURE, stroke_width=1.6),
    )
    curve = FunctionGraph(
        lambda x: math.exp(-x * x / 2.0) * math.cos(3.4 * x),
        x_range=[-2.7, 2.7, 0.05],
        color=color,
        stroke_width=4.5,
    ).scale(0.5)
    return VGroup(axes, curve)


def _grid(color: str) -> VGroup:
    plane = NumberPlane(
        x_range=[-2, 2, 1],
        y_range=[-1.3, 1.3, 1],
        x_length=2.7,
        y_length=1.7,
        background_line_style={"stroke_color": color, "stroke_width": 1.5, "stroke_opacity": 0.9},
        axis_config={"stroke_width": 0},
        faded_line_ratio=0,
    )

    def warp(point):
        x, y, _ = point
        r2 = x * x + y * y
        squeeze = 1.0 - 0.4 * math.exp(-r2 / 0.9)
        return np.array([x * squeeze, y * squeeze, 0.0])

    plane.apply_function(warp)
    mass = Dot(plane.get_center(), color=color, radius=0.06)
    return VGroup(plane, mass)


def _gauge(color: str) -> VGroup:
    rings = VGroup(
        Circle(radius=0.30, color=color, stroke_width=2.0),
        Circle(radius=0.52, color=color, stroke_width=1.5).set_stroke(opacity=0.6),
        Circle(radius=0.74, color=color, stroke_width=1.2).set_stroke(opacity=0.4),
    )
    arrows = VGroup(
        *[
            Arrow(ORIGIN, 0.9 * direction, color=color, buff=0.0, stroke_width=3.0,
                  max_tip_length_to_length_ratio=0.28)
            for direction in (UP, RIGHT, DOWN, LEFT)
        ]
    )
    core = Dot(ORIGIN, color=color, radius=0.08)
    return VGroup(rings, arrows, core)


def _matter(color: str) -> VGroup:
    orbits = VGroup(
        *[
            Ellipse(width=2.4, height=0.92, color=color, stroke_width=1.6)
            .set_stroke(opacity=0.7)
            .rotate(angle)
            for angle in (0.0, math.pi / 3.0, -math.pi / 3.0)
        ]
    )
    nucleus = Dot(ORIGIN, color=color, radius=0.11)
    electrons = VGroup(
        Dot(1.2 * RIGHT, color=FOREGROUND, radius=0.06),
        Dot(0.6 * LEFT + 0.52 * UP, color=FOREGROUND, radius=0.06),
        Dot(0.6 * LEFT + 0.52 * DOWN, color=FOREGROUND, radius=0.06),
    )
    return VGroup(orbits, nucleus, electrons)


_GRAPHICS = {"psi": _wave, "grid": _grid, "gauge": _gauge, "matter": _matter}


def theory_vignette(kind: str, color: str, formula: str, label: str):
    """A single 'existing theory' graphic with its formula and caption.

    Returns ``(column, graphic, formula_mob, label_mob)`` so the caller can
    reveal the graphic as one unit, then the formula, then type the label.
    """
    graphic = _GRAPHICS[kind](color)
    formula_mob = MathTex(formula, color=color).scale(0.85)
    label_mob = Text(label, font=FONT_MONO, font_size=20, color=MUTED)
    column = VGroup(graphic, formula_mob, label_mob).arrange(DOWN, buff=0.24)
    return column, graphic, formula_mob, label_mob
