#!/usr/bin/env python3
"""
Spiral Staircase Endless Loop — character walks in place, staircase rotates.
Start = End frame (latest spiral_softglow_16x9_*.png) → seamlessly loopable.
Models: Kling O3 (no audio), Kling 3.0 Pro (negative prompt + cfg_scale, no audio).
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


def latest_input() -> Path:
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError(f"Missing input: {INPUT_IMAGE}")
    return INPUT_IMAGE


PROMPT = (
    "Endless-climb illusion. The voxel character marches in place — his legs lift and "
    "step rhythmically, but his body stays exactly in the same spot in the frame. "
    "The ENTIRE spiral staircase rotates as one single rigid object around its central "
    "vertical axis. EVERY part of the staircase rotates uniformly at the same speed — "
    "the bottom steps, the middle steps, AND the upper part of the spiral disappearing into "
    "the distance — ALL rotate together as one unit, like a carousel or rotating sculpture. "
    "The whole spiral scrolls downward past the character, so it looks like he's endlessly "
    "ascending. The staircase glow stays constant. Stars and galaxies drift very slowly. "
    "Camera is completely static — no zoom, no pan, no tilt. "
    "He wears a baseball cap with a flat brim — cap shape stays identical throughout."
)

NEGATIVE = (
    "character moving up, character translating, body moving in frame, "
    "only the bottom of the staircase moving, top of staircase frozen, "
    "static upper spiral, partial rotation, perspective distortion, "
    "bowler hat, top hat, fedora, helmet, dome head, sphere head, hat changing shape, "
    "face features, eyes, mouth, camera movement, zoom, pan, tilt, flickering, color shift"
)

MODELS = [
    {
        "name": "kling3_pro_loop",
        "endpoint": "fal-ai/kling-video/v3/pro/image-to-video",
        "image_keys": ("start_image_url", "end_image_url"),
        "args": {
            "duration": "10",
            "aspect_ratio": "16:9",
            "generate_audio": False,
            "negative_prompt": NEGATIVE,
            "cfg_scale": 0.9,
        },
        "cost_est": "$2.00",
        "runs": 5,
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
    print(f"SPIRAL LOOP (walk-in-place + rotating stairs) | run {stamp}")
    print(f"Input: {input_img.name} (start = end frame)")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

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
                    saved_path = save_video(video_url, f"{name}_{run_tag}")
                    saved = saved_path.name
                    print(f"    OK in {elapsed:.1f}s")
                append_record({
                    "run": run_tag, "model": name, "endpoint": cfg["endpoint"],
                    "strategy": "walk-in-place loop, start=end frame",
                    "prompt": PROMPT, "input": input_img.name,
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
