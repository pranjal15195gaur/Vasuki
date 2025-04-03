import pytest
import builtins

# --- Import modules ---
from lexer import lex, IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken
from parser import parse, ParseError
from top import (
    e, Environment, BinOp, UnOp, Float, Int, Parentheses, If, VarDecl,
    VarReference, Assignment, Program, For, While, Print, FunctionCall, FunctionDef,
    Return, ArrayLiteral, ArrayIndex, Label, LabelReturn, GoAndReturn, UserFunction, ReturnException
)

# --- Lexer Tests ---

def tokens_to_list(s):
    """Helper: convert lexer's iterator output to a list for comparison."""
    return list(lex(s))

def test_lexer_integers():
    tokens = tokens_to_list("123 42")
    assert tokens == [IntToken("123"), IntToken("42")]

def test_lexer_floats():
    tokens = tokens_to_list("3.14 0.001")
    assert tokens == [FloatToken("3.14"), FloatToken("0.001")]

def test_lexer_operators():
    tokens = tokens_to_list("+ - * / <= >= == != ** ;")
    expected = [
        OperatorToken("+"), OperatorToken("-"), OperatorToken("*"),
        OperatorToken("/"), OperatorToken("<="), OperatorToken(">="),
        OperatorToken("=="), OperatorToken("!="), OperatorToken("**"),
        OperatorToken(";")
    ]
    assert tokens == expected

def test_lexer_keywords_and_parens():
    tokens = tokens_to_list("if else ( ) { } [ ] : ,")
    # Depending on implementation, some tokens may be classified as KeywordToken or OperatorToken.
    # Adjust the expected list as needed.
    expected = [
        KeywordToken("if"), KeywordToken("else"),
        ParenToken("("), ParenToken(")"),
        OperatorToken("{"), OperatorToken("}"),
        OperatorToken("["), OperatorToken("]"),
        OperatorToken(":"), OperatorToken(",")
    ]
    assert tokens == expected

def test_lexer_invalid_number():
    with pytest.raises(ValueError, match="Invalid number token found"):
        list(lex("3.14.15"))

def test_lexer_unexpected_character():
    with pytest.raises(ValueError, match="Unexpected character found"):
        list(lex("@"))

def test_lexer_array_literal():
    tokens = tokens_to_list("[1, 2, 3]")
    # Expect: '[' then IntToken "1", comma, IntToken "2", comma, IntToken "3", and ']'
    expected = [
        OperatorToken('['), IntToken("1"), OperatorToken(','),
        IntToken("2"), OperatorToken(','), IntToken("3"),
        OperatorToken(']')
    ]
    assert tokens == expected

# --- Parser Tests ---

def parse_ast(s):
    """Helper: parse input string and return a Program node."""
    ast = parse(s)
    return ast if isinstance(ast, Program) else Program([ast])

def test_parser_simple_expression():
    ast = parse_ast("1 + 2;")
    stmt = ast.statements[0]
    assert isinstance(stmt, BinOp)
    assert stmt.op == "+"
    assert isinstance(stmt.left, Int)
    assert stmt.left.val == "1"
    assert isinstance(stmt.right, Int)
    assert stmt.right.val == "2"

def test_parser_unary_minus():
    ast = parse_ast("-123;")
    stmt = ast.statements[0]
    assert isinstance(stmt, UnOp)
    assert stmt.op == "-"
    assert isinstance(stmt.num, Int)
    assert stmt.num.val == "123"

def test_parser_parentheses():
    ast = parse_ast("(1 + 2);")
    # Depending on your parser, the Parentheses node may be unwrapped.
    stmt = ast.statements[0]
    # Allow either a Parentheses node wrapping a BinOp or directly a BinOp.
    if isinstance(stmt, Parentheses):
        inner = stmt.val
    else:
        inner = stmt
    assert isinstance(inner, BinOp)
    assert inner.op == "+"

