#!/usr/bin/env python3
"""
Behind-Chase Video — Schritt 2 von 2.

Macht aus dem Plate-Edit (Schritt 1) ein HD-Driving-Video:
der Cadillac faehrt die Wuestenstrasse hinunter, Vollmond, Heckansicht.

Modell-Wahl: Seedance 1.0 Pro. Laut Jennifers Bewertung
(video_test_02_bewertung.csv) war Seedance fuer die night_drive-Szene das
einzige "Gut" ohne Halluzination ("Ueberraschenderweise gut"). LTX-2 und
Veo 3.1 sind dort genau am Problem gescheitert, das hier auch auftrat:
"Auto faehrt rueckwaerts". Darum: Seedance + expliziter Vorwaerts-Prompt.

Settings wie im validierten Test: image_url + camera_fixed=True.
duration "10" deckt die 8s-Vorgabe ab, resolution 1080p (>= HD).

Model: fal-ai/bytedance/seedance/v1/pro/image-to-video  (~$1.20 fuer 10s/1080p)
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
    "The lego-block convertible Cadillac drives steadily FORWARD down the "
    "empty two-lane desert highway, moving away from the camera into the "
    "moonlit distance. Forward motion only — the car never reverses, never "
    "rolls backward. The road surface and the painted dashed center lines "
    "flow past underneath the car from the far horizon toward the bottom of "
    "the frame, the natural look of a car driving ahead. The red tail lights "
    "glow steadily. The voxel character driver sits calm behind the wheel, "
    "head and cap above the seat-back, unchanged. The full moon stays still "
    "high in the starry sky. Distant mountains stay still. The camera follows "
    "smoothly from directly behind at road level and holds steady — no zoom, "
    "no pan, no tilt. Cinematic moonlit night, cool blue grading with warm "
    "tail-light amber."
)

ARGS = {
    "duration": "10",
    "resolution": "1080p",
    "camera_fixed": True,
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
    print(f"BEHIND-CHASE VIDEO (Schritt 2/2) | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    print(f"\n  seedance_pro | {ENDPOINT} | est ~$1.20")
    args = {"image_url": image_url, "prompt": PROMPT, **ARGS}
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            ENDPOINT, arguments=args, with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        video_url = extract_video_url(result)
        saved = None
        if video_url:
            saved = save_video(video_url, f"behind_chase_seedance_{stamp}").name
        append_record({
            "run": stamp, "model": "seedance_pro", "endpoint": ENDPOINT,
            "strategy": "forward drive, camera_fixed, evaluated winner for night_drive",
            "prompt": PROMPT, "args": ARGS, "input": input_img.name,
            "elapsed_s": round(elapsed, 1), "cost_est": "$1.20",
            "video_url": video_url, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": "seedance_pro", "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.20", "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
