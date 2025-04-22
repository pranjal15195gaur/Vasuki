# bytecode_pure.py

from enum import Enum, auto
from top import Environment, UserFunction, Int, Float, String, Boolean, Dictionary

# Define opcodes as an enum for clarity
class OC(Enum):
    PUSH = auto()    # Push a constant onto the stack
    STORE = auto()   # Store a value in a variable
    GET = auto()     # Get a variable's value
    ADD = auto()     # Add two values
    SUB = auto()     # Subtract two values
    MUL = auto()     # Multiply two values
    DIV = auto()     # Divide two values
    MOD = auto()     # Modulo operation
    POW = auto()     # Power operation
    NEG = auto()     # Negate a value
    LT = auto()      # Less than comparison
    LE = auto()      # Less than or equal comparison
    GT = auto()      # Greater than comparison
    GE = auto()      # Greater than or equal comparison
    EQ = auto()      # Equal comparison
    NE = auto()      # Not equal comparison
    AND = auto()     # Logical AND
    OR = auto()      # Logical OR
    PRINT = auto()   # Print a value
    JMP = auto()     # Unconditional jump
    JF = auto()      # Jump if false
    CALL = auto()    # Call a function
    RET = auto()     # Return from a function
    MAKE_FUNC = auto() # Create a function
    HALT = auto()    # Stop execution
    READ = auto()    # Read from input (terminal)
    ARRAY_INDEX = auto() # Get an element from an array
    ARRAY_SET = auto()  # Set an element in an array

# Instruction class
class Instruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        if self.operand is not None:
            return f"({self.opcode}, {repr(self.operand)})"
        return f"({self.opcode}, None)"

# Bytecode class
class Bytecode:
    def __init__(self):
        self.instructions = []
        self.function_table = {}  # Maps function names to instruction indices

    def add(self, opcode, operand=None):
        self.instructions.append(Instruction(opcode, operand))
        return len(self.instructions) - 1  # Return the index of the added instruction

    def __repr__(self):
        return "\n".join(f"{i}: {instr}" for i, instr in enumerate(self.instructions))

