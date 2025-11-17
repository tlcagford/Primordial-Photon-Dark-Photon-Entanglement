[updated_readme.md](https://github.com/user-attachments/files/23573346/updated_readme.md)
# Primordial Photon–Dark Photon Entanglement

A research and analysis framework for testing the **Photon–Dark Photon Entanglement Hypothesis**, analyzing astronomical imaging data, and generating reproducible physics validation results using HST, JWST, and other observatory FITS products.

---

## 🚀 Overview
This repository provides:

- **Physics Validation Tests** that compute predicted P–D entanglement observables.
- **Expected Numerical Results** for cross‑checking model predictions.
- **Automated pipelines** for running analyses on clusters (e.g., *Abell 1689*) and other astrophysical targets.
- **Jupyter notebooks** for full end‑to‑end scientific workflows.
- **Data ingestion tools** for MAST/HST/JWST FITS downloads.

---

## 📂 Repository Structure

```
Primordial-Photon-Dark-Photon-Entanglement/
├── Physics_Validation_Tests.py
├── Expected_Numerical_Results.py
├── utils/
│   ├── preprocessing.py
│   ├── fits_tools.py
│   └── visualization.py
├── notebooks/
│   ├── Photon_DarkPhoton_Cluster_Analysis.ipynb
│   └── JWST_COSMOS_Advanced.ipynb (optional)
└── README.md
```

---

## 🧪 Running Analyses

### **Quickstart Example (Abell 1689)**

```bash
python run_abell1689_demo.py
```

Outputs include:
- Processed maps
- Numerical validation results
- Metadata JSON
- PNGs of reconstructed entanglement signals

A full Jupyter notebook version is included in:
```
notebooks/Photon_DarkPhoton_Cluster_Analysis.ipynb
```

---

## 📥 Data Sources Supported
- **Hubble Space Telescope (HST)** via **MAST**
- **JWST NIRCam/MIRI**, including COSMOS-Web
- **MeerKAT / SKA FITS** (optional extensions)
- Any standard FITS file with WCS metadata

---

## 📊 Outputs
The pipeline produces:
- Entanglement maps
- Numerical validation tables
- Model deviation/error metrics
- Reproducible metadata packages

---

## ⚙️ Installation

```bash
git clone https://github.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement
cd Primordial-Photon-Dark-Photon-Entanglement
pip install -r requirements.txt
```

---

## 📝 Licensing
This project uses a **Dual-License model**:

- **Commercial License**: Required for for-profit, enterprise, or corporate use.
- **Open Academic & Personal License**: Free for academic research, public study, and personal exploration.

See the `LICENSE` file for details.

Badge:
```
![License: Dual License](https://img.shields.io/badge/license-Dual--License-blue)
```

---

## 🤝 Contributing
Pull requests are welcome.
For major changes, open an issue to discuss your proposal.

A Contributor License Agreement (CLA) may be required for future releases.

---

## 📫 Contact
Author: **Tony E. Ford**  
Independent Researcher / Astrophysics & Quantum Systems

