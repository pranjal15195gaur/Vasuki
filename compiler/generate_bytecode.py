#!/usr/bin/env python3
"""
Simple bytecode generator for testing the Vasuki VM
"""

import sys
import struct

def write_bytecode(filename, bytecode, constants, names):
    """Write bytecode to a file"""
    with open(filename, 'wb') as f:
        # Write bytecode
        f.write(struct.pack('<I', len(bytecode)))  # 4-byte unsigned int for size
        for byte in bytecode:
            f.write(struct.pack('B', byte))  # 1-byte unsigned char

        # Write constants
        f.write(struct.pack('<I', len(constants)))  # 4-byte unsigned int for size
        for constant in constants:
            if constant is None:
                f.write(struct.pack('B', 0))  # Type 0: Null
            elif isinstance(constant, bool):
                f.write(struct.pack('B', 1))  # Type 1: Boolean
                f.write(struct.pack('B', 1 if constant else 0))
            elif isinstance(constant, int):
                f.write(struct.pack('B', 2))  # Type 2: Integer
                f.write(struct.pack('<q', constant))  # 8-byte signed int
            elif isinstance(constant, float):
                f.write(struct.pack('B', 3))  # Type 3: Float
                f.write(struct.pack('<d', constant))  # 8-byte double
            elif isinstance(constant, str):
                f.write(struct.pack('B', 4))  # Type 4: String
                encoded = constant.encode('utf-8')
                f.write(struct.pack('<I', len(encoded)))  # 4-byte unsigned int for length
                f.write(encoded)

        # Write names
        f.write(struct.pack('<I', len(names)))  # 4-byte unsigned int for size
        for name in names:
            encoded = name.encode('utf-8')
            f.write(struct.pack('<I', len(encoded)))  # 4-byte unsigned int for length
            f.write(encoded)

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

def generate_test_bytecode():
    """Generate bytecode for a simple test program"""
    bytecode = [
        # Push two integers
        OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
        OpCode.PUSH_INT, 5, 0, 0, 0,   # Push 5

        # Add them
        OpCode.ADD,

        # Print the result
        OpCode.PRINT,

        # Push a string
        OpCode.PUSH_STRING, 0, 0,  # String index 0

        # Print the string
        OpCode.PRINT,

        # Define a function 'add'
        OpCode.FUNCTION, 1, 0,  # Function name index 1
        30, 0, 0, 0,  # Start position (30)
        2,            # 2 parameters
        2, 0,         # Parameter 1 name index (2)
        3, 0,         # Parameter 2 name index (3)

        # Jump over function body
        OpCode.JUMP, 10, 0, 0, 0,  # Jump to position 40

        # Function body starts here (position 30)
        OpCode.GET_LOCAL, 2, 0,  # Get parameter x
        OpCode.GET_LOCAL, 3, 0,  # Get parameter y
        OpCode.ADD,              # Add them
        OpCode.RETURN,           # Return the result

        # Main program continues here (position 40)
        # Get the function
        OpCode.GET_GLOBAL, 1, 0,  # Get function 'add'

        # Push arguments
        OpCode.PUSH_INT, 3, 0, 0, 0,  # Push 3
        OpCode.PUSH_INT, 4, 0, 0, 0,  # Push 4

        # Call the function
        OpCode.CALL, 2,  # Call with 2 arguments

        # Print the result
        OpCode.PRINT,

        # Push a value for the main program's implicit return
        OpCode.PUSH_INT, 42, 0, 0, 0,  # Push 42

        # Halt
        OpCode.HALT
    ]

    constants = []

    names = [
        "Hello, Vasuki!",  # String index 0
        "add",             # Function name (index 1)
        "x",               # Parameter 1 (index 2)
        "y"                # Parameter 2 (index 3)
    ]

    return bytecode, constants, names

def generate_missing_semicolon_test():
    """Generate bytecode for testing the missing semicolon feature"""
    bytecode = [
        # Push a string
        OpCode.PUSH_STRING, 0, 0,  # String index 0

        # Print the string
        OpCode.PRINT,

        # Define a function 'subtract' that returns x - y (with missing semicolon)
        OpCode.FUNCTION, 1, 0,  # Function name index 1
        20, 0, 0, 0,  # Start position (20)
        2,            # 2 parameters
        2, 0,         # Parameter 1 name index (2)
        3, 0,         # Parameter 2 name index (3)

        # Jump over function body
        OpCode.JUMP, 14, 0, 0, 0,  # Jump to position 34

        # Function body starts here (position 20)
        OpCode.GET_LOCAL, 2, 0,  # Get parameter x
        OpCode.GET_LOCAL, 3, 0,  # Get parameter y
        OpCode.SUB,              # Subtract
        OpCode.RETURN,           # Return (simulating missing semicolon)

        # Main program starts here (position 34)
        # Push the function name
        OpCode.GET_GLOBAL, 1, 0,  # Get function 'subtract'

        # Push arguments
        OpCode.PUSH_INT, 10, 0, 0, 0,  # Push 10
        OpCode.PUSH_INT, 3, 0, 0, 0,   # Push 3

        # Call the function
        OpCode.CALL, 2,  # Call with 2 arguments

        # Duplicate the result for printing
        OpCode.DUP,

        # Push a string
        OpCode.PUSH_STRING, 4, 0,  # String index 4

        # Print the string and the result
        OpCode.PRINT,
        OpCode.PRINT,

        # Push a value for the main program's implicit return
        OpCode.PUSH_INT, 42, 0, 0, 0,  # Push 42

        # Halt (the VM will return the top value on the stack)
        OpCode.HALT
    ]

    constants = []

    names = [
        "Testing missing semicolon feature...",  # String index 0
        "subtract",  # Function name (index 1)
        "x",         # Parameter 1 (index 2)
        "y",         # Parameter 2 (index 3)
        "Result of subtract(10, 3) = "  # String index 4
    ]

    return bytecode, constants, names

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_bytecode.py <output_file> [test_type]")
        sys.exit(1)

    output_file = sys.argv[1]
    test_type = sys.argv[2] if len(sys.argv) > 2 else "basic"

    if test_type == "missing_semicolon":
        bytecode, constants, names = generate_missing_semicolon_test()
    else:
        bytecode, constants, names = generate_test_bytecode()

    write_bytecode(output_file, bytecode, constants, names)
    print(f"Bytecode written to {output_file}")

if __name__ == "__main__":
    main()
