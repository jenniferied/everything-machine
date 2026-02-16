#!/usr/bin/env python3
"""
Video Test 02: Image-to-Video Model Comparison — Four Images, Five Models
Four input images (studio, pool, night_drive, spiral_staircase) tested with
5 models. PixVerse v5.5 and Seedance Pro dropped after first round.
Skips already-generated videos (re-runnable).
Estimated total cost: ~$14.96 (5 models × 4 images = 20 videos)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "video_test_02"
RESULTS_FILE = SCRIPT_DIR / "video_test_02_results.json"

IMAGES = [
    {
        "tag": "studio",
        "path": SCRIPT_DIR / "outputs" / "14_nanobanana_scenes_landscape" / "studio.png",
        "prompt": (
            "The voxel character nods gently to the beat, fingers resting on "
            "the mixing console. Monitor screens glow steadily. Camera holds still."
        ),
    },
    {
        "tag": "pool",
        "path": SCRIPT_DIR / "outputs" / "24_nanobanana_apose_portrait" / "pool_floaty.png",
        "prompt": (
            "The voxel character drifts slowly on the pool ring. Water ripples "
            "gently around the float. Camera holds still from above."
        ),
    },
    {
        "tag": "night_drive",
        "path": SCRIPT_DIR / "outputs" / "20_nanobanana_final_portrait" / "night_drive.png",
        "prompt": (
            "The voxel character drives steadily down the desert highway. "
            "Headlights illuminate the road ahead. Camera holds still from behind."
        ),
    },
    {
        "tag": "spiral_staircase",
        "path": SCRIPT_DIR / "outputs" / "18_nanobanana_v2_portrait" / "spiral_staircase.png",
        "prompt": (
            "The white marble staircase begins to glow with a deep blue light. "
            "The voxel character slowly ascends the steps. Camera holds still."
        ),
    },
]

MODELS = [
    {
        "name": "pixverse_v55",
        "endpoint": "fal-ai/pixverse/v5.5/image-to-video",
        "cost": "$0.20",
        "image_key": "image_url",
        "extra_args": {
            "duration": 5,
            "generate_audio_switch": False,
            "thinking_type": "disabled",
        },
    },
    {
        "name": "ltx2",
        "endpoint": "fal-ai/ltx-2/image-to-video",
        "cost": "$0.36",
        "image_key": "image_url",
        "extra_args": {
            "duration": 6,
        },
    },
    {
        "name": "wan_v26",
        "endpoint": "wan/v2.6/image-to-video",
        "cost": "$0.50",
        "image_key": "image_url",
        "extra_args": {
            "duration": "5",
        },
    },
    {
        "name": "seedance_pro",
        "endpoint": "fal-ai/bytedance/seedance/v1/pro/image-to-video",
        "cost": "$0.62",
        "image_key": "image_url",
        "extra_args": {
            "duration": "5",
            "camera_fixed": True,
        },
    },
    {
        "name": "veo31",
        "endpoint": "fal-ai/veo3/image-to-video",
        "cost": "$0.80",
        "image_key": "image_url",
        "extra_args": {
            "duration": "4s",
            "generate_audio": False,
        },
    },
    {
        "name": "kling_o3",
        "endpoint": "fal-ai/kling-video/o3/standard/image-to-video",
        "cost": "$0.84",
        "image_key": "image_url",
        "extra_args": {
            "duration": "5",
            "generate_audio": False,
        },
    },
    {
        "name": "kling_v3",
        "endpoint": "fal-ai/kling-video/v3/standard/image-to-video",
        "cost": "$0.84",
        "image_key": "start_image_url",
        "extra_args": {
            "duration": "5",
            "generate_audio": False,
        },
    },
]

results = []
uploaded_urls = {}  # cache: image path -> uploaded URL


def load_existing_results():
    global results
    if RESULTS_FILE.exists():
        results = json.loads(RESULTS_FILE.read_text())
        print(f"  Loaded {len(results)} existing results")


def already_done(filename):
    """Skip if MP4 already exists and has a successful result."""
    mp4 = OUTPUT_DIR / f"{filename}.mp4"
    if not mp4.exists():
        return False
    return any(r["test"] == filename and not r.get("error") for r in results)


def upload(path: Path) -> str:
    key = str(path)
    if key not in uploaded_urls:
        print(f"  Uploading {path.name}...")
        uploaded_urls[key] = fal_client.upload_file(str(path))
        print(f"  -> {uploaded_urls[key]}")
    return uploaded_urls[key]


def save_video(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{name}.mp4"
    resp = httpx.get(url, timeout=120)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log(test, model, prompt, elapsed, cost, video_url, error=None):
    results.append({
        "test": test, "model": model, "prompt": prompt[:80],
        "elapsed_s": round(elapsed, 1), "cost_est": cost,
        "video": video_url, "error": error, "timestamp": datetime.now().isoformat(),
    })
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for l in update.logs:
            print(f"      [{l.get('message', '')}]")


def run_model(model_cfg, image_url, image_tag, prompt):
    name = model_cfg["name"]
    endpoint = model_cfg["endpoint"]
    cost = model_cfg["cost"]
    filename = f"{name}_{image_tag}"

    if already_done(filename):
        print(f"\n  {name} × {image_tag} | SKIP (already done)")
        return

    print(f"\n  {name} × {image_tag} | {endpoint}")

    args = {"prompt": prompt}
    args.update(model_cfg["extra_args"])
    args[model_cfg["image_key"]] = image_url

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            endpoint, arguments=args, with_logs=True, on_queue_update=on_queue
        )
        elapsed = time.time() - t0

        video_url = result.get("video", {}).get("url", "")
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
            log(filename, endpoint, prompt, elapsed, cost, video_url)
            print(f"    OK in {elapsed:.1f}s")
        else:
            print(f"    WARNING: No video URL found in response")
            print(f"    Response keys: {list(result.keys())}")
            log(filename, endpoint, prompt, elapsed, cost, "", f"No video URL in response: {list(result.keys())}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(filename, endpoint, prompt, elapsed, cost, "", str(e))


def main():
    import sys
    only = set(sys.argv[1:])  # pass model names to retry specific ones

    total_runs = len(IMAGES) * len(MODELS)
    print("=" * 60)
    print("VIDEO TEST 02 — Four Images × Five Models")
    if only:
        print(f"Retrying: {', '.join(only)}")
    else:
        print(f"{len(IMAGES)} Images × {len(MODELS)} Models = {total_runs} videos")
    for img in IMAGES:
        print(f"  [{img['tag']}] {img['path'].name}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for img in IMAGES:
        if not img["path"].exists():
            print(f"ERROR: Input image not found: {img['path']}")
            return

    load_existing_results()

    # Upload only images that have pending work
    for img in IMAGES:
        has_pending = any(
            not already_done(f"{m['name']}_{img['tag']}")
            for m in MODELS
            if not only or m["name"] in only
        )
        if has_pending:
            upload(img["path"])

    # Run each image × model combination
    for img in IMAGES:
        image_url = uploaded_urls.get(str(img["path"]))
        if not image_url:
            continue  # all done for this image

        print(f"\n{'—'*60}")
        print(f"IMAGE: {img['tag']} ({img['path'].name})")
        print(f"{'—'*60}")

        for model_cfg in MODELS:
            if only and model_cfg["name"] not in only:
                continue
            run_model(model_cfg, image_url, img["tag"], img["prompt"])

    print(f"\n{'='*60}\nVIDEO TEST 02 COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Total results: {total}, OK: {ok_count}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