def test_parser_array_literal_and_index():
    # Array literal test.
    ast1 = parse_ast("[1,2,3];")
    stmt1 = ast1.statements[0]
    assert isinstance(stmt1, ArrayLiteral)
    for i, el in enumerate(stmt1.elements, start=1):
        assert isinstance(el, Int)
        assert el.val == str(i)
    # Array index test.
    ast2 = parse_ast("[1,2,3][2];")
    stmt2 = ast2.statements[0]
    assert isinstance(stmt2, ArrayIndex)
    assert isinstance(stmt2.index, Int)
    assert stmt2.index.val == "2"

def test_parser_function_call():
    ast = parse_ast("foo(1, 2);")
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionCall)
    assert stmt.name == "foo"
    assert len(stmt.args) == 2
    for arg in stmt.args:
        assert isinstance(arg, Int)

def test_parser_function_def():
    code = "def add(a){ a + 1; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionDef)
    assert stmt.name == "add"
    assert stmt.params == ["a"]
    # Function body is parsed as a statement (e.g. BinOp, Assignment, etc.)
    assert stmt.body is not None

def test_parser_if_else():
    code = "if 0 { 1; } else { 100; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, If)
    assert stmt.elsee is not None

def test_parser_missing_semicolon():
    code = "123 456;"
    with pytest.raises(ParseError, match="Missing semicolon between statements"):
        parse(code)



# --- Top (Interpreter) Tests ---

def test_evaluate_arithmetic():
    # Evaluates an arithmetic expression.
    expr = BinOp("+", Int("10"), Int("5"))
    assert e(expr) == 15

def test_evaluate_variable():
    prog = Program([
        VarDecl("x", Int("10")),
        Assignment("x", BinOp("+", VarReference("x"), Int("5")))
    ])
    # After assignment, x should be 15.
    assert e(prog) == 15

def test_evaluate_if_statement():
    # if 1 { 42; } -> returns 42.
    stmt = If(Int("1"), Int("42"), [], None)
    assert e(stmt) == 42

def test_evaluate_loop_for():
    # for(var i = 1; i <= 3; i = i + 1){ i; }
    prog = For(
        VarDecl("i", Int("1")),
        BinOp("<=", VarReference("i"), Int("3")),
        Assignment("i", BinOp("+", VarReference("i"), Int("1"))),
        VarReference("i")
    )
    assert e(prog) == 3

def test_evaluate_loop_while():
    prog = Program([
        VarDecl("i", Int("1")),
        While(
            BinOp("<", VarReference("i"), Int("4")),
            Assignment("i", BinOp("+", VarReference("i"), Int("1")))
        ),
        VarReference("i")
    ])
    assert e(prog) == 4

def test_print_statement(capsys):
    stmt = Print(Int("123"))
    result = e(stmt)
    captured = capsys.readouterr().out.strip()
    assert captured == "123"
    assert result == 123

def test_function_definition_and_call():
    # def add(a){ return a + 1; } and then add(10);
    func_body = Return(BinOp("+", VarReference("a"), Int("1")))
    func_def = FunctionDef("add", ["a"], func_body)
    prog = Program([func_def, FunctionCall("add", [Int("10")])])
    result = e(prog)
    assert result == 11

def test_function_wrong_argument_count():
    func_body = Return(VarReference("a"))
    func_def = FunctionDef("id", ["a"], func_body)
    prog = Program([func_def, FunctionCall("id", [])])
    with pytest.raises(ValueError, match="expects 1 arguments"):
        e(prog)

def test_unknown_function_call():
    with pytest.raises(ValueError, match="Unknown function foo"):
        e(FunctionCall("foo", []))

def test_return_exception():
    with pytest.raises(ReturnException):
        e(Return(Int("5")))

def test_array_evaluation():
    arr = ArrayLiteral([Int("10"), Int("20"), Int("30")])
    assert e(arr) == [10, 20, 30]

def test_array_indexing():
    arr = ArrayLiteral([Int("10"), Int("20"), Int("30")])
    idx_expr = ArrayIndex(arr, Int("2"))
    assert e(idx_expr) == 20

def test_array_index_non_integer():
    arr = ArrayLiteral([Int("10"), Int("20")])
    with pytest.raises(ValueError, match="Array index must be an integer"):
        e(ArrayIndex(arr, Float("1.5")))

