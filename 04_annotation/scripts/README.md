# Annotation Scripts

This folder contains all the scripts used for downloading databases, configuring EnTAP, running annotations, and generating publication figures.

## Execution Order

### 1. Installation & Environment Setup
Run these first to get all tools and databases ready:
- `install_01_create_env.sh`: Creates the conda environment.
- `install_02_build_entap.sh`: Clones and compiles EnTAP from source.
- `install_03_download_databases.sh`: Grabs EggNOG, UniProt, and the EnTAP bin.
- `install_04_download_interproscan_databases.sh`: Pulls down the heavy InterProScan databases (takes a while!).

### 2. Annotation Pipeline 
Make sure you've activated the `entap` conda environment before running these:
- `run_01_configure_entap.sh`: Double-checks if all the DBs from step 1 are actually there.
- `run_02_annotate.sh`: The main EnTAP run.
- `run_03_interproscan.sh`: InterProScan annotation on the cleaned FASTA.
- `run_03_interproscan_split.sh`: Alternative InterProScan script if we need to chunk the FASTA to run on a cluster.

### 3. Utility Scripts
- `clean_fasta_for_interproscan.sh`: Scrubs annoying asterisk (*) stop codons from our FASTAs before InterProScan complains. 
- `decompress_eggnog.sh`: Helper for unpacking the EggNOG tarballs.

### 4. Downstream Processing & Figures (Python)
- `merge_annotations.py`: Smushes the EnTAP and InterProScan results into a single, clean `.xlsx` workbook.
- `create_*.py` and `update_*.py`: Various visualization scripts that generate figures (heatmaps, pie charts, publication-ready panels) using our merged annotations. All outputs go to `../results/annotation_graphics/`.
