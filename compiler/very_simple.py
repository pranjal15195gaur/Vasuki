#!/usr/bin/env python3
"""
Script to generate bytecode for a very simple test
"""

import struct

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

# Generate bytecode for a very simple test
bytecode = [
    # Push a string
    OpCode.PUSH_STRING, 0, 0,  # String index 0
    
    # Print the string
    OpCode.PRINT,
    
    # Push two integers
    OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
    OpCode.PUSH_INT, 5, 0, 0, 0,   # Push 5
    
    # Add them
    OpCode.ADD,
    
    # Print the result
    OpCode.PRINT,
    
    # Push a value for the main program's implicit return
    OpCode.PUSH_INT, 42, 0, 0, 0,  # Push 42 (missing semicolon - this is the return value)
    
    # Halt
    OpCode.HALT
]

# Constants
constants = []

# Names (strings)
names = [
    "Testing a very simple program..."
]

# Write bytecode to a file
with open("very_simple.bytecode", "wb") as f:
    # Write bytecode
    f.write(struct.pack("<I", len(bytecode)))  # 4-byte unsigned int for size
    for byte in bytecode:
        f.write(struct.pack("B", byte))  # 1-byte unsigned char
    
    # Write constants
    f.write(struct.pack("<I", len(constants)))  # 4-byte unsigned int for size
    
    # Write names
    f.write(struct.pack("<I", len(names)))  # 4-byte unsigned int for size
    for name in names:
        encoded = name.encode("utf-8")
        f.write(struct.pack("<I", len(encoded)))  # 4-byte unsigned int for length
        f.write(encoded)

print("Bytecode written to very_simple.bytecode")
