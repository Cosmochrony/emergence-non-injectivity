#!/usr/bin/env bash

# Render the Emergence and Non-Injectivity explanatory video.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENE_FILE="one_reality_multiple_descriptions.py"
SCENE_NAME="OneRealityMultipleDescriptions"
OUTPUT_STEM="one-reality-multiple-descriptions"
MODE="${1:-final}"

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
uv run manim "$QUALITY_FLAG" --output_file "$OUTPUT_STEM" "$SCENE_FILE" "$SCENE_NAME"

RENDERED_FILE="media/videos/${SCENE_FILE%.py}/${QUALITY_DIR}/${OUTPUT_STEM}.mp4"
FINAL_FILE="out/$OUTPUT_FILE"

if [ ! -f "$RENDERED_FILE" ]; then
    echo "Error: Manim did not produce the expected file: $RENDERED_FILE" >&2
    exit 1
fi

cp "$RENDERED_FILE" "$FINAL_FILE"

echo "=== Render successful ==="
echo "Output: $FINAL_FILE"
ls -lh "$FINAL_FILE"
