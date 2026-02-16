#!/usr/bin/env python3
"""
Experiment 9 — Phase 1: Schnelle fal.ai Tests mit Kepler A-Pose
Systematisches Testen von Modellen mit Kepler-Referenzbild.
"""

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

# Paths
SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = SCRIPT_DIR / "inputs"
OUTPUT_DIR = SCRIPT_DIR / "outputs"
RESULTS_FILE = SCRIPT_DIR / "phase1_results.json"

KEPLER_IMAGE = INPUT_DIR / "kepler-a-pose-1024.png"

# Base prompt describing Kepler
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


def upload_image(path: Path) -> str:
    """Upload local image to fal.ai and return URL."""
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_result_image(result_url: str, test_name: str, index: int) -> Path:
    """Download result image from URL."""
    import httpx
    out_dir = OUTPUT_DIR / test_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{test_name}_{index:03d}.png"
    resp = httpx.get(result_url)
    out_path.write_bytes(resp.content)
    print(f"  Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log_result(results: list, test_name: str, model: str, prompt: str,
               elapsed: float, cost_est: str, image_urls: list, error: str = None):
    """Append result to log."""
    entry = {
        "test": test_name,
        "model": model,
        "prompt": prompt[:100],
        "elapsed_s": round(elapsed, 1),
        "cost_est": cost_est,
        "images": image_urls,
        "error": error,
        "timestamp": datetime.now().isoformat(),
    }
    results.append(entry)
    # Save incrementally
    RESULTS_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(f"    [{log.get('message', '')}]")


