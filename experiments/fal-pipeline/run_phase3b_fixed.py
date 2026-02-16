#!/usr/bin/env python3
"""
Experiment 9 — Phase 3b: Fixed Signature Scenes
Fixes: correct GPT sizes, pre-resized inputs for NanoBanana, stronger no-face prompts,
replaced bridge scene, fixed pool floaty.
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
RESULTS_FILE = SCRIPT_DIR / "phase3c_results.json"
INPUTS = SCRIPT_DIR / "inputs"

# GPT uses the square original — size param controls output ratio
INPUT_SQUARE = INPUTS / "kepler-posed-1024.png"          # 1024x1024
# NanoBanana needs padded inputs (stretched = distorted, aspect_ratio param unreliable)
INPUT_NB_PORTRAIT = INPUTS / "kepler-posed-portrait-padded.png"   # 1024x1536 padded
INPUT_NB_LANDSCAPE = INPUTS / "kepler-posed-landscape-padded.png"  # 1536x1024 padded

# Scenes — structured for GPT (spatial), conversational for NanoBanana
SCENES = [
    {
        "name": "studio",
        "gpt": (
            "Background: A professional recording studio with acoustic foam walls, warm amber lighting, two glowing studio monitors. "
            "Center: This faceless voxel character sits at a large analog mixing console, both hands resting on the faders. "
            "Details: Headphones on head, DAW software on multiple screens behind him, cable mess on the floor. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses."
        ),
        "nb": (
            "Show this voxel character in a cozy recording studio. He's sitting at a big mixing desk with his hands on the faders, "
            "wearing headphones. Warm amber lighting, acoustic panels on walls, DAW screens glowing behind him. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic throughout."
        ),
    },
    {
        "name": "tokyo_rain",
        "gpt": (
            "Background: A rain-soaked Tokyo alley at night, dense with neon signs in Japanese, steam rising from vents, puddles reflecting pink and cyan lights. "
            "Center: This faceless voxel character walks toward the camera through the rain, hands relaxed at sides. "
            "Details: Wet pavement reflections, light fog, moody noir atmosphere, shot from slightly low angle. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses."
        ),
        "nb": (
            "This voxel character is walking through a rainy Tokyo alley at night. Neon signs everywhere in Japanese, "
            "steam rising from street vents, puddles reflecting pink and blue light. Moody cinematic atmosphere. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic throughout."
        ),
    },
    {
        "name": "spiral_staircase",
        "gpt": (
            "Background: Infinite deep space filled with galaxies, nebulae, and scattered stars in purple and blue hues. "
            "Center: This faceless voxel character climbs an endless white marble spiral staircase that winds upward through clouds. "
            "Details: The staircase has no railing, floats freely in space, passes through layers of soft clouds. Ethereal lighting from below. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses. "
            "Composition suggests infinite continuation — seamlessly loopable."
        ),
        "nb": (
            "This voxel character walks up an endless spiral staircase made of white marble, floating through deep space. "
            "Stars and galaxies surround the staircase, soft clouds drift by at different levels. Surreal dreamlike feeling. "
            "The staircase spirals infinitely upward — make the composition feel endlessly loopable. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic throughout."
        ),
    },
    {
        "name": "pool_floaty",
        "gpt": (
            "Camera: Directly overhead, bird's eye view looking straight down at a turquoise swimming pool. "
            "Center: This faceless voxel character lies relaxed on a pink inflatable pool ring (donut shape with hole in center) floating in the pool. "
            "Details: Arms behind head, legs dangling in water. Crystal clear water with light caustics and ripples. Palm tree shadows on pool surface. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. "
            "NO sunglasses anywhere in the image. The pool float MUST have a hole in the center (donut/ring shape, not solid disc)."
        ),
        "nb": (
            "Top-down bird's eye view of a turquoise swimming pool. This voxel character is lying on an inflatable pool ring "
            "(donut shape with a hole in the middle, not a solid float) drifting in the water. He's relaxed with arms behind his head. "
            "Crystal clear water with beautiful light caustics, palm tree shadows on the surface. Summer vibes. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The pool ring MUST be a ring/donut shape with a visible hole in the center. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic."
        ),
    },
]

FORMATS = [
    {"tag": "portrait", "gpt_size": "1024x1536", "nb_input": INPUT_NB_PORTRAIT},
    {"tag": "landscape", "gpt_size": "1536x1024", "nb_input": INPUT_NB_LANDSCAPE},
]

results = []
uploaded_urls = {}


def upload(path: Path) -> str:
    if str(path) not in uploaded_urls:
        print(f"  Uploading {path.name}...")
        uploaded_urls[str(path)] = fal_client.upload_file(str(path))
        print(f"  -> {uploaded_urls[str(path)]}")
    return uploaded_urls[str(path)]


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


def run_gpt(scene_name, prompt, fmt, image_url):
    model = "fal-ai/gpt-image-1.5/edit"
    tag = f"gpt15_{scene_name}_{fmt['tag']}"
    print(f"\n  GPT-1.5 | {scene_name} | {fmt['tag']} ({fmt['gpt_size']})")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            "quality": "high",
            "size": fmt["gpt_size"],
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"17_gpt15_v2_{fmt['tag']}", scene_name)
        log(tag, model, prompt, elapsed, "$0.08", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.08", [], fmt["tag"], str(e))


def run_nanobanana(scene_name, prompt, fmt, image_url):
    model = "fal-ai/nano-banana-pro/edit"
    tag = f"nb_{scene_name}_{fmt['tag']}"
    print(f"\n  NanoBanana | {scene_name} | {fmt['tag']} (pre-resized input)")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            # Omit aspect_ratio — let it auto-detect from pre-resized input
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"18_nanobanana_v2_{fmt['tag']}", scene_name)
        log(tag, model, prompt, elapsed, "$0.15", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.15", [], fmt["tag"], str(e))


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 3b: Fixed Signature Scenes")
    print(f"4 Scenes × 2 Formats × 2 Models = 16 images")
    print(f"Fixes: correct sizes, pre-resized inputs, no-face prompts")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    # GPT always uses the square original — size param handles output ratio
    gpt_url = upload(INPUT_SQUARE)

    for fmt in FORMATS:
        # NanoBanana needs padded input per format
        nb_url = upload(fmt["nb_input"])
        for scene in SCENES:
            run_gpt(scene["name"], scene["gpt"], fmt, gpt_url)
            run_nanobanana(scene["name"], scene["nb"], fmt, nb_url)

    print(f"\n{'='*60}\nPHASE 3b COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    print(f"Tests: {total}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['format']} — {r['elapsed_s']}s")


if __name__ == "__main__":
    main()
