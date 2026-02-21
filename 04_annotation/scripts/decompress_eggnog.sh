#!/bin/bash
# Decompress EggNOG database files 
# Do this after the download is done if it didn't do it automatically

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
EGGNOG_DIR="${BASE_DIR}/downloads/entap_databases/eggnog_data"

echo "Extracting the EggNOG Databases..."

if [ ! -d "${EGGNOG_DIR}" ]; then
    echo "EggNOG directory not found at ${EGGNOG_DIR}"
    exit 1
fi

cd "${EGGNOG_DIR}"

echo "1. Dealing with eggnog.db.gz..."
if [ -f "eggnog.db.gz" ] && [ ! -f "eggnog.db" ]; then
    gunzip eggnog.db.gz
    echo "   ✓ Extracted eggnog.db"
elif [ -f "eggnog.db" ]; then
    echo "   ✓ Already extracted eggnog.db"
else
    echo "   ✗ eggnog.db.gz is missing!"
    exit 1
fi

echo "2. Extracting eggnog.taxa.tar.gz..."
if [ -f "eggnog.taxa.tar.gz" ]; then
    tar -zxf eggnog.taxa.tar.gz
    rm eggnog.taxa.tar.gz
    echo "   ✓ Taxonomy data pulled"
elif [ ! -f "eggnog.taxa.db" ]; then
    # Might not strictly need this check but just in case
    echo "   ✗ eggnog.taxa.tar.gz missing!"
    exit 1
fi

echo "3. Dealing with eggnog_proteins.dmnd.gz..."
if [ -f "eggnog_proteins.dmnd.gz" ] && [ ! -f "eggnog_proteins.dmnd" ]; then
    gunzip eggnog_proteins.dmnd.gz
    echo "   ✓ Extracted eggnog_proteins.dmnd"
elif [ -f "eggnog_proteins.dmnd" ]; then
    echo "   ✓ Already extracted eggnog_proteins.dmnd"
else
    echo "   ✗ eggnog_proteins.dmnd.gz is missing!"
    exit 1
fi

echo "All done here."
echo "EggNOG should be ready to roll in entap_config/entap_config.ini now!"
