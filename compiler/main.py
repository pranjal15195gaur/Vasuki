from compiler.parser import parse
from compiler.top import e, Environment
from compiler.errors import VasukiError
import sys
import os

def main():
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
        # Parse the code with the filename for better error messages
        ast = parse(code, os.path.basename(filename))
        # Execute the code
        e(ast, Environment())
    except VasukiError as error:
        # Print the formatted error message
        print(f"\033[91m{error}\033[0m")  # Red color for errors
        sys.exit(1)
    except Exception as ex:
        # Unexpected errors
        print(f"\033[91mInternal error: {ex}\033[0m")
        # Print stack trace for debugging
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

