#!/usr/bin/env python3
"""
Sie-schreibt Driving — Input-Image-Varianten fuer ein Driving-Video.

Kepler (voxel character, baseball cap mit flat brim, NICHT Kapuze) im Cabrio
bei Vollmond. Verschiedene Framings testen.

Source-Refs:
- inputs/sie-schreibt/seedance-cadillac-frontal-mond.jpeg  (frontal hero shot)
- inputs/sie-schreibt/gpt-cockpit-pov-mond-wueste.jpeg     (cockpit pov)
- outputs/spiral_upscale/spiral_upscale_clarity_edited.png (canonical voxel char)

Model: fal-ai/nano-banana-pro/edit  (~$0.04/image)
6 Varianten = ~$0.24
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_driving"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_driving_results.json"

INPUT_DIR = SCRIPT_DIR / "inputs" / "sie-schreibt"
REF_CADILLAC = INPUT_DIR / "seedance-cadillac-frontal-mond.jpeg"
REF_COCKPIT = INPUT_DIR / "gpt-cockpit-pov-mond-wueste.jpeg"
REF_VOXEL_CHAR = SCRIPT_DIR / "outputs" / "spiral_upscale" / "spiral_upscale_clarity_edited.png"

CHAR_DESC = (
    "The character is a small voxel/lego-style figure made of small cubic "
    "blocks — light grey/white blocky body, blocky arms with visible cubic "
    "texture. He wears a dark baseball cap with a flat brim (NOT a hood, NOT "
    "a hoodie, NOT a helmet). The cap shape is identical to the reference: "
    "flat curved brim pointing forward, structured crown. Face features are "
    "minimal/abstract — no detailed eyes or mouth."
)

NEGATIVE_HINTS = (
    "Avoid: hooded figure, hoodie, robe, cloak, hood, monk, druid, bowler "
    "hat, top hat, fedora, helmet, dome head, realistic human face."
)

VARIANTS = [
    {
        "name": "01_frontal_cadillac_dunes",
        "refs": [REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Edit the first image. Keep the frontal hero shot of the lego-block "
            f"convertible Cadillac on a desert road at night, full moon high in "
            f"the starry sky, distant mountains, warm headlight glow. "
            f"Replace the driver with the voxel character from the second image. "
            f"{CHAR_DESC} He sits behind the wheel, visible from chest up "
            f"through the windshield. Cinematic 16:9, cool moonlit blues + warm "
            f"headlight ambers. {NEGATIVE_HINTS}"
        ),
    },
    {
        "name": "02_cockpit_pov_passenger",
        "refs": [REF_COCKPIT, REF_VOXEL_CHAR],
        "prompt": (
            f"Edit the first image. Keep the cockpit POV from inside a "
            f"convertible: dashboard with glowing instrument cluster, "
            f"desert road stretching to a distant horizon, full moon in the "
            f"starry night sky. The driver visible on the left side is the "
            f"voxel character from the second image. {CHAR_DESC} He grips the "
            f"steering wheel with both blocky voxel hands. Maintain the dreamy "
            f"midnight palette. {NEGATIVE_HINTS}"
        ),
    },
    {
        "name": "03_side_tracking_road",
        "refs": [REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a cinematic side tracking shot of the lego-block "
            f"convertible Cadillac driving along an empty desert highway at "
            f"night. Camera at car level, slightly behind side. Full moon huge "
            f"and low on the horizon, casting silver light. Mountains in the "
            f"distance. Inside the car the voxel character from the second "
            f"image is driving. {CHAR_DESC} Motion blur on the wheels and "
            f"road. 16:9 cinematic. {NEGATIVE_HINTS}"
        ),
    },
    {
        "name": "04_low_angle_hilltop",
        "refs": [REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a low angle hero shot: the lego-block convertible Cadillac "
            f"cresting a small desert hill at night, headlights blazing, full "
            f"moon enormous in the sky directly behind/above the car like a "
            f"halo. The voxel character from the second image is driving, "
            f"visible above the windshield. {CHAR_DESC} Stars, distant "
            f"mountains. Cinematic, slightly underexposed. 16:9. "
            f"{NEGATIVE_HINTS}"
        ),
    },
    {
        "name": "05_behind_chase",
        "refs": [REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a behind-the-car chase shot: camera follows the lego-block "
            f"convertible Cadillac from directly behind at road level. Empty "
            f"two-lane desert highway disappearing into the horizon. Tail "
            f"lights glowing red. Full moon high in the starry sky ahead. The "
            f"voxel character driver visible from behind, head and cap above "
            f"the seat-back. {CHAR_DESC} 16:9 cinematic. {NEGATIVE_HINTS}"
        ),
    },
    {
        "name": "06_serpentine_aerial",
        "refs": [REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a high cinematic aerial shot of the lego-block convertible "
            f"Cadillac driving along a serpentine mountain road at night, "
            f"headlights cutting through darkness. Full moon huge in the sky, "
            f"silvering the cliffs and switchbacks. Camera at ~30 degrees above "
            f"horizontal, following from above-behind. Visible driver is the "
            f"voxel character. {CHAR_DESC} 16:9 cinematic. {NEGATIVE_HINTS}"
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
    print(f"SIE-SCHREIBT DRIVING | run {stamp}")
    print(f"  {len(VARIANTS)} Varianten, geschaetzt ~${len(VARIANTS) * 0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for ref in [REF_CADILLAC, REF_COCKPIT, REF_VOXEL_CHAR]:
        assert ref.exists(), f"missing: {ref}"

    print("\nUploading references (cached)...")
    url_cache = {}
    for ref in [REF_CADILLAC, REF_COCKPIT, REF_VOXEL_CHAR]:
        url_cache[ref] = upload(ref)

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
    print(f"DONE: {successes}/{len(VARIANTS)} erfolgreich")
    print(f"Outputs: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
