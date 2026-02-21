#!/bin/bash

# Define global paths dynamically
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
ROOT_DIR="${BASE_DIR}"

TRINITY_FASTA="${BASE_DIR}/data/Trinity.fasta"
GENE_MAP="${BASE_DIR}/data/Trinity.fasta.gene_trans_map"
METADATA_DIR="${BASE_DIR}/metadata/metadata_iterations"
RESULTS_BASE_DIR="${BASE_DIR}/results/results_iterations"
GLOBAL_ABUNDANCE_DIR="${BASE_DIR}/results/RSEM_abundance_all"
RAW_METADATA="${BASE_DIR}/metadata/metadata_trinity.txt"

# Create base results directory
mkdir -p "$RESULTS_BASE_DIR"

# Loop through iterations 1 to 40
for i in {1..40}; do
    echo "Processing Iteration $i..."
    
    METADATA_FILE="${METADATA_DIR}/metadata_trinity_iter_${i}.txt"
    ITER_DIR="${RESULTS_BASE_DIR}/iter_${i}"
    
    # Create directory for this iteration
    mkdir -p "$ITER_DIR"
    
    ISOFORM_FILES=""
    
    # Read metadata file line by line to get samples
    while read -r line; do
        [[ -z "$line" ]] && continue
        SAMPLE_ID=$(echo "$line" | awk '{print $2}')
        # Point to the original 1_S1..12_S12 inside results
        ISOFORM_FILES+="${BASE_DIR}/results/${SAMPLE_ID}/RSEM.isoforms.results "
    done < "$METADATA_FILE"
    
    # 2. Abundance Estimates to Matrix
    echo "  Running abundance_estimates_to_matrix.pl..."
    $TRINITY_HOME/util/abundance_estimates_to_matrix.pl \
        --est_method RSEM \
        --gene_trans_map "$GENE_MAP" \
        --name_sample_by_basedir \
        $ISOFORM_FILES \
        --out_prefix "${ITER_DIR}/RSEM_matrix"
    
    # 4. Differential Expression (DESeq2) - GENES
    echo "  Running DE analysis for GENES..."
    DE_GENES_DIR="${ITER_DIR}/deseq2_genes"
    mkdir -p "$DE_GENES_DIR"
    
    $TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
        --matrix "${ITER_DIR}/RSEM_matrix.gene.counts.matrix" \
        --samples_file "$METADATA_FILE" \
        --method DESeq2 \
        --output "$DE_GENES_DIR"
    
    cd "$DE_GENES_DIR" 
    REL_GENE_MATRIX_TMM="${ITER_DIR}/RSEM_matrix.gene.TMM.EXPR.matrix"

    echo "    Analyzing diff expr (Genes)..."
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4
    
    # 5. Differential Expression (DESeq2) - ISOFORMS
    echo "  Running DE analysis for ISOFORMS..."
    DE_ISOFORMS_DIR="${ITER_DIR}/deseq2_isoforms"
    mkdir -p "$DE_ISOFORMS_DIR"
    
    cd "${BASE_DIR}" # Just to be safe before running next step

    $TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
        --matrix "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" \
        --samples_file "$METADATA_FILE" \
        --method DESeq2 \
        --output "$DE_ISOFORMS_DIR"
    
    cd "$DE_ISOFORMS_DIR"
    REL_ISO_MATRIX_TMM="${ITER_DIR}/RSEM_matrix.isoform.TMM.EXPR.matrix"
    
    echo "    Analyzing diff expr (Isoforms)..."
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
    $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4
    
    cd "$ROOT_DIR" || exit
    
    echo "Iteration $i complete."
done

echo "All 40 iterations finished."
