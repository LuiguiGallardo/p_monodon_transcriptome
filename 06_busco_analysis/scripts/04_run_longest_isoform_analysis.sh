#!/bin/bash

# Script to run BUSCO analysis on P. monodon longest isoforms (one per gene)
# File: Trinity_longest_isoform.fasta
# Analysis: Assessment of gene set completeness (removing isoform redundancy)

# Configuration
TRANSCRIPTOME="/home/luigui/Documents/2026/p_monodon_transcriptome/02_assembly/01_trinity_output/Trinity_longest_isoform.fasta"
OUTPUT_DIR="../results"
THREADS=24

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "=========================================="
echo "BUSCO Analysis: Longest Isoforms (Gene Level)"
echo "=========================================="
echo "Input: ${TRANSCRIPTOME}"
echo "Threads: ${THREADS}"
echo "=========================================="
echo ""

# Activate environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate busco

# 1. Run Arthropoda Analysis
echo "Starting Arthropoda Analysis..."
busco \
    -i "${TRANSCRIPTOME}" \
    -o arthropoda_longest_isoform \
    -l "arthropoda_odb10" \
    -m "transcriptome" \
    -c "${THREADS}" \
    --out_path "${OUTPUT_DIR}" \
    --download_path "../downloads" \
    --force

# 2. Run Metazoa Analysis
echo ""
echo "Starting Metazoa Analysis..."
busco \
    -i "${TRANSCRIPTOME}" \
    -o metazoa_longest_isoform \
    -l "metazoa_odb10" \
    -m "transcriptome" \
    -c "${THREADS}" \
    --out_path "${OUTPUT_DIR}" \
    --download_path "../downloads" \
    --force

echo ""
echo "=========================================="
echo "Analysis Complete"
echo "=========================================="
