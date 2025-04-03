import pytest
import builtins
from top import (
    e, Environment, BinOp, UnOp, Float, Int, Parentheses, If, VarDecl,
    VarReference, Assignment, Program, For, While, Print, FunctionCall, FunctionDef,
    Return, ArrayLiteral, ArrayIndex, Label, LabelReturn, GoAndReturn, UserFunction, ReturnException
)

# --- Basic Expression Evaluation ---

def test_int_evaluation():
    assert e(Int("123")) == 123

def test_float_evaluation():
    assert e(Float("3.14")) == 3.14

def test_binop_addition():
    expr = BinOp("+", Int("1"), Int("2"))
    assert e(expr) == 3

def test_unop_minus():
    expr = UnOp("-", Int("5"))
    assert e(expr) == -5

def test_parentheses_evaluation():
    # Parentheses node should simply evaluate the inner expression.
    expr = Parentheses(BinOp("*", Int("2"), Int("3")))
    assert e(expr) == 6

# --- Variable Declarations and Assignments ---

def test_var_declaration_and_assignment():
    prog = Program([
        VarDecl("x", Int("10")),
        Assignment("x", BinOp("+", VarReference("x"), Int("5")))
    ])
    # After declaration and assignment, x should be 15.
    assert e(prog) == 15

def test_undefined_variable():
    with pytest.raises(ValueError, match="Variable y not defined"):
        e(VarReference("y"))

# --- Control Flow: If Statement ---

def test_if_statement_then_branch():
    # if 1 { 42; }  -> should return 42 since condition is true.
    stmt = If(Int("1"), Int("42"), [], None)
    assert e(stmt) == 42

def test_if_statement_else_branch():
    # if 0 { 42; } else { 100; } -> condition false, so return else branch.
    stmt = If(Int("0"), Int("42"), [], Int("100"))
    assert e(stmt) == 100

def test_if_statement_elseif_branch():
    # if 0 { 42; } else if 1 { 55; } -> should execute elseif.
    stmt = If(Int("0"), Int("42"), [(Int("1"), Int("55"))], None)
    assert e(stmt) == 55

def test_if_missing_condition():
    with pytest.raises(ValueError, match="Condition missing in 'if' statement"):
         e(If(None, Int("1"), [], None))

# --- Loops ---

def test_for_loop():
    # for(var i = 1; i <= 3; i = i + 1) { i; }
    prog = For(
        VarDecl("i", Int("1")),
        BinOp("<=", VarReference("i"), Int("3")),
        Assignment("i", BinOp("+", VarReference("i"), Int("1"))),
        VarReference("i")
    )
    # Last iteration: i becomes 3 before the loop ends, so the body returns 3.
    assert e(prog) == 3

def test_while_loop():
    # Program that increments i while i < 4, then returns i.
    prog = Program([
       VarDecl("i", Int("1")),
       While(
           BinOp("<", VarReference("i"), Int("4")),
           Assignment("i", BinOp("+", VarReference("i"), Int("1")))
       ),
       VarReference("i")
    ])
    # Final value should be 4.
    assert e(prog) == 4

# --- Print Statement ---

def test_print_statement(capsys):
    stmt = Print(Int("123"))
    result = e(stmt)
    captured = capsys.readouterr().out.strip()
    assert captured == "123"
    assert result == 123

# --- Function Definitions and Calls ---

def test_function_def_and_call():
    # def add(a) { return a + 1; }  followed by add(10);
    func_body = Return(BinOp("+", VarReference("a"), Int("1")))
    func_def = FunctionDef("add", ["a"], func_body)
    prog = Program([func_def, FunctionCall("add", [Int("10")])])
    result = e(prog)
    assert result == 11

def test_function_call_wrong_arguments():
    # Define a function expecting 1 argument but call it with 0.
    func_body = Return(VarReference("a"))
    func_def = FunctionDef("id", ["a"], func_body)
    prog = Program([func_def, FunctionCall("id", [])])
    with pytest.raises(ValueError, match="expects 1 arguments"):
         e(prog)

def test_unknown_function():
    # Calling an undefined function should raise an error.
    with pytest.raises(ValueError, match="Unknown function foo"):
         e(FunctionCall("foo", []))

# --- Return Handling ---

def test_return_statement():
    # A return should raise a ReturnException.
    with pytest.raises(ReturnException):
         e(Return(Int("5")))

# --- Array Handling ---

def test_array_literal():
    arr = ArrayLiteral([Int("10"), Int("20"), Int("30")])
    assert e(arr) == [10, 20, 30]

def test_array_index():
    arr = ArrayLiteral([Int("10"), Int("20"), Int("30")])
    # Array indexing is one-based: index 2 should return 20.
    idx_expr = ArrayIndex(arr, Int("2"))
    assert e(idx_expr) == 20

def test_array_index_non_integer():
    arr = ArrayLiteral([Int("10"), Int("20")])
    with pytest.raises(ValueError, match="Array index must be an integer"):
         e(ArrayIndex(arr, Float("1.5")))

# --- Labels and GoAndReturn ---

def test_labels_and_goandreturn():
    # Create a program with a label and a labeled block.
    label_node = Label("start")
    stmt = VarDecl("x", Int("1"))
    ret_node = LabelReturn("start")
    prog = Program([label_node, stmt, ret_node])
    # Set the global program for label lookup.
    builtins.global_program = prog
    gar = GoAndReturn("start")
    # Running the goandreturn should execute the block and return None.
    assert e(gar) is None

# --- Parentheses Node ---

def test_parentheses_node():
    # Even if wrapped in a Parentheses node, the expression should evaluate correctly.
    expr = Parentheses(BinOp("*", Int("3"), Int("4")))
    assert e(expr) == 12
