#!/usr/bin/env python3
"""
Script to generate bytecode for a working tail call optimization test
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

# Generate bytecode for a working tail call optimization test
bytecode = []

# Push a welcome message
bytecode.extend([
    OpCode.PUSH_STRING, 0, 0,  # String index 0
    OpCode.PRINT,
])

# Define the countdown function
bytecode.extend([
    # Define countdown function
    OpCode.FUNCTION, 1, 0,  # Function name index 1 (countdown)
    50, 0, 0, 0,  # Start position (50)
    1,            # 1 parameter
    2, 0,         # Parameter 1 name index (2) - n
])

# Define the factorial function with tail call optimization
bytecode.extend([
    # Define factorial_tail function
    OpCode.FUNCTION, 3, 0,  # Function name index 3 (factorial_tail)
    100, 0, 0, 0,  # Start position (100)
    2,            # 2 parameters
    4, 0,         # Parameter 1 name index (4) - n
    5, 0,         # Parameter 2 name index (5) - acc
])

# Jump to main program
bytecode.extend([
    OpCode.JUMP, 130, 0, 0, 0,  # Jump to position 160
])

# Countdown function body starts here (position 50)
bytecode.extend([
    # Print current value
    OpCode.PUSH_STRING, 6, 0,  # String index 6
    OpCode.PRINT,
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PRINT,

    # if n <= 0 return 0
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PUSH_INT, 0, 0, 0, 0,  # Push 0
    OpCode.LTE,                # n <= 0
    OpCode.JUMP_IF_FALSE, 10, 0, 0, 0,  # Jump to else branch if false

    # Return 0
    OpCode.PUSH_INT, 0, 0, 0, 0,  # Push 0
    OpCode.RETURN,             # Return 0
])

# else return countdown(n-1)
bytecode.extend([
    # Get function countdown
    OpCode.GET_GLOBAL, 1, 0,   # Get function countdown

    # First argument: n-1
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.SUB,                # n - 1

    # Call countdown(n-1) with tail call optimization
    OpCode.TAIL_CALL, 1,       # Call with 1 argument (tail call)
    OpCode.RETURN,             # This return is needed for the VM to recognize it as a tail call
])

# Factorial_tail function body starts here (position 100)
bytecode.extend([
    # Print current values
    OpCode.PUSH_STRING, 7, 0,  # String index 7
    OpCode.PRINT,
    OpCode.GET_LOCAL, 4, 0,    # Get parameter n
    OpCode.PRINT,
    OpCode.PUSH_STRING, 8, 0,  # String index 8
    OpCode.PRINT,
    OpCode.GET_LOCAL, 5, 0,    # Get parameter acc
    OpCode.PRINT,

    # if n <= 1 return acc
    OpCode.GET_LOCAL, 4, 0,    # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.LTE,                # n <= 1
    OpCode.JUMP_IF_FALSE, 10, 0, 0, 0,  # Jump to else branch if false

    # Return acc
    OpCode.GET_LOCAL, 5, 0,    # Get parameter acc
    OpCode.RETURN,             # Return acc
])

# else return factorial_tail(n-1, n*acc)
bytecode.extend([
    # Get function factorial_tail
    OpCode.GET_GLOBAL, 3, 0,   # Get function factorial_tail

    # First argument: n-1
    OpCode.GET_LOCAL, 4, 0,    # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.SUB,                # n - 1

    # Second argument: n*acc
    OpCode.GET_LOCAL, 4, 0,    # Get parameter n
    OpCode.GET_LOCAL, 5, 0,    # Get parameter acc
    OpCode.MUL,                # n * acc

    # Call factorial_tail(n-1, n*acc) with tail call optimization
    OpCode.TAIL_CALL, 2,       # Call with 2 arguments (tail call)
    OpCode.RETURN,             # This return is needed for the VM to recognize it as a tail call
])

# Define the factorial wrapper function
bytecode.extend([
    # Define factorial function
    OpCode.FUNCTION, 9, 0,     # Function name index 9 (factorial)
    150, 0, 0, 0,              # Start position (150)
    1,                         # 1 parameter
    4, 0,                      # Parameter 1 name index (4) - n
])

# Jump to main program
bytecode.extend([
    OpCode.JUMP, 40, 0, 0, 0,  # Jump to position 190
])

# Factorial function body starts here (position 150)
bytecode.extend([
    # return factorial_tail(n, 1)
    OpCode.GET_GLOBAL, 3, 0,   # Get function factorial_tail
    OpCode.GET_LOCAL, 4, 0,    # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1 (initial accumulator)
    OpCode.CALL, 2,            # Call with 2 arguments
    OpCode.RETURN,             # Return the result
])

# Main program starts here (position 200)
bytecode.extend([
    # Test countdown function
    OpCode.PUSH_STRING, 10, 0,  # String index 10
    OpCode.PRINT,

    OpCode.GET_GLOBAL, 1, 0,   # Get function countdown
    OpCode.PUSH_INT, 5, 0, 0, 0,  # Push 5
    OpCode.CALL, 1,            # Call with 1 argument

    OpCode.PUSH_STRING, 11, 0,  # String index 11
    OpCode.PRINT,
    OpCode.PRINT,

    # Test factorial function
    OpCode.PUSH_STRING, 12, 0,  # String index 12
    OpCode.PRINT,

    OpCode.GET_GLOBAL, 9, 0,   # Get function factorial
    OpCode.PUSH_INT, 5, 0, 0, 0,  # Push 5
    OpCode.CALL, 1,            # Call with 1 argument

    OpCode.PUSH_STRING, 11, 0,  # String index 11
    OpCode.PRINT,
    OpCode.PRINT,

    # Push a value for the main program's implicit return
    OpCode.PUSH_INT, 42, 0, 0, 0,  # Push 42

    # Halt
    OpCode.HALT
])

# Constants
constants = []

# Names (strings)
names = [
    "Testing working tail call optimization...",  # String index 0
    "countdown",                                 # Function name (index 1)
    "n",                                         # Parameter name (index 2)
    "factorial_tail",                            # Function name (index 3)
    "n",                                         # Parameter name (index 4)
    "acc",                                       # Parameter name (index 5)
    "Counting down: ",                           # String index 6
    "factorial_tail(n=",                         # String index 7
    ", acc=",                                    # String index 8
    "factorial",                                 # Function name (index 9)
    "Testing countdown(5)...",                   # String index 10
    "Result: ",                                  # String index 11
    "Testing factorial(5)..."                    # String index 12
]

# Write bytecode to a file
with open("working_tail_call.bytecode", "wb") as f:
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

print("Bytecode written to working_tail_call.bytecode")
