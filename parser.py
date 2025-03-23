from top import BinOp, UnOp, Float, Int, If, Parentheses, Program, VarDecl, VarReference, Assignment, AST, For, While, Print, FunctionCall
from lexer import IntToken, FloatToken, OperatorToken, KeywordToken, ParenToken, Token, lex

class ParseError(Exception):
    pass

def parse(s: str) -> AST:
    from more_itertools import peekable
    t = peekable(lex(s))

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError

    def parse_comparison():
        l = parse_add_sub()
        match t.peek(None):
            case OperatorToken('<') | OperatorToken('<=') | OperatorToken('>') | OperatorToken('>=') | OperatorToken('==') | OperatorToken('!='):
                op = t.peek(None).o
                next(t)
                r = parse_add_sub()
                return BinOp(op, l, r)
            case _:
                return l

    def parse_logic_and():
        expr = parse_comparison()
        while t.peek(None) == KeywordToken("and"):
            next(t)
            right = parse_comparison()
            expr = BinOp("and", expr, right)
        return expr

    def parse_logic_or():
        expr = parse_logic_and()
        while t.peek(None) == KeywordToken("or"):
            next(t)
            right = parse_logic_and()
            expr = BinOp("or", expr, right)
        return expr

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
                    break
        return ast

    def parse_mul_div():
        ast = parse_exp()
        while True:
            match t.peek(None):
                case OperatorToken('*') | OperatorToken('/') | OperatorToken('%'):
                    op = t.peek(None).o
                    next(t)
                    ast = BinOp(op, ast, parse_exp())
                case _:
                    break
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
        cond = parse_logic_or()
        then_expr = parse_block()
        elseif_branches = []
        while t.peek(None) == KeywordToken("else"):
            next(t)  # consume "else"
            if t.peek(None) == KeywordToken("if"):
                next(t)  # consume "if"
                elseif_cond = parse_logic_or()
                elseif_then = parse_block()
                elseif_branches.append((elseif_cond, elseif_then))
            else:
                else_expr = parse_block()
                return If(cond, then_expr, elseif_branches, else_expr)
        return If(cond, then_expr, elseif_branches, None)

    def parse_atom():
        match t.peek(None):
            case IntToken(v):
                next(t)
                return Int(v)
            case FloatToken(v):
                next(t)
                return Float(v)
            case ParenToken('('):
                next(t)
                expr = parse_logic_or()
                expect(ParenToken(')'))
                return Parentheses(expr)
            case OperatorToken('-'):
                next(t)
                return UnOp('-', parse_atom())
            case KeywordToken(x) if x not in ["if", "else", "var", "and", "or", "print", "for", "while"]:
                func_name = x
                next(t)
                if t.peek(None) == ParenToken('('):
                    next(t)  # consume '('
                    call_args = []
                    if t.peek(None) != ParenToken(')'):
                        call_args.append(parse_logic_or())
                        while t.peek(None) == OperatorToken(','):
                            next(t)
                            call_args.append(parse_logic_or())
                    try:
                        expect(ParenToken(')'))
                    except ParseError:
                        raise ParseError("Unclosed parenthesis in function call")
                    return FunctionCall(func_name, call_args)
                return VarReference(func_name)
        raise ParseError("Unexpected token in atom")
    
    def parse_block():
        try:
            expect(OperatorToken('{'))
        except ParseError:
            raise ParseError("Expected '{' at beginning of block")
        statements = []
        while t.peek(None) is not None and t.peek(None) != OperatorToken('}'):
            statements.append(parse_statement())
            if t.peek(None) == OperatorToken(';'):
                next(t)
        try:
            expect(OperatorToken('}'))
        except ParseError:
            raise ParseError("Missing closing '}' after block")
        return Program(statements) if len(statements) > 1 else statements[0]
    
    def parse_statement():
        match t.peek(None):
            case KeywordToken("print"):
                next(t)  # consume "print"
                try:
                    expect(ParenToken('('))
                except ParseError:
                    raise ParseError("Expected '(' after 'print'")
                expr = parse_logic_or()
                try:
                    expect(ParenToken(')'))
                except ParseError:
                    raise ParseError("Expected ')' after print argument")
                return Print(expr)
            case KeywordToken("for"):
                next(t)  # consume "for"
                try:
                    expect(ParenToken('('))
                except ParseError:
                    raise ParseError("Expected '(' after 'for'")
                init = parse_statement()
                try:
                    expect(OperatorToken(';'))
                except ParseError:
                    raise ParseError("Expected ';' after for-loop initializer")
                condition = parse_logic_or()
                try:
                    expect(OperatorToken(';'))
                except ParseError:
                    raise ParseError("Expected ';' after for-loop condition")
                increment = parse_statement()
                try:
                    expect(ParenToken(')'))
                except ParseError:
                    raise ParseError("Expected ')' after for-loop increment")
                body = parse_block()
                return For(init, condition, increment, body)
            case KeywordToken("while"):
                next(t)  # consume "while"
                try:
                    expect(ParenToken('('))
                except ParseError:
                    raise ParseError("Expected '(' after 'while'")
                condition = parse_logic_or()
                try:
                    expect(ParenToken(')'))
                except ParseError:
                    raise ParseError("Expected ')' after while-loop condition")
                body = parse_block()
                return While(condition, body)
            case KeywordToken("var"):
                next(t)  # consume "var"
                token = t.peek(None)
                if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "for", "while", "and", "or", "print"]):
                    raise ParseError("Expected variable name after 'var'")
                var_name = token.w
                next(t)
                try:
                    expect(OperatorToken('='))
                except ParseError:
                    raise ParseError("Expected '=' after variable name in declaration")
                expr = parse_logic_or()
                return VarDecl(var_name, expr)
            case _:
                expr = parse_logic_or()
                if isinstance(expr, VarReference) and t.peek(None) == OperatorToken('='):
                    next(t)  # consume '='
                    rhs = parse_logic_or()
                    return Assignment(expr.name, rhs)
                return expr

    def parse_program():
        statements = []
        while t.peek(None) is not None:
            statements.append(parse_statement())
            if t.peek(None) is not None:
                if t.peek(None) == OperatorToken(';'):
                    next(t)
                else:
                    raise ParseError("Missing semicolon between statements")
        return statements[0] if len(statements) == 1 else Program(statements)

    result = parse_program()
    return result
