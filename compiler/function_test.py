#!/usr/bin/env python3
"""
Script to generate bytecode for testing functions with the missing semicolon feature
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

# Generate bytecode for a function test
bytecode = [
    # Push a string
    OpCode.PUSH_STRING, 0, 0,  # String index 0

    # Print the string
    OpCode.PRINT,

    # Define a function 'subtract' that returns x - y (with missing semicolon)
    OpCode.FUNCTION, 1, 0,  # Function name index 1
    30, 0, 0, 0,  # Start position (30)
    2,            # 2 parameters
    2, 0,         # Parameter 1 name index (2)
    3, 0,         # Parameter 2 name index (3)

    # Jump over function body
    OpCode.JUMP, 14, 0, 0, 0,  # Jump to position 40

    # Function body starts here (position 30)
    OpCode.GET_LOCAL, 2, 0,  # Get parameter x
    OpCode.GET_LOCAL, 3, 0,  # Get parameter y
    OpCode.SUB,              # Subtract (missing semicolon - this is the return value)
    OpCode.RETURN,           # Return (this is added by the compiler for the missing semicolon)

    # Main program continues here (position 40)
    # Push a string
    OpCode.PUSH_STRING, 4, 0,  # String index 4

    # Print the string
    OpCode.PRINT,

    # Get the function
    OpCode.GET_GLOBAL, 1, 0,  # Get function 'subtract'

    # Push arguments
    OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
    OpCode.PUSH_INT, 3, 0, 0, 0,   # Push 3

    # Call the function
    OpCode.CALL, 2,  # Call with 2 arguments

    # Print the result
    OpCode.PRINT,

    # Define another function 'add' that returns x + y (with missing semicolon)
    OpCode.FUNCTION, 5, 0,  # Function name index 5
    70, 0, 0, 0,  # Start position (70)
    2,            # 2 parameters
    2, 0,         # Parameter 1 name index (2)
    3, 0,         # Parameter 2 name index (3)

    # Jump over function body
    OpCode.JUMP, 14, 0, 0, 0,  # Jump to position 80

    # Function body starts here (position 70)
    OpCode.GET_LOCAL, 2, 0,  # Get parameter x
    OpCode.GET_LOCAL, 3, 0,  # Get parameter y
    OpCode.ADD,              # Add (missing semicolon - this is the return value)
    OpCode.RETURN,           # Return (this is added by the compiler for the missing semicolon)

    # Main program continues here (position 80)
    # Push a string
    OpCode.PUSH_STRING, 6, 0,  # String index 6

    # Print the string
    OpCode.PRINT,

    # Get the function
    OpCode.GET_GLOBAL, 5, 0,  # Get function 'add'

    # Push arguments
    OpCode.PUSH_INT, 7, 0, 0, 0,  # Push 7
    OpCode.PUSH_INT, 8, 0, 0, 0,  # Push 8

    # Call the function
    OpCode.CALL, 2,  # Call with 2 arguments

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
    "Testing functions with missing semicolons...",  # String index 0
    "subtract",                                      # Function name (index 1)
    "x",                                             # Parameter 1 (index 2)
    "y",                                             # Parameter 2 (index 3)
    "Calling subtract(10, 3):",                      # String index 4
    "add",                                           # Function name (index 5)
    "Calling add(7, 8):"                             # String index 6
]

# Write bytecode to a file
with open("function_test.bytecode", "wb") as f:
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

print("Bytecode written to function_test.bytecode")
