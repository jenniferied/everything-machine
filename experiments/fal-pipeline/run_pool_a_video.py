#!/usr/bin/env python3
"""
Pool-Video aus A_v6_run3 (Kling 3.0 V3 standard image-to-video).

Modellwahl: Kling 3.0 V3 ist Jennifers klarer Pool-Favorit aus
video_test_02_bewertung.csv — "Gut", Halluzination "Nein", Notiz
"Das beste!". Alle anderen pool-Modelle haben Gesichter erzeugt
(wan, seedance, pixverse) oder die Kamera bewegt (ltx2). Kling V3
ist hier essentiell, weil die weisse Maske nicht zu einem Gesicht
halluzinieren darf.

Input:  outputs/pool_badehose/A_v6_run3_20260527_104322.png  (1376x768)
Output: outputs/pool_video/A_v6_run3_kling_v3_<stamp>.mp4

Prompt: statische Kamera, Char liegt entspannt auf dem Ring, Wasser-
Rippeln und Caustics. Sonst nichts.

Model: fal-ai/kling-video/v3/standard/image-to-video  (15s, audio off, ~$1.26)
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

ENDPOINT = "fal-ai/kling-video/v3/standard/image-to-video"

PROMPT = (
    "Static locked-off camera looking down at a turquoise swimming pool. "
    "The voxel / lego-block character lies relaxed on the gold inflatable "
    "pool ring and drifts ever so gently in place. The pool water ripples "
    "softly all around the ring and the caustic light patterns on the "
    "pool floor shimmer and dance with the water movement. Everything "
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

ARGS = {
    "duration": "15",   # max bei Kling V3 standard
    "generate_audio": False,
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
    print(f"POOL-VIDEO A_v6_run3 | Kling 3.0 V3 standard | 15s | "
          f"{stamp} | ~$1.26")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert IMG.exists(), f"missing: {IMG}"

    image_url = upload(IMG)

    args = {
        "start_image_url": image_url,
        "prompt": PROMPT,
        "negative_prompt": NEG,
        **ARGS,
    }

    print(f"\n  kling_v3 | {ENDPOINT}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            ENDPOINT, arguments=args,
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        video_url = extract_video_url(result)
        saved = None
        if video_url:
            saved = save_video(video_url, f"A_v6_run3_kling_v3_15s_{stamp}")
        append_record({
            "run": stamp, "model": "kling_v3", "endpoint": ENDPOINT,
            "input": IMG.name, "prompt": PROMPT, "negative_prompt": NEG,
            "args": ARGS, "elapsed_s": round(elapsed, 1),
            "cost_est": "$1.26",
            "video_url": video_url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO VIDEO'}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": "kling_v3", "endpoint": ENDPOINT,
            "input": IMG.name, "error": str(e),
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.84",
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
