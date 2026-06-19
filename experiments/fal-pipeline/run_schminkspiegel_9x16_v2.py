#!/usr/bin/env python3
"""
Schminkspiegel-CD hochkant — KORREKT.
Input = das ECHTE v6-Chosen-Bild (dd_flux_20260602_150012.jpg, Chrom-Look),
mittig auf 9:16 gecroppt -> auf 1080x1920 hochskaliert (scharfer Startframe) ->
Seedance 2.0 i2v nativ 9:16 1080p. Prompt: CD dreht (Hauptbewegung), Gesicht
glatt-chrom & still (nur Nase/Lippen/Kinn, Rest nahtloses Chrom -> keine Augen),
dezenter Sway. 2 Seeds parallel.
Crop+Upscale via clarity-upscaler. ~1,30 $ gesamt.
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
SRC = SD / "outputs" / "schminkspiegel_dedot2" / "dd_flux_20260602_150012.jpg"
OUT = SD / "outputs" / "schminkspiegel_9x16"
TMP = OUT / "_inputprep"
RESULTS = SD / "schminkspiegel_9x16_v2_results.json"
VID_ENDPOINT = "bytedance/seedance-2.0/image-to-video"
UPSCALE_ENDPOINT = "fal-ai/clarity-upscaler"

PROMPT = (
    "The round holographic disc spins like a vinyl record on a turntable — "
    "clearly and continuously rotating around its centre, its radial rainbow "
    "streaks sweeping around; this spinning disc is the main motion of the "
    "shot. The chrome reflected face in the mirror stays completely still and "
    "solid, a smooth seamless mirror-chrome surface showing only a subtle "
    "nose, closed red lips and chin, the upper face remaining perfectly "
    "polished featureless chrome, with the dark starry blue GALAXY clearly "
    "reflected behind it in the mirror. The chrome hand stays steady. The "
    "camera sways very gently with a slow, subtle cinematic drift."
)

TAKES = [{"tag": "v2_a", "seed": 8101}, {"tag": "v2_b", "seed": 8102}]
ARGS = {"duration": "8", "resolution": "1080p", "aspect_ratio": "9:16",
        "generate_audio": False}


def ff(args):
    subprocess.run(["ffmpeg", "-y", *args, "-loglevel", "error"], check=True)


def dims(p):
    return subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","csv=p=0",str(p)],
        capture_output=True, text=True).stdout.strip()


def img_url(r):
    if isinstance(r.get("image"), dict): return r["image"].get("url","")
    if isinstance(r.get("images"), list) and r["images"]:
        f=r["images"][0]; return f.get("url","") if isinstance(f,dict) else f
    return ""


def vid_url(r):
    v = r.get("video")
    if isinstance(v, dict): return v.get("url","")
    if isinstance(v, str): return v
    return ""


def prep_input() -> Path:
    """Chosen-Bild auf 9:16 croppen, AI-upscalen, auf exakt 1080x1920."""
    TMP.mkdir(parents=True, exist_ok=True)
    w, h = map(int, dims(SRC).split(","))
    if w/h > 9/16:
        cw, ch = int(h*9/16), h
    else:
        cw, ch = w, int(w*16/9)
    crop = TMP / "chosen_9x16_crop.png"
    ff(["-i", str(SRC), "-vf", f"crop={cw}:{ch}:(in_w-{cw})/2:(in_h-{ch})/2", str(crop)])
    print(f"  crop {w}x{h} -> {dims(crop)}")
    # AI-Upscale (faithful: niedrige creativity, hohe resemblance)
    print("  upload+clarity upscale...")
    curl = fal_client.upload_file(str(crop))
    res = fal_client.subscribe(UPSCALE_ENDPOINT, arguments={
        "image_url": curl, "upscale_factor": 2, "creativity": 0.2,
        "resemblance": 1.0, "prompt": "chrome mirror compact, holographic CD, starry galaxy, crisp clean",
        "negative_prompt": "blur, jpeg artifacts, compression"})
    u = img_url(res)
    up = TMP / "chosen_9x16_up.png"
    up.write_bytes(httpx.get(u, timeout=300, follow_redirects=True).content)
    # exakt 1080x1920
    final_in = TMP / "chosen_9x16_1080x1920.png"
    ff(["-i", str(up), "-vf", "scale=1080:1920:flags=lanczos", str(final_in)])
    print(f"  upscaled startframe -> {dims(final_in)}")
    return final_in


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"):
        print("ERROR FAL_KEY fehlt"); return
    if not SRC.exists():
        print(f"ERROR Chosen-Input fehlt {SRC}"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("="*60); print(f"SCHMINKSPIEGEL 9:16 v2 (richtiges Chosen-Input) | {stamp}")
    print("="*60)
    startframe = prep_input()
    print("  upload startframe für i2v...")
    in_url = fal_client.upload_file(str(startframe))

    handles = {}
    for t in TAKES:
        args = {"image_url": in_url, "prompt": PROMPT, "seed": t["seed"], **ARGS}
        handles[t["tag"]] = (fal_client.submit(VID_ENDPOINT, arguments=args), t["seed"])
        print(f"  submitted {t['tag']} seed={t['seed']}")

    recs = []
    for tag, (h, seed) in handles.items():
        print(f"\n  warte {tag}...")
        t0 = time.time()
        try:
            res = h.get(); el = time.time()-t0
            u = vid_url(res); saved=None
            if u:
                p = OUT / f"schmink_{tag}_{stamp}.mp4"
                p.write_bytes(httpx.get(u, timeout=900, follow_redirects=True).content)
                saved = p.name
                print(f"    OK {el:.0f}s -> {saved} ({dims(p)}, {p.stat().st_size//1024}KB)")
            else:
                print(f"    WARN keine URL keys={list(res.keys())}")
            recs.append({"tag":tag,"seed_in":seed,"seed_returned":res.get("seed"),
                         "saved":saved,"elapsed_s":round(el,1)})
        except Exception as e:
            print(f"    ERROR {tag}: {e}")
            recs.append({"tag":tag,"seed_in":seed,"error":str(e)})
    RESULTS.write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