# BytecodeGenerator class
class BytecodeGenerator:
    def __init__(self):
        self.bytecode = Bytecode()
        self.function_table = {}  # Maps function names to instruction indices
        self.current_function = None

    def generate(self, ast):
        self.visit(ast)
        self.bytecode.add(OC.HALT)  # Add a HALT instruction at the end
        return self.bytecode

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Int(self, node):
        self.bytecode.add(OC.PUSH, int(node.val))

    def visit_Float(self, node):
        self.bytecode.add(OC.PUSH, float(node.val))

    def visit_String(self, node):
        self.bytecode.add(OC.PUSH, node.val)

    def visit_Boolean(self, node):
        # The val attribute might be a string or a boolean
        if isinstance(node.val, str):
            value = node.val.lower() == 'true'
        else:
            value = node.val
        self.bytecode.add(OC.PUSH, value)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

        op = node.op
        if op == '+':
            self.bytecode.add(OC.ADD)
        elif op == '-':
            self.bytecode.add(OC.SUB)
        elif op == '*':
            self.bytecode.add(OC.MUL)
        elif op == '/':
            self.bytecode.add(OC.DIV)
        elif op == '%':
            self.bytecode.add(OC.MOD)
        elif op == '**':
            self.bytecode.add(OC.POW)
        elif op == '<':
            self.bytecode.add(OC.LT)
        elif op == '<=':
            self.bytecode.add(OC.LE)
        elif op == '>':
            self.bytecode.add(OC.GT)
        elif op == '>=':
            self.bytecode.add(OC.GE)
        elif op == '==':
            self.bytecode.add(OC.EQ)
        elif op == '!=':
            self.bytecode.add(OC.NE)
        elif op == 'and':
            self.bytecode.add(OC.AND)
        elif op == 'or':
            self.bytecode.add(OC.OR)
        else:
            raise Exception(f"Unsupported binary operator: {op}")

    def visit_UnOp(self, node):
        self.visit(node.expr)
        if node.op == '-':
            self.bytecode.add(OC.NEG)
        else:
            raise Exception(f"Unsupported unary operator: {node.op}")

    def visit_VarDecl(self, node):
        self.visit(node.value)
        self.bytecode.add(OC.STORE, node.name)

    def visit_VarReference(self, node):
        self.bytecode.add(OC.GET, node.name)

    def visit_Assignment(self, node):
        self.visit(node.value)
        self.bytecode.add(OC.STORE, node.name)

    def visit_Print(self, node):
        self.visit(node.expr)
        self.bytecode.add(OC.PRINT)

    def visit_If(self, node):
        # Evaluate condition
        self.visit(node.cond)

        # Add a placeholder JF instruction (we'll update it later)
        jf_idx = self.bytecode.add(OC.JF, None)

        # Generate code for the then branch
        self.visit(node.then)

        # Add a placeholder JMP instruction to skip the else branches (we'll update it later)
        jmp_idx = self.bytecode.add(OC.JMP, None)

        # Update the JF instruction to jump to the first else-if branch or the else branch
        self.bytecode.instructions[jf_idx].operand = len(self.bytecode.instructions)

        # Keep track of all JMP instructions that need to be updated to the end
        jmp_indices = [jmp_idx]

        # Generate code for the else-if branches if they exist
        if hasattr(node, "elseif_branches") and node.elseif_branches:
            for elseif_cond, elseif_body in node.elseif_branches:
                # Evaluate the else-if condition
                self.visit(elseif_cond)

                # Add a placeholder JF instruction (we'll update it later)
                elseif_jf_idx = self.bytecode.add(OC.JF, None)

                # Generate code for the else-if body
                self.visit(elseif_body)

                # Add a placeholder JMP instruction to skip to the end (we'll update it later)
                elseif_jmp_idx = self.bytecode.add(OC.JMP, None)
                jmp_indices.append(elseif_jmp_idx)

                # Update the JF instruction to jump to the next else-if branch or the else branch
                self.bytecode.instructions[elseif_jf_idx].operand = len(self.bytecode.instructions)

        # Generate code for the else branch if it exists
        if hasattr(node, "elsee") and node.elsee is not None:
            self.visit(node.elsee)

        # Update all JMP instructions to jump to the end
        for idx in jmp_indices:
            self.bytecode.instructions[idx].operand = len(self.bytecode.instructions)

    def visit_While(self, node):
        # Create a label for the start of the loop
        start_idx = len(self.bytecode.instructions)

        # Evaluate condition
        self.visit(node.condition)

        # Add a placeholder JF instruction (we'll update it later)
        jf_idx = self.bytecode.add(OC.JF, None)

        # Generate code for the loop body
        self.visit(node.body)

        # Add a JMP instruction to go back to the start
        self.bytecode.add(OC.JMP, start_idx)

        # Update the JF instruction with the correct end index
        self.bytecode.instructions[jf_idx].operand = len(self.bytecode.instructions)

    def visit_For(self, node):
        # Initialize the loop variable
        self.visit(node.init)

        # Create a label for the start of the loop
        start_idx = len(self.bytecode.instructions)

        # Evaluate condition
        self.visit(node.condition)

        # Add a placeholder JF instruction (we'll update it later)
        jf_idx = self.bytecode.add(OC.JF, None)

        # Generate code for the loop body
        self.visit(node.body)

        # Increment the loop variable
        self.visit(node.increment)

        # Add a JMP instruction to go back to the start
        self.bytecode.add(OC.JMP, start_idx)

        # Update the JF instruction with the correct end index
        self.bytecode.instructions[jf_idx].operand = len(self.bytecode.instructions)

    def visit_FunctionDef(self, node):
        # Save the current function
        old_function = self.current_function
        self.current_function = node.name

        # Add a JMP instruction to skip the function body
        jmp_idx = self.bytecode.add(OC.JMP, None)

        # Record the function's start index
        func_idx = len(self.bytecode.instructions)
        self.function_table[node.name] = func_idx
        self.bytecode.function_table[node.name] = func_idx

        # Generate code for the function body
        self.visit(node.body)

        # Add a return instruction if there isn't one already
        if len(self.bytecode.instructions) == 0 or self.bytecode.instructions[-1].opcode != OC.RET:
            self.bytecode.add(OC.PUSH, None)  # Push None as the default return value
            self.bytecode.add(OC.RET)

        # Update the JMP instruction with the correct end index
        self.bytecode.instructions[jmp_idx].operand = len(self.bytecode.instructions)

        # Create a function object and store it in a variable
        self.bytecode.add(OC.MAKE_FUNC, (node.name, node.params, func_idx))
        self.bytecode.add(OC.STORE, node.name)

        # Restore the current function
        self.current_function = old_function

    def visit_FunctionCall(self, node):
        # Push the arguments onto the stack
        for arg in node.args:
            self.visit(arg)

        # Get the function and call it
        self.bytecode.add(OC.GET, node.name)
        self.bytecode.add(OC.CALL, len(node.args))

    def visit_Return(self, node):
        # Evaluate the return value
        self.visit(node.value)

        # Add a return instruction
        self.bytecode.add(OC.RET)

    def visit_ArrayLiteral(self, node):
        # Evaluate all elements first
        elements = []
        for element in node.elements:
            # We need to evaluate each element at compile time
            if isinstance(element, Int):
                elements.append(int(element.val))
            elif isinstance(element, Float):
                elements.append(float(element.val))
            elif isinstance(element, String):
                elements.append(element.val)
            else:
                # For more complex expressions, we'll use the push approach
                return self.visit_ArrayLiteral_dynamic(node)

        # Push the complete array directly
        self.bytecode.add(OC.PUSH, elements)

    def visit_ArrayLiteral_dynamic(self, node):
        # Create an empty array
        self.bytecode.add(OC.PUSH, [])

        # Push each element onto the stack and add it to the array
        for element in node.elements:
            # Duplicate the array reference
            self.bytecode.add(OC.GET, "push")

            # The array is already on the stack from the previous instruction or the initial push

            # Push the element
            self.visit(element)

            # Call push(array, element)
            self.bytecode.add(OC.CALL, 2)

    def visit_ArrayIndex(self, node):
        # Push the array and index onto the stack
        self.visit(node.array)
        self.visit(node.index)

        # Add a custom instruction for array indexing
        self.bytecode.add(OC.ARRAY_INDEX)

    def visit_ArrayAssignment(self, node):
        # Push the array, index, and value onto the stack
        self.visit(node.array)
        self.visit(node.index)
        self.visit(node.value)

        # Add a custom instruction for array assignment
        self.bytecode.add(OC.ARRAY_SET)

