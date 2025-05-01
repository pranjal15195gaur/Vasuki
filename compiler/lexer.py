"""
Lexical analyzer for the Vasuki programming language.

This module provides functionality to tokenize source code into a stream of tokens
that can be processed by the parser. It handles various token types including
integers, floats, operators, keywords, parentheses, and strings.
"""
from collections.abc import Iterator
from compiler.errors import LexerError, SourceLocation

class Token:
    """Base class for all tokens in the Vasuki language.

    All specific token types inherit from this class and implement their own
    equality comparison methods.
    """
    def __init__(self):
        self.location = SourceLocation()

    def set_location(self, line, column, file=None):
        """Set the source location for this token.

        Args:
            line: The line number where the token appears (1-based)
            column: The column number where the token starts (1-based)
            file: Optional filename where the token appears

        Returns:
            self: Returns the token instance for method chaining
        """
        self.location = SourceLocation(line, column, file)
        return self

class IntToken(Token):
    """Token representing an integer literal in the source code."""
    def __init__(self, v):
        super().__init__()
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, IntToken):
            return False
        return self.v == other.v

class FloatToken(Token):
    """Token representing a floating-point literal in the source code."""
    def __init__(self, v):
        super().__init__()
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, FloatToken):
            return False
        return self.v == other.v

class OperatorToken(Token):
    """Token representing an operator or delimiter in the source code.

    This includes arithmetic operators, comparison operators, and delimiters
    like braces, brackets, and semicolons.
    """
    def __init__(self, o):
        super().__init__()
        self.o = o

    def __eq__(self, other):
        if not isinstance(other, OperatorToken):
            return False
        return self.o == other.o

class KeywordToken(Token):
    """Token representing a keyword or identifier in the source code.

    This includes language keywords like 'if', 'else', 'var', etc.,
    as well as user-defined identifiers.
    """
    def __init__(self, w):
        super().__init__()
        self.w = w

    def __eq__(self, other):
        if not isinstance(other, KeywordToken):
            return False
        return self.w == other.w

class ParenToken(Token):
    """Token representing parentheses in the source code.

    This specifically handles '(' and ')' characters, which are used for
    grouping expressions and function calls.
    """
    def __init__(self, w):
        super().__init__()
        self.w = w

    def __eq__(self, other):
        if not isinstance(other, ParenToken):
            return False
        return self.w == other.w

class StringToken(Token):
    """Token representing a string literal in the source code."""
    def __init__(self, s):
        super().__init__()
        self.s = s

    def __eq__(self, other):
        if not isinstance(other, StringToken):
            return False
        return self.s == other.s

