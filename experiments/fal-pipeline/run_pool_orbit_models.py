#!/usr/bin/env python3
"""
Pool-Orbit Modell-Vergleich — andere Modelle als Kling V3 standard.

Problem mit Kling V3 standard:
  - Pool-Caustics pulsieren statt natuerlich zu flow-en
  - Gesicht entsteht in der Maske bei Close-ups
  - Char sinkt teilweise ins Wasser
  - Dive-in ist eigentlich nur ein Push-in geworden (nicht wirklich in den Pool)

Hier: derselbe Orbit-Prompt auf 4 alternative Modelle, plus dive_in auf
Kling V3 Pro zum Vergleich. Alle 5s, audio off. Separate Dateinamen pro
Modell zum Rueckverfolgen.

Modelle (orbit, 5s):
  1) Kling V3 PRO          ~$0.80   start_image_url
  2) Kling O3 standard     ~$0.42   image_url
  3) Veo 3.1               ~$0.80   image_url, duration "4s"
  4) Seedance 1.0 Pro      ~$0.62   image_url, resolution 1080p

Plus 1 dive_in auf Kling V3 Pro: ~$0.80

Gesamt ~$3.44, unter $5-Budget.
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
    "pool deck. Water ripples and caustic light patterns on the pool "
    "floor shimmer SMOOTHLY without pulsing. Bright summer daylight."
)

ORBIT_CAMERA = (
    "The CAMERA slowly ORBITS around the inflatable ring at a constant "
    "medium-low altitude — circling smoothly so the viewing angle on "
    "the ring and the voxel character gradually shifts through 30-60 "
    "degrees over the clip. Smooth cinematic arc movement, no jitter, "
    "no zoom. The ring and character stay roughly centred in frame as "
    "the world rotates around them."
)

DIVE_CAMERA = (
    "The CAMERA performs a dramatic DESCENT INTO THE POOL: it starts "
    "at the original high angle looking down at the character on the "
    "ring, then sweeps continuously DOWNWARD and FORWARD as if a "
    "drone-camera diving toward the water surface. By the END of the "
    "clip the camera is right at the water surface near the ring, "
    "almost touching it — a cinematic plunge toward the float. Smooth "
    "continuous motion, no jitter. The voxel character, ring and white "
    "face mask stay exactly the same throughout — only the camera's "
    "vantage point changes."
)

NEG = (
    "face, eyes, mouth, nose, facial features appearing on the white "
    "mask, the white face becoming skin coloured, character sinking "
    "into the water, character submerged, character moves around the "
    "pool, deformed limbs, melted voxels, photorealistic style, loss "
    "of voxel blocks, jittery scene, heavy reframing, pulsing caustics, "
    "flickering water"
)

ORBIT_PROMPT = f"{SCENE_BASE} {ORBIT_CAMERA}"
DIVE_PROMPT = f"{SCENE_BASE} {DIVE_CAMERA}"


# Modell-Configs. image_key + extra_args + supports_negative
MODELS = [
    {
        "name": "kling_v3_pro",
        "endpoint": "fal-ai/kling-video/v3/pro/image-to-video",
        "image_key": "start_image_url",
        "extra_args": {"duration": "5", "generate_audio": False},
        "supports_neg": True,
        "cost_est": "$0.80",
    },
    {
        "name": "kling_o3",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "5", "generate_audio": False},
        "supports_neg": True,
        "cost_est": "$0.42",
    },
    {
        "name": "veo31",
        "endpoint": "fal-ai/veo3/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "4s", "generate_audio": False},
        "supports_neg": False,
        "cost_est": "$0.80",
    },
    {
        "name": "seedance_pro",
        "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
        "image_key": "image_url",
        "extra_args": {"duration": "5", "resolution": "1080p",
                       "camera_fixed": False},
        "supports_neg": False,
        "cost_est": "$0.62",
    },
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


def run(label: str, model_cfg: dict, prompt: str, source_url: str,
        save_name: str, stamp: str):
    m = model_cfg
    args = {m["image_key"]: source_url, "prompt": prompt, **m["extra_args"]}
    if m["supports_neg"]:
        args["negative_prompt"] = NEG
    print(f"\n--- {label} | {m['endpoint']} | {m['cost_est']} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=args,
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = extract_video_url(result)
        saved = save_video(url, f"{save_name}_{stamp}") if url else None
        append_record({
            "run": stamp, "label": label, "model": m["name"],
            "endpoint": m["endpoint"], "input": SOURCE.name,
            "prompt": prompt,
            "args": {k: v for k, v in args.items() if k != m["image_key"]},
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost_est"],
            "video_url": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> "
              f"{saved.name if saved else 'NO VIDEO'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": label, "model": m["name"],
            "endpoint": m["endpoint"], "args": args, "error": str(e),
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost_est"],
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL ORBIT MODEL COMPARE | {stamp} | ~$3.44 (Budget $5)")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)

    # 1-4: orbit auf 4 Modelle
    for m in MODELS:
        run(f"orbit_{m['name']}", m, ORBIT_PROMPT, src_url,
            f"A_v6_run3_orbit_{m['name']}_5s", stamp)

    # 5: dive_in auf Kling V3 Pro
    pro_cfg = MODELS[0]
    run("dive_in_kling_v3_pro", pro_cfg, DIVE_PROMPT, src_url,
        "A_v6_run3_dive_in_kling_v3_pro_5s", stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
