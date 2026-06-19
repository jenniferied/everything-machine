#!/usr/bin/env python3
"""
Schminkspiegel-CD — RECOLOR der Hoop/Openhair-Basis auf Berry-Schema.

Basis (perfekte Groesse/Pose, soll erhalten bleiben):
  outputs/schminkspiegel_cyber_v2/
    cy2_edit_openhair_hoop_flux2_pro_rose_p43_p43_20260529_155747.png
  -> Chrom-Hand, Compact + Holo-CD, Chrom-Gesicht im Spiegel, offene
     Haare + Hoop-Earrings, ROSA Lippen/Naegel, schwarzer Raum.

Ziel-Farbschema (Referenz):
  outputs/schminkspiegel_chrome_galaxy/
    cg_nano_pro_LF_lip_berry_p43_20260529_100253.png
  -> tiefes BEERE/Pflaume-Lippenstift, kuehler blau-stichiger Chrom,
     dezent blaue Galaxie.

Nur das FARBSCHEMA aendern (Lippen + Naegel -> Beere/Pflaume, Chrom
leicht kuehler/blauer, Hintergrund darf dezent blau werden). Komposition,
Pose, Hand, Hoops, Haare, Compact, CD bleiben EXAKT. Sehr nah am Original.

Vier Methoden zum Vergleich:
  M1 nano-edit   (1 Input)               Recolor per Prompt
  M2 flux kontext max (1 Input)          Recolor per Prompt
  M3 nano-edit   (2 Inputs: Basis+Ref)   "Farbpalette von Bild 2 uebernehmen"
  M4 seedream v4.5/edit (1 Input)        Recolor per Prompt

Format 3:4. Kein Negativ-Prompting. Parallel. ~6 Jobs, ~$0.3.
"""

import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

import fal_client
import httpx

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_recolor_berry"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_recolor_berry_results.json"

BASE = (SCRIPT_DIR / "outputs" / "schminkspiegel_cyber_v2"
        / "cy2_edit_openhair_hoop_flux2_pro_rose_p43_p43_20260529_155747.png")
BERRY_REF = (SCRIPT_DIR / "outputs" / "schminkspiegel_chrome_galaxy"
             / "cg_nano_pro_LF_lip_berry_p43_20260529_100253.png")

MAX_WORKERS = 6
_lock = threading.Lock()
_url_cache: dict[str, str] = {}

# ── Recolor-Prompts (Komposition strikt erhalten) ───────────────────
KEEP = (
    "Keep the composition, framing, pose, the chrome hand and fingers, "
    "the hoop earrings, the open flowing hair, the open compact, the "
    "holographic CD and the dark space background EXACTLY as they are, "
    "completely unchanged"
)
RECOLOR_SINGLE = (
    f"{KEEP}. Only shift the COLOUR SCHEME to a deep BERRY / plum theme: "
    "repaint the lips with rich deep berry-plum lipstick and the "
    "fingernails with matching berry-plum polish, and give the chrome a "
    "slightly cooler blue-steel tone with a subtle deep-blue nebula glow "
    "in the background. Stay very close to the original image, this is a "
    "recolour only."
)
RECOLOR_TWO = (
    "Take the FIRST image and keep its composition, pose, chrome hand, "
    "hoop earrings, open hair, compact, CD and background EXACTLY "
    "unchanged. Apply only the COLOUR PALETTE of the SECOND image to it: "
    "the same deep berry-plum lips, matching berry-plum nails and the "
    "cooler blue-steel chrome and deep-blue galaxy tone. This is a "
    "recolour of the first image only; do not change its shapes or layout."
)

# ── Methoden ────────────────────────────────────────────────────────
def build_nano1(base_url, ref_url):
    return ("fal-ai/nano-banana-pro/edit",
            {"image_urls": [base_url], "prompt": RECOLOR_SINGLE,
             "aspect_ratio": "3:4", "num_images": 1})

def build_flux(base_url, ref_url):
    return ("fal-ai/flux-pro/kontext/max",
            {"image_url": base_url, "prompt": RECOLOR_SINGLE,
             "aspect_ratio": "3:4", "num_images": 1,
             "guidance_scale": 3.5, "safety_tolerance": "5"})

def build_nano2(base_url, ref_url):
    return ("fal-ai/nano-banana-pro/edit",
            {"image_urls": [base_url, ref_url], "prompt": RECOLOR_TWO,
             "aspect_ratio": "3:4", "num_images": 1})

def build_seedream(base_url, ref_url):
    return ("fal-ai/bytedance/seedream/v4.5/edit",
            {"image_urls": [base_url], "prompt": RECOLOR_SINGLE,
             "image_size": "portrait_4_3", "num_images": 1})

METHODS = {
    "M1_nano1":     {"build": build_nano1,    "cost": "$0.04"},
    "M2_flux":      {"build": build_flux,     "cost": "$0.08"},
    "M3_nano2ref":  {"build": build_nano2,    "cost": "$0.04"},
    "M4_seedream":  {"build": build_seedream, "cost": "$0.04"},
}
# nano-edit zweimal je Methode (verschiedene Seeds) fuer M1 + M3
JOBS = ["M1_nano1", "M1_nano1", "M2_flux", "M3_nano2ref", "M3_nano2ref",
        "M4_seedream"]


def upload(path: Path) -> str:
    key = str(path)
    with _lock:
        if key in _url_cache:
            return _url_cache[key]
    url = fal_client.upload_file(key)
    with _lock:
        _url_cache[key] = url
    return url


def first_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    if isinstance(result.get("image"), str):
        return result["image"]
    return ""


def save_image(url: str, name: str) -> Path | None:
    if not url:
        return None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url.lower() or "jpeg" in url.lower()) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=180, follow_redirects=True)
    out_path.write_bytes(resp.content)
    return out_path


def append_record(record: dict):
    with _lock:
        existing = []
        if RESULTS_FILE.exists():
            try:
                existing = json.loads(RESULTS_FILE.read_text())
            except Exception:
                existing = []
        existing.append(record)
        RESULTS_FILE.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False))


def run_job(method_key, idx, base_url, ref_url, stamp):
    m = METHODS[method_key]
    endpoint, args = m["build"](base_url, ref_url)
    label = f"{method_key}__run{idx}"
    name = f"rb_{method_key}_run{idx}_{stamp}"
    with _lock:
        print(f"  START  {label} | {endpoint}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(endpoint, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "method": method_key,
            "endpoint": endpoint, "base": BASE.name, "ref": BERRY_REF.name,
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
            "image": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   {label} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO IMAGE'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "label": label, "method": method_key,
            "endpoint": endpoint, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL RECOLOR BERRY | {len(JOBS)} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.3")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert BASE.exists(), f"missing base: {BASE}"
    assert BERRY_REF.exists(), f"missing ref: {BERRY_REF}"

    print("  Uploading base + berry reference...")
    base_url = upload(BASE)
    ref_url = upload(BERRY_REF)

    wall0 = time.time()
    ok = 0
    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for method_key in JOBS:
            counts[method_key] = counts.get(method_key, 0) + 1
            idx = counts[method_key]
            futures.append(
                ex.submit(run_job, method_key, idx, base_url, ref_url, stamp))
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(JOBS)} ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
