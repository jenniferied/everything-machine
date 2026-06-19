#!/usr/bin/env python3
"""
Pool-Badehose Bild A — v6 (Hawaii-Hose, Maske = Voxel-Recolor von Gesicht+Ohr).

Feedback aus Vorlauf:
  - nano-banana ist das einzige Modell, das den Voxel-Stil trifft
  - Hawaii-Hose in pink-weiss cooler als plain pink-weiss
  - Maske: das OHR muss auch weiss sein, und die Voxel-Struktur (cubic
    blocks) muss in der weissen Flaeche erhalten bleiben — es ist nur
    ein RECOLOR von Gesicht+Ohr, keine glatte Mask-Auflage
  - Cap bleibt DUNKEL (Original-Farbe), nicht weiss
  - Ausgangsbild: 22_nanobanana_refined_landscape/pool_floaty.png (Original)

3 Versuche mit nano-banana-pro/edit (~$0.12 total).
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
    "Edit this voxel / lego-block style swimming pool image. KEEP "
    "EVERYTHING IDENTICAL — the pool, turquoise water and ripples, the "
    "gold inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops on the pool deck, the camera angle, "
    "framing, lighting and colour grade. Keep the voxel character's "
    "relaxed lying pose unchanged.\n"
    "\n"
    "Make EXACTLY these two changes — nothing else:\n"
    "\n"
    "1) OUTFIT — HAWAIIAN BOARD SHORTS: he now wears ONLY swim trunks on "
    "his hips. The trunks are HAWAIIAN-STYLE BOARD SHORTS in PINK AND "
    "WHITE — a clearly Hawaiian / tropical floral pattern (pink hibiscus, "
    "tropical flowers, palm leaves) over a white base, or a pink base "
    "with white floral pattern. NOT plain stripes, NOT a single solid "
    "colour, NOT blue. A real Hawaiian swim-shorts vibe.\n"
    "His torso, arms, legs and bare feet are uncovered bare skin in a "
    "warm, natural, healthy light-medium skin tone (NOT pale, NOT orange), "
    "with the same blocky cubic voxel texture as the rest of his body. He "
    "wears NOTHING on his feet — bare voxel feet, NOT flip-flops or shoes.\n"
    "\n"
    "2) FACE + EAR RECOLOUR (this is JUST a colour recolour, not a smooth "
    "mask overlay): change the colour of his FACE voxels AND his visible "
    "EAR voxels to PURE WHITE. The blocky cubic voxel structure stays "
    "FULLY VISIBLE in the white area — same cubic resolution, same block "
    "edges, same lego-block texture as the rest of his head. Do NOT "
    "smooth it out, do NOT make it a glossy mask, do NOT round the "
    "blocks — it must clearly look like the same voxel cubes, just "
    "recoloured white. NO eyes, NO nose, NO mouth, NO eyebrows, NO "
    "facial features at all on the white voxel face.\n"
    "\n"
    "KEEP HIS CAP UNCHANGED — same DARK colour as in the original image, "
    "same shape, same position. The cap does NOT become white. KEEP HIS "
    "HAIR UNCHANGED around and below the cap — same colour, same shape. "
    "Only the FACE voxels and the EAR voxels change colour to white.\n"
    "\n"
    "Maintain the voxel / lego-block art style precisely. Do NOT touch "
    "the flip-flops at the poolside — they stay exactly where they are."
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


def run_one(label: str, url: str, name: str, stamp: str):
    print(f"\n--- {label} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "image_urls": [url], "prompt": PROMPT,
                "aspect_ratio": "16:9", "num_images": 1,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        items = result.get("images", [])
        url_out = items[0].get("url", "") if items else ""
        saved = save_image(url_out, f"{name}_{stamp}")
        append_record({
            "run": stamp, "step": label, "model": MODEL,
            "prompt": PROMPT, "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "image": url_out, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": label, "model": MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL-BADEHOSE A v6 | Hawaii + Recolor Face+Ear | "
          f"{stamp} | ~$0.12 (3 Versuche)")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG_A.exists(), f"missing: {IMG_A}"

    url_a = upload(IMG_A)
    for i in (1, 2, 3):
        run_one(f"A_v6_run{i}", url_a, f"A_v6_run{i}", stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
