#!/usr/bin/env bash

# Render the Emergence and Non-Injectivity explanatory video.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENE_FILE="one_reality_multiple_descriptions.py"
SCENE_NAME="OneRealityMultipleDescriptions"
OUTPUT_STEM="one-reality-multiple-descriptions"
MODE="${1:-final}"
MANIM_PACKAGE="manim==0.20.1"
VOICEOVER_PACKAGE="manim-voiceover[gtts]==0.3.7"
SETUPTOOLS_PACKAGE="setuptools==80.9.0"
PYTHON_VERSION="3.13"

case "$MODE" in
    final)
        QUALITY_FLAG="-qh"
        QUALITY_DIR="1080p60"
        OUTPUT_FILE="${OUTPUT_STEM}.mp4"
        ;;
    draft)
        QUALITY_FLAG="-ql"
        QUALITY_DIR="480p15"
        OUTPUT_FILE="${OUTPUT_STEM}-draft.mp4"
        ;;
    *)
        echo "Usage: $0 [final|draft]" >&2
        exit 2
        ;;
esac

if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is required but was not found on PATH." >&2
    exit 1
fi

cd "$SCRIPT_DIR"
mkdir -p out

echo "=== Rendering One Reality, Multiple Descriptions ($MODE) ==="
uv tool run \
    --python "$PYTHON_VERSION" \
    --from "$MANIM_PACKAGE" \
    --with "$VOICEOVER_PACKAGE" \
    --with "$SETUPTOOLS_PACKAGE" \
    manim \
    "$QUALITY_FLAG" \
    --disable_caching \
    --output_file "$OUTPUT_STEM" \
    "$SCENE_FILE" \
    "$SCENE_NAME"

RENDERED_FILE="media/videos/${SCENE_FILE%.py}/${QUALITY_DIR}/${OUTPUT_STEM}.mp4"
FINAL_FILE="out/$OUTPUT_FILE"

if [ ! -f "$RENDERED_FILE" ]; then
    echo "Error: Manim did not produce the expected file: $RENDERED_FILE" >&2
    exit 1
fi

cp "$RENDERED_FILE" "$FINAL_FILE"

SUBTITLE_FILE="${RENDERED_FILE%.mp4}.srt"
if [ -f "$SUBTITLE_FILE" ]; then
    FINAL_SUBTITLE_FILE="${FINAL_FILE%.mp4}.srt"
    cp "$SUBTITLE_FILE" "$FINAL_SUBTITLE_FILE"
fi

echo "=== Render successful ==="
echo "Output: $FINAL_FILE"
ls -lh "$FINAL_FILE"
if [ -n "${FINAL_SUBTITLE_FILE:-}" ]; then
    echo "Subtitles: $FINAL_SUBTITLE_FILE"
    ls -lh "$FINAL_SUBTITLE_FILE"
fi