# BytecodeVM class
class BytecodeVM:
    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.pc = 0  # Program counter
        self.stack = []  # Operand stack
        self.env = Environment()  # Global environment
        self.call_stack = []  # Call stack for function calls

    def run(self):
        while self.pc < len(self.bytecode.instructions):
            instr = self.bytecode.instructions[self.pc]

            if instr.opcode == OC.PUSH:
                self.stack.append(instr.operand)
                self.pc += 1

            elif instr.opcode == OC.STORE:
                value = self.stack.pop()
                self.env.declare(instr.operand, value)
                self.pc += 1

            elif instr.opcode == OC.GET:
                var_name = instr.operand
                try:
                    value = self.env.lookup(var_name)
                except Exception as e:
                    # If not found, check if it's a built-in function
                    if var_name in ["read_line", "read_int", "read_float"]:
                        value = var_name
                    else:
                        raise e
                self.stack.append(value)
                self.pc += 1

            elif instr.opcode == OC.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                # Handle string concatenation with other types
                if isinstance(a, str) or isinstance(b, str):
                    self.stack.append(str(a) + str(b))
                else:
                    self.stack.append(a + b)
                self.pc += 1

            elif instr.opcode == OC.SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.pc += 1

            elif instr.opcode == OC.MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.pc += 1

            elif instr.opcode == OC.DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)
                self.pc += 1

            elif instr.opcode == OC.MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)
                self.pc += 1

            elif instr.opcode == OC.POW:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a ** b)
                self.pc += 1

            elif instr.opcode == OC.NEG:
                a = self.stack.pop()
                self.stack.append(-a)
                self.pc += 1

            elif instr.opcode == OC.LT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
                self.pc += 1

            elif instr.opcode == OC.LE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)
                self.pc += 1

            elif instr.opcode == OC.GT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
                self.pc += 1

            elif instr.opcode == OC.GE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)
                self.pc += 1

            elif instr.opcode == OC.EQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
                self.pc += 1

            elif instr.opcode == OC.NE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)
                self.pc += 1

            elif instr.opcode == OC.AND:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a and b)
                self.pc += 1

            elif instr.opcode == OC.OR:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a or b)
                self.pc += 1

            elif instr.opcode == OC.PRINT:
                value = self.stack.pop()
                print(value)
                self.pc += 1

            elif instr.opcode == OC.JMP:
                self.pc = instr.operand

            elif instr.opcode == OC.JF:
                condition = self.stack.pop()
                if not condition:
                    self.pc = instr.operand
                else:
                    self.pc += 1

            elif instr.opcode == OC.MAKE_FUNC:
                # The operand is a tuple: (function_name, parameter_list, function_index)
                _, params, func_idx = instr.operand  # Ignore function_name as it's not used here
                # Create a function object with the current environment as closure
                func = UserFunction(params, None, self.env)
                # Store additional information for bytecode execution
                func.func_idx = func_idx
                # Push the function onto the stack
                self.stack.append(func)
                self.pc += 1

            elif instr.opcode == OC.CALL:
                # The operand is the number of arguments
                num_args = instr.operand
                # Pop the function from the stack
                func = self.stack.pop()
                # Get the variable name from the previous GET instruction
                var_name = None
                if self.pc > 0 and self.bytecode.instructions[self.pc-1].opcode == OC.GET:
                    var_name = self.bytecode.instructions[self.pc-1].operand
                # Pop the arguments from the stack
                args = [self.stack.pop() for _ in range(num_args)]
                args.reverse()  # Reverse to maintain order

                # Handle built-in functions
                if isinstance(func, str):
                    # Handle built-in input functions
                    if func == "read_line" or (func == "__builtin__" and var_name == "read_line"):
                        # Execute it immediately
                        user_input = input()
                        self.stack.append(user_input)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "read_int" or (func == "__builtin__" and var_name == "read_int"):
                        try:
                            user_input = int(input())
                            self.stack.append(user_input)
                            self.pc += 1
                            continue  # Continue to the next instruction
                        except ValueError:
                            raise ValueError("Input is not a valid integer")
                    elif func == "read_float" or (func == "__builtin__" and var_name == "read_float"):
                        try:
                            user_input = float(input())
                            self.stack.append(user_input)
                            self.pc += 1
                            continue  # Continue to the next instruction
                        except ValueError:
                            raise ValueError("Input is not a valid float")
                    # Handle array functions
                    elif func == "push" or (func == "__builtin__" and var_name == "push"):
                        if len(args) != 2:
                            raise ValueError("push() requires 2 arguments: array and element")
                        array, element = args
                        if not isinstance(array, list):
                            raise TypeError(f"First argument to push() must be an array, got {type(array)}")
                        array.append(element)
                        self.stack.append(array)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "pop" or (func == "__builtin__" and var_name == "pop"):
                        if len(args) != 1:
                            raise ValueError("pop() requires 1 argument: array")
                        array = args[0]
                        if not isinstance(array, list):
                            raise TypeError(f"Argument to pop() must be an array, got {type(array)}")
                        if not array:
                            raise ValueError("Cannot pop from an empty array")
                        value = array.pop()
                        self.stack.append(value)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "length" or (func == "__builtin__" and var_name == "length"):
                        if len(args) != 1:
                            raise ValueError("length() requires 1 argument: array or string")
                        obj = args[0]
                        if not isinstance(obj, (list, str, Dictionary)):
                            raise TypeError(f"Argument to length() must be an array, string, or dictionary, got {type(obj)}")
                        if isinstance(obj, Dictionary):
                            self.stack.append(obj.size)
                        else:
                            self.stack.append(len(obj))
                        self.pc += 1
                        continue  # Continue to the next instruction

                    # Dictionary operations
                    elif func == "dict" or (func == "__builtin__" and var_name == "dict"):
                        if len(args) != 0:
                            raise ValueError("dict() requires 0 arguments")
                        self.stack.append(Dictionary())
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_put" or (func == "__builtin__" and var_name == "dict_put"):
                        if len(args) != 3:
                            raise ValueError("dict_put() requires 3 arguments: dictionary, key, value")
                        dictionary, key, value = args
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"First argument to dict_put() must be a dictionary, got {type(dictionary)}")
                        dictionary.put(key, value)
                        self.stack.append(dictionary)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_get" or (func == "__builtin__" and var_name == "dict_get"):
                        if len(args) != 2:
                            raise ValueError("dict_get() requires 2 arguments: dictionary, key")
                        dictionary, key = args
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"First argument to dict_get() must be a dictionary, got {type(dictionary)}")
                        self.stack.append(dictionary.get(key))
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_contains" or (func == "__builtin__" and var_name == "dict_contains"):
                        if len(args) != 2:
                            raise ValueError("dict_contains() requires 2 arguments: dictionary, key")
                        dictionary, key = args
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"First argument to dict_contains() must be a dictionary, got {type(dictionary)}")
                        self.stack.append(dictionary.contains(key))
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_remove" or (func == "__builtin__" and var_name == "dict_remove"):
                        if len(args) != 2:
                            raise ValueError("dict_remove() requires 2 arguments: dictionary, key")
                        dictionary, key = args
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"First argument to dict_remove() must be a dictionary, got {type(dictionary)}")
                        dictionary.remove(key)
                        self.stack.append(dictionary)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_clear" or (func == "__builtin__" and var_name == "dict_clear"):
                        if len(args) != 1:
                            raise ValueError("dict_clear() requires 1 argument: dictionary")
                        dictionary = args[0]
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"Argument to dict_clear() must be a dictionary, got {type(dictionary)}")
                        dictionary.clear()
                        self.stack.append(dictionary)
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_keys" or (func == "__builtin__" and var_name == "dict_keys"):
                        if len(args) != 1:
                            raise ValueError("dict_keys() requires 1 argument: dictionary")
                        dictionary = args[0]
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"Argument to dict_keys() must be a dictionary, got {type(dictionary)}")
                        self.stack.append(dictionary.keys())
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_values" or (func == "__builtin__" and var_name == "dict_values"):
                        if len(args) != 1:
                            raise ValueError("dict_values() requires 1 argument: dictionary")
                        dictionary = args[0]
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"Argument to dict_values() must be a dictionary, got {type(dictionary)}")
                        self.stack.append(dictionary.values())
                        self.pc += 1
                        continue  # Continue to the next instruction
                    elif func == "dict_size" or (func == "__builtin__" and var_name == "dict_size"):
                        if len(args) != 1:
                            raise ValueError("dict_size() requires 1 argument: dictionary")
                        dictionary = args[0]
                        if not isinstance(dictionary, Dictionary):
                            raise TypeError(f"Argument to dict_size() must be a dictionary, got {type(dictionary)}")
                        self.stack.append(dictionary.size)
                        self.pc += 1
                        continue  # Continue to the next instruction

                if not isinstance(func, UserFunction):
                    raise ValueError(f"Not a function: {func}")

                # Save the current state for when the function returns
                self.call_stack.append((self.pc + 1, self.env))

                # Create a new environment using the function's closure
                new_env = Environment(func.closure)

                # Declare the parameters in the new environment
                for param, arg in zip(func.params, args):
                    new_env.declare(param, arg)

                # Switch to the new environment
                self.env = new_env

                # Jump to the function's code
                self.pc = func.func_idx

            elif instr.opcode == OC.RET:
                # Pop the return value from the stack
                ret_value = self.stack.pop()

                # If there's no calling function, we're done
                if not self.call_stack:
                    return ret_value

                # Restore the previous state
                self.pc, self.env = self.call_stack.pop()

                # Push the return value onto the stack
                self.stack.append(ret_value)

            elif instr.opcode == OC.HALT:
                # If there's a value on the stack, return it
                if self.stack:
                    return self.stack.pop()
                return None

            elif instr.opcode == OC.READ:
                read_type = instr.operand

                if read_type == "line":
                    self.stack.append(input())
                elif read_type == "int":
                    try:
                        self.stack.append(int(input()))
                    except ValueError:
                        raise ValueError("Input is not a valid integer")
                elif read_type == "float":
                    try:
                        self.stack.append(float(input()))
                    except ValueError:
                        raise ValueError("Input is not a valid float")
                else:
                    raise ValueError(f"Unknown read type: {read_type}")

                self.pc += 1

            elif instr.opcode == OC.ARRAY_INDEX:
                # Pop the index and array from the stack
                index = self.stack.pop()
                array = self.stack.pop()

                # Check if the array is valid
                if not isinstance(array, list):
                    raise TypeError(f"Cannot index non-array: {array}")

                # Check if the index is valid
                if not isinstance(index, int):
                    raise TypeError(f"Array index must be an integer: {index}")

                # Adjust for 1-based indexing (Vasuki uses 1-based indexing)
                if index < 1 or index > len(array):
                    raise IndexError(f"Array index out of range: {index}")

                # Get the element at the index (adjusting for 0-based Python lists)
                self.stack.append(array[index - 1])
                self.pc += 1

            elif instr.opcode == OC.ARRAY_SET:
                # Pop the value, index, and array from the stack
                value = self.stack.pop()
                index = self.stack.pop()
                array = self.stack.pop()

                # Check if the array is valid
                if not isinstance(array, list):
                    raise TypeError(f"Cannot assign to index of non-array: {type(array).__name__}")

                # Check if the index is valid
                if not isinstance(index, int):
                    raise TypeError(f"Array index must be an integer: {index}")

                # Adjust for 1-based indexing (Vasuki uses 1-based indexing)
                if index < 1 or index > len(array):
                    raise IndexError(f"Array index out of range: {index}")

                # Create a new array with the updated element
                new_array = array.copy()
                # Set the element at the index (adjusting for 0-based Python lists)
                new_array[index - 1] = value

                # Push the new array onto the stack
                self.stack.append(new_array)

                # Update the variable if this is a variable reference
                # Look for the variable name in the previous instructions
                var_name = None
                if self.pc >= 3 and self.bytecode.instructions[self.pc-3].opcode == OC.GET:
                    var_name = self.bytecode.instructions[self.pc-3].operand
                    # Update the variable in the environment
                    if var_name:
                        self.env.assign(var_name, new_array)

                self.pc += 1

            else:
                raise ValueError(f"Unknown opcode: {instr.opcode}")

        # If we reach the end of the bytecode without a HALT instruction,
        # return the top of the stack if there is one, otherwise None
        if self.stack:
            return self.stack.pop()
        return None
