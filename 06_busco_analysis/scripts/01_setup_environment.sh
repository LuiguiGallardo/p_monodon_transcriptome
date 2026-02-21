#!/bin/bash

# Script to create and setup BUSCO conda environment
# BUSCO (Benchmarking Universal Single-Copy Orthologs) is used to assess
# the completeness of genome and transcriptome assemblies

echo "Creating conda environment for BUSCO analysis..."

# Create conda environment with BUSCO and dependencies
conda create -n busco -c conda-forge -c bioconda busco=5.7.1 -y

echo ""
echo "BUSCO environment created successfully!"
echo ""
echo "To activate the environment, run:"
echo "  conda activate busco"
echo ""
echo "To verify installation, run:"
echo "  conda activate busco"
echo "  busco --version"
