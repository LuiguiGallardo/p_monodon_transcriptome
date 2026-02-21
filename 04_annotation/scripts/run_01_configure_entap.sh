#!/bin/bash
# Verify EnTAP configuration before we start analyzing things
# Note: activate the entap conda env first!

set -e

if [[ "$CONDA_DEFAULT_ENV" != "entap" ]]; then
    echo "Bro, activate the 'entap' conda environment first:"
    echo "$ conda activate entap"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
DB_DIR="${BASE_DIR}/downloads/entap_databases"

echo "Checking if databases are ready in ${DB_DIR}..."

if [ ! -f "${DB_DIR}/entap_database.bin" ]; then
    echo "Missing EnTAP database. You might need to rerun install_03_download_databases.sh"
    exit 1
fi
echo "✓ EnTAP database is here"

if [ ! -f "${DB_DIR}/uniprot_sprot.dmnd" ]; then
    echo "Missing UniProt DIAMOND database. Rerun install_03."
    exit 1
fi
echo "✓ UniProt/Swiss-Prot DIAMOND database is here"

if [ ! -d "${DB_DIR}/eggnog_data" ]; then
    echo "Missing EggNOG database. Rerun install_03."
    exit 1
fi
echo "✓ EggNOG database is here"

echo "Everything looks good! You can go ahead and run the annotation:"
echo "$ ./run_02_annotate.sh"
