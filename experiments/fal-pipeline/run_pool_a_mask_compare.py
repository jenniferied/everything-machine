#!/usr/bin/env python3
"""
Pool-Badehose Bild A — Maskenversuch mit mehreren Edit-Modellen.

Recherche (fal.ai/models, Mai 2026): aktuell zuverlaessige Edit-Modelle
fuer "alles behalten, nur kleines Detail aendern" sind nano-banana-pro/
edit (Google Gemini), flux-pro/kontext/max (Black Forest Labs, beruehmt
fuer praezise Localized Edits), bytedance seedream v4.5/edit. nano-banana
ist nicht automatisch das zuverlaessigste — kontext gilt als besonders
gut bei "keep almost everything".

Vergleichslauf: derselbe Edit auf dem Original
outputs/22_nanobanana_refined_landscape/pool_floaty.png, vier Versuche:
  1) nano-banana-pro/edit  (run A)
  2) nano-banana-pro/edit  (run B, anderer Seed)
  3) flux-pro/kontext/max
  4) bytedance/seedream/v4.5/edit

Gesamtkosten ~$0.20.
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

PROMPT = (
    "Edit this voxel / lego-block style swimming pool image. KEEP "
    "EVERYTHING IDENTICAL — the pool, turquoise water and ripples, the "
    "gold inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops on the pool deck, the camera angle, "
    "framing, lighting and colour grade. Keep the voxel character's "
    "relaxed lying pose, his cap and his hair exactly the same.\n"
    "\n"
    "Make EXACTLY two changes, nothing else:\n"
    "\n"
    "1) OUTFIT: he now wears ONLY swim trunks (board shorts) on his hips — "
    "no white shirt, no dark long trousers. The swim trunks are WHITE AND "
    "PINK in a clean two-tone design (NOT blue). His torso, arms, legs "
    "and bare feet are uncovered bare skin in a warm, natural, healthy "
    "light-medium skin tone (NOT orange, NOT pale) with the same blocky "
    "cubic voxel texture. He wears NOTHING on his feet — bare voxel feet, "
    "NOT flip-flops or shoes.\n"
    "\n"
    "2) FACE-MASK: ONLY the small face area (where eyes, nose and mouth "
    "normally sit) becomes a FEATURELESS, BLANK, PURE WHITE voxel surface "
    "— absolutely NO eyes, NO nose, NO mouth, NO facial features of any "
    "kind, like a smooth plain white mask is glued onto only the face. "
    "KEEP his CAP unchanged (same shape, same colour, same position). "
    "KEEP his HAIR unchanged around and below the cap. The white mask "
    "covers ONLY the face, NOT the cap, NOT the hair, NOT the back of "
    "the head. Pure white blocks, slightly lighter than the pool deck.\n"
    "\n"
    "Maintain the voxel / lego-block art style precisely. Do NOT touch the "
    "flip-flops at the poolside — they stay exactly where they are."
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


def first_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    return ""


def try_model(label: str, model: str, args: dict, save_name: str, stamp: str,
              cost: str):
    print(f"\n--- {label}  ({model}) ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model, arguments=args, with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, f"{save_name}_{stamp}")
        append_record({
            "run": stamp, "label": label, "model": model, "args": args,
            "elapsed_s": round(elapsed, 1), "cost_est": cost,
            "image": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
        return saved
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": label, "model": model, "args": args,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        return None


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL-MASK VERGLEICH | 4 Modelle | {stamp} | ~$0.20")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_A.exists(), f"missing: {IMG_A}"

    url_a = upload(IMG_A)

    # 1+2) nano-banana-pro/edit zweimal (verschiedene Seeds)
    nb_args = {
        "image_urls": [url_a], "prompt": PROMPT,
        "aspect_ratio": "16:9", "num_images": 1,
    }
    try_model("nano-banana-pro/edit run A", "fal-ai/nano-banana-pro/edit",
              nb_args, "A_mask_nano_A", stamp, "$0.04")
    try_model("nano-banana-pro/edit run B", "fal-ai/nano-banana-pro/edit",
              nb_args, "A_mask_nano_B", stamp, "$0.04")

    # 3) flux-pro/kontext/max — beruehmt fuer "keep everything, change only X"
    flux_args = {
        "image_url": url_a, "prompt": PROMPT,
        "aspect_ratio": "16:9", "num_images": 1,
        "guidance_scale": 3.5, "safety_tolerance": "5",
    }
    try_model("flux-pro/kontext/max", "fal-ai/flux-pro/kontext/max",
              flux_args, "A_mask_flux_kontext_max", stamp, "$0.08")

    # 4) bytedance seedream v4.5/edit
    seed_args = {"image_urls": [url_a], "prompt": PROMPT}
    try_model("seedream v4.5/edit", "fal-ai/bytedance/seedream/v4.5/edit",
              seed_args, "A_mask_seedream", stamp, "$0.04")

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