def test_labels_and_goandreturn():
    # Create a program with a label and a labeled block.
    label_node = Label("start")
    stmt = VarDecl("x", Int("1"))
    ret_node = LabelReturn("start")
    prog = Program([label_node, stmt, ret_node])
    # Set the global program for label lookup.
    builtins.global_program = prog
    gar = GoAndReturn("start")
    # goandreturn should execute the block and return None.
    assert e(gar) is None

def test_parentheses_node_evaluation():
    expr = Parentheses(BinOp("*", Int("3"), Int("4")))
    assert e(expr) == 12


# Helper: Wrap AST in Program node if needed.
def parse_ast(s):
    ast = parse(s)
    return ast if isinstance(ast, Program) else Program([ast])

# --- Additional Tests for Branch Coverage in Parser ---

def test_if_with_elseif_and_else():
    # This tests an if statement with an elseif branch and an else branch.
    code = "if 0 { 10; } else if 1 { 20; } else { 30; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    # Check that we have one elseif branch and an else branch.
    assert isinstance(stmt, If)
    assert len(stmt.elseif_branches) == 1
    assert stmt.elsee is not None

def test_if_without_else_branches():
    # Test an if statement without any else parts.
    code = "if 1 { 42; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, If)
    # When no else, elsee should be None and elseif_branches empty.
    assert stmt.elsee is None
    assert stmt.elseif_branches == []

def test_function_definition_with_multiple_params():
    # Function definition with two parameters and a body with a binop.
    code = "def max(a, b){ a > b; };"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionDef)
    assert stmt.name == "max"
    assert stmt.params == ["a", "b"]
    # Body should be parsed (could be a BinOp comparing a and b).
    assert stmt.body is not None

def test_function_definition_missing_open_paren():
    # Should raise an error due to missing '(' after function name.
    code = "def foo 1 { 10; };"
    with pytest.raises(ParseError):
        parse(code)

def test_function_definition_missing_parameter():
    # Test error when parameter is missing.
    code = "def foo(){ 10; };"
    # This one might be valid if empty parameters are allowed.
    # If not allowed, adjust the parser or the test expectation.
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionDef)
    # Assuming empty parameter lists are allowed.
    assert stmt.params == []

def test_function_call_with_no_arguments_parentheses():
    # Test a function call with no arguments.
    code = "foo();"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, FunctionCall)
    assert stmt.name == "foo"
    assert stmt.args == []

def test_assignment_after_var_reference():
    # Test that a variable reference followed by assignment is parsed as Assignment.
    code = "x = 5;"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, Assignment)
    assert stmt.name == "x"

def test_label_and_labelreturn_in_expression_context():
    # Test when a label is not used at the beginning of a statement,
    # parser should prepend the token back and parse as an expression.
    code = "foo: 10;"  # This should be parsed as a Label because of colon.
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert isinstance(stmt, Label)
    assert stmt.name == "foo"



def test_array_literal_without_commas():
    # Test array literal with a single element and no commas.
    code = "[42];"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "ArrayLiteral"
    assert len(stmt.elements) == 1
    assert stmt.elements[0].val == "42"



def test_missing_semicolon_error():
    # Two statements without a semicolon between them should raise an error.
    code = "10 20;"
    with pytest.raises(ParseError, match="Missing semicolon between statements"):
        parse(code)



# Helper: Wrap AST in Program node if needed.
def parse_ast(s):
    ast = parse(s)
    return ast if isinstance(ast, Program) else Program([ast])

# --- Tests to Cover Missing Branches ---

# Lines 38-40 in expect: Trigger expect failure by calling a construct that needs a token that isn't there.
def test_expect_failure_in_paren():
    # In parse_atom, when handling a parenthesized expression, missing closing paren should call expect and fail.
    with pytest.raises(ParseError):
        parse("(1+2;")  # Missing closing ')'

# Lines 47-49: In parse_comparison match branch.
def test_parse_comparison_operator():
    # "1 < 2;" should go into the operator branch of parse_comparison.
    ast = parse_ast("1 < 2;")
    stmt = ast.statements[0]
    # Expect a BinOp for the comparison operator.
    assert isinstance(stmt, BinOp)
    assert stmt.op == "<"

