#!/usr/bin/env python3
"""Optimize experiment images for PDF build.

Mirrors fal-pipeline images to _img_cache/ with sips resize to 600px width.
Source files are NEVER modified. Uses timestamp-based caching.
"""

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_DIR = os.path.join(SCRIPT_DIR, "..")
REPO_ROOT = os.path.normpath(os.path.join(SUBMISSION_DIR, "..", ".."))

# Source directories to mirror
SOURCES = [
    "experiments/fal-pipeline/outputs",
    "experiments/fal-pipeline/inputs",
]

CACHE_BASE = os.path.join(SUBMISSION_DIR, "_img_cache")
MAX_WIDTH = 600  # At 0.3\textwidth on A4, 600px ≈ 300 DPI
JPEG_QUALITY = 75  # Good enough for 0.3\textwidth print
IMAGE_EXTS = {".png", ".jpg", ".jpeg"}


def optimize_file(src_path, cache_path):
    """Resize + convert to JPEG for small file size. Returns True if processed."""
    # Always output as JPEG for compression (replace extension)
    base, _ = os.path.splitext(cache_path)
    cache_path = base + ".jpg"

    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    # Skip if cache is newer than source
    if os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(src_path):
        return False

    # Get current width
    try:
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", src_path],
            capture_output=True, text=True,
        )
        width = int(result.stdout.strip().split()[-1])
    except (ValueError, IndexError):
        subprocess.run(["cp", src_path, cache_path], capture_output=True)
        return True

    cmds = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(JPEG_QUALITY)]
    if width > MAX_WIDTH:
        cmds += ["--resampleWidth", str(MAX_WIDTH)]
    cmds += [src_path, "--out", cache_path]

    subprocess.run(cmds, capture_output=True)
    return True


def main():
    total = 0
    processed = 0

    for rel_source in SOURCES:
        src_dir = os.path.join(REPO_ROOT, rel_source)
        if not os.path.isdir(src_dir):
            print(f"  SKIP: {rel_source} not found", file=sys.stderr)
            continue

        cache_dir = os.path.join(CACHE_BASE, rel_source)

        for root, _, files in os.walk(src_dir):
            for fname in sorted(files):
                ext = os.path.splitext(fname)[1].lower()
                if ext not in IMAGE_EXTS:
                    continue

                total += 1
                src_path = os.path.join(root, fname)
                rel_path = os.path.relpath(src_path, src_dir)
                cache_path = os.path.join(cache_dir, rel_path)

                if optimize_file(src_path, cache_path):
                    processed += 1
                    print(f"  {rel_source}/{rel_path}", file=sys.stderr)

    print(f"Done: {processed}/{total} images processed, cache at _img_cache/", file=sys.stderr)


if __name__ == "__main__":
    main()
