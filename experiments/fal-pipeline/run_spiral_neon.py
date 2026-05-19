#!/usr/bin/env python3
"""
Spiral Staircase — Soft Glow Remix at 16:9.
Edits the original 18_nanobanana_v2_landscape/spiral_staircase.png with
fal-ai/nano-banana-pro/edit, explicit aspect_ratio=16:9, subtle glow (no color
named, no neon). Never overwrites — every run gets a timestamped filename.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "spiral_neon"
RESULTS_FILE = SCRIPT_DIR / "spiral_neon_results.json"

INPUT_IMAGE = (
    SCRIPT_DIR / "outputs" / "18_nanobanana_v2_landscape" / "spiral_staircase.png"
)

PROMPT = (
    "Edit this image. Keep the character, pose, background (space, stars, galaxies, "
    "clouds) and the overall cosmic color grading. "
    "Make these changes: "
    "1) Reframe to a true 16:9 landscape — wider, more cinematic, more space on left and right. "
    "2) The character's shoes should be white. "
    "3) The spiral staircase is NOT marble. The steps themselves are luminous — they emit "
    "a soft, even warm-white light from within, like frosted glass lit from inside. "
    "The whole staircase glows gently. Keep the glow soft and uniform — single color (warm white), "
    "not bright, not pulsing, not neon, no multi-color. Subtle illumination casts faint "
    "light onto the surrounding space. The dreamy blue/purple cosmic atmosphere of the "
    "original must be preserved."
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_image(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=120)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(record: dict):
    existing = []
    if RESULTS_FILE.exists():
        try:
            existing = json.loads(RESULTS_FILE.read_text())
        except Exception:
            existing = []
    existing.append(record)
    RESULTS_FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print(f"SPIRAL STAIRCASE — Soft Glow 16:9 | run {stamp}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(INPUT_IMAGE)
    model = "fal-ai/nano-banana-pro/edit"

    print(f"\n  {model} | aspect_ratio=16:9")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_urls": [image_url],
                "prompt": PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        saved = []
        for i, url in enumerate(urls):
            suffix = "" if i == 0 else f"_{i}"
            name = f"spiral_softglow_16x9_{stamp}{suffix}"
            p = save_image(url, name)
            saved.append(str(p.name))

        append_record({
            "run": stamp,
            "model": model,
            "prompt": PROMPT,
            "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.15",
            "images": urls,
            "saved": saved,
            "input": str(INPUT_IMAGE.name),
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s — {len(urls)} image(s)")
        print(f"  Saved: {saved}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")


if __name__ == "__main__":
    main()
