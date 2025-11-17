#!/usr/bin/env python3
"""
generate_abell_demo_local.py

Creates synthetic 'before' (raw) and 'after' (entanglement map) images
for Abell 2218, Abell 1689, and a synthetic interstellar comet.
Also writes a demo runner script, metadata, previews, and packages everything into a ZIP.

Output folder: ./abell_demo_package/
ZIP: ./abell_demo_package.zip
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import zipfile
import os

# Optional: if scipy is available, the entanglement simulation uses gaussian_filter
try:
    from scipy.ndimage import gaussian_filter
except Exception:
    gaussian_filter = None

OUT_DIR = Path("./abell_demo_package")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def make_cluster_image(seed, nx=1024, ny=1024, core=200):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:ny, 0:nx]
    cx, cy = nx//2 + rng.integers(-40,40), ny//2 + rng.integers(-40,40)
    r = np.sqrt((x-cx)**2 + (y-cy)**2)
    profile = core / (1 + (r/80.0)**2)
    sub = rng.normal(0, 0.02*core, size=(ny,nx)) * np.exp(-r/200.0)
    data = profile + sub
    for _ in range(20):
        gx = rng.integers(0,nx); gy = rng.integers(0,ny)
        amp = rng.uniform(5,30); s = rng.integers(2,6)
        data += amp * np.exp(-(((x-gx)**2)/(2*s**2) + ((y-gy)**2)/(2*s**2)))
    data += rng.normal(0, 5, size=(ny,nx))
    return data

def make_comet_image(seed, nx=1024, ny=1024):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:ny, 0:nx]
    cx, cy = rng.integers(300, 724), rng.integers(300,724)
    r = np.sqrt((x-cx)**2 + (y-cy)**2)
    coma = 300 * np.exp(-r/200.0)
    tail = np.exp(-((x - cx - 200)**2)/(2*80**2)) * np.exp(-((y-cy)**2)/(2*200**2))
    data = coma + 50*tail
    for _ in range(150):
        gx = rng.integers(0,nx); gy = rng.integers(0,ny)
        amp = rng.uniform(2,15); s = rng.integers(1,3)
        data += amp * np.exp(-(((x-gx)**2)/(2*s**2) + ((y-gy)**2)/(2*s**2)))
    data += rng.normal(0, 8, size=(ny,nx))
    return data

def simulate_entmap(raw, seed=0, strength=1.0):
    rng = np.random.default_rng(seed)
    if gaussian_filter is not None:
        norm = (raw - np.median(raw)) / (np.std(raw)+1e-9)
        smooth = gaussian_filter(norm, sigma=10)
        pattern = 0.2 * gaussian_filter(rng.normal(0,1,raw.shape), sigma=30)
        ent = strength * smooth + pattern
    else:
        # fallback smoothing if scipy not installed
        ent = np.copy(raw)
        ent = (ent - np.min(ent)) / (np.max(ent) - np.min(ent) + 1e-9)
        # apply a simple low-pass by block-averaging
        kernel = 8
        ent = ent.reshape((ent.shape[0]//kernel, kernel, ent.shape[1]//kernel, kernel)).mean(axis=(1,3))
        ent = np.repeat(np.repeat(ent, kernel, axis=0), kernel, axis=1)
    return ent

def save_png(data, path, cmap='gray'):
    plt.figure(figsize=(6,6))
    plt.imshow(data, origin='lower', cmap=cmap)
    plt.axis('off')
    plt.savefig(path, bbox_inches='tight', pad_inches=0.02, dpi=150)
    plt.close()

# Generate raw images
a2218_raw = make_cluster_image(seed=42)
a1689_raw = make_cluster_image(seed=84)
comet_raw = make_comet_image(seed=123)

# Generate entanglement maps
a2218_ent = simulate_entmap(a2218_raw, seed=5, strength=1.0)
a1689_ent = simulate_entmap(a1689_raw, seed=6, strength=0.8)
comet_ent = simulate_entmap(comet_raw, seed=7, strength=1.5)

# Save PNG previews (reduced sizes)
save_png(a2218_raw, OUT_DIR / "Abell2218_raw.png")
save_png(a2218_ent, OUT_DIR / "Abell2218_entmap.png", cmap='plasma')
save_png(a1689_raw, OUT_DIR / "Abell1689_raw.png")
save_png(a1689_ent, OUT_DIR / "Abell1689_entmap.png", cmap='plasma')
save_png(comet_raw, OUT_DIR / "Comet_raw.png")
save_png(comet_ent, OUT_DIR / "Comet_entmap.png", cmap='plasma')

# Create demo runner script (reads PNGs, saves before/after composite and summary)
demo_runner = r'''#!/usr/bin/env python3
"""
demo_run_pngs.py - Compose before/after images and write a JSON summary.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.image as mpimg

