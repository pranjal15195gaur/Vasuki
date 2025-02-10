from top import BinOp, UnOp, Float, Int, If, Parentheses, AST, Var, Assign
from lexer import IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken, IdentifierToken, Token, lex

class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError(f"Expected {what}, but got {t.peek(None)}")

    def parse_cmp():
        l = parse_add_sub()
        match t.peek(None):
            case OperatorToken('<') | OperatorToken('<=') | OperatorToken('>') | OperatorToken('>=') | OperatorToken('==') | OperatorToken('!='):
                op = t.peek(None).o
                next(t)
                r = parse_add_sub()
                return BinOp(op, l, r)
            case _:
                return l

    def parse_add_sub():
        ast = parse_mul_div()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul_div())
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_mul_div())
                case _:
                    return ast

    def parse_mul_div():
        ast = parse_exp()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_exp())
                case OperatorToken('/'):
                    next(t)
                    ast = BinOp("/", ast, parse_exp())
                case _:
                    return ast

    def parse_exp():
        l = parse_if()
        match t.peek(None):
            case OperatorToken('**'):
                next(t)
                r = parse_if()
                return BinOp("**", l, r)
            case _:
                return l

    def parse_if():
        if t.peek(None) != KeywordToken("if"):
            return parse_atom()
        next(t)  # consume "if"
        cond = parse_cmp()
        if cond is None:
            raise ParseError("Missing condition after 'if'")
        try:
            expect(OperatorToken('{'))
        except ParseError:
            raise ParseError("Expected '{' after 'if' condition")
        then_expr = parse_cmp()
        try:
            expect(OperatorToken('}'))
        except ParseError:
            raise ParseError("Missing closing '}' after 'if' block")

        elseif_branches = []
        while True:
            if t.peek(None) == KeywordToken("else"):
                next(t)  # consume "else"
                if t.peek(None) == KeywordToken("if"):
                    next(t)  # consume "if"
                    elseif_cond = parse_cmp()
                    if elseif_cond is None:
                        raise ParseError("Missing condition after 'else if'")
                    try:
                        expect(OperatorToken('{'))
                    except ParseError:
                        raise ParseError("Expected '{' after 'else if' condition")
                    elseif_then = parse_cmp()
                    try:
                        expect(OperatorToken('}'))
                    except ParseError:
                        raise ParseError("Missing closing '}' after 'else if' block")
                    elseif_branches.append((elseif_cond, elseif_then))
                else:
                    try:
                        expect(OperatorToken('{'))
                    except ParseError:
                        raise ParseError("Expected '{' after 'else'")
                    else_expr = parse_cmp()
                    try:
                        expect(OperatorToken('}'))
                    except ParseError:
                        raise ParseError("Missing closing '}' after 'else' block")
                    return If(cond, then_expr, elseif_branches, else_expr)
            else:
                return If(cond, then_expr, elseif_branches, None)

    def parse_atom():
        match t.peek(None):
            case IntToken(v):
                next(t)
                return Int(v)
            case FloatToken(v):
                next(t)
                return Float(v)
            case IdentifierToken(name):
                next(t)
                return Var(name)
            case ParenToken('('):
                next(t)
                # Allow assignments inside parentheses by calling the top production.
                expr = parse_assignment()
                expect(ParenToken(')'))
                return Parentheses(expr)
            case OperatorToken('-'):
                next(t)
                val = parse_atom()
                return UnOp('-', val)
            case KeywordToken("if"):
                return parse_if()
            case _:
                raise ParseError("Unexpected token: {}".format(t.peek(None)))

    # New production: assignment (right–associative and lowest precedence)
    def parse_assignment():
        left = parse_cmp()
        if isinstance(left, Var) and t.peek(None) == OperatorToken('='):
            next(t)  # consume '='
            right = parse_assignment()
            return Assign(left.name, right)
        return left

    return parse_assignment()
