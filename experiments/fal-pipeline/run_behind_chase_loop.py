#!/usr/bin/env python3
"""
Behind-Chase LOOP — Variante mit Kamerafahrt + nahtlosem Loop.

Idee (von Jennifer): die Kamera faehrt erst naeher ans Auto heran und dann
wieder zurueck zum Ausgangspunkt. Start- und Endframe sind dasselbe Bild
-> der Clip loopt nahtlos. Das Auto faehrt dabei trotzdem echt VORWAERTS
(gleichmaessige Wuestenstrasse, Mittellinie scrollt) — kein Rueckwaerts-Bug
wie bei der Treadmill-Mechanik, weil der Loop ueber die Kamera entsteht,
nicht ueber ein fixiertes Auto.

Modell: Seedance 1.0 Pro — laut video_test_02_bewertung.csv der night_drive-
Sieger ("Gut", keine Halluzination). Seedance unterstuetzt end_image_url
(First-Last-Frame) und freie Dauer 2-12s -> hier 8s wie urspruenglich
gewuenscht. camera_fixed=False, weil die Kamera sich bewegen SOLL.

Model: fal-ai/bytedance/seedance/v1/pro/image-to-video  (~$1.00 fuer 8s/1080p)
Input: neuestes outputs/behind_chase_plate/behind_chase_plate_*.png
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "behind_chase_video"
RESULTS_FILE = SCRIPT_DIR / "behind_chase_video_results.json"
PLATE_DIR = SCRIPT_DIR / "outputs" / "behind_chase_plate"

ENDPOINT = "fal-ai/bytedance/seedance/v1/pro/image-to-video"

PROMPT = (
    "Seamless looping shot. The camera starts directly behind the lego-block "
    "convertible Cadillac at road level, then performs ONE smooth move: it "
    "slowly pushes IN, gliding closer toward the back of the car, then "
    "smoothly pulls BACK OUT, returning to the exact same starting distance "
    "and framing by the end. The camera begins and ends at the identical "
    "position so the clip loops perfectly. "
    "Throughout, the Cadillac drives steadily FORWARD down the empty, uniform "
    "two-lane desert highway — forward motion only, the car never reverses "
    "and never rolls backward. The painted dashed center lines flow past "
    "underneath the car toward the camera, the natural look of driving ahead. "
    "The red tail lights glow steadily. The voxel character driver sits calm "
    "behind the wheel, unchanged. The full moon stays still high in the "
    "starry sky, distant mountains stay still. Cinematic moonlit night, cool "
    "blue grading with warm tail-light amber."
)

ARGS = {
    "duration": "8",
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "camera_fixed": False,
}


def latest_plate_edit() -> Path:
    candidates = sorted(PLATE_DIR.glob("behind_chase_plate_*.png"))
    if not candidates:
        raise FileNotFoundError(
            f"Kein Plate-Edit in {PLATE_DIR} — erst run_behind_chase_plate.py laufen lassen."
        )
    return candidates[-1]


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
        return first.get("url", "") if isinstance(first, dict) else first
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
    input_img = latest_plate_edit()
    print("=" * 60)
    print(f"BEHIND-CHASE LOOP | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name} (start == end frame -> Loop)")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    print(f"\n  seedance_pro_loop | {ENDPOINT} | est ~$1.00")
    args = {
        "image_url": image_url,
        "end_image_url": image_url,
        "prompt": PROMPT,
        **ARGS,
    }
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            ENDPOINT, arguments=args, with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        video_url = extract_video_url(result)
        saved = None
        if video_url:
            saved = save_video(video_url, f"behind_chase_loop_{stamp}").name
        append_record({
            "run": stamp, "model": "seedance_pro_loop", "endpoint": ENDPOINT,
            "strategy": "camera push-in/pull-out, start=end frame loop, car drives forward",
            "prompt": PROMPT, "args": ARGS, "input": input_img.name,
            "elapsed_s": round(elapsed, 1), "cost_est": "$1.00",
            "video_url": video_url, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": "seedance_pro_loop", "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.00", "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
