#!/usr/bin/env python3
"""
Behind-Chase ROAD — Startbild mit deutscher Landstrasse.

Nimmt das letzte Bordeaux-Bild und aendert NUR die Strasse: aus dem
unklaren US-Mehrspur-Layout mit doppelter gelber Linie wird eine
deutsche Landstrasse — zwei Spuren (je eine pro Richtung), getrennt
durch eine einzelne weisse Strichlinie. Das Auto faehrt auf der RECHTEN
Spur (Strichlinie links neben dem Auto im Bild).

Auto, Kennzeichen 'KEP - LE 18', Mond, Berge, Charakter, Bordeaux-Lack
und violettes Grading bleiben unveraendert.

Hinweis Kopf-Konsistenz: in der naechsten Video-Generierung lassen wir
das Wort 'Lego' ganz weg (Jennifers Beobachtung: das Wort triggert
vermutlich genau den Effekt, den wir vermeiden wollen — Anchoring).
Stattdessen positiv beschreiben: 'Minecraft-style cubic voxel block
cluster head', nichts Negatives.

Model: fal-ai/nano-banana-pro/edit  (~$0.04)
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "behind_chase_recolor"
RESULTS_FILE = SCRIPT_DIR / "behind_chase_recolor_results.json"

REF_IMAGE = (
    SCRIPT_DIR / "outputs" / "behind_chase_recolor"
    / "behind_chase_bordeaux_20260527_100556.png"
)


PROMPT = (
    "Edit the image. KEEP EVERYTHING EXACTLY: same composition, same "
    "framing (camera directly behind the bordeaux convertible Cadillac at "
    "road level), the full moon high in the starry sky, distant mountains, "
    "the violet-leaning moonlit color grading, the voxel character driver "
    "with his dark baseball cap and brown voxel hair, the rear license "
    "plate 'KEP - LE 18' (German plate, must stay sharp and legible), the "
    "red tail-light glow, the bordeaux paint. Do NOT change car colour, "
    "plate, character, moon, mountains or framing. "
    "Make ONLY this change: redesign the road as a German country highway "
    "(Landstrasse). The road must have EXACTLY TWO LANES total — one lane "
    "in each direction, separated in the middle by a SINGLE WHITE DASHED "
    "CENTER LINE (broken white dashes, evenly spaced, painted on dark "
    "asphalt). There must NOT be any yellow lines anywhere on the road. "
    "There must NOT be more than two lanes. The right edge of the road is "
    "just asphalt fading into the sandy desert shoulder. The Cadillac is "
    "driving in the RIGHT LANE (its lane of travel) — so the white dashed "
    "center line runs along the LEFT side of the car (from the camera's "
    "view, slightly left of the car), and the open second lane on the far "
    "left is for oncoming traffic but is empty. The road surface stays "
    "the same dark asphalt; the dashed line is fresh clean white paint. "
    "Receding into the horizon naturally with one-point perspective."
)


def upload(path: Path) -> str:
    print(f"  Uploading {path.name}...")
    return fal_client.upload_file(str(path))


def save_image(url: str, name: str) -> Path:
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


def append_record(record: dict):
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
    print(f"BEHIND-CHASE ROAD (deutsche Landstrasse) | run {stamp} | ~$0.04")
    print("=" * 60)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert REF_IMAGE.exists(), f"missing: {REF_IMAGE}"

    print("\nUploading...")
    ref_url = upload(REF_IMAGE)

    model = "fal-ai/nano-banana-pro/edit"
    print(f"\n--- landstrasse ---")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            model,
            arguments={
                "image_urls": [ref_url],
                "prompt": PROMPT,
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
            saved.append(str(save_image(url, f"behind_chase_landstrasse_{stamp}{suffix}").name))
        append_record({
            "run": stamp, "model": model, "prompt": PROMPT,
            "refs": [REF_IMAGE.name], "aspect_ratio": "16:9",
            "elapsed_s": round(elapsed, 1),
            "images": urls, "saved": saved,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"\n  OK in {elapsed:.1f}s -> {saved}")
        print(f"  Outputs: {OUTPUT_DIR}")
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR ({elapsed:.1f}s): {e}")
        append_record({
            "run": stamp, "model": model, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })


if __name__ == "__main__":
    main()
