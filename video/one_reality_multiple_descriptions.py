"""Explain why genuine emergence requires a many-to-one projection."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import (
    Arrow,
    Circle,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    LEFT,
    Line,
    ORIGIN,
    RIGHT,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
    WHITE,
    Write,
    config,
)


BACKGROUND = "#080D1B"
FOREGROUND = "#EFF4FF"
MUTED = "#9DACBC"
STRUCTURE = "#62789B"
CYAN = "#49D3DF"
VIOLET = "#996FFF"
CORAL = "#FF7D80"
FIBRE_COLORS = (CYAN, VIOLET, CORAL)
FONT = "Arial"

config.background_color = BACKGROUND


@dataclass
class StructureDiagram:
    """A graph-like fine-grained structure and its individually addressable nodes."""

    group: VGroup
    edges: VGroup
    nodes: VGroup


NODE_COORDINATES = (
    (-1.25, 1.35),
    (-0.10, 1.72),
    (1.18, 1.18),
    (-1.48, 0.18),
    (-0.24, 0.55),
    (1.02, 0.08),
    (-1.18, -1.02),
    (0.02, -0.72),
    (1.28, -1.18),
    (-0.35, -1.62),
)

EDGES = (
    (0, 1),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 4),
    (2, 4),
    (2, 5),
    (3, 4),
    (3, 6),
    (4, 5),
    (4, 6),
    (4, 7),
    (5, 7),
    (5, 8),
    (6, 7),
    (6, 9),
    (7, 8),
    (7, 9),
    (8, 9),
)

FIBRES = (
    (0, 3, 6),
    (1, 4, 7, 9),
    (2, 5, 8),
)


def make_structure(center: np.ndarray, scale: float = 0.88) -> StructureDiagram:
    """Create a compact relational graph centred at the requested position."""

    positions = [center + scale * np.array([x, y, 0.0]) for x, y in NODE_COORDINATES]
    edges = VGroup(
        *[
            Line(positions[start], positions[end], color=STRUCTURE, stroke_width=1.8, stroke_opacity=0.72)
            for start, end in EDGES
        ]
    )
    nodes = VGroup(
        *[
            Dot(position, radius=0.075, color=CYAN, fill_opacity=1.0).set_stroke(WHITE, width=1.2)
            for position in positions
        ]
    )
    return StructureDiagram(VGroup(edges, nodes), edges, nodes)


def make_label(title: str, symbol: str) -> VGroup:
    """Create a textual level label with a mathematical symbol."""

    words = Text(title, font=FONT, font_size=27, color=MUTED)
    maths = Text(symbol, font=FONT, font_size=34, color=FOREGROUND)
    return VGroup(words, maths).arrange(RIGHT, buff=0.18)


class OneRealityMultipleDescriptions(Scene):
    """Animate the no-go theorem connecting emergence and non-injectivity."""

    def construct(self) -> None:
        title = Text("ONE REALITY", font=FONT, font_size=64, weight="BOLD", color=FOREGROUND)
        subtitle = Text("MULTIPLE DESCRIPTIONS", font=FONT, font_size=34, color=CYAN)
        opening = VGroup(title, subtitle).arrange(DOWN, buff=0.20).move_to(ORIGIN)

        self.play(Write(title), run_time=1.25)
        self.play(FadeIn(subtitle, shift=0.16 * UP), run_time=0.85)
        self.wait(0.8)
        self.play(FadeOut(opening), run_time=0.7)

        question = Text(
            "When is an effective description genuinely emergent?",
            font=FONT,
            font_size=34,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.48)

        source = make_structure(3.65 * LEFT + 0.25 * DOWN)
        source_label = make_label("Fine-grained level", "Ω")
        source_label.next_to(source.group, DOWN, buff=0.36)

        self.play(Write(question), run_time=0.8)
        self.play(
            LaggedStart(*[Create(edge) for edge in source.edges], lag_ratio=0.045),
            LaggedStart(*[GrowFromCenter(node) for node in source.nodes], lag_ratio=0.07),
            run_time=2.0,
        )
        self.play(FadeIn(source_label, shift=0.12 * UP), run_time=0.6)

        projection_arrow = Arrow(0.9 * LEFT, 0.9 * RIGHT, buff=0, color=FOREGROUND, stroke_width=4)
        projection_symbol = Text("Π", font=FONT, font_size=48, color=CYAN).next_to(
            projection_arrow, UP, buff=0.14
        )
        self.play(Create(projection_arrow), FadeIn(projection_symbol), run_time=0.7)

        target = make_structure(3.65 * RIGHT + 0.25 * DOWN)
        target_label = make_label("Effective level", "O")
        target_label.next_to(target.group, DOWN, buff=0.36)
        injective_lines = VGroup(
            *[
                Line(
                    source.nodes[index].get_center(),
                    target.nodes[index].get_center(),
                    color=MUTED,
                    stroke_width=1.1,
                    stroke_opacity=0.24,
                )
                for index in range(len(source.nodes))
            ]
        )

        injective_heading = Text(
            "Injective: every distinction survives",
            font=FONT,
            font_size=30,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.48)
        injective_verdict = VGroup(
            Text("O ≅ Ω", font=FONT, font_size=42, color=CYAN),
            Text("a relabelling, not genuine emergence", font=FONT, font_size=25, color=MUTED),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(question, injective_heading),
            LaggedStart(*[Create(line) for line in injective_lines], lag_ratio=0.035),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[Create(edge) for edge in target.edges], lag_ratio=0.035),
            LaggedStart(*[GrowFromCenter(node) for node in target.nodes], lag_ratio=0.05),
            FadeIn(target_label, shift=0.12 * UP),
            run_time=1.6,
        )
        self.play(FadeIn(injective_verdict, shift=0.12 * UP), run_time=0.7)
        self.wait(1.2)

        outcome_centres = (3.65 * RIGHT + 1.18 * UP, 3.65 * RIGHT, 3.65 * RIGHT + 1.18 * DOWN)
        outcomes = VGroup()
        outcome_text = VGroup()
        for index, (centre, colour) in enumerate(zip(outcome_centres, FIBRE_COLORS, strict=True), start=1):
            circle = Circle(radius=0.28, color=WHITE, stroke_width=1.4, fill_color=colour, fill_opacity=1.0)
            circle.move_to(centre)
            label = Text(f"o{index}", font=FONT, font_size=25, color=FOREGROUND).move_to(centre)
            outcomes.add(circle)
            outcome_text.add(label)

        fibre_lines = VGroup()
        for fibre_index, node_indices in enumerate(FIBRES):
            for node_index in node_indices:
                fibre_lines.add(
                    Line(
                        source.nodes[node_index].get_center(),
                        outcomes[fibre_index].get_center(),
                        color=FIBRE_COLORS[fibre_index],
                        stroke_width=2.2,
                        stroke_opacity=0.72,
                    )
                )

        many_to_one_heading = Text(
            "Many-to-one: distinct configurations share one effective state",
            font=FONT,
            font_size=29,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.48)
        many_to_one_label = make_label("Effective level", "O")
        many_to_one_label.next_to(outcomes, DOWN, buff=0.50)

        self.play(
            Transform(question, many_to_one_heading),
            FadeOut(injective_verdict),
            FadeOut(injective_lines),
            FadeOut(target.group),
            FadeOut(target_label),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[Create(line) for line in fibre_lines], lag_ratio=0.04),
            LaggedStart(*[GrowFromCenter(circle) for circle in outcomes], lag_ratio=0.15),
            LaggedStart(*[FadeIn(label) for label in outcome_text], lag_ratio=0.15),
            FadeIn(many_to_one_label, shift=0.12 * UP),
            run_time=1.8,
        )

        colour_animations = []
        for fibre_index, node_indices in enumerate(FIBRES):
            for node_index in node_indices:
                colour_animations.append(source.nodes[node_index].animate.set_color(FIBRE_COLORS[fibre_index]))
        self.play(*colour_animations, run_time=0.9)

        fibre_caption = Text(
            "Each colour marks a fibre of indistinguishable configurations",
            font=FONT,
            font_size=25,
            color=MUTED,
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(fibre_caption, shift=0.12 * UP), run_time=0.6)
        self.wait(1.5)

        diagram = VGroup(
            question,
            source.group,
            source_label,
            projection_arrow,
            projection_symbol,
            fibre_lines,
            outcomes,
            outcome_text,
            many_to_one_label,
            fibre_caption,
        )
        self.play(FadeOut(diagram), run_time=0.9)

        theorem_heading = Text("STRUCTURAL NECESSITY", font=FONT, font_size=30, color=CYAN)
        theorem = Text(
            "genuine emergence  ⇒  Π non-injective",
            font=FONT,
            font_size=43,
            color=FOREGROUND,
        )
        entropy_symbol = VGroup(
            Text("S", font=FONT, font_size=49, color=CYAN),
            Text("Π", font=FONT, font_size=25, color=CYAN),
        )
        entropy_symbol[1].next_to(entropy_symbol[0], DOWN, buff=-0.08).shift(0.18 * RIGHT)
        entropy = VGroup(
            Text("⇒", font=FONT, font_size=49, color=CYAN),
            entropy_symbol,
            Text("> 0", font=FONT, font_size=49, color=CYAN),
        ).arrange(RIGHT, buff=0.22)
        closing = Text(
            "A lossless projection preserves structure; it does not create an emergent level.",
            font=FONT,
            font_size=25,
            color=MUTED,
        )
        conclusion = VGroup(theorem_heading, theorem, entropy, closing).arrange(DOWN, buff=0.34)

        self.play(FadeIn(theorem_heading, shift=0.15 * UP), run_time=0.6)
        self.play(Write(theorem), run_time=1.5)
        self.play(Write(entropy), run_time=0.8)
        self.play(FadeIn(closing, shift=0.12 * UP), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(conclusion), run_time=0.8)
