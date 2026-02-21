#!/bin/bash

# Script to run isoform differential expression analysis for all 40 iterations
# This script processes existing iteration directories and adds isoform DE analysis

# Activate Trinity conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate trinity

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
ROOT_DIR="${BASE_DIR}"

TRINITY_FASTA="${BASE_DIR}/data/Trinity.fasta"
GENE_MAP="${BASE_DIR}/data/Trinity.fasta.gene_trans_map"
METADATA_DIR="${BASE_DIR}/metadata/metadata_iterations"
RESULTS_BASE_DIR="${BASE_DIR}/results/results_iterations"

echo "=========================================="
echo "Running isoform DE analysis for all 40 iterations"
echo "=========================================="

# Loop through iterations 1 to 40
for i in {1..40}; do
    echo ""
    echo "Processing Iteration $i..."
    
    METADATA_FILE="${METADATA_DIR}/metadata_trinity_iter_${i}.txt"
    ITER_DIR="${RESULTS_BASE_DIR}/iter_${i}"
    
    # Check if iteration directory exists
    if [ ! -d "$ITER_DIR" ]; then
        echo "  Warning: Iteration directory not found: $ITER_DIR - skipping"
        continue
    fi
    
    # Check if isoform matrix exists
    if [ ! -f "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" ]; then
        echo "  Warning: Isoform counts matrix not found - skipping"
        continue
    fi
    
    # Check if deseq2_isoforms already exists
    DE_ISOFORMS_DIR="${ITER_DIR}/deseq2_isoforms"
    if [ -d "$DE_ISOFORMS_DIR" ] && [ -f "${DE_ISOFORMS_DIR}/RSEM_matrix.isoform.counts.matrix.WSSV_infection_vs_knockdown_PmSTAT.DESeq2.DE_results" ]; then
        echo "  Isoform DE results already exist - skipping"
        continue
    fi
    
    # Create deseq2_isoforms directory
    mkdir -p "$DE_ISOFORMS_DIR"
    
    echo "  Running DESeq2 on isoform matrix..."
    $TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
        --matrix "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" \
        --samples_file "$METADATA_FILE" \
        --method DESeq2 \
        --output "$DE_ISOFORMS_DIR"
    
    # Enter isoforms DE directory to run downstream analysis
    cd "$DE_ISOFORMS_DIR"
    
    REL_ISO_MATRIX_TMM="${ITER_DIR}/RSEM_matrix.isoform.TMM.EXPR.matrix"
    
    # Analyze differential expression for isoforms
    echo "  Analyzing differential expression (C2, C3, C4)..."
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4
    
    # Return to root
    cd "$ROOT_DIR"
    
    echo "  ✓ Iteration $i complete"
done

echo ""
echo "=========================================="
echo "✓ All 40 iterations processed!"
echo "=========================================="
echo ""
echo "Next step: Run the Python script to create two-column isoform files:"
echo "  python3 scripts/create_two_column_gene_lists.py"
