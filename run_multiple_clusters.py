#!/usr/bin/env python3
"""
run_multiple_clusters.py

Runs your P-D entanglement pipeline on a list of clusters.
For each cluster:
- Downloads SCIENCE FITS (HST) via MAST.
- Runs validation + numerical pipeline on each FITS.
- Saves outputs (map, metadata) under one folder per cluster.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from astroquery.mast import Observations
import numpy as np
from matplotlib import pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
REPO_ROOT = Path("/path/to/Primordial-Photon-Dark-Photon-Entanglement")  # <--- edit
OUTPUT_ROOT = Path("cluster_runs")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
CLUSTERS = ["Abell 1689", "Abell 2218", "Coma"]  # add more target names as needed
QUICK_MODE = False  # or True for demo

sys.path.append(str(REPO_ROOT))
try:
    from Physics_Validation_Tests import run_validation
    from Expected_Numerical_Results import compute_results
except ImportError as e:
    print("ERROR: Could not import pipeline functions.")
    raise e

# Loop over clusters
for target in CLUSTERS:
    print(f"\n=== Processing target: {target} ===")
    target_dir = OUTPUT_ROOT / target.replace(" ", "_")
    fits_dir = target_dir / "fits"
    fits_dir.mkdir(parents=True, exist_ok=True)

    # Download FITS
    obs = Observations.query_criteria(target_name=target, obs_collection="HST")
    prods = Observations.get_product_list(obs)
    fits_prods = Observations.filter_products(prods, productType="SCIENCE", extension="fits")
    if not fits_prods:
        print(f"No FITS for {target}, skipping.")
        continue

    print(f"Downloading {len(fits_prods)} FITS products for {target} …")
    Observations.download_products(fits_prods, download_dir=fits_dir)
    fits_files = list(fits_dir.glob("*.fits"))
    print(f"Got {len(fits_files)} FITS files for {target}.")

    # Run pipeline on each
    for fits_file in fits_files:
        print(f"  → Running on {fits_file.name}")
        valid = run_validation(fits_file, quick=QUICK_MODE)
        numres = compute_results(fits_file, quick=QUICK_MODE)

        obj_out = target_dir / fits_file.stem
        obj_out.mkdir(exist_ok=True)

        if "map" in valid:
            plt.figure(figsize=(6,5))
            plt.imshow(valid["map"], origin="lower", cmap="viridis")
            plt.colorbar(label="P-D Ent. Signal")
            plt.title(f"{target} — {fits_file.name}")
            figfile = obj_out / "map.png"
            plt.savefig(figfile, dpi=300)
            plt.close()
            print("    Saved map:", figfile)

        metadata = {
            "target": target,
            "fits_file": str(fits_file),
            "timestamp": datetime.utcnow().isoformat(),
            "repo_commit": os.popen(f"git -C {REPO_ROOT} rev-parse HEAD").read().strip(),
            "quick_mode": QUICK_MODE,
            "valid_keys": list(valid.keys()),
            "numres_keys": list(numres.keys()),
            "validation": {k: float(valid[k]) if isinstance(valid[k], (int, float, np.generic)) else str(valid[k]) for k in valid},
            "numerical": {k: float(numres[k]) if isinstance(numres[k], (int, float, np.generic)) else str(numres[k]) for k in numres},
        }
        meta_file = obj_out / "metadata.json"
        with open(meta_file, "w") as fh:
            json.dump(metadata, fh, indent=2)
        print("    Saved metadata:", meta_file)
