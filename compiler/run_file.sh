#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <vasuki_file>"
    exit 1
fi

# Make sure the compiler.py script is executable
chmod +x ../compiler.py

# Compile the Vasuki runner
make vasuki_runner

# Run the specified Vasuki file with verbose output and bytecode dump
./vasuki_runner -v -d "$1"
