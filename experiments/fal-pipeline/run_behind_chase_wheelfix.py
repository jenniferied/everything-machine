#!/usr/bin/env python3
"""
behind_chase neu generieren mit ruhigerem Lenkrad.
Basis: PROMPT_A_FIX aus run_behind_chase_parallel.py, Lenkrad-Stelle verstaerkt
(positiv formuliert, kein Negativ-Anchoring). Diesmal MIT festem Seed pro Take,
2 Takes parallel mit verschiedenen Seeds -> bestes picken.
Model: Seedance 1.0 Pro, ~1,49 $ je Take (~3 $ gesamt).
"""
import os, json, time
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

import fal_client, httpx

SD = Path(__file__).parent
RECOLOR = SD / "outputs" / "behind_chase_recolor"
OUT = SD / "outputs" / "behind_chase_wheelfix"
RESULTS = SD / "behind_chase_wheelfix_results.json"
ENDPOINT = "fal-ai/bytedance/seedance/v1/pro/image-to-video"

# PROMPT_A_FIX, aber die Fahrer-/Lenkrad-Stelle verstaerkt: Haende halten das
# Lenkrad fest und gerade, Lenkrad bleibt ruhig und mittig (positiv).
PROMPT = (
    "A bordeaux-red voxel-block convertible Cadillac drives steadily forward "
    "down an empty desert road at night. The car drives forward and "
    "gradually recedes into the distance, getting smaller as it moves away "
    "from the static camera position behind it. The road has two lanes "
    "separated by a single white dashed center line; the car cruises in the "
    "right lane. Sandy desert shoulders with brush and rocks stretch out on "
    "both sides. The asphalt and the dashed white line flow past from the "
    "far horizon toward the bottom of the frame, the natural look of "
    "driving forward at steady highway speed. The red tail lights glow "
    "calmly. The full moon stays high in the starry sky, the moon and "
    "night sky remain pale and naturalistic with only a gentle hint of "
    "violet in the air. Distant mountains stay still on the horizon. The "
    "camera is positioned behind the car at road level with a locked, "
    "steady framing — no zoom, no pan, no tilt. "
    "The driver behind the wheel is a small voxel character: his head is a "
    "tight cluster of small cubic voxel blocks in light grey and white, "
    "Minecraft-style pixel-art geometry, hard edges and visible cubic "
    "facets. A dark navy baseball cap with a flat curved brim sits firmly "
    "on top of his head; small brown voxel hair blocks peek out from under "
    "the cap. He sits perfectly still and calm. Both of his blocky voxel "
    "hands grip the steering wheel firmly and keep it held straight and "
    "centered, steering smoothly straight ahead; the steering wheel stays "
    "steady and centered, the hands and arms remain calm and relaxed the "
    "whole time, holding the wheel in one fixed position. The cap and the "
    "cubic voxel texture of his head stay exactly the same throughout the "
    "entire shot. "
    "Cinematic moonlit night. The bordeaux car body keeps its rich "
    "aged-wine burgundy color throughout."
)

TAKES = [
    {"tag": "wheelfix_s1", "seed": 7001},
    {"tag": "wheelfix_s2", "seed": 7002},
]
ARGS = {"duration": "12", "resolution": "1080p", "camera_fixed": True}


def latest_start() -> Path:
    c = sorted(RECOLOR.glob("behind_chase_landstrasse_*.png"))
    if not c:
        raise FileNotFoundError("kein behind_chase_landstrasse_*.png")
    return c[-1]


def vid_url(r):
    v = r.get("video")
    if isinstance(v, dict): return v.get("url", "")
    if isinstance(v, str): return v
    return ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY fehlt"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = latest_start()
    print("=" * 60)
    print(f"BEHIND-CHASE WHEELFIX | Seedance 1.0 Pro | {stamp}")
    print(f"Startbild: {src.name} | 2 Takes parallel | est ~3 $")
    print("=" * 60)
    print("  upload...")
    image_url = fal_client.upload_file(str(src))
    print(f"  -> {image_url}")

    handles = {}
    for t in TAKES:
        args = {"image_url": image_url, "prompt": PROMPT, "seed": t["seed"], **ARGS}
        handles[t["tag"]] = (fal_client.submit(ENDPOINT, arguments=args), t["seed"])
        print(f"  submitted {t['tag']} (seed={t['seed']})")

    records = []
    for tag, (h, seed) in handles.items():
        print(f"\n  warte auf {tag}...")
        t0 = time.time()
        try:
            res = h.get()
            el = time.time() - t0
            url = vid_url(res)
            saved = None
            if url:
                p = OUT / f"behind_chase_{tag}_{stamp}.mp4"
                p.write_bytes(httpx.get(url, timeout=900, follow_redirects=True).content)
                saved = p.name
                print(f"    OK {el:.0f}s -> {saved} ({p.stat().st_size//1024}KB)")
            else:
                print(f"    WARN keine URL keys={list(res.keys())}")
            records.append({"tag": tag, "seed_in": seed,
                            "seed_returned": res.get("seed"), "saved": saved,
                            "elapsed_s": round(el, 1), "output_url": url})
        except Exception as e:
            print(f"    ERROR {tag}: {e}")
            records.append({"tag": tag, "seed_in": seed, "error": str(e)})
    RESULTS.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
