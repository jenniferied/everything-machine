#!/usr/bin/env python3
"""
Neues behind_chase Input-Bild via nano-banana-pro/edit Fusion:
Szene (landstrasse) + kepler-a-pose (Fahrer) + sauberes Kennzeichen.
-> scharfes vertikales 9:16, saubere Straße, on-model Fahrer, klares Schild.
2 Varianten. ~0,3 $.
"""
import os, json
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
OUT = SD / "outputs" / "input_prep_v3"
EDIT = "fal-ai/nano-banana-pro/edit"

SCENE = SD/"outputs/behind_chase_recolor/behind_chase_landstrasse_20260527_104711.png"
KEPLER = SD/"inputs/kepler-a-pose-portrait-padded.png"
PLATE = SD/"inputs/sie-schreibt/kennzeichen-kep-le-18.png"

PROMPT = (
    "Create a vertical 9:16 night scene. Use the FIRST image for the composition and "
    "grading: a bordeaux-red voxel-block convertible Cadillac seen from directly "
    "behind, driving away down an empty two-lane desert highway, a big full moon high "
    "in a starry sky, distant mountains on the horizon, cinematic moonlit night with a "
    "gentle violet hint. Seat the voxel-block character from the SECOND image in the "
    "driver seat, on-model: blocky light-grey and white Minecraft-style voxel head and "
    "body with hard cubic facets and a dark navy flat-brim baseball cap. On the rear of "
    "the car, render the license plate exactly like the THIRD image: a clean white "
    "German plate reading 'KEP-LE 18' with the blue EU 'D' strip and the round emblems, "
    "crisp and sharp with no artifacts. The two-lane desert road has a single clean "
    "white dashed center line running naturally to the horizon, clean and undistorted "
    "in the foreground. Keep the bordeaux burgundy car color. Sharp, crisp, high detail."
)


def img_urls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    elif isinstance(r.get("image"),dict): out.append(r["image"].get("url",""))
    return [u for u in out if u]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY fehlt"); return
    for p in (SCENE, KEPLER, PLATE):
        if not Path(p).exists(): print(f"ERROR fehlt {p}"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    urls = [fal_client.upload_file(str(p)) for p in (SCENE, KEPLER, PLATE)]
    print("fusion läuft...")
    res = fal_client.subscribe(EDIT, arguments={
        "image_urls": urls, "prompt": PROMPT, "aspect_ratio": "9:16", "num_images": 2})
    saved=[]
    for i,u in enumerate(img_urls(res)):
        p = OUT/f"behind_kepler_{i}_{stamp}.png"
        p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
        saved.append(p.name); print(f"  saved {p.name}")
    (SD/"behind_input_v3_results.json").write_text(json.dumps({"saved":saved},indent=2))
    print(f"DONE -> {OUT}")


if __name__ == "__main__":
    main()
