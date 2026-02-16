#!/usr/bin/env python3
"""
Experiment 9 — Phase 3d: Final Signature Scenes
Fix: GPT size param ignored on edit → use padded inputs + size=auto for both models.
Fix: Stairs no longer marble, voxel-style instead.
Fix: NanoBanana gets both padded input AND explicit aspect_ratio as belt-and-suspenders.
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
RESULTS_FILE = SCRIPT_DIR / "phase3d_results.json"
INPUTS = SCRIPT_DIR / "inputs"

# Padded (NOT stretched) inputs — both models use these
INPUT_PORTRAIT = INPUTS / "kepler-posed-portrait-padded.png"   # 1024x1536
INPUT_LANDSCAPE = INPUTS / "kepler-posed-landscape-padded.png"  # 1536x1024

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
            "Center: This faceless voxel character climbs an endless spiral staircase that winds upward through clouds. "
            "Details: The staircase is made of the same voxel blocks as the character — blocky, geometric, pixel-art style steps. "
            "No railing, floating freely in space, passes through layers of soft clouds. Ethereal lighting from below. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses. "
            "Composition suggests infinite continuation — seamlessly loopable."
        ),
        "nb": (
            "This voxel character walks up an endless spiral staircase floating through deep space. "
            "The staircase is built from the same voxel cubes as the character — blocky geometric steps, not smooth marble. "
            "Stars and galaxies surround it, soft clouds drift by at different levels. Surreal dreamlike feeling. "
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
    {"tag": "portrait", "input_file": INPUT_PORTRAIT, "nb_ratio": "9:16"},
    {"tag": "landscape", "input_file": INPUT_LANDSCAPE, "nb_ratio": "16:9"},
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
    # Check actual dimensions
    from PIL import Image
    from io import BytesIO
    img = Image.open(BytesIO(resp.content))
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB) — {img.size[0]}x{img.size[1]}")
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
    print(f"\n  GPT-1.5 | {scene_name} | {fmt['tag']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            "quality": "high",
            "size": "auto",  # auto = match input dimensions
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"19_gpt15_final_{fmt['tag']}", scene_name)
        log(tag, model, prompt, elapsed, "$0.08", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.08", [], fmt["tag"], str(e))


def run_nanobanana(scene_name, prompt, fmt, image_url):
    model = "fal-ai/nano-banana-pro/edit"
    tag = f"nb_{scene_name}_{fmt['tag']}"
    print(f"\n  NanoBanana | {scene_name} | {fmt['tag']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            "aspect_ratio": fmt["nb_ratio"],  # explicit ratio as backup
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"20_nanobanana_final_{fmt['tag']}", scene_name)
        log(tag, model, prompt, elapsed, "$0.15", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.15", [], fmt["tag"], str(e))


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 3d: Final Signature Scenes")
    print(f"Fix: padded inputs for BOTH models, size=auto for GPT")
    print(f"Fix: voxel stairs instead of marble")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for fmt in FORMATS:
        img_url = upload(fmt["input_file"])
        for scene in SCENES:
            run_gpt(scene["name"], scene["gpt"], fmt, img_url)
            run_nanobanana(scene["name"], scene["nb"], fmt, img_url)

    print(f"\n{'='*60}\nPHASE 3d COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Tests: {total}, OK: {ok_count}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['format']} — {r['elapsed_s']}s")


if __name__ == "__main__":
    main()
