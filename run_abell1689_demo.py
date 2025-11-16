#!/usr/bin/env python3
"""
run_abell1689_demo.py

Demo pipeline for running the Primordial-Photon-Dark-Photon-Entanglement repo
on Abell 1689 HST data.

Requirements:
- Python 3.10+
- astroquery, astropy, numpy, matplotlib
- Your cloned repo accessible at REPO_ROOT

Author: Tony E. Ford
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
REPO_ROOT = Path("/path/to/Primordial-Photon-Dark-Photon-Entanglement")  # <--- EDIT
DEMO_DIR = Path("mast_downloads/Abell1689")
DEMO_DIR.mkdir(parents=True, exist_ok=True)
QUICK_MODE = True  # True = small demo, False = full processing

# -----------------------------
# Add repo to sys.path
# -----------------------------
sys.path.append(str(REPO_ROOT))

# -----------------------------
# Astroquery to fetch Abell 1689 data
# -----------------------------
from astroquery.mast import Observations

print("Searching for Abell 1689 HST observations...")
obs_table = Observations.query_criteria(target_name="Abell 1689", obs_collection="HST")
products = Observations.get_product_list(obs_table)
fits_products = Observations.filter_products(products, productType="SCIENCE", extension="fits")

if not fits_products:
    raise RuntimeError("No SCIENCE FITS products found for Abell 1689")

# Download first 2 FITS files for demo
downloads = Observations.download_products(fits_products[:2], download_dir=DEMO_DIR)
fits_files = list(DEMO_DIR.glob("*.fits"))
print(f"Downloaded {len(fits_files)} FITS files.")

# -----------------------------
# Import your repo scripts
# -----------------------------
try:
    from Physics_Validation_Tests import run_validation  # adjust if function name differs
    from Expected_Numerical_Results import compute_results  # adjust as needed
except ImportError:
    print("ERROR: Could not import repo scripts. Check REPO_ROOT path and function names.")
    sys.exit(1)

# -----------------------------
# Run pipeline on first FITS file
# -----------------------------
demo_file = fits_files[0]
print(f"Running demo on {demo_file.name}...")

validation_result = run_validation(demo_file, quick=QUICK_MODE)
numeric_result = compute_results(demo_file, quick=QUICK_MODE)

print("Validation Result:", validation_result)
print("Numerical Result:", numeric_result)

# -----------------------------
# Generate demo plot
# -----------------------------
if "map" in validation_result:
    plt.figure(figsize=(6,5))
    plt.imshow(validation_result['map'], origin='lower', cmap='plasma')
    plt.colorbar(label="P-D Entanglement Signal (arb units)")
    plt.title(f"Abell 1689 – P-D Entanglement Map ({demo_file.name})")
    plt.savefig("abell1689_demo.png", dpi=300)
    plt.show()
else:
    print("No 'map' key in validation_result, skipping plot.")

# -----------------------------
# Save run metadata
# -----------------------------
metadata = {
    "object": "Abell 1689",
    "fits_file": str(demo_file),
    "timestamp": datetime.utcnow().isoformat(),
    "repo_commit": os.popen("git -C {} rev-parse HEAD".format(REPO_ROOT)).read().strip(),
    "quick_mode": QUICK_MODE,
    "validation_keys": list(validation_result.keys()),
    "numeric_keys": list(numeric_result.keys())
}

with open("abell1689_demo_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("Demo run complete. Metadata saved to abell1689_demo_metadata.json")
