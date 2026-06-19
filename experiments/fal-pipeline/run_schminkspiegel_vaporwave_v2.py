#!/usr/bin/env python3
"""
Schminkspiegel-CD — Vaporwave v2: Dark Galaxy, kein Dripping, mehr
Variation, Format-Mix, Kepler-(Voxel-)Bezug. Parallel.

Feedback-Iteration auf run_schminkspiegel_vaporwave.py:
  - DRIPPING WEG: ueber POSITIVE Sprache geloest (festes, glattes,
    sauberkantiges, nahtloses Chrom) statt Negativ-Prompts. Kein
    Negativ-Prompting (Anti-Anchoring-Regel).
  - CD MUSS im Pan liegen: explizit positiv festgeschrieben (lag vorher
    manchmal nicht drin).
  - FINGER: genau fuenf, positiv benannt.
  - MEHR VARIATION: vier verschiedene Kompositionen statt immer gleicher
    Pose (Macro, Seitenhand, Zwei-Hand-Offer, Aufsicht).
  - HINTERGRUND: Dark Galaxy (tiefes Schwarz, wenige Sterne, niedrige
    Saettigung) statt bunter Regenbogen-Galaxie.
  - FORMAT-MIX: 9:16, 1:1, 3:4, 4:3.
  - KEPLER-BEZUG (Voxel): zwei Blend-Varianten —
      K1 Voxel-Kepler-Figur (weisse blanke Voxel-Maske, dunkle Cap)
         als Reflexion IM Spiegel;
      K2 voxelisiertes Chrom (Chrom als kubische Voxel gerendert).
  - Modelle: FLUX-2 Pro + NanoBanana Pro (Seedream raus -> war
    Dripping-/Puder-Quelle). Parallel ueber ThreadPoolExecutor.

~16 Bilder, parallel, ~$0.8.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_vaporwave_v2"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_vaporwave_v2_results.json"

MAX_WORKERS = 8
_lock = threading.Lock()

# ── Gemeinsame Bausteine (positiv formuliert) ───────────────────────
# Festes, glattes, sauberkantiges Chrom => verhindert Dripping ohne
# das Wort "dripping" zu nennen.
CHROME = (
    "solid, smooth, highly polished mirror-chrome with crisp clean "
    "sculptural edges and a firm, seamless, glossy finish"
)
# CD immer klar im Pan.
CD_IN_PAN = (
    "a round iridescent holographic CD sits clearly INSIDE the lower pan "
    "of the open compact, filling it and scattering rainbow light across "
    "its grooves"
)
# Dark Galaxy.
DARK_BG = (
    "Background is a DARK galaxy: deep near-black space with only a few "
    "faint distant stars and a subtle low-saturation haze, moody and "
    "mostly black"
)
TAIL = "Vaporwave aesthetic, high detail, 3D render."

# ── Konzepte: jeweils vollstaendiger, eigenstaendiger Prompt ────────
PROMPTS = {
    "C1_close_macro": (
        f"A surreal vaporwave MACRO still. Extreme close-up on an open "
        f"round makeup compact held by {CHROME} chrome fingertips of a "
        f"hand with exactly five fingers. {CD_IN_PAN}. The upper-lid "
        f"mirror shows the chrome reflection of glossy chrome lips and "
        f"chin sculpted in liquid mirror-metal. Shallow depth of field, "
        f"the compact and CD fill the frame. {DARK_BG}. {TAIL}"
    ),
    "C2_one_hand_side": (
        f"A surreal vaporwave still. A SINGLE chrome hand with exactly "
        f"five fingers enters from the side and holds an open round "
        f"makeup compact at a relaxed natural angle, slightly off-centre. "
        f"The skin is {CHROME}. {CD_IN_PAN}. The upper-lid mirror shows "
        f"the chrome reflection of the lower half of a face — chrome lips "
        f"and chin in mirror-metal. {DARK_BG}. {TAIL}"
    ),
    "C3_two_hands_offer": (
        f"A surreal vaporwave still. TWO chrome hands, each with exactly "
        f"five fingers, cradle and lift an open round makeup compact "
        f"toward the viewer in a relaxed asymmetric pose, one hand a "
        f"little higher. The skin is {CHROME}. {CD_IN_PAN}. The mirror "
        f"shows the chrome reflection of chrome lips and chin. {DARK_BG}. "
        f"{TAIL}"
    ),
    "C4_high_angle": (
        f"A surreal vaporwave still seen from a HIGH ANGLE looking down. "
        f"A chrome hand with exactly five fingers holds an open round "
        f"makeup compact flat in an upturned palm. The skin is {CHROME}. "
        f"{CD_IN_PAN}. Looking into the mirror from above we see the "
        f"chrome reflection of a chrome lower face, lips and chin. "
        f"{DARK_BG}. {TAIL}"
    ),
    # ── Kepler-Bezug (Voxel) ──
    "K1_voxel_reflection": (
        f"A surreal still bridging two worlds. A {CHROME} chrome hand "
        f"with exactly five fingers holds an open round makeup compact; "
        f"{CD_IN_PAN}. But the reflection in the upper-lid MIRROR is a "
        f"blocky VOXEL / Minecraft-style figure — a cubic character with "
        f"a plain featureless WHITE voxel face mask (smooth and blank, no "
        f"facial features) and a dark voxel cap, appearing in the mirror "
        f"like a tiny pixel-world avatar. {DARK_BG}. Vaporwave meets "
        f"voxel, high detail, 3D render."
    ),
    "K2_voxel_chrome": (
        f"A surreal still where chrome meets voxel. A hand and an open "
        f"round makeup compact, all sculpted from CHROME rendered as a "
        f"structure of small cubic VOXELS — blocky faceted mirror-metal "
        f"like a Minecraft object cast in chrome, with five blocky "
        f"fingers, solid and firm with clean cubic edges. {CD_IN_PAN}. "
        f"The upper-lid mirror shows a blocky chrome-voxel reflection of "
        f"a lower face. {DARK_BG}. Vaporwave-voxel aesthetic, high "
        f"detail, 3D render."
    ),
}

# ── Formate ─────────────────────────────────────────────────────────
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

# (concept_key, model_key, format) — bewusst gemischt fuer Variation
JOBS = [
    ("C1_close_macro",      "flux2_pro", "sq"),
    ("C1_close_macro",      "nano_pro",  "p43"),
    ("C2_one_hand_side",    "flux2_pro", "p169"),
    ("C2_one_hand_side",    "nano_pro",  "l43"),
    ("C3_two_hands_offer",  "flux2_pro", "sq"),
    ("C3_two_hands_offer",  "nano_pro",  "p169"),
    ("C4_high_angle",       "flux2_pro", "l43"),
    ("C4_high_angle",       "nano_pro",  "sq"),
    ("K1_voxel_reflection", "flux2_pro", "p169"),
    ("K1_voxel_reflection", "nano_pro",  "sq"),
    ("K1_voxel_reflection", "nano_pro",  "p43"),
    ("K2_voxel_chrome",     "flux2_pro", "p43"),
    ("K2_voxel_chrome",     "nano_pro",  "p169"),
    ("C2_one_hand_side",    "flux2_pro", "p43"),
    ("C3_two_hands_offer",  "nano_pro",  "l43"),
    ("C1_close_macro",      "flux2_pro", "p169"),
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
    name = f"vw2_{model_key}_{concept_key}_{fmt}_{stamp}"
    with _lock:
        print(f"  START  {label} | {m['endpoint']}")
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
    print(f"SCHMINKSPIEGEL VAPORWAVE v2 | {len(JOBS)} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.8")
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
