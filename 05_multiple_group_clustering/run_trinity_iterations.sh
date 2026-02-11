    #!/bin/bash

    # Define global paths
    ROOT_DIR=$(pwd)
    TRINITY_FASTA="Trinity.fasta"
    GENE_MAP="Trinity.fasta.gene_trans_map"
    METADATA_DIR="metadata_iterations"
    RESULTS_BASE_DIR="results_iterations"
    GLOBAL_ABUNDANCE_DIR="RSEM_abundance_all"
    RAW_METADATA="metadata_trinity.txt"

    # Create base results directory
    mkdir -p "$RESULTS_BASE_DIR"

    # 1. Global Align and Estimate Abundance
    # Run this once for ALL samples found in metadata_trinity.txt
    # if [ ! -d "$GLOBAL_ABUNDANCE_DIR" ]; then
    #     echo "Running GLOBAL align_and_estimate_abundance.pl..."
    #     $TRINITY_HOME/util/align_and_estimate_abundance.pl \
    #         --transcripts "$TRINITY_FASTA" \
    #         --seqType fq \
    #         --samples_file "$RAW_METADATA" \
    #         --est_method RSEM \
    #         --output_dir "$GLOBAL_ABUNDANCE_DIR" \
    #         --trinity_mode \
    #         --prep_reference \
    #         --gene_trans_map "$GENE_MAP" \
    #         --aln_method bowtie2 \
    #         --thread_count 24
    # else
    #     echo "Global abundance directory found ($GLOBAL_ABUNDANCE_DIR). Skipping alignment step."
    # fi

    # Loop through iterations 1 to 40
    for i in {1..40}; do
        echo "Processing Iteration $i..."
        
        # Use absolute path for metadata to avoid issues when changing directories
        METADATA_FILE="${ROOT_DIR}/${METADATA_DIR}/metadata_trinity_iter_${i}.txt"
        ITER_DIR="${RESULTS_BASE_DIR}/iter_${i}"
        
        # Create directory for this iteration
        mkdir -p "$ITER_DIR"
        
        # Extract sample IDs from metadata file (2nd column) to check which samples are in this iteration
        # We construct the list of files pointing to the GLOBAL_ABUNDANCE_DIR
        
        ISOFORM_FILES=""
        
        # Read metadata file line by line to get samples
        while read -r line; do
            # Skip empty lines
            [[ -z "$line" ]] && continue
            
            # Extract sample ID (2nd column)
            SAMPLE_ID=$(echo "$line" | awk '{print $2}')
            
            # Point to the pre-calculated isoform results in global directory
            ISOFORM_FILES+="${ROOT_DIR}/${SAMPLE_ID}/RSEM.isoforms.results "
            
        done < "$METADATA_FILE"
        
        # 2. Abundance Estimates to Matrix
        # Using isoform files with gene_trans_map generates BOTH gene and isoform matrices
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
        
        # Run DE analysis (Genes)
        $TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
            --matrix "${ITER_DIR}/RSEM_matrix.gene.counts.matrix" \
            --samples_file "$METADATA_FILE" \
            --method DESeq2 \
            --output "$DE_GENES_DIR"
        
        # Enter genes DE directory to run downstream analysis
        cd "$DE_GENES_DIR" 
        
        REL_GENE_MATRIX_TMM="${ROOT_DIR}/${ITER_DIR}/RSEM_matrix.gene.TMM.EXPR.matrix"

        # Analyze differential expression for genes
        echo "    Analyzing diff expr (Genes)..."
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_GENE_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4
        
        # Return to iteration directory
        cd "${ROOT_DIR}/${ITER_DIR}"
        
        # 5. Differential Expression (DESeq2) - ISOFORMS
        echo "  Running DE analysis for ISOFORMS..."
        DE_ISOFORMS_DIR="${ITER_DIR}/deseq2_isoforms"
        mkdir -p "$DE_ISOFORMS_DIR"
        
        # Run DE analysis (Isoforms)
        $TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl \
            --matrix "${ITER_DIR}/RSEM_matrix.isoform.counts.matrix" \
            --samples_file "$METADATA_FILE" \
            --method DESeq2 \
            --output "$DE_ISOFORMS_DIR"
        
        # Enter isoforms DE directory to run downstream analysis
        cd "$DE_ISOFORMS_DIR"
        
        REL_ISO_MATRIX_TMM="${ROOT_DIR}/${ITER_DIR}/RSEM_matrix.isoform.TMM.EXPR.matrix"
        
        # Analyze differential expression for isoforms
        echo "    Analyzing diff expr (Isoforms)..."
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 2
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 3
        $TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix "$REL_ISO_MATRIX_TMM" --samples "$METADATA_FILE" -P 1e-3 -C 4
        
        # Return to root for next iteration
        cd "$ROOT_DIR" || exit
        
        echo "Iteration $i complete."
    done

    echo "All 40 iterations finished."
