import pytest
from parser import parse, ParseError
from top import (
    BinOp, UnOp, Float, Int, If, Program, VarDecl,
    VarReference, Assignment, For, While, Print, 
    ArrayLiteral, ArrayIndex, FunctionCall, FunctionDef, Return,  
    Label, LabelReturn, GoAndReturn
)

# Helper function to reparse and simplify AST comparisons for simple expressions.
def parse_ast(s):
    ast = parse(s)
    # Wrap non-program ASTs in a Program for uniformity.
    return ast if isinstance(ast, Program) else Program([ast])

### --- Basic Expressions ---

def test_parse_int_and_float():
    ast = parse_ast("123; 3.14;")
    # We expect a Program with two statements: one Int and one Float node.
    stmts = ast.statements
    assert isinstance(stmts[0], Int)
    assert stmts[0].val == "123"
    assert isinstance(stmts[1], Float)
    assert stmts[1].val == "3.14"

def test_parse_unary_minus():
    ast = parse_ast("-123;")
    # Expect an UnOp wrapping an Int
    stmt = ast.statements[0]
    assert isinstance(stmt, UnOp)
    assert stmt.op == '-'
    assert isinstance(stmt.num, Int)
    assert stmt.num.val == "123"

def test_parse_binop():
    ast = parse_ast("1 + 2;")
    stmt = ast.statements[0]
    assert isinstance(stmt, BinOp)
    # Check left and right operands.
    assert isinstance(stmt.left, Int)
    assert stmt.left.val == "1"
    assert isinstance(stmt.right, Int)
    assert stmt.right.val == "2"
    assert stmt.op == "+"

def test_parse_parentheses():
    ast = parse_ast("(1 + 2);")
    # Parentheses should not change the computed AST; check the inner expression.
    # Here we assume the parser removes the Parentheses node when building the AST.
    # (If it leaves a Parentheses node, adjust your test accordingly.)
    stmt = ast.statements[0]
    # It might either be a Parentheses node or directly the inner BinOp.
    if hasattr(stmt, "val"):
        inner = stmt.val
    else:
        inner = stmt
    assert isinstance(inner, BinOp)
    assert inner.op == "+"

def test_parse_array_literal_and_index():
    ast = parse_ast("[1, 2, 3];")
    stmt = ast.statements[0]
    assert isinstance(stmt, ArrayLiteral)
    # Check that elements are Int nodes.
    for i, el in enumerate(stmt.elements, start=1):
        assert isinstance(el, Int)
        assert el.val == str(i)
    
    # Test array indexing: e.g., [1,2,3][2] should yield an ArrayIndex node.
    ast_index = parse_ast("[1,2,3][2];")
    stmt_index = ast_index.statements[0]
    assert isinstance(stmt_index, ArrayIndex)
    # The index expression should evaluate to an Int.
    assert isinstance(stmt_index.index, Int)
    assert stmt_index.index.val == "2"

### --- Function Calls and Definitions ---

def test_parse_function_call():
    # Test function call with arguments.
    ast = parse_ast("foo(1, 2);")
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionCall)
    assert stmt.name == "foo"
    assert len(stmt.args) == 2
    for arg in stmt.args:
        assert isinstance(arg, Int)

def test_parse_function_def():
    # A simple function definition with one parameter.
    code = "def add(a){ a + 1; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionDef)
    assert stmt.name == "add"
    assert stmt.params == ["a"]
    # Body should be parsed as a statement (e.g., BinOp or Assignment)
    # In this example, it's a BinOp.
    assert hasattr(stmt, "body")

def test_parse_return_statement():
    # Test that a return statement inside a function is parsed.
    ast = parse_ast("return 123;")
    stmt = ast.statements[0]
    assert isinstance(stmt, Return)

### --- Control Flow ---

def test_parse_if_statement_without_else():
    code = "if 1 { 2; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, If)
    # else branch is None when not provided.
    assert stmt.elsee is None

def test_parse_if_statement_with_else_if_and_else():
    code = "if 0 { 1; } else if 2 { 3; } else { 4; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, If)
    # There should be one elseif branch.
    assert len(stmt.elseif_branches) == 1
    # And an else branch.
    assert stmt.elsee is not None

def test_parse_for_loop():
    # For-loop with initializer, condition, and increment.
    code = "for( var i = 1; i < 3; i = i + 1 ){ print(i); };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "For"

def test_parse_while_loop():
    code = "while(1){ print(1); };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, While)

def test_parse_print_statement():
    code = "print(123);"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, Print)

### --- Variable Declarations and Assignments ---

def test_parse_variable_declaration_and_assignment():
    code = "var x = 10; x = x + 1;"
    ast = parse_ast(code)
    # Expect two statements: a variable declaration and an assignment.
    assert len(ast.statements) == 2
    decl, assign = ast.statements
    assert isinstance(decl, VarDecl)
    assert decl.name == "x"
    assert isinstance(assign, Assignment)
    assert assign.name == "x"



### --- Error Cases ---

def test_unclosed_parenthesis_in_function_call():
    code = "foo(1, 2;"
    with pytest.raises(ParseError, match="Unclosed parenthesis in function call"):
        parse(code)

def test_missing_semicolon_between_statements():
    # Two statements without semicolon in between should raise an error.
    code = "123 456;"
    with pytest.raises(ParseError, match="Missing semicolon between statements"):
        parse(code)