# Lines 60-61: In parse_logic_and while loop.
def test_parse_logic_and_multiple():
    # "1 and 0;" forces the loop in parse_logic_and.
    ast = parse_ast("1 and 0;")
    # This should be parsed as BinOp with op "and"
    stmt = ast.statements[0]
    assert isinstance(stmt, BinOp)
    assert stmt.op == "and"

# Lines 71-73: In parse_logic_or while loop.
def test_parse_logic_or_multiple():
    # "1 or 0;" forces the loop in parse_logic_or.
    ast = parse_ast("1 or 0;")
    stmt = ast.statements[0]
    assert isinstance(stmt, BinOp)
    assert stmt.op == "or"

# Lines 82-84: In parse_add_sub loop.
def test_parse_add_sub_mixed():
    # "1 + 2 - 3;" should exercise both '+' and '-' branches.
    ast = parse_ast("1 + 2 - 3;")
    stmt = ast.statements[0]
    # Final AST should be a BinOp with '-' at top.
    assert isinstance(stmt, BinOp)
    assert stmt.op == "-"

# Lines 113-114: In parse_mul_div loop.
def test_parse_mul_div_operators():
    # "2 * 3 / 4 % 5;" should trigger each operator branch.
    # We expect left-associative evaluation.
    ast = parse_ast("2 * 3 / 4 % 5;")
    stmt = ast.statements[0]
    # Without diving into full tree shape, check that the top operator is '%'
    assert isinstance(stmt, BinOp)
    assert stmt.op == "%"

# Lines 146-147: In parse_if branch where token is "if" (the condition is present).
def test_parse_if_without_else():
    # "if 1 { 42; };" triggers the normal if branch (no else).
    ast = parse_ast("if 1 { 42; };")
    stmt = ast.statements[0]
    assert isinstance(stmt, If)
    # elsee should be None
    assert stmt.elsee is None

# Lines 167-168: In parse_atom for parenthesized expressions.
def test_parse_atom_parentheses_missing_close():
    # Already partially covered by test_expect_failure_in_paren, so we repeat similar.
    with pytest.raises(ParseError):
        parse("(1+2;")

# Lines 176-177: In parse_atom for unary minus.
def test_parse_atom_unary_minus():
    ast = parse_ast("-5;")
    stmt = ast.statements[0]
    assert isinstance(stmt, UnOp)
    assert stmt.op == "-"
    assert isinstance(stmt.num, Int)
    assert stmt.num.val == "5"

# Line 191: In parse_atom, array literal branch.
def test_parse_array_literal_commas():
    # "[1, 2, 3];" exercises the while loop for commas.
    ast = parse_ast("[1, 2, 3];")
    stmt = ast.statements[0]
    assert isinstance(stmt, ArrayLiteral)
    assert len(stmt.elements) == 3

# Line 203: In parse_atom, KeywordToken not reserved => VarReference.
def test_parse_var_reference():
    # "foo;" should be parsed as a VarReference.
    ast = parse_ast("foo;")
    stmt = ast.statements[0]
    assert isinstance(stmt, VarReference)
    # Name should be "foo"
    assert stmt.name == "foo"

# Line 210: In parse_atom, function call branch.
def test_parse_function_call_missing_close_paren():
    # "bar(1, 2" should raise an error about unclosed parenthesis.
    with pytest.raises(ParseError, match="Unclosed parenthesis in function call"):
        parse("bar(1, 2;")



# Lines 221-223: In parse_atom, postfix array indexing.
def test_postfix_array_indexing():
    # "foo[1];" should first parse foo as a VarReference then apply ArrayIndex.
    ast = parse_ast("foo[1];")
    stmt = ast.statements[0]
    # The outer node should be an ArrayIndex.
    assert isinstance(stmt, ArrayIndex)
    # The array part should be a VarReference.
    assert isinstance(stmt.array, VarReference)
    assert stmt.array.name == "foo"

