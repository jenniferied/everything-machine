#!/usr/bin/env python3
"""
Seed-Determinismus-Test.

Frage: Reproduziert ein fester Seed dasselbe Video, wenn man nur Aufloesung
oder Seitenverhaeltnis aendert? Und ist Seedance bei identischen Parametern
ueberhaupt deterministisch?

Alle Runs nutzen dasselbe Input-Bild, denselben Prompt, denselben Seed.
Bewegungsreicher Prompt, damit Unterschiede sichtbar werden. Nur positiv
formuliert (kein Negativ-Anchoring).

Kostenrahmen: ~2,8 $ (< 5 EUR).
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
INPUT = SCRIPT_DIR / "outputs" / "seed_test" / "_test_input.png"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "seed_test"
RESULTS_FILE = SCRIPT_DIR / "seed_test_results.json"

SEED = 42
DURATION = "5"

PROMPT = (
    "The voxel Cadillac convertible races forward at high speed down the desert "
    "highway. The dashed yellow center line streaks rapidly toward the camera. "
    "Roadside desert, rocks and jagged mountains rush past on both sides. The "
    "headlights blaze, warm light flaring. The full moon glows bright in a starry "
    "sky, stars drifting slowly. Fast cinematic tracking shot, strong sense of "
    "speed, motion blur on the ground, cool blue moonlit night with warm amber "
    "headlight glow."
)

# (name, endpoint, aspect_ratio, resolution)
RUNS = [
    # Seedance 1.0 Pro — der eigentliche Determinismus-Test
    ("s1_16x9_480p",  "fal-ai/bytedance/seedance/v1/pro/image-to-video", "16:9", "480p"),
    ("s1_16x9_1080p", "fal-ai/bytedance/seedance/v1/pro/image-to-video", "16:9", "1080p"),
    ("s1_16x9_1080p_repeat", "fal-ai/bytedance/seedance/v1/pro/image-to-video", "16:9", "1080p"),
    ("s1_9x16_1080p", "fal-ai/bytedance/seedance/v1/pro/image-to-video", "9:16", "1080p"),
    # Seedance 2.0 — zweiter Modell-Datenpunkt
    ("s2_16x9_480p",  "bytedance/seedance-2.0/image-to-video", "16:9", "480p"),
    ("s2_16x9_1080p", "bytedance/seedance-2.0/image-to-video", "16:9", "1080p"),
]


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


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
    resp = httpx.get(url, timeout=600, follow_redirects=True)
    out.write_bytes(resp.content)
    print(f"    Saved: {out.name} ({len(resp.content) // 1024}KB)")
    return out


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
    print("=" * 64)
    print(f"SEED-DETERMINISMUS-TEST | run {stamp} | seed={SEED} | {DURATION}s")
    print(f"Input: {INPUT.name}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    if not INPUT.exists():
        print(f"ERROR: Input fehlt: {INPUT}")
        return

    print("  Uploading input...")
    image_url = fal_client.upload_file(str(INPUT))
    print(f"  -> {image_url}")

    for name, endpoint, aspect, res in RUNS:
        print(f"\n  {name} | {endpoint}")
        print(f"     aspect={aspect} res={res} seed={SEED}")
        args = {
            "image_url": image_url,
            "prompt": PROMPT,
            "duration": DURATION,
            "resolution": res,
            "aspect_ratio": aspect,
            "seed": SEED,
        }
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                endpoint, arguments=args,
                with_logs=True, on_queue_update=on_queue,
            )
            elapsed = time.time() - t0
            url = extract_video_url(result)
            saved = None
            if url:
                saved = save_video(url, f"{name}_{stamp}").name
                print(f"    OK in {elapsed:.1f}s")
            else:
                print(f"    WARNING: keine video-URL. keys={list(result.keys())}")
            # fal gibt manchmal den tatsaechlich verwendeten seed zurueck
            returned_seed = result.get("seed")
            append_record({
                "run": stamp, "name": name, "endpoint": endpoint,
                "aspect_ratio": aspect, "resolution": res, "seed_in": SEED,
                "seed_returned": returned_seed,
                "duration": DURATION, "elapsed_s": round(elapsed, 1),
                "output_url": url, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
            if returned_seed is not None:
                print(f"    seed_returned = {returned_seed}")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"    ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "name": name, "endpoint": endpoint,
                "aspect_ratio": aspect, "resolution": res, "seed_in": SEED,
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "timestamp": datetime.now().isoformat(),
            })

    print(f"\n{'='*64}\nDONE — Videos in {OUTPUT_DIR}\n{'='*64}")


if __name__ == "__main__":
    main()
