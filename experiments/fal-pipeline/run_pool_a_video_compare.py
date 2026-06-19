#!/usr/bin/env python3
"""
Pool-Video Vergleich: Top-3 Pool-Modelle aus Jennifers Bewertung.

Aus video_test_02_bewertung.csv die drei besten fuer pool:
  1) Kling 3.0 V3  — Nein-Halluzination, "Das beste!"  (schon generiert)
  2) Kling O3      — Ja-leichte Halluzination, "Wassersimulation top"
  3) Veo 3.1       — Ja-leichte Halluzination, aber "water ripples fehlen"

Hier laeuft nur 2) und 3) auf demselben Ausgangsbild (Kling V3 liegt
schon in outputs/pool_video/). Ripples explizit im Prompt um den
Schwimmring herum gefordert.

Input:  outputs/pool_badehose/A_v6_run3_20260527_104322.png
Output: outputs/pool_video/A_v6_run3_<modell>_<stamp>.mp4

Kosten: Kling O3 ~$0.84 + Veo 3.1 ~$0.80 = ~$1.64
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_video"
RESULTS_FILE = SCRIPT_DIR / "pool_video_results.json"

IMG = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

PROMPT = (
    "Static locked-off camera looking down at a turquoise swimming pool. "
    "The voxel / lego-block character lies relaxed on the gold inflatable "
    "pool ring and drifts ever so gently in place. Soft concentric water "
    "RIPPLES radiate outward from around the inflatable ring across the "
    "turquoise pool, and bright caustic light patterns on the pool floor "
    "shimmer and dance continuously with the water movement. Everything "
    "else stays completely still — the sun loungers, potted plants and "
    "palm-leaf shadows on the deck do not move, the flip-flops at the "
    "poolside do not move, the framing does not change. The voxel "
    "character's body, his cap and his white featureless voxel face / "
    "ear stay exactly as they are in the still image — no facial "
    "features ever appear, no eyes, no mouth, no nose. Voxel / lego-block "
    "art style preserved throughout. Bright summer daylight."
)

NEG = (
    "face, eyes, mouth, nose, eyebrows, facial features appearing on the "
    "white mask, the white face becoming skin coloured, character pose "
    "changes, character moves around the pool, camera pan, camera tilt, "
    "camera zoom, camera dolly, camera movement of any kind, scene "
    "reframing, deformed limbs, melted voxels, photorealistic style, "
    "loss of voxel blocks"
)

MODELS = [
    {
        "name": "kling_o3",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "5", "generate_audio": False},
        "cost": "$0.84",
        "supports_negative": True,
    },
    # Veo 3.1 already generated this run — comment out to avoid re-spend
    # {
    #     "name": "veo31",
    #     "endpoint": "fal-ai/veo3/image-to-video",
    #     "image_key": "image_url",
    #     "extra_args": {"duration": "4s", "generate_audio": False},
    #     "cost": "$0.80",
    #     "supports_negative": False,
    # },
]


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
    print("=" * 64)
    print(f"POOL-VIDEO COMPARE | Kling O3 + Veo 3.1 | {stamp} | ~$1.64")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG.exists(), f"missing: {IMG}"

    image_url = upload(IMG)

    for m in MODELS:
        print(f"\n--- {m['name']} | {m['endpoint']} ---")
        args = {m["image_key"]: image_url, "prompt": PROMPT, **m["extra_args"]}
        if m["supports_negative"]:
            args["negative_prompt"] = NEG
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                m["endpoint"], arguments=args,
                with_logs=True, on_queue_update=on_queue,
            )
            elapsed = time.time() - t0
            video_url = extract_video_url(result)
            saved = None
            if video_url:
                saved = save_video(video_url, f"A_v6_run3_{m['name']}_{stamp}")
            append_record({
                "run": stamp, "model": m["name"], "endpoint": m["endpoint"],
                "input": IMG.name, "prompt": PROMPT,
                "args": {k: v for k, v in args.items() if k != m["image_key"]},
                "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
                "video_url": video_url,
                "saved": saved.name if saved else None,
                "timestamp": datetime.now().isoformat(),
            })
            print(f"  OK in {elapsed:.1f}s -> "
                  f"{saved.name if saved else 'NO VIDEO'}")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "model": m["name"], "endpoint": m["endpoint"],
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "cost_est": m["cost"],
                "timestamp": datetime.now().isoformat(),
            })

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
