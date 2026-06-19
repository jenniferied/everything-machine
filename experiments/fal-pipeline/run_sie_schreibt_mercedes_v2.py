#!/usr/bin/env python3
"""
Sie-schreibt Mercedes V2 — Fixes + neue Winkel.

V1-Probleme:
- 02_landscape und 03_low_angle: Gesicht hat in die Cap-Schirm gebleedet
  (man sieht Gesichtszuege auf/unter dem Schirm). FIX: Schirm wirft Schatten,
  Gesicht ist abstrakt-leer.
- Cap soll weiter ueberstehen (Flat-Brim deutlicher).
- Kennzeichen: deutsches Kennzeichen "KEP·LE 23" mit Kepler-Thema und
  TUEV-Plakette in der oberen rechten Ecke der hinteren Kennzeichen.
- Variiertes Color Grading: cinematic, farbig, kontrastreich.

5 Varianten, Refs aus V1-Sieger + Unreal + A-pose:
  01 Front-Hero gefixt (basiert auf V1 #03)
  02 Rear-Hero (neu) — Heckansicht mit Ruecklichtern + Kennzeichen
  03 Interior cockpit (V1 #05 mit korrekter Cap)
  04 Establishing wide (V1 #02 Grading: teal-orange)
  05 Side 3/4 rear neon sodium street lights (anderes Grading)
  06 Front-Hero mit magenta/cyan night-club grading

Model: fal-ai/nano-banana-pro/edit (~$0.04 = ~$0.24 total)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes_v2"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_mercedes_v2_results.json"

V1_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes"
REF_V1_FRONT_HERO = V1_DIR / "03_low_angle_hero_mercedes_20260519_223740.png"
REF_V1_WIDE = V1_DIR / "02_landscape_16x9_same_compo_20260519_223740.png"
REF_V1_INTERIOR = V1_DIR / "05_cockpit_interior_pov_mercedes_20260519_223740.png"
REF_UNREAL_MERC = SCRIPT_DIR / "inputs" / "sie-schreibt" / "unreal-mercedes-w123-rot-bruecke.png"
REF_KEPLER_APOSE = SCRIPT_DIR / "inputs" / "kepler-a-pose-1024.png"

CAP_DESC = (
    "He wears a dark navy/black baseball cap with a clearly visible flat "
    "curved brim that protrudes forward beyond the face. The brim casts a "
    "strong shadow over the upper face. The face itself is ABSTRACT and "
    "FEATURELESS — pure light grey voxel blocks, NO eyes, NO mouth, NO nose, "
    "NO facial features whatsoever bleeding through or onto the cap. The "
    "cap is opaque and solid — nothing visible through it."
)

KEPLER_DESC = (
    "Kepler voxel character (per the A-pose reference): humanoid figure "
    "built from small cubic voxel blocks, white/light-grey blocky upper "
    "body with visible cubic texture, dark trousers, BLOCKY abstract head. "
    + CAP_DESC
)

PLATE_DESC = (
    "Vehicle license plate is a standard German plate: white background, "
    "black bold characters, blue EU strip on the left with 'D' and stars. "
    "Plate text reads exactly 'KEP·LE 23' (KEP = fictional Kepler county, "
    "LE = letters, 23 = number, with the small round official sticker "
    "between county and letters). Round TUV/inspection sticker visible in "
    "the upper-right corner of the plate (yellow/orange round badge with "
    "year markings). Sharp, legible text."
)

CAR_KEEP = (
    "The car is the red 1970s/80s Mercedes-Benz W123 sedan: deep red paint, "
    "square chrome grille with the three-pointed Mercedes star, four round "
    "headlights, boxy European sedan silhouette, chrome bumpers."
)

NEG = (
    "Avoid: face features bleeding through cap, eyes on cap, mouth on cap, "
    "transparent cap, hooded figure, hoodie, robe, realistic human driver, "
    "deformed car, melted dashboard, wrong license plate, blurry plate."
)

VARIANTS = [
    {
        "name": "01_front_hero_fixed_kep_plate",
        "ar": "16:9",
        "refs": [REF_V1_FRONT_HERO, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the low-angle hero front shot of "
            f"the red Mercedes W123 at night on the bridge — same framing, "
            f"same chrome grille, same headlights, same street-lamp bokeh. "
            f"FIX two things: "
            f"(A) The driver behind the windshield is the Kepler voxel "
            f"character. {KEPLER_DESC} The cap brim sticks out clearly and "
            f"shadows the face. NO face features bleeding into the cap. "
            f"(B) The front license plate must read EXACTLY 'KEP·LE 23'. "
            f"{PLATE_DESC} "
            f"Color grading: cinematic teal-orange, deep blue shadows + warm "
            f"amber highlights from headlights and street lamps. High "
            f"contrast, colorful but not garish. {NEG}"
        ),
    },
    {
        "name": "02_rear_hero_new_taillights_plate",
        "ar": "16:9",
        "refs": [REF_V1_FRONT_HERO, REF_UNREAL_MERC, REF_KEPLER_APOSE],
        "prompt": (
            f"Create a NEW low-angle hero shot from BEHIND the same red "
            f"Mercedes W123 at night on the same bridge. Camera close to the "
            f"asphalt, looking up at the rear of the car. Show the iconic "
            f"W123 rear: square red tail-light clusters glowing intensely, "
            f"chrome bumper, the back of the boxy sedan body, the trunk "
            f"line. Driver silhouette of the Kepler voxel character visible "
            f"through the rear windshield with cap on. {KEPLER_DESC} "
            f"The REAR license plate must read EXACTLY 'KEP·LE 23'. "
            f"{PLATE_DESC} {CAR_KEEP} "
            f"Street lamps recede into the distance on the bridge. "
            f"Color grading: warm sodium-yellow street lights + deep "
            f"blue night sky, strong red glow from taillights. High "
            f"contrast cinematic. {NEG}"
        ),
    },
    {
        "name": "03_interior_cockpit_cap_fixed",
        "ar": "16:9",
        "refs": [REF_V1_INTERIOR, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the Mercedes W123 interior exactly: "
            f"cream leather seats, wooden dashboard, round amber gauges, "
            f"thin-rimmed steering wheel with chrome Mercedes horn pad, view "
            f"through windshield onto the night bridge. "
            f"FIX the driver: replace him with a cleaner Kepler voxel "
            f"character. {KEPLER_DESC} The cap is properly placed on the "
            f"head with the brim protruding forward and casting shadow. NO "
            f"facial features. Voxel hands grip the steering wheel naturally "
            f"at 9 and 3. Color grading: warm amber dashboard glow vs cool "
            f"blue moonlight from outside, cinematic, colorful, contrast. "
            f"{NEG}"
        ),
    },
    {
        "name": "04_wide_establishing_teal_orange",
        "ar": "16:9",
        "refs": [REF_V1_WIDE, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the wide establishing shot of the "
            f"red Mercedes W123 driving across the night bridge with the "
            f"line of street lamps. FIX the driver — cleaner Kepler voxel "
            f"character, {KEPLER_DESC}. FIX the front license plate to "
            f"read EXACTLY 'KEP·LE 23'. {PLATE_DESC} "
            f"Color grading: strong cinematic teal-orange — push the shadows "
            f"deep teal/cyan, push highlights warm orange. Filmic contrast. "
            f"{NEG}"
        ),
    },
    {
        "name": "05_3q_rear_sodium_neon",
        "ar": "16:9",
        "refs": [REF_V1_FRONT_HERO, REF_UNREAL_MERC, REF_KEPLER_APOSE],
        "prompt": (
            f"Create a NEW three-quarter rear shot of the red Mercedes W123 "
            f"on a wet city night street, reflections on the asphalt. "
            f"Camera slightly behind and to the right of the car. The "
            f"taillights glow red, the chrome bumper catches light, the "
            f"rear license plate is clearly readable: 'KEP·LE 23'. "
            f"{PLATE_DESC} {CAR_KEEP} Driver visible through rear window: "
            f"Kepler voxel character. {KEPLER_DESC} "
            f"Color grading: dominant warm sodium-vapour street light "
            f"yellow-orange with magenta/pink neon shop signs reflecting in "
            f"the wet pavement. Heavy contrast, cinematic. {NEG}"
        ),
    },
    {
        "name": "06_front_hero_magenta_cyan",
        "ar": "16:9",
        "refs": [REF_V1_FRONT_HERO, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the low-angle front hero of the "
            f"red Mercedes W123 on the bridge. FIX the driver and plate as "
            f"in the other variants: {KEPLER_DESC} Plate reads EXACTLY "
            f"'KEP·LE 23'. {PLATE_DESC} "
            f"Color grading: night-club magenta + cyan — push shadows deep "
            f"cyan/teal, push neon highlights bright magenta and pink. "
            f"Highly saturated, high contrast, cinematic, like a Refn or "
            f"Drive-style night palette. {NEG}"
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
    print(f"MERCEDES V2 | run {stamp} | {len(VARIANTS)} ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    refs_all = {REF_V1_FRONT_HERO, REF_V1_WIDE, REF_V1_INTERIOR,
                REF_UNREAL_MERC, REF_KEPLER_APOSE}
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
