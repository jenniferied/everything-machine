#!/usr/bin/env python3
"""
Experiment 9 — Phase 2: Thesis-Top-Modelle mit Kepler A-Pose
FLUX Kontext, GPT-Image-1.5, SeedDream v4.5, NanoBanana Pro
"""

import os
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
RESULTS_FILE = SCRIPT_DIR / "phase2_results.json"

IMAGE_URL = "https://v3b.fal.media/files/b/0a8e9551/0wGuORlLx52Tm1-xf-96K_kepler-a-pose-1024.png"

# Prompts: Kepler in verschiedenen Szenen mit neuen Posen
SCENE_PROMPTS = [
    "Place this voxel character in a neon-lit cyberpunk city at night, walking down the street with hands in pockets, cinematic lighting",
    "Place this voxel character in a foggy forest clearing, sitting on a fallen tree, golden light rays filtering through the canopy",
    "Place this voxel character on a concert stage, performing with arms raised, dramatic spotlights and fog machine effects",
]

results = []


def save_image(url: str, test_name: str, idx: int) -> Path:
    out_dir = OUTPUT_DIR / test_name
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = ".png"
    if ".jpg" in url or "jpeg" in url:
        ext = ".jpg"
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


# ─── Test 6: FLUX Kontext [pro] — Character→New Scene ────────────────────────
def test_flux_kontext():
    test_name = "06_flux_kontext"
    model = "fal-ai/flux-pro/kontext"
    print(f"\n{'='*60}\nTEST 6: FLUX Kontext [pro] — Character Consistency\n{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-60:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(model, arguments={
                "image_url": IMAGE_URL,
                "prompt": prompt,
                "guidance_scale": 3.5,
            }, with_logs=True, on_queue_update=on_queue)
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_image(url, test_name, i * 10 + j)
            log(test_name, model, prompt, elapsed, "$0.04", urls)
            print(f"  OK in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            log(test_name, model, prompt, elapsed, "$0.04", [], str(e))


# ─── Test 7: GPT-Image-1.5 edit ──────────────────────────────────────────────
def test_gpt_image():
    test_name = "07_gpt_image_15"
    model = "fal-ai/gpt-image-1.5/edit"
    print(f"\n{'='*60}\nTEST 7: GPT-Image-1.5 Edit\n{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-60:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(model, arguments={
                "image_urls": [IMAGE_URL],
                "prompt": prompt,
                "quality": "medium",
                "size": "1024x1024",
            }, with_logs=True, on_queue_update=on_queue)
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_image(url, test_name, i * 10 + j)
            log(test_name, model, prompt, elapsed, "$0.04", urls)
            print(f"  OK in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            log(test_name, model, prompt, elapsed, "$0.04", [], str(e))


# ─── Test 8: SeedDream v4.5 edit ─────────────────────────────────────────────
def test_seeddream():
    test_name = "08_seeddream"
    model = "fal-ai/bytedance/seedream/v4.5/edit"
    print(f"\n{'='*60}\nTEST 8: SeedDream v4.5 Edit\n{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-60:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(model, arguments={
                "image_urls": [IMAGE_URL],
                "prompt": f"Using the voxel character from image 1: {prompt}",
            }, with_logs=True, on_queue_update=on_queue)
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_image(url, test_name, i * 10 + j)
            log(test_name, model, prompt, elapsed, "$0.04", urls)
            print(f"  OK in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            log(test_name, model, prompt, elapsed, "$0.04", [], str(e))


# ─── Test 9: NanoBanana Pro edit ─────────────────────────────────────────────
def test_nanobanana():
    test_name = "09_nanobanana_pro"
    model = "fal-ai/nano-banana-pro/edit"
    print(f"\n{'='*60}\nTEST 9: NanoBanana Pro (Gemini 3 Pro) Edit\n{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-60:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(model, arguments={
                "image_urls": [IMAGE_URL],
                "prompt": f"Take the voxel character from the reference image and {prompt}. "
                          f"Keep the character's blocky voxel aesthetic, no face, geometric style.",
                "aspect_ratio": "1:1",
            }, with_logs=True, on_queue_update=on_queue)
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_image(url, test_name, i * 10 + j)
            log(test_name, model, prompt, elapsed, "$0.15", urls)
            print(f"  OK in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            log(test_name, model, prompt, elapsed, "$0.15", [], str(e))


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 2: Thesis-Top-Modelle")
    print(f"Input: {IMAGE_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    test_flux_kontext()    # $0.04/img × 3 = $0.12
    test_gpt_image()       # ~$0.04/img × 3 = $0.12
    test_seeddream()       # $0.04/img × 3 = $0.12
    test_nanobanana()      # $0.15/img × 3 = $0.45

    print(f"\n{'='*60}\nPHASE 2 COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    print(f"Tests: {total}, Errors: {errors}")
    for r in results:
        s = "FAIL" if r.get("error") else "OK"
        print(f"  [{s}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
