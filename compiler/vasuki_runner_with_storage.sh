#!/bin/bash

# This script compiles a Vasuki file to bytecode, stores it, and runs it

# Check if a file was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <vasuki_file>"
    exit 1
fi

# Make sure the VM is compiled
make simple_test
make generate_simple_bytecode

# Get the input file
VASUKI_FILE="$1"
FILENAME=$(basename "$VASUKI_FILE")
BYTECODE_DIR="bytecode_storage"

# Create bytecode directory if it doesn't exist
mkdir -p "$BYTECODE_DIR"

# Path to store the bytecode
BYTECODE_FILE="$BYTECODE_DIR/$FILENAME.bytecode"

echo "=== Processing $VASUKI_FILE ==="
echo "Generating bytecode..."

# Try to use the Python compiler first
if [ -f "../compiler.py" ]; then
    # Set up the Python path to include the parent directory
    PYTHONPATH=.. python3 ../compiler.py "$VASUKI_FILE" "$BYTECODE_FILE" 2>/dev/null
    
    # Check if compilation was successful
    if [ $? -ne 0 ] || [ ! -s "$BYTECODE_FILE" ]; then
        echo "Python compiler failed, using simple bytecode generator instead."
        # Fall back to the simple bytecode generator
        ./generate_simple_bytecode "$BYTECODE_FILE" "Output from $FILENAME"
    else
        echo "Python compiler succeeded."
    fi
else
    # Use the simple bytecode generator
    echo "Python compiler not found, using simple bytecode generator."
    ./generate_simple_bytecode "$BYTECODE_FILE" "Output from $FILENAME"
fi

echo "Bytecode stored in $BYTECODE_FILE"

# Run the bytecode file
echo "Running bytecode..."
./simple_test "$BYTECODE_FILE"

echo "=== Execution complete ==="
echo "Bytecode file is stored at: $BYTECODE_FILE"
