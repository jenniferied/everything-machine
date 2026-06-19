#!/usr/bin/env python3
"""
Sie-schreibt Unreal Combo — Cabrio + Voxel Char in die Unreal-Welten.

Idee: Unreal-Screenshots als Welt/Background-Ref, Cadillac + Voxel-Char
hineinkomponieren.

- Hexagon Neon Tunnel (UE5)  -> Cabrio rast durch Tunnel
- Kapuzenfigur Bergpanorama  -> wir lassen die Figur weg, nutzen Berg-Welt
  als Hintergrund, Cabrio davor (cap statt kapuze!)

Model: fal-ai/nano-banana-pro/edit (~$0.04/img)
4 Varianten = ~$0.16
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "sie_schreibt_unreal_combo"
RESULTS_FILE = SCRIPT_DIR / "sie_schreibt_unreal_combo_results.json"

INPUT_DIR = SCRIPT_DIR / "inputs" / "sie-schreibt"
REF_TUNNEL = INPUT_DIR / "unreal-hexagon-tunnel-neon.png"
REF_BERGE = INPUT_DIR / "unreal-kapuzenfigur-berge.png"
REF_CADILLAC = INPUT_DIR / "seedance-cadillac-frontal-mond.jpeg"
REF_VOXEL_CHAR = SCRIPT_DIR / "outputs" / "spiral_upscale" / "spiral_upscale_clarity_edited.png"

CHAR_DESC = (
    "Driver: small voxel/lego-style figure, light grey/white cubic blocks, "
    "dark baseball cap with flat curved brim (NOT a hood). Abstract minimal "
    "face."
)
CAR_DESC = (
    "Vintage lego-block convertible Cadillac, same as in the Cadillac "
    "reference: square chrome grille, four glowing headlights, sharp 1970s "
    "boxy silhouette, body assembled from lego-like blocks."
)
NEG = (
    "Avoid: hooded figure, hoodie, robe, monk, realistic human driver, "
    "deformed car, blurry car."
)

VARIANTS = [
    {
        "name": "01_cabrio_through_hex_tunnel",
        "refs": [REF_TUNNEL, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Edit the first image. Keep the surreal blue-neon hexagonal "
            f"tunnel exactly as is — its geometry, glowing edges, perspective "
            f"and color palette. Composite the Cadillac from the second "
            f"reference into the tunnel: the car is driving toward the camera "
            f"out of the hexagonal corridor, slightly off-center, headlights "
            f"blazing warm against the cool blue neon. Add the voxel character "
            f"from the third reference as driver, visible behind the "
            f"windshield. {CAR_DESC} {CHAR_DESC} The hexagonal neon light "
            f"reflects on the car's chrome and paint. Cinematic 16:9, "
            f"dramatic contrast. {NEG}"
        ),
    },
    {
        "name": "02_cabrio_at_tunnel_exit",
        "refs": [REF_TUNNEL, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Create a wide cinematic frame: the Cadillac from the second "
            f"reference has just exited the blue-neon hexagonal tunnel from "
            f"the first reference and is now driving on a dark road, the "
            f"glowing hexagonal tunnel mouth still visible behind it like a "
            f"portal. Voxel character driver from the third reference. "
            f"{CAR_DESC} {CHAR_DESC} Cool neon blue rim light on the car "
            f"from behind, warm headlights ahead. 16:9 cinematic. {NEG}"
        ),
    },
    {
        "name": "03_cabrio_at_kapuzenberge_wide",
        "refs": [REF_BERGE, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Edit the first image. REMOVE the cloaked/hooded figure "
            f"completely. KEEP the dramatic mountain landscape, the stormy "
            f"clouds, the desaturated grey-purple palette. Add the Cadillac "
            f"from the second reference parked on a rocky outcrop in the "
            f"foreground, three-quarter view, looking out over the mountains. "
            f"The voxel character driver from the third reference stands "
            f"beside the open driver door, looking out at the view, his cap "
            f"silhouetted against the sky. {CAR_DESC} {CHAR_DESC} "
            f"Cinematic 16:9. {NEG}"
        ),
    },
    {
        "name": "04_cabrio_mountain_road_serpentine",
        "refs": [REF_BERGE, REF_CADILLAC, REF_VOXEL_CHAR],
        "prompt": (
            f"Use the dramatic mountain landscape and cloudy-purple sky from "
            f"the first reference as the world. REMOVE the hooded figure. "
            f"Add a winding mountain road carved into the cliffs leading "
            f"toward the camera, and on it the Cadillac from the second "
            f"reference, headlights on, driving toward the viewer. Voxel "
            f"character driver visible. {CAR_DESC} {CHAR_DESC} "
            f"Cinematic 16:9. {NEG}"
        ),
    },
]


def upload(path):
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url, name):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if (".jpg" in url or "jpeg" in url) else ".png"
    out_path = OUTPUT_DIR / f"{name}{ext}"
    resp = httpx.get(url, timeout=120)
    out_path.write_bytes(resp.content)
    print(f"    Saved: {out_path.name} ({len(resp.content) // 1024}KB)")
    return out_path


def on_queue(update):
    if isinstance(update, fal_client.InProgress):
        for entry in update.logs:
            msg = entry.get("message", "")
            if msg:
                print(f"      [{msg}]")


def append_record(record):
    existing = []
    if RESULTS_FILE.exists():
        try:
            existing = json.loads(RESULTS_FILE.read_text())
        except Exception:
            existing = []
    existing.append(record)
    RESULTS_FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False))


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 60)
    print(f"UNREAL COMBO | run {stamp} | {len(VARIANTS)} ~${len(VARIANTS)*0.04:.2f}")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return

    refs_all = {REF_TUNNEL, REF_BERGE, REF_CADILLAC, REF_VOXEL_CHAR}
    for r in refs_all:
        assert r.exists(), f"missing: {r}"

    print("\nUploading references...")
    url_cache = {r: upload(r) for r in refs_all}

    model = "fal-ai/nano-banana-pro/edit"
    successes = 0

    for v in VARIANTS:
        print(f"\n--- {v['name']} ---")
        refs = [url_cache[r] for r in v["refs"]]
        t0 = time.time()
        try:
            result = fal_client.subscribe(
                model,
                arguments={
                    "image_urls": refs,
                    "prompt": v["prompt"],
                    "aspect_ratio": "16:9",
                    "num_images": 1,
                },
                with_logs=True,
                on_queue_update=on_queue,
            )
            elapsed = time.time() - t0
            urls = [img["url"] for img in result.get("images", [])]
            saved = []
            for i, url in enumerate(urls):
                suffix = "" if i == 0 else f"_{i}"
                name = f"{v['name']}_{stamp}{suffix}"
                p = save_image(url, name)
                saved.append(str(p.name))
            append_record({
                "run": stamp, "variant": v["name"], "model": model,
                "prompt": v["prompt"], "refs": [r.name for r in v["refs"]],
                "aspect_ratio": "16:9", "elapsed_s": round(elapsed, 1),
                "images": urls, "saved": saved,
                "timestamp": datetime.now().isoformat(),
            })
            print(f"  OK in {elapsed:.1f}s -> {saved}")
            successes += 1
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ERROR ({elapsed:.1f}s): {e}")
            append_record({
                "run": stamp, "variant": v["name"], "model": model,
                "error": str(e), "elapsed_s": round(elapsed, 1),
                "timestamp": datetime.now().isoformat(),
            })

    print("\n" + "=" * 60)
    print(f"DONE: {successes}/{len(VARIANTS)} -> {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
