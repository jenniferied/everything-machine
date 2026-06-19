#!/usr/bin/env python3
"""
Sie-schreibt Cockpit V2 — Cockpit POV mit realistischerem Interior.

Erstes Cockpit (02_cockpit_pov_passenger) war konzeptuell richtig, aber:
- Lenkrad-Geometrie / Haende-Position kaputt
- Armaturenbrett zu schematisch / nicht ueberzeugend

Diese Runde: realistisches 70s Cadillac Convertible Interior + sauberes
Lenkrad, Voxel-Haende sitzen plausibel am Wheel. 4 Sub-Varianten.

Model: fal-ai/nano-banana-pro/edit  (~$0.04/img, 4 = ~$0.16)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_cockpit_v2"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_cockpit_v2_results.json"

REF_GPT_COCKPIT = SCRIPT_DIR / "inputs" / "sie-schreibt" / "gpt-cockpit-pov-mond-wueste.jpeg"
REF_CADILLAC = SCRIPT_DIR / "inputs" / "sie-schreibt" / "seedance-cadillac-frontal-mond.jpeg"
REF_VOXEL_CHAR = SCRIPT_DIR / "outputs" / "spiral_upscale" / "spiral_upscale_clarity_edited.png"
REF_PREV_BEST = SCRIPT_DIR / "outputs" / "sie_schreibt_driving" / "02_cockpit_pov_passenger_20260519_221446.png"

CHAR_DESC = (
    "The driver is a small voxel/lego-style figure: light grey/white blocky "
    "body made of small cubic blocks, visible cubic texture on arms and "
    "shoulders. He wears a dark baseball cap with a flat curved brim pointing "
    "forward (NOT a hood, NOT a hoodie). Abstract minimal face — no "
    "photoreal eyes or mouth. Blocky voxel hands grip the steering wheel "
    "naturally — fingers wrapped around the rim at roughly 9 and 3 o'clock."
)

INTERIOR_BASE = (
    "Realistic vintage 1970s American convertible car interior: dark "
    "leather/vinyl dashboard with subtle stitching, real chrome trim around "
    "the instrument cluster, four clearly visible analog gauges (speedometer, "
    "tachometer, fuel, temperature) glowing with warm amber backlight. "
    "Wood-grain accents on the center console. A correctly proportioned "
    "round steering wheel with a chrome horn ring and a chrome center hub "
    "with a small enamel emblem. The windshield frame is visible at the "
    "edges. Subtle reflections of the moonlight on the chrome and glass."
)

WORLD = (
    "Through the windshield: an empty desert two-lane highway at night "
    "stretching to a distant horizon, full moon high in a starry sky, low "
    "silhouetted mountains on both sides. Headlights cast warm pools of light "
    "on the asphalt ahead."
)

NEG = (
    "Avoid: hooded figure, hoodie, robe, monk, melted dashboard, deformed "
    "steering wheel, extra fingers, missing wheel rim, fantasy interior, "
    "neon multi-color dashboard, garish colors."
)

VARIANTS = [
    {
        "name": "01_realistic_70s_cadillac_interior",
        "refs": [REF_PREV_BEST, REF_VOXEL_CHAR],
        "prompt": (
            f"Edit the first image to fix the cockpit and replace the interior "
            f"with a realistic, photographically detailed cockpit. Keep the "
            f"voxel character driver, his cap, the night-desert world through "
            f"the windshield, and the cinematic moonlit mood. "
            f"NEW INTERIOR: {INTERIOR_BASE} "
            f"DRIVER: {CHAR_DESC} "
            f"WORLD: {WORLD} "
            f"Cinematic 16:9, soft moonlit blues plus warm amber dash glow. "
            f"{NEG}"
        ),
    },
    {
        "name": "02_lower_angle_steering_centered",
        "refs": [REF_PREV_BEST, REF_VOXEL_CHAR],
        "prompt": (
            f"Re-frame this shot from a slightly lower angle: the camera is at "
            f"the passenger seat looking left-forward, so the steering wheel "
            f"is more centered in the frame and we see both voxel hands "
            f"gripping it. The dashboard fills the lower third. "
            f"INTERIOR: {INTERIOR_BASE} "
            f"DRIVER: {CHAR_DESC} "
            f"WORLD: {WORLD} "
            f"Cinematic 16:9. {NEG}"
        ),
    },
    {
        "name": "03_first_person_driver_pov",
        "refs": [REF_GPT_COCKPIT, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a first-person driver POV: the camera sits where the "
            f"driver's eyes would be, looking forward over the steering wheel "
            f"and dashboard onto the desert road. Voxel hands visible at the "
            f"bottom of the frame gripping the wheel at 9 and 3. "
            f"INTERIOR: {INTERIOR_BASE} "
            f"WORLD: {WORLD} The steering wheel rim and chrome center "
            f"emblem dominate the lower half of the frame. "
            f"HANDS: blocky voxel hands as in the third reference, "
            f"light-grey cubic texture, fingers wrapping the wheel naturally. "
            f"Cinematic 16:9, depth of field with road slightly soft. {NEG}"
        ),
    },
    {
        "name": "04_three_quarter_dashboard_hero",
        "refs": [REF_PREV_BEST, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a 3/4 interior shot from the back-passenger angle: the "
            f"voxel driver is on the left mid-frame, the realistic dashboard "
            f"and steering wheel are on the right, the windshield occupies "
            f"the upper third showing the moonlit desert road ahead. The "
            f"dashboard gauges glow warm amber and reflect on the dark vinyl. "
            f"DRIVER: {CHAR_DESC} "
            f"INTERIOR: {INTERIOR_BASE} "
            f"WORLD: {WORLD} "
            f"Cinematic 16:9. {NEG}"
        ),
    },
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


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
    print(f"COCKPIT V2 | run {stamp}  | {len(VARIANTS)} Varianten ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    all_refs = {REF_GPT_COCKPIT, REF_CADILLAC, REF_VOXEL_CHAR, REF_PREV_BEST}
    for r in all_refs:
        assert r.exists(), f"missing: {r}"

    print("\nUploading references...")
    url_cache = {r: upload(r) for r in all_refs}

    model = "fal-ai/nano-banana-pro/edit"
    successes = 0

    for v in VARIANTS:
        print(f"\n--- {v['name']} ---")
        refs = [url_cache[r] for r in v["refs"]]
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "image_urls": refs,
                    "prompt": v["prompt"],
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
                name = f"{v['name']}_{stamp}{suffix}"
                p = save_image(url, name)
                saved.append(str(p.name))
            append_record({
                "run": stamp, "variant": v["name"], "model": model,
                "prompt": v["prompt"], "refs": [r.name for r in v["refs"]],
                "aspect_ratio": "16:9", "elapsed_s": round(elapsed, 1),
                "images": urls, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
            print(f"  OK in {elapsed:.1f}s -> {saved}")
            successes += 1
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "variant": v["name"], "model": model,
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "timestamp": datetime.now().isoformat(),
            })

    print("\n" + "=" * 60)
    print(f"DONE: {successes}/{len(VARIANTS)} -> {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
