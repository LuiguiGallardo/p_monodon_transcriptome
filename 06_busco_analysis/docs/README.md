# BUSCO Analysis for P. monodon Transcriptome

This directory contains scripts and results for BUSCO (Benchmarking Universal Single-Copy Orthologs) analysis on the *P. monodon* transcriptome assembly, as requested by the reviewer.

## Directory Structure

```
06_busco_analysis/
├── scripts/                         # Analysis scripts
│   ├── 01_setup_environment.sh      # Create BUSCO conda environment
│   ├── 02_run_arthropoda_analysis.sh # Run arthropoda_odb10 analysis
│   └── 03_run_metazoa_analysis.sh   # Run metazoa_odb10 analysis
├── results/                         # Analysis results
│   ├── arthropoda_odb10/            # Arthropoda database results
│   ├── metazoa_odb10/               # Metazoa database results
│   └── comparison_summary.md        # Results comparison
├── docs/                            # Documentation
│   ├── README.md                    # This file
│   └── database_information.md      # Database details
├── downloads/                       # BUSCO database downloads
└── logs/                            # Run logs
```

## Purpose

BUSCO provides quantitative assessment of transcriptome assembly completeness based on evolutionarily-informed expectations of gene content from near-universal single-copy orthologs. This analysis uses the **arthropoda_odb10** database as recommended by the reviewer.

## Setup Instructions

### 1. Create the BUSCO conda environment

```bash
cd /home/luigui/Documents/2026/p_monodon_transcriptome/06_busco_analysis/scripts
bash 01_setup_environment.sh
```

This will create a new conda environment named `busco` with BUSCO v5.7.1 and all dependencies.

### 2. Verify installation

```bash
conda activate busco
busco --version
busco --list-datasets  # Optional: see available lineage datasets
```

## Running the Analysis

### Option 1: Run Arthropoda Analysis (Primary)
```bash
bash 02_run_arthropoda_analysis.sh
```

### Option 2: Run Metazoa Analysis (Broader Comparison)
```bash
bash 03_run_metazoa_analysis.sh
```

### Option 3: Run Longest Isoform Analysis
```bash
bash 04_run_longest_isoform_analysis.sh
```
This runs BUSCO on the `Trinity_longest_isoform.fasta` file (one isoform per gene).

### Generate Plots
```bash
bash 05_generate_plots.sh
```
This updates all figures with the latest results.

**Note:** BUSCO analysis can take several hours depending on:
- Transcriptome size
- Number of threads available
- System resources

## Output Files

After completion, results will be in the `results/` directory:

### Arthropoda Results (`results/arthropoda_odb10/`)

- **short_summary.txt**: Summary statistics showing percentages of:
  - Complete BUSCOs (single-copy + duplicated)
  - Fragmented BUSCOs
  - Missing BUSCOs
  
- **full_table.tsv**: Detailed results for each BUSCO gene
- **missing_busco_list.tsv**: List of missing BUSCOs
- **logs/**: Log files for troubleshooting

### Metazoa Results (`results/metazoa_odb10/`)

Same structure as arthropoda results, but for the metazoa database.

### Comparison Summary

See `results/comparison_summary.md` for a side-by-side comparison of both analyses.

## Interpreting Results

A high-quality transcriptome assembly typically shows:
- **>90% complete BUSCOs**: Excellent assembly
- **80-90% complete BUSCOs**: Good assembly
- **<80% complete BUSCOs**: May indicate incomplete assembly or biological factors

For transcriptomes, some duplication is expected due to alternative splicing and gene family expansions.

## For the Reviewer Response

Include in your manuscript:
1. The percentage of complete, fragmented, and missing BUSCOs
2. The total number of BUSCOs searched (arthropoda_odb10 has 1,013 BUSCOs)
3. A brief interpretation of the results

Example text:
> "Assembly completeness was assessed using BUSCO v5.7.1 with the arthropoda_odb10 database (n=1,013 orthologs). The analysis revealed X% complete BUSCOs (X% single-copy, X% duplicated), X% fragmented, and X% missing, indicating [excellent/good] transcriptome completeness."

## Troubleshooting

If the analysis fails:
1. Check that the transcriptome path is correct in the script
2. Ensure sufficient disk space (BUSCO downloads ~500MB database)
3. Check log files in `results/[database_name]/logs/`
4. Verify conda environment is activated: `conda activate busco`

## References

- BUSCO: Manni M, Berkeley MR, Seppey M, Simão FA, Zdobnov EM. 2021. BUSCO Update: Novel and Streamlined Workflows along with Broader and Deeper Phylogenetic Coverage for Scoring of Eukaryotic, Prokaryotic, and Viral Genomes. Molecular Biology and Evolution 38(10):4647-4654.
