#!/bin/bash

# Make sure the compiler.py script is executable
chmod +x ../compiler.py

# Compile the test program
make

# Run the test program
if [ $# -eq 0 ]; then
    # No arguments, test all files in the presentation directory
    ./test_vm ../presentation
else
    # Test the specified file or directory
    ./test_vm "$1"
fi
