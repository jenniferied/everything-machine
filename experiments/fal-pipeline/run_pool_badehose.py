#!/usr/bin/env python3
"""
Pool-Badehose — statische Bilder (Schritt 1, Videos kommen spaeter).

Zwei zusammengehoerende Pool-Szenen mit dem Kepler-Voxel-Char auf dem
Schwimmring. Beide werden zu 16:9-Stills mit Badehose vorbereitet:

  Bild A  outputs/22_nanobanana_refined_landscape/pool_floaty.png
          schraege Ansicht, schon 16:9 (1376x768)
          -> nur Outfit-Edit: Badehose

  Bild B  outputs/24_nanobanana_apose_portrait/pool_floaty.png
          Ausgangsbild des "Das beste!"-Kling-V3-Pool-Videos,
          hochkant 9:16 (768x1376)
          -> Schritt 1: generativ links/rechts auf 16:9 erweitern
             (Bild wird mittig auf graue 16:9-Leinwand gepaddet,
              nano-banana fuellt nur die grauen Raender -> Mitte bleibt)
          -> Schritt 2: Outfit-Edit auf dem erweiterten Bild: Badehose

Outfit-Edit: Voxel-Char traegt nur eine Badehose. Torso, Arme, Beine und
nackte Fuesse sind alle unbedeckte Voxel-Bloecke in Hautfarbe (kein weisses
Oberteil, keine dunkle lange Hose). Keine Flip-Flops am Fuss. Die Flip-Flops
am Poolrand bleiben als Deko stehen.

Model: fal-ai/nano-banana-pro/edit (~$0.04/img, 3 Bilder = ~$0.12)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "pool_badehose"
RESULTS_FILE = SCRIPT_DIR / "pool_badehose_results.json"

IMG_A = SCRIPT_DIR / "outputs" / "22_nanobanana_refined_landscape" / "pool_floaty.png"
IMG_B = SCRIPT_DIR / "outputs" / "24_nanobanana_apose_portrait" / "pool_floaty.png"

MODEL = "fal-ai/nano-banana-pro/edit"

# --- Prompts -------------------------------------------------------------

BADEHOSE_PROMPT = (
    "Edit this voxel-style swimming pool image. KEEP EVERYTHING IDENTICAL — "
    "the swimming pool, turquoise water and ripple pattern, the gold/bronze "
    "inflatable pool ring, the sun loungers, potted plants, palm-leaf "
    "shadows, the pair of flip-flops resting on the pool deck, and the camera "
    "angle, framing, lighting and colour grade. ONLY change the voxel "
    "character's outfit: he is now dressed for a day at the pool, wearing "
    "ONLY swim trunks (board shorts) on his hips. His torso, arms, legs and "
    "bare feet are all uncovered skin-tone voxel blocks in a warm light skin "
    "tone, with the same blocky cubic voxel texture as the rest of his body "
    "— no white shirt or top, no dark long trousers anymore. He wears NOTHING "
    "on his feet: bare skin-tone voxel feet, definitely NOT flip-flops, "
    "sandals or shoes on his feet. The swim trunks cover only his hips and "
    "upper thighs. Keep his head, hair/cap and his relaxed lying pose exactly "
    "the same. Maintain the voxel / lego-block art style precisely. Do NOT "
    "move, remove or restyle the flip-flops that sit on the pool deck as "
    "scenery — they stay exactly where they are."
)

OUTPAINT_PROMPT = (
    "This image shows a voxel-style top-down swimming pool scene placed in "
    "the centre of a larger 16:9 canvas, with flat neutral-grey margins on "
    "the left and right sides. Fill ONLY the grey left and right margin "
    "areas by naturally extending the existing scene outward — more "
    "turquoise pool water with the same ripple pattern, more pale pool "
    "deck, more sun loungers, potted plants and palm-leaf shadows, "
    "consistent with whatever is already visible at the left and right "
    "edges of the central image. KEEP the entire central pool area, the "
    "voxel character and the gold inflatable ring EXACTLY as they are — do "
    "not move, resize, recolour, restyle or redraw any of the central "
    "content. Match the lighting, colour grade, top-down camera perspective "
    "and voxel / lego-block art style precisely. The final result is one "
    "seamless 16:9 image with no visible grey areas and no seams."
)

# --- Helpers -------------------------------------------------------------


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def pad_to_16x9(src: Path, dst: Path) -> Path:
    """Mittig auf eine graue 16:9-Leinwand legen (fuer Outpainting)."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target_w = round(h * 16 / 9)
    if target_w <= w:
        target_w = w
    canvas = Image.new("RGB", (target_w, h), (127, 127, 127))
    canvas.paste(im, ((target_w - w) // 2, 0))
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst)
    print(f"  Padded {src.name} {w}x{h} -> {target_w}x{h}  ({dst.name})")
    return dst


def save_image(url: str, name: str) -> Path:
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


def edit(step: str, image_url: str, prompt: str, name: str, stamp: str):
    """Ein nano-banana-pro/edit-Call. Gibt den lokalen Pfad zurueck (oder None)."""
    print(f"\n--- {step} ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            MODEL,
            arguments={
                "image_urls": [image_url],
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "num_images": 1,
            },
            with_logs=True,
            on_queue_update=on_queue,
        )
        elapsed = time.time() - t0
        urls = [img["url"] for img in result.get("images", [])]
        saved = None
        if urls:
            saved = save_image(urls[0], f"{name}_{stamp}")
        append_record({
            "run": stamp, "step": step, "model": MODEL,
            "prompt": prompt, "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1), "cost_est": "$0.04",
            "images": urls, "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"  OK in {elapsed:.1f}s -> {saved.name if saved else 'NO IMAGE'}")
        return saved
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "step": step, "model": MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        return None


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"POOL-BADEHOSE | statische Bilder | run {stamp} | ~$0.12")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    for p in (IMG_A, IMG_B):
        assert p.exists(), f"missing: {p}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- Bild A: schon 16:9, nur Outfit-Edit ---
    url_a = upload(IMG_A)
    edit("A_badehose (22_refined schraege Ansicht -> Badehose)",
         url_a, BADEHOSE_PROMPT, "A_badehose", stamp)

    # --- Bild B Schritt 1: hochkant -> 16:9 erweitern ---
    padded = pad_to_16x9(IMG_B, OUTPUT_DIR / f"B_padded_{stamp}.png")
    url_b_padded = upload(padded)
    b_wide = edit("B_16x9 (24_apose hochkant -> 16:9 erweitert)",
                  url_b_padded, OUTPAINT_PROMPT, "B_16x9", stamp)

    # --- Bild B Schritt 2: Outfit-Edit auf dem erweiterten Bild ---
    if b_wide:
        url_b_wide = upload(b_wide)
        edit("B_16x9_badehose (erweitertes Bild B -> Badehose)",
             url_b_wide, BADEHOSE_PROMPT, "B_16x9_badehose", stamp)
    else:
        print("\n  Schritt B_16x9 fehlgeschlagen — B_16x9_badehose uebersprungen.")

    print("\n" + "=" * 64)
    print(f"DONE -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