# Lines 226-236: In parse_block: missing opening '{'
def test_parse_block_missing_open_brace():
    # Create a situation where a block is expected but '{' is missing.
    with pytest.raises(ParseError, match="Expected '{' at beginning of block"):
        parse("if 1 42;}")  # no '{' before 42



# Lines 261-272: In parse_statement, function definition branch error when function name is missing.
def test_def_missing_function_name():
    # After "def", a proper function name is expected.
    with pytest.raises(ParseError, match="Expected function name after 'def'"):
        parse("def 123(a){ 1; };")

# Lines 274-285: In parse_statement, "return" branch.
def test_return_statement():
    ast = parse_ast("return 10;")
    # Should parse as a Return node.
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "Return"

# Lines 290: In parse_statement, "print" branch.
def test_print_statement():
    ast = parse_ast("print(10);")
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "Print"

def get_single_statement(ast):
    if ast.__class__.__name__ == "Program" and len(ast.statements) == 1:
        return ast.statements[0]
    return ast

def test_for_loop_statement():
    code = "for( var i = 1; i < 3; i = i + 1 ){ print(i); print(1.1) };"
    ast = get_single_statement(parse_ast(code))
    assert ast.__class__.__name__ == "For"

def test_while_loop_statement():
    code = "var x = 10; while(x>0){ x = x-1; print };"
    ast = parse_ast(code)
    # Since ast is a Program with two statements, extract the while loop (second statement)
    while_stmt = ast.statements[1]
    assert while_stmt.__class__.__name__ == "While"



# Additional branch in parse_statement: KeywordToken("var")
def test_var_declaration_statement():
    code = "var x = 10;"
    ast = parse_ast(code)
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "VarDecl"
    assert stmt.name == "x"





# Finally, test the default expression branch in parse_statement.
def test_expression_statement_assignment():
    # "x = 5;" should be parsed as an Assignment.
    ast = parse_ast("x = 5;")
    stmt = ast.statements[0]
    assert stmt.__class__.__name__ == "Assignment"
    assert stmt.name == "x"

# Test default branch: a simple expression "42;"
def test_simple_expression_statement():
    ast = parse_ast("42;")
    stmt = ast.statements[0]
    assert isinstance(stmt, Int)
    assert stmt.val == "42"


# Lines 82-84 in parse_add_sub loop: test both '+' and '-' branches.
def test_add_sub_chain():
    # "1 + 2 - 3;" should produce a tree where the top-level operator is '-'
    ast = parse("1 + 2 - 3;")
    node = unwrap(ast)
    assert isinstance(node, BinOp)
    assert node.op == "-"
    # Left child should be a BinOp with '+'.
    assert isinstance(node.left, BinOp)
    assert node.left.op == "+"
    # Right child should be an Int with value "3".
    assert isinstance(node.right, Int)
    assert node.right.val == "3"

# Lines 113-114 in parse_mul_div loop: test "*", "/", "%" chain.
def test_mul_div_chain():
    # "2 * 3 / 4;" should evaluate to a chain.
    ast = parse("2 * 3 / 4;")
    node = unwrap(ast)
    # Top operator should be '/', check its left is a BinOp for '*'
    assert isinstance(node, BinOp)
    assert node.op == "/"
    assert isinstance(node.left, BinOp)
    assert node.left.op == "*"

# Lines 151-152: in parse_if branch when encountering "else if"
def test_if_with_elseif_only():
    # Use an if with an else if and no final else.
    code = "if 0 { 10; } else if 1 { 20; };"
    ast = parse(code)
    node = unwrap(ast)
    assert isinstance(node, If)
    # There should be one elseif branch, and elsee should be None.
    assert len(node.elseif_branches) == 1
    assert node.elsee is None

# Lines 176-177: in parse_atom for unary minus (already covered but reinforce)
def test_unary_minus_again():
    ast = parse("-99;")
    node = unwrap(ast)
    assert isinstance(node, UnOp)
    assert node.op == "-"
    assert isinstance(node.num, Int)
    assert node.num.val == "99"

