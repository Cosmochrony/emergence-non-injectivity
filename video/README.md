# Emergence and Non-Injectivity Videos

This directory contains the editable Manim sources associated with the paper
*Emergence and Non-Injectivity*.

## One Reality, Multiple Descriptions

The first animation presents the paper's central structural distinction:

- an injective projection preserves every fine-grained distinction and therefore gives only a relabelling;
- a genuinely emergent effective level merges distinctions through a many-to-one projection;
- under the hypotheses of the paper, genuine emergence requires non-injectivity and strictly positive projection
  entropy.

Render the final 1080p60 video with:

```bash
./render.sh
```

For a faster 480p15 draft render, use:

```bash
./render.sh draft
```

The generated MP4 is written to `out/`.
