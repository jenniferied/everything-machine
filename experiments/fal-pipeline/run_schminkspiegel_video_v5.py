#!/usr/bin/env python3
"""
Schminkspiegel-CD — Animation v5: "weniger ist mehr", sauber & ruhig.

v4-Feedback:
  - sway: Kinn spiegelt komisch (Kamera-Schwenk verzerrt die Chrom-
    Reflexion).
  - static: komische Effekte/Partikel im Hintergrund -> weg.
  - bewegt sich eh kaum -> bewusst MINIMAL halten.

Loesung: nur ein dezenter Holo-Schimmer auf der Scheibe, Gesicht/Nase/
Lippen/Kinn bleiben FEST und unveraendert, Hintergrund ruhig und stabil.
Kamera nahezu fix. Stabilitaet positiv formuliert (kein Drift erzwingen,
keine Negativ-Prompts).

Basis: outputs/schminkspiegel_dedot2/dd_flux_20260602_150012.jpg
Seedance 2.0, 8s, 4:3, 720p. Zwei sehr ruhige Varianten.
~2 Clips, parallel.
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
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_video_v5_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_dedot2"
       / "dd_flux_20260602_150012.jpg")

MAX_WORKERS = 2
_lock = threading.Lock()

ENDPOINT = "bytedance/seedance-2.0/image-to-video"

# Minimal & stabil: nur Schimmer auf der Scheibe, Gesicht/Kinn fest,
# Hintergrund ruhig. (positiv formuliert)
BASE = (
    "Very calm, minimal motion. Only a soft iridescent holographic "
    "shimmer of light glides gently across the round disc, with a faint "
    "slow rotation of its rainbow sheen. The chrome reflected face — its "
    "nose, lips and chin — stays completely solid, smooth and unchanged, "
    "perfectly stable. The dark starry galaxy background stays calm and "
    "steady. Clean and elegant. "
)
CAM = {
    "still":     "Locked static camera, no camera movement at all.",
    "softfloat": "The camera holds almost perfectly still, with only the "
                 "faintest, slowest floating drift.",
}

VARIANTS = [
    {"name": "v5_still",     "cam": "still",     "res": "720p"},
    {"name": "v5_softfloat", "cam": "softfloat", "res": "720p"},
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
    prompt = BASE + CAM[v["cam"]]
    name = f"{v['name']}_{stamp}"
    args = {"image_url": src_url, "prompt": prompt, "duration": "8",
            "resolution": v["res"], "aspect_ratio": "4:3",
            "generate_audio": False}
    with _lock:
        print(f"  START  {v['name']} | {v['res']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(ENDPOINT, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(url, name)
        append_record({
            "run": stamp, "variant": v["name"], "endpoint": ENDPOINT,
            "src": SRC.name, "prompt": prompt, "args": args,
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
    print(f"SCHMINKSPIEGEL VIDEO v5 (weniger ist mehr) | "
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
