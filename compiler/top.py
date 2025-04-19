from dataclasses import dataclass
import builtins

class AST:
    pass

# Global registry for dynamic variables and functions
dynamic_variables = {}
dynamic_functions = {}

# Environment class supporting both static and dynamic scoping
class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}
    def lookup(self, name):
        # First try to find in static scope
        if name in self.values:
            return self.values[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        # If not found in static scope, check dynamic scope
        elif name in dynamic_variables:
            return dynamic_variables[name]
        # If not found in dynamic variables, check dynamic functions
        elif name in dynamic_functions:
            return dynamic_functions[name]
        else:
            raise ValueError(f"Variable or function {name} not defined")
    def assign(self, name, value):
        # First try to assign in static scope
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        # If not found in static scope, check dynamic scope
        elif name in dynamic_variables:
            dynamic_variables[name] = value
        # If not found in dynamic variables, check dynamic functions
        elif name in dynamic_functions:
            dynamic_functions[name] = value
        else:
            raise ValueError(f"Variable or function {name} not defined")
    def declare(self, name, value):
        self.values[name] = value
    def declare_dynamic(self, name, value):
        # Dynamic variables are stored in the global registry
        dynamic_variables[name] = value
    def declare_dynamic_function(self, name, value):
        # Dynamic functions are stored in the global registry
        dynamic_functions[name] = value

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class UnOp(AST):
    op: str
    num: AST

@dataclass
class Float(AST):
    val: str

@dataclass
class Int(AST):
    val: str

@dataclass
class String(AST):
    val: str

@dataclass
class Parentheses(AST):
    val: AST

@dataclass
class If(AST):
    cond: AST
    then: AST
    elseif_branches: list[tuple[AST, AST]]
    elsee: AST

@dataclass
class VarDecl(AST):
    name: str
    value: AST

@dataclass
class DynamicVarDecl(AST):
    name: str
    value: AST

@dataclass
class VarReference(AST):
    name: str

@dataclass
class Assignment(AST):
    name: str
    value: AST

@dataclass
class Program(AST):
    statements: list[AST]

@dataclass
class For(AST):
    init: AST
    condition: AST
    increment: AST
    body: AST

@dataclass
class While(AST):
    condition: AST
    body: AST

@dataclass
class Print(AST):
    expr: AST

@dataclass
class FunctionCall(AST):
    name: str
    args: list[AST]

@dataclass
class Label(AST):
    name: str

@dataclass
class LabelReturn(AST):
    name: str

@dataclass
class GoAndReturn(AST):
    name: str

# New AST nodes for arrays
@dataclass
class ArrayLiteral(AST):
    elements: list[AST]

@dataclass
class ArrayIndex(AST):
    array: AST
    index: AST

@dataclass
class StringIndex(AST):
    string: AST
    index: AST

@dataclass
class FunctionDef(AST):
    name: str
    params: list[str]
    body: AST

@dataclass
class DynamicFunctionDef(AST):
    name: str
    params: list[str]
    body: AST

# A helper to represent a user‐defined function (its parameter names, body, and the closure in which it was defined)
@dataclass
class UserFunction:
    params: list[str]
    body: AST
    closure: Environment

@dataclass
class Return(AST):
    value: AST

@dataclass
class Yield(AST):
    value: AST

class ReturnException(Exception):
    def __init__(self, value, is_yield=False):
        self.value = value
        self.is_yield = is_yield


def e(tree: AST, env=None) -> int:
    if env is None:
        env = Environment()

    match tree:

        case FunctionDef(name, params, body):
            uf = UserFunction(params, body, env)
            env.declare(name, uf)
            return uf

        case DynamicFunctionDef(name, params, body):
            uf = UserFunction(params, body, env)
            env.declare_dynamic_function(name, uf)
            return uf


        case Program(stmts):
            result = None
            for stmt in stmts:
                result = e(stmt, env)
            return result

        case VarDecl(name, value):
            result = e(value, env)
            env.declare(name, result)
            return result

        case DynamicVarDecl(name, value):
            result = e(value, env)
            env.declare_dynamic(name, result)
            return result

        case Assignment(name, value):
            result = e(value, env)
            env.assign(name, result)
            return result

        case VarReference(name):
            return env.lookup(name)
        case Int(v):
            return int(v)
        case Float(v):
            return float(v)
        case String(v):
            return v
        case UnOp("-", expp):
            return -1 * e(expp, env)

        case BinOp(op, l, r):
            left_val = e(l, env)
            right_val = e(r, env)
            match op:
                case "**": return left_val ** right_val
                case "*": return left_val * right_val
                case "/":
                    if isinstance(left_val, int) and left_val % right_val == 0:
                        return left_val // right_val
                    return left_val / right_val
                case "%": return left_val % right_val
                case "+":
                    # Handle string concatenation
                    if isinstance(left_val, str) or isinstance(right_val, str):
                        return str(left_val) + str(right_val)
                    return left_val + right_val
                case "-": return left_val - right_val
                case "<": return left_val < right_val
                case "<=": return left_val <= right_val
                case ">": return left_val > right_val
                case ">=": return left_val >= right_val
                case "==": return left_val == right_val
                case "!=": return left_val != right_val
                case "and": return (left_val and right_val)
                case "or": return (left_val or right_val)
                case _: raise ValueError(f"Unsupported binary operator: {op}")

        case Parentheses(expp):
            return e(expp, env)

        case If(cond, then, elseif_branches, elsee):
            if cond is None:
                raise ValueError("Condition missing in 'if' statement")
            for elseif_cond, _ in elseif_branches:
                if elseif_cond is None:
                    raise ValueError("Condition missing in 'elseif' statement")
            if e(cond, env):
                try:
                    return e(then, Environment(env))
                except ReturnException as re:
                    if re.is_yield:
                        # Yield statements exit the entire function
                        raise  # Re-raise the exception to be caught by the function call
                    else:
                        # Return statements exit the conditional
                        return re.value
            for elseif_cond, elseif_then in elseif_branches:
                if e(elseif_cond, env):
                    try:
                        return e(elseif_then, Environment(env))
                    except ReturnException as re:
                        if re.is_yield:
                            # Yield statements exit the entire function
                            raise  # Re-raise the exception to be caught by the function call
                        else:
                            # Return statements exit the conditional
                            return re.value
            if elsee is not None:
                try:
                    return e(elsee, Environment(env))
                except ReturnException as re:
                    if re.is_yield:
                        # Yield statements exit the entire function
                        raise  # Re-raise the exception to be caught by the function call
                    else:
                        # Return statements exit the conditional
                        return re.value
            return None

        case For(init, condition, increment, body):
            e(init, env)
            result = None
            while e(condition, env):
                try:
                    result = e(body, Environment(env))
                except ReturnException as re:
                    if re.is_yield:
                        # Yield statements exit the entire function
                        raise  # Re-raise the exception to be caught by the function call
                    else:
                        # Return statements exit the loop
                        return re.value
                e(increment, env)
            return result

        case While(condition, body):
            result = None
            while e(condition, env):
                try:
                    result = e(body, env)
                except ReturnException as re:
                    if re.is_yield:
                        # Yield statements exit the entire function
                        raise  # Re-raise the exception to be caught by the function call
                    else:
                        # Return statements exit the loop
                        return re.value
            return result

        case Print(expr):
            value = e(expr, env)
            print(value)
            return value

        case FunctionCall(name, args):
            evaluated_args = [e(a, env) for a in args]
            try:
                func = env.lookup(name)
            except ValueError:
                func = None
            if func is not None and isinstance(func, UserFunction):
                if len(evaluated_args) != len(func.params):
                    raise ValueError(f"Function {name} expects {len(func.params)} arguments, got {len(evaluated_args)}")
                new_env = Environment(func.closure)
                for param, arg in zip(func.params, evaluated_args):
                    new_env.declare(param, arg)
                try:
                    return e(func.body, new_env)
                except ReturnException as re:
                    # Both return and yield statements return from the function
                    return re.value
            elif name == "max":
                return max(*evaluated_args)
            elif name == "min":
                return min(*evaluated_args)
            elif name == "push":
                # Expecting two arguments: the array and the element to push.
                if len(evaluated_args) != 2:
                    raise ValueError("push expects two arguments: push(array, element)")
                arr, value = evaluated_args
                if not isinstance(arr, list):
                    raise ValueError("push: first argument must be an array")
                arr.append(value)
                # Optionally, you can return the modified array or its new length.
                return arr  # or: return len(arr)
            elif name == "pop":
                # Expecting one argument: the array to pop from.
                if len(evaluated_args) != 1:
                    raise ValueError("pop expects one argument: pop(array)")
                arr = evaluated_args[0]
                if not isinstance(arr, list):
                    raise ValueError("pop: argument must be an array")
                if not arr:
                    raise ValueError("pop: cannot pop from an empty array")
                return arr.pop()

            # String functions
            elif name == "length":
                # Get the length of a string or array
                if len(evaluated_args) != 1:
                    raise ValueError("length expects one argument: length(str_or_array)")
                val = evaluated_args[0]
                if not isinstance(val, (str, list)):
                    raise ValueError("length: argument must be a string or array")
                return len(val)

            elif name == "substring":
                # Get a substring: substring(str, start, end)
                if len(evaluated_args) not in [2, 3]:
                    raise ValueError("substring expects 2 or 3 arguments: substring(str, start[, end])")
                s = evaluated_args[0]
                start = evaluated_args[1]
                if not isinstance(s, str):
                    raise ValueError("substring: first argument must be a string")
                if not isinstance(start, int):
                    raise ValueError("substring: second argument must be an integer")
                # Adjust for 1-based indexing
                start = start - 1
                if start < 0 or start >= len(s):
                    raise ValueError(f"substring: start index {start+1} out of range (1 to {len(s)})")
                if len(evaluated_args) == 3:
                    end = evaluated_args[2]
                    if not isinstance(end, int):
                        raise ValueError("substring: third argument must be an integer")
                    # Adjust for 1-based indexing
                    end = end - 1
                    if end < start or end >= len(s):
                        raise ValueError(f"substring: end index {end+1} out of range ({start+1} to {len(s)})")
                    return s[start:end+1]  # Include the end character
                else:
                    return s[start:]

            elif name == "uppercase":
                # Convert a string to uppercase
                if len(evaluated_args) != 1:
                    raise ValueError("uppercase expects one argument: uppercase(str)")
                s = evaluated_args[0]
                if not isinstance(s, str):
                    raise ValueError("uppercase: argument must be a string")
                return s.upper()

            elif name == "lowercase":
                # Convert a string to lowercase
                if len(evaluated_args) != 1:
                    raise ValueError("lowercase expects one argument: lowercase(str)")
                s = evaluated_args[0]
                if not isinstance(s, str):
                    raise ValueError("lowercase: argument must be a string")
                return s.lower()

            elif name == "contains":
                # Check if a string contains a substring
                if len(evaluated_args) != 2:
                    raise ValueError("contains expects two arguments: contains(str, substr)")
                s = evaluated_args[0]
                substr = evaluated_args[1]
                if not isinstance(s, str) or not isinstance(substr, str):
                    raise ValueError("contains: both arguments must be strings")
                return substr in s

            elif name == "startswith":
                # Check if a string starts with a prefix
                if len(evaluated_args) != 2:
                    raise ValueError("startswith expects two arguments: startswith(str, prefix)")
                s = evaluated_args[0]
                prefix = evaluated_args[1]
                if not isinstance(s, str) or not isinstance(prefix, str):
                    raise ValueError("startswith: both arguments must be strings")
                return s.startswith(prefix)

            elif name == "endswith":
                # Check if a string ends with a suffix
                if len(evaluated_args) != 2:
                    raise ValueError("endswith expects two arguments: endswith(str, suffix)")
                s = evaluated_args[0]
                suffix = evaluated_args[1]
                if not isinstance(s, str) or not isinstance(suffix, str):
                    raise ValueError("endswith: both arguments must be strings")
                return s.endswith(suffix)

            elif name == "replace":
                # Replace occurrences of a substring
                if len(evaluated_args) != 3:
                    raise ValueError("replace expects three arguments: replace(str, old, new)")
                s = evaluated_args[0]
                old = evaluated_args[1]
                new = evaluated_args[2]
                if not isinstance(s, str) or not isinstance(old, str) or not isinstance(new, str):
                    raise ValueError("replace: all arguments must be strings")
                return s.replace(old, new)

            elif name == "trim":
                # Remove whitespace from the beginning and end of a string
                if len(evaluated_args) != 1:
                    raise ValueError("trim expects one argument: trim(str)")
                s = evaluated_args[0]
                if not isinstance(s, str):
                    raise ValueError("trim: argument must be a string")
                return s.strip()

            elif name == "split":
                # Split a string by a delimiter
                if len(evaluated_args) not in [1, 2]:
                    raise ValueError("split expects 1 or 2 arguments: split(str[, delimiter])")
                s = evaluated_args[0]
                if not isinstance(s, str):
                    raise ValueError("split: first argument must be a string")
                if len(evaluated_args) == 2:
                    delimiter = evaluated_args[1]
                    if not isinstance(delimiter, str):
                        raise ValueError("split: second argument must be a string")
                    return s.split(delimiter)
                else:
                    return s.split()
            else:
                raise ValueError(f"Unknown function {name}")

        case Return(expr):
            # When a return is encountered, evaluate the expression and raise an exception to exit the current block.
            raise ReturnException(e(expr, env), is_yield=False)

        case Yield(expr):
            # When a yield is encountered, evaluate the expression and raise an exception to exit the entire function.
            raise ReturnException(e(expr, env), is_yield=True)

        # New evaluation rules for arrays and strings
        case ArrayLiteral(elements):
            return [e(el, env) for el in elements]
        case ArrayIndex(array, index):
            arr = e(array, env)
            idx = e(index, env)
            if not isinstance(idx, int):
                raise ValueError("Array index must be an integer")
            # Check if we're indexing a string or an array
            if isinstance(arr, str):
                if idx < 1 or idx > len(arr):
                    raise ValueError(f"String index {idx} out of range (1 to {len(arr)})")
                # One-based indexing: adjust for Python's zero-based strings.
                return arr[idx - 1]
            elif isinstance(arr, list):
                if idx < 1 or idx > len(arr):
                    raise ValueError(f"Array index {idx} out of range (1 to {len(arr)})")
                # One-based indexing: adjust for Python's zero-based lists.
                return arr[idx - 1]
            else:
                raise ValueError(f"Cannot index a {type(arr).__name__} value")
        case StringIndex(string, index):
            s = e(string, env)
            idx = e(index, env)
            if not isinstance(s, str):
                raise ValueError("Cannot index a non-string value")
            if not isinstance(idx, int):
                raise ValueError("String index must be an integer")
            if idx < 1 or idx > len(s):
                raise ValueError(f"String index {idx} out of range (1 to {len(s)})")
            # One-based indexing: adjust for Python's zero-based strings.
            return s[idx - 1]



        case Label(name):
            # Just a marker, do nothing
            return None
        case LabelReturn(name):
            # Also just a marker, do nothing
            return None
        case GoAndReturn(name):
            # Interpret the labeled block again, reusing same env
            labeled_ast = find_label_block(name)
            if not labeled_ast:
                raise ValueError(f"Label {name} not found")
            return run_label_block(labeled_ast, name, env)

        case _:
            raise ValueError("Unsupported node type")


def find_label_block(label_name: str):
    global_program = getattr(builtins, 'global_program', None)
    if not global_program or not isinstance(global_program, Program):
        return None
    return _find_label_block_in(global_program, label_name)

def _find_label_block_in(node: AST, label_name: str):
    # If it's a Program, check each statement, and also recurse within statements
    if isinstance(node, Program):
        in_block = False
        collected = []
        for stmt in node.statements:
            # Start collecting after matching Label
            if isinstance(stmt, Label) and stmt.name == label_name:
                in_block = True
                collected = []
                continue
            # Stop collecting at matching LabelReturn
            if in_block:
                if isinstance(stmt, LabelReturn) and stmt.name == label_name:
                    return collected
                collected.append(stmt)
            # Recurse into nested statements
            found = _find_label_block_in(stmt, label_name)
            if found is not None:
                return found

    # If it's a FunctionDef, recurse into its body
    elif isinstance(node, FunctionDef):
        return _find_label_block_in(node.body, label_name)

    # Otherwise, not found here
    return None

def run_label_block(stmts, label_name, env):
    if not stmts:
        return None
    for stmt in stmts:
        if isinstance(stmt, LabelReturn) and stmt.name == label_name:
            return None
        e(stmt, env)
    return None
