#!/bin/bash
# Running EnTAP Annotation
# Make sure entap is configured and the conda env is active!

set -e

if [[ "$CONDA_DEFAULT_ENV" != "entap" ]]; then
    echo "Wait, please activate the 'entap' conda environment first:"
    echo "$ conda activate entap"
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"

echo "Fire up EnTAP annotation..."
echo "Using configs from ${BASE_DIR}/entap_config..."

# We are defining the run parameters and the config in entap_run.params and entap_config.ini
EnTAP --run \
  --run-ini "${BASE_DIR}/entap_config/entap_run.params" \
  --entap-ini "${BASE_DIR}/entap_config/entap_config.ini" \
  -t 32

echo "Annotation finished!"
echo "Check the results defined in your run.params/config output directory."
