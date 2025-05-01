"""
Bytecode generation and representation for the Vasuki programming language.

This module defines the core classes for representing bytecode instructions
and generating bytecode from the abstract syntax tree (AST). It provides
the foundation for the Vasuki virtual machine execution model.
"""

class Instruction:
    """Represents a single bytecode instruction.

    An instruction consists of an opcode and an optional operand.
    The opcode determines the operation to perform, while the operand
    provides additional data needed for the operation.
    """
    def __init__(self, opcode, operand=None):
        """Initialize a new instruction.

        Args:
            opcode: The operation code as a string
            operand: Optional data for the operation
        """
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        """Return a string representation of the instruction."""
        if self.operand is not None:
            return f"{self.opcode} {self.operand}"
        return f"{self.opcode}"


class Bytecode:
    """Container for a sequence of bytecode instructions.

    This class provides methods to add instructions and convert the
    entire sequence to a string representation.
    """
    def __init__(self):
        """Initialize an empty bytecode sequence."""
        self.instructions = []

    def emit(self, opcode, operand=None):
        """Add a new instruction to the bytecode sequence.

        Args:
            opcode: The operation code as a string
            operand: Optional data for the operation
        """
        instr = Instruction(opcode, operand)
        self.instructions.append(instr)

    def __repr__(self):
        """Return a string representation of the bytecode sequence."""
        return "\n".join(str(instr) for instr in self.instructions)

