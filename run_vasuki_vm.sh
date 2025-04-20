#!/bin/bash

# This script runs a Vasuki file using the C++ VM

# Check if a file was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <vasuki_file>"
    exit 1
fi

# Get the input file
INPUT_FILE="$1"

# Check if the file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File $INPUT_FILE does not exist"
    exit 1
fi

# Create the bytecode storage directory if it doesn't exist
BYTECODE_DIR="compiler/vm/bytecode_storage"
mkdir -p "$BYTECODE_DIR"

# Generate the output file path
FILENAME=$(basename "$INPUT_FILE")
BYTECODE_FILE="$BYTECODE_DIR/$FILENAME.bytecode"

# Compile the VM if needed
if [ ! -f "compiler/vm/generate_bytecode" ] || [ ! -f "compiler/vm/simple_test" ]; then
    echo "Compiling the VM..."
    cd compiler/vm && make generate_bytecode simple_test && cd ../..
fi

# Generate bytecode silently
compiler/vm/generate_bytecode "$INPUT_FILE" "$BYTECODE_FILE" > /dev/null 2>&1

# Create a temporary file for the output
TEMP_OUTPUT=$(mktemp)

# Run the bytecode and save the output to the temporary file
compiler/vm/simple_test "$BYTECODE_FILE" > "$TEMP_OUTPUT" 2>/dev/null

# Extract the actual output (between the markers)
OUTPUT=$(cat "$TEMP_OUTPUT" | awk '/-------------------/{flag=1;next}/-------------------/{flag=0}flag' | grep -v "HALT:")

# Print the output
echo "$OUTPUT"

# Clean up the temporary file
rm "$TEMP_OUTPUT"
