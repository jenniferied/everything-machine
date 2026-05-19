#!/usr/bin/env python3
"""
Planet landscape plate — three current-gen image models at 16:9.
Inspiration: No Man's Sky aesthetic (not named in prompt — trademark risk).
Models: Nano Banana 2, Seedream 4.0, Flux 2 Pro. Estimated total: ~$0.14.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "planet_landscape"
RESULTS_FILE = SCRIPT_DIR / "planet_landscape_results.json"

PROMPT = (
    "Vibrant alien exoplanet landscape, rolling hills of magenta and violet grass, "
    "bioluminescent mushroom-like flora glowing softly, towering crystalline rock "
    "formations reflecting light, two massive moons low on the horizon, gradient "
    "cyan-to-orange sky with swirling nebula clouds, distant asteroid belt visible, "
    "geometric alien structures silhouetted far in the distance, sci-fi exploration "
    "atmosphere, saturated colors, cel-shaded painterly style, cinematic wide "
    "composition, no characters, environment only, 16:9 landscape."
)

MODELS = [
    {
        "name": "nano_banana_2",
        "endpoint": "fal-ai/nano-banana-2",
        "cost_est": "$0.08",
        "args": {
            "aspect_ratio": "16:9",
            "resolution": "1K",
            "num_images": 1,
        },
    },
    {
        "name": "seedream_v4",
        "endpoint": "fal-ai/bytedance/seedream/v4/text-to-image",
        "cost_est": "$0.03",
        "args": {
            "image_size": "landscape_16_9",
            "num_images": 1,
        },
    },
    {
        "name": "flux_2_pro",
        "endpoint": "fal-ai/flux-2-pro",
        "cost_est": "$0.03",
        "args": {
            "image_size": "landscape_16_9",
            "safety_tolerance": "5",
        },
    },
]

results = []


def load_existing_results():
    global results
    if RESULTS_FILE.exists():
        results = json.loads(RESULTS_FILE.read_text())
        print(f"  Loaded {len(results)} existing results")


def already_done(name):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        if (OUTPUT_DIR / f"{name}{ext}").exists():
            if any(r["test"] == name and not r.get("error") for r in results):
                return True
    return False


def save_image(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".png"
    if ".jpg" in url.lower() or ".jpeg" in url.lower():
        ext = ".jpg"
    elif ".webp" in url.lower():
        ext = ".webp"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=120)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def log(test, model, elapsed, cost, image_url, error=None):
    results.append({
        "test": test,
        "model": model,
        "prompt": PROMPT[:120],
        "elapsed_s": round(elapsed, 1),
        "cost_est": cost,
        "image": image_url,
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


def extract_image_url(result):
    if isinstance(result.get("images"), list) and result["images"]:
        first = result["images"][0]
        if isinstance(first, dict):
            return first.get("url", "")
        if isinstance(first, str):
            return first
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    if isinstance(result.get("image"), str):
        return result["image"]
    for key in ("output", "data"):
        val = result.get(key)
        if isinstance(val, dict):
            url = val.get("url") or (val.get("images", [{}])[0].get("url") if isinstance(val.get("images"), list) else "")
            if url:
                return url
    return ""


def run_model(model_cfg):
    name = model_cfg["name"]
    endpoint = model_cfg["endpoint"]

    if already_done(name):
        print(f"\n  {name} | SKIP (already done)")
        return

    print(f"\n  {name} | {endpoint} | {model_cfg['cost_est']}")

    args = {"prompt": PROMPT}
    args.update(model_cfg["args"])

    t0 = time.time()
    try:
        result = fal_client.subscribe(
            endpoint,
            arguments=args,
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0

        image_url = extract_image_url(result)
        if image_url:
            save_image(image_url, name)
            log(name, endpoint, elapsed, model_cfg["cost_est"], image_url)
            print(f"    OK in {elapsed:.1f}s")
        else:
            print(f"    WARNING: No image URL. Keys: {list(result.keys())}")
            log(name, endpoint, elapsed, model_cfg["cost_est"], "",
                f"No image URL. Response keys: {list(result.keys())}")

    except Exception as e:
        elapsed = time.time() - t0
        print(f"    ERROR ({elapsed:.1f}s): {e}")
        log(name, endpoint, elapsed, model_cfg["cost_est"], "", str(e))


def main():
    import sys
    only = set(sys.argv[1:])

    print("=" * 60)
    print("PLANET LANDSCAPE — 3 current-gen image models at 16:9")
    if only:
        print(f"Retrying: {', '.join(only)}")
    total_cost = sum(
        float(m["cost_est"].replace("$", ""))
        for m in MODELS
        if not only or m["name"] in only
    )
    print(f"Models: {len(MODELS) if not only else len(only)} | Estimated total: ${total_cost:.2f}")
    print(f"Prompt: {PROMPT[:90]}...")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    load_existing_results()

    for model_cfg in MODELS:
        if only and model_cfg["name"] not in only:
            continue
        run_model(model_cfg)

    print(f"\n{'='*60}\nPLANET LANDSCAPE COMPLETE\n{'='*60}")
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    ok_count = total - errors
    print(f"Total results: {total} | OK: {ok_count} | Errors: {errors}")
    for r in results:
        status = "FAIL" if r.get("error") else "OK"
        print(f"  [{status}] {r['test']} — {r['elapsed_s']}s — {r['cost_est']}")


if __name__ == "__main__":
    main()
