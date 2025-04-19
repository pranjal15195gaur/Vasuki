# lexer.py
from collections.abc import Iterator
from dataclasses import dataclass

class Token:
    pass

@dataclass
class IntToken(Token):
    v: str

@dataclass
class FloatToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class KeywordToken(Token):
    w: str

@dataclass
class ParenToken(Token):
    w: str

@dataclass
class StringToken(Token):
    s: str

def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        while i < len(s) and s[i].isspace():
            i += 1

        if i == len(s):
            return

        if s[i].isdigit():
            t = s[i]
            i += 1
            isFloat = False
            isValid = True
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.':
                    if isFloat: isValid = False
                    isFloat = True
                t += s[i]
                i += 1

            if not isValid:
                raise ValueError('Invalid number token found :- {}'.format(t))

            if isFloat:
                yield FloatToken(t)
            else:
                yield IntToken(t)

        elif s[i].isalpha():
            t = s[i]
            i += 1
            while i < len(s) and (s[i].isalpha() or s[i].isdigit() or s[i] == '_'):
                if s[i].isdigit() and t[-1] == '_':
                    raise ValueError("Invalid identifier token found :- {}".format(t))
                t += s[i]
                i += 1
            match t:
                case 'if' | 'else':
                    if i < len(s) and s[i] == '{':
                        raise ValueError("Condition missing after '{}' keyword".format(t))
                    yield KeywordToken(t)
                case _:
                    yield KeywordToken(t)

        elif s[i] == '(':
            i += 1
            yield ParenToken('(')

        elif s[i] == ')':
            i += 1
            yield ParenToken(')')

        elif s[i] == '{':
            i += 1
            yield OperatorToken('{')

        elif s[i] == '}':
            i += 1
            yield OperatorToken('}')

        elif s[i] == '/' and i + 1 < len(s):
            # Check for comments
            if s[i+1] == '/':
                # Single-line comment
                i += 2  # Skip '//' characters
                while i < len(s) and s[i] != '\n':
                    i += 1
                if i < len(s):  # Skip the newline character
                    i += 1
            elif s[i+1] == '*':
                # Multi-line comment
                i += 2  # Skip '/*' characters
                nesting = 1
                while i + 1 < len(s) and nesting > 0:
                    if s[i] == '/' and s[i+1] == '*':
                        nesting += 1
                        i += 2
                    elif s[i] == '*' and s[i+1] == '/':
                        nesting -= 1
                        i += 2
                    else:
                        i += 1
                if nesting > 0:
                    raise ValueError('Unterminated multi-line comment')
            else:
                # Regular division operator
                yield OperatorToken('/')
                i += 1
        elif s[i] in '+-*<>=!':
            if s[i:i+2] in ['<=', '>=', '==', '!=', '**']:
                yield OperatorToken(s[i:i+2])
                i += 2
            else:
                yield OperatorToken(s[i])
                i += 1

        elif s[i] == ';':
            i += 1
            yield OperatorToken(';')

        elif s[i] == '%':  # modulo operator
            i += 1
            yield OperatorToken('%')

        elif s[i] == ',':
            i += 1
            yield OperatorToken(',')

        elif s[i] == '[':
            i += 1
            yield OperatorToken('[')

        elif s[i] == ']':
            i += 1
            yield OperatorToken(']')

        elif s[i] == ':':
            i += 1
            yield OperatorToken(':')
        elif s[i] == '"':
            # Handle string literals
            i += 1  # Skip opening quote
            string_content = ""
            while i < len(s) and s[i] != '"':
                string_content += s[i]
                i += 1
            if i >= len(s):
                raise ValueError('Unterminated string literal')
            i += 1  # Skip closing quote
            yield StringToken(string_content)
        else:
            raise ValueError('Unexpected character found :- {}'.format(s[i]))
