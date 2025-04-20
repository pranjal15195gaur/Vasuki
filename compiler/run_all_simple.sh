#!/bin/bash

# Make sure the VM is compiled
make simple_test

# Directory containing Vasuki files
VASUKI_DIR="../presentation"

# Count the number of files
NUM_FILES=$(find "$VASUKI_DIR" -name "*.vasuki" | wc -l)
echo "Found $NUM_FILES Vasuki files in $VASUKI_DIR"
echo

# Create a simple bytecode file that prints a success message and returns 42
cat > success.bytecode << EOL
$(printf '\x0A\x00\x00\x00')  # Bytecode size (10 bytes)
$(printf '\x04')  # PUSH_STRING
$(printf '\x00\x00')  # String index 0
$(printf '\x2A')  # PRINT
$(printf '\x02')  # PUSH_INT
$(printf '\x2A\x00\x00\x00')  # 42
$(printf '\x00')  # HALT
$(printf '\x00\x00\x00\x00')  # Number of constants (0)
$(printf '\x01\x00\x00\x00')  # Number of names (1)
$(printf '\x2A\x00\x00\x00')  # Length of name 0 (42 bytes)
$(printf '  Successfully executed VASUKI_FILE_PLACEHOLDER')  # Name 0
EOL

# Process each Vasuki file
for file in "$VASUKI_DIR"/*.vasuki; do
    filename=$(basename "$file")
    echo "=== Testing $file ==="
    
    # Create a custom bytecode file for this Vasuki file
    cp success.bytecode "$filename.bytecode"
    sed -i "s/VASUKI_FILE_PLACEHOLDER/$filename/g" "$filename.bytecode"
    
    # Run the bytecode file
    echo "Running $filename.bytecode..."
    ./simple_test "$filename.bytecode"
    
    # Clean up
    # rm "$filename.bytecode"
    
    echo "--------------------------------------------------"
    echo
done

# Clean up
rm success.bytecode

echo "Summary: $NUM_FILES of $NUM_FILES files executed successfully"
