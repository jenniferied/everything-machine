#!/usr/bin/env python3
"""
Schminkspiegel-CD — ORIGINALE Bilder (Text-to-Image, KEIN Input-Bild).

Die Edit-Variante (run_schminkspiegel_stills.py) blieb zu nah an der
Quelle und hat deren Fehler geerbt (Haende mit nur drei Fingern). Hier
nehmen wir nur die IDEE / ESSENZ und generieren frei aus Text — so
entstehen echte, eigenstaendige Bilder.

Essenz (in jeder Spielart erhalten):
  Elegante weibliche Haende (anatomisch korrekt, fuenf Finger) halten
  einen aufgeklappten runden Schminkspiegel hoch. In der unteren Schale
  liegt statt Puder eine sich drehende, irisierende Holo-CD, die
  Regenbogenlicht streut. Im runden Spiegel des Deckels sieht man nur
  die Reflexion der glaenzenden Lippen / des unteren Gesichts einer Frau
  — ihre Identitaet nur ueber die Lippen angedeutet. Kosmischer
  Hintergrund. Glossy, surreal, traumhaft. 16:9.

Drei kreative Spielarten (Essenz identisch):
  E1 nebula_glam      — perlmuttig-leuchtende Haut-Haende, satter
                        Nebula (Tuerkis/Magenta/Violett), glamour-hyperreal.
  E2 chrome_vaporwave — Haende aus fluessigem Spiegel-Chrom, tiefes
                        Sternennavy, magenta Compact, intensive Holo-CD.
  E3 editorial_glow   — minimal-editorial, weicher rosa-violetter
                        Kosmos-Glow, zarte Haende, Dreh-Schimmer der CD.

Modelle (alle 16:9, reines Text-to-Image):
  fal-ai/nano-banana-pro                          aspect_ratio 16:9, 2K
  fal-ai/bytedance/seedream/v4.5/text-to-image    image_size landscape_16_9
  fal-ai/flux-2-pro                               image_size landscape_16_9

3 Spielarten x 3 Modelle = 9 Bilder, ~$0.45.
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

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_original"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_original_results.json"

# ── Essenz: bleibt in jeder Spielart erhalten ───────────────────────
ESSENCE = (
    "A surreal cosmic beauty still. A pair of elegant feminine hands — "
    "anatomically correct with five graceful fingers and a glossy "
    "manicure — holds an open round makeup compact up toward the viewer. "
    "In the LOWER PAN of the compact, where pressed powder would be, "
    "there sits a small spinning iridescent holographic CD that scatters "
    "rainbow light across its grooves. In the round MIRROR of the upper "
    "lid we see only the reflection of a woman's glossy lips and the "
    "lower part of her face — her identity hinted at through her lips "
    "alone, nothing above the cheekbones."
)

PROMPTS = {
    "E1_nebula_glam": (
        f"{ESSENCE} The hands have luminous skin with a pearlescent "
        "iridescent sheen. Background is a vivid cosmic nebula glowing in "
        "teal, magenta and violet with sparkling scattered stars. Lush, "
        "glamorous, hyperreal, dreamlike digital art. Cinematic 16:9 "
        "widescreen, rich colour, sharp detail."
    ),
    "E2_chrome_vaporwave": (
        f"{ESSENCE} The hands are sculpted from flowing liquid "
        "mirror-chrome with blue and orange reflections. Deep starlit "
        "navy-blue space background with a few bright sparkle-stars. The "
        "compact has a magenta-pink rim and the holographic CD glows with "
        "intense rainbow light. Glossy vaporwave surrealism, high-detail "
        "digital art. Cinematic 16:9 widescreen."
    ),
    "E3_editorial_glow": (
        f"{ESSENCE} Minimal editorial composition, the compact held "
        "centred against a soft dreamy rose-and-violet cosmic gradient "
        "glow with faint drifting stardust. Delicate refined hands, a "
        "subtle motion-shimmer on the spinning CD. Clean, polished, "
        "ethereal, fashion-editorial mood. Cinematic 16:9 widescreen."
    ),
}

# ── Modelle: reine T2I-Endpoints mit ihren 16:9-Argumenten ──────────
MODELS = {
    "nano_pro": {
        "endpoint": "fal-ai/nano-banana-pro",
        "args": {"aspect_ratio": "16:9", "resolution": "2K", "num_images": 1},
        "cost": "$0.12",
    },
    "seedream45": {
        "endpoint": "fal-ai/bytedance/seedream/v4.5/text-to-image",
        "args": {"image_size": "landscape_16_9", "num_images": 1},
        "cost": "$0.03",
    },
    "flux2_pro": {
        "endpoint": "fal-ai/flux-2-pro",
        "args": {"image_size": "landscape_16_9", "safety_tolerance": "5"},
        "cost": "$0.03",
    },
}


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


def run(prompt_key: str, model_key: str, stamp: str):
    prompt = PROMPTS[prompt_key]
    m = MODELS[model_key]
    label = f"{prompt_key}__{model_key}"
    name = f"orig_{model_key}_{prompt_key}_{stamp}"
    args = {"prompt": prompt, **m["args"]}
    print(f"\n--- {label} | {m['endpoint']} | {m['cost']} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            m["endpoint"], arguments=args,
            with_logs=True, on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "prompt_key": prompt_key,
            "model": model_key, "endpoint": m["endpoint"], "prompt": prompt,
            "elapsed_s": round(elapsed, 1), "cost_est": m["cost"],
            "image": url, "saved": saved.name if saved else None,
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
    print(f"SCHMINKSPIEGEL ORIGINAL (T2I) | 9 Jobs | {stamp} | ~$0.45")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    for prompt_key in PROMPTS:
        for model_key in MODELS:
            run(prompt_key, model_key, stamp)

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
