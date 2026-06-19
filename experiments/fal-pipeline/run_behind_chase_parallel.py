#!/usr/bin/env python3
"""
Behind-Chase PARALLEL — zwei parallele Seedance-Runs (A/B-Test).

Beide Runs nutzen dasselbe Startbild
  outputs/behind_chase_recolor/behind_chase_landstrasse_*.png
und unterscheiden sich nur im Prompt.

Run A — Fix-Prompt:
  Korrekturen aus dem letzten Drift-Debrief: 'desert road' statt 'country
  highway' (keine Leitplanke triggern), 'gradually recedes into the distance'
  statt 'follows' (Auto muss sichtbar nach hinten weg), 'gentle hint of
  violet' statt 'violet-leaning grading' (kein lila Mond-Hof), positive
  Wuesten-Schultern statt nichts.

Run B — Clip-1-Prompt (den Jennifer mochte) mit minimalen Anpassungen:
  - 'lego-block' Auto-Adjektiv ersetzt (vermeidet L-Wort-Anchoring)
  - Farben auf bordeaux + violet-getoenten Grading umgestellt
  - Kopf positiv als Minecraft-Voxel-Cluster beschrieben (statt nur
    'head and cap unchanged')
  Sonst Wort fuer Wort wie Clip 1 — Fahrgefuehl + Recede sind dort
  bewiesen funktioniert.

Parallel via fal_client.submit -> beide Jobs laufen gleichzeitig auf fal.

Model: fal-ai/bytedance/seedance/v1/pro/image-to-video  (~$1.49 × 2 = $2.98)
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

PROMPT_A_FIX = (
    "A bordeaux-red voxel-block convertible Cadillac drives steadily forward "
    "down an empty desert road at night. The car drives forward and "
    "gradually recedes into the distance, getting smaller as it moves away "
    "from the static camera position behind it. The road has two lanes "
    "separated by a single white dashed center line; the car cruises in the "
    "right lane. Sandy desert shoulders with brush and rocks stretch out on "
    "both sides. The asphalt and the dashed white line flow past from the "
    "far horizon toward the bottom of the frame, the natural look of "
    "driving forward at steady highway speed. The red tail lights glow "
    "calmly. The full moon stays high in the starry sky, the moon and "
    "night sky remain pale and naturalistic with only a gentle hint of "
    "violet in the air. Distant mountains stay still on the horizon. The "
    "camera is positioned behind the car at road level with a locked, "
    "steady framing — no zoom, no pan, no tilt. "
    "The driver behind the wheel is a small voxel character: his head is a "
    "tight cluster of small cubic voxel blocks in light grey and white, "
    "Minecraft-style pixel-art geometry, hard edges and visible cubic "
    "facets. A dark navy baseball cap with a flat curved brim sits firmly "
    "on top of his head; small brown voxel hair blocks peek out from under "
    "the cap. He sits still and steady, both blocky voxel hands on the "
    "wheel. The cap and the cubic voxel texture of his head stay exactly "
    "the same throughout the entire shot. "
    "Cinematic moonlit night. The bordeaux car body keeps its rich "
    "aged-wine burgundy color throughout."
)

PROMPT_B_CLIP1 = (
    "The bordeaux-red voxel-block convertible Cadillac drives steadily "
    "FORWARD down the empty two-lane desert highway, moving away from the "
    "camera into the moonlit distance. Forward motion only — the car never "
    "reverses, never rolls backward. The road surface and the painted "
    "dashed white center line flow past underneath the car from the far "
    "horizon toward the bottom of the frame, the natural look of a car "
    "driving ahead. The red tail lights glow steadily. The voxel character "
    "driver sits calm behind the wheel, head and cap above the seat-back, "
    "unchanged — his head is a tight cluster of small cubic voxel blocks "
    "in light grey and white, Minecraft-style pixel-art geometry with hard "
    "edges and visible cubic facets, and a dark navy baseball cap with a "
    "flat curved brim sits firmly on top. The full moon stays still high "
    "in the starry sky. Distant mountains stay still. The camera follows "
    "smoothly from directly behind at road level and holds steady — no "
    "zoom, no pan, no tilt. Cinematic moonlit night, cool violet-tinted "
    "grading with warm tail-light amber."
)

ARGS = {
    "duration": "12",
    "resolution": "1080p",
    "camera_fixed": True,
}

VARIANTS = [
    {"tag": "A_fix", "prompt": PROMPT_A_FIX,
     "note": "new corrected prompt: desert road, recedes, subtle violet, positive shoulders"},
    {"tag": "B_clip1", "prompt": PROMPT_B_CLIP1,
     "note": "clip-1 prompt with bordeaux/violet update + positive head, drop lego-block"},
]


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
    print(f"BEHIND-CHASE PARALLEL A/B | Seedance 1.0 Pro | run {stamp}")
    print(f"Input: {input_img.name} | duration {ARGS['duration']}s | est ~$2.98 total")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(input_img)

    # Submit both jobs in parallel
    handles = {}
    t_submit = time.time()
    for v in VARIANTS:
        args = {"image_url": image_url, "prompt": v["prompt"], **ARGS}
        print(f"\n  Submitting {v['tag']}... ({v['note']})")
        handles[v["tag"]] = fal_client.submit(ENDPOINT, arguments=args)
        print(f"    request_id: {handles[v['tag']].request_id}")

    print(f"\nBeide Jobs submitted in {time.time()-t_submit:.1f}s — warte auf Ergebnisse (parallel)...")

    # Collect results
    for v in VARIANTS:
        tag = v["tag"]
        print(f"\n--- {tag} ---")
        t0 = time.time()
        try:
            result = handles[tag].get()
            elapsed = time.time() - t0
            video_url = extract_video_url(result)
            saved = None
            if video_url:
                saved = save_video(video_url, f"behind_chase_{tag}_{stamp}").name
            append_record({
                "run": stamp, "model": f"seedance_pro_{tag}", "endpoint": ENDPOINT,
                "strategy": v["note"], "prompt": v["prompt"], "args": ARGS,
                "input": input_img.name, "elapsed_s": round(elapsed, 1),
                "cost_est": "$1.49", "video_url": video_url, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
            print(f"  OK in {elapsed:.1f}s -> {saved}")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "model": f"seedance_pro_{tag}", "endpoint": ENDPOINT,
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "cost_est": "$1.49", "timestamp": datetime.now().isoformat(),
            })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
