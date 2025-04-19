# bytecode_pure.py

from enum import Enum, auto
from top import Environment, UserFunction

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
        
        # Create labels for else and end
        else_idx = len(self.bytecode.instructions) + 2  # Skip the JF instruction and its operand
        
        # Add a placeholder JF instruction (we'll update it later)
        jf_idx = self.bytecode.add(OC.JF, None)
        
        # Generate code for the then branch
        self.visit(node.then)
        
        # Create a label for the end of the if statement
        end_idx = len(self.bytecode.instructions) + 2  # Skip the JMP instruction and its operand
        
        # Add a placeholder JMP instruction (we'll update it later)
        jmp_idx = self.bytecode.add(OC.JMP, None)
        
        # Update the JF instruction with the correct else index
        self.bytecode.instructions[jf_idx].operand = len(self.bytecode.instructions)
        
        # Generate code for the else branch if it exists
        if hasattr(node, "elsee") and node.elsee is not None:
            self.visit(node.elsee)
        
        # Update the JMP instruction with the correct end index
        self.bytecode.instructions[jmp_idx].operand = len(self.bytecode.instructions)
    
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
                value = self.env.lookup(instr.operand)
                self.stack.append(value)
                self.pc += 1
            
            elif instr.opcode == OC.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
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
                func_name, params, func_idx = instr.operand
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
                # Pop the arguments from the stack
                args = [self.stack.pop() for _ in range(num_args)]
                args.reverse()  # Reverse to maintain order
                
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
            
            else:
                raise ValueError(f"Unknown opcode: {instr.opcode}")
        
        # If we reach the end of the bytecode without a HALT instruction,
        # return the top of the stack if there is one, otherwise None
        if self.stack:
            return self.stack.pop()
        return None
