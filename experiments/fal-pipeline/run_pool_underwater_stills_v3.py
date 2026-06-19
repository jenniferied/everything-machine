#!/usr/bin/env python3
"""
Unterwasser-Stills v3 — komplett andere Prompt-Ansaetze.

v1/v2 Probleme: das Modell versteht "auf dem Ring liegen, von unten
fotografiert" nicht zuverlaessig — egal wie detailliert die Physik
beschrieben war. Hier drei radikal verschiedene Prompt-Strategien:

  S1 SPLIT-LEVEL — als klassisches Foto beschrieben:
     "iconic over-under split-level shot, horizon line cuts the frame
     across the middle, top half above water shows character, bottom
     half below water shows submerged ring half + legs"
  S2 MINIMAL PHOTO-REF — extrem knapp, photography-Sprache:
     "Underwater photo, snorkeler-POV looking up at someone floating
     on a pool tube above"
  S3 STARK STILISIERT — als Voxel-Game-Render beschrieben statt
     Foto, mit klarer 3D-Engine-Bildsprache

3 Bilder, alle NanoBanana Pro (Pool-Champion). ~$0.12.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_underwater"
RESULTS_FILE = SCRIPT_DIR / "pool_underwater_results.json"
SOURCE = SCRIPT_DIR / "outputs" / "pool_badehose" / "A_v6_run3_20260527_104322.png"

MODEL = "fal-ai/nano-banana-pro/edit"

PROMPTS = {
    "S1_splitlevel": (
        "Iconic OVER-UNDER SPLIT-LEVEL underwater photograph of this "
        "voxel / lego-block pool scene. The horizon-like WATERLINE cuts "
        "across the middle of the frame as a clear wavy horizontal line "
        "that divides the image in two:\n"
        "TOP HALF (above water, in air): the voxel character lying "
        "relaxed across the TOP of the gold inflatable ring — torso, "
        "arms, dark CAP and featureless white face MASK clearly visible "
        "in the bright sunny air. Pool deck and palm-leaf shadows in "
        "the background.\n"
        "BOTTOM HALF (underwater, submerged): we see the SUBMERGED "
        "BOTTOM HALF of the gold inflatable ring pressing into the "
        "water from above, the character's voxel LEGS and bare voxel "
        "FEET hanging down into the turquoise water, his pink-and-white "
        "Hawaiian swim trunks straddling the waterline, GOD-RAY "
        "sunbeams piercing down through the rippling surface, caustic "
        "patterns shimmering on the pool floor below, air bubbles "
        "rising. The waterline is the visual centre of the composition.\n"
        "Voxel / lego-block art style throughout. No facial features on "
        "the white mask. Cinematic 16:9."
    ),
    "S2_minimal": (
        "Underwater photograph. Snorkeler point of view looking UP from "
        "below the water surface at a person floating ABOVE on a gold "
        "pool ring. We see the underside of the inflatable ring "
        "pressing into the rippling water surface, the person's "
        "submerged legs and feet dangling down into the turquoise "
        "water, and the silhouette of their torso visible refracted "
        "through the wavy surface above. Strong sunbeams, bubbles, "
        "caustics on pool floor. Voxel / lego-block art style. The "
        "person wears pink-and-white Hawaiian swim trunks and a dark "
        "cap with a white blank face mask. 16:9 cinematic."
    ),
    "S3_voxel_render": (
        "Voxel-engine 3D render of a swimming pool, isometric-feeling "
        "low-angle UNDERWATER CAMERA SHOT inside the pool's volume. "
        "Composition: in the upper portion of the frame, the wavy "
        "turquoise water surface forms a ceiling; pushing through that "
        "ceiling from above is the gold cubic-voxel pool ring — its "
        "lower half is below the surface and clearly visible, its "
        "upper half breaks above the surface. Lying across the top of "
        "the ring above the waterline: the lego-block character with "
        "pink-and-white Hawaiian voxel trunks, dark voxel cap and "
        "featureless white voxel face mask. His blocky legs hang DOWN "
        "INTO the water below the ring, visible to the camera. "
        "Volumetric god-rays pierce down through the surface, caustic "
        "voxel patterns dance on the pool floor below. Bubbles drift "
        "up. 16:9, clean voxel aesthetic, vivid summer palette."
    ),
}


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url: str, name: str) -> Path | None:
    if not url:
        return None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=180, follow_redirects=True)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def first_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
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


def run(label: str, prompt: str, src_url: str, name: str, stamp: str):
    print(f"\n--- {label} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "image_urls": [src_url], "prompt": prompt,
                "aspect_ratio": "16:9", "num_images": 1,
            },
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, f"{name}_{stamp}")
        append_record({
            "run": stamp, "label": label, "model": MODEL,
            "prompt_strategy": label, "prompt": prompt,
            "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "image": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": label, "model": MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"UW STILLS v3 | 3 verschiedene Prompt-Ansaetze | {stamp} | ~$0.12")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)
    for key, prompt in PROMPTS.items():
        run(key, prompt, src_url, f"uw3_{key}", stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
