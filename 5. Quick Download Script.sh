#!/bin/bash
# download_manuscript.sh
echo "Downloading Primordial Entanglement Manuscript..."

# Create directory structure
mkdir -p primordial_entanglement_manuscript/figures
mkdir -p primordial_entanglement_manuscript/sections

# Download main files
wget https://raw.githubusercontent.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement/main/manuscript/main.tex -O primordial_entanglement_manuscript/main.tex
wget https://raw.githubusercontent.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement/main/manuscript/references.bib -O primordial_entanglement_manuscript/references.bib

# Download figures
wget https://raw.githubusercontent.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement/main/manuscript/figures/verification.png -O primordial_entanglement_manuscript/figures/verification.png
wget https://raw.githubusercontent.com/tlcagford/Primordial-Photon-Dark-Photon-Entanglement/main/manuscript/figures/parameter_space.png -O primordial_entanglement_manuscript/figures/parameter_space.png

echo "Manuscript downloaded to primordial_entanglement_manuscript/"
echo "Compile with: pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex"