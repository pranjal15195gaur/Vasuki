"""
Read-Eval-Print Loop (REPL) for the Vasuki programming language.

This module provides an interactive shell for executing Vasuki code.
It supports multi-line input and maintains state between commands.
"""

from compiler.parser import parse
from compiler.errors import ParserError
from compiler.top import e, Environment

def main():
    """Run the Vasuki REPL.

    Creates an interactive shell that:
    1. Reads user input, supporting multi-line code blocks
    2. Parses and evaluates the input
    3. Prints the result of the evaluation
    4. Maintains environment state between commands

    The REPL continues until the user enters 'exit' or sends an EOF signal (Ctrl+D).
    """
    env = Environment()
    print("\033[1;92m")
    print("╔════════════════════════════════════════════╗")
    print("║           Welcome to the Vasuki REPL!      ║")
    print("╚════════════════════════════════════════════╝")
    print("\033[0m")
    print("Enter 'exit' to quit.")
    print("Enter a blank line to execute the code block.")

    while True:
        # Start a new code block
        code_lines = []
        prompt = ">>> "

        # Read lines until an empty line is entered
        while True:
            try:
                line = input(prompt)

                # Check for exit command
                if line.strip().lower() == "exit" and not code_lines:
                    return

                # Empty line ends the code block if we have some code
                if not line.strip() and code_lines:
                    break

                # Skip empty lines at the beginning
                if not line.strip() and not code_lines:
                    continue

                # Add the line to our code block
                code_lines.append(line)
                prompt = "... "  # Change prompt for continuation lines
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                code_lines = []
                break
            except EOFError:
                print("\nExiting...")
                return

        # Skip if no code was entered
        if not code_lines:
            continue

        # Join the lines and execute the code
        code = "\n".join(code_lines)

        try:
            tree = parse(code)
            result = e(tree, env)

            # Only print the result if the last line doesn't end with a semicolon
            if not code_lines[-1].strip().endswith(";"):
                if result is not None:
                    print(result)
        except ParserError as pe:
            print("Parse Error:", pe)
        except Exception as ex:
            print("Error:", ex)

if __name__ == "__main__":
    main()
