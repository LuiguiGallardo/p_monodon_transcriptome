#!/bin/bash
# InterProScan Batch Script
# Splits up the FASTA, runs jobs, and keeps my sanity intact.
# Great if we need to run things in chunks or on a SLURM cluster.

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

INPUT_FASTA="${BASE_DIR}/results/entap_output/transcriptomes/Trinity_longest_isoform_final.fasta"
OUTPUT_DIR="${BASE_DIR}/results/interproscan_output_batches"
CHUNKS_DIR="${OUTPUT_DIR}/chunks"
RESULTS_DIR="${OUTPUT_DIR}/results"
MERGED_DIR="${OUTPUT_DIR}/merged"
LOG_DIR="${BASE_DIR}/logs/interproscan_chunks"

# 5k sequences per chunk seems reasonable for our 28k total
CHUNK_SIZE=5000
CPUS=32
MEMORY="32G"
MODE="full"

mkdir -p "${CHUNKS_DIR}"
mkdir -p "${RESULTS_DIR}"
mkdir -p "${MERGED_DIR}"
mkdir -p "${LOG_DIR}"

if [ ! -f "${INPUT_FASTA}" ]; then
    echo "Wait up, where's the input file: ${INPUT_FASTA}?"
    exit 1
fi

TOTAL_SEQS=$(grep -c "^>" "${INPUT_FASTA}")
NUM_CHUNKS=$(( (TOTAL_SEQS + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo "Looking at ${TOTAL_SEQS} sequences total, splitting into ${NUM_CHUNKS} chunks of ${CHUNK_SIZE}..."

awk -v chunk_size=${CHUNK_SIZE} -v output_dir="${CHUNKS_DIR}" '
BEGIN {
    seq_count = 0
    chunk_num = 1
    output_file = sprintf("%s/chunk_%03d.fasta", output_dir, chunk_num)
}
/^>/ {
    if (seq_count > 0 && seq_count % chunk_size == 0) {
        close(output_file)
        chunk_num++
        output_file = sprintf("%s/chunk_%03d.fasta", output_dir, chunk_num)
    }
    seq_count++
}
{
    print > output_file
}
' "${INPUT_FASTA}"

echo "Split done. Generating job scripts..."

if [ "${MODE}" == "full" ]; then
    APPLICATIONS="Pfam,TIGRFAM,PRINTS,ProSiteProfiles,ProSitePatterns,SMART,CDD,SUPERFAMILY,PANTHER,Gene3D,Hamap,Coils,MobiDBLite,PIRSF"
else
    APPLICATIONS="Pfam,SMART,PANTHER,Gene3D,CDD,SUPERFAMILY"
fi

for i in $(seq 1 ${NUM_CHUNKS}); do
    CHUNK_FILE="${CHUNKS_DIR}/chunk_$(printf "%03d" ${i}).fasta"
    JOB_SCRIPT="${OUTPUT_DIR}/job_$(printf "%03d" ${i}).sh"
    
    cat > "${JOB_SCRIPT}" << EOF
#!/bin/bash
# Job script for chunk ${i}
#SBATCH --job-name=ipr_chunk_${i}
#SBATCH --output=${LOG_DIR}/chunk_${i}_%j.out
#SBATCH --error=${LOG_DIR}/chunk_${i}_%j.err
#SBATCH --cpus-per-task=${CPUS}
#SBATCH --mem=${MEMORY}
#SBATCH --time=24:00:00

set -e

echo "Hitting chunk ${i}/${NUM_CHUNKS}. Job started at: \$(date)"
interproscan.sh \\
    --input "${CHUNK_FILE}" \\
    --output-dir "${RESULTS_DIR}" \\
    --formats TSV,GFF3 \\
    --cpu ${CPUS} \\
    --applications ${APPLICATIONS} \\
    --goterms \\
    --pathways \\
    --disable-precalc \\
    --verbose

echo "Chunk ${i} finished up at: \$(date)"
EOF
    
    chmod +x "${JOB_SCRIPT}"
done

echo "Nice, created ${NUM_CHUNKS} job scripts in ${OUTPUT_DIR}/"
echo "You can submit these via SLURM or run them manually in a for-loop:"
echo "  for i in {1..${NUM_CHUNKS}}; do bash ${OUTPUT_DIR}/job_\$(printf \"%03d\" \${i}).sh; done"
