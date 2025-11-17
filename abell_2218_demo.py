# Abell 2218 Demo Pipeline
# Download FITS from MAST, run validation + numerical tests, produce before/after maps

from astroquery.mast import Observations
from pathlib import Path
from astropy.io import fits
import matplotlib.pyplot as plt
from Physics_Validation_Tests import run_validation
from Expected_Numerical_Results import compute_results

# Step 1: Download data
target = "Abell 2218"
out_dir = Path("demo_data/Abell2218")
out_dir.mkdir(parents=True, exist_ok=True)

obs_table = Observations.query_criteria(target_name=target, obs_collection="HST")
products = Observations.get_product_list(obs_table)
fits_products = Observations.filter_products(products, productType="SCIENCE", extension="fits")

# Download a few FITS files
downloaded = Observations.download_products(fits_products[:2], download_dir=out_dir)
print("Downloaded:", downloaded)

# Step 2: Process data
fits_files = list(out_dir.glob("*.fits"))
results = []

for f in fits_files:
    print("Processing:", f)
    val = run_validation(f, quick=True)
    num = compute_results(f, quick=True)
    results.append((f, val, num))

    # Save validation map if present
    ent_map = val.get("map")
    if ent_map is not None:
        raw = fits.getdata(f)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(raw, origin='lower', cmap='gray')
        ax1.set_title("Abell 2218 Raw")
        ax2.imshow(ent_map, origin='lower', cmap='plasma')
        ax2.set_title("P–D Entanglement Map")
        fig.savefig(out_dir / f"{f.stem}_before_after.png", dpi=200)
        plt.close(fig)

# Step 3: Save summary
with open(out_dir / "abell2218_summary.txt", "w") as fsum:
    for f, val, num in results:
        fsum.write(f"File: {f}\nValidation: {val}\nNumerical: {num}\n\n")
