#!/usr/bin/env python3
"""
Upscaler-Vergleich an Gavins behind_chase (9:16-Crop, schmaler 612px-Streifen).
Topaz vs SeedVR2, Faktor 2. Input ist ein 4s-Segment, Kosten ~0,58 $.
"""
import os, json, time
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

import fal_client, httpx

SCRIPT_DIR = Path(__file__).parent
INPUT = SCRIPT_DIR / "outputs" / "upscale_test" / "crop_9x16_native_612.mp4"
OUT = SCRIPT_DIR / "outputs" / "upscale_test"
RESULTS = SCRIPT_DIR / "upscale_test_results.json"

RUNS = [
    {"name": "B_topaz", "endpoint": "fal-ai/topaz/upscale/video",
     "args": {"upscale_factor": 2}},
    {"name": "C_seedvr2", "endpoint": "fal-ai/seedvr/upscale/video",
     "args": {"upscale_mode": "factor", "upscale_factor": 2, "seed": 42}},
]


def on_queue(u):
    if isinstance(u, fal_client.InProgress):
        for e in u.logs:
            m = e.get("message", "")
            if m:
                print(f"      [{m}]")


def vid_url(r):
    v = r.get("video")
    if isinstance(v, dict):
        return v.get("url", "")
    if isinstance(v, str):
        return v
    return ""


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print(f"UPSCALE-TEST | {stamp} | input={INPUT.name}")
    print("=" * 60)
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY fehlt"); return
    if not INPUT.exists():
        print(f"ERROR: input fehlt {INPUT}"); return

    print("  upload...")
    url = fal_client.upload_file(str(INPUT))
    print(f"  -> {url}")

    records = []
    for cfg in RUNS:
        print(f"\n  {cfg['name']} | {cfg['endpoint']} | {cfg['args']}")
        args = {"video_url": url, **cfg["args"]}
        t0 = time.time()
        try:
            res = fal_client.subscribe(cfg["endpoint"], arguments=args,
                                       with_logs=True, on_queue_update=on_queue)
            el = time.time() - t0
            out_url = vid_url(res)
            saved = None
            if out_url:
                p = OUT / f"{cfg['name']}.mp4"
                p.write_bytes(httpx.get(out_url, timeout=600, follow_redirects=True).content)
                saved = p.name
                print(f"    OK {el:.1f}s -> {saved} ({p.stat().st_size//1024}KB)")
            else:
                print(f"    WARN keine URL. keys={list(res.keys())}")
            records.append({"name": cfg["name"], "endpoint": cfg["endpoint"],
                            "args": cfg["args"], "elapsed_s": round(el, 1),
                            "saved": saved, "output_url": out_url})
        except Exception as e:
            el = time.time() - t0
            print(f"    ERROR ({el:.1f}s): {e}")
            records.append({"name": cfg["name"], "endpoint": cfg["endpoint"],
                            "args": cfg["args"], "error": str(e)})
    RESULTS.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
