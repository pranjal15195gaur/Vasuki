from compiler.top import Int, BinOp, Program

# Opcodes (must match vm.py definitions)
OP_ADD  = 0  # add

def compile_expr(ast, target_reg=0):
    """
    Compile an expression into a list of VM instructions that leave the result in target_reg.
    For demo purposes, only these cases are supported:
      - Int: compiles as ADD target, R0 (assumed 0) with immediate value.
      - BinOp with '+' operator: compile left and right into registers and add.
    """
    code = []
    if isinstance(ast, Int):
        # Use: ADD target, R0, immediate <value>
        # Format: [opcode(4)|dest(3)|src1(3)|imm_flag(1)|imm(5)]
        imm = int(ast.val)
        instr = (OP_ADD << 12) | (target_reg << 9) | (0 << 6) | (1 << 5) | (imm & 0x1F)
        code.append(instr)
    elif isinstance(ast, BinOp) and ast.op == '+':
        # Compile left into R1 and right into R2, then add R1 and R2 into target.
        left_code = compile_expr(ast.left, target_reg=1)
        right_code = compile_expr(ast.right, target_reg=2)
        # Use: ADD R(target)= R1 + R2.
        instr = (OP_ADD << 12) | (target_reg << 9) | (1 << 6) | (0 << 5) | (2 & 0x7)
        code.extend(left_code)
        code.extend(right_code)
        code.append(instr)
    else:
        raise ValueError("Unsupported AST node in codegen")
    return code

def compile_program(ast):
    """
    Compile a Program AST node.
    For simplicity, compile the last statement as the program result.
    """
    if isinstance(ast, Program):
        code = []
        for stmt in ast.statements:
            code = compile_expr(stmt)
        return code
    else:
        return compile_expr(ast)
