import os,json,time,subprocess
from pathlib import Path
from datetime import datetime
env=Path("../../.env.local")
for line in env.read_text().strip().split("\n"):
    if "=" in line and not line.startswith("#"):
        k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
import fal_client, httpx
OUT=Path("outputs/hd_vertical_final"); OUT.mkdir(parents=True,exist_ok=True)
IMG="outputs/input_final/cd_final_edit.png"
PROMPT=("The round holographic disc spins like a vinyl record on a turntable, clearly and "
 "continuously rotating around its centre, its rainbow streaks sweeping around. The scene has "
 "subtle gentle life — a soft slow shimmer travelling across the polished chrome and a very "
 "faint drift — but the camera stays completely still and locked in place, no camera movement, "
 "no pan, no zoom. The chrome reflected face stays a smooth chrome surface with calm berry lips "
 "and a still chin, the chrome hand stays steady. Dark berry-toned cosmic galaxy behind.")
def vurl(r):
    v=r.get("video"); return v.get("url","") if isinstance(v,dict) else (v if isinstance(v,str) else "")
def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); u=fal_client.upload_file(IMG); hs=[]
for seed in [8801,8802]:
    hs.append((seed,fal_client.submit("bytedance/seedance-2.0/image-to-video",arguments={"image_url":u,"prompt":PROMPT,"duration":"8","resolution":"1080p","aspect_ratio":"9:16","generate_audio":False,"seed":seed})))
    print("submitted",seed)
for seed,h in hs:
    try:
        r=h.get(); vu=vurl(r)
        if vu:
            p=OUT/f"cd_final_s{seed}_{stamp}.mp4"; p.write_bytes(httpx.get(vu,timeout=900,follow_redirects=True).content)
            print("OK",p.name,dims(p))
    except Exception as e: print("ERR",seed,e)
print("DONE")
