#!/bin/bash
# Setting up the conda environment for EnTAP

set -e

# get paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

echo "Creating the 'entap' conda environment..."
conda env create -f "${BASE_DIR}/environment_entap.yml"

echo "Environment ready! Don't forget to activate it:"
echo "$ conda activate entap"
echo "Then move on to install_02_build_entap.sh"
