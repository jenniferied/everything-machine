#!/usr/bin/env python3
"""
Behind-Chase LANDSTRASSE — 12s forward-chase clip vom Landstrasse-Startbild.

Setup wie Clip 1 (camera_fixed=True, natuerliche Vorwaertsfahrt, kein
end-pin), Tempo unveraendert. Diff zu run_behind_chase_bordeaux.py:

- Input: behind_chase_landstrasse_*.png (Bordeaux + Violett + dt. Landstrasse
  mit weisser Strichlinie, Auto auf der rechten Spur).
- Prompt: NUR positive Beschreibung. Keine Negativ-Erwaehnungen
  (Jennifer's Beobachtung: 'NOT a Lego head' hat den Effekt verstaerkt,
  weil das Modell das Wort gehoert und das NOT ignoriert hat). Der Kopf
  wird positiv beschrieben als Minecraft-style cubic voxel cluster.
  Auch keine 'gelben Linien' verneinen — das Startbild macht den Job.

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
    "A bordeaux-red lego-block convertible Cadillac drives steadily forward "
    "down an empty German country highway at night, moving away from the "
    "camera into the violet-moonlit distance. The road has two lanes "
    "separated by a single white dashed center line; the car cruises in "
    "the right lane. The asphalt and the dashed white line flow past from "
    "the far horizon toward the bottom of the frame, the natural look of "
    "driving forward at steady highway speed. The red tail lights glow "
    "calmly. The full moon stays high in the starry sky. Distant mountains "
    "stay still on the horizon. The camera follows from directly behind at "
    "road level with a locked steady framing — no zoom, no pan, no tilt. "
    "The driver behind the wheel is a small voxel character: his head is "
    "a tight cluster of small cubic voxel blocks in light grey and white, "
    "Minecraft-style pixel-art geometry, hard edges and visible cubic "
    "facets. A dark navy baseball cap with a flat curved brim sits firmly "
    "on top of his head; small brown voxel hair blocks peek out from "
    "under the cap. He sits still and steady, both blocky voxel hands on "
    "the wheel. The cap and the cubic voxel texture of his head stay "
    "exactly the same throughout the entire shot. "
    "Cinematic moonlit night, cool violet-leaning grading with warm "
    "tail-light amber. The bordeaux car body keeps its rich aged-wine "
    "burgundy color throughout."
)

ARGS = {
    "duration": "12",
    "resolution": "1080p",
    "camera_fixed": True,
}


def latest_landstrasse() -> Path:
    candidates = sorted(RECOLOR_DIR.glob("behind_chase_landstrasse_*.png"))
    if not candidates:
        raise FileNotFoundError(
            f"Kein Landstrasse-Bild in {RECOLOR_DIR} — erst run_behind_chase_road.py."
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
    input_img = latest_landstrasse()
    print("=" * 60)
    print(f"BEHIND-CHASE LANDSTRASSE | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name} | duration {ARGS['duration']}s | positive-only prompt")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    print(f"\n  seedance_pro_landstrasse | {ENDPOINT} | est ~$1.49")
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
            saved = save_video(video_url, f"behind_chase_landstrasse_{stamp}").name
        append_record({
            "run": stamp, "model": "seedance_pro_landstrasse", "endpoint": ENDPOINT,
            "strategy": "clip-1 setup + landstrasse input + positive-only prompt (no negatives)",
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
            "run": stamp, "model": "seedance_pro_landstrasse", "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.49", "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
