#!/bin/bash

# Script to monitor the progress of isoform DE analysis

echo "=========================================="
echo "Isoform DE Analysis Progress Monitor"
echo "=========================================="
echo ""

# Check if log file exists
if [ ! -f "isoform_de_all.log" ]; then
    echo "Log file not found. The script may not be running."
    exit 1
fi

# Show current iteration
echo "Current progress:"
grep "Processing Iteration" isoform_de_all.log | tail -1
echo ""

# Count completed iterations
completed=$(grep -c "✓ Iteration.*complete" isoform_de_all.log)
echo "Completed iterations: $completed / 40"
echo ""

# Show last few log lines
echo "Recent activity:"
tail -15 isoform_de_all.log
echo ""

# Check if process is still running
if pgrep -f "run_isoform_de_all.sh" > /dev/null; then
    echo "Status: RUNNING ✓"
else
    echo "Status: COMPLETED or STOPPED"
    if grep -q "All 40 iterations processed" isoform_de_all.log; then
        echo "✓ All iterations have been processed successfully!"
    fi
fi
