# Emergence and Non-Injectivity Videos

This directory contains the editable Manim sources associated with the paper
*Emergence and Non-Injectivity*.

## One Reality, Multiple Descriptions

The first animation presents the paper's central structural distinction:

- an injective projection preserves every fine-grained distinction and therefore gives only a relabelling;
- a genuinely emergent effective level merges distinctions through a many-to-one projection;
- under the hypotheses of the paper, genuine emergence requires non-injectivity and strictly positive projection
  entropy.

In the animation, $\Omega$ denotes the framework-independent theorem's fine-grained configuration space.
It is not another name for $\chi$, the proposed substrate symbol used in the preliminary Cosmochrony white-paper
vocabulary. The paper does not identify the two or construct a Cosmochrony-specific $\Omega$.

The rendering script uses `uv run --no-project` with the shared global `uv` package cache and pins Python 3.13,
Manim 0.20.1, Manim Voiceover 0.3.7, Edge TTS 7.2.8, and the compatibility version of `setuptools` required by the
voice-over plugin.
It does not create a virtual environment inside this directory or install a persistent tool under `~/.local`.
The free online Edge TTS service generates the English narration automatically from `narration.py` with the
British male voice `en-GB-RyanNeural`.

The final video is published through the official Cosmochrony accounts:

- YouTube: <https://www.youtube.com/watch?v=cz4ralii728>
- Instagram: <https://www.instagram.com/reel/Da3oPm6holA/>

Render the final narrated 1080p60 video with:

```bash
./render.sh
```

For a faster 480p15 draft render, use:

```bash
./render.sh draft
```

The generated MP4 and, when emitted by Manim Voiceover, its YouTube-ready SRT subtitle file are written to `out/`.
Synthesized speech is cached globally by `uv` at the tool level and locally by Manim Voiceover under the ignored
`media/` tree.