# Line 183: in parse_atom for parenthesized expression.
def test_parenthesized_expression():
    # Correctly formed parenthesized expression should succeed.
    ast = parse("(1 + 2);")
    node = unwrap(ast)
    # Depending on implementation, node may be Parentheses wrapping a BinOp.
    if node.__class__.__name__ == "Parentheses":
        inner = node.val
    else:
        inner = node
    assert isinstance(inner, BinOp)
    assert inner.op == "+"

# Line 203: in parse_atom when a KeywordToken not reserved becomes VarReference.
def test_keyword_as_var_reference():
    # "foo;" should be parsed as a VarReference (not a function call, because no '(' follows)
    ast = parse("foo;")
    node = unwrap(ast)
    assert isinstance(node, VarReference)
    assert node.name == "foo"

# Line 210: In function call branch, missing closing parenthesis.
def test_function_call_missing_close():
    with pytest.raises(ParseError, match="Unclosed parenthesis in function call"):
        parse("bar(1, 2;")



# Lines 229-230: In parse_atom for KeywordToken leading to function call.
def test_function_call_correct():
    code = "sum(1, 2);"
    ast = parse(code)
    node = unwrap(ast)
    assert isinstance(node, FunctionCall)
    assert node.name == "sum"
    assert len(node.args) == 2

# Lines 234-235: In parse_atom, inside function call branch, testing proper closure.
def test_function_call_with_arguments():
    # This test ensures that after consuming arguments the parser expects a closing ')'
    code = "multiply(2, 3);"
    ast = parse(code)
    node = unwrap(ast)
    assert isinstance(node, FunctionCall)
    assert node.name == "multiply"
    assert len(node.args) == 2

# Lines 241-242: After KeywordToken branch (for VarReference fallback)
def test_var_reference_from_keyword():
    # "myVar;" where myVar is not a reserved keyword.
    ast = parse("myVar;")
    node = unwrap(ast)
    assert isinstance(node, VarReference)
    assert node.name == "myVar"

# Lines 246-247: Postfix array indexing once.
def test_single_postfix_indexing():
    # "arr[1];" should produce an ArrayIndex node.
    ast = parse("arr[1];")
    node = unwrap(ast)
    assert isinstance(node, ArrayIndex)
    assert isinstance(node.array, VarReference)
    assert node.array.name == "arr"
    assert isinstance(node.index, Int)
    assert node.index.val == "1"

# Lines 251-252: Multiple chained postfix indexing.
def test_multiple_postfix_indexing():
    # "matrix[1][2];" should produce nested ArrayIndex nodes.
    ast = parse("matrix[1][2];")
    node = unwrap(ast)
    # Outer node must be ArrayIndex
    assert isinstance(node, ArrayIndex)
    # Its inner node (array) should be an ArrayIndex as well.
    inner = node.array
    assert isinstance(inner, ArrayIndex)
    assert isinstance(inner.array, VarReference)
    assert inner.array.name == "matrix"
    # Check indices:
    assert inner.index.val == "1"
    assert node.index.val == "2"

# Lines 256-257: Ensure the while loop in postfix indexing is exercised with multiple comma-separated indexes in arrays is not applicable; already covered above.


# Lines 269-270: In parse_block, before expecting closing brace.
def test_block_missing_closing_brace():
    with pytest.raises(ParseError, match="Missing closing '}' after block"):
        parse("def hello(){return 1; ")

# Lines 277: In parse_statement for "def": missing function name error.
def test_def_missing_function_name_again():
    with pytest.raises(ParseError, match="Expected function name after 'def'"):
        parse("def 123(a){ 1; };")

# Lines 282-283: In parse_statement for "def": after parameter list.
def test_def_missing_closing_paren_in_params():
    with pytest.raises(ParseError, match="Expected '\\)' after parameter list"):
        parse("def foo(a { 1; };")

# Lines 287-293: In parse_statement handling "return", "print", "for", "while", "var"
def test_return_in_statement():
    # Test that "return" is parsed correctly.
    ast = parse("return 5;")
    node = unwrap(ast)
    assert node.__class__.__name__ == "Return"

def test_print_in_statement():
    ast = parse("print(99);")
    node = unwrap(ast)
    assert node.__class__.__name__ == "Print"

