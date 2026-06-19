#!/usr/bin/env python3
"""
Schminkspiegel-CD — Cyber v2: Chrom-Indents (kein Leuchten), Galaxy IN
der Reflexion, offene Haare / Hoops. Querformat. Parallel.

Feedback-Iteration auf run_schminkspiegel_cyber.py:
  - Cyber-Linien NICHT leuchtend/farbig -> nur subtile, eingravierte
    CHROM-INDENTS im selben Spiegel-Chrom (Relief, das Licht faengt),
    sehr subtil, tonal/farblos.
  - Im Spiegel fehlte der Hintergrund: die Spiegelung soll die DARK
    GALAXY hinter ihr REFLEKTIEREN (Raum + Sterne sichtbar im Spiegel).
  - Mehr Edits: offene Haare PLUS Hoop-Earrings, und einige NUR mit
    offenen Haaren (ohne Hoops).
  - Beibehalten: pink painted Lippen + Naegel, Augen verdeckt
    (Reflexion an der Nasenwurzel), kein Sockel, Querformat 4:3 (+3:4).

Kein Negativ-Prompting. FLUX-2 Pro + Nano (t2i), nano-edit (Edits).
~11 Jobs, ~$0.6.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_cyber_v2"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_cyber_v2_results.json"

PINK_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_chrome_pink"
SRC_HOT_L43  = PINK_DIR / "cp_nano_pro_hot_l43_20260529_101357.png"
SRC_ROSE_P43 = PINK_DIR / "cp_flux2_pro_rose_p43_20260529_101357.jpg"
SRC_HOT_SQ   = PINK_DIR / "cp_flux2_pro_hot_sq_20260529_101357.jpg"

MAX_WORKERS = 8
_lock = threading.Lock()
_url_cache: dict[str, str] = {}

# ── Bausteine ───────────────────────────────────────────────────────
ANCHOR = (
    "A solid, smooth, highly polished mirror-chrome hand with exactly "
    "five fingers and slightly elongated, elegant tapered fingernails "
    "painted glossy PINK with a real nail-polish finish that softly "
    "contrasts the chrome skin, holding an open round makeup compact up "
    "in mid-air; the chrome forearm rises into the frame from the bottom "
    "edge, the hand and compact floating freely. A round iridescent "
    "holographic CD sits clearly INSIDE the lower pan of the compact, "
    "scattering rainbow light across its grooves"
)
BLACK_SPACE = (
    "Background is deep BLACK space — near-total black with only a few "
    "faint distant stars and a very subtle dark nebula haze, she floats "
    "in the universe"
)
TAIL = "Vaporwave-cyber, high detail, glossy 3D render."

def mirror_cyber(shade: str) -> str:
    return (
        "In the upper-lid MIRROR we see her grey mirror-chrome face "
        "reflected FROM THE NOSE DOWNWARD — only her chrome nose, lips "
        "and chin appear, sitting LOW in the mirror, the reflection "
        "cropped right at the bridge of the nose so her eyes stay out of "
        "the mirror's frame. Around and above her face the mirror clearly "
        "REFLECTS the dark galaxy behind her — deep black space, "
        "scattered faint stars and a soft nebula fill the rest of the "
        "mirror, so she reads as floating in the universe. The lips wear "
        "glossy " + shade + " PINK lipstick with a soft, richly pigmented "
        "painted finish — the only colour in the image. Just a FEW "
        "subtle, low-key cyber accents are engraved into the chrome cheek "
        "— one or two fine indented lines of the very same mirror-chrome, "
        "tonal and colourless, sparse and understated, catching the light "
        "only as faint relief"
    )

PROMPTS = {
    "cyber_rose": f"{ANCHOR}. {mirror_cyber('soft rose')}. {BLACK_SPACE}. {TAIL}",
    "cyber_hot":  f"{ANCHOR}. {mirror_cyber('vivid hot bubblegum')}. {BLACK_SPACE}. {TAIL}",
}

# ── Edit-Prompts ────────────────────────────────────────────────────
EDIT_PROMPTS = {
    "openhair_hoop": (
        "Keep the chrome hand, the open compact, the holographic CD, the "
        "chrome reflected face, the pink lips, the pink fingernails and "
        "the dark galaxy background exactly as they are. Replace the "
        "feather earrings with sleek silver chrome HOOP earrings, and "
        "give her long flowing OPEN HAIR, loose and down, softly framing "
        "her face."
    ),
    "openhair_only": (
        "Keep the chrome hand, the open compact, the holographic CD, the "
        "chrome reflected face, the pink lips, the pink fingernails and "
        "the dark galaxy background exactly as they are. Replace the "
        "feather earrings with long flowing OPEN HAIR, loose and down, "
        "softly framing her face, with bare ears."
    ),
}

# ── Formate (Querformat 4:3 primaer) ────────────────────────────────
SIZE_MAP = {
    "nano_pro":  {"sq": "1:1", "p43": "3:4", "l43": "4:3"},
    "flux2_pro": {"sq": "square_hd", "p43": "portrait_4_3",
                  "l43": "landscape_4_3"},
}
EDIT_ASPECT = {"l43": "4:3", "sq": "1:1", "p43": "3:4"}
EDIT_ENDPOINT = "fal-ai/nano-banana-pro/edit"

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

# (concept, model, format)
T2I_JOBS = [
    ("cyber_rose", "flux2_pro", "l43"),
    ("cyber_hot",  "flux2_pro", "l43"),
    ("cyber_rose", "flux2_pro", "p43"),
    ("cyber_hot",  "nano_pro",  "l43"),
    ("cyber_rose", "nano_pro",  "l43"),
    ("cyber_hot",  "flux2_pro", "sq"),
]

# (source_path, prompt_key, format)
EDIT_JOBS = [
    (SRC_HOT_L43,  "openhair_hoop", "l43"),
    (SRC_ROSE_P43, "openhair_hoop", "p43"),
    (SRC_HOT_SQ,   "openhair_hoop", "sq"),
    (SRC_HOT_L43,  "openhair_only", "l43"),
    (SRC_ROSE_P43, "openhair_only", "p43"),
]


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


def run_t2i(job, stamp):
    concept_key, model_key, fmt = job
    m = MODELS[model_key]
    prompt = PROMPTS[concept_key]
    label = f"{concept_key}__{model_key}__{fmt}"
    name = f"cy2_{model_key}_{concept_key}_{fmt}_{stamp}"
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


def run_edit(job, stamp):
    src_path, prompt_key, fmt = job
    prompt = EDIT_PROMPTS[prompt_key]
    src_tag = src_path.stem.replace("cp_", "").replace("_20260529_101357", "")
    label = f"edit_{prompt_key}__{src_tag}__{fmt}"
    name = f"cy2_edit_{prompt_key}_{src_tag}_{fmt}_{stamp}"
    with _lock:
        print(f"  START  edit {label}")
    t0 = time.time()
    try:
        src_url = upload(src_path)
        args = {"image_urls": [src_url], "prompt": prompt,
                "aspect_ratio": EDIT_ASPECT[fmt], "num_images": 1}
        result = fal_client.subscribe(EDIT_ENDPOINT, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "mode": "edit", "label": label,
            "prompt_key": prompt_key, "endpoint": EDIT_ENDPOINT,
            "src": src_path.name, "prompt": prompt, "format": fmt,
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
            "prompt_key": prompt_key, "endpoint": EDIT_ENDPOINT,
            "src": src_path.name, "error": str(e),
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
    print(f"SCHMINKSPIEGEL CYBER v2 | {total} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$0.6")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    for src_path, _, _ in EDIT_JOBS:
        assert src_path.exists(), f"missing edit source: {src_path}"

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for job in EDIT_JOBS:
            futures.append(ex.submit(run_edit, job, stamp))
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
