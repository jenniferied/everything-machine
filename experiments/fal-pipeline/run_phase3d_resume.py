#!/usr/bin/env python3
"""
Experiment 9 — Phase 3d RESUME:
- Replace tokyo_rain → night_drive (retro car, moon, stars)
- Redo night_drive portraits (both models) since tokyo_rain portraits are unwanted
- Generate missing NanoBanana pool_floaty portrait
- Generate all 8 landscape images
Total: 13 images (~$1.51)
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
RESULTS_FILE = SCRIPT_DIR / "phase3d_resume_results.json"
INPUTS = SCRIPT_DIR / "inputs"

INPUT_PORTRAIT = INPUTS / "kepler-posed-portrait-padded.png"
INPUT_LANDSCAPE = INPUTS / "kepler-posed-landscape-padded.png"

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
        "name": "night_drive",
        "gpt": (
            "Background: A long empty night road stretching into the distance, full moon and stars visible in a clear dark sky, distant mountain silhouettes on the horizon. "
            "Center: This faceless voxel character sits behind the wheel of a vintage 1970s convertible car, one hand on the steering wheel, cruising down the road. "
            "Details: Dashboard glowing faintly, headlights illuminating the road ahead, retro film grain aesthetic, cinematic wide composition. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses."
        ),
        "nb": (
            "This voxel character is driving a vintage 1970s convertible down a long empty road at night. "
            "A big full moon and stars fill the dark sky, mountains visible in the distance. "
            "He has one hand on the steering wheel, headlights lighting up the road ahead. Retro cinematic vibes, film grain look. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic throughout."
        ),
    },
    {
        "name": "spiral_staircase",
        "gpt": (
            "Background: Infinite deep space filled with galaxies, nebulae, and scattered stars in purple and blue hues. "
            "Center: This faceless voxel character climbs an endless spiral staircase that winds upward through clouds. "
            "Details: The staircase is made of the same voxel blocks as the character — blocky, geometric, pixel-art style steps that glow with a soft blue light. "
            "The steps emit a blue neon glow. No railing, floating freely in space, passes through layers of soft clouds. Ethereal blue lighting from the staircase itself. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses. "
            "The staircase is NOT marble or stone — it glows blue. Composition suggests infinite continuation — seamlessly loopable."
        ),
        "nb": (
            "This voxel character walks up an endless spiral staircase floating through deep space. "
            "The staircase is built from the same voxel cubes as the character — blocky geometric steps that glow with soft blue light. "
            "The steps emit a blue neon glow, NOT marble, NOT stone. "
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


def run_gpt(scene_name, prompt, fmt_tag, image_url):
    model = "fal-ai/gpt-image-1.5/edit"
    tag = f"gpt15_{scene_name}_{fmt_tag}"
    print(f"\n  GPT-1.5 | {scene_name} | {fmt_tag}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            "quality": "high",
            "size": "auto",
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"19_gpt15_final_{fmt_tag}", scene_name)
        log(tag, model, prompt, elapsed, "$0.08", urls, fmt_tag)
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.08", [], fmt_tag, str(e))


def run_nanobanana(scene_name, prompt, fmt_tag, image_url, nb_ratio):
    model = "fal-ai/nano-banana-pro/edit"
    tag = f"nb_{scene_name}_{fmt_tag}"
    print(f"\n  NanoBanana | {scene_name} | {fmt_tag}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(model, arguments={
            "image_urls": [image_url],
            "prompt": prompt,
            "aspect_ratio": nb_ratio,
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"20_nanobanana_final_{fmt_tag}", scene_name)
        log(tag, model, prompt, elapsed, "$0.15", urls, fmt_tag)
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.15", [], fmt_tag, str(e))


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 3d RESUME")
    print(f"Redo: night_drive (2) + staircase (2) portraits")
    print(f"Missing: NB pool_floaty portrait (1)")
    print(f"New: all 8 landscapes")
    print(f"Total: 13 images, ~$1.51")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    portrait_url = upload(INPUT_PORTRAIT)

    # --- 1) New night_drive portraits (replacing tokyo_rain) ---
    print(f"\n{'='*60}")
    print("PART 1: Night Drive portraits (new scene, replaces tokyo_rain)")
    print(f"{'='*60}")
    drive = next(s for s in SCENES if s["name"] == "night_drive")
    run_gpt("night_drive", drive["gpt"], "portrait", portrait_url)
    run_nanobanana("night_drive", drive["nb"], "portrait", portrait_url, "9:16")

    # --- 2) Redo spiral_staircase portraits (now blue glowing) ---
    print(f"\n{'='*60}")
    print("PART 2: Spiral Staircase portraits (blue glow, redo)")
    print(f"{'='*60}")
    stairs = next(s for s in SCENES if s["name"] == "spiral_staircase")
    run_gpt("spiral_staircase", stairs["gpt"], "portrait", portrait_url)
    run_nanobanana("spiral_staircase", stairs["nb"], "portrait", portrait_url, "9:16")

    # --- 3) Missing NanoBanana portrait: pool_floaty ---
    print(f"\n{'='*60}")
    print("PART 3: Missing NanoBanana portrait (pool_floaty)")
    print(f"{'='*60}")
    pool = next(s for s in SCENES if s["name"] == "pool_floaty")
    run_nanobanana("pool_floaty", pool["nb"], "portrait", portrait_url, "9:16")

    # --- 3) All 8 landscape images ---
    print(f"\n{'='*60}")
    print("PART 3: All 8 landscape images")
    print(f"{'='*60}")
    landscape_url = upload(INPUT_LANDSCAPE)
    for scene in SCENES:
        run_gpt(scene["name"], scene["gpt"], "landscape", landscape_url)
        run_nanobanana(scene["name"], scene["nb"], "landscape", landscape_url, "16:9")

    print(f"\n{'='*60}\nPHASE 3d RESUME COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Tests: {total}, OK: {ok_count}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['format']} — {r['elapsed_s']}s")


if __name__ == "__main__":
    main()
