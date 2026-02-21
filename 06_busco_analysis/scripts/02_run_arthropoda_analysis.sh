#!/bin/bash

# Script to run BUSCO analysis on P. monodon transcriptome assembly
# This evaluates assembly completeness using arthropod-specific orthologs
# Database: arthropoda_odb10 (most specific available for P. monodon)

# Configuration
TRANSCRIPTOME="/home/luigui/Documents/2026/p_monodon_transcriptome/05_multiple_group_clustering/Trinity.fasta"
OUTPUT_DIR="../results"
LINEAGE="arthropoda_odb10"  # Arthropod database as requested by reviewer
MODE="transcriptome"         # Analysis mode
THREADS=24                   # Number of CPU threads to use

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

echo "=========================================="
echo "BUSCO Analysis for P. monodon Transcriptome"
echo "=========================================="
echo "Input transcriptome: ${TRANSCRIPTOME}"
echo "Output directory: ${OUTPUT_DIR}"
echo "Lineage database: ${LINEAGE}"
echo "Mode: ${MODE}"
echo "Threads: ${THREADS}"
echo "=========================================="
echo ""

# Check if transcriptome file exists
if [ ! -f "${TRANSCRIPTOME}" ]; then
    echo "ERROR: Transcriptome file not found: ${TRANSCRIPTOME}"
    echo "Please update the TRANSCRIPTOME variable in this script with the correct path"
    exit 1
fi

# Activate conda environment
echo "Activating BUSCO conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate busco

# Verify BUSCO is available
if ! command -v busco &> /dev/null; then
    echo "ERROR: BUSCO not found. Please run 01_setup_environment.sh first"
    exit 1
fi

echo "BUSCO version:"
busco --version
echo ""

# Run BUSCO analysis
echo "Starting BUSCO analysis..."
echo "This may take several hours depending on transcriptome size..."
echo ""

busco \
    -i "${TRANSCRIPTOME}" \
    -o arthropoda_odb10 \
    -l "${LINEAGE}" \
    -m "${MODE}" \
    -c "${THREADS}" \
    --out_path "${OUTPUT_DIR}" \
    --download_path "../downloads" \
    --force

# Check if analysis completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "BUSCO analysis completed successfully!"
    echo "=========================================="
    echo ""
    echo "Results location: ${OUTPUT_DIR}/arthropoda_odb10"
    echo ""
    echo "Key output files:"
    echo "  - short_summary.txt: Summary statistics"
    echo "  - full_table.tsv: Detailed results for each BUSCO"
    echo "  - missing_busco_list.tsv: List of missing BUSCOs"
    echo ""
    echo "To view the summary:"
    echo "  cat ${OUTPUT_DIR}/arthropoda_odb10/short_summary.*.txt"
else
    echo ""
    echo "ERROR: BUSCO analysis failed"
    echo "Check the log files in ${OUTPUT_DIR}/arthropoda_odb10/logs/"
    exit 1
fi
