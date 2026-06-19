#!/usr/bin/env python3
"""
Sie-schreibt Mercedes V3 — Fix-Pass.

V2-Probleme + Jennifer-Feedback:
- Plate-Logik: KEP LE + 18 (R = 18. Buchstabe = 'Kepler') -> "KEP·LE 18"
- V2 #01: Seitenspiegel sieht unrealistisch -> echte W123-Aussenspiegel
- V2 #02 ging gar nicht (cartoony char) -> Char streng aus A-pose, kein
  Cartoon
- V2 #03 Innen: Cap zu duenn, Ohr zu prominent, BRAUNE voxel-Haare gucken
  oben/seitlich aus der Cap raus, Kepler MIT angeschnalltem Gurt
- V2 #04: Random runder Sticker auf dem Grill -> weg. Restl. Gesichts-Bleed
  unter Cap -> weg.
- V2 #05: BG etwas blurry, Heckscheibe klar/glas-artig
- V2 #06: Seitenspiegel-Fix wie #01

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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes_v3"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_mercedes_v3_results.json"

V2_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_mercedes_v2"
REF_V2_FRONT = V2_DIR / "01_front_hero_fixed_kep_plate_20260519_224312.png"
REF_V2_INTERIOR = V2_DIR / "03_interior_cockpit_cap_fixed_20260519_224312.png"
REF_V2_WIDE = V2_DIR / "04_wide_establishing_teal_orange_20260519_224312.png"
REF_V2_3Q_REAR = V2_DIR / "05_3q_rear_sodium_neon_20260519_224312.png"
REF_V2_MAGENTA = V2_DIR / "06_front_hero_magenta_cyan_20260519_224312.png"

REF_UNREAL_MERC = SCRIPT_DIR / "inputs" / "sie-schreibt" / "unreal-mercedes-w123-rot-bruecke.png"
REF_KEPLER_APOSE = SCRIPT_DIR / "inputs" / "kepler-a-pose-1024.png"

CAP_DESC = (
    "He wears a dark navy/black baseball cap, well-structured with a clearly "
    "visible THICK flat curved brim that protrudes forward and casts a "
    "shadow over the upper face. The cap is full and solid, NOT thin or "
    "flattened. BROWN voxel hair (small brown cubic blocks, same voxel "
    "resolution as the body) is visible peeking out from under the cap — "
    "from the back of the head and slightly at the sides. The face is "
    "ABSTRACT and FEATURELESS: pure light-grey voxel blocks, NO eyes, NO "
    "mouth, NO nose. The ear is minimal — barely a hint, NOT prominent or "
    "detailed. Cap is opaque."
)

KEPLER_DESC = (
    "Kepler voxel character (strict per the A-pose reference): humanoid "
    "figure built from small cubic voxel blocks, white/light-grey blocky "
    "upper body with visible cubic texture, brown voxel hair, dark "
    "trousers, BLOCKY abstract head. " + CAP_DESC + " "
    "DO NOT render him as a cartoon character, DO NOT smooth out the voxel "
    "blocks, DO NOT add human facial detail."
)

PLATE_DESC = (
    "German license plate: white background, black bold characters, blue EU "
    "strip on the left with 'D' and EU stars. Plate text reads EXACTLY: "
    "'KEP·LE 18' (KEP = fictional Kepler county code, then the small round "
    "official seal, then LE 18). Round TUV/inspection sticker visible in "
    "the upper-right area of the rear plate (small round yellow/orange "
    "badge). Plate text is sharp and legible."
)

CAR_DESC = (
    "1976-1985 Mercedes-Benz W123 sedan in deep red: 4 round headlights, "
    "square chrome grille with the three-pointed Mercedes star centered on "
    "top, chrome bumpers, boxy European 4-door sedan silhouette. CORRECT "
    "side mirrors: thin chrome stalks with small rectangular mirror heads "
    "mounted on the front of the front doors (period-correct W123 mirrors, "
    "NOT modern oversized mirrors, NOT round mirrors)."
)

NEG = (
    "Avoid: face features bleeding through cap, eyes on cap, mouth on cap, "
    "transparent cap, cartoonish character, smooth non-voxel character, "
    "Pixar style, anime style, prominent detailed ear, oversized modern "
    "side mirrors, round side mirrors, deformed steering wheel, random "
    "sticker on grille, blank circular sticker, wrong license plate text."
)

VARIANTS = [
    {
        "name": "01_front_hero_v3_mirror_fix",
        "ar": "16:9",
        "refs": [REF_V2_FRONT, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the low-angle front hero shot of "
            f"the red Mercedes W123 at night on the bridge — same framing, "
            f"same chrome grille, same headlights, same street-lamp bokeh, "
            f"same teal-orange grading. "
            f"FIX 1: Front license plate must read EXACTLY 'KEP·LE 18' (NOT "
            f"'KEP·LE 23' as currently). {PLATE_DESC} "
            f"FIX 2: Side mirrors of the Mercedes must be period-correct "
            f"W123 mirrors — thin chrome stalks with small rectangular "
            f"mirror heads mounted on the front edges of the doors. NOT "
            f"oversized modern mirrors. "
            f"FIX 3: Driver behind the windshield is the Kepler voxel "
            f"character — {KEPLER_DESC} "
            f"{CAR_DESC} {NEG}"
        ),
    },
    {
        "name": "02_rear_hero_strict_voxel",
        "ar": "16:9",
        "refs": [REF_UNREAL_MERC, REF_KEPLER_APOSE],
        "prompt": (
            f"Create a low-angle hero shot from BEHIND the same red Mercedes "
            f"W123 sedan at night on a bridge with street lamps. Camera "
            f"close to the asphalt, looking up at the rear of the car. Show "
            f"the iconic W123 rear: large rectangular red tail-light "
            f"clusters with horizontal ribs glowing intensely red, chrome "
            f"rear bumper, the boxy trunk and rear window. Rear license "
            f"plate must read EXACTLY 'KEP·LE 18'. {PLATE_DESC} Driver "
            f"silhouette of the Kepler voxel character visible through the "
            f"rear windshield with cap. {KEPLER_DESC} {CAR_DESC} "
            f"Cinematic 16:9, deep blue night sky, warm sodium street "
            f"lamps, intense red glow from taillights, high contrast. "
            f"IMPORTANT: render the driver as a STRICT VOXEL figure (small "
            f"cubic blocks), NOT as a cartoon, NOT as Pixar, NOT smooth. "
            f"{NEG}"
        ),
    },
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
            f"FIX 1: The driver's cap must be FULLER and THICKER with a "
            f"clearly visible thick flat brim. NOT thin or pressed flat. "
            f"FIX 2: Brown voxel hair (small brown cubic blocks) peeks out "
            f"from under the cap at the back and slightly at the sides. "
            f"FIX 3: The ear is minimal — barely indicated, NOT prominent "
            f"and NOT detailed. NO photoreal ear cartilage. "
            f"FIX 4: Kepler is wearing the SEATBELT — a dark diagonal "
            f"shoulder strap crossing from his right shoulder down to his "
            f"left hip, clearly visible against his light-grey voxel torso. "
            f"{KEPLER_DESC} Cinematic, colorful, contrast. {NEG}"
        ),
    },
    {
        "name": "04_wide_establishing_grill_sticker_fix",
        "ar": "16:9",
        "refs": [REF_V2_WIDE, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the wide establishing shot of the "
            f"red Mercedes W123 driving across the night bridge with the "
            f"line of street lamps and teal-orange grading. "
            f"FIX 1: Remove the random round sticker/badge that is "
            f"currently sitting on the grille below the Mercedes star. The "
            f"grille should be clean: just the vertical chrome slats and the "
            f"large three-pointed Mercedes star on top — NO additional "
            f"circular sticker or badge. "
            f"FIX 2: Front license plate must read EXACTLY 'KEP·LE 18'. "
            f"{PLATE_DESC} "
            f"FIX 3: Driver is cleaner Kepler voxel character — "
            f"{KEPLER_DESC} NO face features bleeding through under the "
            f"cap brim. "
            f"{CAR_DESC} {NEG}"
        ),
    },
    {
        "name": "05_3q_rear_bg_blur_glass_clear",
        "ar": "16:9",
        "refs": [REF_V2_3Q_REAR, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the three-quarter rear shot of the "
            f"red Mercedes W123 on the wet city night street, sodium yellow "
            f"+ magenta/pink neon reflections, taillights glowing red, "
            f"general atmosphere. "
            f"FIX 1: Background — push it MORE OUT OF FOCUS, gentle "
            f"cinematic bokeh on the neon shop signs and far buildings, "
            f"keeping the car itself razor sharp. "
            f"FIX 2: The rear windshield (back glass) should read CLEARER "
            f"as actual glass — slight reflections of the neon, but "
            f"transparent enough that you can faintly see the driver "
            f"silhouette inside. Currently it looks too opaque/painted. "
            f"FIX 3: Rear license plate must read EXACTLY 'KEP·LE 18'. "
            f"{PLATE_DESC} "
            f"FIX 4: Driver is Kepler voxel character — {KEPLER_DESC} "
            f"{CAR_DESC} {NEG}"
        ),
    },
    {
        "name": "06_front_magenta_cyan_mirror_fix",
        "ar": "16:9",
        "refs": [REF_V2_MAGENTA, REF_KEPLER_APOSE],
        "prompt": (
            f"Edit the first image. KEEP the low-angle front hero of the "
            f"red Mercedes W123 with the magenta + cyan Refn/Drive-style "
            f"night-club grading. "
            f"FIX 1: Side mirrors must be period-correct W123 mirrors — "
            f"thin chrome stalks with small rectangular mirror heads on the "
            f"front doors. NOT oversized modern mirrors. "
            f"FIX 2: Front license plate must read EXACTLY 'KEP·LE 18'. "
            f"{PLATE_DESC} "
            f"FIX 3: Driver is Kepler voxel character — {KEPLER_DESC} "
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
    print(f"MERCEDES V3 | run {stamp} | {len(VARIANTS)} ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    refs_all = {REF_V2_FRONT, REF_V2_INTERIOR, REF_V2_WIDE, REF_V2_3Q_REAR,
                REF_V2_MAGENTA, REF_UNREAL_MERC, REF_KEPLER_APOSE}
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
