#!/usr/bin/env python3
"""
Slight edits via flux-pro/kontext/max (behält den Rest faithful):
- CD: Basis = scharfer og-9:16-Crop (1080x1920). Edit: Boden unter der CD zu.
- Stairs: Basis = stairs_kepler_1. Edit: Cap auf dunkles Navy + braune Haare
  (passend zur kepler-a-pose).
Je 2 Varianten. Final auf exakt 1080x1920 normalisiert (9:16, 1920 hoch).
~0,3 $.
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
OUT = SD / "outputs" / "input_edit_v4"
KONTEXT = "fal-ai/flux-pro/kontext/max"

CD_BASE = SD/"outputs/schminkspiegel_9x16/_inputprep/chosen_9x16_1080x1920.png"
STAIRS_BASE = SD/"outputs/input_prep_v3/stairs_kepler_1_20260618_233331.png"

CD_PROMPT = (
    "Close the bottom of the compact case beneath the round holographic disc, so "
    "the disc rests inside a solid closed chrome compact base with no see-through "
    "gap or hole underneath it; the lower half is a solid polished chrome casing. "
    "Keep absolutely everything else identical: the chrome mirror-finish hand, the "
    "chrome reflected face with red lips, the holographic disc, the dark blue starry "
    "galaxy background and all colors and framing."
)
STAIRS_PROMPT = (
    "Recolor only the character's cap to a dark navy blue baseball cap with a flat "
    "curved brim, with a little brown hair showing underneath the cap brim. Keep "
    "absolutely everything else identical: the voxel-block character and pose, the "
    "glowing white spiral staircase, the clouds, the cosmic galaxy background and all "
    "other colors."
)

JOBS = [
    {"name": "cd_closed_k", "base": CD_BASE, "prompt": CD_PROMPT},
    {"name": "stairs_capfix_k", "base": STAIRS_BASE, "prompt": STAIRS_PROMPT},
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
        if not Path(job["base"]).exists():
            print(f"  ERROR Basis fehlt {job['base']}"); recs.append({"name":job["name"],"error":"base missing"}); continue
        url = fal_client.upload_file(str(job["base"]))
        try:
            res = fal_client.subscribe(KONTEXT, arguments={
                "image_url": url, "prompt": job["prompt"], "aspect_ratio": "9:16",
                "num_images": 2, "guidance_scale": 3.5, "safety_tolerance": "5"})
            saved=[]
            for i,u in enumerate(img_urls(res)):
                raw = OUT/f"{job['name']}_{i}_{stamp}_raw.png"
                raw.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
                fin = OUT/f"{job['name']}_{i}_{stamp}.png"
                ff(["-i",str(raw),"-vf","scale=1080:1920:flags=lanczos",str(fin)])
                saved.append(fin.name)
                print(f"  saved {fin.name} (1080x1920)")
            recs.append({"name":job["name"],"saved":saved})
        except Exception as e:
            print(f"  ERROR {job['name']}: {e}"); recs.append({"name":job["name"],"error":str(e)})
    (SD/"inputedit_v4_results.json").write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
