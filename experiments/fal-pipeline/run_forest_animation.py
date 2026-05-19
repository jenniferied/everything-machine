#!/usr/bin/env python3
"""
Animate the Seedream-generated anime forest with Seedance 2.0 Fast.
Input: outputs/anime_forest/seedream_v4.png (16:9 anime forest plate).
Duration: 8s. Estimated: ~$1.94.
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
INPUT_IMAGE = SCRIPT_DIR / "outputs" / "anime_forest" / "seedream_v4.png"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "forest_animation"
RESULTS_FILE = SCRIPT_DIR / "forest_animation_results.json"

PROMPT = (
    "Glowing magical particles drift slowly through the air. Soft mist flows "
    "gently between the ancient trees. Sunbeams shift subtly through the canopy, "
    "dappled light playing across the moss-covered forest floor. Leaves and ferns "
    "sway in a soft breeze. The camera is completely static and does not move. "
    "Fixed camera, locked-off shot, no camera motion. Atmospheric anime scene, "
    "painterly, serene."
)

MODEL = {
    "name": "seedance_v2_fast_forest_static",
    "endpoint": "bytedance/seedance-2.0/fast/image-to-video",
    "image_key": "image_url",
    "duration_s": 7,
    "cost_est": "$1.69",
    "args": {
        "duration": "7",
        "resolution": "720p",
        "aspect_ratio": "auto",
        "generate_audio": False,
        "camera_fixed": True,
    },
}


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=180)
    out_path.write_bytes(resp.content)
    print(f"  Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def main():
    print("=" * 60)
    print("FOREST ANIMATION — Seedream forest → Seedance 2.0 Fast (8s)")
    print(f"Input: {INPUT_IMAGE.name}")
    print(f"Cost est: {MODEL['cost_est']}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    if not INPUT_IMAGE.exists():
        print(f"ERROR: Input image not found: {INPUT_IMAGE}")
        return

    print(f"\nUploading {INPUT_IMAGE.name}...")
    image_url = fal_client.upload_file(str(INPUT_IMAGE))
    print(f"-> {image_url}")

    print(f"\nRunning {MODEL['name']} | {MODEL['endpoint']}")
    args = {"prompt": PROMPT}
    args.update(MODEL["args"])
    args[MODEL["image_key"]] = image_url

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL["endpoint"],
            arguments=args,
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0

        video_url = ""
        if isinstance(result.get("video"), dict):
            video_url = result["video"].get("url", "")
        if not video_url:
            video_url = result.get("video_url", "")

        if video_url:
            save_video(video_url, MODEL["name"])
            record = {
                "test": MODEL["name"],
                "model": MODEL["endpoint"],
                "source_image": str(INPUT_IMAGE.relative_to(SCRIPT_DIR)),
                "duration_s": MODEL["duration_s"],
                "prompt": PROMPT,
                "elapsed_s": round(elapsed, 1),
                "cost_est": MODEL["cost_est"],
                "video": video_url,
                "timestamp": datetime.now().isoformat(),
            }
            RESULTS_FILE.write_text(json.dumps(record, indent=2, ensure_ascii=False))
            print(f"\nOK in {elapsed:.1f}s")
        else:
            print(f"\nWARNING: No video URL. Keys: {list(result.keys())}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"\nERROR ({elapsed:.1f}s): {e}")


if __name__ == "__main__":
    main()
