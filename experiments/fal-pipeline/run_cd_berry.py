#!/usr/bin/env python3
"""CD neu: v6-Basis, mehr BERRY + zoom-out (Hand kleiner, mehr Galaxy), nativ 2K.
Direkt per nano-Reframe (kein Padding -> keine Naht). 4 Variationen."""
import os, json
from pathlib import Path
from datetime import datetime
env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
import fal_client, httpx
SD=Path(__file__).parent
OUT=SD/"outputs"/"input_v9"; OUT.mkdir(parents=True,exist_ok=True)
SRC=SD/"outputs/input_v6/cd_v6_0_20260618_235628.png"
PROMPT=("Recompose this image: place the chrome hand and compact noticeably SMALLER, "
  "occupying only the central ~60 percent of the frame, surrounded by a generous expanse "
  "of dark, berry-toned blue-purple cosmic galaxy with stars — much more background space "
  "around the hand. Grade the whole image more BERRY: richer berry-red lips, warm "
  "berry-magenta and plum tones woven through the cool silver chrome and the dark cosmos, "
  "tasteful and balanced, not bright. Keep the silver chrome hand, the CD-player tray with "
  "the holographic disc on its hub, and the chrome face. Crisp, high quality, sharp.")
def img_urls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    return [u for u in out if u]
def main():
    url=fal_client.upload_file(str(SRC))
    res=fal_client.subscribe("fal-ai/nano-banana-pro/edit",arguments={
        "image_urls":[url],"prompt":PROMPT,"aspect_ratio":"9:16","resolution":"2K","num_images":4})
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); saved=[]
    for i,u in enumerate(img_urls(res)):
        p=OUT/f"cd_v9_{i}_{stamp}.png"; p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
        saved.append(p.name); print("saved",p.name,subprocess_dims(p))
    (SD/"cd_berry_results.json").write_text(json.dumps(saved)); print("DONE")
def subprocess_dims(p):
    import subprocess
    return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
if __name__=="__main__": main()
