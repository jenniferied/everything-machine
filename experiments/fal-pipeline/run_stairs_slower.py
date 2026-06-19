#!/usr/bin/env python3
"""Treppe langsamer + kleinere Steps: Input stairs_v6_0 (weiter, feinere Steps),
Endless-Climb aber langsam/sanft. 8s, Seedance 1.0 Pro, 2 Seeds."""
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
S1="fal-ai/bytedance/seedance/v1/pro/image-to-video"
IMG=SD/"outputs/input_v6/stairs_v6_0_20260618_235628.png"
PROMPT=("Endless-climb illusion at a slow, calm, dreamy pace. The voxel character slowly "
  "marches in place — his legs lift and step gently and slowly, his body staying in exactly "
  "the same spot in the frame. The entire spiral staircase rotates together as one single "
  "rigid object around its central vertical axis, very slowly and smoothly, the whole spiral "
  "scrolling gently downward past the character so he looks endlessly and slowly ascending. "
  "The staircase glow stays constant. Stars and galaxies drift very slowly. Camera completely "
  "static. His head, white visor and brown voxel hair stay identical throughout. Everything "
  "moves slowly and calmly.")
def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
def vid_url(r):
    v=r.get("video")
    if isinstance(v,dict): return v.get("url","")
    if isinstance(v,str): return v
    return ""
def main():
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY"); return
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); in_url=fal_client.upload_file(str(IMG))
    handles=[]
    for seed in [7101,7102]:
        handles.append((seed,fal_client.submit(S1,arguments={"image_url":in_url,"prompt":PROMPT,
            "duration":"8","resolution":"1080p","aspect_ratio":"9:16","camera_fixed":True,"seed":seed})))
        print("submitted stairs_slow seed",seed)
    recs=[]
    for seed,h in handles:
        t0=time.time()
        try:
            res=h.get(); el=time.time()-t0; u=vid_url(res); saved=None
            if u:
                p=OUT/f"stairs_slow_s{seed}_{stamp}.mp4"; p.write_bytes(httpx.get(u,timeout=900,follow_redirects=True).content); saved=p.name
                print(f"  s{seed} OK {el:.0f}s -> {saved} ({dims(p)})")
            recs.append({"seed":seed,"saved":saved,"elapsed_s":round(el,1)})
        except Exception as e:
            print("  ERROR",seed,e); recs.append({"seed":seed,"error":str(e)})
    (SD/"stairs_slower_results.json").write_text(json.dumps(recs,indent=2)); print("DONE")
if __name__=="__main__": main()