# ─── Test 1: MiniMax Subject Reference (cheapest: $0.01/image) ───────────────
def test_minimax_subject(image_url: str, results: list):
    """Subject-reference test — does MiniMax keep the voxel look?"""
    test_name = "01_minimax_subject"
    model = "fal-ai/minimax/image-01/subject-reference"
    print(f"\n{'='*60}")
    print(f"TEST 1: MiniMax Subject Reference")
    print(f"Model: {model}")
    print(f"{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-50:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "image_url": image_url,
                    "aspect_ratio": "1:1",
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_result_image(url, test_name, i * 10 + j)
            log_result(results, test_name, model, prompt, elapsed, "$0.01", urls)
            print(f"  Done in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e}")
            log_result(results, test_name, model, prompt, elapsed, "$0.01", [], str(e))


# ─── Test 2: Z-Image Turbo ControlNet (cheapest ControlNet: $0.0065/MP) ──────
def test_zimage_controlnet(image_url: str, results: list):
    """ControlNet with depth — cheapest structural generation."""
    test_name = "02_zimage_controlnet"
    model = "fal-ai/z-image/turbo/controlnet"
    print(f"\n{'='*60}")
    print(f"TEST 2: Z-Image Turbo ControlNet")
    print(f"Model: {model}")
    print(f"{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-50:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "image_url": image_url,
                    "preprocess": "depth",
                    "image_size": "square_hd",
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_result_image(url, test_name, i * 10 + j)
            log_result(results, test_name, model, prompt, elapsed, "$0.007", urls)
            print(f"  Done in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e}")
            log_result(results, test_name, model, prompt, elapsed, "$0.007", [], str(e))


# ─── Test 3: FLUX Control LoRA Depth ($0.04/MP) ──────────────────────────────
def test_flux_depth(image_url: str, results: list):
    """FLUX depth control — structural generation with depth map."""
    test_name = "03_flux_depth"
    model = "fal-ai/flux-control-lora-depth"
    print(f"\n{'='*60}")
    print(f"TEST 3: FLUX Control LoRA Depth")
    print(f"Model: {model}")
    print(f"{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-50:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "control_lora_image_url": image_url,
                    "image_size": "square_hd",
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_result_image(url, test_name, i * 10 + j)
            log_result(results, test_name, model, prompt, elapsed, "$0.04", urls)
            print(f"  Done in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e}")
            log_result(results, test_name, model, prompt, elapsed, "$0.04", [], str(e))


# ─── Test 4: FLUX Control LoRA Canny ($0.04/MP) ──────────────────────────────
def test_flux_canny(image_url: str, results: list):
    """FLUX canny control — edge-based structural generation."""
    test_name = "04_flux_canny"
    model = "fal-ai/flux-control-lora-canny"
    print(f"\n{'='*60}")
    print(f"TEST 4: FLUX Control LoRA Canny")
    print(f"Model: {model}")
    print(f"{'='*60}")

    for i, prompt in enumerate(SCENE_PROMPTS):
        print(f"\n  Prompt {i+1}/3: ...{prompt[-50:]}")
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "control_lora_image_url": image_url,
                    "image_size": "square_hd",
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            for j, url in enumerate(urls):
                save_result_image(url, test_name, i * 10 + j)
            log_result(results, test_name, model, prompt, elapsed, "$0.04", urls)
            print(f"  Done in {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR: {e}")
            log_result(results, test_name, model, prompt, elapsed, "$0.04", [], str(e))


# ─── Test 5: Era 3D Multiview (FREE) ─────────────────────────────────────────
def test_era3d(image_url: str, results: list):
    """Era 3D — generate multiviews from single image. Free!"""
    test_name = "05_era3d"
    model = "fal-ai/era-3d"
    print(f"\n{'='*60}")
    print(f"TEST 5: Era 3D Multiview")
    print(f"Model: {model}")
    print(f"{'='*60}")

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_url": image_url,
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        elapsed = time.time() - t0

        # Era 3D returns multiview images and normal maps
        urls = []
        out_dir = OUTPUT_DIR / test_name
        out_dir.mkdir(parents=True, exist_ok=True)

        # Check various possible output formats
        if "images" in result:
            for j, img in enumerate(result["images"]):
                url = img["url"] if isinstance(img, dict) else img
                urls.append(url)
                save_result_image(url, test_name, j)
        if "mesh" in result:
            mesh_url = result["mesh"].get("url", "") if isinstance(result["mesh"], dict) else result["mesh"]
            if mesh_url:
                urls.append(mesh_url)
                import httpx
                resp = httpx.get(mesh_url)
                mesh_path = out_dir / "kepler_era3d.glb"
                mesh_path.write_bytes(resp.content)
                print(f"  Saved mesh: {mesh_path.name}")

        log_result(results, test_name, model, "multiview from A-pose", elapsed, "FREE", urls)
        print(f"  Done in {elapsed:.1f}s — {len(urls)} outputs")
        # Log full result keys for debugging
        print(f"  Result keys: {list(result.keys())}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR: {e}")
        log_result(results, test_name, model, "multiview from A-pose", elapsed, "FREE", [], str(e))


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("EXPERIMENT 9 — Phase 1: fal.ai Kepler Pipeline")
    print(f"Input: {KEPLER_IMAGE}")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set. Check .env.local")
        sys.exit(1)

    # Upload input image once
    image_url = upload_image(KEPLER_IMAGE)

    results = []

    # Run tests in order of cost (cheapest first)
    test_era3d(image_url, results)           # FREE
    test_minimax_subject(image_url, results)  # $0.01/img
    test_zimage_controlnet(image_url, results)  # $0.0065/MP
    test_flux_depth(image_url, results)       # $0.04/MP
    test_flux_canny(image_url, results)       # $0.04/MP

    # Summary
    print(f"\n{'='*60}")
    print(f"PHASE 1 COMPLETE")
    print(f"{'='*60}")
    total_tests = len(results)
    errors = sum(1 for r in results if r.get("error"))
    print(f"Tests: {total_tests}, Errors: {errors}")
    print(f"Results: {RESULTS_FILE}")
    print(f"Images: {OUTPUT_DIR}")

    for r in results:
        status = "FAIL" if r.get("error") else "OK"
        print(f"  [{status}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
