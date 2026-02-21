#!/bin/bash
# Download and compile EnTAP from source
# Note: make sure the 'entap' conda env is active first!

set -e

if [[ "$CONDA_DEFAULT_ENV" != "entap" ]]; then
    echo "Bro, activate the 'entap' conda environment first:"
    echo "$ conda activate entap"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

# set up the install dir
INSTALL_DIR="${BASE_DIR}/entap_install"
mkdir -p "${INSTALL_DIR}"
cd "${INSTALL_DIR}"

echo "Fetching EnTAP source code..."
if [ ! -d "EnTAP" ]; then
    git clone https://gitlab.com/PlantGenomicsLab/EnTAP.git
fi

cd EnTAP

echo "Configuring with CMake..."
mkdir -p build
cd build

cmake .. \
    -DCMAKE_INSTALL_PREFIX="${CONDA_PREFIX}" \
    -DCMAKE_BUILD_TYPE=Release

echo "Compiling (grab a coffee, this takes a minute)..."
make -j$(nproc)

echo "Installing into the conda env..."
make install

echo "Done building EnTAP!"
echo "Testing if it worked:"
EnTAP --version

echo "Next up: install_03_download_databases.sh"
