#!/usr/bin/env python3
"""
Generate an end-frame variant of the latest spiral_softglow image: same scene,
same character, same cap — only the character is several steps further up the
staircase. Output is timestamped and saved as spiral_softglow_endframe_*.png.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "spiral_neon"
RESULTS_FILE = SCRIPT_DIR / "spiral_neon_results.json"


def latest_softglow() -> Path:
    candidates = sorted(OUTPUT_DIR.glob("spiral_softglow_16x9_*.png"))
    if not candidates:
        raise FileNotFoundError("No spiral_softglow_16x9_*.png yet")
    return candidates[-1]


PROMPT = (
    "Edit this image. Keep EVERYTHING identical — same composition, same camera angle, "
    "same staircase, same cosmic background, same color grading, same character with the "
    "same baseball cap and same white shoes. "
    "ONLY change: the voxel character has climbed a clear distance further up the spiral "
    "staircase — noticeably higher than in the source, but not at the very top yet. "
    "He is shown FROM BEHIND, his back facing the camera, walking away upward into the "
    "spiral. The cap is seen from behind. Calm, small natural walking step — NOT a wide "
    "stride. The character must remain faceless, same outfit, same cap shape — no morphing "
    "of cap, no added face features. Aspect ratio stays 16:9 landscape."
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    url = fal_client.upload_file(str(path))
    print(f"  -> {url}")
    return url


def save_image(url: str, name: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=120)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for e in update.logs:
            msg = e.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(rec):
    existing = []
    if RESULTS_FILE.exists():
        try:
            existing = json.loads(RESULTS_FILE.read_text())
        except Exception:
            existing = []
    existing.append(rec)
    RESULTS_FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = latest_softglow()
    print("=" * 60)
    print(f"END-FRAME GEN | run {stamp}")
    print(f"Source: {src.name}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    image_url = upload(src)
    model = "fal-ai/nano-banana-pro/edit"

    print(f"\n  {model} | aspect_ratio=16:9")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_urls": [image_url],
                "prompt": PROMPT,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        saved = []
        for i, u in enumerate(urls):
            suffix = "" if i == 0 else f"_{i}"
            name = f"spiral_softglow_endframe_{stamp}{suffix}"
            p = save_image(u, name)
            saved.append(p.name)
        append_record({
            "run": stamp, "kind": "endframe", "model": model, "prompt": PROMPT,
            "aspect_ratio": "16:9", "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.15", "images": urls, "saved": saved,
            "input": src.name, "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s — {saved}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")


if __name__ == "__main__":
    main()
