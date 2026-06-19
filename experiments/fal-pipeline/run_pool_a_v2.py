#!/usr/bin/env python3
"""
Pool-Badehose Bild A — v2, weniger orange Hautfarbe.

Erste Version (A_badehose) hatte eine zu orange Hautfarbe. Hier derselbe
Outfit-Edit auf dem Original (schraege 16:9-Ansicht), aber mit explizit
neutraler, heller Hautfarbe statt warmem Orange-Ton.

Bild A  outputs/22_nanobanana_refined_landscape/pool_floaty.png  (1376x768)
Model:  fal-ai/nano-banana-pro/edit  (~$0.04)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_badehose"
RESULTS_FILE = SCRIPT_DIR / "pool_badehose_results.json"

IMG_A = SCRIPT_DIR / "outputs" / "22_nanobanana_refined_landscape" / "pool_floaty.png"
MODEL = "fal-ai/nano-banana-pro/edit"

BADEHOSE_PROMPT = (
    "Edit this voxel-style swimming pool image. KEEP EVERYTHING IDENTICAL — "
    "the swimming pool, turquoise water and ripple pattern, the gold/bronze "
    "inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops resting on the pool deck, and the camera "
    "angle, framing, lighting and colour grade. ONLY change the voxel "
    "character's outfit: he is now dressed for a day at the pool, wearing "
    "ONLY swim trunks (board shorts) on his hips. His torso, arms, legs and "
    "bare feet are all uncovered bare skin in a NATURAL, HEALTHY MEDIUM skin "
    "tone — a normal everyday human skin tone with a gentle warmth, NOT pale "
    "or washed-out, but also NOT orange and NOT a deep tan or bronze. A "
    "balanced, believable mid skin tone. Same blocky cubic "
    "voxel texture as the rest of his body — no white shirt or top, no dark "
    "long trousers anymore. He wears NOTHING on his feet: bare skin-tone "
    "voxel feet, definitely NOT flip-flops, sandals or shoes on his feet. "
    "The swim trunks cover only his hips and upper thighs. Keep his head, "
    "hair/cap and his relaxed lying pose exactly the same. Maintain the "
    "voxel / lego-block art style precisely. Do NOT move, remove or restyle "
    "the flip-flops that sit on the pool deck as scenery — they stay exactly "
    "where they are."
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
    print(f"POOL-BADEHOSE A v3 | mittlerer Hautton | {stamp} | ~$0.04")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_A.exists(), f"missing: {IMG_A}"

    url_a = upload(IMG_A)
    print(f"\n--- A_badehose_v3 (nano-banana, 16:9) ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "image_urls": [url_a],
                "prompt": BADEHOSE_PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [im["url"] for im in result.get("images", [])]
        saved = save_image(urls[0], f"A_badehose_v3_{stamp}") if urls else None
        append_record({
            "run": stamp, "step": "A_badehose_v3 (mittlerer Hautton)",
            "model": MODEL, "prompt": BADEHOSE_PROMPT, "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "images": urls, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "A_badehose_v3 (mittlerer Hautton)",
            "model": MODEL, "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
