#!/usr/bin/env python3
"""
Behind-Chase TREADMILL — loopbarer Driving-Clip, Schritt A (Generierung).

Ansatz (mit Jennifer abgestimmt):
- KEIN start=end-Pin. Das hat vorher die Strasse eingefroren (Modell nahm
  den billigen Weg: statische Strasse + Auto schaukelt vor/zurueck).
- Stattdessen Treadmill: das Auto bleibt fix und gleich gross im Frame,
  nur die WELT (Strasse + Mittellinie) scrollt -> echtes Vorwaerts-Gefuehl.
- Der Loop wird NICHT generativ erzwungen, sondern danach per ffmpeg-
  Crossfade gebaut (run via run_behind_chase_treadmill.py -> dann blenden).
- Relativ lang generieren (10s), damit nach dem ~1s-Crossfade noch ein
  9s-Loop bleibt (Jennifers Vorgabe: fertiger Loop mind. 8s).

Kopf-Fix: expliziter Prompt, dass Kopf/Cap/Voxel-Textur konstant bleiben
und NICHT zu einem glatten Lego-Spielzeugkopf morphen.

Modell: Seedance 1.0 Pro — night_drive-Sieger in video_test_02_bewertung.csv.
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
    "Tracking chase shot. The camera is a chase camera that FOLLOWS the "
    "lego-block convertible Cadillac, traveling forward together with it and "
    "tracking it at a CONSTANT distance directly behind it at road level. "
    "Because the camera moves with the car, the CAR stays exactly the same "
    "size and in the same spot in the frame for the entire clip — it never "
    "recedes, never shrinks, never gets closer, never drifts left or right, "
    "never drives out of frame, and NEVER rolls backward. "
    "The camera holds a steady locked framing — no zoom, no pan, no tilt, no "
    "shake — it simply travels forward with the car. "
    "Because the car and camera move forward together, the WORLD streams "
    "continuously past: the empty two-lane desert highway, its painted "
    "dashed white center lines, the roadside terrain and the mid-ground "
    "hills all appear far away at the horizon, grow larger as they rush "
    "toward the camera, and sweep down and out past the bottom of the frame. "
    "This continuous forward flow is the look of driving steadily ahead at "
    "speed — smooth, even, constant, never reversing, never stopping, never "
    "freezing. "
    "The red tail lights glow steadily. "
    "The voxel character driver stays 100% constant: his head, his dark "
    "baseball cap with flat brim, his brown voxel hair and his blocky cubic "
    "voxel texture do NOT change. The head keeps its hard cubic voxel blocks "
    "— it must NOT morph, must NOT smooth into a rounded Lego-toy head, and "
    "NO face features (eyes, nose, mouth) ever appear. He simply sits still "
    "behind the wheel. "
    "The full moon and the distant background mountains stay still. "
    "Cinematic moonlit night, cool blue grading with warm tail-light amber."
)

ARGS = {
    "duration": "10",
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
    print(f"BEHIND-CHASE TREADMILL | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name} | duration {ARGS['duration']}s")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    print(f"\n  seedance_pro_treadmill | {ENDPOINT} | est ~$1.20")
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
            saved = save_video(video_url, f"behind_chase_treadmill_{stamp}").name
        append_record({
            "run": stamp, "model": "seedance_pro_treadmill", "endpoint": ENDPOINT,
            "strategy": "treadmill: car fixed in frame, road scrolls; loop built in post via crossfade",
            "prompt": PROMPT, "args": ARGS, "input": input_img.name,
            "elapsed_s": round(elapsed, 1), "cost_est": "$1.20",
            "video_url": video_url, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
        print(f"  Naechster Schritt: ffmpeg-Crossfade -> nahtloser Loop")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": "seedance_pro_treadmill", "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.20", "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
