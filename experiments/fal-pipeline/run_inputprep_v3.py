#!/usr/bin/env python3
"""
Neue Input-Bilder (nur Bilder, billig) via nano-banana-pro/edit:
1) CD: dd_flux editieren -> Boden unter CD zu (kein Durchsicht-Loch), etwas
   rauszoomen, vertikal 9:16.
2) Treppe: Szene (spiral_softglow) + kepler-a-pose-Figur fusionieren -> scharfe
   vertikale 9:16 Treppen-Szene, Figur on-model.
Je 2 Varianten. ~0,3 $.
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
OUT = SD / "outputs" / "input_prep_v3"
EDIT = "fal-ai/nano-banana-pro/edit"

CD_SRC = SD / "outputs" / "schminkspiegel_dedot2" / "dd_flux_20260602_150012.jpg"
SPIRAL_SCENE = SD / "outputs" / "spiral_neon" / "spiral_softglow_16x9_20260512_220408.png"
KEPLER = SD / "inputs" / "kepler-a-pose-portrait-padded.png"

CD_PROMPT = (
    "Edit this image. Keep everything exactly the same: the chrome mirror-finish "
    "hand, the chrome reflected face in the open compact mirror (smooth seamless "
    "chrome showing only a subtle nose, closed red lips and chin, the upper face "
    "smooth featureless chrome), the round holographic rainbow disc, the dark blue "
    "starry galaxy background and cosmic color grading. Make two changes only: "
    "1) Close the bottom of the compact under the disc — the disc rests inside a "
    "solid closed chrome compact case, the lower half a solid chrome casing with no "
    "see-through gap or hole beneath the disc. "
    "2) Zoom out a little so a bit more of the chrome hand and the full compact are "
    "visible with more space around them. Vertical 9:16 framing."
)

STAIRS_PROMPT = (
    "Create a vertical 9:16 image of a luminous spiral staircase in deep space. "
    "Use the FIRST image for the scene and grading: the glowing warm-white spiral "
    "staircase whose steps emit soft, even light from within like frosted glass lit "
    "from inside, soft white clouds, a dreamy dark blue and purple cosmic galaxy "
    "background full of stars. Place the voxel-block character from the SECOND image "
    "standing mid-climb on the staircase, fully on-model: blocky light-grey and white "
    "Minecraft-style voxel body with hard cubic facets, a dark navy baseball cap with "
    "a flat brim, dark trousers, white shoes. Tall vertical composition that "
    "emphasises the staircase spiralling upward into the distance. Sharp, crisp, high "
    "detail."
)

JOBS = [
    {"name": "cd_closed", "image_urls": [CD_SRC], "prompt": CD_PROMPT},
    {"name": "stairs_kepler", "image_urls": [SPIRAL_SCENE, KEPLER], "prompt": STAIRS_PROMPT},
]


def img_urls(r):
    out = []
    if isinstance(r.get("images"), list):
        for f in r["images"]:
            out.append(f.get("url","") if isinstance(f, dict) else f)
    elif isinstance(r.get("image"), dict):
        out.append(r["image"].get("url",""))
    return [u for u in out if u]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY fehlt"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recs = []
    for job in JOBS:
        print("="*60); print(job["name"])
        for src in job["image_urls"]:
            if not Path(src).exists():
                print(f"  ERROR fehlt: {src}")
        urls = [fal_client.upload_file(str(p)) for p in job["image_urls"]]
        args = {"image_urls": urls, "prompt": job["prompt"],
                "aspect_ratio": "9:16", "num_images": 2}
        try:
            res = fal_client.subscribe(EDIT, arguments=args, with_logs=False)
            outs = img_urls(res)
            saved = []
            for i, u in enumerate(outs):
                p = OUT / f"{job['name']}_{i}_{stamp}.png"
                p.write_bytes(httpx.get(u, timeout=300, follow_redirects=True).content)
                saved.append(p.name)
                print(f"  saved {p.name}")
            recs.append({"name": job["name"], "saved": saved})
        except Exception as e:
            print(f"  ERROR {job['name']}: {e}")
            recs.append({"name": job["name"], "error": str(e)})
    (SD / "inputprep_v3_results.json").write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
