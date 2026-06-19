#!/usr/bin/env python3
"""
Neue Treppe-Input-Bilder (nur Bilder). Spiraltreppe im offenen Kosmos, KEINE Wolken,
kepler-a-pose als Figur (on-model), groß/cinematic/artistic, diverse Kompositionen
inkl. leichter Untersicht. Keine Negativ-Prompts. 9:16 hochauflösend.
Modelle: nano-banana-pro/edit (2K) + seedream v4.5/edit. 4 Kompositionen x 2 Modelle = 8.
"""
import os, json, subprocess
from pathlib import Path
from datetime import datetime
env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); os.environ[k.strip()]=v.strip()
import fal_client, httpx
SD=Path(__file__).parent
OUT=SD/"outputs"/"stairs_inputs_new"; OUT.mkdir(parents=True,exist_ok=True)
KEPLER=SD/"inputs/kepler-a-pose-portrait-padded.png"
NANO="fal-ai/nano-banana-pro/edit"
SEEDREAM="fal-ai/bytedance/seedream/v4.5/edit"

CHAR=(" The character is exactly the voxel-block figure from the reference image: a blocky "
 "light-grey and white Minecraft-style voxel body with hard cubic facets, a white visor brim "
 "and dark brown voxel hair on top, dark trousers and white shoes, fully on-model. Vertical "
 "9:16 composition, sharp high detail.")

COMPS = {
 "epic_wide": ("Epic wide cinematic shot. A grand, majestic luminous spiral staircase ascends "
   "through deep open cosmic space, filling the tall vertical frame, its steps glowing soft "
   "warm-white from within like frosted glass lit from inside. A vast clear starfield of deep "
   "blue and purple nebulae surrounds it, open empty cosmos, the staircase floating freely "
   "among the stars. The voxel character climbs mid-stride on the staircase. Grand scale, "
   "cinematic depth."),
 "low_angle": ("Dramatic low-angle worm's-eye view looking upward along a luminous spiral "
   "staircase as it twists and rises into deep starry cosmos. The voxel character climbs the "
   "steps above, his legs clearly visible mid-stride. Soft warm-white glowing steps, a vast "
   "clear field of blue-purple nebulae and stars, open empty space, dynamic upward perspective, "
   "cinematic."),
 "three_quarter": ("Artistic three-quarter cinematic composition. A luminous spiral staircase "
   "sweeps diagonally through deep cosmic space, glowing warm-white from within. The voxel "
   "character ascends mid-climb. A vast clear starry galaxy of deep blue and violet nebulae, "
   "open empty cosmos, painterly cinematic lighting and depth, elegant artistic framing."),
 "follow": ("Intimate cinematic shot following the voxel character as he climbs a luminous "
   "spiral staircase through open cosmic space, the spiral consistently framed around him. Soft "
   "warm-white glowing steps, a clear vast starfield of blue-purple nebulae, open empty cosmos "
   "of just stars and nebulae, gentle cinematic depth, the character mid-stride on the steps."),
}

def dims(p): return subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
def img_urls(r):
    out=[]
    if isinstance(r.get("images"),list):
        for f in r["images"]: out.append(f.get("url","") if isinstance(f,dict) else f)
    elif isinstance(r.get("image"),dict): out.append(r["image"].get("url",""))
    return [u for u in out if u]

def main():
    if not os.environ.get("FAL_KEY"): print("ERROR FAL_KEY"); return
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    kurl=fal_client.upload_file(str(KEPLER))
    recs=[]
    for comp,scene in COMPS.items():
        prompt=scene+CHAR
        for model,args in [
            (NANO,{"image_urls":[kurl],"prompt":prompt,"aspect_ratio":"9:16","resolution":"2K","num_images":1}),
            (SEEDREAM,{"image_urls":[kurl],"prompt":prompt,"image_size":"portrait_16_9","num_images":1}),
        ]:
            tag=f"{comp}_{'nano' if model==NANO else 'seedream'}"
            print(f"== {tag} ==")
            try:
                res=fal_client.subscribe(model,arguments=args)
                for i,u in enumerate(img_urls(res)):
                    p=OUT/f"{tag}_{stamp}.png"
                    p.write_bytes(httpx.get(u,timeout=300,follow_redirects=True).content)
                    print(f"  saved {p.name} ({dims(p)})")
                    recs.append({"tag":tag,"model":model,"saved":p.name})
            except Exception as e:
                print(f"  ERROR {tag}: {e}"); recs.append({"tag":tag,"error":str(e)})
            (SD/"stairs_inputs_results.json").write_text(json.dumps(recs,indent=2,ensure_ascii=False))
    print("DONE ->",OUT)

if __name__=="__main__": main()
