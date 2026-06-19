#!/usr/bin/env python3
"""
Input-Bilder v5 — Korrekturen:
- CD (kontext, slight edit auf og-Crop): Unterteil als CD-PLAYER-TRAY, Disc sitzt
  sichtbar auf einem zentralen Hub/Spindel, rausnehmbar wie bei einem CD-Player.
  Disc bleibt holografisch. Rest identisch.
- Treppe (nano fusion): Szene + kepler-a-pose. Kopf = wie im a-pose-Bild: weißes
  Voxel-Gesicht, weißer Visor-Brim, dunkelbraunes Voxel-Haar oben. KEINE Navy-Cap.
- behind_chase (nano fusion): Szene + kepler (gleicher Kopf) + sauberes Schild.
Alle 9:16, final 1080x1920. ~0,6 $.
"""
import os, json, subprocess
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
OUT = SD / "outputs" / "input_v5"
NANO = "fal-ai/nano-banana-pro/edit"
KONTEXT = "fal-ai/flux-pro/kontext/max"

CD_BASE = SD/"outputs/schminkspiegel_9x16/_inputprep/chosen_9x16_1080x1920.png"
SPIRAL = SD/"outputs/spiral_neon/spiral_softglow_16x9_20260512_220408.png"
LANDSTR = SD/"outputs/behind_chase_recolor/behind_chase_landstrasse_20260527_104711.png"
KEPLER = SD/"inputs/kepler-a-pose-portrait-padded.png"
PLATE = SD/"inputs/sie-schreibt/kennzeichen-kep-le-18.png"

# Kopf-Beschreibung minimal + korrekt, primär übers Referenzbild:
HEAD = ("Render the character's head exactly like the reference: a blocky voxel head "
        "with a featureless white face, a white visor brim across the brow, and a "
        "cluster of dark brown voxel hair on top and back of the head — no cap, no navy.")

CD_PROMPT = (
    "Edit the lower half of the compact so it looks like a CD player tray: the round "
    "holographic disc rests on a central round hub/spindle inside a shallow circular "
    "tray, as if it can be lifted out or slotted in like a CD player. Keep the disc "
    "itself fully visible, holographic and rainbow-reflective — do not cover or fill "
    "it. Keep absolutely everything else identical: the chrome hand, the chrome "
    "mirror face with red lips, the dark blue galaxy background, colors and framing."
)
STAIRS_PROMPT = (
    "Create a vertical 9:16 image of a luminous spiral staircase in deep space. Use "
    "the FIRST image for the scene and grading: the glowing warm-white spiral "
    "staircase whose steps emit soft even light from within, soft white clouds, a "
    "dreamy dark blue and purple cosmic galaxy full of stars. Place the voxel-block "
    "character from the SECOND image standing mid-climb on the staircase, fully "
    f"on-model. {HEAD} Tall vertical composition emphasising the staircase spiralling "
    "upward. Sharp, crisp, high detail."
)
BEHIND_PROMPT = (
    "Create a vertical 9:16 night scene. Use the FIRST image for the composition and "
    "grading: a bordeaux-red voxel-block convertible Cadillac seen from directly "
    "behind, driving away down an empty two-lane desert highway, a big full moon high "
    "in a starry sky, distant mountains, cinematic moonlit night with a gentle violet "
    f"hint. Seat the voxel character from the SECOND image in the driver seat. {HEAD} "
    "On the rear of the car render the license plate exactly like the THIRD image: a "
    "clean white German plate reading 'KEP-LE 18' with the blue EU 'D' strip and the "
    "round emblems, crisp and sharp with no artifacts. The two-lane desert road has a "
    "single clean white dashed center line running naturally to the horizon, clean and "
    "undistorted in the foreground. Keep the bordeaux burgundy car color. Sharp, crisp."
)

JOBS = [
    {"name": "cd_tray", "endpoint": KONTEXT, "imgs": [CD_BASE], "prompt": CD_PROMPT,
     "extra": {"guidance_scale": 3.5, "safety_tolerance": "5"}},
    {"name": "stairs_v5", "endpoint": NANO, "imgs": [SPIRAL, KEPLER], "prompt": STAIRS_PROMPT, "extra": {}},
    {"name": "behind_v5", "endpoint": NANO, "imgs": [LANDSTR, KEPLER, PLATE], "prompt": BEHIND_PROMPT, "extra": {}},
]


def ff(a): subprocess.run(["ffmpeg","-y",*a,"-loglevel","error"], check=True)
def img_urls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    elif isinstance(r.get("image"),dict): out.append(r["image"].get("url",""))
    return [u for u in out if u]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY fehlt"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recs=[]
    for job in JOBS:
        print("="*60); print(job["name"])
        for p in job["imgs"]:
            if not Path(p).exists(): print(f"  ERROR fehlt {p}")
        urls=[fal_client.upload_file(str(p)) for p in job["imgs"]]
        args={"prompt": job["prompt"], "aspect_ratio":"9:16", "num_images":2, **job["extra"]}
        if job["endpoint"]==KONTEXT: args["image_url"]=urls[0]
        else: args["image_urls"]=urls
        try:
            res=fal_client.subscribe(job["endpoint"], arguments=args)
            saved=[]
            for i,u in enumerate(img_urls(res)):
                raw=OUT/f"{job['name']}_{i}_{stamp}_raw.png"
                raw.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
                fin=OUT/f"{job['name']}_{i}_{stamp}.png"
                ff(["-i",str(raw),"-vf","scale=1080:1920:flags=lanczos",str(fin)])
                saved.append(fin.name); print(f"  saved {fin.name}")
            recs.append({"name":job["name"],"saved":saved})
        except Exception as e:
            print(f"  ERROR {job['name']}: {e}"); recs.append({"name":job["name"],"error":str(e)})
        (SD/"inputs_v5_results.json").write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