def lex(s: str, filename="<input>") -> Iterator[Token]:
    """Tokenize the input string into a stream of tokens.

    This function scans through the input string character by character,
    identifying tokens according to the Vasuki language syntax rules.
    It handles whitespace, comments, numbers, identifiers, operators,
    and other language elements.

    Args:
        s: The source code string to tokenize
        filename: Optional name of the source file (for error reporting)

    Returns:
        An iterator yielding Token objects

    Raises:
        LexerError: If invalid syntax is encountered
    """
    i = 0
    line = 1
    column = 1

    def create_token_with_location(token_class, value, start_column):
        """Create a token with source location information.

        Args:
            token_class: The token class to instantiate
            value: The value to pass to the token constructor
            start_column: The column where the token starts

        Returns:
            A new token with location information set
        """
        token = token_class(value)
        token.set_location(line, start_column, filename)
        return token

    def raise_lexer_error(message, error_column=None):
        """Raise a lexer error with detailed location information.

        Args:
            message: The error message
            error_column: Optional specific column where the error occurred

        Raises:
            LexerError: With location information and source line
        """
        loc = SourceLocation(line, error_column or column, filename)
        source_line = s.splitlines()[line-1] if line <= len(s.splitlines()) else None
        raise LexerError(message, loc, source_line)

    while True:
        # Skip whitespace and track line/column numbers
        while i < len(s) and s[i].isspace():
            if s[i] == '\n':
                line += 1
                column = 1
            else:
                column += 1
            i += 1

        if i == len(s):
            return

        if s[i].isdigit():
            start_column = column
            t = s[i]
            i += 1
            column += 1
            isFloat = False
            isValid = True
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.':
                    if isFloat: isValid = False
                    isFloat = True
                t += s[i]
                i += 1
                column += 1

            if not isValid:
                raise_lexer_error(f'Invalid number format: {t}', start_column)

            if isFloat:
                yield create_token_with_location(FloatToken, t, start_column)
            else:
                yield create_token_with_location(IntToken, t, start_column)

        elif s[i].isalpha():
            start_column = column
            t = s[i]
            i += 1
            column += 1
            while i < len(s) and (s[i].isalpha() or s[i].isdigit() or s[i] == '_'):
                if s[i].isdigit() and t[-1] == '_':
                    raise_lexer_error(f"Invalid identifier: {t} (digit cannot follow underscore)", start_column)
                t += s[i]
                i += 1
                column += 1
            match t:
                case 'if' | 'else':
                    if i < len(s) and s[i] == '{':
                        raise_lexer_error(f"Condition missing after '{t}' keyword", start_column)
                    yield create_token_with_location(KeywordToken, t, start_column)
                case 'true':
                    yield create_token_with_location(KeywordToken, 'true', start_column)
                case 'false':
                    yield create_token_with_location(KeywordToken, 'false', start_column)
                case _:
                    yield create_token_with_location(KeywordToken, t, start_column)

        elif s[i] == '(':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(ParenToken, '(', start_column)

        elif s[i] == ')':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(ParenToken, ')', start_column)

        elif s[i] == '{':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, '{', start_column)

        elif s[i] == '}':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, '}', start_column)

        elif s[i] == '/' and i + 1 < len(s):
            # Check for comments
            start_column = column
            if s[i+1] == '/':
                # Single-line comment
                i += 2  # Skip '//' characters
                column += 2
                while i < len(s) and s[i] != '\n':
                    i += 1
                    column += 1
                if i < len(s):  # Skip the newline character
                    i += 1
                    line += 1
                    column = 1
            elif s[i+1] == '*':
                # Multi-line comment with support for nested comments
                start_column = column
                i += 2  # Skip '/*' characters
                column += 2
                nesting = 1
                while i + 1 < len(s) and nesting > 0:
                    if s[i] == '\n':
                        line += 1
                        column = 1
                        i += 1
                    elif s[i] == '/' and s[i+1] == '*':
                        nesting += 1
                        i += 2
                        column += 2
                    elif s[i] == '*' and s[i+1] == '/':
                        nesting -= 1
                        i += 2
                        column += 2
                    else:
                        i += 1
                        column += 1
                if nesting > 0:
                    raise_lexer_error('Unterminated multi-line comment', start_column)
            else:
                # Regular division operator
                yield create_token_with_location(OperatorToken, '/', start_column)
                i += 1
                column += 1
        elif s[i] in '+-*<>=!':
            start_column = column
            if i+1 < len(s) and s[i:i+2] in ['<=', '>=', '==', '!=', '**']:
                op = s[i:i+2]
                i += 2
                column += 2
                yield create_token_with_location(OperatorToken, op, start_column)
            else:
                op = s[i]
                i += 1
                column += 1
                yield create_token_with_location(OperatorToken, op, start_column)

        elif s[i] == ';':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, ';', start_column)

        elif s[i] == '%':  # modulo operator
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, '%', start_column)

        elif s[i] == ',':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, ',', start_column)

        elif s[i] == '[':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, '[', start_column)

        elif s[i] == ']':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, ']', start_column)

        elif s[i] == ':':
            start_column = column
            i += 1
            column += 1
            yield create_token_with_location(OperatorToken, ':', start_column)
        elif s[i] == '"':
            # Handle string literals
            start_column = column
            i += 1  # Skip opening quote
            column += 1
            string_content = ""
            while i < len(s) and s[i] != '"':
                if s[i] == '\n':
                    raise_lexer_error('Unterminated string literal (newline in string)', start_column)
                string_content += s[i]
                i += 1
                column += 1
            if i >= len(s):
                raise_lexer_error('Unterminated string literal (reached end of file)', start_column)
            i += 1  # Skip closing quote
            column += 1
            yield create_token_with_location(StringToken, string_content, start_column)
        else:
            raise_lexer_error(f'Unexpected character: {s[i]}')
