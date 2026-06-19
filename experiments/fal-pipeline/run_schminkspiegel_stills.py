#!/usr/bin/env python3
"""
Schminkspiegel-CD — Ausgangsbilder fuer das naechste Video.

Motiv (Quelle: inputs/schminkspiegel/source.jpeg):
  Elegante, fluessig-verchromte weibliche Haende halten einen
  aufgeklappten runden Schminkspiegel. Im oberen Deckel: ein runder,
  fein gesprungener Spiegel, der das untere Gesicht einer Frau zeigt
  (glaenzende Lippen, Nase). In der unteren Schale liegt — statt
  Make-up-Puder — eine sich drehende, irisierende Holo-CD mit einem
  kleinen Goldstern. Tiefer kosmischer Hintergrund mit Sternen.

Statt nur das Modell zu variieren, variieren wir die PROMPTS (drei
kreative Spielarten, Basismotiv bleibt erhalten) und kreuzen sie mit
mehreren aktuellen Edit-Modellen. So entstehen echte Variationen statt
vier Reproduktionen derselben Quelle.

Drei Prompt-Spielarten (Basismotiv identisch):
  P1 faithful_cosmic  — nah am Original: enges Framing, klares
                        Sternenfeld, verchromte Haende, gesprungener
                        Spiegel mit Lippen, Regenbogen-CD + Goldstern.
  P2 nebula_iris      — etwas weiter, bunter Nebel/Aurora-Hintergrund,
                        perlmutt-irisierende Haende, intensiv leuchtende
                        Holo-CD.
  P3 studio_glow      — minimalistisch, weicher rosa-violetter
                        Kosmos-Glow, glossy Chrom-Haende, im Spiegel
                        Lippen + angedeutete gespiegelte Haende, CD mit
                        deutlichem Dreh-Schimmer.

Modell-Matrix (alle 16:9 fuer Video-Input):
  nano-banana-pro/edit   P1, P2, P3   (echtes 16:9, starker Allrounder)
  seedream v4.5/edit      P1, P2       (image_size landscape_16_9)
  flux-pro/kontext/max    P1           (haelt Komposition treu)
  gpt-image-1.5/edit      P2           (1536x1024 -> Center-Crop 16:9)

7 Bilder, ~$0.32.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

env_path = Path(__file__).parent.parent.parent / ".env.local"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ[key.strip()] = val.strip()

import fal_client
import httpx
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_results.json"
SOURCE = SCRIPT_DIR / "inputs" / "schminkspiegel" / "source.jpeg"

# ── Basismotiv: bleibt in jeder Spielart erhalten ────────────────────
MOTIF = (
    "Elegant slender feminine hands with a glossy liquid-chrome / "
    "mirror-metal finish cradle an open round compact mirror from below. "
    "UPPER LID: a round mirror, its glass delicately cracked with fine "
    "spider-web fractures, reflecting the lower half of a woman's face — "
    "full glossy lips and the tip of her nose, nothing above the "
    "cheekbones. LOWER PAN: where the make-up powder would sit there is "
    "instead a spinning iridescent holographic CD catching rainbow light "
    "across its grooves, a tiny gold star resting on it. The compact has "
    "a magenta-pink rim."
)

PROMPTS = {
    "P1_faithful_cosmic": (
        f"{MOTIF} Tight centred framing on the compact and the chrome "
        "hands. Deep cosmic navy-blue background scattered with bright "
        "sparkling stars. Hyper-glossy, surreal, dreamlike, high-detail "
        "digital art. Cinematic 16:9 widescreen."
    ),
    "P2_nebula_iris": (
        f"{MOTIF} Slightly wider framing leaving cosmic air around the "
        "compact. Background is a luminous colourful nebula with aurora "
        "ribbons of teal, magenta and violet and drifting stars. The "
        "hands shimmer with a pearlescent iridescent sheen; the "
        "holographic CD glows intensely. Lush, surreal, painterly "
        "digital art. Cinematic 16:9 widescreen."
    ),
    "P3_studio_glow": (
        f"{MOTIF} Minimal clean composition, the compact floating "
        "centred against a soft rose-and-violet cosmic gradient glow "
        "with a few faint stars. The cracked mirror reflects the glossy "
        "lips and a faint hint of the chrome hands holding the compact. "
        "The CD shows a subtle motion-shimmer of spinning. Polished, "
        "editorial, dreamy. Cinematic 16:9 widescreen."
    ),
}

# ── Modelle: arg-Builder kapselt die unterschiedlichen Signaturen ────
def args_nano(url, prompt):
    return {"image_urls": [url], "prompt": prompt,
            "aspect_ratio": "16:9", "num_images": 1}

def args_seedream(url, prompt):
    return {"image_urls": [url], "prompt": prompt,
            "image_size": "landscape_16_9", "num_images": 1}

def args_flux(url, prompt):
    return {"image_url": url, "prompt": prompt, "aspect_ratio": "16:9",
            "num_images": 1, "guidance_scale": 3.5, "safety_tolerance": "5"}

def args_gpt(url, prompt):
    # GPT kann kein echtes 16:9 — 1536x1024 (3:2), danach Center-Crop.
    return {"image_urls": [url], "prompt": prompt,
            "quality": "high", "size": "1536x1024"}

MODELS = {
    "nano":     {"endpoint": "fal-ai/nano-banana-pro/edit",
                 "args": args_nano, "cost": "$0.04", "crop_169": False},
    "seedream": {"endpoint": "fal-ai/bytedance/seedream/v4.5/edit",
                 "args": args_seedream, "cost": "$0.04", "crop_169": False},
    "flux":     {"endpoint": "fal-ai/flux-pro/kontext/max",
                 "args": args_flux, "cost": "$0.08", "crop_169": False},
    "gpt":      {"endpoint": "fal-ai/gpt-image-1.5/edit",
                 "args": args_gpt, "cost": "$0.04", "crop_169": True},
}

# (prompt_key, model_key)
JOBS = [
    ("P1_faithful_cosmic", "nano"),
    ("P2_nebula_iris",     "nano"),
    ("P3_studio_glow",     "nano"),
    ("P1_faithful_cosmic", "seedream"),
    ("P2_nebula_iris",     "seedream"),
    ("P1_faithful_cosmic", "flux"),
    ("P2_nebula_iris",     "gpt"),
]


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def first_url(result) -> str:
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    return ""


def crop_to_169(path: Path) -> str:
    """Center-crop ein Bild auf exakt 16:9. Gibt das neue Format zurueck."""
    with Image.open(path) as im:
        w, h = im.size
        target = 16 / 9
        if abs((w / h) - target) < 0.01:
            return f"{w}x{h} (already 16:9)"
        if w / h > target:          # zu breit -> Breite beschneiden
            new_w = int(round(h * target))
            left = (w - new_w) // 2
            box = (left, 0, left + new_w, h)
        else:                        # zu hoch -> Hoehe beschneiden
            new_h = int(round(w / target))
            top = (h - new_h) // 2
            box = (0, top, w, top + new_h)
        im.crop(box).save(path)
    with Image.open(path) as im2:
        return f"cropped {w}x{h} -> {im2.size[0]}x{im2.size[1]}"


def save_image(url: str, name: str) -> Path | None:
    if not url:
        return None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=180, follow_redirects=True)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(record: dict):
    existing = []
    if RESULTS_FILE.exists():
        try:
            existing = json.loads(RESULTS_FILE.read_text())
        except Exception:
            existing = []
    existing.append(record)
    RESULTS_FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


def run(prompt_key: str, model_key: str, src_url: str, stamp: str):
    prompt = PROMPTS[prompt_key]
    m = MODELS[model_key]
    label = f"{prompt_key}__{model_key}"
    name = f"schmink_{model_key}_{prompt_key}_{stamp}"
    print(f"\n--- {label} | {m['endpoint']} | {m['cost']} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=m["args"](src_url, prompt),
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        crop_note = None
        if saved and m["crop_169"]:
            crop_note = crop_to_169(saved)
            print(f"    16:9 fix: {crop_note}")
        append_record({
            "run": stamp, "label": label, "prompt_key": prompt_key,
            "model": model_key, "endpoint": m["endpoint"], "prompt": prompt,
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
            "crop_169": crop_note, "image": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "label": label, "prompt_key": prompt_key,
            "model": model_key, "endpoint": m["endpoint"],
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL STILLS | {len(JOBS)} Jobs | {stamp} | ~$0.32")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SOURCE.exists(), f"missing: {SOURCE}"

    src_url = upload(SOURCE)
    for prompt_key, model_key in JOBS:
        run(prompt_key, model_key, src_url, stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
