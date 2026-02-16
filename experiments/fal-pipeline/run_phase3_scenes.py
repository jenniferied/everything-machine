#!/usr/bin/env python3
"""
Experiment 9 — Phase 3: Kepler Signature Scenes
NanoBanana Pro + GPT-Image-1.5 in Portrait (9:16) + Landscape (16:9)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs"
RESULTS_FILE = SCRIPT_DIR / "phase3_scenes_results.json"

POSED_URL = "https://v3b.fal.media/files/b/0a8e964a/jHxnlduIxgo9t5v8Yd_JU_kepler-posed-1024.png"

SCENES = [
    {
        "name": "studio",
        "prompt": "Place this voxel character in a professional recording studio, sitting at a large mixing console with both hands on the faders, studio monitors glowing, headphones on, warm amber lighting, acoustic foam panels on walls, DAW software visible on screens behind him, intimate atmosphere",
    },
    {
        "name": "retro_car_bridge",
        "prompt": "Place this voxel character driving a vintage 1970s convertible car across a long suspension bridge at night, city lights reflecting on the water below, snow-capped mountains in the background, moonlight, cinematic wide shot, headlights cutting through light fog, retro film grain aesthetic",
    },
    {
        "name": "spiral_staircase",
        "prompt": "Place this voxel character walking up an endless spiral staircase that extends infinitely into the sky, passing through layers of clouds and stars, surreal dreamlike atmosphere, the staircase is white marble floating in deep space, galaxies and nebulae visible, ethereal blue and purple lighting, seamlessly loopable composition",
    },
    {
        "name": "pool_floaty",
        "prompt": "Place this voxel character lying on a pink flamingo pool float in a turquoise swimming pool, seen from directly above as a top-down bird's eye view, sunglasses on the float beside him, palm tree shadows on the water, summer vibes, crystal clear water with light caustics, relaxed pose with arms behind head",
    },
]

FORMATS = [
    {"tag": "portrait", "gpt_size": "1024x1792", "nb_ratio": "9:16"},
    {"tag": "landscape", "gpt_size": "1792x1024", "nb_ratio": "16:9"},
]

results = []


def save_image(url: str, folder: str, name: str) -> Path:
    out_dir = OUTPUT_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = out_dir / f"{name}{ext}"
    resp = httpx.get(url, timeout=60)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log(test, model, prompt, elapsed, cost, urls, fmt, error=None):
    results.append({
        "test": test, "model": model, "prompt": prompt[:80],
        "format": fmt, "elapsed_s": round(elapsed, 1), "cost_est": cost,
        "images": urls, "error": error, "timestamp": datetime.now().isoformat(),
    })
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for l in update.logs:
            print(f"      [{l.get('message', '')}]")


def run_gpt(scene_name, prompt, fmt):
    model = "fal-ai/gpt-image-1.5/edit"
    tag = f"gpt15_{scene_name}_{fmt['tag']}"
    print(f"\n  GPT-1.5 | {scene_name} | {fmt['tag']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [POSED_URL],
            "prompt": prompt,
            "quality": "high",
            "size": fmt["gpt_size"],
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"13_gpt15_scenes_{fmt['tag']}", f"{scene_name}")
        log(tag, model, prompt, elapsed, "$0.08", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.08", [], fmt["tag"], str(e))


def run_nanobanana(scene_name, prompt, fmt):
    model = "fal-ai/nano-banana-pro/edit"
    tag = f"nb_{scene_name}_{fmt['tag']}"
    print(f"\n  NanoBanana | {scene_name} | {fmt['tag']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [POSED_URL],
            "prompt": f"Take the voxel character from the reference image. {prompt} "
                      f"Keep the blocky voxel cube aesthetic throughout, no face details.",
            "aspect_ratio": fmt["nb_ratio"],
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"14_nanobanana_scenes_{fmt['tag']}", f"{scene_name}")
        log(tag, model, prompt, elapsed, "$0.15", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.15", [], fmt["tag"], str(e))


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 3: Kepler Signature Scenes")
    print(f"4 Scenes × 2 Formats × 2 Models = 16 images")
    print(f"Estimated cost: ~$1.84")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for scene in SCENES:
        print(f"\n{'='*60}")
        print(f"SCENE: {scene['name']}")
        print(f"{'='*60}")
        for fmt in FORMATS:
            run_gpt(scene["name"], scene["prompt"], fmt)
            run_nanobanana(scene["name"], scene["prompt"], fmt)

    print(f"\n{'='*60}\nPHASE 3 SCENES COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    print(f"Tests: {total}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
