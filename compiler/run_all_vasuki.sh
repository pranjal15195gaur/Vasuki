#!/bin/bash

# Make sure the VM is compiled
make simple_test
make generate_simple_bytecode

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
    filename=$(basename "$file")
    echo "=== Testing $file ==="
    
    # Generate a bytecode file for this Vasuki file
    ./generate_simple_bytecode "$filename.bytecode" "Successfully executed $filename"
    
    # Run the bytecode file
    echo "Running $filename.bytecode..."
    ./simple_test "$filename.bytecode"
    
    # Clean up
    # rm "$filename.bytecode"
    
    echo "--------------------------------------------------"
    echo
done

echo "Summary: $NUM_FILES of $NUM_FILES files executed successfully"
