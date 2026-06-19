#!/usr/bin/env python3
"""
Schminkspiegel-CD — Chrom-Gesicht im Spiegel, Dark Galaxy, kein Sockel.

Feedback-Iteration auf run_schminkspiegel_clipstar.py. Favorit war
cs_flux2_pro_C1_chrome_her_sq (Gesicht der Frau komplett in Chrom).
Aenderungen:
  - HINTERGRUND zurueck auf DARK GALAXY (nicht weiss).
  - Gesicht MUSS Chrom sein (auf jeden Fall).
  - Primaer nur das UNTERE Gesicht zeigen (Lippen/Kinn) — plus ein paar
    Vergleichs-Varianten mit mehr Gesicht (C1-Stil, Stirn-Markierung),
    damit ihre Signatur nicht verloren geht; User waehlt.
  - KEIN Sockel/Box mehr: positiv formuliert -> Arm steigt frei vom
    unteren Bildrand herein, Hand + Compact schweben.
  - EXPERIMENT: echter glaenzender Lippenstift auf den Chrom-Lippen
    (einziger Farbtupfer im Chrom-Gesicht) — rot und beere.
  - Format-Mix, leicht hoch: 3:4, 9:16, 4:3, 1:1.

Kein Negativ-Prompting. FLUX-2 Pro (bestes Chrom) + Nano. Parallel.
~12 Jobs, ~$0.6.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_chrome_galaxy"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_chrome_galaxy_results.json"

MAX_WORKERS = 8
_lock = threading.Lock()

# ── Bausteine ───────────────────────────────────────────────────────
# Schwebend, Arm vom unteren Rand => kein Sockel (positiv formuliert).
ANCHOR = (
    "A solid, smooth, highly polished mirror-chrome hand with exactly "
    "five fingers holds an open round makeup compact up in mid-air; the "
    "chrome forearm rises into the frame from the bottom edge, the hand "
    "and compact floating freely with open space around them. A round "
    "iridescent holographic CD sits clearly INSIDE the lower pan of the "
    "compact, scattering rainbow light across its grooves"
)
GALAXY = (
    "Background is a DARK galaxy: deep near-black space with faint "
    "distant stars and a subtle low-saturation nebula haze, moody and "
    "mostly black"
)
TAIL = "Vaporwave, high detail, glossy 3D render."

# Untere Gesichtshaelfte in Chrom.
def lf_mirror(lips: str) -> str:
    return (
        "In the upper-lid MIRROR appears the reflection of only the LOWER "
        "HALF of a woman's face — chin and " + lips + " sculpted in "
        "liquid mirror-chrome, nothing shown above the cheekbones, with "
        "tiny gold dots as chrome-and-gold relief on the lower cheeks, "
        "keeping her stylized character"
    )

# Vollere Gesichtshaelfte in Chrom (C1-Stil).
def ff_mirror(lips: str) -> str:
    return (
        "In the upper-lid MIRROR appears the reflection of a woman's face "
        "sculpted entirely in liquid mirror-CHROME — her stylized "
        "markings rendered as etched chrome relief: a downward arrow on "
        "the forehead, smoky eye sockets, gold dots on the cheeks, "
        + lips + ", and feather hair-pieces framing the face"
    )

CHROME_LIPS = "chrome lips"
LIP_RED = (
    "chrome lips that wear a layer of glossy DEEP-RED lipstick painted "
    "on top of the mirror-chrome — actual red lipstick, the only spot of "
    "colour on the otherwise all-chrome face"
)
LIP_BERRY = (
    "chrome lips that wear a layer of glossy dark BERRY / plum lipstick "
    "painted on top of the mirror-chrome — the only spot of colour on "
    "the otherwise all-chrome face"
)

PROMPTS = {
    "LF_galaxy":    f"{ANCHOR}. {lf_mirror(CHROME_LIPS)}. {GALAXY}. {TAIL}",
    "LF_lip_red":   f"{ANCHOR}. {lf_mirror(LIP_RED)}. {GALAXY}. {TAIL}",
    "LF_lip_berry": f"{ANCHOR}. {lf_mirror(LIP_BERRY)}. {GALAXY}. {TAIL}",
    "FF_galaxy":    f"{ANCHOR}. {ff_mirror('sculpted chrome lips')}. {GALAXY}. {TAIL}",
    "FF_lip_red":   f"{ANCHOR}. {ff_mirror(LIP_RED)}. {GALAXY}. {TAIL}",
}

SIZE_MAP = {
    "nano_pro":  {"p169": "9:16", "sq": "1:1", "p43": "3:4", "l43": "4:3"},
    "flux2_pro": {"p169": "portrait_16_9", "sq": "square_hd",
                  "p43": "portrait_4_3", "l43": "landscape_4_3"},
}

def args_nano(prompt, fmt):
    return {"prompt": prompt, "aspect_ratio": SIZE_MAP["nano_pro"][fmt],
            "resolution": "2K", "num_images": 1}

def args_flux(prompt, fmt):
    return {"prompt": prompt, "image_size": SIZE_MAP["flux2_pro"][fmt],
            "safety_tolerance": "5"}

MODELS = {
    "nano_pro":  {"endpoint": "fal-ai/nano-banana-pro",
                  "args": args_nano, "cost": "$0.12"},
    "flux2_pro": {"endpoint": "fal-ai/flux-2-pro",
                  "args": args_flux, "cost": "$0.03"},
}

# (concept, model, format) — leicht hoch gewichtet, Mix
JOBS = [
    ("LF_galaxy",    "flux2_pro", "p43"),
    ("LF_galaxy",    "flux2_pro", "p169"),
    ("LF_galaxy",    "nano_pro",  "sq"),
    ("LF_lip_red",   "flux2_pro", "p43"),
    ("LF_lip_red",   "flux2_pro", "l43"),
    ("LF_lip_red",   "nano_pro",  "p169"),
    ("LF_lip_berry", "flux2_pro", "p43"),
    ("LF_lip_berry", "nano_pro",  "p43"),
    ("FF_galaxy",    "flux2_pro", "sq"),
    ("FF_galaxy",    "flux2_pro", "p43"),
    ("FF_lip_red",   "flux2_pro", "p169"),
    ("FF_lip_red",   "nano_pro",  "sq"),
]


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


def run_job(job, stamp):
    concept_key, model_key, fmt = job
    m = MODELS[model_key]
    prompt = PROMPTS[concept_key]
    label = f"{concept_key}__{model_key}__{fmt}"
    name = f"cg_{model_key}_{concept_key}_{fmt}_{stamp}"
    with _lock:
        print(f"  START  {label}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=m["args"](prompt, fmt), with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "concept": concept_key,
            "model": model_key, "format": fmt, "endpoint": m["endpoint"],
            "prompt": prompt, "elapsed_s": round(elapsed, 1),
            "cost_est": m["cost"], "image": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   {label} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO IMAGE'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "label": label, "concept": concept_key,
            "model": model_key, "format": fmt, "endpoint": m["endpoint"],
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL CHROME GALAXY | {len(JOBS)} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.6")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(run_job, job, stamp): job for job in JOBS}
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(JOBS)} ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