class BytecodeGenerator:
    """Traverses the AST and generates bytecode instructions.

    This class implements the visitor pattern to walk through the abstract
    syntax tree (AST) and emit appropriate bytecode instructions for each
    node type. It handles expressions, statements, control flow, and other
    language constructs.
    """
    def __init__(self):
        """Initialize a new bytecode generator."""
        self.bytecode = Bytecode()
        self.label_count = 0

    def new_label(self):
        """Generate a unique label for control flow instructions.

        Returns:
            A string representing a unique label (e.g., "L1", "L2", etc.)
        """
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        """Generate bytecode for an AST node and its children.

        Args:
            node: The root AST node to generate bytecode for

        Returns:
            The complete Bytecode object
        """
        self.visit(node)
        return self.bytecode

    def visit(self, node):
        """Visit an AST node and dispatch to the appropriate visit method.

        Args:
            node: The AST node to visit

        Returns:
            The result of the specific visit method
        """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Default handler for node types without a specific visit method.

        Args:
            node: The AST node that has no specific visit method

        Raises:
            Exception: Always raises an exception indicating the missing visit method
        """
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_Program(self, node):
        """Generate bytecode for a program node (sequence of statements).

        Args:
            node: The Program AST node
        """
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Int(self, node):
        """Generate bytecode for an integer literal.

        Args:
            node: The Int AST node
        """
        self.bytecode.emit("LOAD_CONST", int(node.val))

    def visit_Float(self, node):
        """Generate bytecode for a floating-point literal.

        Args:
            node: The Float AST node
        """
        self.bytecode.emit("LOAD_CONST", float(node.val))

    def visit_BinOp(self, node):
        """Generate bytecode for a binary operation.

        Evaluates the left and right operands, then applies the operation.

        Args:
            node: The BinOp AST node

        Raises:
            Exception: If the operator is not supported
        """
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
        """Generate bytecode for a unary operation.

        Args:
            node: The UnOp AST node

        Raises:
            Exception: If the operator is not supported
        """
        self.visit(node.expr)
        if node.op == '-':
            self.bytecode.emit("NEG")
        else:
            raise Exception(f"Unsupported unary operator: {node.op}")

    def visit_VarDecl(self, node):
        """Generate bytecode for a variable declaration.

        Args:
            node: The VarDecl AST node
        """
        self.visit(node.value)
        self.bytecode.emit("STORE_VAR", node.name)

    def visit_VarReference(self, node):
        """Generate bytecode for a variable reference.

        Args:
            node: The VarReference AST node
        """
        self.bytecode.emit("LOAD_VAR", node.name)

    def visit_Assignment(self, node):
        """Generate bytecode for a variable assignment.

        Args:
            node: The Assignment AST node
        """
        self.visit(node.expr)
        self.bytecode.emit("STORE_VAR", node.name)

    def visit_Print(self, node):
        """Generate bytecode for a print statement.

        Args:
            node: The Print AST node
        """
        self.visit(node.expr)
        self.bytecode.emit("PRINT")

    def visit_If(self, node):
        """Generate bytecode for an if statement.

        Evaluates the condition and generates appropriate jumps for the
        then and else branches.

        Args:
            node: The If AST node
        """
        self.visit(node.cond)
        else_label = self.new_label()
        end_label = self.new_label()

        # If condition is false, jump to else label
        self.bytecode.emit("JUMP_IF_FALSE", else_label)

        # Then branch
        self.visit(node.then)

        # Jump past the else branch
        self.bytecode.emit("JUMP", end_label)

        # Else branch label
        self.bytecode.emit("LABEL", else_label)

        # If an else branch exists, visit it
        if hasattr(node, "elsee") and node.elsee is not None:
            self.visit(node.elsee)

        # End label
        self.bytecode.emit("LABEL", end_label)

    def visit_While(self, node):
        """Generate bytecode for a while loop.

        Creates a loop structure with condition checking and appropriate jumps.

        Args:
            node: The While AST node
        """
        start_label = self.new_label()
        end_label = self.new_label()

        self.bytecode.emit("LABEL", start_label)
        self.visit(node.condition)
        self.bytecode.emit("JUMP_IF_FALSE", end_label)
        self.visit(node.body)
        self.bytecode.emit("JUMP", start_label)
        self.bytecode.emit("LABEL", end_label)

    def visit_For(self, node):
        """Generate bytecode for a for loop.

        Handles initialization, condition checking, body execution, and increment.

        Args:
            node: The For AST node
        """
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

    def visit_ArrayLiteral(self, node):
        """Generate bytecode for an array literal.

        Evaluates each element and builds an array.

        Args:
            node: The ArrayLiteral AST node
        """
        for element in node.elements:
            self.visit(element)
        self.bytecode.emit("BUILD_ARRAY", len(node.elements))

    def visit_ArrayIndex(self, node):
        """Generate bytecode for array indexing.

        Evaluates the array and index expressions, then loads the element.

        Args:
            node: The ArrayIndex AST node
        """
        self.visit(node.array)
        self.visit(node.index)
        self.bytecode.emit("LOAD_INDEX")

    def visit_FunctionCall(self, node):
        """Generate bytecode for a function call.

        Evaluates arguments and emits a call instruction.

        Args:
            node: The FunctionCall AST node
        """
        for arg in node.args:
            self.visit(arg)
        self.bytecode.emit("CALL", (node.name, len(node.args)))

    def visit_FunctionDef(self, node):
        """Generate bytecode for a function definition.

        Creates a function object, stores it, and generates code for the body.

        Args:
            node: The FunctionDef AST node
        """
        # Create a function object and store it in a variable
        self.bytecode.emit("MAKE_FUNCTION", (node.name, node.params))
        self.bytecode.emit("STORE_VAR", node.name)

        # Emit the function body code with a label
        func_label = f"func_{node.name}"
        self.bytecode.emit("LABEL", func_label)

        # Store parameters in reverse order (they'll be popped from the stack in reverse)
        for param in reversed(node.params):
            self.bytecode.emit("STORE_VAR", param)

        # Generate bytecode for the function body
        self.visit(node.body)

        # Add implicit return None if no explicit return is present
        if not (len(self.bytecode.instructions) > 0 and
                self.bytecode.instructions[-1].opcode == "RETURN"):
            self.bytecode.emit("LOAD_CONST", None)
            self.bytecode.emit("RETURN")

    def visit_Return(self, node):
        """Generate bytecode for a return statement.

        Evaluates the return value and emits a return instruction.

        Args:
            node: The Return AST node
        """
        self.visit(node.value)
        self.bytecode.emit("RETURN")

    def visit_Label(self, node):
        """Generate bytecode for a label declaration.

        Args:
            node: The Label AST node
        """
        self.bytecode.emit("LABEL", node.name)

    def visit_LabelReturn(self, node):
        """Generate bytecode for a label return statement.

        Args:
            node: The LabelReturn AST node
        """
        self.bytecode.emit("JUMP", node.name)

    def visit_GoAndReturn(self, node):
        """Generate bytecode for a go-and-return statement.

        Jumps to a label and then returns.

        Args:
            node: The GoAndReturn AST node
        """
        self.bytecode.emit("JUMP", node.label)
        self.bytecode.emit("RETURN")

