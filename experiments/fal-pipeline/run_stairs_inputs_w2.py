import os,json,subprocess
from pathlib import Path
from datetime import datetime
env=Path("../../.env.local")
for line in env.read_text().strip().split("\n"):
    if "=" in line and not line.startswith("#"):
        k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
import fal_client, httpx
OUT=Path("outputs/stairs_inputs_new"); OUT.mkdir(parents=True,exist_ok=True)
KEPLER="inputs/kepler-a-pose-portrait-padded.png"
CHAR=(" The character is exactly the voxel-block figure from the reference image: a blocky "
 "light-grey and white Minecraft-style voxel body with hard cubic facets, a white visor brim "
 "and dark brown voxel hair on top, dark trousers and white shoes, fully on-model.")
# Original funktionierende Leucht-Stufen-Prompt, ohne Wolken, ohne Negative:
ORIG=("A grand spiral staircase ascending through deep cosmic space. The staircase is not marble "
 "— the steps themselves are luminous, emitting a soft, even warm-white light from within like "
 "frosted glass lit from inside; the whole staircase glows gently in a single soft warm-white, "
 "subtle illumination casting faint light onto the surrounding space. A dreamy deep blue and "
 "purple cosmic atmosphere with stars and nebulae, open clear cosmos of just stars, the "
 "staircase floating freely in open space. The voxel character climbs the staircase mid-stride. "
 "Cinematic, tall vertical 9:16 composition, sharp high detail."+CHAR)
EPIC=("Epic wide cinematic shot, a grand luminous spiral staircase ascending through open cosmic "
 "space, glowing soft warm-white from within, a vast clear starfield of blue-purple nebulae, "
 "open empty cosmos, the voxel character climbing mid-stride. Tall vertical 9:16."+CHAR)
LOW=("Dramatic low-angle worm's-eye view up a luminous spiral staircase twisting into starry "
 "cosmos, the voxel character climbing above with legs visible, warm-white glowing steps, clear "
 "blue-purple nebulae, open empty space, cinematic. Tall vertical 9:16."+CHAR)
def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
def iurls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    return [u for u in out if u]
stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
k=fal_client.upload_file(KEPLER)
jobs=[
 ("orig_nano","fal-ai/nano-banana-pro/edit",{"image_urls":[k],"prompt":ORIG,"aspect_ratio":"9:16","resolution":"2K","num_images":1}),
 ("orig_seedream","fal-ai/bytedance/seedream/v4.5/edit",{"image_urls":[k],"prompt":ORIG,"image_size":"portrait_16_9","num_images":1}),
 ("epic_gpt","fal-ai/gpt-image-1.5/edit",{"image_urls":[k],"prompt":EPIC,"quality":"high","size":"1024x1536"}),
 ("low_gpt","fal-ai/gpt-image-1.5/edit",{"image_urls":[k],"prompt":LOW,"quality":"high","size":"1024x1536"}),
]
recs=[]
for tag,model,args in jobs:
    print("==",tag)
    try:
        r=fal_client.subscribe(model,arguments=args)
        for u in iurls(r):
            p=OUT/f"{tag}_{stamp}.png"; p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
            print("  saved",p.name,dims(p)); recs.append({"tag":tag,"saved":p.name})
    except Exception as e: print("  ERR",e); recs.append({"tag":tag,"error":str(e)})
    Path("stairs_inputs_w2_results.json").write_text(json.dumps(recs,indent=2))
print("DONE")
