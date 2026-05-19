#!/usr/bin/env python3
"""
Kepler Vid2Vid — Wan 2.2 Animate Move
Driving Video: Blender Greyplate (head tilt +20 X auf Neck, horizontal geflippt).
Reference Image: spiral_upscale_clarity_edited.png (Kepler-Voxelchar auf Spiral Staircase).
Modell retargetiert Pose vom Driver-Skelett auf den Char im Bild.
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
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "kepler_vid2vid"
RESULTS_FILE = SCRIPT_DIR / "kepler_vid2vid_results.json"

GREYPLATE = (
    SCRIPT_DIR / "outputs" / "ea_greyplate" / "headtilt"
    / "headtilt_neck_worldX20_hflip.mp4"
)
STYLE_REF = (
    SCRIPT_DIR / "outputs" / "spiral_upscale" / "spiral_upscale_clarity_edited.png"
)

ENDPOINT = "fal-ai/wan/v2.2-14b/animate/move"


def upload(p: Path) -> str:
    print(f"  uploading {p.name} ({p.stat().st_size//1024}KB)…")
    url = fal_client.upload_file(str(p))
    print(f"  -> {url}")
    return url


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"    [{msg}]")


def extract_video_url(result):
    v = result.get("video")
    if isinstance(v, dict):
        return v.get("url", "")
    if isinstance(v, str):
        return v
    return ""


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"{name}.mp4"
    out.write_bytes(httpx.get(url, timeout=600, follow_redirects=True).content)
    print(f"  saved: {out.name} ({out.stat().st_size//1024}KB)")
    return out


def append_record(rec):
    items = []
    if RESULTS_FILE.exists():
        try:
            items = json.loads(RESULTS_FILE.read_text())
        except Exception:
            items = []
    items.append(rec)
    RESULTS_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False))


def main():
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert GREYPLATE.exists(), f"missing: {GREYPLATE}"
    assert STYLE_REF.exists(), f"missing: {STYLE_REF}"

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print(f"KEPLER VID2VID | wan-2.2 animate/move | {stamp}")
    print(f"  driving: {GREYPLATE.name}")
    print(f"  char ref: {STYLE_REF.name}")
    print(f"  endpoint: {ENDPOINT}")
    print("=" * 60)

    vid_url = upload(GREYPLATE)
    img_url = upload(STYLE_REF)

    args = {
        "video_url": vid_url,
        "image_url": img_url,
        "resolution": "720p",
        "video_quality": "high",
        "num_inference_steps": 30,
        "guidance_scale": 1.5,
    }

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            ENDPOINT, arguments=args, with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = None
        if url:
            p = save_video(url, f"kepler_wan_animate_move_{stamp}")
            saved = p.name
        print(f"  OK in {elapsed:.1f}s")
        append_record({
            "run": stamp, "model": "wan-2.2-animate-move", "endpoint": ENDPOINT,
            "driving": GREYPLATE.name, "image_ref": STYLE_REF.name,
            "args": {k: v for k, v in args.items() if k not in ("video_url", "image_url")},
            "elapsed_s": round(elapsed, 1), "video_url": url, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "endpoint": ENDPOINT, "error": str(e),
            "elapsed_s": round(elapsed, 1), "timestamp": datetime.now().isoformat(),
        })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
