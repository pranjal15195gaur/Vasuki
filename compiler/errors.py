"""
Error handling system for the Vasuki language.
Provides detailed error messages with source location information.
"""

class SourceLocation:
    """Represents a location in the source code."""
    def __init__(self, line=None, column=None, file=None):
        self.line = line
        self.column = column
        self.file = file or "<unknown>"
    
    def __str__(self):
        if self.line is not None and self.column is not None:
            return f"{self.file}:{self.line}:{self.column}"
        elif self.line is not None:
            return f"{self.file}:{self.line}"
        else:
            return self.file


class VasukiError(Exception):
    """Base class for all Vasuki language errors."""
    def __init__(self, message, location=None, source_line=None):
        self.message = message
        self.location = location or SourceLocation()
        self.source_line = source_line
        super().__init__(self.format_message())
    
    def format_message(self):
        """Format the error message with location information."""
        result = f"{self.location}: {self.__class__.__name__}: {self.message}"
        
        if self.source_line and self.location.column is not None:
            result += f"\n{self.source_line}\n{' ' * (self.location.column - 1)}^"
        
        return result


class LexerError(VasukiError):
    """Raised when the lexer encounters an invalid token."""
    pass


class ParserError(VasukiError):
    """Raised when the parser encounters a syntax error."""
    pass


class NameError(VasukiError):
    """Raised when a variable or function name is not found."""
    pass


class TypeError(VasukiError):
    """Raised when an operation is performed on an inappropriate type."""
    pass


class ValueError(VasukiError):
    """Raised when an operation receives an argument of the correct type but inappropriate value."""
    pass


class IndexError(VasukiError):
    """Raised when a sequence subscript is out of range."""
    pass


class KeyError(VasukiError):
    """Raised when a dictionary key is not found."""
    pass


class DivisionByZeroError(VasukiError):
    """Raised when division or modulo by zero is encountered."""
    pass


class RecursionError(VasukiError):
    """Raised when the interpreter detects that the maximum recursion depth is exceeded."""
    pass


class RuntimeError(VasukiError):
    """Raised when an error is detected that doesn't fall into any of the other categories."""
    pass


def get_source_line(source, line_number):
    """Extract a specific line from the source code."""
    if not source:
        return None
    
    lines = source.splitlines()
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1]
    return None


def format_error_location(source, location):
    """Format the error location with a pointer to the exact position."""
    if not source or location.line is None:
        return ""
    
    source_line = get_source_line(source, location.line)
    if not source_line:
        return ""
    
    result = f"{source_line}\n"
    if location.column is not None:
        result += f"{' ' * (location.column - 1)}^"
    
    return result
