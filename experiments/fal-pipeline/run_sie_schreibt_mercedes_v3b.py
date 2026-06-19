#!/usr/bin/env python3
"""
Sie-schreibt Mercedes V3b — Rerun der 4 Varianten, die V3 ueber Nacht
durch einen Netzwerkabbruch (DNS) verloren hat.

V3 #01 (front) und #02 (rear) sind OK -> bleiben.
Hier neu: 03 interior, 04 wide, 05 3q-rear, 06 magenta.

NEU: exaktes Kennzeichen als Referenzbild
(inputs/sie-schreibt/kennzeichen-kep-le-18.png) — deutsches Schild
'KEP · LE 18', brauner TUEV-Sticker + NRW-Siegel. Das Modell soll das
Plate-Design exakt aus dieser Referenz uebernehmen.

Model: fal-ai/nano-banana-pro/edit (~$0.04 = ~$0.16 total)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes_v3"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_mercedes_v3_results.json"

V2_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes_v2"
REF_V2_INTERIOR = V2_DIR / "03_interior_cockpit_cap_fixed_20260519_224312.png"
REF_V2_WIDE = V2_DIR / "04_wide_establishing_teal_orange_20260519_224312.png"
REF_V2_3Q_REAR = V2_DIR / "05_3q_rear_sodium_neon_20260519_224312.png"
REF_V2_MAGENTA = V2_DIR / "06_front_hero_magenta_cyan_20260519_224312.png"

REF_KEPLER_APOSE = SCRIPT_DIR / "inputs" / "kepler-a-pose-1024.png"
REF_PLATE = SCRIPT_DIR / "inputs" / "sie-schreibt" / "kennzeichen-kep-le-18.png"

CAP_DESC = (
    "He wears a dark navy/black baseball cap, well-structured with a clearly "
    "visible THICK flat curved brim that protrudes forward and casts a "
    "shadow over the upper face. The cap is full and solid, NOT thin. BROWN "
    "voxel hair (small brown cubic blocks, same voxel resolution as the "
    "body) peeks out from under the cap at the back and slightly at the "
    "sides. The face is ABSTRACT and FEATURELESS: pure light-grey voxel "
    "blocks, NO eyes, NO mouth, NO nose. The ear is minimal — barely a "
    "hint, NOT prominent. Cap is opaque."
)

KEPLER_DESC = (
    "Kepler voxel character (strict per the A-pose reference): humanoid "
    "figure of small cubic voxel blocks, white/light-grey blocky upper "
    "body with visible cubic texture, brown voxel hair, dark trousers, "
    "BLOCKY abstract head. " + CAP_DESC + " "
    "DO NOT render him as a cartoon, DO NOT smooth the voxels, DO NOT add "
    "human facial detail."
)

PLATE_DESC = (
    "The car's license plate must match the dedicated license-plate "
    "reference image EXACTLY: a German plate, blue EU strip with 'D' on the "
    "left, then bold black text 'KEP', a brown/orange round TUV sticker, a "
    "round grey registration seal, then 'LE 18'. Reproduce that plate "
    "design and text faithfully and keep it sharp and legible."
)

CAR_DESC = (
    "1976-1985 Mercedes-Benz W123 sedan in deep red: 4 round headlights, "
    "square chrome grille with the three-pointed Mercedes star on top, "
    "chrome bumpers, boxy 4-door sedan silhouette. Period-correct W123 "
    "side mirrors: thin chrome stalks with small rectangular mirror heads "
    "on the front of the doors — NOT modern oversized mirrors."
)

NEG = (
    "Avoid: face features bleeding through cap, eyes on cap, mouth on cap, "
    "transparent cap, cartoonish character, smooth non-voxel character, "
    "Pixar style, anime, prominent detailed ear, oversized modern side "
    "mirrors, round side mirrors, random sticker on grille, blank circular "
    "sticker, wrong license plate text."
)

VARIANTS = [
    {
        "name": "03_interior_cap_thick_hair_seatbelt",
        "ar": "16:9",
        "refs": [REF_V2_INTERIOR, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the Mercedes W123 interior exactly: "
            f"cream leather seats, wooden dashboard, round amber gauges, "
            f"thin-rimmed steering wheel with chrome Mercedes horn pad, view "
            f"through windshield onto the night bridge, the warm amber dash "
            f"glow vs cool blue moonlight grading. "
            f"FIX 1: The driver's cap is FULLER and THICKER with a clearly "
            f"visible thick flat brim — NOT thin, NOT pressed flat. "
            f"FIX 2: Brown voxel hair peeks out from under the cap at the "
            f"back and slightly at the sides. "
            f"FIX 3: The ear is minimal — barely indicated, NOT prominent. "
            f"FIX 4: Kepler wears the SEATBELT — a dark diagonal shoulder "
            f"strap from his right shoulder down to his left hip, clearly "
            f"visible against his light-grey voxel torso. "
            f"{KEPLER_DESC} Cinematic, colorful, high contrast. {NEG}"
        ),
    },
    {
        "name": "04_wide_establishing_grill_sticker_fix",
        "ar": "16:9",
        "refs": [REF_V2_WIDE, REF_KEPLER_APOSE, REF_PLATE],
        "prompt": (
            f"Edit the first image. KEEP the wide establishing shot of the "
            f"red Mercedes W123 driving across the night bridge with the "
            f"line of street lamps and teal-orange grading. "
            f"FIX 1: Remove the random round sticker/badge currently on the "
            f"grille below the Mercedes star — the grille should be clean: "
            f"vertical chrome slats + the three-pointed star only. "
            f"FIX 2: Front license plate. {PLATE_DESC} "
            f"FIX 3: Driver is the cleaner Kepler voxel character — "
            f"{KEPLER_DESC} NO face features bleeding through under the "
            f"cap brim. {CAR_DESC} {NEG}"
        ),
    },
    {
        "name": "05_3q_rear_bg_blur_glass_clear",
        "ar": "16:9",
        "refs": [REF_V2_3Q_REAR, REF_KEPLER_APOSE, REF_PLATE],
        "prompt": (
            f"Edit the first image. KEEP the three-quarter rear shot of the "
            f"red Mercedes W123 on the wet city night street, sodium yellow "
            f"+ magenta/pink neon reflections, taillights glowing red. "
            f"FIX 1: Background — push it MORE OUT OF FOCUS, gentle "
            f"cinematic bokeh on the neon signs and far buildings, car "
            f"stays razor sharp. "
            f"FIX 2: The rear windshield reads CLEARER as actual glass — "
            f"slight neon reflections but transparent enough to faintly see "
            f"the driver silhouette inside. Currently too opaque/painted. "
            f"FIX 3: Rear license plate. {PLATE_DESC} "
            f"FIX 4: Driver is the Kepler voxel character — {KEPLER_DESC} "
            f"{CAR_DESC} {NEG}"
        ),
    },
    {
        "name": "06_front_magenta_cyan_mirror_fix",
        "ar": "16:9",
        "refs": [REF_V2_MAGENTA, REF_KEPLER_APOSE, REF_PLATE],
        "prompt": (
            f"Edit the first image. KEEP the low-angle front hero of the "
            f"red Mercedes W123 with the magenta + cyan Refn/Drive-style "
            f"night-club grading. "
            f"FIX 1: Side mirrors must be period-correct W123 mirrors — "
            f"thin chrome stalks with small rectangular mirror heads on the "
            f"front doors. NOT oversized modern mirrors. "
            f"FIX 2: Front license plate. {PLATE_DESC} "
            f"FIX 3: Driver is the Kepler voxel character — {KEPLER_DESC} "
            f"{CAR_DESC} High saturation, high contrast. {NEG}"
        ),
    },
]


def upload(path):
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url, name):
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


def append_record(record):
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
    print(f"MERCEDES V3b (rerun) | run {stamp} | {len(VARIANTS)} ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    refs_all = {REF_V2_INTERIOR, REF_V2_WIDE, REF_V2_3Q_REAR, REF_V2_MAGENTA,
                REF_KEPLER_APOSE, REF_PLATE}
    for r in refs_all:
        assert r.exists(), f"missing: {r}"

    print("\nUploading references...")
    url_cache = {r: upload(r) for r in refs_all}

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
                    "aspect_ratio": v["ar"],
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
                "aspect_ratio": v["ar"], "elapsed_s": round(elapsed, 1),
                "images": urls, "saved": saved, "rerun_of": "v3",
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
