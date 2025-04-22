# lexer.py
from collections.abc import Iterator
from errors import LexerError, SourceLocation

class Token:
    """Base class for all tokens."""
    def __init__(self):
        self.location = SourceLocation()

    def set_location(self, line, column, file=None):
        """Set the source location for this token."""
        self.location = SourceLocation(line, column, file)
        return self

class IntToken(Token):
    def __init__(self, v):
        super().__init__()
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, IntToken):
            return False
        return self.v == other.v

class FloatToken(Token):
    def __init__(self, v):
        super().__init__()
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, FloatToken):
            return False
        return self.v == other.v

class OperatorToken(Token):
    def __init__(self, o):
        super().__init__()
        self.o = o

    def __eq__(self, other):
        if not isinstance(other, OperatorToken):
            return False
        return self.o == other.o

class KeywordToken(Token):
    def __init__(self, w):
        super().__init__()
        self.w = w

    def __eq__(self, other):
        if not isinstance(other, KeywordToken):
            return False
        return self.w == other.w

class ParenToken(Token):
    def __init__(self, w):
        super().__init__()
        self.w = w

    def __eq__(self, other):
        if not isinstance(other, ParenToken):
            return False
        return self.w == other.w

class StringToken(Token):
    def __init__(self, s):
        super().__init__()
        self.s = s

    def __eq__(self, other):
        if not isinstance(other, StringToken):
            return False
        return self.s == other.s

def lex(s: str, filename="<input>") -> Iterator[Token]:
    i = 0
    line = 1
    column = 1

    # Helper function to create tokens with location information
    def create_token_with_location(token_class, value, start_column):
        token = token_class(value)
        token.set_location(line, start_column, filename)
        return token

    # Helper function to raise lexer errors with location information
    def raise_lexer_error(message, error_column=None):
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
                # Multi-line comment
                comment_start_line = line
                comment_start_column = column
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
                    raise_lexer_error('Unterminated multi-line comment', comment_start_column)
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
