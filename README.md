# *Penaeus monodon* Transcriptome

Black tiger shrimp (*Penaeus monodon*) transcriptome assembly, functional annotation, differential expression, and completeness analysis.

**Created at the Dr. Adrian Ochoa Lab, Instituto de Biotecnología, UNAM by:**
- Luigui Gallardo-Becerra
- Dr. Fernanda Cornejo-Granados  
- Dr. Adrian Ochoa-Leyva

## Overview

This repository contains the bioinformatics pipeline and results for transcriptome assembly, functional annotation, differential gene expression analysis, and assembly completeness evaluation of *Penaeus monodon* RNA-seq data.

## Project Structure

```
├── 00_rawdata/                   # Raw FASTQ files and quality reports
├── 01_quality/                   # Quality-filtered reads using Trimmomatic
├── 02_assembly/                  # Trinity transcriptome assembly
├── 03_diff_expr/                 # Differential expression analysis (DESeq2)
├── 04_annotation/                # Functional annotation (EnTAP, InterProScan, GO, KEGG)
├── 05_multiple_group_clustering/ # Multi-group expression clustering across 40 iterations
├── 06_busco_analysis/            # Assembly completeness evaluation (BUSCO v5.7.1)
└── Additional_Tables/            # Supplementary data tables
```

## Key Results

- **Raw reads**: 12 paired-end RNA-seq samples
- **Assembly**: 778,680 transcripts (586,928 longest isoforms)
- **Predicted proteins**: 58,678 total (28,423 longest isoforms)
- **Differential expression**: Gene and isoform-level analysis across 40 bootstrap iterations
- **Annotation**: Comprehensive functional annotation via EnTAP (DIAMOND + EggNOG-mapper) and InterProScan
- **Assembly completeness**: 89.4% (Arthropoda odb10) and 91.3% (Metazoa odb10) complete BUSCOs

Large FASTA files have been split into 5 parts each and compressed with gzip for GitHub compatibility:
- All files are under 100MB limit
- Use `zcat file*_Trinity*.fasta.gz > Trinity.fasta` to reconstruct original files
- See `02_assembly/01_trinity_output/README_reassemble.md` for detailed instructions

## Pipeline

1. **Quality control**: FastQC → Trimmomatic filtering
2. **Assembly**: Trinity *de novo* transcriptome assembly
3. **Protein prediction**: TransDecoder protein prediction
4. **Functional annotation**: EnTAP (DIAMOND + EggNOG-mapper), InterProScan (GO, KEGG, Pfam, IPR domains)
5. **Differential expression**: DESeq2 gene- and isoform-level analysis across 40 bootstrap iterations
6. **Multi-group clustering**: Expression pattern clustering and visualization across sample groups
7. **Completeness assessment**: BUSCO evaluation against Arthropoda (odb10) and Metazoa (odb10) lineage datasets

## Files

### Key Outputs
- **Assembly (Trinity)**: `02_assembly/01_trinity_output/file*_Trinity.fasta.gz` (split into 5 compressed parts)
- **Assembly (longest isoforms)**: `02_assembly/01_trinity_output/file*_Trinity_longest_isoform.fasta.gz` (split into 5 compressed parts)
- **Assembly instructions**: `02_assembly/01_trinity_output/README_reassemble.md` (how to reconstruct original files)
- **Proteins (all)**: `04_annotation/Trinity.fasta.transdecoder.pep.gz` (compressed)
- **Proteins (longest)**: `04_annotation/Trinity_longest_isoform.fasta.transdecoder.pep.gz` (compressed)
- **Annotations (TSV)**: `04_annotation/results/trinity_longest_isoform_annotations.tsv` (tab-delimited)
- **Annotations (Excel)**: `04_annotation/results/trinity_longest_isoform_annotations.xlsx`
- **Comprehensive annotations**: `04_annotation/results/comprehensive_protein_annotations.xlsx` (EnTAP + InterProScan merged)
- **DE results (genes)**: `03_diff_expr/deseq2_genes.xlsx`
- **DE results (isoforms)**: `03_diff_expr/deseq2_isoforms.xlsx`
- **DE results (proteins)**: `03_diff_expr/deseq2_genes_proteins.xlsx`
- **Clustering report**: `05_multiple_group_clustering/results/report_40_iterations.pdf`
- **BUSCO figures**: `06_busco_analysis/results/figures/`

### Analysis Reports
- **Assembly stats**: `05_multiple_group_clustering/metadata/metadata_trinity.txt`
- **Clustering report (MD)**: `05_multiple_group_clustering/results/report_40_iterations.md`
- **BUSCO summary**: `06_busco_analysis/docs/`

### Metadata
- **SRA metadata**: `SraRunTable.csv` (sample information and SRA accessions)
- **SRA accession list**: `SRR_Acc_List.txt` (list of SRA run accessions)
- **Iteration metadata**: `05_multiple_group_clustering/metadata/metadata_iterations/` (per-iteration details)
