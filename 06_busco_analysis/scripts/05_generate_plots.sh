#!/bin/bash

# Script to generate BUSCO visualization plots
# Creates publication-quality bar plots for BUSCO results

echo "=========================================="
echo "BUSCO Visualization Generator"
echo "=========================================="
echo ""

# Activate conda environment
echo "Activating BUSCO conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate busco

# Check if matplotlib is installed
echo "Checking dependencies..."
python -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "matplotlib not found. Installing..."
    conda install -y -c conda-forge matplotlib
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install matplotlib"
        exit 1
    fi
fi

echo "✓ Dependencies ready"
echo ""

# Run the plotting script
echo "Generating BUSCO plots..."
python 05_generate_plots.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Success! Plots generated."
    echo "=========================================="
    echo ""
    echo "View your plots in: ../results/figures/"
else
    echo ""
    echo "ERROR: Plot generation failed"
    exit 1
fi
