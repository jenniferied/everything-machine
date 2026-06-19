#!/usr/bin/env python3
"""
Pool-Video Kamera-Varianten (vorbereitet, manuell zu starten).

4 Kamera-Bewegungen, alle Kling V3 i2v auf A_v6_run3, 5s:
  orbit         langsamer Orbit um den Schwimmring
  push_in       langsamer Zoom auf den Charakter
  crane_up      Crane-Up Reveal — startet tight, faehrt hoch zur Aufsicht
  drift         sanftes Side-Dolly links-nach-rechts

Optional --pro: nutzt fal-ai/kling-video/v3/pro/image-to-video statt
standard (stabilere Wassersimulation, ~doppelter Preis).

Aufruf:
  .venv/bin/python run_pool_a_camera_variants.py orbit
  .venv/bin/python run_pool_a_camera_variants.py orbit push_in
  .venv/bin/python run_pool_a_camera_variants.py crane_up --pro
  .venv/bin/python run_pool_a_camera_variants.py orbit dive_in --duration 15
  .venv/bin/python run_pool_a_camera_variants.py all       # alle 5

Preise (audio off, $0.084/s standard, ~$0.16/s pro):
  standard 5s ~$0.42 | 10s ~$0.84 | 15s ~$1.26
  pro      5s ~$0.80 | 10s ~$1.60 | 15s ~$2.40
"""

import os
import sys
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_video"
RESULTS_FILE = SCRIPT_DIR / "pool_video_results.json"

SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

ENDPOINT_STANDARD = "fal-ai/kling-video/v3/standard/image-to-video"
ENDPOINT_PRO = "fal-ai/kling-video/v3/pro/image-to-video"

# Gemeinsames Szenen-Statement
SCENE_BASE = (
    "Voxel / lego-block style swimming pool scene. The voxel character "
    "lies relaxed on the gold inflatable pool ring in the turquoise "
    "pool. He wears pink-and-white Hawaiian swim trunks and his face "
    "is a featureless plain WHITE voxel mask (no eyes, no mouth, no "
    "facial features ever appear). He keeps his dark cap and his "
    "relaxed pose throughout. Sun loungers, potted plants and palm "
    "shadows on the pool deck. Water ripples and caustic light "
    "patterns on the pool floor shimmer. Bright summer daylight."
)

NEG = (
    "face, eyes, mouth, nose, facial features appearing on the white "
    "mask, the white face becoming skin coloured, character pose "
    "changes, character moves around the pool, deformed limbs, melted "
    "voxels, photorealistic style, loss of voxel blocks, jittery "
    "scene, heavy reframing"
)

VARIANTS = {
    "orbit": {
        "label": "Slow orbit around the ring",
        "camera": (
            "The CAMERA slowly ORBITS around the inflatable ring at a "
            "constant medium-low altitude — circling smoothly so the "
            "viewing angle on the ring and the voxel character gradually "
            "shifts through 30-60 degrees over the clip. Smooth cinematic "
            "arc movement, no jitter, no zoom. The ring and character "
            "stay roughly centred in frame as the world rotates around "
            "them."
        ),
    },
    "push_in": {
        "label": "Slow push-in toward the character",
        "camera": (
            "The CAMERA slowly PUSHES IN toward the voxel character on "
            "the ring — a gentle continuous dolly-in / zoom along the "
            "current viewing axis, ending tighter on the character and "
            "the ring than it started. Smooth cinematic push, no tilt, "
            "no pan, framing tightens uniformly."
        ),
    },
    "crane_up": {
        "label": "Crane-up reveal",
        "camera": (
            "The CAMERA starts framed TIGHT on the voxel character lying "
            "on the ring, then smoothly CRANES UP and slightly tilts "
            "down, revealing more and more of the pool, the deck, the "
            "sun loungers and the surrounding scenery as it rises. A "
            "cinematic reveal — start intimate, end wide overhead. "
            "Smooth continuous vertical lift, no jitter."
        ),
    },
    "drift": {
        "label": "Slow side dolly left to right",
        "camera": (
            "The CAMERA performs a slow sideways DOLLY from LEFT to "
            "RIGHT, parallel to the pool — a gentle horizontal track "
            "across the scene at constant height. No tilt, no zoom, no "
            "rotation. The ring and character drift slowly across the "
            "frame as the camera passes them by. Very subtle, "
            "cinematic, hypnotic pace."
        ),
    },
    "dive_in": {
        "label": "Camera dives down into the pool",
        "camera": (
            "The CAMERA performs a dramatic DESCENT INTO THE POOL: it "
            "starts at the original high angle looking down at the "
            "character on the ring, then sweeps continuously DOWNWARD "
            "and FORWARD as if a drone-camera diving toward the water "
            "surface. By the END of the clip the camera is right at the "
            "water surface near the ring, almost touching it — a "
            "cinematic plunge toward the float. Smooth continuous "
            "motion, no jitter. The voxel character, ring and white "
            "face mask stay exactly the same throughout — only the "
            "camera's vantage point changes."
        ),
    },
}


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


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


