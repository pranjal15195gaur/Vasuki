# bytecode.py

# A simple instruction and bytecode container
class Instruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        if self.operand is not None:
            return f"{self.opcode} {self.operand}"
        return f"{self.opcode}"


class Bytecode:
    def __init__(self):
        self.instructions = []

    def emit(self, opcode, operand=None):
        instr = Instruction(opcode, operand)
        self.instructions.append(instr)

    def __repr__(self):
        return "\n".join(str(instr) for instr in self.instructions)


# BytecodeGenerator traverses the AST and emits bytecode

class BytecodeGenerator:
    def __init__(self):
        self.bytecode = Bytecode()
        self.label_count = 0

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        self.visit(node)
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

    # Updated for Int: use node.val instead of node.value
    def visit_Int(self, node):
        self.bytecode.emit("LOAD_CONST", int(node.val))

    # Similarly, if you have a Float node, adjust accordingly:
    def visit_Float(self, node):
        self.bytecode.emit("LOAD_CONST", float(node.val))

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op
        if op == '+':
            self.bytecode.emit("ADD")
        elif op == '-':
            self.bytecode.emit("SUB")
        elif op == '*':
            self.bytecode.emit("MUL")
        elif op == '/':
            self.bytecode.emit("DIV")
        elif op == '%':
            self.bytecode.emit("MOD")
        elif op == '**':
            self.bytecode.emit("POW")
        elif op == '<':
            self.bytecode.emit("LT")
        elif op == '<=':
            self.bytecode.emit("LE")
        elif op == '>':
            self.bytecode.emit("GT")
        elif op == '>=':
            self.bytecode.emit("GE")
        elif op == '==':
            self.bytecode.emit("EQ")
        elif op == '!=':
            self.bytecode.emit("NE")
        elif op in ("and", "or"):
            self.bytecode.emit(op.upper())
        else:
            raise Exception(f"Unsupported binary operator: {op}")

    def visit_UnOp(self, node):
        self.visit(node.expr)
        if node.op == '-':
            self.bytecode.emit("NEG")
        else:
            raise Exception(f"Unsupported unary operator: {node.op}")

    # Updated for VarDecl: use node.value instead of node.expr
    def visit_VarDecl(self, node):
        self.visit(node.value)
        self.bytecode.emit("STORE_VAR", node.name)

    def visit_VarReference(self, node):
        self.bytecode.emit("LOAD_VAR", node.name)

    def visit_Assignment(self, node):
        self.visit(node.expr)
        self.bytecode.emit("STORE_VAR", node.name)

    def visit_Print(self, node):
        self.visit(node.expr)
        self.bytecode.emit("PRINT")

    # If: generate branch instructions
    def visit_If(self, node):
        # Evaluate the condition.
        self.visit(node.cond)
        else_label = self.new_label()
        end_label = self.new_label()
        # If condition is false, jump to else label.
        self.bytecode.emit("JUMP_IF_FALSE", else_label)
        # Then branch: note we're now using node.then.
        self.visit(node.then)
        # Jump past the else branch.
        self.bytecode.emit("JUMP", end_label)
        # Else branch label.
        self.bytecode.emit("LABEL", else_label)
        # If an else branch exists, visit it. In your AST it's stored in node.elsee.
        if hasattr(node, "elsee") and node.elsee is not None:
            self.visit(node.elsee)
        # End label.
        self.bytecode.emit("LABEL", end_label)



    # While loops: similar to if, but with a loop back
    def visit_While(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        self.bytecode.emit("LABEL", start_label)
        self.visit(node.condition)
        self.bytecode.emit("JUMP_IF_FALSE", end_label)
        self.visit(node.body)
        self.bytecode.emit("JUMP", start_label)
        self.bytecode.emit("LABEL", end_label)

    # For loop: assume it contains initializer, condition, increment, and body
    def visit_For(self, node):
        self.visit(node.init)  # initializer
        start_label = self.new_label()
        end_label = self.new_label()
        self.bytecode.emit("LABEL", start_label)
        self.visit(node.condition)
        self.bytecode.emit("JUMP_IF_FALSE", end_label)
        self.visit(node.body)
        self.visit(node.increment)
        self.bytecode.emit("JUMP", start_label)
        self.bytecode.emit("LABEL", end_label)

    # Array literal: evaluate elements and build an array
    def visit_ArrayLiteral(self, node):
        for element in node.elements:
            self.visit(element)
        # Emit a BUILD_ARRAY instruction with the number of elements
        self.bytecode.emit("BUILD_ARRAY", len(node.elements))

    # Array indexing: first evaluate the array, then the index, then load the element
    def visit_ArrayIndex(self, node):
        self.visit(node.array)
        self.visit(node.index)
        self.bytecode.emit("LOAD_INDEX")

    # Function call: evaluate arguments then emit a call instruction.
    def visit_FunctionCall(self, node):
        for arg in node.args:
            self.visit(arg)
        # The CALL instruction contains the function name and number of arguments
        self.bytecode.emit("CALL", (node.name, len(node.args)))

    # Function definition: label the function entry point and generate its body

    def visit_FunctionDef(self, node):
        func_label = f"func_{node.name}"
        # Emit a label for the function entry point.
        self.bytecode.emit("LABEL", func_label)
        # Emit instructions to store each parameter.
        # Note: If your CALL opcode pushes arguments in order,
        # you may need to reverse the parameters so that the first parameter
        # ends up in the correct variable.
        for param in reversed(node.params):
            self.bytecode.emit("STORE_VAR", param)
        # Generate bytecode for the function body.
        self.visit(node.body)
        self.bytecode.emit("RETURN")

    def visit_FunctionDef(self, node):
        func_label = f"func_{node.name}"
        # Emit a label for the function entry point
        self.bytecode.emit("LABEL", func_label)
        # Function parameters and environment handling would be implemented in your VM.
        self.visit(node.body)
        self.bytecode.emit("RETURN")

    # Return: evaluate the return expression then return
    def visit_Return(self, node):
        self.visit(node.value)
        self.bytecode.emit("RETURN")


    # Labels: allow marking positions in code
    def visit_Label(self, node):
        self.bytecode.emit("LABEL", node.name)

    # LabelReturn: jump to a previously declared label
    def visit_LabelReturn(self, node):
        self.bytecode.emit("JUMP", node.name)

    # GoAndReturn: jump to a label and then perform a return
    def visit_GoAndReturn(self, node):
        self.bytecode.emit("JUMP", node.label)
        self.bytecode.emit("RETURN")

