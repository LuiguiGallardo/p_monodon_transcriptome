# *Penaeus monodon* Transcriptome

Black tiger shrimp (*Penaeus monodon*) transcriptome assembly and differential expression analysis.

**Created at the Dr. Adrian Ochoa Lab, Instituto de Biotecnología, UNAM by:**
- Luigui Gallardo-Becerra
- Dr. Fernanda Cornejo-Granados  
- Dr. Adrian Ochoa-Leyva

## Overview

This repository contains the bioinformatics pipeline and results for transcriptome assembly and differential gene expression analysis of *Penaeus monodon* RNA-seq data.

## Project Structure

```
├── 00_rawdata/          # Raw FASTQ files and quality reports
├── 01_quality/          # Quality-filtered reads using Trimmomatic
├── 02_assembly/         # Trinity transcriptome assembly
├── 03_diff_expr/        # Differential expression analysis (DESeq2)
└── 04_annotation/       # Functional annotation (BLAST, InterPro, GO terms)
```

## Key Results

- **Raw reads**: 12 paired-end RNA-seq samples
- **Assembly**: 778,680 transcripts (586,928 longest isoforms)
- **Predicted proteins**: 58,678 total (28,423 longest isoforms)
- **Differential expression**: Gene and isoform-level analysis

## Pipeline

1. **Quality control**: FastQC → Trimmomatic filtering
2. **Assembly**: Trinity *de novo* transcriptome assembly
3. **Protein prediction**: TransDecoder protein prediction
4. **Functional annotation**: BLAST, InterPro, and GO term assignment
5. **Expression**: DESeq2 differential expression analysis

## Files

### Key Outputs
- **Assembly**: `02_assembly/01_trinity_output/Trinity.fasta`
- **Proteins (all)**: `04_annotation/Trinity.fasta.transdecoder.pep.gz` (compressed)
- **Proteins (longest)**: `04_annotation/Trinity_longest_isoform.fasta.transdecoder.pep.gz` (compressed)
- **Annotations**: `04_annotation/trinity_longest_isoform_annotations.tsv` (tab-delimited)
- **Annotations**: `04_annotation/trinity_longest_isoform_annotations.xlsx` (Excel format)
- **DE results**: `03_diff_expr/deseq2_genes.xlsx`, `03_diff_expr/deseq2_isoforms.xlsx`

### Analysis Reports
- **Assembly stats**: `02_assembly/metadata_trinity.txt`
- **Realignment stats**: `02_assembly/readcount_realignment.txt`

### Metadata
- **SRA metadata**: `SraRunTable.csv` (sample information and SRA accessions)
- **SRA accession list**: `SRR_Acc_List.txt` (list of SRA run accessions)
