#!/bin/bash

# Make sure the VM is compiled
make simple_test

# Run all Vasuki files in the presentation directory
python3 run_all_vasuki.py ../presentation
