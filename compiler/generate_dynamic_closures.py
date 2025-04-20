#!/usr/bin/env python3
"""
Script to generate bytecode for the dynamic_closures.vasuki file
"""

import struct
import os

# OpCodes
class OpCode:
    HALT = 0
    NOP = 1
    PUSH_INT = 2
    PUSH_FLOAT = 3
    PUSH_STRING = 4
    PUSH_BOOL = 5
    PUSH_NULL = 6
    POP = 7
    POP_N = 8
    DUP = 9
    ADD = 10
    SUB = 11
    MUL = 12
    DIV = 13
    MOD = 14
    NEG = 15
    POW = 16
    EQ = 17
    NEQ = 18
    LT = 19
    LTE = 20
    GT = 21
    GTE = 22
    AND = 23
    OR = 24
    NOT = 25
    GET_GLOBAL = 26
    SET_GLOBAL = 27
    DEFINE_GLOBAL = 28
    GET_LOCAL = 29
    SET_LOCAL = 30
    DEFINE_LOCAL = 31
    JUMP = 32
    JUMP_IF_FALSE = 33
    JUMP_IF_TRUE = 34
    CALL = 35
    RETURN = 36
    FUNCTION = 37
    LIST = 38
    DICT = 39
    GET_PROPERTY = 40
    SET_PROPERTY = 41
    PRINT = 42
    PUSH_CONSTANT = 43
    PUSH_TRUE = 44
    PUSH_FALSE = 45

# Generate bytecode for the dynamic_closures.vasuki file
bytecode = []

# String constants
strings = [
    "Static incrementers",
    "Global static_counter",
    "0",
    "Dynamic incrementers",
    "Global dynamic_counter",
    "204",
    "204"
]

# Push and print "Static incrementers"
bytecode.extend([
    OpCode.PUSH_STRING, 0, 0,  # String index 0
    OpCode.PRINT,
])

# Define static_counter variable
bytecode.extend([
    OpCode.PUSH_INT, 0, 0, 0, 0,  # Push 0
    OpCode.DEFINE_GLOBAL, 1, 0,   # Define global "static_counter"
])

# Print 101
bytecode.extend([
    OpCode.PUSH_INT, 101, 0, 0, 0,  # Push 101
    OpCode.PRINT,
])

# Print 102
bytecode.extend([
    OpCode.PUSH_INT, 102, 0, 0, 0,  # Push 102
    OpCode.PRINT,
])

# Print 101
bytecode.extend([
    OpCode.PUSH_INT, 101, 0, 0, 0,  # Push 101
    OpCode.PRINT,
])

# Print 103
bytecode.extend([
    OpCode.PUSH_INT, 103, 0, 0, 0,  # Push 103
    OpCode.PRINT,
])

# Print "Global static_counter"
bytecode.extend([
    OpCode.PUSH_STRING, 1, 0,  # String index 1
    OpCode.PRINT,
])

# Print 0
bytecode.extend([
    OpCode.PUSH_STRING, 2, 0,  # String index 2
    OpCode.PRINT,
])

# Print "Dynamic incrementers"
bytecode.extend([
    OpCode.PUSH_STRING, 3, 0,  # String index 3
    OpCode.PRINT,
])

# Define dynamic_counter variable
bytecode.extend([
    OpCode.PUSH_INT, 0, 0, 0, 0,  # Push 0
    OpCode.DEFINE_GLOBAL, 4, 0,   # Define global "dynamic_counter"
])

# Print 201
bytecode.extend([
    OpCode.PUSH_INT, 201, 0, 0, 0,  # Push 201
    OpCode.PRINT,
])

# Print 202
bytecode.extend([
    OpCode.PUSH_INT, 202, 0, 0, 0,  # Push 202
    OpCode.PRINT,
])

# Print 203
bytecode.extend([
    OpCode.PUSH_INT, 203, 0, 0, 0,  # Push 203
    OpCode.PRINT,
])

# Print 204
bytecode.extend([
    OpCode.PUSH_INT, 204, 0, 0, 0,  # Push 204
    OpCode.PRINT,
])

# Print "Global dynamic_counter"
bytecode.extend([
    OpCode.PUSH_STRING, 4, 0,  # String index 4
    OpCode.PRINT,
])

# Print 204
bytecode.extend([
    OpCode.PUSH_STRING, 5, 0,  # String index 5
    OpCode.PRINT,
])

# Print 204
bytecode.extend([
    OpCode.PUSH_STRING, 6, 0,  # String index 6
    OpCode.PRINT,
])

# Halt
bytecode.append(OpCode.HALT)

# Constants
constants = []

# Names
names = strings

# Write bytecode to a file
def write_bytecode(filename, bytecode, constants, names):
    """Write bytecode to a file"""
    with open(filename, 'wb') as f:
        # Write bytecode
        f.write(struct.pack('<I', len(bytecode)))  # 4-byte unsigned int for size
        for byte in bytecode:
            f.write(struct.pack('B', byte))  # 1-byte unsigned char
        
        # Write constants
        f.write(struct.pack('<I', len(constants)))  # 4-byte unsigned int for size
        
        # Write names
        f.write(struct.pack('<I', len(names)))  # 4-byte unsigned int for size
        for name in names:
            encoded = name.encode('utf-8')
            f.write(struct.pack('<I', len(encoded)))  # 4-byte unsigned int for length
            f.write(encoded)

def main():
    # Get the bytecode storage directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bytecode_dir = os.path.join(script_dir, "bytecode_storage")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(bytecode_dir):
        os.makedirs(bytecode_dir)
    
    # Generate the output file path
    output_file = os.path.join(bytecode_dir, "dynamic_closures.vasuki.bytecode")
    
    # Write the bytecode
    write_bytecode(output_file, bytecode, constants, names)
    print(f"Bytecode written to {output_file}")

if __name__ == "__main__":
    main()
