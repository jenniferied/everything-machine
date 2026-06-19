#!/usr/bin/env python3
"""
Finale Videos v2 — alle 8s.
- CD (Seedance 2.0): rausgezoomtes Input cd_v7_1. CD dreht, Kamera statisch, Kinn ruhig.
- Treppe (Seedance 1.0 Pro): VERBATIM die funktionierende Endless-Climb-Prompt aus
  run_spiral_loop.py (nur Kopf-Zeile auf Visor+braunes Haar korrigiert). Input stairs_v6b_0.
Je 2 Seeds. behind_chase ist separat als 8s-Schnitt fertig.
"""
import os, json, time, subprocess
from pathlib import Path
from datetime import datetime
env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
import fal_client, httpx
SD=Path(__file__).parent
OUT=SD/"outputs"/"hd_vertical_final"; OUT.mkdir(parents=True,exist_ok=True)
RESULTS=SD/"videos_v2_results.json"
S1="fal-ai/bytedance/seedance/v1/pro/image-to-video"
S2="bytedance/seedance-2.0/image-to-video"

CD_PROMPT=("The round holographic disc spins like a vinyl record on a turntable — clearly "
  "and continuously rotating around its centre, its radial rainbow streaks sweeping around; "
  "this spinning disc is the main and only motion of the shot. The chrome reflected face in "
  "the mirror stays completely still and solid, a smooth seamless mirror-chrome surface "
  "showing only a subtle nose, closed lips and a calm smooth chin with soft minimal "
  "reflection, the upper face featureless polished chrome, the dark blue galaxy reflected "
  "behind it. The chrome hand stays perfectly steady. The camera is completely static and "
  "locked in place, no camera movement at all.")
# VERBATIM aus run_spiral_loop.py, nur letzte Zeile (Kopf) korrigiert:
STAIRS_PROMPT=("Endless-climb illusion. The voxel character marches in place — his legs lift "
  "and step rhythmically, but his body stays exactly in the same spot in the frame. The "
  "ENTIRE spiral staircase rotates as one single rigid object around its central vertical "
  "axis. EVERY part of the staircase rotates uniformly at the same speed — the bottom steps, "
  "the middle steps, AND the upper part of the spiral disappearing into the distance — ALL "
  "rotate together as one unit, like a carousel or rotating sculpture. The whole spiral "
  "scrolls downward past the character, so it looks like he's endlessly ascending. The "
  "staircase glow stays constant. Stars and galaxies drift very slowly. Camera is completely "
  "static — no zoom, no pan, no tilt. His head, white visor and brown voxel hair stay "
  "identical throughout.")

JOBS=[
 {"name":"cd2","endpoint":S2,"img":SD/"outputs/input_v7/cd_v7_1_20260619_002301.png",
  "prompt":CD_PROMPT,"seeds":[6001,6002],"cam":False},
 {"name":"stairs2","endpoint":S1,"img":SD/"outputs/input_v6/stairs_v6b_0_20260618_235628.png",
  "prompt":STAIRS_PROMPT,"seeds":[6101,6102],"cam":True},
]
def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
def vid_url(r):
    v=r.get("video")
    if isinstance(v,dict): return v.get("url","")
    if isinstance(v,str): return v
    return ""
def main():
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY"); return
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); recs=[]
    for job in JOBS:
        print("="*50, job["name"])
        in_url=fal_client.upload_file(str(job["img"])); handles=[]
        for seed in job["seeds"]:
            args={"image_url":in_url,"prompt":job["prompt"],"duration":"8","resolution":"1080p","aspect_ratio":"9:16","seed":seed}
            if job["cam"]: args["camera_fixed"]=True
            if job["endpoint"]==S2: args["generate_audio"]=False
            handles.append((seed,fal_client.submit(job["endpoint"],arguments=args)))
            print(f"  submitted {job['name']} seed={seed}")
        for seed,h in handles:
            t0=time.time()
            try:
                res=h.get(); el=time.time()-t0; u=vid_url(res); saved=None
                if u:
                    p=OUT/f"{job['name']}_s{seed}_{stamp}.mp4"
                    p.write_bytes(httpx.get(u,timeout=900,follow_redirects=True).content); saved=p.name
                    print(f"    {job['name']} s{seed} OK {el:.0f}s -> {saved} ({dims(p)})")
                recs.append({"name":job["name"],"seed":seed,"saved":saved,"elapsed_s":round(el,1)})
            except Exception as e:
                print(f"    ERROR {job['name']} s{seed}: {e}"); recs.append({"name":job["name"],"seed":seed,"error":str(e)})
        RESULTS.write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print("DONE ->",OUT)
if __name__=="__main__": main()
