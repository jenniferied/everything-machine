#!/usr/bin/env python3
"""
Pool-Badehose Bild B — echtes Outpainting (Redo).

Erster Versuch (run_pool_badehose.py) hat nano-banana zum 16:9-Machen
benutzt — das hat die Szene umgerahmt statt erweitert, der Charakter
wurde winzig. Hier: echtes Outpainting mit fal-ai/bria/expand. Die
Originalpixel des hochkant-Bildes bleiben EXAKT erhalten, nur die
Streifen links/rechts werden neu generiert.

  Bild B  outputs/24_nanobanana_apose_portrait/pool_floaty.png
          768x1376 (9:16), Ausgangsbild des "Das beste!"-Kling-V3-Videos
  Schritt 1  bria/expand: original mittig auf 2446x1376-Leinwand,
             Seiten werden generiert -> B2_16x9
  Schritt 2  nano-banana-pro/edit: Outfit-Edit Badehose -> B2_16x9_badehose

Models: fal-ai/bria/expand (~$0.04) + fal-ai/nano-banana-pro/edit (~$0.04)
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

EXPAND_MODEL = "fal-ai/bria/expand"
EDIT_MODEL = "fal-ai/nano-banana-pro/edit"

EXPAND_PROMPT = (
    "A turquoise swimming pool seen directly from above, with pale stone "
    "pool deck, white sun loungers, potted green plants and soft palm leaf "
    "shadows on the tiles, bright summer daylight, voxel lego block art "
    "style, smooth and seamless continuation of the existing scene."
)
EXPAND_NEG = "people, characters, text, watermark, dark areas, seams, blur"

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
    print(f"POOL-BADEHOSE B | echtes Outpainting | run {stamp} | ~$0.08")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_B.exists(), f"missing: {IMG_B}"

    w, h = Image.open(IMG_B).size               # 768 x 1376
    canvas_w = round(h * 16 / 9)                # -> 2446
    loc_x = (canvas_w - w) // 2                 # original mittig
    print(f"  Original {w}x{h} -> Canvas {canvas_w}x{h}, original @ ({loc_x},0)")

    # --- Schritt 1: bria/expand ---
    print(f"\n--- B2_16x9 (bria/expand, Originalpixel bleiben exakt) ---")
    url_b = upload(IMG_B)
    t0 = time.time()
    b_wide = None
    try:
        result = fal_client.subscribe(
            EXPAND_MODEL,
            arguments={
                "image_url": url_b,
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
        if url:
            b_wide = save_image(url, f"B2_16x9_{stamp}")
        append_record({
            "run": stamp, "step": "B2_16x9 bria/expand", "model": EXPAND_MODEL,
            "canvas_size": [canvas_w, h], "original_image_location": [loc_x, 0],
            "prompt": EXPAND_PROMPT, "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.04", "image": url,
            "saved": b_wide.name if b_wide else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {b_wide.name if b_wide else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "B2_16x9 bria/expand", "model": EXPAND_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    if not b_wide:
        print("\n  bria/expand fehlgeschlagen — Badehose-Schritt uebersprungen.")
        return

    # --- Schritt 2: Outfit-Edit Badehose ---
    print(f"\n--- B2_16x9_badehose (nano-banana-pro/edit) ---")
    url_b_wide = upload(b_wide)
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            EDIT_MODEL,
            arguments={
                "image_urls": [url_b_wide],
                "prompt": BADEHOSE_PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [im["url"] for im in result.get("images", [])]
        saved = save_image(urls[0], f"B2_16x9_badehose_{stamp}") if urls else None
        append_record({
            "run": stamp, "step": "B2_16x9_badehose", "model": EDIT_MODEL,
            "prompt": BADEHOSE_PROMPT, "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "images": urls, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "B2_16x9_badehose", "model": EDIT_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
