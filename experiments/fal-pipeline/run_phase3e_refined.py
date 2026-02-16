#!/usr/bin/env python3
"""
Experiment 9 — Phase 3e: Refined Scenes (final iteration)
- Staircase: clouds + soft sky, less intense galaxies, blue glow
- Night Drive: retro car (not vintage), city behind, mountains ahead
- Pool: more poolside enrichment (loungers, drinks, towels, plants)
3 scenes × 2 formats × 2 models = 12 images (~$1.38)
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
RESULTS_FILE = SCRIPT_DIR / "phase3e_results.json"
INPUTS = SCRIPT_DIR / "inputs"

INPUT_PORTRAIT = INPUTS / "kepler-posed-portrait-padded.png"
INPUT_LANDSCAPE = INPUTS / "kepler-posed-landscape-padded.png"

SCENES = [
    {
        "name": "night_drive",
        "gpt": (
            "Background: A wide night road cutting through a valley, a glowing city skyline receding behind the car, "
            "dark mountain range rising ahead on the horizon, full moon low in the sky, scattered stars. "
            "Center: This faceless voxel character sits behind the wheel of a sleek retro sports car (1980s style, pop-up headlights), "
            "one hand on the steering wheel, cruising forward. "
            "Details: Dashboard instruments glowing softly, headlights cutting through light mist on the road, "
            "retro synthwave color palette with teal and magenta tones, cinematic composition. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses."
        ),
        "nb": (
            "This voxel character is cruising down a night road in a sleek retro 1980s sports car with pop-up headlights. "
            "Behind him a glowing city skyline fades into the distance. Ahead, dark mountains rise on the horizon. "
            "Full moon in the sky, stars visible. Dashboard glowing softly, headlights cutting through mist. "
            "Retro synthwave vibes with teal and magenta tones. "
            "IMPORTANT: The character must remain completely faceless — no eyes, no nose, no mouth, no sunglasses. "
            "The head is a smooth blank block of voxels. Keep the blocky cube aesthetic throughout."
        ),
    },
    {
        "name": "spiral_staircase",
        "gpt": (
            "Background: A dreamy sky filled with soft layered clouds in pastel blue and lavender tones, "
            "a few distant stars peeking through gaps in the clouds, gentle twilight atmosphere — NOT heavy galaxies or nebulae. "
            "Center: This faceless voxel character climbs an endless spiral staircase that winds upward through the clouds. "
            "Details: The staircase is made of the same voxel blocks as the character — blocky, geometric, pixel-art style steps "
            "that emit a soft blue neon glow. No railing, floating freely in the sky, passes through layers of soft clouds. "
            "Ethereal blue lighting from the staircase itself. Calm, serene, dreamlike mood. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. No sunglasses. "
            "The staircase is NOT marble or stone — it glows blue. Composition suggests infinite continuation — seamlessly loopable."
        ),
        "nb": (
            "This voxel character walks up an endless spiral staircase floating through a dreamy cloudy sky. "
            "The sky is soft pastel blue and lavender with layered clouds, a few stars peeking through — "
            "NOT intense galaxies, just a calm dreamy twilight atmosphere. "
            "The staircase is built from the same voxel cubes as the character — blocky geometric steps that glow with soft blue neon light. "
            "No railing, floating freely, passing through cloud layers. Serene and dreamlike. "
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
            "Details: Arms behind head, legs dangling in water. Crystal clear water with light caustics and ripples. "
            "Pool edge visible with white sun loungers, a small table with a colorful cocktail drink and sunscreen bottle, "
            "potted tropical plants, folded towels, flip-flops on the tiles. Palm tree shadows on the pool surface. Luxurious summer resort feel. "
            "Constraints: The character has NO face — the head is a smooth blank surface of voxel cubes. No eyes, no nose, no mouth. "
            "NO sunglasses anywhere in the image. The pool float MUST have a hole in the center (donut/ring shape, not solid disc)."
        ),
        "nb": (
            "Top-down bird's eye view of a turquoise swimming pool at a luxurious summer resort. "
            "This voxel character is lying on an inflatable pool ring (donut shape with a hole in the middle, not a solid float) drifting in the water. "
            "He's relaxed with arms behind his head. Crystal clear water with beautiful light caustics. "
            "Around the pool edge: white sun loungers, a small table with a cocktail and sunscreen, "
            "tropical potted plants, neatly folded towels, flip-flops on the tiles. Palm tree shadows on the surface. "
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
            "size": "auto",
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"21_gpt15_refined_{fmt['tag']}", scene_name)
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
            "aspect_ratio": fmt["nb_ratio"],
        }, with_logs=True, on_queue_update=on_queue)
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        for url in urls:
            save_image(url, f"22_nanobanana_refined_{fmt['tag']}", scene_name)
        log(tag, model, prompt, elapsed, "$0.15", urls, fmt["tag"])
        print(f"    OK in {elapsed:.1f}s")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(tag, model, prompt, elapsed, "$0.15", [], fmt["tag"], str(e))


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 3e: Refined Scenes")
    print(f"3 Scenes × 2 Formats × 2 Models = 12 images")
    print(f"Staircase: clouds + blue glow (less galaxies)")
    print(f"Night Drive: retro car, city behind, mountains ahead")
    print(f"Pool: enriched poolside (loungers, drinks, plants)")
    print(f"Estimated cost: ~$1.38")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for fmt in FORMATS:
        img_url = upload(fmt["input_file"])
        print(f"\n{'='*60}")
        print(f"FORMAT: {fmt['tag']}")
        print(f"{'='*60}")
        for scene in SCENES:
            run_gpt(scene["name"], scene["gpt"], fmt, img_url)
            run_nanobanana(scene["name"], scene["nb"], fmt, img_url)

    print(f"\n{'='*60}\nPHASE 3e COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Tests: {total}, OK: {ok_count}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['format']} — {r['elapsed_s']}s")


if __name__ == "__main__":
    main()