DATA_DIR = Path(__file__).parent
pairs = [
    ("Abell2218_raw.png", "Abell2218_entmap.png"),
    ("Abell1689_raw.png", "Abell1689_entmap.png"),
    ("Comet_raw.png", "Comet_entmap.png"),
]

summary = {}
for raw_fn, ent_fn in pairs:
    raw_p = DATA_DIR / raw_fn
    ent_p = DATA_DIR / ent_fn
    if not raw_p.exists() or not ent_p.exists():
        print(f"Missing {raw_fn} or {ent_fn}, skipping.")
        continue
    raw = mpimg.imread(raw_p)
    ent = mpimg.imread(ent_p)
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(8,4))
    ax1.imshow(raw)
    ax1.set_title(raw_fn.replace('_',' '))
    ax1.axis('off')
    ax2.imshow(ent)
    ax2.set_title(ent_fn.replace('_',' '))
    ax2.axis('off')
    outpng = DATA_DIR / (raw_p.stem + "_before_after.png")
    plt.savefig(outpng, bbox_inches='tight', pad_inches=0.02, dpi=150)
    plt.close()
    summary[raw_p.stem] = {
        "raw_mean": float(np.mean(raw)),
        "raw_std": float(np.std(raw)),
        "ent_mean": float(np.mean(ent)),
        "ent_std": float(np.std(ent))
    }

with open(DATA_DIR / "demo_png_summary.json","w") as fh:
    json.dump(summary, fh, indent=2)
print("Done. Summary saved to demo_png_summary.json")
'''

(demo_path := OUT_DIR / "demo_run_pngs.py").write_text(demo_runner)
os.chmod(demo_path, 0o755)

# Write metadata and README
metadata = {
    "objects": [
        {"name":"Abell 2218","raw":"Abell2218_raw.png","entmap":"Abell2218_entmap.png"},
        {"name":"Abell 1689","raw":"Abell1689_raw.png","entmap":"Abell1689_entmap.png"},
        {"name":"Interstellar Comet (synthetic)","raw":"Comet_raw.png","entmap":"Comet_entmap.png"}
    ],
    "note":"Synthetic PNG demo package created for repository demo purposes."
}
with open(OUT_DIR / "demo_png_metadata.json","w") as fh:
    json.dump(metadata, fh, indent=2)

with open(OUT_DIR / "README_demo.txt","w") as fh:
    fh.write("""Abell PNG Demo Package

This package contains synthetic PNG images (raw and 'entanglement map' processed versions)
for Abell 2218, Abell 1689, and a synthetic interstellar comet.
Files:
- Abell2218_raw.png, Abell2218_entmap.png
- Abell1689_raw.png, Abell1689_entmap.png
- Comet_raw.png, Comet_entmap.png
- demo_run_pngs.py - script that composes before/after images and writes demo_png_summary.json
- demo_png_metadata.json - metadata about contents

Run:
python demo_run_pngs.py
""")

# Create ZIP package
zip_path = Path("./abell_demo_package.zip")
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for p in OUT_DIR.rglob("*"):
        zf.write(p, arcname=p.relative_to(OUT_DIR))

print("Package created:", zip_path.resolve())
print("Files in package directory:", [p.name for p in OUT_DIR.iterdir()])
