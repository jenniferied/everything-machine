#!/usr/bin/env python3
"""
Input-Bilder v6 — nativ hochauflösend + ausgewogene Farben.
- nano-banana-pro/edit mit resolution="2K" (nativ ~1152x2048, >=1920 hoch, KEIN lanczos).
- Komposition der v5-Bilder als Referenz beibehalten.
- CD bekommt zusätzlich rb_M3_nano2ref als FARB-Referenz (poliertes Silber-Chrom,
  sanftes Blau-Lila, gedämpfte Lippen — geschmackvolles Mittelding statt grellem
  Elektroblau).
2 Varianten je. ~0,7 $.
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
OUT = SD / "outputs" / "input_v6"
NANO = "fal-ai/nano-banana-pro/edit"

CD_V5 = SD/"outputs/input_v5/cd_tray_0_20260618_234745.png"
RB_REF = SD/"outputs/schminkspiegel_recolor_berry/rb_M3_nano2ref_run1_20260602_123415.png"
STAIRS_V5 = SD/"outputs/input_v5/stairs_v5_1_20260618_234745.png"
STAIRS_V5_B = SD/"outputs/input_v5/stairs_v5_0_20260618_234745.png"
BEHIND_V5 = SD/"outputs/input_v5/behind_v5_0_20260618_234745.png"

CD_PROMPT = (
    "Keep the composition of the FIRST image exactly: the chrome mirror-finish hand, "
    "the chrome reflected face with lips, and especially the CD-player-style tray where "
    "the holographic disc rests on a central hub. Re-grade the colors to match the "
    "SECOND image: polished neutral SILVER chrome (not electric blue), a soft, balanced "
    "dark blue and purple cosmic background, muted berry-red lips, tasteful and "
    "well-balanced cinematic color, not oversaturated. Crisp high detail."
)
STAIRS_PROMPT = (
    "Keep this image's composition exactly: the glowing white spiral staircase, the "
    "voxel-block character (featureless white face, white visor brim, dark brown voxel "
    "hair on top — no cap), the clouds and the cosmic galaxy background. Enhance to "
    "crisp, sharp high detail. Tasteful, well-balanced, natural cinematic color grading, "
    "not oversaturated."
)
BEHIND_PROMPT = (
    "Keep this image's composition exactly: the bordeaux voxel-block Cadillac seen from "
    "behind, the clean desert highway with its dashed center line, the full moon, the "
    "mountains, the voxel driver and the clean license plate reading 'KEP-LE 18'. "
    "Enhance to crisp, sharp high detail. Tasteful, well-balanced, natural cinematic "
    "color grading, not oversaturated."
)

JOBS = [
    {"name": "cd_v6", "imgs": [CD_V5, RB_REF], "prompt": CD_PROMPT},
    {"name": "stairs_v6", "imgs": [STAIRS_V5], "prompt": STAIRS_PROMPT},
    {"name": "stairs_v6b", "imgs": [STAIRS_V5_B], "prompt": STAIRS_PROMPT},
    {"name": "behind_v6", "imgs": [BEHIND_V5], "prompt": BEHIND_PROMPT},
]


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
        try:
            res=fal_client.subscribe(NANO, arguments={"image_urls": urls,
                "prompt": job["prompt"], "aspect_ratio":"9:16",
                "resolution":"2K", "num_images":2})
            saved=[]
            for i,u in enumerate(img_urls(res)):
                p=OUT/f"{job['name']}_{i}_{stamp}.png"
                p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
                saved.append(p.name); print(f"  saved {p.name}")
            recs.append({"name":job["name"],"saved":saved})
        except Exception as e:
            print(f"  ERROR {job['name']}: {e}"); recs.append({"name":job["name"],"error":str(e)})
        (SD/"inputs_v6_results.json").write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
