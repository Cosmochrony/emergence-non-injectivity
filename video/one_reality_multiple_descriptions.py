"""Episode 1.1 — One Reality, Multiple Descriptions (redesigned).

Why genuine emergence requires a many-to-one projection.

Drop-in replacement for ``one_reality_multiple_descriptions.py``.  Requires
``cosmochrony_style.py`` (shared visual system) alongside it, plus ``narration.py``
and ``edge_tts_service.py`` as before.  Computer Modern prose needs the
``cm-unicode`` Pango fonts; equations need a LaTeX distribution.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    ORIGIN,
    RIGHT,
    Transform,
    UP,
    VGroup,
    Write,
)
from manim_voiceover import VoiceoverScene

from cosmochrony_style import (
    CORAL,
    CYAN,
    FOREGROUND,
    MUTED,
    STRUCTURE,
    VIOLET,
    kicker,
    serif,
    type_on,
    type_sentence,
)
from edge_tts_service import EdgeTTSService
from narration import NARRATION

FIBRE_COLORS = (CYAN, VIOLET, CORAL)
BACKGROUND_CONTRAST = "#0A0D14"  # outcome-disc label colour, for contrast on filled discs

NODE_COORDINATES = (
    (-1.25, 1.35), (-0.10, 1.72), (1.18, 1.18), (-1.48, 0.18), (-0.24, 0.55),
    (1.02, 0.08), (-1.18, -1.02), (0.02, -0.72), (1.28, -1.18), (-0.35, -1.62),
)
EDGES = (
    (0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5), (3, 4), (3, 6),
    (4, 5), (4, 6), (4, 7), (5, 7), (5, 8), (6, 7), (6, 9), (7, 8), (7, 9), (8, 9),
)
FIBRES = ((0, 3, 6), (1, 4, 7, 9), (2, 5, 8))


def make_structure(center: np.ndarray, scale: float = 0.88):
    positions = [center + scale * np.array([x, y, 0.0]) for x, y in NODE_COORDINATES]
    edges = VGroup(
        *[
            Line(positions[a], positions[b], color=STRUCTURE, stroke_width=1.8, stroke_opacity=0.72)
            for a, b in EDGES
        ]
    )
    nodes = VGroup(
        *[Dot_like(p) for p in positions]
    )
    return VGroup(edges, nodes), edges, nodes, positions


def Dot_like(point: np.ndarray) -> Circle:
    dot = Circle(radius=0.075, color=CYAN, fill_color=CYAN, fill_opacity=1.0, stroke_width=1.2)
    dot.set_stroke(FOREGROUND, width=1.2)
    dot.move_to(point)
    return dot


class OneRealityMultipleDescriptions(VoiceoverScene):
    """The no-go theorem connecting emergence and non-injectivity, redesigned."""

    def construct(self) -> None:
        self.set_speech_service(EdgeTTSService(voice="en-GB-RyanNeural"))
        self.scene_opening()
        self.scene_fine_grained()
        self.scene_injective()
        self.scene_many_to_one()
        self.scene_conclusion()

    # ------------------------------------------------------------------ opening
    def scene_opening(self) -> None:
        badge = kicker("Episode 1.1", size=26)
        title = serif("One reality", size=110, bold=True)
        subtitle = serif("many descriptions", size=64, color=CYAN, italic=True)
        stack = VGroup(badge, title, subtitle).arrange(DOWN, buff=0.28)

        with self.voiceover(text=NARRATION["opening"]) as tracker:
            self.play(FadeIn(badge, shift=0.2 * DOWN), run_time=tracker.duration * 0.18)
            type_on(self, title, run_time=tracker.duration * 0.42)
            type_on(self, subtitle, run_time=tracker.duration * 0.30)
        self.play(FadeOut(stack), run_time=0.5)

    # ------------------------------------------------------------- fine grained
    def scene_fine_grained(self) -> None:
        self.question = serif("When is an effective description genuinely emergent?",
                              size=34).to_edge(UP, buff=0.5)

        group, edges, nodes, _ = make_structure(3.65 * LEFT + 0.25 * DOWN)
        self.source = group
        self.source_nodes = nodes
        label = VGroup(serif("Fine-grained level", size=27, color=MUTED),
                       MathTex(r"\Omega", color=FOREGROUND).scale(1.1)).arrange(RIGHT, buff=0.2)
        label.next_to(group, DOWN, buff=0.36)
        self.source_label = label

        arrow = Arrow(0.9 * LEFT, 0.9 * RIGHT, buff=0, color=FOREGROUND, stroke_width=4)
        symbol = MathTex(r"\Pi", color=CYAN).scale(1.4).next_to(arrow, UP, buff=0.14)
        self.projection = VGroup(arrow, symbol)

        placeholder = VGroup(
            Circle(radius=0.9, color=STRUCTURE, stroke_width=2.5).set_stroke(opacity=0.55),
            serif("?", size=54, color=MUTED),
        )
        placeholder.move_to(3.65 * RIGHT + 0.25 * DOWN)
        self.placeholder = placeholder
        placeholder_label = VGroup(serif("Effective level", size=27, color=STRUCTURE),
                                   MathTex("O", color=STRUCTURE).scale(1.1)).arrange(RIGHT, buff=0.2)
        placeholder_label.next_to(placeholder, DOWN, buff=0.36)
        self.placeholder = VGroup(placeholder, placeholder_label)

        with self.voiceover(text=NARRATION["fine_grained"]) as tracker:
            type_on(self, self.question, run_time=tracker.duration * 0.22)
            self.play(
                LaggedStart(*[Create(e) for e in edges], lag_ratio=0.045),
                LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.07),
                run_time=tracker.duration * 0.42,
            )
            self.play(FadeIn(label, shift=0.12 * UP), run_time=tracker.duration * 0.14)
            self.play(Create(arrow), FadeIn(symbol), run_time=tracker.duration * 0.10)
            self.play(FadeIn(self.placeholder), run_time=tracker.duration * 0.08)

    # ---------------------------------------------------------------- injective
    def scene_injective(self) -> None:
        target, edges, nodes, _ = make_structure(3.65 * RIGHT + 0.25 * DOWN)
        self.target = target
        label = VGroup(serif("Effective level", size=27, color=MUTED),
                       MathTex("O", color=FOREGROUND).scale(1.1)).arrange(RIGHT, buff=0.2)
        label.next_to(target, DOWN, buff=0.36)
        self.target_label = label

        lines = VGroup(
            *[
                Line(self.source_nodes[i].get_center(), nodes[i].get_center(),
                     color=MUTED, stroke_width=1.1, stroke_opacity=0.24)
                for i in range(len(self.source_nodes))
            ]
        )
        self.injective_lines = lines

        heading = serif("Injective \u2014 every distinction survives the map", size=30).to_edge(UP, buff=0.5)
        verdict = VGroup(
            MathTex(r"O \cong \Omega", color=CYAN).scale(1.4),
            serif("a relabelling \u2014 not genuine emergence", size=25, color=MUTED),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        self.injective_verdict = verdict

        with self.voiceover(text=NARRATION["injective"]) as tracker:
            self.play(Transform(self.question, heading),
                      FadeOut(self.placeholder),
                      LaggedStart(*[Create(l) for l in lines], lag_ratio=0.035),
                      run_time=tracker.duration * 0.24)
            self.play(
                LaggedStart(*[Create(e) for e in edges], lag_ratio=0.035),
                LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.05),
                FadeIn(label, shift=0.12 * UP),
                run_time=tracker.duration * 0.40,
            )
            self.play(FadeIn(verdict, shift=0.12 * UP), run_time=tracker.duration * 0.16)

    # ------------------------------------------------------------- many to one
    def scene_many_to_one(self) -> None:
        centres = (3.65 * RIGHT + 1.18 * UP, 3.65 * RIGHT, 3.65 * RIGHT + 1.18 * DOWN)
        outcomes = VGroup()
        labels = VGroup()
        for index, (centre, colour) in enumerate(zip(centres, FIBRE_COLORS), start=1):
            circle = Circle(radius=0.28, color=FOREGROUND, stroke_width=1.4,
                            fill_color=colour, fill_opacity=1.0).move_to(centre)
            tag = MathTex(f"o_{index}", color=BACKGROUND_CONTRAST).scale(0.8).move_to(centre)
            outcomes.add(circle)
            labels.add(tag)

        fibre_lines = VGroup()
        for fibre_index, node_indices in enumerate(FIBRES):
            for node_index in node_indices:
                fibre_lines.add(
                    Line(self.source_nodes[node_index].get_center(),
                         outcomes[fibre_index].get_center(),
                         color=FIBRE_COLORS[fibre_index], stroke_width=2.2, stroke_opacity=0.72)
                )

        heading = serif("Many-to-one: distinct configurations share one effective state",
                        size=29).to_edge(UP, buff=0.5)
        effective = VGroup(serif("Effective level", size=27, color=MUTED),
                           MathTex("O", color=FOREGROUND).scale(1.1)).arrange(RIGHT, buff=0.2)
        effective.next_to(outcomes, DOWN, buff=0.5)

        recolour = []
        for fibre_index, node_indices in enumerate(FIBRES):
            for node_index in node_indices:
                recolour.append(self.source_nodes[node_index].animate.set_fill(FIBRE_COLORS[fibre_index]))

        with self.voiceover(text=NARRATION["many_to_one"]) as tracker:
            self.play(
                Transform(self.question, heading),
                FadeOut(self.injective_verdict),
                FadeOut(self.injective_lines),
                FadeOut(self.target),
                FadeOut(self.target_label),
                run_time=tracker.duration * 0.24,
            )
            self.play(
                LaggedStart(*[Create(l) for l in fibre_lines], lag_ratio=0.04),
                LaggedStart(*[GrowFromCenter(c) for c in outcomes], lag_ratio=0.15),
                LaggedStart(*[FadeIn(t) for t in labels], lag_ratio=0.15),
                FadeIn(effective, shift=0.12 * UP),
                run_time=tracker.duration * 0.42,
            )
            self.play(*recolour, run_time=tracker.duration * 0.18)

        caption = serif("Each colour marks a fibre of indistinguishable configurations",
                        size=25, color=MUTED).to_edge(DOWN, buff=0.3)
        with self.voiceover(text=NARRATION["fibres"]) as tracker:
            type_on(self, caption, run_time=tracker.duration * 0.55)

        self.diagram = VGroup(self.question, self.source, self.source_label,
                              self.projection, fibre_lines, outcomes, labels,
                              effective, caption)

    # -------------------------------------------------------------- conclusion
    def scene_conclusion(self) -> None:
        badge = kicker("Structural necessity", size=28)
        theorem = MathTex(r"\textbf{genuine emergence}", r"\;\Longrightarrow\;",
                          r"\Pi\ \text{non-injective}").scale(1.25)
        theorem[0].set_color(FOREGROUND)
        theorem[1].set_color(CYAN)
        theorem[2].set_color(FOREGROUND)
        entropy = MathTex(r"\Longrightarrow", r"S_{\Pi}", r"> 0", color=CYAN).scale(1.35)
        closing = serif("A lossless projection preserves structure — it does not create an "
                        "emergent level.", size=25, color=MUTED)
        stack = VGroup(badge, theorem, entropy, closing).arrange(DOWN, buff=0.4)

        with self.voiceover(text=NARRATION["conclusion"]) as tracker:
            self.play(FadeOut(self.diagram), run_time=tracker.duration * 0.16)
            self.play(FadeIn(badge, shift=0.15 * UP), run_time=tracker.duration * 0.12)
            self.play(Write(theorem), run_time=tracker.duration * 0.30)
            self.play(Write(entropy), run_time=tracker.duration * 0.18)
            self.play(FadeIn(closing, shift=0.12 * UP), run_time=tracker.duration * 0.14)
        self.play(FadeOut(stack), run_time=0.8)
