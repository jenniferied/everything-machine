#!/usr/bin/env python3
"""
Schminkspiegel-CD — Animation: CD dreht sich, Haare leicht in Bewegung.

Input: outputs/schminkspiegel_extend/ext_4x3_run2_20260602_140520.png
       (2048x1536, Landscape 4:3, Berry-Schema)

Bewegung: die Holo-CD in der unteren Schale dreht sich gleichmaessig,
ihre Regenbogen-Reflexe wandern; die langen Haare wehen ganz leicht.
Alles andere bleibt still, Kamera fix. 8 Sekunden, kein Audio.

Drei Modelle, die exakt 8s koennen (parallel):
  Veo 3.1 fast   duration "8s"   image_url
  Veo 3          duration "8s"   image_url
  Pixverse v5.5  duration 8      image_url

~3 Clips, ~$2.4.
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
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_video_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_extend"
       / "ext_4x3_run2_20260602_140520.png")

MAX_WORKERS = 3
_lock = threading.Lock()

MOTION = (
    "The iridescent holographic CD resting in the lower pan of the "
    "compact spins steadily and smoothly around its centre, its rainbow "
    "light reflections shimmering and shifting as it rotates. Her long "
    "flowing hair sways and drifts very gently, a soft subtle movement. "
    "Everything else stays completely still and holds its position — the "
    "chrome hand, the open compact and the chrome reflected face with "
    "berry lips remain stable. Locked static camera, no camera movement, "
    "no zoom."
)

MODELS = [
    {
        "name": "veo31_fast",
        "endpoint": "fal-ai/veo3.1/fast/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": "8s", "resolution": "720p",
                  "generate_audio": False},
        "cost": "$0.80",
    },
    {
        "name": "veo3",
        "endpoint": "fal-ai/veo3/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": "8s", "generate_audio": False},
        "cost": "$1.60",
    },
    {
        "name": "pixverse_v55",
        "endpoint": "fal-ai/pixverse/v5.5/image-to-video",
        "image_key": "image_url",
        "extra": {"duration": 8, "generate_audio_switch": False,
                  "thinking_type": "disabled"},
        "cost": "$0.30",
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
    name = f"vid_{m['name']}_8s_{stamp}"
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
    print(f"SCHMINKSPIEGEL VIDEO (8s) | {len(MODELS)} Modelle PARALLEL | "
          f"{stamp} | ~$2.4")
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
