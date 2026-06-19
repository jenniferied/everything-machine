#!/usr/bin/env python3
"""
Schminkspiegel-CD x CLIPSTAR — Video-Aesthetik lose einfliessen lassen.

Referenz: Frames aus dem KEPLER-Musikvideo "CLIPSTAR" (Official Video),
extrahiert nach inputs/yt_reference/frames/. Aesthetik:
  - High-Key WEISSES Studio / Galerie, Waende voller Skizzen-Collage
  - die Frau mit markantem Make-up: Stirn-Pfeil/Horn-Markierung,
    Smokey Eyes, goldene Wangenpunkte, dunkle Lippen, weisse
    Feder-Haarteile, lange schwarze Haare
  - Marionetten-/Puppet-an-Faeden-Motiv
  - eine GRUENE VOXEL-Figur an Faeden (Kepler-Voxel-Bezug!)

Ansatz (nach Advisor): "ganz lose Referenz" => primaer TEXT-TO-IMAGE,
die Aesthetik in Worte uebersetzt (nicht das Video reproduzieren). Die
Frau kommt "ein bisschen" rein = ihr Gesicht als SPIEGEL-Reflexion
(statt Chrom-Lippen), nicht als Ganzkoerper. Anker bleibt Chrom-Hand +
Compact + drehende Holo-CD.

Bewusste Auswahl-Forks (User entscheidet aus dem Spread):
  - Hintergrund: WEISS-Studio (neu, primaer) vs DARK GALAXY (Kontinuitaet)
  - die Frau: menschlich gestylt vs in Chrom
  - Marionetten-Faeden + gruene Voxel-Figur als Fusions-Straenge

Plus 2 klar markierte FUSION-Experimente (Edit, 2 Referenzbilder) zum
direkten Vergleich literal-vs-lose.

Modelle: FLUX-2 Pro + NanoBanana Pro (t2i), nano-banana-pro/edit (fusion).
Parallel. ~16 Jobs, ~$1.0.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_clipstar"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_clipstar_results.json"

# Fusion-Referenzen
CHROME_REF = (SCRIPT_DIR / "outputs" / "schminkspiegel_vaporwave_v2"
              / "vw2_flux2_pro_C1_close_macro_sq_20260529_094349.jpg")
FACE_REF = (SCRIPT_DIR / "inputs" / "yt_reference" / "frames"
            / "scene_017.jpg")

MAX_WORKERS = 8
_lock = threading.Lock()

# ── Bausteine ───────────────────────────────────────────────────────
CHROME_ANCHOR = (
    "A solid, smooth, polished mirror-chrome hand with exactly five "
    "fingers holds an open round makeup compact; a round iridescent "
    "holographic CD sits clearly INSIDE the lower pan, scattering "
    "rainbow light across its grooves"
)
WOMAN = (
    "a young woman's face with distinctive styling — a dark downward "
    "arrow / horn marking on her forehead between the brows, smoky dark "
    "eye make-up, tiny gold dots on her cheeks, dark lips, soft white "
    "feather hair-pieces framing her face, long black hair"
)
WHITE_STUDIO = (
    "Set in a bright high-key all-WHITE studio gallery, the white walls "
    "behind densely covered in a collage of sketchy black-and-white "
    "drawings and photos, clean, minimal, soft even lighting"
)

PROMPTS = {
    # ── Weiss-Studio, Frau als Reflexion (primaere Fusion) ──
    "W1_white_face": (
        f"{CHROME_ANCHOR}. In the upper-lid MIRROR appears the reflection "
        f"of {WOMAN}. {WHITE_STUDIO}. Vaporwave-editorial mood, high "
        f"detail, glossy 3D render with photographic realism."
    ),
    "W2_white_strings": (
        f"{CHROME_ANCHOR}. Thin black MARIONETTE STRINGS descend from "
        f"above and attach to the chrome hand and wrist, as if the hand "
        f"is a puppet being guided. In the mirror appears the reflection "
        f"of {WOMAN}. {WHITE_STUDIO}. Surreal puppet / marionette mood, "
        f"high detail."
    ),
    "W3_white_voxel_puppet": (
        f"{CHROME_ANCHOR}. In the upper-lid mirror, instead of a face, "
        f"appears a small GREEN VOXEL / Minecraft-style marionette figure "
        f"— a blocky pixel character hanging from thin black-and-green "
        f"strings like a puppet. {WHITE_STUDIO}. Chrome meets voxel, "
        f"surreal marionette mood, high detail."
    ),
    "W4_white_collage": (
        f"{CHROME_ANCHOR}. In the mirror appears the reflection of "
        f"{WOMAN}. {WHITE_STUDIO}; the sketch-collage gallery wall is "
        f"prominent and in focus behind. Editorial art-gallery mood, "
        f"high detail."
    ),
    # ── Chrome-Variante der Frau (Vergleichs-Fork) ──
    "C1_chrome_her": (
        f"{CHROME_ANCHOR}. In the mirror appears the reflection of the "
        f"same woman BUT her face is itself sculpted in liquid "
        f"mirror-CHROME — her forehead arrow marking, cheek dots and "
        f"feather hair-pieces rendered as etched chrome relief. "
        f"{WHITE_STUDIO}. Vaporwave, high detail."
    ),
    # ── Dark-Galaxy-Kontinuitaet ──
    "D1_dark_face": (
        f"{CHROME_ANCHOR}. In the mirror appears the reflection of "
        f"{WOMAN}. Background is a DARK galaxy: deep near-black space "
        f"with faint stars and a subtle low-saturation haze, moody. "
        f"Vaporwave, high detail."
    ),
}

FUSION_PROMPT = (
    "Combine the two reference images. Keep the chrome hand, the open "
    "makeup compact and the spinning holographic CD from the first image "
    "as the main subject. In the round MIRROR of the compact, place the "
    "reflected face of the woman from the second image, keeping her "
    "forehead arrow marking, smoky eyes, gold cheek dots, dark lips, "
    "white feather hair-pieces and long black hair. Bright high-key "
    "WHITE studio background. Vaporwave-editorial, high detail."
)

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

# t2i-Jobs: (concept_key, model_key, format)
T2I_JOBS = [
    ("W1_white_face",         "flux2_pro", "p169"),
    ("W1_white_face",         "nano_pro",  "sq"),
    ("W1_white_face",         "flux2_pro", "p43"),
    ("W2_white_strings",      "flux2_pro", "p169"),
    ("W2_white_strings",      "nano_pro",  "p43"),
    ("W3_white_voxel_puppet", "nano_pro",  "sq"),
    ("W3_white_voxel_puppet", "flux2_pro", "p169"),
    ("W4_white_collage",      "flux2_pro", "l43"),
    ("W4_white_collage",      "nano_pro",  "p169"),
    ("C1_chrome_her",         "flux2_pro", "sq"),
    ("D1_dark_face",          "flux2_pro", "p169"),
    ("D1_dark_face",          "nano_pro",  "sq"),
]

# Fusion-Jobs (Edit, 2 Referenzen): (format,)
FUSION_FORMATS = ["sq", "p169"]
FUSION_ENDPOINT = "fal-ai/nano-banana-pro/edit"


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
    name = f"cs_{model_key}_{concept_key}_{fmt}_{stamp}"
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
            "run": stamp, "mode": "t2i", "label": label,
            "concept": concept_key, "model": model_key, "format": fmt,
            "endpoint": m["endpoint"], "prompt": prompt,
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
            "run": stamp, "mode": "t2i", "label": label,
            "concept": concept_key, "model": model_key, "format": fmt,
            "endpoint": m["endpoint"], "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def run_fusion(fmt, ref_urls, stamp):
    label = f"FUSION_2ref__nano_edit__{fmt}"
    name = f"cs_fusion_nano_edit_{fmt}_{stamp}"
    args = {"image_urls": ref_urls, "prompt": FUSION_PROMPT,
            "aspect_ratio": SIZE_MAP["nano_pro"][fmt], "num_images": 1}
    with _lock:
        print(f"  START  {label}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            FUSION_ENDPOINT, arguments=args, with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "mode": "fusion", "label": label,
            "endpoint": FUSION_ENDPOINT, "refs": [p for p in ref_urls],
            "prompt": FUSION_PROMPT, "format": fmt,
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
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
            "run": stamp, "mode": "fusion", "label": label,
            "endpoint": FUSION_ENDPOINT, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = len(T2I_JOBS) + len(FUSION_FORMATS)
    print("=" * 64)
    print(f"SCHMINKSPIEGEL x CLIPSTAR | {total} Jobs PARALLEL "
          f"(max {MAX_WORKERS}) | {stamp} | ~$1.0")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert CHROME_REF.exists(), f"missing chrome ref: {CHROME_REF}"
    assert FACE_REF.exists(), f"missing face ref: {FACE_REF}"

    print("  Uploading fusion references...")
    ref_urls = [upload(CHROME_REF), upload(FACE_REF)]

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = []
        for job in T2I_JOBS:
            futures.append(ex.submit(run_t2i, job, stamp))
        for fmt in FUSION_FORMATS:
            futures.append(ex.submit(run_fusion, fmt, ref_urls, stamp))
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/{total} ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
