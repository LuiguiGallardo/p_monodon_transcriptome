#!/bin/bash
# Clean FASTA for InterProScan
# Gotta remove those annoying asterisk (*) characters (stop codons) that InterProScan chokes on

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

INPUT_FASTA="${BASE_DIR}/results/entap_output/transcriptomes/Trinity_longest_isoform_final.fasta"
OUTPUT_FASTA="${BASE_DIR}/results/entap_output/transcriptomes/Trinity_longest_isoform_final_clean.fasta"

if [ ! -f "${INPUT_FASTA}" ]; then
    echo "Can't find the input file man: ${INPUT_FASTA}"
    exit 1
fi

echo "Cleaning up the FASTA for InterProScan..."
echo "In:  ${INPUT_FASTA}"
echo "Out: ${OUTPUT_FASTA}"

BEFORE_COUNT=$(grep -c "^>" "${INPUT_FASTA}")
ASTERISK_COUNT=$(grep -v "^>" "${INPUT_FASTA}" | grep -o "\*" | wc -l || true)
echo "Sequences: ${BEFORE_COUNT} | Asterisks to scrap: ${ASTERISK_COUNT}"

# Strip asterisks on non-header lines
sed '/^>/!s/\*//g' "${INPUT_FASTA}" > "${OUTPUT_FASTA}"
AFTER_COUNT=$(grep -c "^>" "${OUTPUT_FASTA}")
REMAINING=$(grep -v "^>" "${OUTPUT_FASTA}" | grep -o "\*" | wc -l || echo "0")

if [ "${BEFORE_COUNT}" -eq "${AFTER_COUNT}" ] && [ "${REMAINING}" -eq "0" ]; then
    echo "✓ Look at that, all clean!"
    echo "Now you can run: bash run_03_interproscan.sh"
else
    echo "✗ ERROR: Something got messed up during cleaning..."
    exit 1
fi
