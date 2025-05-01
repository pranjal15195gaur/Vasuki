"""
Main entry point for the Vasuki programming language interpreter.

This module provides the main function to parse and execute Vasuki source files.
It handles command-line arguments, file loading, and error reporting.
"""

from compiler.parser import parse
from compiler.top import e, Environment
from compiler.errors import VasukiError
import sys
import os
import time
import random

def main():
    """Execute a Vasuki source file specified as a command-line argument.

    This function:
    1. Seeds the random number generator with the current time
    2. Reads the source file specified as a command-line argument
    3. Parses the source code into an abstract syntax tree
    4. Executes the AST in a new environment
    5. Handles and reports any errors that occur during execution

    Returns:
        None. Exits with status code 0 on success, 1 on error.
    """
    # Seed random number generator with current time
    random.seed(int(time.time()))

    if len(sys.argv) < 2:
        print("Usage: python -m compiler.main <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as ex:
        print(f"Error reading file: {ex}")
        sys.exit(1)

    try:
        # Parse and execute the code
        ast = parse(code, os.path.basename(filename))
        e(ast, Environment())
    except VasukiError as error:
        # Format and display language errors
        print(f"\033[91m{error}\033[0m")  # Red color for errors
        sys.exit(1)
    except Exception as ex:
        # Handle unexpected internal errors
        print(f"\033[91mInternal error: {ex}\033[0m")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

