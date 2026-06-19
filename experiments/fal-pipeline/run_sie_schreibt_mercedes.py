#!/usr/bin/env python3
"""
Sie-schreibt Mercedes — Kepler A-pose im roten Mercedes W123.

Komposition + Auto kommen aus dem Unreal-Screenshot
(unreal-mercedes-w123-rot-bruecke.png — portrait 9:16, Frontalblick aufs
Auto bei Nacht auf einer Bruecke, Kepler-Voxel-Char hinterm Lenkrad).

Char-Identitaet kommt aus inputs/kepler-a-pose-1024.png — saubere Voxel-
Referenz mit dem richtigen Kepler-Modell.

Model: fal-ai/nano-banana-pro/edit (~$0.04/img, 5 = ~$0.20)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_mercedes_results.json"

INPUT_DIR = SCRIPT_DIR / "inputs" / "sie-schreibt"
REF_UNREAL_MERCEDES = INPUT_DIR / "unreal-mercedes-w123-rot-bruecke.png"
REF_KEPLER_APOSE = SCRIPT_DIR / "inputs" / "kepler-a-pose-1024.png"

KEPLER_DESC = (
    "Driver is the Kepler voxel character from the second reference: small "
    "humanoid figure built from many small cubic voxel blocks, white/light "
    "grey blocky upper body with visible cubic texture, dark hair/cap on "
    "the head, dark trousers. Abstract minimal face. Same proportions and "
    "voxel resolution as in the A-pose reference."
)

CAR_DESC = (
    "The car is a red vintage Mercedes-Benz W123 sedan, EXACTLY as shown in "
    "the first reference: deep red paint, square chrome grille with the "
    "Mercedes star, four round headlights, boxy 1970s/80s European sedan "
    "silhouette, German license plate reading 'MR W123'. Preserve the car "
    "identity precisely."
)

NEG = (
    "Avoid: convertible, Cadillac, American muscle car, hooded figure, "
    "hoodie, robe, realistic human driver, deformed car, melted dashboard."
)

VARIANTS = [
    {
        "name": "01_keep_unreal_compo_clean_kepler",
        "refs": [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the composition, framing, lighting "
            f"and atmosphere as is: portrait frontal shot of the red Mercedes "
            f"W123 at night on a bridge, deep blue sky with clouds, street "
            f"lamps in the background. KEEP the red Mercedes itself unchanged. "
            f"REPLACE the driver behind the windshield with a cleaner, "
            f"sharper version of the Kepler voxel character from the second "
            f"reference. {KEPLER_DESC} He sits behind the steering wheel, "
            f"visible from chest up through the windshield, cap on his head. "
            f"Improve the rendering quality of the character — crisper voxel "
            f"edges, less mushy. {NEG}"
        ),
    },
    {
        "name": "02_landscape_16x9_same_compo",
        "refs": [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE],
        "prompt": (
            f"Re-frame this scene as a cinematic 16:9 landscape: same red "
            f"Mercedes W123 frontal hero shot at night on a bridge, but with "
            f"more horizontal context — both ends of the bridge, sky stretched "
            f"wider, street lamps on both sides. Kepler voxel character "
            f"driving. {CAR_DESC} {KEPLER_DESC} Cinematic, moody night "
            f"colour grade. {NEG}"
        ),
    },
    {
        "name": "03_low_angle_hero_mercedes",
        "refs": [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE],
        "prompt": (
            f"Create a low-angle hero shot of the same red Mercedes W123 from "
            f"the first reference: camera close to the asphalt looking up at "
            f"the front of the car on a night bridge, headlights blazing, "
            f"chrome grille dominant, the chrome Mercedes star glinting. "
            f"Driver visible through the windshield: the Kepler voxel "
            f"character. {CAR_DESC} {KEPLER_DESC} Cinematic 16:9, "
            f"underexposed sky, warm headlight bounce. {NEG}"
        ),
    },
    {
        "name": "04_side_profile_bridge",
        "refs": [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE],
        "prompt": (
            f"Create a side profile shot of the same red Mercedes W123 "
            f"driving across a night bridge — the entire boxy silhouette "
            f"visible in profile, chrome trim, square headlights, the "
            f"distinctive Mercedes W123 shape. Bridge structure and street "
            f"lamps in the background as in the first reference. Driver "
            f"silhouette visible through the side windows: Kepler voxel "
            f"character. {CAR_DESC} {KEPLER_DESC} Cinematic 16:9. {NEG}"
        ),
    },
    {
        "name": "05_cockpit_interior_pov_mercedes",
        "refs": [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE],
        "prompt": (
            f"Create an interior shot inside the same red Mercedes W123: "
            f"camera at the passenger seat looking toward the driver and "
            f"forward through the windshield. Authentic Mercedes W123 70s/80s "
            f"interior: cream-coloured leather seats and door panels (as "
            f"hinted in the first reference), simple wooden dashboard with "
            f"round analog gauges glowing amber, large thin-rimmed steering "
            f"wheel with chrome Mercedes horn pad. Through the windshield: "
            f"the night bridge ahead. Driver is the Kepler voxel character "
            f"from the second reference. {KEPLER_DESC} Cinematic 16:9. {NEG}"
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
    print(f"MERCEDES | run {stamp} | {len(VARIANTS)} ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for r in [REF_UNREAL_MERCEDES, REF_KEPLER_APOSE]:
        assert r.exists(), f"missing: {r}"

    print("\nUploading references...")
    url_cache = {
        REF_UNREAL_MERCEDES: upload(REF_UNREAL_MERCEDES),
        REF_KEPLER_APOSE: upload(REF_KEPLER_APOSE),
    }

    model = "fal-ai/nano-banana-pro/edit"
    successes = 0

    for v in VARIANTS:
        print(f"\n--- {v['name']} ---")
        refs = [url_cache[r] for r in v["refs"]]
        # variant 01 stays portrait, others go landscape 16:9
        ar = "9:16" if v["name"].startswith("01_") else "16:9"
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "image_urls": refs,
                    "prompt": v["prompt"],
                    "aspect_ratio": ar,
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
                "aspect_ratio": ar, "elapsed_s": round(elapsed, 1),
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
