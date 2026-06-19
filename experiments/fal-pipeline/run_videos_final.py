#!/usr/bin/env python3
"""
Finale Hochkant-Videos aus den v6-Inputs (1536x2752). i2v nativ 9:16 1080p.
- CD (Seedance 2.0): CD dreht = Hauptbewegung, Kamera STATISCH, Kinn ruhig/wenig
  Reflex, Gesicht glatt-chrom ohne Augen.
- Treppe (Seedance 1.0 Pro): Endless-Climb-Illusion, Kamera fix.
- behind_chase (Seedance 1.0 Pro): originaler kopfstabiler A_fix-Prompt.
Je 2 Seeds. ~6,6 $.
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
OUT = SD / "outputs" / "hd_vertical_final"
RESULTS = SD / "videos_final_results.json"
S1 = "fal-ai/bytedance/seedance/v1/pro/image-to-video"
S2 = "bytedance/seedance-2.0/image-to-video"

CD_PROMPT = (
    "The round holographic disc spins like a vinyl record on a turntable — clearly "
    "and continuously rotating around its centre, its radial rainbow streaks sweeping "
    "around; this spinning disc is the main and only motion of the shot. The chrome "
    "reflected face in the mirror stays completely still and solid, a smooth seamless "
    "mirror-chrome surface showing only a subtle nose, closed lips and a calm smooth "
    "chin with soft minimal reflection, the upper face remaining featureless polished "
    "chrome, with the dark blue starry galaxy reflected behind it. The chrome hand "
    "stays perfectly steady. The camera is completely static and locked in place, no "
    "camera movement at all."
)
STAIRS_PROMPT = (
    "Endless-climb illusion. The voxel character marches in place — his legs lift and "
    "step rhythmically, but his body stays exactly in the same spot in the frame. The "
    "ENTIRE spiral staircase rotates as one single rigid object around its central "
    "vertical axis. EVERY part of the staircase rotates uniformly at the same speed — "
    "bottom, middle and the upper part disappearing into the distance — ALL together "
    "as one unit, like a carousel. The whole spiral scrolls downward past the "
    "character, so he looks endlessly ascending. The staircase glow stays constant. "
    "Stars and galaxies drift very slowly. Camera is completely static. The character "
    "keeps his white visor and brown voxel hair identical throughout."
)
BEHIND_PROMPT = (
    "A bordeaux-red voxel-block convertible Cadillac drives steadily forward down an "
    "empty desert road at night. The car drives forward and gradually recedes into the "
    "distance, getting smaller as it moves away from the static camera position behind "
    "it. The road has two lanes separated by a single white dashed center line; the car "
    "cruises in the right lane. Sandy desert shoulders with brush and rocks on both "
    "sides. The asphalt and the dashed white line flow past from the far horizon toward "
    "the bottom of the frame, the natural look of driving forward at steady highway "
    "speed. The red tail lights glow calmly. The full moon stays high in the starry "
    "sky with only a gentle hint of violet. Distant mountains stay still. The camera is "
    "behind the car at road level with a locked, steady framing. The voxel character "
    "driver sits still and steady, both blocky voxel hands on the wheel, his white "
    "visor and brown voxel hair staying exactly the same throughout. Cinematic moonlit "
    "night. The bordeaux car body keeps its rich aged-wine burgundy color throughout."
)

JOBS = [
    {"name": "cd", "endpoint": S2, "img": SD/"outputs/input_v6/cd_v6_0_20260618_235628.png",
     "prompt": CD_PROMPT, "duration": "8", "seeds": [5001, 5002], "cam_fixed": False},
    {"name": "stairs", "endpoint": S1, "img": SD/"outputs/input_v6/stairs_v6b_0_20260618_235628.png",
     "prompt": STAIRS_PROMPT, "duration": "10", "seeds": [5101, 5102], "cam_fixed": True},
    {"name": "behind_chase", "endpoint": S1, "img": SD/"outputs/input_v6/behind_v6_0_20260618_235628.png",
     "prompt": BEHIND_PROMPT, "duration": "12", "seeds": [5201, 5202], "cam_fixed": True},
]


def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
    "-show_entries","stream=width,height","-of","csv=p=0",str(p)],
    capture_output=True,text=True).stdout.strip()
def vid_url(r):
    v=r.get("video")
    if isinstance(v,dict): return v.get("url","")
    if isinstance(v,str): return v
    return ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY fehlt"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recs=[]
    for job in JOBS:
        print("="*60); print(job["name"])
        if not Path(job["img"]).exists():
            print(f"  ERROR input fehlt {job['img']}"); recs.append({"name":job["name"],"error":"input missing"}); continue
        in_url = fal_client.upload_file(str(job["img"]))
        handles=[]
        for seed in job["seeds"]:
            args={"image_url":in_url,"prompt":job["prompt"],"duration":job["duration"],
                  "resolution":"1080p","aspect_ratio":"9:16","seed":seed}
            if job["cam_fixed"]: args["camera_fixed"]=True
            if job["endpoint"]==S2: args["generate_audio"]=False
            handles.append((seed, fal_client.submit(job["endpoint"], arguments=args)))
            print(f"  submitted {job['name']} seed={seed}")
        for seed,h in handles:
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
                recs.append({"name":job["name"],"seed":seed,"seed_returned":res.get("seed"),
                             "saved":saved,"elapsed_s":round(el,1)})
            except Exception as e:
                print(f"    ERROR {job['name']} s{seed}: {e}")
                recs.append({"name":job["name"],"seed":seed,"error":str(e)})
        RESULTS.write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print("="*60); print(f"DONE -> {OUT}")


if __name__ == "__main__":
    main()
