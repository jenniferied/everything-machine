#!/usr/bin/env python3
"""CD echter Zoom-out: gepaddetes cd_v6 -> nano füllt Rand mit passender (dunkler!)
Galaxy, v6-Farben erhalten. 4 Variationen zum Entscheiden."""
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
OUT=SD/"outputs"/"input_v8"; OUT.mkdir(parents=True,exist_ok=True)
SRC=OUT/"cd_padded.png"
PROMPT=("Fill and extend the dark border areas around the chrome hand with a natural, "
  "seamless continuation of the existing dark blue and purple starry galaxy, matching the "
  "muted, balanced color grading of the central image exactly. Keep it DARK and tasteful — "
  "do NOT brighten the galaxy. Keep the polished silver chrome hand, the compact, the "
  "CD-player tray with the holographic disc, and the chrome face with berry lips exactly as "
  "they are. Result: a zoomed-out composition with the hand and compact smaller within more "
  "cosmic space.")
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
        p=OUT/f"cd_v8_{i}_{stamp}.png"; p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
        saved.append(p.name); print("saved",p.name)
    (SD/"cd_outpaint_results.json").write_text(json.dumps(saved)); print("DONE")
if __name__=="__main__": main()
