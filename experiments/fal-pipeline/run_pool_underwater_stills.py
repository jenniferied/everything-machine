#!/usr/bin/env python3
"""
Unterwasser-Stills Vergleich — KEINE Videos.

Aus Jennifers bewertungstabelle.csv: fuer pool_floaty die besten Stills:
  - NanoBanana Pro: "Sehr cool!", "Super", "Transparenter Pool Float
    gefaellt sehr" (mehrfach ja-Bewertung, keine Halluzinationen)
  - GPT-Image-1.5: solide Platz 2
  - Seedream v4.5/edit hat im Mask-Vergleich Voxel-Stil sauber gehalten

5 Stills, derselbe Prompt, verschiedene Modelle/Generationen:
  1) NanoBanana Pro run A
  2) NanoBanana Pro run B
  3) NanoBanana Pro run C
  4) GPT-Image-1.5 edit
  5) Seedream v4.5 edit

Output: outputs/pool_underwater/uw_<modell>_<runtag>_<stamp>.png
Kosten: ~$0.20 (5 Edits a ~$0.04). KEINE VIDEOS.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_underwater"
RESULTS_FILE = SCRIPT_DIR / "pool_underwater_results.json"

SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

UNDERWATER_PROMPT = (
    "Re-render this SAME voxel / lego-block swimming pool scene from a "
    "completely different camera angle: an UNDERWATER point of view, "
    "camera placed BELOW the water surface inside the pool, looking "
    "diagonally UP toward the bright water surface above. From this "
    "underwater perspective we can see: the dark silhouette of the gold "
    "inflatable pool ring pressing into the rippling water surface from "
    "above, the voxel character's submerged LEGS and BARE FEET dangling "
    "down into the turquoise water (in the same pink-and-white Hawaiian "
    "swim trunks), and from below we glimpse the underside of his torso "
    "above the surface. The water is clear turquoise. Strong bright "
    "GOD-RAYS / SUNBEAMS pierce down through the rippling surface, "
    "shimmering caustics on the pool floor far below, suspended air "
    "BUBBLES rising slowly through the water. Keep the voxel / lego-"
    "block art style precisely — chunky cubic blocks everywhere, "
    "including in the water effects. Keep the character's white "
    "featureless face mask if any part of the face/cap is still visible "
    "from this angle, otherwise show his head silhouetted against the "
    "surface. Cinematic 16:9 underwater composition, dreamy summer "
    "swimming pool atmosphere."
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
    print(f"UNDERWATER STILLS VERGLEICH | 5 Stills | {stamp} | ~$0.20")
    print("KEINE Videos — nur Stills zum Review")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)

    # NanoBanana Pro × 3
    nb_args = {
        "image_urls": [src_url], "prompt": UNDERWATER_PROMPT,
        "aspect_ratio": "16:9", "num_images": 1,
    }
    for tag in ("A", "B", "C"):
        try_model(f"NanoBanana Pro run {tag}", "fal-ai/nano-banana-pro/edit",
                  nb_args, f"uw_nanobanana_{tag}", stamp, "$0.04")

    # GPT-Image-1.5 edit (1536x1024 ist die naechste 16:9-aehnliche Option)
    gpt_args = {
        "image_urls": [src_url], "prompt": UNDERWATER_PROMPT,
        "quality": "medium", "image_size": "1536x1024",
    }
    try_model("GPT-Image-1.5 edit", "fal-ai/gpt-image-1.5/edit",
              gpt_args, "uw_gpt15", stamp, "$0.04")

    # Seedream v4.5 edit
    seed_args = {"image_urls": [src_url], "prompt": UNDERWATER_PROMPT}
    try_model("Seedream v4.5 edit", "fal-ai/bytedance/seedream/v4.5/edit",
              seed_args, "uw_seedream", stamp, "$0.04")

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
