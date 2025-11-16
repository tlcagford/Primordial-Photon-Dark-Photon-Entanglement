# Test conda environment
conda env create -f environment.yaml
conda activate primordial-entanglement
python src/main.py

# Test pip installation
pip install -r requirements.txt
python src/main.py