#!/usr/bin/env python3
"""Batch: several low-angle prompt variants via flux-pro/kontext/max."""

import os
import json
import time
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "kepler_lowangle_batch"
RESULTS_FILE = SCRIPT_DIR / "kepler_lowangle_batch_results.json"

SCENE_IMAGE = (
    SCRIPT_DIR / "outputs" / "spiral_upscale"
    / "spiral_upscale_clarity_edited.png"
)

VARIANTS = {
    "mild10": "Tilt the camera up by 10 degrees. Gentle low-angle, keep composition.",
    "mild15": "Tilt the camera up by 15 degrees. Mild low-angle, keep composition.",
    "mild20": "Tilt the camera up by 20 degrees. Moderate low-angle, keep composition.",
    "slightlylower": "Lower the camera height slightly and tilt it up gently. Mild low-angle, same scene and framing otherwise.",
}


def upload(p):
    return fal_client.upload_file(str(p))


def save(url, name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out = OUTPUT_DIR / f"{name}{ext}"
    out.write_bytes(httpx.get(url, timeout=120).content)
    return out


def append(rec):
    items = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else []
    items.append(rec)
    RESULTS_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False))


def main():
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY")
        return
    print(f"Uploading {SCENE_IMAGE.name}...")
    img_url = upload(SCENE_IMAGE)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model = "fal-ai/flux-pro/kontext/max"
    for tag, prompt in VARIANTS.items():
        print(f"\n[{tag}] {prompt[:60]}...")
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "image_url": img_url, "prompt": prompt,
                    "aspect_ratio": "16:9", "num_images": 1,
                    "guidance_scale": 3.5, "safety_tolerance": "5",
                },
                with_logs=False,
            )
            elapsed = time.time() - t0
            urls = [i["url"] for i in result.get("images", [])]
            saved = [save(u, f"flux_{tag}_{stamp}").name for u in urls]
            print(f"  OK {elapsed:.1f}s -> {saved}")
            append({"tag": tag, "prompt": prompt, "saved": saved, "model": model, "stamp": stamp})
        except Exception as e:
            print(f"  ERR: {e}")


if __name__ == "__main__":
    main()
