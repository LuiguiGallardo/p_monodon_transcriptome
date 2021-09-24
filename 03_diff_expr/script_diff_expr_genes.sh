#!/bin/bash

mkdir 05_deseq2_genes

$TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl --matrix 03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.counts.matrix --samples_file metadata_trinity.txt --method DESeq2 --output 05_deseq2_genes
#$TRINITY_HOME/Analysis/DifferentialExpression/run_DE_analysis.pl --matrix 03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.counts.matrix --samples_file metadata_trinity.txt --method DESeq2 --output 05_deseq2_genes

cd 05_deseq2_genes

# For genes:
$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 2
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 3
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.gene.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 4

# For isoforms:
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 2
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 3
#$TRINITY_HOME/Analysis/DifferentialExpression/analyze_diff_expr.pl --matrix ../03_RSEM_matrix_isoforms.results/03_RSEM_matrix_isoforms.results.isoform.TMM.EXPR.matrix  --samples ../metadata_trinity.txt  -P 1e-3 -C 4
