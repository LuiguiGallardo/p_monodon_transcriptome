#!/bin/bash
# Running InterProScan on the EnTAP protein output
# Make sure InterProScan is in your PATH. This might take a while on our 28k proteins!
# We're running this bad boy on 32 cores. 

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

INPUT_FASTA="${BASE_DIR}/results/entap_output/transcriptomes/Trinity_longest_isoform_final_clean.fasta"
OUTPUT_DIR="${BASE_DIR}/results/interproscan_output"
TEMP_DIR="${OUTPUT_DIR}/temp"
LOG_FILE="${BASE_DIR}/logs/interproscan_$(date +%Y%m%d_%H%M%S).log"

# Max out the CPUs but keep it reasonable for memory (server has 128GB)
CPUS=32
# full mode takes longer but gives us all the nice databases (Pfam, GO terms, Panthers, etc.)
MODE="full"

mkdir -p "${OUTPUT_DIR}"
mkdir -p "${TEMP_DIR}"
mkdir -p "${BASE_DIR}/logs"

if [ ! -f "${INPUT_FASTA}" ]; then
    echo "Wait, I can't find the input file here: ${INPUT_FASTA}"
    exit 1
fi

if ! command -v interproscan.sh &> /dev/null; then
    echo "Bro, interproscan.sh is not in PATH."
    exit 1
fi

echo "All systems go. InterProScan version:"
interproscan.sh --version || true

SEQ_COUNT=$(grep -c "^>" "${INPUT_FASTA}")
echo "Look at that, we've got ${SEQ_COUNT} sequences to chew through."

if [ "${MODE}" == "full" ]; then
    echo "Running in FULL mode (the whole shebang) ..."
    APPLICATIONS="Pfam,TIGRFAM,PRINTS,ProSiteProfiles,ProSitePatterns,SMART,CDD,SUPERFAMILY,PANTHER,Gene3D,Hamap,Coils,MobiDBLite,PIRSF"
else
    echo "Running in FAST mode (just the hits) ..."
    APPLICATIONS="Pfam,SMART,PANTHER,Gene3D,CDD,SUPERFAMILY"
fi

START_TIME=$(date +%s)
echo "Kicking off at: $(date), grab a coffee, this will take 24-48 hours."

interproscan.sh \
    --input "${INPUT_FASTA}" \
    --output-dir "${OUTPUT_DIR}" \
    --formats TSV,GFF3,JSON \
    --cpu ${CPUS} \
    --applications ${APPLICATIONS} \
    --goterms \
    --pathways \
    --tempdir "${TEMP_DIR}" \
    --disable-precalc \
    --verbose \
    2>&1 | tee "${LOG_FILE}"

END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))
HOURS=$((RUNTIME / 3600))
MINUTES=$(((RUNTIME % 3600) / 60))

echo "Boom. InterProScan finished in ${HOURS}h ${MINUTES}m"
echo "Check your results at: ${OUTPUT_DIR}"

if [ -f "${OUTPUT_DIR}"/*.tsv ]; then
    ANNOTATED=$(cut -f1 "${OUTPUT_DIR}"/*.tsv | sort -u | wc -l)
    PERCENTAGE=$((ANNOTATED * 100 / SEQ_COUNT))
    echo "We annotated ${ANNOTATED} / ${SEQ_COUNT} sequences. That's ${PERCENTAGE}% coverage."
fi
