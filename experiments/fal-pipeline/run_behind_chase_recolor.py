#!/usr/bin/env python3
"""
Behind-Chase Recolor — alternatives Startbild.

Nimmt das Plate-Edit-Bild
  outputs/behind_chase_plate/behind_chase_plate_20260522_171447.png
und faerbt den Cadillac in tiefes Vintage-Bordeauxrot um. Das Color
Grading der gesamten Szene geht leicht ins Lila/Violett (statt rein
kuehlblaues Mondlicht). Komposition, Kennzeichen 'KEP - LE 18', Mond,
Berge, Voxel-Charakter bleiben EXAKT erhalten.

Model: fal-ai/nano-banana-pro/edit  (~$0.04)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "behind_chase_recolor"
RESULTS_FILE = SCRIPT_DIR / "behind_chase_recolor_results.json"

REF_IMAGE = (
    SCRIPT_DIR / "outputs" / "behind_chase_plate"
    / "behind_chase_plate_20260522_171447.png"
)

PROMPT = (
    "Edit the image. KEEP EVERYTHING EXACTLY: the same composition, the "
    "same framing (camera directly behind the convertible Cadillac at road "
    "level), the full moon high in the starry sky, the distant mountains, "
    "the two-lane desert highway with its painted dashed center lines, the "
    "voxel character driver with his dark baseball cap and brown voxel hair, "
    "the rear license plate 'KEP - LE 18' (German plate with EU strip, TUV "
    "and NRW stickers — must stay sharp and legible), the red tail-light "
    "glow. Do NOT change pose, framing, plate, character, moon or mountains. "
    "Make ONLY these two color changes: "
    "1) Recolor the Cadillac's body paint to a deep VINTAGE BORDEAUX RED — "
    "rich and slightly desaturated, like aged wine or 1970s muscle-car "
    "burgundy. The car body, fenders and trunk lid are all this bordeaux "
    "red; chrome bumpers, tail lights and trim stay metallic / red as "
    "before. The voxel-block surface texture stays the same, only the hue "
    "is now bordeaux red. "
    "2) Shift the overall color grading of the scene slightly toward violet "
    "/ purple. Instead of the current cool-blue moonlight, the moonlight, "
    "the sky and the shadowed parts of the desert pick up a gentle purple "
    "/ magenta-violet cast. The grading should feel dreamy and night-club-"
    "moonlit, not garish — subtle violet, not neon. Tail-light amber stays "
    "warm against the violet ambient."
)

NEGATIVE_HINTS = (
    "Avoid: changing the framing, changing the plate text, distorted plate, "
    "blank plate, changing the character or his cap, fluorescent neon "
    "colors, oversaturated red, candy-apple red, fire-engine red, pink car, "
    "removing the moon, changing the mountains."
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


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
    print("=" * 60)
    print(f"BEHIND-CHASE RECOLOR (Bordeaux + Violett) | run {stamp} | ~$0.04")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert REF_IMAGE.exists(), f"missing: {REF_IMAGE}"

    print("\nUploading...")
    ref_url = upload(REF_IMAGE)

    model = "fal-ai/nano-banana-pro/edit"
    full_prompt = f"{PROMPT} {NEGATIVE_HINTS}"
    print(f"\n--- bordeaux_violet ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_urls": [ref_url],
                "prompt": full_prompt,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        saved = []
        for i, url in enumerate(urls):
            suffix = "" if i == 0 else f"_{i}"
            saved.append(str(save_image(url, f"behind_chase_bordeaux_{stamp}{suffix}").name))
        append_record({
            "run": stamp, "model": model, "prompt": full_prompt,
            "refs": [REF_IMAGE.name], "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1),
            "images": urls, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": model, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
