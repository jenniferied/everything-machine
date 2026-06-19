#!/usr/bin/env python3
"""
Behind-Chase BORDEAUX — 12s forward-chase clip vom recolorierten Startbild.

Setup wie Clip 1 (behind_chase_seedance_20260522_171633.mp4 — den Jennifer
mochte): camera_fixed=True, kein end-pin, Auto faehrt natuerlich nach vorne
weg in die Mond-Wueste. Fahrgeschwindigkeit unveraendert (Jennifer: "war
eigentlich ok").

Diff zu Clip 1:
- Input: bordeaux-rotes Startbild mit violettem Grading
  outputs/behind_chase_recolor/behind_chase_bordeaux_*.png
- Dauer: 12s (Seedance-Maximum)
- VERSCHAERFTER Kopf-Lock-Prompt — Kopf darf NICHT zu glattem Lego-Spielzeug-
  kopf morphen, Voxel-Wuerfel muessen erhalten bleiben.

Modell: Seedance 1.0 Pro — night_drive-Sieger laut Bewertung.
Model: fal-ai/bytedance/seedance/v1/pro/image-to-video  (~$1.49 fuer 12s/1080p)
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
RECOLOR_DIR = SCRIPT_DIR / "outputs" / "behind_chase_recolor"

ENDPOINT = "fal-ai/bytedance/seedance/v1/pro/image-to-video"

PROMPT = (
    "The bordeaux-red lego-block convertible Cadillac drives steadily "
    "FORWARD down the empty two-lane desert highway, moving away from the "
    "camera into the violet-moonlit distance. Forward motion only — the car "
    "never reverses, never rolls backward. The road surface and the painted "
    "dashed white center lines flow past underneath the car from the far "
    "horizon toward the bottom of the frame — the natural look of a car "
    "driving steadily ahead. The red tail lights glow steadily. The full "
    "moon stays still high in the starry sky. Distant mountains stay still. "
    "The camera follows smoothly from directly behind at road level and "
    "holds steady — no zoom, no pan, no tilt. "
    "CRITICAL — driver character consistency: the voxel character behind "
    "the wheel must stay 100% IDENTICAL for the entire clip. His head MUST "
    "keep its hard CUBIC VOXEL BLOCK texture — small visible cubic blocks "
    "of light grey/white. His dark baseball cap with the flat brim must "
    "stay on his head, the cap shape never changing. His brown voxel hair "
    "stays the same. The head must NEVER smooth out into a rounded "
    "Lego-toy minifigure head, NEVER become a plain cylinder or sphere, "
    "and NO face features (eyes, nose, mouth, ears) may appear or animate. "
    "He simply sits still behind the wheel — no head turning, no nodding. "
    "Cinematic moonlit night, violet-leaning cool grading with warm "
    "tail-light amber. Bordeaux car body stays bordeaux throughout."
)

ARGS = {
    "duration": "12",
    "resolution": "1080p",
    "camera_fixed": True,
}


def latest_bordeaux() -> Path:
    candidates = sorted(RECOLOR_DIR.glob("behind_chase_bordeaux_*.png"))
    if not candidates:
        raise FileNotFoundError(
            f"Kein Bordeaux-Bild in {RECOLOR_DIR} — erst run_behind_chase_recolor.py."
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
    input_img = latest_bordeaux()
    print("=" * 60)
    print(f"BEHIND-CHASE BORDEAUX | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name} | duration {ARGS['duration']}s")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    print(f"\n  seedance_pro_bordeaux | {ENDPOINT} | est ~$1.49")
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
            saved = save_video(video_url, f"behind_chase_bordeaux_{stamp}").name
        append_record({
            "run": stamp, "model": "seedance_pro_bordeaux", "endpoint": ENDPOINT,
            "strategy": "clip-1 setup (camera_fixed, forward recede) + bordeaux input + head-lock prompt",
            "prompt": PROMPT, "args": ARGS, "input": input_img.name,
            "elapsed_s": round(elapsed, 1), "cost_est": "$1.49",
            "video_url": video_url, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": "seedance_pro_bordeaux", "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.49", "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
