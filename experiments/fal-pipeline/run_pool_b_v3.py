#!/usr/bin/env python3
"""
Pool-Badehose Bild B — finaler Versuch (Reihenfolge getauscht).

Problem der Vorversuche: nano-banana-pro/edit rahmt ein breites 2446px-Bild
beim Outfit-Edit wieder um (B2_16x9_badehose kam als umgerahmtes 1376x768
zurueck). Auf einem normal grossen Bild (~1376px) verhaelt es sich brav —
so wie bei Bild A.

Darum hier Reihenfolge getauscht:
  Schritt 1  nano-banana-pro/edit: Badehose-Edit auf dem HOCHKANT-Original
             (768x1376) -> Charakter bleibt gross, Komposition erhalten
  Schritt 2  bria/expand: echtes Outpainting auf 16:9 -> Originalpixel
             (inkl. Badehose-Char) bleiben exakt, nur Seiten generiert

Ergebnis B3_16x9_badehose: 16:9, Charakter gross, mit Badehose.

Models: fal-ai/nano-banana-pro/edit (~$0.04) + fal-ai/bria/expand (~$0.04)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_badehose"
RESULTS_FILE = SCRIPT_DIR / "pool_badehose_results.json"

IMG_B = SCRIPT_DIR / "outputs" / "24_nanobanana_apose_portrait" / "pool_floaty.png"

EDIT_MODEL = "fal-ai/nano-banana-pro/edit"
EXPAND_MODEL = "fal-ai/bria/expand"

BADEHOSE_PROMPT = (
    "Edit this voxel-style swimming pool image. KEEP EVERYTHING IDENTICAL — "
    "the swimming pool, turquoise water and ripple pattern, the gold/bronze "
    "inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops resting on the pool deck, and the camera "
    "angle, framing, lighting and colour grade. ONLY change the voxel "
    "character's outfit: he is now dressed for a day at the pool, wearing "
    "ONLY swim trunks (board shorts) on his hips. His torso, arms, legs and "
    "bare feet are all uncovered skin-tone voxel blocks in a warm light skin "
    "tone, with the same blocky cubic voxel texture as the rest of his body "
    "— no white shirt or top, no dark long trousers anymore. He wears NOTHING "
    "on his feet: bare skin-tone voxel feet, definitely NOT flip-flops, "
    "sandals or shoes on his feet. The swim trunks cover only his hips and "
    "upper thighs. Keep his head, hair/cap and his relaxed lying pose exactly "
    "the same. Maintain the voxel / lego-block art style precisely. Do NOT "
    "move, remove or restyle the flip-flops that sit on the pool deck as "
    "scenery — they stay exactly where they are."
)

EXPAND_PROMPT = (
    "A turquoise swimming pool seen directly from above, with pale stone "
    "pool deck, white sun loungers, potted green plants and soft palm leaf "
    "shadows on the tiles, bright summer daylight, voxel lego block art "
    "style, smooth and seamless continuation of the existing scene."
)
EXPAND_NEG = "people, characters, text, watermark, dark areas, seams, blur"


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=180, follow_redirects=True)
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
    print("=" * 64)
    print(f"POOL-BADEHOSE B v3 | Badehose zuerst, dann expand | {stamp} | ~$0.08")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_B.exists(), f"missing: {IMG_B}"

    # --- Schritt 1: Badehose-Edit auf dem hochkant-Original ---
    print(f"\n--- B3_portrait_badehose (nano-banana, 9:16) ---")
    url_b = upload(IMG_B)
    t0 = time.time()
    portrait_badehose = None
    try:
        result = fal_client.subscribe(
            EDIT_MODEL,
            arguments={
                "image_urls": [url_b],
                "prompt": BADEHOSE_PROMPT,
                "aspect_ratio": "9:16",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [im["url"] for im in result.get("images", [])]
        if urls:
            portrait_badehose = save_image(urls[0], f"B3_portrait_badehose_{stamp}")
        append_record({
            "run": stamp, "step": "B3_portrait_badehose", "model": EDIT_MODEL,
            "prompt": BADEHOSE_PROMPT, "aspect_ratio": "9:16",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "images": urls,
            "saved": portrait_badehose.name if portrait_badehose else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> "
              f"{portrait_badehose.name if portrait_badehose else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "B3_portrait_badehose", "model": EDIT_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    if not portrait_badehose:
        print("\n  Schritt 1 fehlgeschlagen — expand uebersprungen.")
        return

    # --- Schritt 2: bria/expand auf 16:9 ---
    w, h = Image.open(portrait_badehose).size
    canvas_w = round(h * 16 / 9)
    loc_x = (canvas_w - w) // 2
    print(f"\n--- B3_16x9_badehose (bria/expand) ---")
    print(f"  {w}x{h} -> Canvas {canvas_w}x{h}, original @ ({loc_x},0)")
    url_pb = upload(portrait_badehose)
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            EXPAND_MODEL,
            arguments={
                "image_url": url_pb,
                "canvas_size": [canvas_w, h],
                "original_image_size": [w, h],
                "original_image_location": [loc_x, 0],
                "prompt": EXPAND_PROMPT,
                "negative_prompt": EXPAND_NEG,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        img = result.get("image") or {}
        url = img.get("url", "")
        saved = save_image(url, f"B3_16x9_badehose_{stamp}") if url else None
        append_record({
            "run": stamp, "step": "B3_16x9_badehose", "model": EXPAND_MODEL,
            "canvas_size": [canvas_w, h], "original_image_location": [loc_x, 0],
            "prompt": EXPAND_PROMPT, "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.04", "image": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "B3_16x9_badehose", "model": EXPAND_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
