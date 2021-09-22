#!/bin/bash
# Title: script_trinity.sh
# Purpose: Penaeus monodon Trinity assembly.
# Author: Luigui Gallardo-Becerra (bfllg77@gmail.com)
# Date: 03.09.2021

# Beginning of the script
Trinity --seqType fq --samples_file metadata_trinity.txt --output 01_trinity_output --CPU 64 --max_memory 1000G --bflyCPU 64 --bflyHeapSpaceMax 15G

$TRINITY_HOME/util/TrinityStats.pl 01_trinity_output/Trinity.fasta > 01_trinity_output/stats_Trinity.fasta.txt

bowtie2-build 01_trinity_output/Trinity.fasta Trinity_assembly --threads 64

bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 1_S1_paired_R1_2.fastq.gz -2 1_S1_paired_R2_2.fastq.gz 2> align_stats_1_S1.txt | samtools view -@60 -Sb -o 1_S1_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 2_S2_paired_R1_2.fastq.gz -2 2_S2_paired_R2_2.fastq.gz 2> align_stats_2_S2.txt | samtools view -@60 -Sb -o 2_S2_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 3_S3_paired_R1_2.fastq.gz -2 3_S3_paired_R2_2.fastq.gz 2> align_stats_3_S3.txt | samtools view -@60 -Sb -o 3_S3_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 4_S4_paired_R1_2.fastq.gz -2 4_S4_paired_R2_2.fastq.gz 2> align_stats_4_S4.txt | samtools view -@60 -Sb -o 4_S4_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 5_S5_paired_R1_2.fastq.gz -2 5_S5_paired_R2_2.fastq.gz 2> align_stats_5_S5.txt | samtools view -@60 -Sb -o 5_S5_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 7_S7_paired_R1_2.fastq.gz -2 7_S7_paired_R2_2.fastq.gz 2> align_stats_7_S7.txt | samtools view -@60 -Sb -o 7_S7_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 6_S6_paired_R1_2.fastq.gz -2 6_S6_paired_R2_2.fastq.gz 2> align_stats_6_S6.txt | samtools view -@60 -Sb -o 6_S6_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 8_S8_paired_R1_2.fastq.gz -2 8_S8_paired_R2_2.fastq.gz 2> align_stats_8_S8.txt | samtools view -@60 -Sb -o 8_S8_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 9_S9_paired_R1_2.fastq.gz -2 9_S9_paired_R2_2.fastq.gz 2> align_stats_9_S9.txt | samtools view -@60 -Sb -o 9_S9_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 10_S10_paired_R1_2.fastq.gz -2 10_S10_paired_R2_2.fastq.gz 2> align_stats_10_S10.txt | samtools view -@60 -Sb -o 10_S10_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 11_S11_paired_R1_2.fastq.gz -2 11_S11_paired_R2_2.fastq.gz 2> align_stats_11_S11.txt | samtools view -@60 -Sb -o 11_S11_bowtie2.bam
bowtie2 -p 64 --no-unal -k 20 -x Trinity_assembly -1 12_S12_paired_R1_2.fastq.gz -2 12_S12_paired_R2_2.fastq.gz 2> align_stats_12_S12.txt | samtools view -@60 -Sb -o 12_S12_bowtie2.bam

$TRINITY_HOME/util/align_and_estimate_abundance.pl --transcripts 01_trinity_output/Trinity.fasta --seqType fq --samples_file metadata_trinity.txt --est_method RSEM --output_dir 02_rsem_abundance --trinity_mode --prep_reference --gene_trans_map 01_trinity_output/Trinity.fasta.gene_trans_map --aln_method bowtie2 --thread_count 30

$TRINITY_HOME/util/abundance_estimates_to_matrix.pl --est_method RSEM --gene_trans_map 01_trinity_output/Trinity.fasta.gene_trans_map --name_sample_by_basedir 10_S10/RSEM.genes.results 11_S11/RSEM.genes.results 12_S12/RSEM.genes.results 1_S1/RSEM.genes.results 2_S2/RSEM.genes.results 3_S3/RSEM.genes.results 4_S4/RSEM.genes.results 5_S5/RSEM.genes.results 6_S6/RSEM.genes.results 7_S7/RSEM.genes.results 8_S8/RSEM.genes.results 9_S9/RSEM.genes.results --out_prefix 02_RSEM_matrix_gene.results
mkdir 02_RSEM_matrix_gene.results ; mv 02_RSEM_matrix_gene.results* 02_RSEM_matrix_gene.results

$TRINITY_HOME/util/abundance_estimates_to_matrix.pl --est_method RSEM --gene_trans_map 01_trinity_output/Trinity.fasta.gene_trans_map --name_sample_by_basedir 10_S10/RSEM.isoforms.results 11_S11/RSEM.isoforms.results 12_S12/RSEM.isoforms.results 1_S1/RSEM.isoforms.results 2_S2/RSEM.isoforms.results 3_S3/RSEM.isoforms.results 4_S4/RSEM.isoforms.results 5_S5/RSEM.isoforms.results 6_S6/RSEM.isoforms.results 7_S7/RSEM.isoforms.results 8_S8/RSEM.isoforms.results 9_S9/RSEM.isoforms.results --out_prefix 03_RSEM_matrix_isoforms.results
mkdir 03_RSEM_matrix_isoforms.results ; mv 03_RSEM_matrix_isoforms.results* 03_RSEM_matrix_isoforms.results

# The end!