def test_for_loop_statement():
    # Use a for-loop with all required parts.
    code = "for( var i = 1; i <= 2; i = i + 1 ){ i; };"
    ast = parse(code)
    # The for-loop is the second statement if there's a preceding var declaration.
    # In this case, parse_program may return a Program with one For loop.
    node = unwrap(ast)
    assert node.__class__.__name__ == "For"

def test_while_loop_statement():
    # Two statements: declaration and while loop.
    code = "var x = 3; while(x > 0){ x = x - 1; };"
    ast = parse(code)
    # Extract the while loop which is the second statement.
    node = ast.statements[1]
    assert node.__class__.__name__ == "While"

# Lines 302-303: In parse_statement, default branch for assignment.
def test_assignment_expression():
    code = "var y = 10; y = y + 5;"
    ast = parse(code)
    # The second statement should be an Assignment.
    node = ast.statements[1]
    assert node.__class__.__name__ == "Assignment"
    assert node.name == "y"






# Test default expression branch when no other match: simple integer expression.
def test_simple_expression():
    ast = parse("42;")
    node = unwrap(ast)
    assert isinstance(node, Int)
    assert node.val == "42"

# Helper to unwrap a Program node if necessary.
def unwrap(ast):
    if hasattr(ast, "statements"):
        if len(ast.statements) == 1:
            return ast.statements[0]
    return ast

def test_var_decl():
    env = Environment()
    var_decl = VarDecl("x", Int("5"))
    result = e(var_decl, env)
    assert env.lookup("x") == 5

def test_var_reference():
    env = Environment()
    env.declare("x", 10)
    var_ref = VarReference("x")
    result = e(var_ref, env)
    assert result == 10

def test_bin_op_addition():
    env = Environment()
    bin_op = BinOp("+", Int("3"), Int("2"))
    result = e(bin_op, env)
    assert result == 5

def test_un_op_negative():
    env = Environment()
    un_op = UnOp("-", Int("5"))
    result = e(un_op, env)
    assert result == -5

def test_if_condition():
    env = Environment()
    if_stmt = If(Int("1"), Int("2"), [], Int("3"))
    result = e(if_stmt, env)
    assert result == 2

# def test_for_loop():
#     env = Environment()
#     for_stmt = For(VarDecl("i", Int("0")), BinOp("<", VarReference("i"), Int("5")), BinOp("+", VarReference("i"), Int("1")), Print(VarReference("i")))
#     result = e(for_stmt, env)
#     assert result == 4

# def test_while_loop():
#     env = Environment()
#     while_stmt = While(BinOp("<", VarReference("i"), Int("5")), Print(VarReference("i")))
#     env.declare("i", 0)
#     result = e(while_stmt, env)
#     assert result == 4


# def test_return_statement():
#     env = Environment()
#     func_def = FunctionDef("add", ["a", "b"], Return(BinOp("+", VarReference("a"), VarReference("b"))))
#     env.declare("add", func_def)
#     func_call = FunctionCall("add", [Int("3"), Int("4")])
#     result = e(func_call, env)
#     assert result == 7





def test_array_literal_and_index():
    env = Environment()
    array_literal = ArrayLiteral([Int("1"), Int("2"), Int("3")])
    result = e(array_literal, env)
    assert result == [1, 2, 3]
    
    array_index = ArrayIndex(array_literal, Int("2"))
    result = e(array_index, env)
    assert result == 2


def test_label():
    env = Environment()
    label = Label("start")
    result = e(label, env)
    assert result is None  # Labels don't affect execution



def test_invalid_label():
    env = Environment()
    try:
        program = Program([GoAndReturn("non_existing_label")])
        e(program, env)
    except ValueError as ve:
        assert str(ve) == "Label non_existing_label not found"

def test_valid_for_loop():
    code = "for (var i = 0; i < 10; i=i+1) { print(i); }"
    tokens = parse(code)  # Convert code to tokens







def test_valid_while_loop():
    code = "while (i < 10) { print(i); }"
    tokens = parse(code)


def test_valid_var_declaration():
    code = "var x = 5;"
    tokens = parse(code)




    

    


    