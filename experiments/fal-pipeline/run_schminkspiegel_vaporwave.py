#!/usr/bin/env python3
"""
Schminkspiegel-CD — VAPORWAVE / VOLL-CHROM, HOCHKANT, parallelisiert.

Feedback-Iteration auf run_schminkspiegel_original.py:
  - Vaporwave-Aesthetik weiterverfolgen (war der Favorit).
  - GANZE Haut = fluessiges Spiegel-Chrom — auch die Reflexion im
    Spiegel ist Chrom (kein menschlicher Hautton, keine echten Lippen).
  - Compact-FARBE unbestimmt lassen (nicht vorgeben).
  - Handhaltung NATUERLICHER + variiert (die alten wirkten teils steif).
  - HOCHKANT 9:16 (zum spaeteren Extenden / Outpainten), eine
    Quadrat-Variante als Alternative.
  - PARALLEL: alle fal-Calls laufen gleichzeitig ueber einen
    ThreadPoolExecutor statt nacheinander -> deutlich schneller.

Prompt-Spielarten (Essenz identisch, nur Pose/Format variiert):
  V1 one_hand_relaxed  — eine Chrom-Hand haelt den Compact locker von
                         der Seite, leicht aus der Mitte, candid.
  V2 two_hands_natural — zwei Chrom-Haende, entspannt asymmetrisch
                         gehalten (eine hoeher), natuerlich gebogene Finger.
  V3 threequarter_open — Compact im sanften Dreiviertel-Winkel, wie
                         gerade aufgeklappt, Hand aus der unteren Ecke.

Modelle (je Spielart): nano-banana-pro, seedream v4.5 t2i, flux-2-pro.
Format: 9:16 hochkant. Plus 1 Quadrat-Variante (V2 auf flux + nano).

~14 Bilder, parallel, ~$0.65.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_vaporwave"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_vaporwave_results.json"

MAX_WORKERS = 8          # gleichzeitige fal-Calls
_lock = threading.Lock()  # schuetzt Datei-Schreiben + print

# ── Essenz: Voll-Chrom Vaporwave, Compact-Farbe bewusst NICHT genannt ─
ESSENCE = (
    "A surreal vaporwave cosmic beauty still. EVERYTHING is sculpted "
    "from flowing liquid mirror-chrome: the skin is entirely glossy "
    "chrome metal — hands, fingers, and even the face reflected in the "
    "mirror are the same flowing mirror-chrome, with NO human skin tone "
    "anywhere. A chrome hand holds an open round makeup compact. In the "
    "LOWER PAN, where pressed powder would be, there is instead a "
    "spinning iridescent holographic CD scattering rainbow light across "
    "its grooves. In the round MIRROR of the upper lid appears the "
    "chrome reflection of the lower half of a face — chrome lips and "
    "chin sculpted in liquid mirror-metal, identity hinted only through "
    "the lips. Hands are anatomically correct with five graceful "
    "fingers. Glossy, dreamy, retro-futuristic vaporwave aesthetic, "
    "deep cosmic background with stars and soft teal-magenta-violet "
    "gradients, high detail."
)

POSES = {
    "V1_one_hand_relaxed": (
        "A SINGLE chrome hand holds the compact casually from one side "
        "at a relaxed, natural angle — fingers loosely and naturally "
        "curved, the compact sitting slightly off-centre in the frame, "
        "a candid unposed feel."
    ),
    "V2_two_hands_natural": (
        "TWO chrome hands cradle the compact in a relaxed, natural grip "
        "— not stiffly symmetric: one hand a little higher than the "
        "other, fingers naturally bent, an easy lifelike pose as if "
        "casually showing it."
    ),
    "V3_threequarter_open": (
        "The compact is tilted at a gentle three-quarter angle as if "
        "just flipped open, held naturally by a chrome hand entering "
        "from the lower corner of the frame, fingers relaxed."
    ),
}

# Modelle: arg-Builder bekommt ein Format-Token ("portrait"/"square").
SIZE_MAP = {
    "nano_pro":   {"portrait": "9:16",            "square": "1:1"},
    "seedream45": {"portrait": "portrait_16_9",   "square": "square_hd"},
    "flux2_pro":  {"portrait": "portrait_16_9",   "square": "square_hd"},
}

def args_nano(prompt, fmt):
    return {"prompt": prompt, "aspect_ratio": SIZE_MAP["nano_pro"][fmt],
            "resolution": "2K", "num_images": 1}

def args_seedream(prompt, fmt):
    return {"prompt": prompt, "image_size": SIZE_MAP["seedream45"][fmt],
            "num_images": 1}

def args_flux(prompt, fmt):
    return {"prompt": prompt, "image_size": SIZE_MAP["flux2_pro"][fmt],
            "safety_tolerance": "5"}

MODELS = {
    "nano_pro":   {"endpoint": "fal-ai/nano-banana-pro",
                   "args": args_nano, "cost": "$0.12"},
    "seedream45": {"endpoint": "fal-ai/bytedance/seedream/v4.5/text-to-image",
                   "args": args_seedream, "cost": "$0.03"},
    "flux2_pro":  {"endpoint": "fal-ai/flux-2-pro",
                   "args": args_flux, "cost": "$0.03"},
}

# (pose_key, model_key, format)
JOBS = [
    ("V1_one_hand_relaxed",  "nano_pro",   "portrait"),
    ("V1_one_hand_relaxed",  "seedream45", "portrait"),
    ("V1_one_hand_relaxed",  "flux2_pro",  "portrait"),
    ("V2_two_hands_natural", "nano_pro",   "portrait"),
    ("V2_two_hands_natural", "seedream45", "portrait"),
    ("V2_two_hands_natural", "flux2_pro",  "portrait"),
    ("V3_threequarter_open", "nano_pro",   "portrait"),
    ("V3_threequarter_open", "seedream45", "portrait"),
    ("V3_threequarter_open", "flux2_pro",  "portrait"),
    # Quadrat-Alternativen (zum breiteren Outpainten)
    ("V2_two_hands_natural", "flux2_pro",  "square"),
    ("V2_two_hands_natural", "nano_pro",   "square"),
    ("V1_one_hand_relaxed",  "flux2_pro",  "square"),
]


def full_prompt(pose_key: str) -> str:
    return f"{ESSENCE} {POSES[pose_key]}"


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
    pose_key, model_key, fmt = job
    m = MODELS[model_key]
    prompt = full_prompt(pose_key)
    label = f"{pose_key}__{model_key}__{fmt}"
    name = f"vw_{model_key}_{pose_key}_{fmt}_{stamp}"
    with _lock:
        print(f"  START  {label} | {m['endpoint']} | {m['cost']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=m["args"](prompt, fmt),
            with_logs=False,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "pose": pose_key,
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
            "run": stamp, "label": label, "pose": pose_key,
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
    print(f"SCHMINKSPIEGEL VAPORWAVE | {len(JOBS)} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.65")
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
    print(f"DONE {ok}/{len(JOBS)} ok | wall {wall:.1f}s "
          f"(seriell waeren ~{sum(1 for _ in JOBS) * 30}s) -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
