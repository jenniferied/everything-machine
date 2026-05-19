#!/usr/bin/env python3
"""
Spiral Staircase — Camera Orbit Loop.
Camera orbits 360° around the staircase while character walks naturally.
Start = End frame → seamless loop after one full orbit. 10s duration.
Walking is real (legs move), but the camera rotation creates the climb feel
so the character doesn't need to "translate" in frame.
Outputs timestamped — never overwrites.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "spiral_videos"
RESULTS_FILE = SCRIPT_DIR / "spiral_videos_results.json"

INPUT_IMAGE = (
    SCRIPT_DIR / "outputs" / "spiral_upscale" / "spiral_upscale_clarity_edited.png"
)


PROMPT = (
    "The camera slowly orbits 360 degrees around the entire spiral staircase, "
    "completing exactly one full revolution by the end of the clip. The orbit is "
    "smooth, steady and continuous — no acceleration, no pauses, no direction change. "
    "Throughout the orbit, the voxel character walks naturally up the staircase, his "
    "legs lifting and stepping with each stair in a calm, even pace. He always faces "
    "the way he is walking. The softly glowing staircase, the stars, the galaxies and "
    "the clouds in the background stay physically static — only the camera moves. "
    "He wears a baseball cap with a flat brim — cap shape stays identical throughout. "
    "Cosmic blue/purple atmosphere preserved."
)

NEGATIVE = (
    "character morphing, hat changing shape, bowler hat, top hat, fedora, helmet, "
    "dome head, sphere head, face features, eyes, mouth, sunglasses, "
    "camera jerks, sudden direction change, partial rotation, no rotation, "
    "stationary camera, slipping feet, floating feet, broken stairs, "
    "duplicate characters, extra limbs, distorted limbs, flickering"
)

MODELS = [
    {
        "name": "kling3_pro_orbit",
        "endpoint": "fal-ai/kling-video/v3/pro/image-to-video",
        "image_keys": ("start_image_url", "end_image_url"),
        "args": {
            "duration": "10",
            "aspect_ratio": "16:9",
            "generate_audio": False,
            "negative_prompt": NEGATIVE,
            "cfg_scale": 0.8,
        },
        "cost_est": "$2.00",
        "runs": 2,
    },
    {
        "name": "kling_o3_orbit",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "image_keys": ("image_url", "end_image_url"),
        "args": {"duration": "10", "aspect_ratio": "16:9", "generate_audio": False},
        "cost_est": "$1.68",
        "runs": 1,
    },
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=600, follow_redirects=True)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def extract_video_url(result):
    if isinstance(result.get("video"), dict):
        return result["video"].get("url", "")
    if isinstance(result.get("video"), str):
        return result["video"]
    if isinstance(result.get("videos"), list) and result["videos"]:
        first = result["videos"][0]
        if isinstance(first, dict):
            return first.get("url", "")
        if isinstance(first, str):
            return first
    return ""


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(record):
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
    print("=" * 60)
    print(f"SPIRAL ORBIT (camera 360° + walking) | run {stamp}")
    print(f"Input: {INPUT_IMAGE.name} (start = end frame, 10s)")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(INPUT_IMAGE)

    for cfg in MODELS:
        name = cfg["name"]
        runs = cfg.get("runs", 1)
        start_key, end_key = cfg["image_keys"]
        for i in range(1, runs + 1):
            run_tag = f"{stamp}_v{i}" if runs > 1 else stamp
            print(f"\n  {name} | run {i}/{runs} | {cfg['endpoint']} | est {cfg['cost_est']}")
            args = {start_key: image_url, end_key: image_url, "prompt": PROMPT, **cfg["args"]}
            t0 = time.time()
            try:
                result = fal_client.subscribe(
                    cfg["endpoint"], arguments=args,
                    with_logs=True, on_queue_update=on_queue,
                )
                elapsed = time.time() - t0
                video_url = extract_video_url(result)
                saved = None
                if video_url:
                    p = save_video(video_url, f"{name}_{run_tag}")
                    saved = p.name
                    print(f"    OK in {elapsed:.1f}s")
                append_record({
                    "run": run_tag, "model": name, "endpoint": cfg["endpoint"],
                    "strategy": "camera 360° orbit + walking, start=end frame, 10s",
                    "prompt": PROMPT, "input": INPUT_IMAGE.name,
                    "elapsed_s": round(elapsed, 1), "cost_est": cfg["cost_est"],
                    "video_url": video_url, "saved": saved,
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception as e:
                elapsed = time.time() - t0
                print(f"    ERROR ({elapsed:.1f}s): {e}")
                append_record({
                    "run": run_tag, "model": name, "endpoint": cfg["endpoint"],
                    "error": str(e), "elapsed_s": round(elapsed, 1),
                    "cost_est": cfg["cost_est"], "timestamp": datetime.now().isoformat(),
                })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
