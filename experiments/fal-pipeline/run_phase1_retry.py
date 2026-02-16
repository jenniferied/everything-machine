#!/usr/bin/env python3
"""Re-run only the failed Phase 1 tests with corrected API parameters."""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Load .env.local
env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs"
RESULTS_FILE = SCRIPT_DIR / "phase1_results.json"

KEPLER_PROMPT = (
    "A voxel character made of small 3D cubes, faceless geometric humanoid figure, "
    "white shirt and dark pants, standing in a dramatic cinematic environment, "
    "volumetric lighting, no face, blocky pixel art style 3D character"
)

SCENE_PROMPTS = [
    f"{KEPLER_PROMPT}, in a neon-lit cyberpunk city at night",
    f"{KEPLER_PROMPT}, in a foggy forest with golden light rays",
    f"{KEPLER_PROMPT}, on a concert stage with dramatic spotlights",
]

# Load existing results
results = json.loads(RESULTS_FILE.read_text()) if RESULTS_FILE.exists() else []

IMAGE_URL = "https://v3b.fal.media/files/b/0a8e9551/0wGuORlLx52Tm1-xf-96K_kepler-a-pose-1024.png"


def save_image(url: str, test_name: str, idx: int) -> Path:
    out_dir = OUTPUT_DIR / test_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{test_name}_{idx:03d}.png"
    resp = httpx.get(url)
    out_path.write_bytes(resp.content)
    print(f"  Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log(test_name, model, prompt, elapsed, cost, urls, error=None):
    entry = {
        "test": test_name, "model": model, "prompt": prompt[:100],
        "elapsed_s": round(elapsed, 1), "cost_est": cost,
        "images": urls, "error": error, "timestamp": datetime.now().isoformat(),
    }
    results.append(entry)
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for l in update.logs:
            print(f"    [{l.get('message', '')}]")


def run_test(test_name, model, extra_args, cost, prompts=SCENE_PROMPTS):
    print(f"\n{'='*60}\n{test_name}: {model}\n{'='*60}")
    for i, prompt in enumerate(prompts):
        print(f"\n  Prompt {i+1}/{len(prompts)}: ...{prompt[-50:]}")
        args = {"prompt": prompt, **extra_args}
        t0 = time.time()
        try:
            result = fal_client.subscribe(model, arguments=args,
                                          with_logs=True, on_queue_update=on_queue)
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_image(url, test_name, i * 10 + j)
            log(test_name, model, prompt, elapsed, cost, urls)
            print(f"  OK in {elapsed:.1f}s — {len(urls)} images")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            log(test_name, model, prompt, elapsed, cost, [], str(e))


print(f"Retry Phase 1 — {datetime.now().isoformat()}")
print(f"Using uploaded image: {IMAGE_URL}")

# Test 1: MiniMax Subject Reference
run_test("01_minimax_subject", "fal-ai/minimax/image-01/subject-reference",
         {"image_url": IMAGE_URL, "aspect_ratio": "1:1"}, "$0.01")

# Test 2: Z-Image Turbo ControlNet (depth preprocessing)
run_test("02_zimage_controlnet", "fal-ai/z-image/turbo/controlnet",
         {"image_url": IMAGE_URL, "preprocess": "depth", "image_size": "square_hd"}, "$0.007")

# Test 3: FLUX Control LoRA Depth
run_test("03_flux_depth", "fal-ai/flux-control-lora-depth",
         {"control_lora_image_url": IMAGE_URL, "image_size": "square_hd"}, "$0.04")

# Test 4: FLUX Control LoRA Canny
run_test("04_flux_canny", "fal-ai/flux-control-lora-canny",
         {"control_lora_image_url": IMAGE_URL, "image_size": "square_hd"}, "$0.04")

# Summary
print(f"\n{'='*60}\nDONE — {len(results)} total results in {RESULTS_FILE.name}")
