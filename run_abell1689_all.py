#!/usr/bin/env python3
"""
run_abell1689_all.py

Runs your P-D entanglement pipeline on *all* downloaded FITS files for Abell 1689.

- Downloads all HST SCIENCE FITS for Abell 1689 via MAST.
- Runs both validation and numerical results for each FITS.
- Saves a map, plot, and metadata JSON per file.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt

# -----------------------------
# User Configuration
# -----------------------------
REPO_ROOT = Path("/path/to/Primordial-Photon-Dark-Photon-Entanglement")  # <--- edit
OUTPUT_ROOT = Path("abell1689_full_runs")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
QUICK_MODE = False  # Set False if you want full runs

# Add your repo to Python path
sys.path.append(str(REPO_ROOT))

# Use astroquery to fetch all data
from astroquery.mast import Observations

print("Querying MAST for Abell 1689 HST observations...")
obs_table = Observations.query_criteria(target_name="Abell 1689", obs_collection="HST")
products = Observations.get_product_list(obs_table)
fits_products = Observations.filter_products(products, productType="SCIENCE", extension="fits")

if not fits_products:
    print("No FITS products; exiting.")
    sys.exit(1)

print(f"Found {len(fits_products)} FITS products. Downloading them...")
downloads = Observations.download_products(fits_products, download_dir=OUTPUT_ROOT / "fits")
fits_files = list((OUTPUT_ROOT / "fits").glob("*.fits"))
print(f"Downloaded {len(fits_files)} FITS files.")

# Import pipeline functions
try:
    from Physics_Validation_Tests import run_validation
    from Expected_Numerical_Results import compute_results
except ImportError as e:
    print("ERROR: Could not import pipeline functions. Check REPO_ROOT.")
    raise e

# Process each FITS
for fits_file in fits_files:
    print(f"Processing {fits_file.name} ...")
    result_valid = run_validation(fits_file, quick=QUICK_MODE)
    result_num = compute_results(fits_file, quick=QUICK_MODE)

    # Save a map if exists
    out_base = OUTPUT_ROOT / fits_file.stem
    out_base.mkdir(exist_ok=True)
    if "map" in result_valid:
        plt.figure(figsize=(6,5))
        plt.imshow(result_valid["map"], origin="lower", cmap="plasma")
        plt.colorbar(label="P-D Entanglement Signal")
        plt.title(f"Abell 1689 — {fits_file.name}")
        plot_file = out_base / "map.png"
        plt.savefig(plot_file, dpi=300)
        plt.close()
        print(f"Saved map to {plot_file}")

    # Save metadata
    metadata = {
        "object": "Abell 1689",
        "fits_file": str(fits_file),
        "timestamp": datetime.utcnow().isoformat(),
        "repo_commit": os.popen(f"git -C {REPO_ROOT} rev-parse HEAD").read().strip(),
        "quick_mode": QUICK_MODE,
        "valid_keys": list(result_valid.keys()),
        "num_keys": list(result_num.keys()),
        "validation": {k: float(result_valid[k]) if isinstance(result_valid[k], (int, float, np.generic)) else str(result_valid[k]) for k in result_valid},
        "numerical": {k: float(result_num[k]) if isinstance(result_num[k], (int, float, np.generic)) else str(result_num[k]) for k in result_num},
    }
    meta_file = out_base / "metadata.json"
    with open(meta_file, "w") as fh:
        json.dump(metadata, fh, indent=2)
    print(f"Saved metadata to {meta_file}")
