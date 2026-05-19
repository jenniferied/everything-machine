#!/usr/bin/env python3
"""
Spiral Staircase Video Test — short clips on 3 newest top-tier i2v models.
Input: latest spiral_softglow_16x9_*.png (16:9, soft glowing staircase).
Models: Sora 2 Pro, Kling 3.0 Pro, Seedance 1.5 Pro.
Static camera, dimensional glow, no pulse — short clips first to pick a winner.
Never overwrites: every output gets a run-timestamp.
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
    "The voxel character slowly ascends the softly glowing spiral staircase. "
    "He keeps his flat cap on — the cap stays a cap, no other headwear. "
    "The staircase glow stays constant. Camera holds still."
)

NEGATIVE = "camera movement, zoom, pan, tilt, pulsing light, flickering, color shift, face details, sunglasses, bowler hat, top hat, fedora, helmet"

MODELS = [
    {
        "name": "kling_o3",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "args": {"duration": "5", "aspect_ratio": "16:9", "negative_prompt": NEGATIVE},
        "cost_est": "$0.84",
    },
    {
        "name": "seedance10_pro",
        "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
        "args": {"duration": "5", "resolution": "1080p", "camera_fixed": True},
        "cost_est": "$0.62",
    },
    {
        "name": "veo31_fast",
        "endpoint": "fal-ai/veo3.1/fast/image-to-video",
        "args": {"duration": "8s", "aspect_ratio": "16:9", "generate_audio": False},
        "cost_est": "$0.80",
    },
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".mp4"
    out_path = OUTPUT_DIR / f"{name}{ext}"
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
    print(f"SPIRAL VIDEO TEST | run {stamp}")
    print(f"Input image: {input_img.name}")
    print(f"Models: {', '.join(m['name'] for m in MODELS)}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    for cfg in MODELS:
        name = cfg["name"]
        print(f"\n  {name} | {cfg['endpoint']} | est {cfg['cost_est']}")
        t0 = time.time()
        try:
            args = {"image_url": image_url, "prompt": PROMPT, **cfg["args"]}
            result = fal_client.subscribe(
                cfg["endpoint"],
                arguments=args,
                with_logs=True,
                on_queue_update=on_queue,
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
                "run": stamp,
                "model": name,
                "endpoint": cfg["endpoint"],
                "args": cfg["args"],
                "prompt": PROMPT,
                "input": input_img.name,
                "elapsed_s": round(elapsed, 1),
                "cost_est": cfg["cost_est"],
                "video_url": video_url,
                "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"    ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "model": name, "endpoint": cfg["endpoint"],
                "args": cfg["args"], "error": str(e),
                "elapsed_s": round(elapsed, 1), "cost_est": cfg["cost_est"],
                "timestamp": datetime.now().isoformat(),
            })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
