#!/usr/bin/env python3
"""
Pool-Badehose Bild A — v5 (vom Original, Maske nur ueber dem Gesicht).

Probleme von v4: Cap war weg und die "Maske" hatte ein Gesicht. Hier vom
ORIGINAL (22_nanobanana_refined_landscape/pool_floaty.png) neu generieren,
mit:
  - Cap und Haare bleiben EXAKT wie im Original
  - NUR das Gesicht (Augen/Nase/Mund-Bereich) wird zu einer featureless
    weissen Maske ohne Gesichtszuege
  - Badehose weiss-pink (wie v4 — war ok)
  - Hautton warm/leicht braeunlich wie in v1 (war "sehr gut")

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

IMG_A = SCRIPT_DIR / "outputs" / "22_nanobanana_refined_landscape" / "pool_floaty.png"
MODEL = "fal-ai/nano-banana-pro/edit"

PROMPT = (
    "Edit this voxel-style swimming pool image. KEEP EVERYTHING IDENTICAL — "
    "the swimming pool, turquoise water and ripple pattern, the gold/bronze "
    "inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops resting on the pool deck, and the "
    "camera angle, framing, lighting and colour grade. Keep the voxel "
    "character's relaxed lying pose exactly the same.\n"
    "\n"
    "Make EXACTLY these changes, nothing else:\n"
    "\n"
    "1) OUTFIT: he now wears ONLY swim trunks (board shorts) on his hips — "
    "no white shirt or top, no dark long trousers anymore. The swim trunks "
    "are WHITE AND PINK in a clean two-tone design (NOT blue). His torso, "
    "arms, legs and feet are uncovered bare skin in a warm, natural light "
    "skin tone with a gentle healthy tan — not pale, not over-saturated "
    "orange, just a normal warm human skin tone, with the same blocky "
    "cubic voxel texture as the rest of his body. He wears NOTHING on his "
    "feet — bare voxel feet, NOT flip-flops or shoes.\n"
    "\n"
    "2) FACE-MASK: KEEP his cap and KEEP his hair EXACTLY as they are in "
    "the original image — same colour, same shape, same voxel blocks. ONLY "
    "the face area (the small region where eyes, nose and mouth normally "
    "are, framed by the cap above and any visible hair around it) becomes "
    "a FEATURELESS, BLANK WHITE voxel surface — no eyes, no nose, no "
    "mouth, no facial features at all, like a small smooth white mask is "
    "fitted over just the face. Pure clean white voxel blocks, slightly "
    "lighter than the pool deck. The mask covers ONLY the face, NOT the "
    "top of the head, NOT the hair, NOT the cap — those stay unchanged.\n"
    "\n"
    "Maintain the voxel / lego-block art style precisely. Do NOT move, "
    "remove or restyle the flip-flops that sit on the pool deck as "
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
    print(f"POOL-BADEHOSE A v5 | Maske nur Gesicht, Cap+Haar bleiben | "
          f"{stamp} | ~$0.04")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_A.exists(), f"missing: {IMG_A}"

    url_a = upload(IMG_A)
    print(f"\n--- A_badehose_v5 (nano-banana, 16:9) ---")
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
        saved = save_image(urls[0], f"A_badehose_v5_{stamp}") if urls else None
        append_record({
            "run": stamp, "step": "A_badehose_v5 (Maske nur Gesicht)",
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
            "run": stamp, "step": "A_badehose_v5 (Maske nur Gesicht)",
            "model": MODEL, "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
