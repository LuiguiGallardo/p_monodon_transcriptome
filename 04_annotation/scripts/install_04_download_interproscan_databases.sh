#!/bin/bash
# Fetch InterProScan Databases
# Note: You should have InterProScan installed via conda first!
# Heads up: this pulls down ~30-40 GB of data. Might take a few hours.

set -e

if [[ "$CONDA_DEFAULT_ENV" != "entap" ]]; then
    echo "Bro, activate the 'entap' conda environment first:"
    echo "$ conda activate entap"
    exit 1
fi

if ! command -v interproscan.sh &> /dev/null; then
    echo "Wait, interproscan.sh isn't in your PATH."
    echo "Run this first to install:"
    echo "$ conda install -c bioconda interproscan"
    exit 1
fi

INTERPROSCAN_DIR=$(dirname $(dirname $(which interproscan.sh)))
INTERPROSCAN_SHARE="${INTERPROSCAN_DIR}/share/InterProScan"

echo "Found the InterProScan folder here:"
echo "  ${INTERPROSCAN_SHARE}"

echo "Checking what we currently have..."
du -sh "${INTERPROSCAN_SHARE}/data/"*/ 2>/dev/null | head -10 || true

echo "Just a warning, this drops ~30-40 GB on your disk."
read -p "Look good? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Cancelling."
    exit 0
fi

cd "${INTERPROSCAN_SHARE}"
echo "We are off... Started at: $(date)"

# Use built-in setup if it exists
if [ -f "setup.py" ]; then
    echo "Looks like setup.py is here, running it..."
    python setup.py -f interproscan.properties
elif [ -f "initial_setup.py" ]; then
    echo "Running initial_setup.py..."
    python initial_setup.py
else
    # Fallback to manual download
    echo "Setup scripts missing, falling back to manual wget..."
    
    IPRSCAN_VERSION=$(interproscan.sh --version 2>&1 | grep -oP 'InterProScan-\K[0-9]+\.[0-9]+-[0-9]+\.[0-9]+' | head -1)
    
    if [ -z "$IPRSCAN_VERSION" ]; then
        echo "Couldn't grab the InterProScan version. Aborting."
        exit 1
    fi
    
    echo "Version: ${IPRSCAN_VERSION}"
    BASE_URL="https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/${IPRSCAN_VERSION}"
    
    TEMP_DIR="${INTERPROSCAN_SHARE}/temp_download"
    mkdir -p "${TEMP_DIR}"
    cd "${TEMP_DIR}"
    
    echo "Pulling the heavy data archive..."
    wget -c "${BASE_URL}/interproscan-${IPRSCAN_VERSION}-64-bit.tar.gz"
    
    if [ -f "interproscan-${IPRSCAN_VERSION}-64-bit.tar.gz.md5" ]; then
        md5sum -c "interproscan-${IPRSCAN_VERSION}-64-bit.tar.gz.md5" || true
    fi
    
    echo "Extracting (this might also take a while)..."
    tar -xzf "interproscan-${IPRSCAN_VERSION}-64-bit.tar.gz" \
        --strip-components=1 \
        "interproscan-${IPRSCAN_VERSION}/data"
    
    echo "Moving files into place..."
    rsync -av data/ "${INTERPROSCAN_SHARE}/data/"
    
    cd "${INTERPROSCAN_SHARE}"
    rm -rf "${TEMP_DIR}"
fi

echo "All done fetching InterProScan databases!"
echo "Ended at: $(date)"

TOTAL_SIZE=$(du -sh "${INTERPROSCAN_SHARE}/data/" | cut -f1)
echo "Total database size sitting at: ${TOTAL_SIZE}"

echo "Check it works: interproscan.sh --version"
echo "Then move to run_03_interproscan.sh"
