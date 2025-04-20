#!/bin/bash

# This script runs all Vasuki files in a directory, stores their bytecode, and executes them

# Directory containing Vasuki files
VASUKI_DIR="../presentation"
if [ $# -ge 1 ]; then
    VASUKI_DIR="$1"
fi

# Count the number of files
NUM_FILES=$(find "$VASUKI_DIR" -name "*.vasuki" | wc -l)
echo "Found $NUM_FILES Vasuki files in $VASUKI_DIR"
echo

# Process each Vasuki file
for file in "$VASUKI_DIR"/*.vasuki; do
    # Run the file using the vasuki_runner_with_storage.sh script
    ./vasuki_runner_with_storage.sh "$file"
    echo "--------------------------------------------------"
    echo
done

echo "Summary: $NUM_FILES Vasuki files processed and their bytecode stored in bytecode_storage/"
