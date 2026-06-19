#!/usr/bin/env python3
"""
Schminkspiegel-CD — ENDFRAME bauen: nur die CD gedreht, Rest identisch.

Zweck: fuer Seedance 2.0 start->end Interpolation. Startframe = Basis,
Endframe = exakt gleiches Bild, aber die holografische Scheibe ist um
ihre Mitte GEDREHT (Regenbogen-Strahlen zeigen woanders hin). Das
erzwingt eine echte CD-Drehung bei FIXER Kamera und STILLEM Gesicht.

Basis: outputs/schminkspiegel_dedot2/dd_flux_20260602_150012.jpg
nano-banana-pro/edit, 2 Kandidaten (verschiedene Dreh-Betraege/Seeds).
4:3. Kein Negativ-Prompting. Parallel.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_endframe"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_endframe_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_dedot2"
       / "dd_flux_20260602_150012.jpg")

ENDPOINT = "fal-ai/nano-banana-pro/edit"
MAX_WORKERS = 2
_lock = threading.Lock()

# Nur die Scheibe drehen, Form/Position/Lochmitte + alles andere bleibt.
def rot_prompt(deg: str) -> str:
    return (
        "Keep this entire image perfectly identical — the chrome hand, "
        "the open compact, the chrome reflected face, the closed berry "
        "lips, the hoop earrings, the hair, the dark galaxy background "
        "and the exact framing — all completely unchanged. The ONLY "
        "change: rotate the holographic rainbow light pattern on the "
        "round disc around its centre by about " + deg + ", so the "
        "coloured radial streaks now point in a clearly different "
        "direction, as if the disc has turned. Keep the disc's round "
        "elliptical shape, its position, size and centre hole exactly "
        "the same — only its rainbow streaks are rotated. Nothing else "
        "moves or changes."
    )

CANDIDATES = [
    {"name": "end_rot120", "deg": "120 degrees clockwise"},
    {"name": "end_rot200", "deg": "200 degrees clockwise"},
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


def run_job(c, src_url, stamp):
    prompt = rot_prompt(c["deg"])
    name = f"{c['name']}_{stamp}"
    args = {"image_urls": [src_url], "prompt": prompt,
            "aspect_ratio": "4:3", "num_images": 1}
    with _lock:
        print(f"  START  {c['name']}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(ENDPOINT, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "name": c["name"], "endpoint": ENDPOINT,
            "src": SRC.name, "prompt": prompt,
            "elapsed_s": round(elapsed, 1), "image": url,
            "saved": saved.name if saved else None,
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  DONE   {c['name']} ({elapsed:.1f}s) -> "
                  f"{saved.name if saved else 'NO IMAGE'}")
        return True
    except Exception as e:
        elapsed = time.time() - t0
        append_record({
            "run": stamp, "name": c["name"], "endpoint": ENDPOINT,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {c['name']} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL ENDFRAME (rotate disc only) | {stamp}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SRC.exists(), f"missing source: {SRC}"

    src_url = fal_client.upload_file(str(SRC))

    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, c, src_url, stamp) for c in CANDIDATES]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(CANDIDATES)} ok -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
