#!/usr/bin/env python3
"""
Schminkspiegel-CD — die Wangen-Punkte aus dem Ausgangsbild entfernen.

Basis: outputs/schminkspiegel_extend/ext_4x3_run2_20260602_140520.png
Die kleinen Stud-/Punkt-Markierungen auf den Wangen (links/rechts neben
Nase/Lippen) verursachen in der Animation Probleme -> entfernen, sonst
alles EXAKT erhalten. Danach dient das als neues Video-Ausgangsbild.

Zwei Methoden zum Vergleich (nano-edit x2 Seeds + FLUX Kontext).
4:3. Kein Negativ-Prompting. Parallel. ~3 Jobs, ~$0.16.
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
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "schminkspiegel_dedot"
RESULTS_FILE = SCRIPT_DIR / "schminkspiegel_dedot_results.json"

SRC = (SCRIPT_DIR / "outputs" / "schminkspiegel_extend"
       / "ext_4x3_run2_20260602_140520.png")

MAX_WORKERS = 3
_lock = threading.Lock()

PROMPT = (
    "Keep the entire image exactly as it is — the chrome hand, the open "
    "compact, the holographic CD, the chrome reflected face with its "
    "berry lips, the hoop earrings, the hair and the dark galaxy "
    "background — all unchanged. ONLY remove the small metal stud dots "
    "on the cheeks of the reflected chrome face (the little dots beside "
    "the nose on the left and right), leaving the cheeks as smooth clean "
    "mirror-chrome. Do not change anything else."
)

JOBS = [
    ("nano1", "fal-ai/nano-banana-pro/edit", "$0.04"),
    ("nano2", "fal-ai/nano-banana-pro/edit", "$0.04"),
    ("flux",  "fal-ai/flux-pro/kontext/max", "$0.08"),
]


def build_args(model_key, src_url):
    if model_key == "flux":
        return {"image_url": src_url, "prompt": PROMPT,
                "aspect_ratio": "4:3", "num_images": 1,
                "guidance_scale": 3.5, "safety_tolerance": "5"}
    return {"image_urls": [src_url], "prompt": PROMPT,
            "aspect_ratio": "4:3", "num_images": 1}


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


def run_job(model_key, endpoint, cost, src_url, stamp):
    label = f"dedot_{model_key}"
    name = f"dd_{model_key}_{stamp}"
    with _lock:
        print(f"  START  {label} | {endpoint}")
    t0 = time.time()
    try:
        result = fal_client.subscribe(
            endpoint, arguments=build_args(model_key, src_url),
            with_logs=False)
        elapsed = time.time() - t0
        url = first_url(result)
        saved = save_image(url, name)
        append_record({
            "run": stamp, "label": label, "model": model_key,
            "endpoint": endpoint, "src": SRC.name, "prompt": PROMPT,
            "elapsed_s": round(elapsed, 1), "cost_est": cost,
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
            "run": stamp, "label": label, "model": model_key,
            "endpoint": endpoint, "error": str(e),
            "elapsed_s": round(elapsed, 1),
            "timestamp": datetime.now().isoformat(),
        })
        with _lock:
            print(f"  ERROR  {label} ({elapsed:.1f}s): {e}")
        return False


def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("=" * 64)
    print(f"SCHMINKSPIEGEL DE-DOT | {len(JOBS)} Jobs PARALLEL | {stamp}")
    print("=" * 64)

    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set")
        return
    assert SRC.exists(), f"missing source: {SRC}"

    src_url = fal_client.upload_file(str(SRC))

    ok = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(run_job, mk, ep, c, src_url, stamp)
                   for mk, ep, c in JOBS]
        for fut in as_completed(futures):
            if fut.result():
                ok += 1

    print("\n" + "=" * 64)
    print(f"DONE {ok}/{len(JOBS)} ok -> {OUTPUT_DIR}")
    print("=" * 64)


if __name__ == "__main__":
    main()
