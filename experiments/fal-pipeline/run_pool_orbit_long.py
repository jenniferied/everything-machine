#!/usr/bin/env python3
"""
Pool-Orbit lang — Veo 3 (8s max) + Seedance Pro (12s max).

Jennifer findet Kling zu zahm fuer den Orbit — Veo und Seedance haben
weiter rotiert. Hier ihre Max-Laenge mit verschaerftem Orbit-Prompt
(full 270-360° rotation explizit), damit die Rotation wirklich rumgeht.

  1) Seedance 1.0 Pro  12s   ~$1.50
  2) Seedance 1.0 Pro  12s (run B, anderer Seed)  ~$1.50
  3) Veo 3.1           8s    ~$1.60

Total ~$4.60, unter $6-Budget.
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

SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

SCENE_BASE = (
    "Voxel / lego-block style swimming pool scene. The voxel character "
    "lies relaxed on the gold inflatable pool ring in the turquoise "
    "pool. He wears pink-and-white Hawaiian swim trunks and his face is "
    "a featureless plain WHITE voxel mask (no eyes, no mouth, no facial "
    "features ever appear). He keeps his dark cap and his relaxed pose "
    "throughout. Sun loungers, potted plants and palm shadows on the "
    "pool deck. Bright summer daylight, smooth water caustics."
)

# Schaerferer Orbit-Prompt: explizit volle Drehung
ORBIT_FULL = (
    "The CAMERA performs a CONTINUOUS FULL 360-DEGREE ORBIT around the "
    "voxel character and the inflatable ring — completing a full or "
    "nearly full circle by the end of the clip. The camera arcs "
    "smoothly all the way around the ring at a constant medium-low "
    "altitude, so the viewing angle sweeps through the entire circle: "
    "we see the character from one side, then from behind, then from "
    "the other side, then back near the original angle. Smooth "
    "continuous cinematic orbital sweep, NOT a small arc, NOT a "
    "subtle shift — a full revolution. The ring and character stay "
    "centred in frame as the world rotates around them. No zoom, no "
    "jitter."
)

PROMPT = f"{SCENE_BASE} {ORBIT_FULL}"

NEG = (
    "face, eyes, mouth, nose, facial features appearing on the white "
    "mask, the white face becoming skin coloured, character sinking "
    "into the water, character submerged, character body distortion, "
    "melted voxels, deflated character, character flattened onto ring, "
    "deformed limbs, photorealistic style, loss of voxel blocks, "
    "jittery scene, heavy reframing, pulsing caustics, flickering "
    "water, subtle camera, small orbit"
)


RUNS = [
    {
        "name": "seedance_pro_12s_A",
        "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "12", "resolution": "1080p",
                       "camera_fixed": False},
        "supports_neg": False,
        "cost_est": "$1.50",
    },
    {
        "name": "seedance_pro_12s_B",
        "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "12", "resolution": "1080p",
                       "camera_fixed": False},
        "supports_neg": False,
        "cost_est": "$1.50",
    },
    {
        "name": "veo31_8s",
        "endpoint": "fal-ai/veo3/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "8s", "generate_audio": False},
        "supports_neg": False,
        "cost_est": "$1.60",
    },
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=600, follow_redirects=True)
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


def run(cfg: dict, source_url: str, stamp: str):
    args = {cfg["image_key"]: source_url, "prompt": PROMPT, **cfg["extra_args"]}
    if cfg["supports_neg"]:
        args["negative_prompt"] = NEG
    print(f"\n--- {cfg['name']} | {cfg['endpoint']} | {cfg['cost_est']} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            cfg["endpoint"], arguments=args,
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(
            url, f"A_v6_run3_orbit_{cfg['name']}_{stamp}"
        ) if url else None
        append_record({
            "run": stamp, "label": f"orbit_{cfg['name']}",
            "model": cfg["name"], "endpoint": cfg["endpoint"],
            "input": SOURCE.name, "prompt": PROMPT,
            "args": {k: v for k, v in args.items() if k != cfg["image_key"]},
            "elapsed_s": round(elapsed, 1), "cost_est": cfg["cost_est"],
            "video_url": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> "
              f"{saved.name if saved else 'NO VIDEO'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": f"orbit_{cfg['name']}",
            "model": cfg["name"], "endpoint": cfg["endpoint"],
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "cost_est": cfg["cost_est"],
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL ORBIT LONG | Seedance×2 + Veo | {stamp} | ~$4.60 von $6")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)
    for cfg in RUNS:
        run(cfg, src_url, stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
