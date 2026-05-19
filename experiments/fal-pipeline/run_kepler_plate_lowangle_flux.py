#!/usr/bin/env python3
"""
Kepler Plate Low-Angle (Flux Kontext) — alternative to nano-banana.
Uses fal-ai/flux-pro/kontext for camera-angle edit on the glowing spiral
staircase. Same prompt intent: moderate low-angle, preserve glow + char.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "kepler_plate_lowangle_flux"
RESULTS_FILE = SCRIPT_DIR / "kepler_plate_lowangle_flux_results.json"

SCENE_IMAGE = (
    SCRIPT_DIR / "outputs" / "spiral_upscale"
    / "spiral_upscale_clarity_edited.png"
)

PROMPT = (
    "Reframe the image so the bottom edge of the frame cuts through the "
    "character at ankle height — the character's feet are below the frame "
    "and not visible. Same scene, same composition otherwise, just framed "
    "lower so the character's feet exit the bottom of the image."
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
    print(f"KEPLER PLATE LOW-ANGLE FLUX | run {stamp}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SCENE_IMAGE.exists(), f"missing: {SCENE_IMAGE}"

    scene_url = upload(SCENE_IMAGE)
    model = "fal-ai/flux-pro/kontext/max"
    print(f"\n  {model}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_url": scene_url,
                "prompt": PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
                "guidance_scale": 3.5,
                "safety_tolerance": "5",
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        saved = []
        for i, url in enumerate(urls):
            suffix = "" if i == 0 else f"_{i}"
            name = f"kepler_plate_lowangle_flux_{stamp}{suffix}"
            p = save_image(url, name)
            saved.append(str(p.name))

        append_record({
            "run": stamp, "model": model, "prompt": PROMPT,
            "elapsed_s": round(elapsed, 1),
            "images": urls, "saved": saved,
            "scene": str(SCENE_IMAGE.name),
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s — {len(urls)} image(s)")
        print(f"  Saved: {saved}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": model, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
