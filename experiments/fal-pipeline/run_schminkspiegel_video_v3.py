#!/usr/bin/env python3
"""
Schminkspiegel-CD — Animation v3: NEUESTE Modelle, CD-Spin-fokussiert.

v2-Feedback der Userin:
  - Kling v3: die CD dreht sich NICHT.
  - Seedance v1: cool, aber ein paar Gesichts-Punkte "sticken" und in
    der Spiegelung hinter der Dame fehlt das Universum.
  - Wunsch: die neuesten Modelle testen; Prompt minimal, nur CD nennen.

Neueste i2v-Modelle (Mitte 2026, verifiziert via fal-Schemas):
  Seedance 2.0       bytedance/seedance-2.0/image-to-video
                     -> kann exakt 8s UND aspect_ratio "4:3" (Fix fuers
                        Crop-Problem), Nachfolger des "coolen" v1
  Kling 2.5 turbo    fal-ai/kling-video/v2.5-turbo/pro/image-to-video
                     -> cfg_scale hoch (0.8) damit die CD WIRKLICH dreht
  PixVerse V6        fal-ai/pixverse/v6/image-to-video
                     -> neuer als v5.5 (das Haare halluzinierte)

Prompt minimal: nur die CD-Drehung + fixe Kamera. Kein Wort zu Haaren,
Gesicht oder Hintergrund (nicht anchoren). Kein Negativ-Prompting.

Input: outputs/schminkspiegel_extend/ext_4x3_run2_20260602_140520.png
~3 Clips, parallel, ~$3.0.
"""

import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_video"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_video_v3_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_extend"
       / "ext_4x3_run2_20260602_140520.png")

MAX_WORKERS = 3
_lock = threading.Lock()

# Minimal, nur CD-Drehung + fixe Kamera.
MOTION = (
    "The round holographic CD inside the open compact spins, rotating "
    "continuously around its centre; its rainbow reflections sweep "
    "around as it turns. Static locked camera, no camera movement."
)

MODELS = [
    {
        "name": "seedance_2_0",
        "endpoint": "bytedance/seedance-2.0/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": "8", "resolution": "1080p",
                  "aspect_ratio": "4:3", "generate_audio": False},
        "cost": "$2.4",
    },
    {
        "name": "kling_v25_turbo_pro",
        "endpoint": "fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": "10", "cfg_scale": 0.8,
                  "negative_prompt": ""},
        "cost": "$1.05",
    },
    {
        "name": "pixverse_v6",
        "endpoint": "fal-ai/pixverse/v6/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": 8, "resolution": "1080p",
                  "thinking_type": "disabled",
                  "generate_audio_switch": False},
        "cost": "$0.40",
    },
]


def extract_video_url(result):
    if isinstance(result.get("video"), dict):
        return result["video"].get("url", "")
    if isinstance(result.get("video"), str):
        return result["video"]
    if isinstance(result.get("videos"), list) and result["videos"]:
        first = result["videos"][0]
        return first.get("url", "") if isinstance(first, dict) else first
    return ""


def save_video(url: str, name: str) -> Path | None:
    if not url:
        return None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=300, follow_redirects=True)
    out_path.write_bytes(resp.content)
    return out_path


def append_record(record: dict):
    with _lock:
        existing = []
        if RESULTS_FILE.exists():
            try:
                existing = json.loads(RESULTS_FILE.read_text())
            except Exception:
                existing = []
        existing.append(record)
        RESULTS_FILE.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False))


def run_job(m, src_url, stamp):
    name = f"vid3_{m['name']}_{stamp}"
    args = {m["image_key"]: src_url, "prompt": MOTION, **m["extra"]}
    with _lock:
        print(f"  START  {m['name']} | {m['endpoint']} | {m['cost']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(m["endpoint"], arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(url, name)
        append_record({
            "run": stamp, "model": m["name"], "endpoint": m["endpoint"],
            "src": SRC.name, "prompt": MOTION, "args": m["extra"],
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
            "video_url": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   {m['name']} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO VIDEO'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "model": m["name"], "endpoint": m["endpoint"],
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {m['name']} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL VIDEO v3 (newest models) | "
          f"{len(MODELS)} Modelle PARALLEL | {stamp} | ~$3.0")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SRC.exists(), f"missing source: {SRC}"

    print(f"  Uploading {SRC.name}...")
    src_url = fal_client.upload_file(str(SRC))

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, m, src_url, stamp) for m in MODELS]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(MODELS)} ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
