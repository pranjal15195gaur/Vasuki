#!/usr/bin/env python3
"""
Script to generate bytecode for a simple tail call optimization test
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

# Generate bytecode for a simple tail call optimization test
bytecode = [
    # Push a string
    OpCode.PUSH_STRING, 0, 0,  # String index 0
    
    # Print the string
    OpCode.PRINT,
    
    # Define a countdown function that uses tail call optimization
    OpCode.FUNCTION, 1, 0,  # Function name index 1 (countdown)
    20, 0, 0, 0,  # Start position (20)
    1,            # 1 parameter
    2, 0,         # Parameter 1 name index (2) - n
    
    # Jump over function body
    OpCode.JUMP, 30, 0, 0, 0,  # Jump to position 50
    
    # Function body starts here (position 20)
    # Print n
    OpCode.PUSH_STRING, 3, 0,  # String index 3 (Counting down: )
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PRINT,              # Print "Counting down: n"
    OpCode.PRINT,
    
    # if n <= 0 return n
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PUSH_INT, 0, 0, 0, 0,  # Push 0
    OpCode.LTE,                # n <= 0
    OpCode.JUMP_IF_FALSE, 10, 0, 0, 0,  # Jump to else branch if false
    
    # Return n
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.RETURN,             # Return n
    
    # else return countdown(n-1)
    OpCode.GET_GLOBAL, 1, 0,   # Get function countdown
    
    # First argument: n-1
    OpCode.GET_LOCAL, 2, 0,    # Get parameter n
    OpCode.PUSH_INT, 1, 0, 0, 0,  # Push 1
    OpCode.SUB,                # n - 1
    
    # Call countdown(n-1) with tail call optimization
    OpCode.TAIL_CALL, 1,       # Call with 1 argument (tail call)
    OpCode.RETURN,             # This return is needed for the VM to recognize it as a tail call
    
    # Main program continues here (position 50)
    # Call countdown(5)
    OpCode.PUSH_STRING, 4, 0,  # String index 4
    OpCode.PRINT,
    
    OpCode.GET_GLOBAL, 1, 0,   # Get function countdown
    OpCode.PUSH_INT, 5, 0, 0, 0,  # Push 5
    OpCode.CALL, 1,            # Call with 1 argument
    
    # Print the result
    OpCode.PUSH_STRING, 5, 0,  # String index 5
    OpCode.PRINT,
    OpCode.PRINT,
    
    # Call countdown(10)
    OpCode.PUSH_STRING, 6, 0,  # String index 6
    OpCode.PRINT,
    
    OpCode.GET_GLOBAL, 1, 0,   # Get function countdown
    OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
    OpCode.CALL, 1,            # Call with 1 argument
    
    # Print the result
    OpCode.PUSH_STRING, 5, 0,  # String index 5
    OpCode.PRINT,
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
    "Testing simple tail call optimization...",  # String index 0
    "countdown",                                # Function name (index 1)
    "n",                                        # Parameter name (index 2)
    "Counting down: ",                          # String index 3
    "Calling countdown(5)...",                  # String index 4
    "Result: ",                                 # String index 5
    "Calling countdown(10)..."                  # String index 6
]

# Write bytecode to a file
with open("simple_tail_call.bytecode", "wb") as f:
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

print("Bytecode written to simple_tail_call.bytecode")
