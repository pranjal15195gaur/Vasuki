#!/usr/bin/env python3
"""
Script to generate bytecode for testing tail call optimization
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
    TAIL_CALL = 46  # New opcode for tail call optimization

# Generate bytecode for a recursive factorial function with tail call optimization
bytecode = [
    # Push a string
    OpCode.PUSH_STRING, 0, 0,  # String index 0

    # Print the string
    OpCode.PRINT,

    # Define a factorial function with an accumulator for tail call optimization
    OpCode.FUNCTION, 1, 0,  # Function name index 1 (factorial_tail)
    20, 0, 0, 0,  # Start position (20)
    2,            # 2 parameters
    2, 0,         # Parameter 1 name index (2) - n
    3, 0,         # Parameter 2 name index (3) - acc

    # Jump over function body
    OpCode.JUMP, 40, 0, 0, 0,  # Jump to position 60

    # Function body starts here (position 20)
    # if n <= 1 return acc
    OpCode.GET_LOCAL, 2, 0,  # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.LTE,              # n <= 1
    OpCode.JUMP_IF_FALSE, 12, 0, 0, 0,  # Jump to else branch if false

    # Return acc
    OpCode.GET_LOCAL, 3, 0,  # Get parameter acc
    OpCode.RETURN,           # Return acc

    # else return factorial_tail(n-1, n*acc)
    OpCode.GET_GLOBAL, 1, 0,  # Get function factorial_tail

    # First argument: n-1
    OpCode.GET_LOCAL, 2, 0,  # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.SUB,              # n - 1

    # Second argument: n*acc
    OpCode.GET_LOCAL, 2, 0,  # Get parameter n
    OpCode.GET_LOCAL, 3, 0,  # Get parameter acc
    OpCode.MUL,              # n * acc

    # Call factorial_tail(n-1, n*acc) with tail call optimization
    OpCode.TAIL_CALL, 2,     # Call with 2 arguments (tail call)
    OpCode.RETURN,           # This return is needed for the VM to recognize it as a tail call

    # Main program continues here (position 50)
    # Define a wrapper function that calls factorial_tail with initial accumulator of 1
    OpCode.FUNCTION, 4, 0,  # Function name index 4 (factorial)
    60, 0, 0, 0,  # Start position (60)
    1,            # 1 parameter
    2, 0,         # Parameter 1 name index (2) - n

    # Jump over function body
    OpCode.JUMP, 20, 0, 0, 0,  # Jump to position 80

    # Function body starts here (position 60)
    # return factorial_tail(n, 1)
    OpCode.GET_GLOBAL, 1, 0,  # Get function factorial_tail
    OpCode.GET_LOCAL, 2, 0,   # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1 (initial accumulator)
    OpCode.CALL, 2,           # Call with 2 arguments
    OpCode.RETURN,            # Return the result

    # Main program continues here (position 75)
    # Print a message
    OpCode.PUSH_STRING, 5, 0,  # String index 5
    OpCode.PRINT,

    # Call factorial(5)
    OpCode.GET_GLOBAL, 4, 0,  # Get function factorial
    OpCode.PUSH_INT, 5, 0, 0, 0,  # Push 5
    OpCode.CALL, 1,           # Call with 1 argument

    # Print the result
    OpCode.PRINT,

    # Print a message
    OpCode.PUSH_STRING, 6, 0,  # String index 6
    OpCode.PRINT,

    # Call factorial(10)
    OpCode.GET_GLOBAL, 4, 0,  # Get function factorial
    OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
    OpCode.CALL, 1,           # Call with 1 argument

    # Print the result
    OpCode.PRINT,

    # Print a message
    OpCode.PUSH_STRING, 7, 0,  # String index 7
    OpCode.PRINT,

    # Call factorial(20)
    OpCode.GET_GLOBAL, 4, 0,  # Get function factorial
    OpCode.PUSH_INT, 20, 0, 0, 0,  # Push 20
    OpCode.CALL, 1,           # Call with 1 argument

    # Print the result
    OpCode.PRINT,

    # Push a value for the main program's implicit return
    OpCode.PUSH_INT, 42, 0, 0, 0,  # Push 42

    # Halt
    OpCode.HALT
]

# Constants
constants = []

# Names (strings)
names = [
    "Testing tail call optimization with factorial function...",  # String index 0
    "factorial_tail",                                            # Function name (index 1)
    "n",                                                         # Parameter name (index 2)
    "acc",                                                       # Parameter name (index 3)
    "factorial",                                                 # Function name (index 4)
    "factorial(5) = ",                                           # String index 5
    "factorial(10) = ",                                          # String index 6
    "factorial(20) = "                                           # String index 7
]

# Write bytecode to a file
with open("tail_call_test.bytecode", "wb") as f:
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

print("Bytecode written to tail_call_test.bytecode")
