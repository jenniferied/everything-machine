#!/usr/bin/env python3
"""
Schminkspiegel-CD — Berry-Favorit auf LANDSCAPE 4:3 outpainten.

Favorit: outputs/schminkspiegel_recolor_berry/
         rb_M4_seedream_run1_20260602_123415.png  (3072x4096, Hochformat)

Ziel: nur LINKS und RECHTS erweitern (Motiv mittig, oben/unten exakt
erhalten) bis LANDSCAPE 4:3 (breiter als hoch). Echtes Outpainting mit
fal-ai/bria/expand — die Originalpixel bleiben erhalten, nur die
Seitenstreifen werden neu als dunkle Galaxie generiert.

Mathe (exakt 4:3):
  Quelle auf Hoehe 1536 skaliert -> 1152x1536 (3:4 bleibt).
  Leinwand 2048x1536 (4:3 landscape). Original mittig:
  loc_x = (2048-1152)/2 = 448, loc_y = 0  -> nur Seiten werden generiert.

Zwei Seeds zum Vergleich. Kein Negativ-Prompting (Fortsetzung positiv
beschrieben). ~2 Jobs, ~$0.08.
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
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_extend"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_extend_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_recolor_berry"
       / "rb_M4_seedream_run1_20260602_123415.png")

EXPAND_MODEL = "fal-ai/bria/expand"

# Ziel-Geometrie (exakt 4:3 landscape)
ORIG_H = 1536
CANVAS_W, CANVAS_H = 2048, 1536

EXPAND_PROMPT = (
    "Deep black outer space continuing seamlessly outward to the left "
    "and right — near-total black with a few faint distant stars and a "
    "subtle deep-blue nebula haze, exactly matching and continuing the "
    "existing dark galaxy background, smooth seamless extension of the "
    "same scene, chrome arm and dark cosmos."
)

MAX_WORKERS = 2
_lock = threading.Lock()


def first_url(result) -> str:
    if isinstance(result.get("image"), dict):
        return result["image"].get("url", "")
    if isinstance(result.get("image"), str):
        return result["image"]
    if isinstance(result.get("images"), list) and result["images"]:
        item = result["images"][0]
        return item.get("url", "") if isinstance(item, dict) else item
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


def prepare_source() -> tuple[str, int, int]:
    """Quelle auf ORIG_H skalieren, hochladen. Gibt (url, w, h)."""
    with Image.open(SRC) as im:
        w0, h0 = im.size
        new_w = round(w0 * ORIG_H / h0)
        resized = im.resize((new_w, ORIG_H), Image.LANCZOS)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_DIR / "_src_resized.png"
        resized.save(tmp)
    print(f"  Source {w0}x{h0} -> resized {new_w}x{ORIG_H}")
    url = fal_client.upload_file(str(tmp))
    return url, new_w, ORIG_H


def run_job(idx, src_url, ow, oh, stamp):
    loc_x = (CANVAS_W - ow) // 2
    label = f"extend_4x3__run{idx}"
    name = f"ext_4x3_run{idx}_{stamp}"
    args = {
        "image_url": src_url,
        "canvas_size": [CANVAS_W, CANVAS_H],
        "original_image_size": [ow, oh],
        "original_image_location": [loc_x, 0],
        "prompt": EXPAND_PROMPT,
    }
    with _lock:
        print(f"  START  {label} | canvas {CANVAS_W}x{CANVAS_H} | "
              f"orig at x={loc_x}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(EXPAND_MODEL, arguments=args,
                                      with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "model": EXPAND_MODEL,
            "src": SRC.name, "canvas_size": [CANVAS_W, CANVAS_H],
            "original_image_size": [ow, oh],
            "original_image_location": [loc_x, 0],
            "prompt": EXPAND_PROMPT, "elapsed_s": round(elapsed, 1),
            "cost_est": "$0.04", "image": url,
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
            "run": stamp, "label": label, "model": EXPAND_MODEL,
            "error": str(e), "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL EXTEND -> LANDSCAPE 4:3 | {stamp} | ~$0.08")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SRC.exists(), f"missing source: {SRC}"

    src_url, ow, oh = prepare_source()

    wall0 = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, i, src_url, ow, oh, stamp)
                   for i in (1, 2)]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    wall = time.time() - wall0
    print("\n" + "=" * 64)
    print(f"DONE {ok}/2 ok | wall {wall:.1f}s -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
