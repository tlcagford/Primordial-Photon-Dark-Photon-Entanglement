# Primordial Photon-Dark Photon Entanglement
## Quick start (reproducibility)
1. Install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Numerical simulation of quantum entanglement between photons and dark photons in the early universe*

## 📖 Abstract

This repository contains the complete code and data for studying primordial entanglement between photons and dark photons. We solve the von Neumann equation for a coupled photon-dark photon system in an expanding universe, quantifying the generation of quantum entanglement and its implications for dark matter.

## 🚀 Quick Start

### Option 1: Using conda (Recommended)
```bash
git clone https://github.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement.git
cd Primordial-Photon-Dark-Photon-Entanglement
conda env create -f environment.yaml
conda activate primordial-entanglement
python src/main.py
