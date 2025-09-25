# *Penaeus monodon* Transcriptome

Black tiger shrimp (*Penaeus monodon*) transcriptome assembly and differential expression analysis.

## Overview

This repository contains the bioinformatics pipeline and results for transcriptome assembly and differential gene expression analysis of *Penaeus monodon* RNA-seq data.

## Project Structure

```
├── 00_rawdata/          # Raw FASTQ files and quality reports
├── 01_quality/          # Quality-filtered reads using Trimmomatic
├── 02_assembly/         # Trinity transcriptome assembly
└── 03_diff_expr/        # Differential expression analysis (DESeq2)
```

## Key Results

- **Raw reads**: 12 paired-end RNA-seq samples
- **Assembly**: 778,680 transcripts (586,928 longest isoforms)
- **Predicted proteins**: 58,678 total (28,423 longest isoforms)
- **Differential expression**: Gene and isoform-level analysis

## Pipeline

1. **Quality control**: FastQC → Trimmomatic filtering
2. **Assembly**: Trinity *de novo* transcriptome assembly
3. **Annotation**: TransDecoder protein prediction
4. **Expression**: DESeq2 differential expression analysis

## Files

- Assembly: `02_assembly/01_trinity_output/Trinity.fasta`
- Proteins: `02_assembly/01_trinity_output/Trinity.fasta.transdecoder.pep`
- DE results: `03_diff_expr/deseq2_genes.xlsx`, `03_diff_expr/deseq2_isoforms.xlsx`
