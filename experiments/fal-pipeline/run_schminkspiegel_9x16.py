#!/usr/bin/env python3
"""
Schminkspiegel-CD NATIV 9:16 1080p (Prove-Run).
Quelle ist 868x1234 (hochkant) -> natives 9:16 = treuer zur Komposition + scharf
(1080p statt 720p-4:3-Crop). Prompt = v7-Strategie (CD-Spin Hauptbewegung,
Gesicht still/glatt-chrom, kein Augen-Drift). 2 Seeds parallel.
Seedance 2.0, 8s. ~1,24 $ gesamt.
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

SD = Path(__file__).parent
SRC = SD / "inputs" / "schminkspiegel" / "source.jpeg"
OUT = SD / "outputs" / "schminkspiegel_9x16"
RESULTS = SD / "schminkspiegel_9x16_results.json"
ENDPOINT = "bytedance/seedance-2.0/image-to-video"

# v7-Strategie: CD-Spin = Hauptbewegung; Gesicht glatt-chrom & still (keine Augen);
# Galaxy-Reflexion; sanfter Sway.
PROMPT = (
    "The round holographic disc spins like a vinyl record on a turntable — "
    "clearly and continuously rotating around its centre, its radial rainbow "
    "streaks sweeping around; this spinning disc is the main motion of the "
    "shot. The chrome reflected face in the mirror stays completely still and "
    "solid, a smooth seamless mirror-chrome surface showing only a subtle "
    "nose, closed lips and chin, the rest perfectly polished featureless "
    "chrome, with the dark starry GALAXY clearly reflected behind it in the "
    "mirror. The chrome hand stays steady. The camera sways gently with a "
    "slow, smooth cinematic drift."
)

TAKES = [{"tag": "9x16_a", "seed": 8001}, {"tag": "9x16_b", "seed": 8002}]
ARGS = {"duration": "8", "resolution": "1080p", "aspect_ratio": "9:16",
        "generate_audio": False}


def vid_url(r):
    v = r.get("video")
    if isinstance(v, dict): return v.get("url", "")
    if isinstance(v, str): return v
    return ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if not os.environ.get("FAL_KEY"):
        print("ERROR FAL_KEY fehlt"); return
    if not SRC.exists():
        print(f"ERROR Quelle fehlt {SRC}"); return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("="*60); print(f"SCHMINKSPIEGEL 9:16 1080p | Seedance 2.0 | {stamp}")
    print(f"Quelle: {SRC.name} (hochkant) | 2 Seeds parallel | ~1,24 $")
    print("="*60)
    url = fal_client.upload_file(str(SRC))
    print(f"  src -> {url}")

    handles = {}
    for t in TAKES:
        args = {"image_url": url, "prompt": PROMPT, "seed": t["seed"], **ARGS}
        handles[t["tag"]] = (fal_client.submit(ENDPOINT, arguments=args), t["seed"])
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
                print(f"    OK {el:.0f}s -> {saved} ({p.stat().st_size//1024}KB)")
            else:
                print(f"    WARN keine URL keys={list(res.keys())}")
            recs.append({"tag":tag,"seed_in":seed,"seed_returned":res.get("seed"),
                         "saved":saved,"elapsed_s":round(el,1),"output_url":u})
        except Exception as e:
            print(f"    ERROR {tag}: {e}")
            recs.append({"tag":tag,"seed_in":seed,"error":str(e)})
    RESULTS.write_text(json.dumps(recs, indent=2, ensure_ascii=False))
    print(f"\nDONE -> {OUT}")


if __name__ == "__main__":
    main()
