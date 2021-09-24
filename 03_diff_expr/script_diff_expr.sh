#!/bin/bash
# Title: script_diff_expr.sh
# Purpose: Differential expression with DESeq2.
# Author: Luigui Gallardo-Becerra (bfllg77@gmail.com)
# Date: 03.09.2021

# Beginning of the script
mkdir 04_deseq2

#$TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl --matrix 03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.counts.matrix --samples_file metadata_trinity.txt --method DESeq2 --output 04_deseq2
$TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl --matrix 03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.counts.matrix --samples_file metadata_trinity.txt --method DESeq2 --output 04_deseq2

cd 04_deseq2

# For genes:
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 2
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 3
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 4

# For isoforms:
$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 2
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 3
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 4

# The end!

