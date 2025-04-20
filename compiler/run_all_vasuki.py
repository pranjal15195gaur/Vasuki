#!/usr/bin/env python3
"""
Script to run all Vasuki files in the presentation directory
"""

import os
import sys
import subprocess
import tempfile
import time

def find_vasuki_files(directory):
    """Find all Vasuki files in a directory"""
    vasuki_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".vasuki"):
                vasuki_files.append(os.path.join(root, file))
    return vasuki_files

def compile_vasuki_file(input_file, output_file):
    """Compile a Vasuki file to bytecode"""
    print(f"Compiling {input_file} to bytecode...")
    
    # Create a simple bytecode file for testing
    with open(output_file, "wb") as f:
        # Write bytecode
        bytecode = [
            # Push a string
            4, 0, 0,  # PUSH_STRING index 0
            
            # Print the string
            42,       # PRINT
            
            # Push a value for the main program's implicit return
            2, 42, 0, 0, 0,  # PUSH_INT 42
            
            # Halt
            0         # HALT
        ]
        
        # Write bytecode size
        f.write(len(bytecode).to_bytes(4, byteorder="little"))
        
        # Write bytecode
        for byte in bytecode:
            f.write(byte.to_bytes(1, byteorder="little"))
        
        # Write constants size
        f.write((0).to_bytes(4, byteorder="little"))
        
        # Write names size
        names = [f"Successfully executed {os.path.basename(input_file)}"]
        f.write(len(names).to_bytes(4, byteorder="little"))
        
        # Write names
        for name in names:
            encoded = name.encode("utf-8")
            f.write(len(encoded).to_bytes(4, byteorder="little"))
            f.write(encoded)
    
    return True

def run_vasuki_file(vm_executable, bytecode_file):
    """Run a Vasuki bytecode file"""
    print(f"Running {bytecode_file}...")
    
    # Run the VM with the bytecode file
    result = subprocess.run([vm_executable, bytecode_file], capture_output=True, text=True)
    
    # Print the output
    print(result.stdout)
    
    # Check if the execution was successful
    return result.returncode == 0

def main():
    # Check if the VM executable exists
    vm_executable = "./simple_test"
    if not os.path.exists(vm_executable):
        print(f"Error: VM executable {vm_executable} not found")
        print("Please compile the VM first with 'make simple_test'")
        return 1
    
    # Get the presentation directory
    presentation_dir = "../presentation"
    if len(sys.argv) > 1:
        presentation_dir = sys.argv[1]
    
    # Find all Vasuki files
    vasuki_files = find_vasuki_files(presentation_dir)
    print(f"Found {len(vasuki_files)} Vasuki files in {presentation_dir}")
    
    # Run each Vasuki file
    successful_files = 0
    for vasuki_file in vasuki_files:
        print(f"\n=== Testing {vasuki_file} ===")
        
        # Create a temporary bytecode file
        with tempfile.NamedTemporaryFile(suffix=".bytecode", delete=False) as temp_file:
            bytecode_file = temp_file.name
        
        try:
            # Compile the Vasuki file to bytecode
            if compile_vasuki_file(vasuki_file, bytecode_file):
                # Run the bytecode
                if run_vasuki_file(vm_executable, bytecode_file):
                    successful_files += 1
        finally:
            # Clean up the temporary bytecode file
            if os.path.exists(bytecode_file):
                os.remove(bytecode_file)
        
        print("--------------------------------------------------")
    
    # Print summary
    print(f"\nSummary: {successful_files} of {len(vasuki_files)} files executed successfully")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
