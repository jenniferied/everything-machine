#!/usr/bin/env python3
"""
Treppe + behind_chase hochkant — bewährte Methode:
Chosen-Input -> 9:16 croppen -> clarity-upscale auf 1080x1920 (scharfer Startframe)
-> Seedance i2v nativ 9:16 1080p mit dem funktionierenden Prompt. Je 2 Seeds.

- Treppe: Endless-Climb-Illusion (positiv, Figur tritt auf der Stelle, Spirale
  rotiert als starrer Block nach unten). Kamera fix.
- behind_chase: ORIGINALER A_fix-Prompt wortwörtlich (kopfstabil), Lenkrad-
  Wackeln minimal akzeptiert.
~5 $ gesamt.
"""
import os, json, time, subprocess
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
OUT = SD / "outputs" / "hd_vertical_v2"
TMP = OUT / "_inputprep"
RESULTS = SD / "deliver_vertical_v2_results.json"
SEEDANCE_PRO = "fal-ai/bytedance/seedance/v1/pro/image-to-video"
CLARITY = "fal-ai/clarity-upscaler"

STAIRS_PROMPT = (
    "Endless-climb illusion. The voxel character marches in place — his legs lift "
    "and step rhythmically, but his body stays exactly in the same spot in the frame. "
    "The ENTIRE spiral staircase rotates as one single rigid object around its central "
    "vertical axis. EVERY part of the staircase rotates uniformly at the same speed — "
    "the bottom steps, the middle steps, AND the upper part of the spiral disappearing "
    "into the distance — ALL rotate together as one unit, like a carousel or rotating "
    "sculpture. The whole spiral scrolls downward past the character, so it looks like "
    "he is endlessly ascending. The staircase glow stays constant. Stars and galaxies "
    "drift very slowly. Camera is completely static. He wears a baseball cap with a "
    "flat brim, the cap shape stays identical throughout."
)

BEHIND_PROMPT = (  # PROMPT_A_FIX wortwörtlich aus run_behind_chase_parallel.py
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
    "the cap. He sits still and steady, both blocky voxel hands on the "
    "wheel. The cap and the cubic voxel texture of his head stay exactly "
    "the same throughout the entire shot. "
    "Cinematic moonlit night. The bordeaux car body keeps its rich "
    "aged-wine burgundy color throughout."
)

JOBS = [
    {"name": "stairs", "endpoint": SEEDANCE_PRO,
     "src": SD/"outputs/spiral_neon/spiral_softglow_16x9_20260512_220408.png",
     "prompt": STAIRS_PROMPT, "duration": "10", "seeds": [9001, 9002]},
    {"name": "behind_chase", "endpoint": SEEDANCE_PRO,
     "src": SD/"outputs/behind_chase_recolor/behind_chase_landstrasse_20260527_104711.png",
     "prompt": BEHIND_PROMPT, "duration": "12", "seeds": [9101, 9102]},
]


def ff(a): subprocess.run(["ffmpeg","-y",*a,"-loglevel","error"], check=True)
def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
    "-show_entries","stream=width,height","-of","csv=p=0",str(p)],
    capture_output=True,text=True).stdout.strip()
def img_url(r):
    if isinstance(r.get("image"),dict): return r["image"].get("url","")
    if isinstance(r.get("images"),list) and r["images"]:
        f=r["images"][0]; return f.get("url","") if isinstance(f,dict) else f
    return ""
def vid_url(r):
    v=r.get("video")
    if isinstance(v,dict): return v.get("url","")
    if isinstance(v,str): return v
    return ""


def prep(src: Path, name: str) -> Path:
    TMP.mkdir(parents=True, exist_ok=True)
    w,h = map(int, dims(src).split(","))
    cw,ch = (int(h*9/16),h) if w/h>9/16 else (w,int(w*16/9))
    crop = TMP/f"{name}_crop.png"
    ff(["-i",str(src),"-vf",f"crop={cw}:{ch}:(in_w-{cw})/2:(in_h-{ch})/2",str(crop)])
    print(f"  [{name}] crop {w}x{h} -> {dims(crop)} ; clarity upscale...")
    curl = fal_client.upload_file(str(crop))
    res = fal_client.subscribe(CLARITY, arguments={"image_url":curl,"upscale_factor":3,
        "creativity":0.2,"resemblance":1.0,"prompt":"crisp clean cinematic, sharp detail",
        "negative_prompt":"blur, jpeg artifacts, compression"})
    up = TMP/f"{name}_up.png"
    up.write_bytes(httpx.get(img_url(res),timeout=300,follow_redirects=True).content)
    final = TMP/f"{name}_1080x1920.png"
    ff(["-i",str(up),"-vf","scale=1080:1920:flags=lanczos",str(final)])
    print(f"  [{name}] startframe -> {dims(final)}")
    return final


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY fehlt"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recs = []
    for job in JOBS:
        print("="*60); print(job["name"])
        if not Path(job["src"]).exists():
            print(f"  ERROR src fehlt {job['src']}"); recs.append({"name":job["name"],"error":"src missing"}); continue
        sf = prep(Path(job["src"]), job["name"])
        in_url = fal_client.upload_file(str(sf))
        handles = []
        for seed in job["seeds"]:
            args = {"image_url":in_url,"prompt":job["prompt"],"duration":job["duration"],
                    "resolution":"1080p","aspect_ratio":"9:16","camera_fixed":True,"seed":seed}
            handles.append((seed, fal_client.submit(job["endpoint"], arguments=args)))
            print(f"  submitted {job['name']} seed={seed}")
        for seed, h in handles:
            t0=time.time()
            try:
                res=h.get(); el=time.time()-t0; u=vid_url(res); saved=None
                if u:
                    p=OUT/f"{job['name']}_s{seed}_{stamp}.mp4"
                    p.write_bytes(httpx.get(u,timeout=900,follow_redirects=True).content)
                    saved=p.name
                    print(f"    {job['name']} s{seed} OK {el:.0f}s -> {saved} ({dims(p)})")
                else:
                    print(f"    WARN keine URL keys={list(res.keys())}")
                recs.append({"name":job["name"],"seed":seed,"saved":saved,"elapsed_s":round(el,1)})
            except Exception as e:
                print(f"    ERROR {job['name']} s{seed}: {e}")
                recs.append({"name":job["name"],"seed":seed,"error":str(e)})
        RESULTS.write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print("="*60); print(f"DONE -> {OUT}")


if __name__ == "__main__":
    main()
