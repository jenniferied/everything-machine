#!/usr/bin/env python3
"""
Behind-Chase Plate — Schritt 1 von 2.

Nimmt das gefallene Bild
  outputs/sie_schreibt_driving/05_behind_chase_20260519_221446.png
(Cadillac-Cabrio faehrt bei Vollmond die Wuestenstrasse hinunter, Heckansicht)
und montiert das exakte Kennzeichen 'KEP - LE 18' ans Heck.

Plate-Referenz: inputs/sie-schreibt/kennzeichen-kep-le-18.png
Model: fal-ai/nano-banana-pro/edit  (~$0.04)

Ergebnis ist der Input fuer run_behind_chase_video.py (Schritt 2).
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "behind_chase_plate"
RESULTS_FILE = SCRIPT_DIR / "behind_chase_plate_results.json"

REF_IMAGE = (
    SCRIPT_DIR / "outputs" / "sie_schreibt_driving"
    / "05_behind_chase_20260519_221446.png"
)
REF_PLATE = SCRIPT_DIR / "inputs" / "sie-schreibt" / "kennzeichen-kep-le-18.png"

PLATE_DESC = (
    "The rear license plate must match the dedicated license-plate reference "
    "image (second image) EXACTLY: a German plate — blue EU strip with a 'D' "
    "on the left, then bold black text 'KEP', a brown/orange round TUV "
    "sticker, a round grey registration seal, then 'LE 18'. Reproduce that "
    "plate design and text faithfully. "
    "IMPORTANT — plate shape: the plate is a WIDE, long, narrow horizontal "
    "rectangle. German plates have a width-to-height ratio of roughly 4.7 to "
    "1 (520mm wide x 110mm tall). Render it clearly WIDE and short — NOT "
    "compressed, NOT squished, NOT square, NOT cropped. The text and stickers "
    "are spread out comfortably across the full width of the wide plate, "
    "exactly proportioned like the reference image. "
    "Keep it as sharp and legible as the viewing distance allows; the plate "
    "is mounted flat on the rear of the car, correctly perspective-matched "
    "to the car's tail and slightly catching the warm tail-light glow."
)

PROMPT = (
    "Edit the first image. KEEP everything exactly as it is: the lego-block "
    "convertible Cadillac seen from directly behind, the empty two-lane "
    "desert highway, the full moon high in the starry sky, the distant "
    "mountains, the red tail-light glow and the cool moonlit color grading. "
    "Do NOT change the composition, framing, lighting or the car. "
    "Make ONLY this change: add a rear license plate to the back of the "
    "Cadillac, mounted centrally between the tail lights. " + PLATE_DESC
)

NEGATIVE_HINTS = (
    "Avoid: changing the car, changing the framing, changing the moon or "
    "sky, wrong license plate text, blank plate, distorted or floating "
    "plate, extra plates, compressed plate, squished plate, square plate, "
    "narrow plate, plate too tall."
)


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
    print(f"BEHIND-CHASE PLATE (Schritt 1/2) | run {stamp} | ~$0.04")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for ref in [REF_IMAGE, REF_PLATE]:
        assert ref.exists(), f"missing: {ref}"

    print("\nUploading references...")
    refs = [upload(REF_IMAGE), upload(REF_PLATE)]

    model = "fal-ai/nano-banana-pro/edit"
    full_prompt = f"{PROMPT} {NEGATIVE_HINTS}"
    print(f"\n--- 01_behind_chase_plate ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_urls": refs,
                "prompt": full_prompt,
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
            saved.append(str(save_image(url, f"behind_chase_plate_{stamp}{suffix}").name))
        append_record({
            "run": stamp, "model": model, "prompt": full_prompt,
            "refs": [REF_IMAGE.name, REF_PLATE.name],
            "aspect_ratio": "16:9", "elapsed_s": round(elapsed, 1),
            "images": urls, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": model, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
