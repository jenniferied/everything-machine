#!/usr/bin/env python3
"""CD-Input rauszoomen via nano-banana-pro/edit (2K, 9:16). Rest identisch."""
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
OUT=SD/"outputs"/"input_v7"; OUT.mkdir(parents=True,exist_ok=True)
SRC=SD/"outputs/input_v6/cd_v6_0_20260618_235628.png"
PROMPT=("Zoom out so the chrome hand and the full compact appear smaller and more "
        "centered in the frame, with more empty cosmic space and galaxy around them. "
        "Keep everything else identical: the polished silver chrome hand, the chrome "
        "mirror face with berry lips and calm chin, the CD-player-style tray with the "
        "holographic disc resting on its central hub, and the balanced silver and soft "
        "blue-purple cosmic color grading. Crisp high detail.")
def img_urls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    return [u for u in out if u]
def main():
    url=fal_client.upload_file(str(SRC))
    res=fal_client.subscribe("fal-ai/nano-banana-pro/edit",arguments={
        "image_urls":[url],"prompt":PROMPT,"aspect_ratio":"9:16","resolution":"2K","num_images":2})
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); saved=[]
    for i,u in enumerate(img_urls(res)):
        p=OUT/f"cd_v7_{i}_{stamp}.png"; p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
        saved.append(p.name); print("saved",p.name)
    (SD/"cd_zoomout_results.json").write_text(json.dumps(saved))
    print("DONE")
if __name__=="__main__": main()
