#!/usr/bin/env python3
"""
Pool Unterwasser — dieselbe Szene aus Unterwasser-Perspektive.

Schritt 1: aus A_v6_run3 eine Unterwasser-POV-Variante machen
           (nano-banana-pro/edit) — Blick von unten nach oben gegen die
           Wasseroberflaeche, Ring als Silhouette, Charakter-Beine im
           Wasser, Sonnenstrahlen, Bubbles. Voxel-Stil bleibt, Maske
           bleibt, Hawaii-Trunks bleiben.
Schritt 2: 5s Kling V3 standard i2v aus dem Unterwasser-Still.
           Statische Kamera (oder leichte Drift), Wasser-Effekte
           dominieren.

Kosten: ~$0.04 (Still) + ~$0.42 (Video) = ~$0.46
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
STILL_DIR = SCRIPT_DIR / "outputs" / "pool_underwater"
VIDEO_DIR = SCRIPT_DIR / "outputs" / "pool_video"
STILL_RESULTS = SCRIPT_DIR / "pool_underwater_results.json"
VIDEO_RESULTS = SCRIPT_DIR / "pool_video_results.json"

SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

EDIT_MODEL = "fal-ai/nano-banana-pro/edit"
VIDEO_MODEL = "fal-ai/kling-video/v3/standard/image-to-video"

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

VIDEO_PROMPT = (
    "Underwater pool scene, voxel / lego-block art style. The camera "
    "stays still beneath the water surface, looking up at the gold "
    "inflatable ring pressing into the rippling surface above and the "
    "voxel character's submerged legs and bare feet hanging into the "
    "turquoise water. The water surface above ripples and shimmers, "
    "bright sunbeams / god-rays continuously dance and shift as they "
    "pierce through the surface, caustic light patterns flicker softly "
    "on the pool floor below, suspended air bubbles drift slowly upward "
    "through the water. The character's legs sway just barely with the "
    "water. His white featureless voxel face mask never gains any "
    "facial features. Voxel blocks stay sharp throughout. Bright "
    "summer pool atmosphere."
)

VIDEO_NEG = (
    "face, eyes, mouth, nose, facial features appearing on the white "
    "mask, character moves out of frame, character swims, character "
    "pose changes, camera pan, camera tilt, camera zoom, camera dolly, "
    "scene reframing, photorealistic style, loss of voxel blocks, "
    "blurry voxels"
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_file(url: str, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    resp = httpx.get(url, timeout=300, follow_redirects=True)
    dst.write_bytes(resp.content)
    print(f"    Saved: {dst.name} ({len(resp.content) // 1024}KB)")
    return dst


def extract_video_url(result):
    if isinstance(result.get("video"), dict):
        return result["video"].get("url", "")
    if isinstance(result.get("video"), str):
        return result["video"]
    return ""


def first_image_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        return result["images"][0].get("url", "")
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    return ""


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(file: Path, record: dict):
    existing = []
    if file.exists():
        try:
            existing = json.loads(file.read_text())
        except Exception:
            existing = []
    existing.append(record)
    file.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL UNDERWATER | Still + 5s Video | {stamp} | ~$0.46")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    # --- Schritt 1: Unterwasser-Still ---
    print("\n--- Schritt 1: Unterwasser-Still (nano-banana-pro/edit) ---")
    src_url = upload(SOURCE)
    t0 = time.time()
    still_path = None
    try:
        result = fal_client.subscribe(
            EDIT_MODEL,
            arguments={
                "image_urls": [src_url], "prompt": UNDERWATER_PROMPT,
                "aspect_ratio": "16:9", "num_images": 1,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_image_url(result)
        if url:
            ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
            still_path = save_file(
                url, STILL_DIR / f"underwater_still_{stamp}{ext}"
            )
        append_record(STILL_RESULTS, {
            "run": stamp, "step": "underwater_still", "model": EDIT_MODEL,
            "prompt": UNDERWATER_PROMPT, "aspect_ratio": "16:9",
            "source": SOURCE.name, "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.04", "image": url,
            "saved": still_path.name if still_path else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> "
              f"{still_path.name if still_path else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record(STILL_RESULTS, {
            "run": stamp, "step": "underwater_still", "model": EDIT_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    if not still_path:
        print("\n  Still fehlgeschlagen — Video uebersprungen.")
        return

    # --- Schritt 2: 5s Kling V3 Video aus dem Unterwasser-Still ---
    print(f"\n--- Schritt 2: Kling V3 standard, 5s, statisch ---")
    still_url = upload(still_path)
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            VIDEO_MODEL,
            arguments={
                "start_image_url": still_url,
                "prompt": VIDEO_PROMPT,
                "negative_prompt": VIDEO_NEG,
                "duration": "5",
                "generate_audio": False,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        vurl = extract_video_url(result)
        saved = None
        if vurl:
            saved = save_file(
                vurl, VIDEO_DIR / f"underwater_kling_v3_5s_{stamp}.mp4"
            )
        append_record(VIDEO_RESULTS, {
            "run": stamp, "step": "underwater_video", "model": "kling_v3",
            "endpoint": VIDEO_MODEL, "input": still_path.name,
            "prompt": VIDEO_PROMPT, "negative_prompt": VIDEO_NEG,
            "args": {"duration": "5", "generate_audio": False},
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.42",
            "video_url": vurl, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> "
              f"{saved.name if saved else 'NO VIDEO'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record(VIDEO_RESULTS, {
            "run": stamp, "step": "underwater_video", "model": "kling_v3",
            "endpoint": VIDEO_MODEL, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })

    print("\n" + "=" * 64)
    print(f"DONE -> still: {STILL_DIR}, video: {VIDEO_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
