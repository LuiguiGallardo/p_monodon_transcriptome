#!/bin/bash

# Script to run isoform differential expression analysis for a single iteration
# Usage: ./run_isoform_de_single.sh <iteration_number>

# Activate Trinity conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate trinity

ITER_NUM=${1:-1}  # Default to iteration 1 if not specified

ROOT_DIR=$(pwd)
TRINITY_FASTA="Trinity.fasta"
GENE_MAP="Trinity.fasta.gene_trans_map"
METADATA_DIR="metadata_iterations"
RESULTS_BASE_DIR="results_iterations"

echo "Running isoform DE analysis for iteration $ITER_NUM..."

METADATA_FILE="${ROOT_DIR}/${METADATA_DIR}/metadata_trinity_iter_${ITER_NUM}.txt"
ITER_DIR="${RESULTS_BASE_DIR}/iter_${ITER_NUM}"

# Check if iteration directory exists
if [ ! -d "$ITER_DIR" ]; then
    echo "Error: Iteration directory not found: $ITER_DIR"
    exit 1
fi

# Check if isoform matrix exists
if [ ! -f "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" ]; then
    echo "Error: Isoform counts matrix not found"
    exit 1
fi

# Create deseq2_isoforms directory
DE_ISOFORMS_DIR="${ITER_DIR}/deseq2_isoforms"
mkdir -p "$DE_ISOFORMS_DIR"

echo "  Running DESeq2 on isoform matrix..."
$TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
    --matrix "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" \
    --samples_file "$METADATA_FILE" \
    --method DESeq2 \
    --output "$DE_ISOFORMS_DIR"

# Enter isoforms DE directory to run downstream analysis
cd "$DE_ISOFORMS_DIR"

REL_ISO_MATRIX_TMM="${ROOT_DIR}/${ITER_DIR}/RSEM_matrix.isoform.TMM.EXPR.matrix"

# Analyze differential expression for isoforms
echo "  Analyzing differential expression..."
$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4

# Return to root
cd "$ROOT_DIR"

echo "✓ Isoform DE analysis complete for iteration $ITER_NUM!"
echo "Results are in: $DE_ISOFORMS_DIR"
