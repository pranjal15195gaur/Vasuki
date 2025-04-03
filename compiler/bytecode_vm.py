# bytecode_vm.py

import sys
from top import Environment, UserFunction  # Import your environment and function definitions
from bytecode import BytecodeGenerator  # The bytecode generator you created
from parser import parse  # Your parser

# A simple virtual machine to evaluate our bytecode instructions
class VM:
    def __init__(self, bytecode):
        self.instructions = bytecode.instructions
        self.pc = 0
        self.stack = []       # Our operand stack
        self.env = Environment()  # Global environment
        self.call_stack = []  # To save (pc, env) when calling a function

        # Preprocess instructions to map labels to instruction indices
        self.labels = {}
        for idx, instr in enumerate(self.instructions):
            if instr.opcode == "LABEL":
                self.labels[instr.operand] = idx

    def run(self):
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            # Process each instruction by opcode
            if instr.opcode == "LOAD_CONST":
                self.stack.append(instr.operand)

            elif instr.opcode == "STORE_VAR":
                value = self.stack.pop()
                self.env.declare(instr.operand, value)

            elif instr.opcode == "LOAD_VAR":
                value = self.env.lookup(instr.operand)
                self.stack.append(value)

            elif instr.opcode in ("ADD", "SUB", "MUL", "DIV", "MOD", "POW"):
                b = self.stack.pop()
                a = self.stack.pop()
                if instr.opcode == "ADD":
                    self.stack.append(a + b)
                elif instr.opcode == "SUB":
                    self.stack.append(a - b)
                elif instr.opcode == "MUL":
                    self.stack.append(a * b)
                elif instr.opcode == "DIV":
                    self.stack.append(a / b)
                elif instr.opcode == "MOD":
                    self.stack.append(a % b)
                elif instr.opcode == "POW":
                    self.stack.append(a ** b)

            elif instr.opcode in ("LT", "LE", "GT", "GE", "EQ", "NE"):
                b = self.stack.pop()
                a = self.stack.pop()
                if instr.opcode == "LT":
                    self.stack.append(a < b)
                elif instr.opcode == "LE":
                    self.stack.append(a <= b)
                elif instr.opcode == "GT":
                    self.stack.append(a > b)
                elif instr.opcode == "GE":
                    self.stack.append(a >= b)
                elif instr.opcode == "EQ":
                    self.stack.append(a == b)
                elif instr.opcode == "NE":
                    self.stack.append(a != b)

            elif instr.opcode in ("AND", "OR"):
                b = self.stack.pop()
                a = self.stack.pop()
                if instr.opcode == "AND":
                    self.stack.append(a and b)
                elif instr.opcode == "OR":
                    self.stack.append(a or b)

            elif instr.opcode == "NEG":
                a = self.stack.pop()
                self.stack.append(-a)

            elif instr.opcode == "PRINT":
                value = self.stack.pop()
                print(value)

            elif instr.opcode == "JUMP_IF_FALSE":
                condition = self.stack.pop()
                if not condition:
                    self.pc = self.labels[instr.operand]
                    continue  # Skip the pc increment at the bottom

            elif instr.opcode == "JUMP":
                self.pc = self.labels[instr.operand]
                continue

            elif instr.opcode == "CALL":
                # The operand is a tuple: (function name, number of arguments)
                func_name, num_args = instr.operand
                # Pop the arguments off the stack (they were pushed in order)
                args = [self.stack.pop() for _ in range(num_args)]
                args.reverse() # Reverse to maintain order
                func = self.env.lookup(func_name)
                if not isinstance(func, UserFunction):
                    raise ValueError(f"{func_name} is not a function")
                # Save the current state for when the function returns.
                self.call_stack.append((self.pc + 1, self.env))
                # Create a new environment using the function's closure.
                new_env = Environment(func.closure)
                # Add the function itself to the new environment so recursive calls work.
                new_env.declare(func_name, func)
                # Declare the parameters in the new environment.
                for param, arg in zip(func.params, args):
                    new_env.declare(param, arg)
                self.env = new_env
                # Jump to the function entry point. The generator labels function entries as "func_<name>"
                label = f"func_{func_name}"
                if label not in self.labels:
                    raise ValueError(f"Function label {label} not found")
                self.pc = self.labels[label]
                continue

            elif instr.opcode == "RETURN":
                ret_value = self.stack.pop()
                if not self.call_stack:
                    # No calling function; we finish execution
                    return ret_value
                # Restore previous PC and environment
                self.pc, self.env = self.call_stack.pop()
                self.stack.append(ret_value)
                continue

            elif instr.opcode == "BUILD_ARRAY":
                n = instr.operand
                arr = [self.stack.pop() for _ in range(n)]
                arr.reverse()
                self.stack.append(arr)

            elif instr.opcode == "LOAD_INDEX":
                idx = self.stack.pop()
                arr = self.stack.pop()
                # Using zero-based indexing here
                self.stack.append(arr[idx])

            elif instr.opcode == "LABEL":
                # No action needed at a label.
                pass

            else:
                raise ValueError(f"Unknown opcode: {instr.opcode}")

            self.pc += 1
        return None

# Main entry point: lex, parse, generate bytecode, then run it.
def main():
    if len(sys.argv) < 2:
        print("Usage: python bytecode_vm.py <source_file>")
        sys.exit(1)
    source_file = sys.argv[1]
    try:
        with open(source_file, "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

    # Lex and parse the source code into an AST.
    try:
        ast = parse(source_code)
        print("printing the AST formed : ")
        from pprint import pprint
        pprint(ast)
    except Exception as e:
        print("Parsing error:", e)
        sys.exit(1)

    # Generate bytecode from the AST.
    generator = BytecodeGenerator()
    bytecode = generator.generate(ast)
    print("printing the bytecode formed : ")
    from pprint import pprint
    pprint(bytecode)
    # Create and run the VM.
    vm = VM(bytecode)
    result = vm.run()
    if result is not None:
        print("Program result:", result)

if __name__ == "__main__":
    main()
