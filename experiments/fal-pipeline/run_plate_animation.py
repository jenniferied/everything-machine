#!/usr/bin/env python3
"""
Plate Animation: Ant macro image through three current-gen video models.
Input: inputs/plate.png (1672x941, 16:9 landscape).
Models: Kling 3.0 Pro (15s), Seedance 2.0 Fast (15s), Veo 3.1 Fast (8s cap).
Estimated total: ~$6.11. Skips already-generated videos (re-runnable).
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
INPUT_IMAGE = SCRIPT_DIR / "inputs" / "plate.png"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "plate_animation"
RESULTS_FILE = SCRIPT_DIR / "plate_animation_results.json"

PROMPT = (
    "The ant walks slowly across the stone, antennae twitching gently. "
    "A soft breeze stirs the surrounding leaves; dappled sunlight shifts "
    "softly across the ground. Shallow depth of field is preserved throughout. "
    "Macro nature shot, cinematic, natural colors. Camera holds still."
)

MODELS = [
    {
        "name": "kling_v3_pro",
        "endpoint": "fal-ai/kling-video/v3/pro/image-to-video",
        "image_key": "start_image_url",
        "duration_s": 15,
        "cost_est": "$1.68",
        "extra_args": {
            "duration": "15",
            "generate_audio": False,
        },
    },
    {
        "name": "veo31_fast",
        "endpoint": "fal-ai/veo3.1/fast/image-to-video",
        "image_key": "image_url",
        "duration_s": 8,
        "cost_est": "$0.80",
        "extra_args": {
            "duration": "8s",
            "resolution": "720p",
            "aspect_ratio": "auto",
            "generate_audio": False,
        },
    },
    {
        "name": "seedance_v2_fast",
        "endpoint": "bytedance/seedance-2.0/fast/image-to-video",
        "image_key": "image_url",
        "duration_s": 15,
        "cost_est": "$3.63",
        "extra_args": {
            "duration": "15",
            "resolution": "720p",
            "aspect_ratio": "auto",
            "generate_audio": False,
        },
    },
]

results = []


def load_existing_results():
    global results
    if RESULTS_FILE.exists():
        results = json.loads(RESULTS_FILE.read_text())
        print(f"  Loaded {len(results)} existing results")


def already_done(filename):
    mp4 = OUTPUT_DIR / f"{filename}.mp4"
    if not mp4.exists():
        return False
    return any(r["test"] == filename and not r.get("error") for r in results)


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=180)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log(test, model, elapsed, cost, video_url, duration_s, error=None):
    results.append({
        "test": test,
        "model": model,
        "duration_s": duration_s,
        "prompt": PROMPT[:100],
        "elapsed_s": round(elapsed, 1),
        "cost_est": cost,
        "video": video_url,
        "error": error,
        "timestamp": datetime.now().isoformat(),
    })
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def run_model(model_cfg, image_url):
    name = model_cfg["name"]
    endpoint = model_cfg["endpoint"]
    filename = name

    if already_done(filename):
        print(f"\n  {name} | SKIP (already done)")
        return

    print(f"\n  {name} | {endpoint} | {model_cfg['duration_s']}s | {model_cfg['cost_est']}")

    args = {"prompt": PROMPT}
    args.update(model_cfg["extra_args"])
    args[model_cfg["image_key"]] = image_url

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            endpoint,
            arguments=args,
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0

        video_url = result.get("video", {}).get("url", "") if isinstance(result.get("video"), dict) else ""
        if not video_url:
            video_url = result.get("video_url", "")
        if not video_url:
            for key in ("output", "data"):
                if key in result and isinstance(result[key], dict):
                    video_url = result[key].get("url", "")
                    if video_url:
                        break

        if video_url:
            save_video(video_url, filename)
            log(filename, endpoint, elapsed, model_cfg["cost_est"], video_url, model_cfg["duration_s"])
            print(f"    OK in {elapsed:.1f}s")
        else:
            print(f"    WARNING: No video URL in response. Keys: {list(result.keys())}")
            log(filename, endpoint, elapsed, model_cfg["cost_est"], "", model_cfg["duration_s"],
                f"No video URL. Response keys: {list(result.keys())}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(filename, endpoint, elapsed, model_cfg["cost_est"], "", model_cfg["duration_s"], str(e))


def main():
    import sys
    only = set(sys.argv[1:])

    print("=" * 60)
    print("PLATE ANIMATION — 3 Models on ant macro image")
    if only:
        print(f"Retrying: {', '.join(only)}")
    total_cost = sum(
        float(m["cost_est"].replace("$", ""))
        for m in MODELS
        if not only or m["name"] in only
    )
    print(f"Models: {len(MODELS) if not only else len(only)} | Estimated total: ${total_cost:.2f}")
    print(f"Input: {INPUT_IMAGE}")
    print(f"Prompt: {PROMPT[:80]}...")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    if not INPUT_IMAGE.exists():
        print(f"ERROR: Input image not found: {INPUT_IMAGE}")
        return

    load_existing_results()

    # Upload once, reuse URL across all models
    pending = [m for m in MODELS if (not only or m["name"] in only) and not already_done(m["name"])]
    if not pending:
        print("\nAll models already complete. Nothing to do.")
        return

    print(f"\n  Uploading {INPUT_IMAGE.name}...")
    image_url = fal_client.upload_file(str(INPUT_IMAGE))
    print(f"  -> {image_url}")

    for model_cfg in MODELS:
        if only and model_cfg["name"] not in only:
            continue
        run_model(model_cfg, image_url)

    print(f"\n{'='*60}\nPLATE ANIMATION COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Total results: {total} | OK: {ok_count} | Errors: {errors}")
    for r in results:
        status = "FAIL" if r.get("error") else "OK"
        print(f"  [{status}] {r['test']} — {r['duration_s']}s — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
