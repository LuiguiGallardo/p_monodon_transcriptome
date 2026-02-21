#!/bin/bash
# Download databases for EnTAP
# Requires 'entap' conda env

set -e

if [[ "$CONDA_DEFAULT_ENV" != "entap" ]]; then
    echo "Bro, activate the 'entap' conda environment first:"
    echo "$ conda activate entap"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
DB_DIR="${BASE_DIR}/downloads/entap_databases"

echo "Setting up EnTAP databases in ${DB_DIR}..."
mkdir -p "${DB_DIR}"
cd "${DB_DIR}"

# EnTAP bin
echo "1. Fetching EnTAP database (~500MB)..."
if [ ! -f "entap_database.bin" ]; then
    wget -c https://treegenesdb.org/FTP/EnTAP/latest/databases/entap_database.bin.gz
    gunzip entap_database.bin.gz
    echo "  > Got EnTAP DB"
else
    echo "  > EnTAP DB already there"
fi

# EggNOG
echo "2. Fetching EggNOG database (~5GB, grab a coffee)..."
if [ ! -d "eggnog_data" ]; then
    mkdir -p eggnog_data
    download_eggnog_data.py --data_dir ./eggnog_data -y
    echo "  > Got EggNOG DB"
else
    echo "  > EggNOG DB already there"
fi

# UniProt
echo "3. Fetching UniProt/Swiss-Prot (~300MB)..."
if [ ! -f "uniprot_sprot.fasta" ]; then
    wget -c https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
    gunzip uniprot_sprot.fasta.gz
    echo "  > Got UniProt/Swiss-Prot"
else
    echo "  > UniProt/Swiss-Prot already there"
fi

# DIAMOND db
echo "4. Making DIAMOND database from UniProt..."
if [ ! -f "uniprot_sprot.dmnd" ]; then
    diamond makedb --in uniprot_sprot.fasta -d uniprot_sprot --threads $(nproc)
    echo "  > DIAMOND DB built"
else
    echo "  > DIAMOND DB already built"
fi

echo "Done fetching databases."
echo "Up next: run_01_configure_entap.sh"