def run_variant(name: str, source_url: str, endpoint: str, tier: str,
                stamp: str, duration: str):
    v = VARIANTS[name]
    full_prompt = f"{SCENE_BASE} {v['camera']}"
    print(f"\n--- {name} | {v['label']} | tier={tier} | duration={duration}s ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            endpoint,
            arguments={
                "start_image_url": source_url,
                "prompt": full_prompt,
                "negative_prompt": NEG,
                "duration": duration,
                "generate_audio": False,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = None
        if url:
            saved = save_video(
                url, f"A_v6_run3_kling_v3_{tier}_{name}_{duration}s_{stamp}"
            )
        rate = 0.16 if tier == "pro" else 0.084
        cost = f"${rate * int(duration):.2f}"
        append_record({
            "run": stamp, "variant": name, "tier": tier,
            "duration_s": int(duration),
            "endpoint": endpoint, "input": SOURCE.name,
            "prompt": full_prompt, "negative_prompt": NEG,
            "elapsed_s": round(elapsed, 1),
            "cost_est": cost,
            "video_url": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO VIDEO'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "variant": name, "tier": tier,
            "endpoint": endpoint, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


def main():
    raw = sys.argv[1:]
    use_pro = "--pro" in raw
    duration = "5"
    cleaned = []
    skip_next = False
    for i, a in enumerate(raw):
        if skip_next:
            skip_next = False
            continue
        if a == "--duration":
            if i + 1 < len(raw):
                duration = raw[i + 1]
                skip_next = True
        elif a.startswith("--duration="):
            duration = a.split("=", 1)[1]
        elif not a.startswith("--"):
            cleaned.append(a)
    args = cleaned

    if not args:
        print(__doc__)
        print(f"\nVerfuegbare Varianten: {', '.join(VARIANTS.keys())} | all")
        return

    if "all" in args:
        chosen = list(VARIANTS.keys())
    else:
        chosen = [a for a in args if a in VARIANTS]
    if not chosen:
        print(f"Keine gueltige Variante. Optionen: {', '.join(VARIANTS.keys())} | all")
        return

    endpoint = ENDPOINT_PRO if use_pro else ENDPOINT_STANDARD
    tier = "pro" if use_pro else "standard"
    rate = 0.16 if use_pro else 0.084
    price_each = rate * int(duration)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 64)
    print(f"POOL CAMERA VARIANTS | {tier} | {len(chosen)} clips a {duration}s | "
          f"~${price_each * len(chosen):.2f} | {stamp}")
    print(f"Varianten: {', '.join(chosen)}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    source_url = upload(SOURCE)

    for name in chosen:
        run_variant(name, source_url, endpoint, tier, stamp, duration)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
