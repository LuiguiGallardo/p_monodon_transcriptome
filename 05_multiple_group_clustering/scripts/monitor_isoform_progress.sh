#!/bin/bash

# Script to monitor the progress of isoform DE analysis

echo "=========================================="
echo "Isoform DE Analysis Progress Monitor"
echo "=========================================="
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( dirname "$SCRIPT_DIR" )"
LOG_FILE="${BASE_DIR}/logs/isoform_de_all.log"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found. The script may not be running."
    exit 1
fi

# Show current iteration
echo "Current progress:"
grep "Processing Iteration" "$LOG_FILE" | tail -1
echo ""

# Count completed iterations
completed=$(grep -c "✓ Iteration.*complete" "$LOG_FILE")
echo "Completed iterations: $completed / 40"
echo ""

# Show last few log lines
echo "Recent activity:"
tail -15 "$LOG_FILE"
echo ""

# Check if process is still running
if pgrep -f "run_isoform_de_all.sh" > /dev/null; then
    echo "Status: RUNNING ✓"
else
    echo "Status: COMPLETED or STOPPED"
    if grep -q "All 40 iterations processed" "$LOG_FILE"; then
        echo "✓ All iterations have been processed successfully!"
    fi
fi
