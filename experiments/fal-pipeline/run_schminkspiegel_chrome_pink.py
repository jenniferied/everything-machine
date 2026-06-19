#!/usr/bin/env python3
"""
Schminkspiegel-CD — Chrom-Gesicht, PINK painted Lippen/Naegel, Galaxy.

Feedback-Iteration auf run_schminkspiegel_chrome_galaxy.py:
  - Punkte NICHT gold -> schlichte subtile CHROM-Punkte.
  - Federn = ECHTE Federn (reales Material), als Ohrringe.
  - Im Spiegel sollen NASE + LIPPEN klar sichtbar sein (unteres-bis-
    mittleres Gesicht), gern weitere subtile, special Details.
  - Lippenstift PINK und PAINTED LOOK (echtes Make-up-Material, satter
    Materialkontrast zum Chrom) — nicht chromey.
  - Naegel leicht verlaengert und PINK painted (Nagellack-Look), nicht chrom.
  - Format nur 3:4 / 4:3 / 1:1 (kein 16:9 / 9:16).
  - Modelle gemischt: FLUX-2 Pro + Nano + Seedream v4.5 (Vergleich).
  - Dark Galaxy, kein Sockel (Arm schwebt vom unteren Rand herein).

ZUERST: Favorit cs_flux2_pro_C1_chrome_her_sq nur im Hintergrund auf
Galaxie editieren (nano-edit + FLUX Kontext Max) — als Option und als
moegliches leichtes Input-Bild.

Kein Negativ-Prompting. Parallel. ~12 Jobs, ~$0.7.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_chrome_pink"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_chrome_pink_results.json"

C1_SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_clipstar"
          / "cs_flux2_pro_C1_chrome_her_sq_20260529_095514.jpg")

MAX_WORKERS = 8
_lock = threading.Lock()

# ── Bausteine ───────────────────────────────────────────────────────
ANCHOR = (
    "A solid, smooth, highly polished mirror-chrome hand with exactly "
    "five fingers and slightly elongated, elegant tapered fingernails "
    "painted glossy PINK with a real nail-polish finish that softly "
    "contrasts the chrome skin, holding an open round makeup compact up "
    "in mid-air; the chrome forearm rises into the frame from the bottom "
    "edge, the hand and compact floating freely with open space around "
    "them. A round iridescent holographic CD sits clearly INSIDE the "
    "lower pan of the compact, scattering rainbow light across its grooves"
)
GALAXY = (
    "Background is a DARK galaxy: deep near-black space with faint "
    "distant stars and a subtle low-saturation nebula haze, moody and "
    "mostly black"
)
TAIL = "Vaporwave, high detail, glossy 3D render."

def mirror(shade: str) -> str:
    return (
        "In the upper-lid MIRROR appears the lower-to-mid half of a "
        "woman's face sculpted in liquid mirror-CHROME — her NOSE, LIPS "
        "and chin clearly visible, framed up to just below the eyes. The "
        "lips wear glossy " + shade + " lipstick with a soft, richly "
        "pigmented painted finish and a satin sheen — a real makeup "
        "material that stands out as the main spot of colour against the "
        "chrome. A few small subtle CHROME dots accent the lower cheeks. "
        "Real soft white FEATHER earrings of actual fluffy feathers "
        "dangle beside her jaw. Subtle special detail: a faint "
        "holographic sparkle drifting across the chrome skin"
    )

PROMPTS = {
    "rose": f"{ANCHOR}. {mirror('soft rose-pink')}. {GALAXY}. {TAIL}",
    "hot":  f"{ANCHOR}. {mirror('vivid hot bubblegum-pink')}. {GALAXY}. {TAIL}",
}

EDIT_PROMPT = (
    "Keep the chrome hand, the open makeup compact, the holographic CD "
    "and the chrome reflected face exactly as they are, unchanged. "
    "Change ONLY the background behind them to a DARK galaxy: deep "
    "near-black space with faint distant stars and a subtle "
    "low-saturation nebula haze, moody and mostly black."
)

# ── Formate (nur 3:4, 4:3, 1:1) ─────────────────────────────────────
SIZE_MAP = {
    "nano_pro":   {"sq": "1:1", "p43": "3:4", "l43": "4:3"},
    "flux2_pro":  {"sq": "square_hd", "p43": "portrait_4_3",
                   "l43": "landscape_4_3"},
    "seedream45": {"sq": "square_hd", "p43": "portrait_4_3",
                   "l43": "landscape_4_3"},
}

def args_nano(prompt, fmt):
    return {"prompt": prompt, "aspect_ratio": SIZE_MAP["nano_pro"][fmt],
            "resolution": "2K", "num_images": 1}

def args_flux(prompt, fmt):
    return {"prompt": prompt, "image_size": SIZE_MAP["flux2_pro"][fmt],
            "safety_tolerance": "5"}

def args_seedream(prompt, fmt):
    return {"prompt": prompt, "image_size": SIZE_MAP["seedream45"][fmt],
            "num_images": 1}

MODELS = {
    "nano_pro":   {"endpoint": "fal-ai/nano-banana-pro",
                   "args": args_nano, "cost": "$0.12"},
    "flux2_pro":  {"endpoint": "fal-ai/flux-2-pro",
                   "args": args_flux, "cost": "$0.03"},
    "seedream45": {"endpoint": "fal-ai/bytedance/seedream/v4.5/text-to-image",
                   "args": args_seedream, "cost": "$0.03"},
}

# (concept, model, format)
T2I_JOBS = [
    ("rose", "flux2_pro",  "p43"),
    ("rose", "nano_pro",   "sq"),
    ("rose", "flux2_pro",  "l43"),
    ("hot",  "flux2_pro",  "p43"),
    ("hot",  "nano_pro",   "p43"),
    ("hot",  "flux2_pro",  "sq"),
    ("rose", "seedream45", "sq"),
    ("hot",  "nano_pro",   "l43"),
    ("rose", "flux2_pro",  "sq"),
    ("hot",  "seedream45", "p43"),
]

# Edit-Jobs fuer den C1-Favoriten: (model_key, endpoint, format)
EDIT_JOBS = [
    ("nano_edit",    "fal-ai/nano-banana-pro/edit", "sq"),
    ("flux_kontext", "fal-ai/flux-pro/kontext/max", "sq"),
]


def upload(path: Path) -> str:
    return fal_client.upload_file(str(path))


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


def run_t2i(job, stamp):
    concept_key, model_key, fmt = job
    m = MODELS[model_key]
    prompt = PROMPTS[concept_key]
    label = f"{concept_key}__{model_key}__{fmt}"
    name = f"cp_{model_key}_{concept_key}_{fmt}_{stamp}"
    with _lock:
        print(f"  START  t2i  {label}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=m["args"](prompt, fmt), with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "mode": "t2i", "label": label,
            "concept": concept_key, "model": model_key, "format": fmt,
            "endpoint": m["endpoint"], "prompt": prompt,
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
            "image": url, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   t2i  {label} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO IMAGE'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "mode": "t2i", "label": label,
            "concept": concept_key, "model": model_key, "format": fmt,
            "endpoint": m["endpoint"], "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  t2i  {label} ({elapsed:.1f}s): {e}")
        return False


def run_edit(job, src_url, stamp):
    model_key, endpoint, fmt = job
    label = f"C1edit__{model_key}__{fmt}"
    name = f"cp_C1galaxy_{model_key}_{fmt}_{stamp}"
    if "kontext" in endpoint:
        args = {"image_url": src_url, "prompt": EDIT_PROMPT,
                "aspect_ratio": "1:1", "num_images": 1,
                "guidance_scale": 3.5, "safety_tolerance": "5"}
    else:  # nano-banana-pro/edit
        args = {"image_urls": [src_url], "prompt": EDIT_PROMPT,
                "aspect_ratio": "1:1", "num_images": 1}
    with _lock:
        print(f"  START  edit {label}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(endpoint, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "mode": "edit", "label": label,
            "model": model_key, "endpoint": endpoint, "src": C1_SRC.name,
            "prompt": EDIT_PROMPT, "format": fmt,
            "elapsed_s": round(elapsed, 1), "image": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   edit {label} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO IMAGE'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "mode": "edit", "label": label,
            "model": model_key, "endpoint": endpoint, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  edit {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = len(T2I_JOBS) + len(EDIT_JOBS)
    print("=" * 64)
    print(f"SCHMINKSPIEGEL CHROME PINK | {total} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.7")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert C1_SRC.exists(), f"missing C1 source: {C1_SRC}"

    print("  Uploading C1 favourite for edit...")
    src_url = upload(C1_SRC)

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for job in EDIT_JOBS:
            futures.append(ex.submit(run_edit, job, src_url, stamp))
        for job in T2I_JOBS:
            futures.append(ex.submit(run_t2i, job, stamp))
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/{total} ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
