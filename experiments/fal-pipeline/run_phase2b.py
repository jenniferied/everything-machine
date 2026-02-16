#!/usr/bin/env python3
"""
Experiment 9 — Phase 2b: Top-3 Modelle mit KeplerPosed (casual pose)
FLUX Kontext, GPT-Image-1.5, NanoBanana Pro
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
OUTPUT_DIR = SCRIPT_DIR / "outputs"
RESULTS_FILE = SCRIPT_DIR / "phase2b_results.json"
INPUT_IMAGE = SCRIPT_DIR / "inputs" / "kepler-posed-1024.png"

SCENE_PROMPTS = [
    "Place this voxel character in a neon-lit cyberpunk city at night, walking down a rain-soaked street with hands in pockets, cinematic lighting, reflections on wet ground",
    "Place this voxel character sitting on a park bench in autumn, golden leaves falling around him, soft warm afternoon light",
    "Place this voxel character on a dark concert stage, performing with a microphone, dramatic red and blue spotlights, fog machine, crowd silhouettes in foreground",
    "Place this voxel character standing on a rooftop at sunset, looking over a vast city skyline, wind blowing, golden hour lighting",
    "Place this voxel character in a recording studio, sitting at a mixing desk with headphones around neck, warm ambient lighting, monitors glowing",
]

results = []


def save_image(url: str, test_name: str, idx: int) -> Path:
    out_dir = OUTPUT_DIR / test_name
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = out_dir / f"{test_name}_{idx:03d}{ext}"
    resp = httpx.get(url, timeout=60)
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


def run_model(test_name, model, build_args, cost, prompts=SCENE_PROMPTS):
    print(f"\n{'='*60}\n{test_name}: {model}\n{'='*60}")
    for i, prompt in enumerate(prompts):
        print(f"\n  Prompt {i+1}/{len(prompts)}: ...{prompt[-60:]}")
        args = build_args(prompt)
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


def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 2b: Top-3 mit KeplerPosed")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    # Upload posed image
    print(f"\nUploading {INPUT_IMAGE.name}...")
    image_url = fal_client.upload_file(str(INPUT_IMAGE))
    print(f"-> {image_url}")

    # FLUX Kontext [pro]
    run_model("10_flux_kontext_posed", "fal-ai/flux-pro/kontext",
              lambda p: {"image_url": image_url, "prompt": p, "guidance_scale": 3.5},
              "$0.04")

    # GPT-Image-1.5 edit
    run_model("11_gpt15_posed", "fal-ai/gpt-image-1.5/edit",
              lambda p: {"image_urls": [image_url], "prompt": p,
                         "quality": "medium", "size": "1024x1024"},
              "$0.04")

    # NanoBanana Pro edit
    run_model("12_nanobanana_posed", "fal-ai/nano-banana-pro/edit",
              lambda p: {"image_urls": [image_url],
                         "prompt": f"Take the voxel character from the reference image and {p}. "
                                   f"Keep the blocky voxel aesthetic, no face.",
                         "aspect_ratio": "1:1"},
              "$0.15")

    # Summary
    print(f"\n{'='*60}\nPHASE 2b COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    print(f"Tests: {total}, Errors: {errors}, Cost: ~${0.04*5 + 0.04*5 + 0.15*5:.2f}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
