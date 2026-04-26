#!/bin/bash
set -e

# Ensure environment is active
source .venv/bin/activate

# Install any missing dependencies that weren't caught in the first pass
pip install jupytext pyarrow

# Run python scripts to process data and generate plots
echo "Running 01_data_loading.py..."
python scripts/01_data_loading.py

echo "Running 02_cleaning.py..."
python scripts/02_cleaning.py

echo "Running 03_feature_engineering.py..."
python scripts/03_feature_engineering.py

echo "Running 04_eda.py..."
python scripts/04_eda.py

echo "Running 05_statistical_analysis.py..."
python scripts/05_statistical_analysis.py > reports/statistical_analysis_results.txt

# Convert python scripts to ipynb notebooks in notebooks/ directory
echo "Generating notebooks..."
mkdir -p notebooks
jupytext --to notebook --output notebooks/01_data_loading.ipynb scripts/01_data_loading.py
jupytext --to notebook --output notebooks/02_cleaning.ipynb scripts/02_cleaning.py
jupytext --to notebook --output notebooks/03_feature_engineering.ipynb scripts/03_feature_engineering.py
jupytext --to notebook --output notebooks/04_eda.ipynb scripts/04_eda.py
jupytext --to notebook --output notebooks/05_statistical_analysis.ipynb scripts/05_statistical_analysis.py

echo "Pipeline complete."
