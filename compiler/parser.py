from top import (BinOp, UnOp, Float, Int, String, Boolean, If, Parentheses, Program, VarDecl, DynamicVarDecl,
                 VarReference, Assignment, AST, For, While, Print,
                 ArrayLiteral, ArrayIndex, ArrayAssignment, StringIndex, DictLiteral, DictGet, FunctionCall, FunctionDef, DynamicFunctionDef, Return, Yield, Label, LabelReturn, GoAndReturn)


from lexer import IntToken, FloatToken, StringToken, OperatorToken, KeywordToken, ParenToken, Token, lex
from errors import ParserError, SourceLocation
import builtins
from more_itertools import peekable

def parse(s: str, filename="<input>") -> AST:
    # Get the tokens with source location information
    t = peekable(lex(s, filename))
    source_lines = s.splitlines()

    # Helper function to raise parser errors with location information
    def raise_parser_error(message, token=None):
        if token is None:
            token = t.peek(None)

        if token is not None and hasattr(token, 'location'):
            loc = token.location
            source_line = source_lines[loc.line-1] if 0 < loc.line <= len(source_lines) else None
            raise ParserError(message, loc, source_line)
        else:
            # Fallback if token doesn't have location information
            raise ParserError(message)

    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        # Get the current token for error reporting
        current = t.peek(None)
        if current is None:
            raise_parser_error(f"Expected {what}, but reached end of file")
        else:
            raise_parser_error(f"Expected {what}, but got {current}")

    def parse_logic_or():
        left = parse_logic_and()
        while t.peek(None) == KeywordToken("or"):
            next(t)
            right = parse_logic_and()
            left = BinOp("or", left, right)
        return left

    def parse_logic_and():
        left = parse_equality()
        while t.peek(None) == KeywordToken("and"):
            next(t)
            right = parse_equality()
            left = BinOp("and", left, right)
        return left

    def parse_equality():
        left = parse_comparison()
        while t.peek(None) in [OperatorToken("=="), OperatorToken("!=")]:
            op = next(t).o
            right = parse_comparison()
            left = BinOp(op, left, right)
        return left

    def parse_comparison():
        left = parse_term()
        while t.peek(None) in [OperatorToken("<"), OperatorToken(">"), OperatorToken("<="), OperatorToken(">=")]:
            op = next(t).o
            right = parse_term()
            left = BinOp(op, left, right)
        return left

    def parse_term():
        left = parse_factor()
        while t.peek(None) in [OperatorToken("+"), OperatorToken("-")]:
            op = next(t).o
            right = parse_factor()
            left = BinOp(op, left, right)
        return left

    def parse_factor():
        left = parse_power()
        while t.peek(None) in [OperatorToken("*"), OperatorToken("/"), OperatorToken("%")]:
            op = next(t).o
            right = parse_power()
            left = BinOp(op, left, right)
        return left

    def parse_power():
        left = parse_if()
        if t.peek(None) == OperatorToken("**"):
            next(t)
            right = parse_power()  # Right-associative
            left = BinOp("**", left, right)
        return left

    def parse_if():
        if t.peek(None) != KeywordToken("if"):
            return parse_atom()
        next(t)  # consume "if"
        cond = parse_logic_or()           # use logical expression for condition
        then_expr = parse_block()         # parse then block
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

    def parse_while():
        next(t)  # consume "while"
        if t.peek(None) != ParenToken('('):
            raise_parser_error("Expected '(' after 'while'")
        next(t)  # consume '('
        condition = parse_logic_or()
        try:
            expect(ParenToken(')'))
        except ParserError:
            raise_parser_error("Expected ')' after while-loop condition")
        body = parse_block()
        return While(condition, body)

    def parse_for():
        next(t)  # consume "for"
        try:
            expect(ParenToken('('))
        except ParserError:
            raise_parser_error("Expected '(' after 'for'")

        # Parse initializer
        init = parse_statement()
        try:
            expect(OperatorToken(';'))
        except ParserError:
            raise_parser_error("Expected ';' after for-loop initializer")

        # Parse condition
        condition = parse_logic_or()
        try:
            expect(OperatorToken(';'))
        except ParserError:
            raise_parser_error("Expected ';' after for-loop condition")

        # Parse increment
        increment = parse_statement()
        try:
            expect(ParenToken(')'))
        except ParserError:
            raise_parser_error("Expected ')' after for-loop increment")
        body = parse_block()
        return For(init, condition, increment, body)

    def parse_atom():
        token = t.peek(None)

        # Integer literal
        if isinstance(token, IntToken):
            next(t)
            node = Int(token.v)

        # Float literal
        elif isinstance(token, FloatToken):
            next(t)
            node = Float(token.v)

        # String literal
        elif isinstance(token, StringToken):
            next(t)
            node = String(token.s)

        # Parenthesized expression
        elif isinstance(token, ParenToken) and token.w == '(':
            next(t)
            node = parse_logic_or()      # full expression in parentheses
            expect(ParenToken(')'))

        # Unary operators (minus and not)
        elif isinstance(token, OperatorToken) and token.o == '-':
            next(t)
            node = UnOp('-', parse_atom())
        elif isinstance(token, KeywordToken) and token.w == 'not':
            next(t)
            node = UnOp('not', parse_atom())

        # Array literal
        elif isinstance(token, OperatorToken) and token.o == '[':
            next(t)  # consume '['
            elements = []
            if t.peek(None) != OperatorToken(']'):
                elements.append(parse_logic_or())
                while t.peek(None) == OperatorToken(','):
                    next(t)
                    elements.append(parse_logic_or())
            expect(OperatorToken(']'))
            node = ArrayLiteral(elements)

        # Dictionary literal
        elif isinstance(token, OperatorToken) and token.o == '{':
            next(t)  # consume '{'
            keys = []
            values = []
            if t.peek(None) != OperatorToken('}'):
                # Parse key
                key = parse_logic_or()
                keys.append(key)
                # Expect colon
                if t.peek(None) != OperatorToken(':'):
                    raise_parser_error("Expected ':' after dictionary key")
                next(t)  # consume ':'
                # Parse value
                value = parse_logic_or()
                values.append(value)
                # Parse additional key-value pairs
                while t.peek(None) == OperatorToken(','):
                    next(t)  # consume ','
                    # Parse key
                    key = parse_logic_or()
                    keys.append(key)
                    # Expect colon
                    if t.peek(None) != OperatorToken(':'):
                        raise_parser_error("Expected ':' after dictionary key")
                    next(t)  # consume ':'
                    # Parse value
                    value = parse_logic_or()
                    values.append(value)
            expect(OperatorToken('}'))
            node = DictLiteral(keys, values)

        # Boolean literals
        elif isinstance(token, KeywordToken) and token.w in ["true", "false"]:
            next(t)
            node = Boolean(token.w == "true")

        # Function call or variable reference
        elif isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "and", "or", "print", "for", "while", "true", "false"]:
            func_name = token.w
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
                except ParserError:
                    raise_parser_error("Unclosed parenthesis in function call")
                node = FunctionCall(func_name, call_args)
            else:
                node = VarReference(func_name)

        # While loop
        elif isinstance(token, KeywordToken) and token.w == "while":
            return parse_while()

        # For loop
        elif isinstance(token, KeywordToken) and token.w == "for":
            return parse_for()

        # Unexpected token
        else:
            raise_parser_error("Unexpected token in atom")

        # Handle postfix array, string, and dictionary indexing: e.g. x[1] or [1,2,3][2] or "hello"[1] or {"key": value}["key"]
        while t.peek(None) == OperatorToken('['):
            next(t)  # consume '['
            index_expr = parse_logic_or()
            expect(OperatorToken(']'))
            # For simplicity, we'll determine at runtime whether it's a string, array, or dictionary
            if isinstance(node, String):
                node = StringIndex(node, index_expr)
            elif isinstance(node, DictLiteral):
                node = DictGet(node, index_expr)
            else:
                node = ArrayIndex(node, index_expr)

            # Check if this is an assignment to an array element: arr[1] = value
            if t.peek(None) == OperatorToken('='):
                next(t)  # consume '='
                value_expr = parse_logic_or()
                node = ArrayAssignment(node.array, node.index, value_expr)
                break  # Exit the loop since we've handled the assignment
        return node


    # New helper to parse a block of statements enclosed in '{' and '}'
    def parse_block():
        try:
            expect(OperatorToken('{'))
        except ParserError:
            raise_parser_error("Expected '{' at beginning of block")
        statements = []
        while t.peek(None) is not None and t.peek(None) != OperatorToken('}'):
            statements.append(parse_statement())
            if t.peek(None) == OperatorToken(';'):
                next(t)
        try:
            expect(OperatorToken('}'))
        except ParserError:
            raise_parser_error("Missing closing '}' after block")
        return Program(statements) if len(statements) > 1 else statements[0]

    def parse_statement():
        # Skip any leading semicolons
        while t.peek(None) == OperatorToken(';'):
            next(t)

        token = t.peek(None)

        # Function definition
        if isinstance(token, KeywordToken) and token.w == "def":
            next(t)  # consume "def"
            token = t.peek(None)
            if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "for", "while", "and", "or", "print", "def"]):
                raise_parser_error("Expected function name after 'def'")
            func_name = token.w
            next(t)
            try:
                expect(ParenToken('('))
            except ParserError:
                raise_parser_error("Expected '(' after function name")
            params = []
            if t.peek(None) != ParenToken(')'):
                # At least one parameter
                token = t.peek(None)
                if not isinstance(token, KeywordToken):
                    raise_parser_error("Expected parameter name")
                params.append(token.w)
                next(t)
                while t.peek(None) == OperatorToken(','):
                    next(t)
                    token = t.peek(None)
                    if not isinstance(token, KeywordToken):
                        raise_parser_error("Expected parameter name")
                    params.append(token.w)
                    next(t)
            try:
                expect(ParenToken(')'))
            except ParserError:
                raise_parser_error("Expected ')' after parameter list")
            body = parse_block()  # Reuse block parsing for the function body.
            return FunctionDef(func_name, params, body)

        # Return statement
        elif isinstance(token, KeywordToken) and token.w == "return":
            next(t)  # consume "return"
            expr = parse_logic_or()  # parse the expression following 'return'
            return Return(expr)

        # Yield statement
        elif isinstance(token, KeywordToken) and token.w == "yield":
            next(t)  # consume "yield"
            expr = parse_logic_or()  # parse the expression following 'yield'
            return Yield(expr)

        # Print statement
        elif isinstance(token, KeywordToken) and token.w == "print":
            next(t)  # consume "print"
            try:
                expect(ParenToken('('))
            except ParserError:
                raise_parser_error("Expected '(' after 'print'")
            expr = parse_logic_or()
            try:
                expect(ParenToken(')'))
            except ParserError:
                raise_parser_error("Expected ')' after print argument")
            return Print(expr)

        # For loop
        elif isinstance(token, KeywordToken) and token.w == "for":
            return parse_for()

        # While loop
        elif isinstance(token, KeywordToken) and token.w == "while":
            return parse_while()

        # Dynamic variable or function
        elif isinstance(token, KeywordToken) and token.w == "dynamic":
            next(t)  # consume "dynamic"
            if t.peek(None) == KeywordToken("var"):
                next(t)  # consume "var"
                token = t.peek(None)
                if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "for", "while", "and", "or", "print", "goandreturn", "dynamic", "def"]):
                    raise_parser_error("Expected variable name after 'dynamic var'")
                var_name = token.w
                next(t)
                try:
                    expect(OperatorToken('='))
                except ParserError:
                    raise_parser_error("Expected '=' after variable name in dynamic declaration")
                expr = parse_logic_or()
                return DynamicVarDecl(var_name, expr)
            elif t.peek(None) == KeywordToken("def"):
                next(t)  # consume "def"
                token = t.peek(None)
                if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "for", "while", "and", "or", "print", "goandreturn", "dynamic", "def"]):
                    raise_parser_error("Expected function name after 'dynamic def'")
                func_name = token.w
                next(t)
                try:
                    expect(ParenToken('('))
                except ParserError:
                    raise_parser_error("Expected '(' after function name")
                params = []
                if t.peek(None) != ParenToken(')'):
                    # At least one parameter
                    token = t.peek(None)
                    if not isinstance(token, KeywordToken):
                        raise_parser_error("Expected parameter name")
                    params.append(token.w)
                    next(t)
                    while t.peek(None) == OperatorToken(','):
                        next(t)
                        token = t.peek(None)
                        if not isinstance(token, KeywordToken):
                            raise_parser_error("Expected parameter name")
                        params.append(token.w)
                        next(t)
                try:
                    expect(ParenToken(')'))
                except ParserError:
                    raise_parser_error("Expected ')' after parameter list")
                body = parse_block()  # Reuse block parsing for the function body.
                return DynamicFunctionDef(func_name, params, body)
            else:
                raise_parser_error("Expected 'var' or 'def' after 'dynamic'")

        # Variable declaration
        elif isinstance(token, KeywordToken) and token.w == "var":
            next(t)  # consume "var"
            token = t.peek(None)
            if not (isinstance(token, KeywordToken) and token.w not in ["if", "else", "var", "for", "while", "and", "or", "print", "goandreturn", "dynamic"]):
                raise_parser_error("Expected variable name after 'var'")
            var_name = token.w
            next(t)
            try:
                expect(OperatorToken('='))
            except ParserError:
                raise_parser_error("Expected '=' after variable name in declaration")
            expr = parse_logic_or()
            return VarDecl(var_name, expr)

        # GoAndReturn statement
        elif isinstance(token, KeywordToken) and token.w == "goandreturn":
            next(t)
            label_name_token = t.peek(None)
            if not isinstance(label_name_token, KeywordToken):
                raise_parser_error("Expected label name after 'goandreturn'")
            label_name = label_name_token.w
            next(t)
            return GoAndReturn(label_name)

        # Label or other keyword
        elif isinstance(token, KeywordToken):
            label_name = token.w
            # Consume the keyword token
            label_token = next(t)
            next_token = t.peek(None)
            if isinstance(next_token, OperatorToken) and next_token.o == ':':
                next(t)  # consume ':'
                return Label(label_name)
            elif isinstance(next_token, KeywordToken) and next_token.w == 'return':
                next(t)
                return LabelReturn(label_name)
            else:
                # Put label_token back and parse expression
                t.prepend(label_token)
                expr = parse_logic_or()
                if isinstance(expr, VarReference) and t.peek(None) == OperatorToken('='):
                    next(t)
                    rhs = parse_logic_or()
                    return Assignment(expr.name, rhs)
                return expr

        # Expression or assignment
        else:
            expr = parse_logic_or()
            if isinstance(expr, VarReference) and t.peek(None) == OperatorToken('='):
                next(t)  # consume '='
                rhs = parse_logic_or()
                return Assignment(expr.name, rhs)
            return expr

    def parse_program():
        statements = []
        while t.peek(None) is not None:
            stmt = parse_statement()
            statements.append(stmt)
            if t.peek(None) is not None:
                # Exempt label, label return, and goandreturn from semicolon enforcement.
                if not isinstance(stmt, (Label, LabelReturn, GoAndReturn)):
                    if t.peek(None) == OperatorToken(';'):
                        next(t)
                    else:
                        raise_parser_error("Missing semicolon between statements")
        return statements[0] if len(statements) == 1 else Program(statements)



    result = parse_program()
    final_ast = result if isinstance(result, Program) else Program([result])
    setattr(builtins, 'global_program', final_ast)
    return result
