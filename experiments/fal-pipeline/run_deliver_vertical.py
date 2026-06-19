#!/usr/bin/env python3
"""
Liefer-Pipeline: Gavins 3 Videos als scharfes Hochkant 1080x1920.
Pro Video: mittig auf 9:16 croppen -> Topaz-Upscale -> auf exakt 1080x1920 normalisieren.
Topaz-Faktor so gewaehlt, dass der Output >= 1080x1920 ist (danach sauberes Downscale).
Kosten ~2,40 $ (Topaz $0,08/s, 30s gesamt).
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
OUT = SD / "outputs" / "hd_vertical"
TMP = OUT / "_tmp"
RESULTS = SD / "deliver_vertical_results.json"
TOPAZ = "fal-ai/topaz/upscale/video"

# (Ausgabename, Quelle, crop_w, crop_h, topaz_factor)
JOBS = [
    ("behind_chase", SD/"outputs/behind_chase_video/behind_chase_A_fix_20260527_110811.mp4", 612, 1088, 2),
    ("kling_spiral", SD/"outputs/spiral_videos/kling3_pro_loop_20260519_180235_v2.mp4",      603, 1072, 2),
    ("schminkspiegel_v6", SD/"outputs/schminkspiegel_video/v6_moresway_20260602_151302.mp4", 469, 834, 4),
]


def ff(args):
    subprocess.run(["ffmpeg", "-y", *args, "-loglevel", "error"], check=True)


def dims(path):
    out = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","csv=p=0",str(path)],
        capture_output=True, text=True).stdout.strip()
    return out


def on_queue(u):
    if isinstance(u, fal_client.InProgress):
        for e in u.logs:
            m = e.get("message", "")
            if m:
                print(f"      [{m}]")


def vid_url(r):
    v = r.get("video")
    if isinstance(v, dict): return v.get("url", "")
    if isinstance(v, str): return v
    return ""


def main():
    OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY fehlt"); return
    records = []
    for name, src, cw, ch, factor in JOBS:
        print("="*60); print(f"{name} | {Path(src).name}")
        if not Path(src).exists():
            print(f"  ERROR Quelle fehlt: {src}"); records.append({"name":name,"error":"src missing"}); continue
        # 1) mittig auf 9:16 croppen (native, ohne Audio)
        cropped = TMP / f"{name}_crop_{cw}x{ch}.mp4"
        ff(["-i", str(src), "-vf", f"crop={cw}:{ch}:(in_w-{cw})/2:0", "-an", str(cropped)])
        print(f"  crop -> {dims(cropped)}")
        # 2) Topaz-Upscale
        print(f"  upload + Topaz x{factor}...")
        up_url = fal_client.upload_file(str(cropped))
        t0 = time.time()
        try:
            res = fal_client.subscribe(TOPAZ, arguments={"video_url": up_url, "upscale_factor": factor},
                                       with_logs=True, on_queue_update=on_queue)
        except Exception as e:
            print(f"  TOPAZ ERROR: {e}"); records.append({"name":name,"error":str(e)}); continue
        el = time.time() - t0
        out_url = vid_url(res)
        if not out_url:
            print(f"  WARN keine URL keys={list(res.keys())}"); records.append({"name":name,"error":"no url"}); continue
        topaz_raw = TMP / f"{name}_topaz.mp4"
        topaz_raw.write_bytes(httpx.get(out_url, timeout=900, follow_redirects=True).content)
        print(f"  topaz {el:.0f}s -> {dims(topaz_raw)}")
        # 3) auf exakt 1080x1920 normalisieren (Downscale)
        final = OUT / f"{name}_9x16_1080x1920.mp4"
        ff(["-i", str(topaz_raw), "-vf", "scale=1080:1920:flags=lanczos", "-an",
            "-c:v","libx264","-crf","16","-pix_fmt","yuv420p", str(final)])
        print(f"  FINAL -> {final.name} ({dims(final)}, {final.stat().st_size//1024}KB)")
        records.append({"name":name, "source":Path(src).name, "crop":f"{cw}x{ch}",
                        "topaz_factor":factor, "topaz_dims":dims(topaz_raw),
                        "final":final.name, "elapsed_s":round(el,1)})
    RESULTS.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print("="*60); print(f"DONE -> {OUT}")
    for r in records:
        print(f"  {r.get('name'):20} {r.get('final') or r.get('error')}")


if __name__ == "__main__":
    main()
