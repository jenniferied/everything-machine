#!/usr/bin/env python3
"""
Schminkspiegel-CD — Animation v7: Sway + CD dreht (Hauptbewegung),
Gesicht still (kein Mund-Aufmachen), Galaxy in der Spiegelung.

v6-Feedback: Sway war gut, aber das Mund-Aufmachen weg, und die CD
dreht sich nicht mehr (die Gesichts-Bewegung hatte den Spin verdraengt).

Hier: CD-Drehung = HAUPTBEWEGUNG (Turntable-Trick, stark betont).
Gesicht bleibt STILL und fest (Lippen geschlossen, unveraendert).
Galaxy bleibt in der Spiegelung. Sanfter Kamera-Sway.

2 Seeds (CD-Spin ist launisch -> hoehere Chance auf sauberen Dreh).
Basis: outputs/schminkspiegel_dedot2/dd_flux_20260602_150012.jpg
Seedance 2.0, 8s, 4:3, 720p. Keine Negativ-Prompts. Parallel.
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
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_video_v7_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_dedot2"
       / "dd_flux_20260602_150012.jpg")

MAX_WORKERS = 2
_lock = threading.Lock()

ENDPOINT = "bytedance/seedance-2.0/image-to-video"

# CD-Spin = Hauptbewegung; Gesicht still; Galaxy-Reflexion; sanfter Sway.
PROMPT = (
    "The round holographic disc spins like a vinyl record on a "
    "turntable — clearly and continuously rotating around its centre, "
    "its radial rainbow streaks sweeping around; this spinning disc is "
    "the main motion of the shot. The chrome reflected face in the "
    "mirror stays completely still and solid, lips closed and unchanged, "
    "a smooth on-model mirror-chrome surface showing nose, lips and "
    "chin, with the dark starry GALAXY clearly reflected behind it in "
    "the mirror. The chrome hand stays steady. The camera sways gently "
    "with a slow, smooth cinematic drift."
)

VARIANTS = [
    {"name": "v7_spin_sway_a", "res": "720p", "seed": 11111},
    {"name": "v7_spin_sway_b", "res": "720p", "seed": 22222},
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


def run_job(v, src_url, stamp):
    name = f"{v['name']}_{stamp}"
    args = {"image_url": src_url, "prompt": PROMPT, "duration": "8",
            "resolution": v["res"], "aspect_ratio": "4:3",
            "generate_audio": False, "seed": v["seed"]}
    with _lock:
        print(f"  START  {v['name']} | seed {v['seed']} | {v['res']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(ENDPOINT, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(url, name)
        append_record({
            "run": stamp, "variant": v["name"], "endpoint": ENDPOINT,
            "src": SRC.name, "prompt": PROMPT, "args": args,
            "elapsed_s": round(elapsed, 1), "video_url": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   {v['name']} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO VIDEO'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "variant": v["name"], "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {v['name']} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL VIDEO v7 (spin + sway, face still) | "
          f"{len(VARIANTS)} Clips | {stamp}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SRC.exists(), f"missing source: {SRC}"

    print(f"  Uploading {SRC.name}...")
    src_url = fal_client.upload_file(str(SRC))

    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, v, src_url, stamp) for v in VARIANTS]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(VARIANTS)} ok -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
