#!/usr/bin/env python3
"""
Schminkspiegel-CD — Animation v8: Start->Endframe, CD dreht WIRKLICH,
fixe Kamera, Gesicht/Lippen still, Galaxy-Reflexion.

Trick: Seedance 2.0 mit start (Basis) + end_image_url (gleiches Bild,
nur Scheibe gedreht) -> die Interpolation erzwingt eine echte CD-Drehung,
waehrend Kamera UND Gesicht fix bleiben (beide Frames haben identisches
Gesicht/Lippen).

Start: outputs/schminkspiegel_dedot2/dd_flux_20260602_150012.jpg
End:   outputs/schminkspiegel_endframe/end_rot120_* bzw. end_rot200_*

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
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_video_v8_results.json"
ENDFRAME_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_endframe"

START = (SCRIPT_DIR / "outputs" / "schminkspiegel_dedot2"
         / "dd_flux_20260602_150012.jpg")

ENDPOINT = "bytedance/seedance-2.0/image-to-video"
MAX_WORKERS = 2
_lock = threading.Lock()

PROMPT = (
    "Static locked camera, absolutely no camera movement. The chrome "
    "reflected face, its closed lips, the chrome hand and the compact "
    "all stay completely still and unchanged. The ONLY motion is the "
    "round holographic disc, which spins smoothly and continuously "
    "around its centre, its rainbow streaks rotating. The dark starry "
    "galaxy stays reflected in the mirror behind the face."
)


def find_endframe(stem_prefix: str) -> Path:
    matches = sorted(ENDFRAME_DIR.glob(f"{stem_prefix}_*.png"))
    assert matches, f"no endframe for {stem_prefix}"
    return matches[-1]


VARIANTS = [
    {"name": "v8_ef120", "end_prefix": "end_rot120"},
    {"name": "v8_ef200", "end_prefix": "end_rot200"},
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


def run_job(v, start_url, stamp):
    end_path = find_endframe(v["end_prefix"])
    end_url = fal_client.upload_file(str(end_path))
    name = f"{v['name']}_{stamp}"
    args = {"image_url": start_url, "end_image_url": end_url,
            "prompt": PROMPT, "duration": "8", "resolution": "720p",
            "aspect_ratio": "4:3", "generate_audio": False}
    with _lock:
        print(f"  START  {v['name']} | end={end_path.name}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(ENDPOINT, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(url, name)
        append_record({
            "run": stamp, "variant": v["name"], "endpoint": ENDPOINT,
            "start": START.name, "end": end_path.name, "prompt": PROMPT,
            "args": {k: v2 for k, v2 in args.items()
                     if k not in ("image_url", "end_image_url")},
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
    print(f"SCHMINKSPIEGEL VIDEO v8 (start->endframe, real CD spin) | "
          f"{len(VARIANTS)} Clips | {stamp}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert START.exists(), f"missing start: {START}"

    print(f"  Uploading start {START.name}...")
    start_url = fal_client.upload_file(str(START))

    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, v, start_url, stamp) for v in VARIANTS]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(VARIANTS)} ok -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
