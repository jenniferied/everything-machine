#!/usr/bin/env python3
"""
Spiral Staircase Video — endframe-lock strategy to fix cap-morph.
Uses the latest spiral_softglow_16x9_*.png as BOTH start AND end frame, so the
model must return to the original character look. No audio. No camera movement.
Models: Kling O3, Kling 3.0 Pro (with negative prompt + cfg_scale).
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
IMG_DIR = SCRIPT_DIR / "outputs" / "spiral_neon"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "spiral_videos"
RESULTS_FILE = SCRIPT_DIR / "spiral_videos_results.json"


def latest_input() -> Path:
    candidates = sorted(IMG_DIR.glob("spiral_softglow_16x9_*.png"))
    if not candidates:
        raise FileNotFoundError("No spiral_softglow_16x9_*.png in outputs/spiral_neon/")
    return candidates[-1]


PROMPT = (
    "The voxel character slowly ascends the softly glowing spiral staircase, one step at a time. "
    "He wears a baseball cap with a flat brim — the cap stays exactly the same shape throughout. "
    "The staircase glow stays constant. Camera holds completely still."
)

NEGATIVE = (
    "bowler hat, bowl-shaped hat, top hat, fedora, helmet, dome head, sphere head, "
    "round head, hat changing shape, headwear morphing, face features, eyes, mouth, "
    "camera movement, zoom, pan, tilt, pulsing light, flickering"
)

MODELS = [
    {
        "name": "kling_o3_endlock",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "image_keys": ("image_url", "end_image_url"),
        "args": {"duration": "5", "aspect_ratio": "16:9", "generate_audio": False},
        "cost_est": "$0.84",
    },
    {
        "name": "kling3_pro_endlock",
        "endpoint": "fal-ai/kling-video/v3/pro/image-to-video",
        "image_keys": ("start_image_url", "end_image_url"),
        "args": {
            "duration": "5",
            "aspect_ratio": "16:9",
            "generate_audio": False,
            "negative_prompt": NEGATIVE,
            "cfg_scale": 0.7,
        },
        "cost_est": "$1.00",
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
    resp = httpx.get(url, timeout=300, follow_redirects=True)
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
    input_img = latest_input()
    print("=" * 60)
    print(f"SPIRAL VIDEO — ENDFRAME LOCK | run {stamp}")
    print(f"Input image: {input_img.name} (used as start AND end frame)")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    for cfg in MODELS:
        name = cfg["name"]
        print(f"\n  {name} | {cfg['endpoint']} | est {cfg['cost_est']}")
        start_key, end_key = cfg["image_keys"]
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
                saved_path = save_video(video_url, f"{name}_{stamp}")
                saved = saved_path.name
                print(f"    OK in {elapsed:.1f}s")
            else:
                print(f"    WARNING: no video URL. keys={list(result.keys())}")

            append_record({
                "run": stamp, "model": name, "endpoint": cfg["endpoint"],
                "args": {k: v for k, v in args.items() if k != start_key and k != end_key},
                "endframe_lock": True, "prompt": PROMPT, "input": input_img.name,
                "elapsed_s": round(elapsed, 1), "cost_est": cfg["cost_est"],
                "video_url": video_url, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"    ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "model": name, "endpoint": cfg["endpoint"],
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "cost_est": cfg["cost_est"], "timestamp": datetime.now().isoformat(),
            })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
