#!/usr/bin/env python3
"""
Pool-Badehose Bild A — v4 (weisse Maske, weiss-pinke Badehose).

Basis: A_badehose_20260522_180847.png (v1, der von Jennifer favorisierte
Hautton). Zwei gezielte Aenderungen:
  1) Kopf wird zu einer WEISSEN MASKE (Kev traegt eine Maske) — featureless
     weisses Voxel-Gesicht, kein Skin-Ton, keine Gesichtszuege.
  2) Badehose wird WEISS-PINK statt blau.

Model: fal-ai/nano-banana-pro/edit (~$0.04)
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

IMG_A_V1 = OUTPUT_DIR / "A_badehose_20260522_180847.png"
MODEL = "fal-ai/nano-banana-pro/edit"

PROMPT = (
    "Edit this voxel-style pool image. KEEP EVERYTHING IDENTICAL — the "
    "swimming pool, turquoise water and ripple pattern, the gold inflatable "
    "pool ring, the sun loungers, potted plants, palm-leaf shadows, the "
    "pair of flip-flops on the pool deck, the camera angle, framing, "
    "lighting and colour grade. Also keep the voxel character's body "
    "(torso, arms, legs, bare feet, skin tone) and his relaxed lying pose "
    "exactly the same. Make EXACTLY two changes, nothing else:\n"
    "1) The character's HEAD is now a plain WHITE mask — a smooth, "
    "featureless WHITE voxel head with NO facial features at all (no eyes, "
    "no mouth, no nose, no skin tone, no hair colour visible). It looks "
    "like he is wearing a blank white mask covering his entire head and "
    "any visible hair. Pure clean white voxel blocks, slightly lighter "
    "than the pool deck, with the same blocky cubic voxel texture.\n"
    "2) The swim trunks (board shorts) are now WHITE AND PINK — a white "
    "base with pink pattern, or pink with white, in a clean two-tone "
    "white-and-pink design (NOT blue, no other colours). Same swim trunks "
    "shape and coverage as before — only the colour changes from blue to "
    "white-and-pink.\n"
    "Maintain the voxel / lego-block art style precisely. Do NOT move or "
    "restyle the flip-flops at the poolside scenery — they stay exactly "
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
    print(f"POOL-BADEHOSE A v4 | weisse Maske + weiss-pink | {stamp} | ~$0.04")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_A_V1.exists(), f"missing: {IMG_A_V1}"

    url_a = upload(IMG_A_V1)
    print(f"\n--- A_badehose_v4 (nano-banana, 16:9) ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "image_urls": [url_a],
                "prompt": PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [im["url"] for im in result.get("images", [])]
        saved = save_image(urls[0], f"A_badehose_v4_{stamp}") if urls else None
        append_record({
            "run": stamp, "step": "A_badehose_v4 (weisse Maske, weiss-pink)",
            "model": MODEL, "prompt": PROMPT, "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "images": urls, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": "A_badehose_v4 (weisse Maske, weiss-pink)",
            "model": MODEL, "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
