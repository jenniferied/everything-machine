#!/usr/bin/env python3
"""
Upscale the latest spiral_softglow_16x9 image with 3 different upscalers.
Outputs timestamped — never overwrites.
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
IMG_DIR = SCRIPT_DIR / "outputs" / "spiral_neon"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "spiral_upscale"
RESULTS_FILE = SCRIPT_DIR / "spiral_upscale_results.json"


def latest_input() -> Path:
    candidates = sorted(IMG_DIR.glob("spiral_softglow_16x9_*.png"))
    if not candidates:
        raise FileNotFoundError("No spiral_softglow_16x9_*.png in outputs/spiral_neon/")
    return candidates[-1]


CONTEXT_PROMPT = (
    "Voxel character with a flat baseball cap walking up a softly glowing spiral "
    "staircase in deep space. Stars, galaxies, soft clouds in the background. "
    "Cosmic blue/purple color grading."
)

MODELS = [
    {
        "name": "clarity",
        "endpoint": "fal-ai/clarity-upscaler",
        "args": {
            "upscale_factor": 2,
            "creativity": 0.25,
            "resemblance": 1.0,
            "prompt": CONTEXT_PROMPT,
            "negative_prompt": "blur, low quality, jpeg artifacts, compression, face features, eyes, mouth",
        },
        "cost_est": "$0.04",
    },
    {
        "name": "ccsr",
        "endpoint": "fal-ai/ccsr",
        "args": {"scale": 2},
        "cost_est": "$0.05",
    },
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_image(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url.lower() or "jpeg" in url.lower()) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=300, follow_redirects=True)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def extract_url(result):
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    if isinstance(result.get("image"), str):
        return result["image"]
    if isinstance(result.get("images"), list) and result["images"]:
        first = result["images"][0]
        if isinstance(first, dict):
            return first.get("url", "")
        if isinstance(first, str):
            return first
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
    src = latest_input()
    print("=" * 60)
    print(f"UPSCALE TEST | run {stamp}")
    print(f"Source: {src.name}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(src)

    for cfg in MODELS:
        name = cfg["name"]
        print(f"\n  {name} | {cfg['endpoint']} | est {cfg['cost_est']}")
        args = {"image_url": image_url, **cfg["args"]}
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                cfg["endpoint"], arguments=args,
                with_logs=True, on_queue_update=on_queue,
            )
            elapsed = time.time() - t0
            out_url = extract_url(result)
            saved = None
            if out_url:
                p = save_image(out_url, f"spiral_upscale_{name}_{stamp}")
                saved = p.name
                print(f"    OK in {elapsed:.1f}s")
            else:
                print(f"    WARNING: no URL. keys={list(result.keys())}")
            append_record({
                "run": stamp, "model": name, "endpoint": cfg["endpoint"],
                "args": cfg["args"], "input": src.name,
                "elapsed_s": round(elapsed, 1), "cost_est": cfg["cost_est"],
                "output_url": out_url, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"    ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "model": name, "endpoint": cfg["endpoint"],
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "cost_est": cfg["cost_est"], "timestamp": datetime.now().isoformat(),
            })

    print(f"\n{'='*60}\nDONE — outputs in {OUTPUT_DIR}\n{'='*60}")


if __name__ == "__main__":
    main()
