#!/usr/bin/env python3
"""
Unterwasser-Stills v2 — Komposition korrigiert.

Fehler in v1: Charakter komplett unter Wasser dargestellt oder durch den
Ring durch — falsch. Korrekt: Charakter liegt OBEN auf dem Ring, Ring
zur Haelfte versenkt, Beine + Po im Wasser, Oberkoerper + Kopf + Maske
UEBER der Oberflaeche. Kamera von unten sieht: untere Ringhaelfte,
baumelnde Voxel-Beine, durch die rippelnde Wasseroberflaeche darueber
hindurch refraktiert die Silhouette des Oberkoerpers.

Modelle:
  - NanoBanana Pro × 2  (Pool-Champion laut bewertungstabelle.csv)
  - GPT-Image-1.5 × 1   (1536x1024 nativ + 16:9-Crop auf 1536x864)

KEINE Videos.
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
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_underwater"
RESULTS_FILE = SCRIPT_DIR / "pool_underwater_results.json"

SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

PROMPT = (
    "Re-render this voxel / lego-block swimming pool scene as an "
    "UNDERWATER point of view — but with the voxel character CORRECTLY "
    "POSITIONED ON TOP of the gold inflatable ring (he is NOT swimming, "
    "NOT submerged, NOT diving through the ring). Physics of the pose:\n"
    "- The gold inflatable POOL RING floats HALF-SUBMERGED — its bottom "
    "half is under the water surface, its top half is above the water.\n"
    "- The voxel character lies relaxed ACROSS THE TOP of the ring. His "
    "TORSO, ARMS, SHOULDERS, HEAD, dark CAP and white featureless face "
    "MASK are clearly ABOVE the water surface (in the air).\n"
    "- His butt rests in the hole of the ring at roughly water level. "
    "His pink-and-white HAWAIIAN swim trunks straddle the waterline — "
    "the top hem above water, the bottom hem in the water.\n"
    "- His voxel LEGS and BARE voxel FEET hang DOWN INTO the turquoise "
    "water, fully submerged, clearly visible to the underwater camera "
    "as chunky cubic voxel blocks dangling under the ring.\n"
    "\n"
    "CAMERA: placed underwater inside the pool, a few feet below and to "
    "the side of the ring, looking DIAGONALLY UP at the underside of "
    "the half-submerged ring and at the dangling submerged legs and "
    "feet. Through the rippling AIR-WATER INTERFACE above, we glimpse "
    "the SILHOUETTE of the character's upper torso, arms, head, cap and "
    "white mask refracted through the rippling surface — clearly "
    "recognisable above the surface, not under it.\n"
    "\n"
    "Underwater effects: bright GOD-RAY sunbeams piercing down through "
    "the rippling water surface from above, shimmering caustic light "
    "patterns dancing on the distant pool floor below, suspended air "
    "BUBBLES drifting slowly upward.\n"
    "\n"
    "Maintain voxel / lego-block art style precisely — chunky cubic "
    "blocks on body, ring and natural blocky look in the water. NO eyes, "
    "no nose, no mouth, no goggles, no snorkel on the white face mask. "
    "Cinematic 16:9 underwater composition, dreamy summer atmosphere."
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url: str, name: str) -> Path | None:
    if not url:
        return None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=180, follow_redirects=True)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def first_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    return ""


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


def crop_to_16x9(src: Path) -> Path:
    """Mittiger 16:9-Crop. Speichert als <name>_16x9.png."""
    im = Image.open(src)
    w, h = im.size
    target_h = round(w * 9 / 16)
    if target_h >= h:
        return src  # schon flach genug
    top = (h - target_h) // 2
    crop = im.crop((0, top, w, top + target_h))
    dst = src.with_stem(src.stem + "_16x9")
    crop.save(dst)
    print(f"  16:9-Crop {w}x{h} -> {w}x{target_h}  ({dst.name})")
    return dst


def try_model(label: str, model: str, args: dict, save_name: str, stamp: str,
              cost: str, crop_16x9: bool = False):
    print(f"\n--- {label}  ({model}) ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model, arguments=args, with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, f"{save_name}_{stamp}")
        cropped = None
        if saved and crop_16x9:
            cropped = crop_to_16x9(saved)
        append_record({
            "run": stamp, "label": label, "model": model, "args": args,
            "elapsed_s": round(elapsed, 1), "cost_est": cost,
            "image": url, "saved": saved.name if saved else None,
            "cropped_16x9": cropped.name if cropped else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": label, "model": model, "args": args,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"UNDERWATER STILLS v2 | korrigierte Komposition | {stamp} | ~$0.12")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)

    # NanoBanana Pro × 2
    nb_args = {
        "image_urls": [src_url], "prompt": PROMPT,
        "aspect_ratio": "16:9", "num_images": 1,
    }
    for tag in ("D", "E"):
        try_model(f"NanoBanana Pro run {tag}", "fal-ai/nano-banana-pro/edit",
                  nb_args, f"uw2_nanobanana_{tag}", stamp, "$0.04")

    # GPT-Image-1.5 — 1536x1024 nativ, dann 16:9-Crop
    gpt_args = {
        "image_urls": [src_url], "prompt": PROMPT,
        "quality": "medium", "image_size": "1536x1024",
    }
    try_model("GPT-Image-1.5 (1536x1024 + 16:9-Crop)",
              "fal-ai/gpt-image-1.5/edit",
              gpt_args, "uw2_gpt15", stamp, "$0.04", crop_16x9=True)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
