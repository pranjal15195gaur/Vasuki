from dataclasses import dataclass
import builtins
from compiler.errors import NameError, TypeError, ValueError, IndexError, KeyError, DivisionByZeroError, RuntimeError

class AST:
    pass


# Dictionary implementation using hash map with buckets for collision resolution
class Dictionary:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.load_factor_threshold = 0.75

    def _hash(self, key):
        # Simple hash function
        if isinstance(key, int):
            return key % self.capacity
        elif isinstance(key, float):
            return int(key) % self.capacity
        elif isinstance(key, str):
            # String hashing using polynomial rolling hash
            h = 0
            for c in key:
                h = (h * 31 + ord(c)) % self.capacity
            return h
        elif isinstance(key, bool):
            return int(key) % self.capacity
        else:
            # For other types, use id as hash
            return id(key) % self.capacity

    def _find_entry(self, key):
        # Find the entry with the given key in the appropriate bucket
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                return bucket_index, i

        return bucket_index, -1

    def _resize(self, new_capacity):
        # Resize the hash map when load factor exceeds threshold
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0

        # Rehash all entries
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def put(self, key, value):
        # Insert or update a key-value pair
        bucket_index, entry_index = self._find_entry(key)

        if entry_index >= 0:
            # Update existing entry
            self.buckets[bucket_index][entry_index] = (key, value)
        else:
            # Insert new entry
            self.buckets[bucket_index].append((key, value))
            self.size += 1

            # Check if resize is needed
            if self.size / self.capacity > self.load_factor_threshold:
                self._resize(self.capacity * 2)

    def get(self, key, default=None):
        # Get the value for a key, or default if key not found
        bucket_index, entry_index = self._find_entry(key)

        if entry_index >= 0:
            return self.buckets[bucket_index][entry_index][1]
        else:
            return default

    def contains(self, key):
        # Check if the dictionary contains a key
        _, entry_index = self._find_entry(key)
        return entry_index >= 0

    def remove(self, key):
        # Remove a key-value pair
        bucket_index, entry_index = self._find_entry(key)

        if entry_index >= 0:
            # Remove the entry
            del self.buckets[bucket_index][entry_index]
            self.size -= 1
            return True
        else:
            return False

    def keys(self):
        # Get all keys
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result

    def values(self):
        # Get all values
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result

    def items(self):
        # Get all key-value pairs
        result = []
        for bucket in self.buckets:
            for key, value in bucket:
                result.append((key, value))
        return result

    def clear(self):
        # Clear the dictionary
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def __str__(self):
        # String representation
        items = []
        for bucket in self.buckets:
            for key, value in bucket:
                items.append(f"{repr(key)}: {repr(value)}")
        return "{" + ", ".join(items) + "}"

# Global registry for dynamic variables and functions
dynamic_variables = {}
dynamic_functions = {}

# List of built-in functions
BUILTIN_FUNCTIONS = [
    "max", "min", "push", "pop", "length", "substring", "uppercase", "lowercase",
    "contains", "startswith", "endswith", "replace", "trim", "split",
    "is_int", "is_float", "is_string", "is_char", "is_bool", "is_array", "is_function",
    "get_type", "to_int", "to_float", "to_string", "to_bool",
    "dict", "dict_put", "dict_get", "dict_contains", "dict_remove", "dict_keys",
    "dict_values", "dict_items", "dict_size", "dict_clear", "is_dict",
    "read_line", "read_int", "read_ints", "read_float", "read_floats", "read_lines", "read_all"
]

# Environment class supporting both static and dynamic scoping
class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}
        self.variables = {}
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
        # If not found in dynamic functions, check built-in functions
        elif name in BUILTIN_FUNCTIONS:
            # Return a special marker to indicate this is a built-in function
            # The actual function will be handled in the FunctionCall case
            return "__builtin__"
        else:
            raise NameError(f"Variable or function '{name}' is not defined")
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
            raise NameError(f"Cannot assign to '{name}': variable or function is not defined")
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
class Boolean(AST):
    val: bool

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
class DictLiteral(AST):
    keys: list[AST]
    values: list[AST]

@dataclass
class DictGet(AST):
    dict_expr: AST
    key: AST

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
        case Boolean(v):
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
                    if right_val == 0:
                        raise DivisionByZeroError("Division by zero")
                    if isinstance(left_val, int) and isinstance(right_val, int) and left_val % right_val == 0:
                        return left_val // right_val
                    return left_val / right_val
                case "%":
                    if right_val == 0:
                        raise DivisionByZeroError("Modulo by zero")
                    return left_val % right_val
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
                case _: raise TypeError(f"Unsupported binary operator: '{op}'")

        case Parentheses(expp):
            return e(expp, env)
        case If(cond, then, elseif_branches, elsee):
            if cond is None:
                raise SyntaxError("Condition missing in 'if' statement")
            for i, (elseif_cond, _) in enumerate(elseif_branches):
                if elseif_cond is None:
                    raise SyntaxError(f"Condition missing in 'elseif' branch {i+1}")
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
            if func == "__builtin__":
                # Handle built-in functions directly
                if name == "max":
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
                # Type checker functions
                elif name == "is_int":
                    # Check if a value is an integer
                    if len(evaluated_args) != 1:
                        raise ValueError("is_int expects one argument: is_int(value)")
                    return isinstance(evaluated_args[0], int) and not isinstance(evaluated_args[0], bool)
                elif name == "is_float":
                    # Check if a value is a floating-point number
                    if len(evaluated_args) != 1:
                        raise ValueError("is_float expects one argument: is_float(value)")
                    return isinstance(evaluated_args[0], float)
                elif name == "is_string":
                    # Check if a value is a string
                    if len(evaluated_args) != 1:
                        raise ValueError("is_string expects one argument: is_string(value)")
                    return isinstance(evaluated_args[0], str)
                elif name == "is_char":
                    # Check if a value is a single character (a string of length 1)
                    if len(evaluated_args) != 1:
                        raise ValueError("is_char expects one argument: is_char(value)")
                    return isinstance(evaluated_args[0], str) and len(evaluated_args[0]) == 1
                elif name == "is_bool":
                    # Check if a value is a boolean
                    if len(evaluated_args) != 1:
                        raise ValueError("is_bool expects one argument: is_bool(value)")
                    return isinstance(evaluated_args[0], bool)
                elif name == "is_array":
                    # Check if a value is an array
                    if len(evaluated_args) != 1:
                        raise ValueError("is_array expects one argument: is_array(value)")
                    return isinstance(evaluated_args[0], list)
                elif name == "is_function":
                    # Check if a value is a function
                    if len(evaluated_args) != 1:
                        raise ValueError("is_function expects one argument: is_function(value)")
                    return isinstance(evaluated_args[0], UserFunction)
                elif name == "get_type":
                    # Return the type of a value as a string
                    if len(evaluated_args) != 1:
                        raise ValueError("get_type expects one argument: get_type(value)")
                    value = evaluated_args[0]
                    if isinstance(value, int) and not isinstance(value, bool):
                        return "int"
                    elif isinstance(value, float):
                        return "float"
                    elif isinstance(value, str):
                        if len(value) == 1:
                            return "char"
                        else:
                            return "string"
                    elif isinstance(value, bool):
                        return "bool"
                    elif isinstance(value, list):
                        return "array"
                    elif isinstance(value, Dictionary):
                        return "dict"
                    elif isinstance(value, UserFunction):
                        return "function"
                    else:
                        return "unknown"
                elif name == "to_int":
                    # Convert a value to an integer if possible
                    if len(evaluated_args) != 1:
                        raise ValueError("to_int expects one argument: to_int(value)")
                    value = evaluated_args[0]
                    try:
                        if isinstance(value, bool):
                            return 1 if value else 0
                        return int(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Cannot convert {value} to int")
                elif name == "to_float":
                    # Convert a value to a float if possible
                    if len(evaluated_args) != 1:
                        raise ValueError("to_float expects one argument: to_float(value)")
                    value = evaluated_args[0]
                    try:
                        if isinstance(value, bool):
                            return 1.0 if value else 0.0
                        return float(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Cannot convert {value} to float")
                elif name == "to_string":
                    # Convert a value to a string
                    if len(evaluated_args) != 1:
                        raise ValueError("to_string expects one argument: to_string(value)")
                    return str(evaluated_args[0])
                elif name == "to_bool":
                    # Convert a value to a boolean
                    if len(evaluated_args) != 1:
                        raise ValueError("to_bool expects one argument: to_bool(value)")
                    value = evaluated_args[0]
                    if isinstance(value, bool):
                        return value
                    elif isinstance(value, (int, float)):
                        return value != 0
                    elif isinstance(value, str):
                        return len(value) > 0
                    elif isinstance(value, list):
                        return len(value) > 0
                    elif isinstance(value, Dictionary):
                        return value.size > 0
                    else:
                        return True  # Functions and other objects are truthy
                # Dictionary functions
                elif name == "dict":
                    # Create a new dictionary
                    return Dictionary()
                elif name == "dict_put":
                    # Add or update a key-value pair in a dictionary
                    if len(evaluated_args) != 3:
                        raise ValueError("dict_put expects three arguments: dict_put(dict, key, value)")
                    dict_obj, key, value = evaluated_args
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_put: first argument must be a dictionary")
                    dict_obj.put(key, value)
                    return dict_obj
                elif name == "dict_get":
                    # Get a value from a dictionary
                    if len(evaluated_args) not in [2, 3]:
                        raise ValueError("dict_get expects 2 or 3 arguments: dict_get(dict, key[, default])")
                    dict_obj = evaluated_args[0]
                    key = evaluated_args[1]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_get: first argument must be a dictionary")
                    if len(evaluated_args) == 3:
                        default = evaluated_args[2]
                        return dict_obj.get(key, default)
                    else:
                        return dict_obj.get(key)
                elif name == "dict_contains":
                    # Check if a dictionary contains a key
                    if len(evaluated_args) != 2:
                        raise ValueError("dict_contains expects two arguments: dict_contains(dict, key)")
                    dict_obj, key = evaluated_args
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_contains: first argument must be a dictionary")
                    return dict_obj.contains(key)
                elif name == "dict_remove":
                    # Remove a key-value pair from a dictionary
                    if len(evaluated_args) != 2:
                        raise ValueError("dict_remove expects two arguments: dict_remove(dict, key)")
                    dict_obj, key = evaluated_args
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_remove: first argument must be a dictionary")
                    return dict_obj.remove(key)
                elif name == "dict_keys":
                    # Get all keys from a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("dict_keys expects one argument: dict_keys(dict)")
                    dict_obj = evaluated_args[0]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_keys: argument must be a dictionary")
                    return dict_obj.keys()
                elif name == "dict_values":
                    # Get all values from a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("dict_values expects one argument: dict_values(dict)")
                    dict_obj = evaluated_args[0]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_values: argument must be a dictionary")
                    return dict_obj.values()
                elif name == "dict_items":
                    # Get all key-value pairs from a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("dict_items expects one argument: dict_items(dict)")
                    dict_obj = evaluated_args[0]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_items: argument must be a dictionary")
                    return dict_obj.items()
                elif name == "dict_size":
                    # Get the number of key-value pairs in a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("dict_size expects one argument: dict_size(dict)")
                    dict_obj = evaluated_args[0]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_size: argument must be a dictionary")
                    return dict_obj.size
                elif name == "dict_clear":
                    # Clear a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("dict_clear expects one argument: dict_clear(dict)")
                    dict_obj = evaluated_args[0]
                    if not isinstance(dict_obj, Dictionary):
                        raise ValueError("dict_clear: argument must be a dictionary")
                    dict_obj.clear()
                    return dict_obj
                elif name == "is_dict":
                    # Check if a value is a dictionary
                    if len(evaluated_args) != 1:
                        raise ValueError("is_dict expects one argument: is_dict(value)")
                    return isinstance(evaluated_args[0], Dictionary)
                # Input/Output functions
                elif name == "read_line":
                    # Read a line from stdin
                    if len(evaluated_args) != 0:
                        raise ValueError("read_line expects no arguments")
                    try:
                        return input()
                    except EOFError:
                        return ""
                elif name == "read_int":
                    # Read a single integer from stdin
                    if len(evaluated_args) != 0:
                        raise ValueError("read_int expects no arguments")
                    try:
                        return int(input())
                    except ValueError:
                        raise ValueError("Input could not be converted to an integer")
                    except EOFError:
                        raise ValueError("End of file reached")
                elif name == "read_ints":
                    # Read multiple integers from a line
                    if len(evaluated_args) != 0:
                        raise ValueError("read_ints expects no arguments")
                    try:
                        return [int(x) for x in input().split()]
                    except ValueError:
                        raise ValueError("Input could not be converted to integers")
                    except EOFError:
                        return []
                elif name == "read_float":
                    # Read a single float from stdin
                    if len(evaluated_args) != 0:
                        raise ValueError("read_float expects no arguments")
                    try:
                        return float(input())
                    except ValueError:
                        raise ValueError("Input could not be converted to a float")
                    except EOFError:
                        raise ValueError("End of file reached")
                elif name == "read_floats":
                    # Read multiple floats from a line
                    if len(evaluated_args) != 0:
                        raise ValueError("read_floats expects no arguments")
                    try:
                        return [float(x) for x in input().split()]
                    except ValueError:
                        raise ValueError("Input could not be converted to floats")
                    except EOFError:
                        return []
                elif name == "read_lines":
                    # Read n lines from stdin
                    if len(evaluated_args) != 1:
                        raise ValueError("read_lines expects one argument: read_lines(n)")
                    n = evaluated_args[0]
                    if not isinstance(n, int):
                        raise ValueError("read_lines: argument must be an integer")
                    if n < 0:
                        raise ValueError("read_lines: argument must be non-negative")
                    lines = []
                    for _ in range(n):
                        try:
                            lines.append(input())
                        except EOFError:
                            break
                    return lines
                elif name == "read_all":
                    # Read all lines until EOF
                    if len(evaluated_args) != 0:
                        raise ValueError("read_all expects no arguments")
                    lines = []
                    while True:
                        try:
                            lines.append(input())
                        except EOFError:
                            break
                    return lines
                # If we get here, it's a built-in function we haven't handled yet
                # This should never happen if BUILTIN_FUNCTIONS is kept in sync
                else:
                    raise ValueError(f"Unknown built-in function {name}")
            elif func is not None and isinstance(func, UserFunction):
                if len(evaluated_args) != len(func.params):
                    raise TypeError(f"Function '{name}' expects {len(func.params)} arguments, but got {len(evaluated_args)}")
                new_env = Environment(func.closure)
                for param, arg in zip(func.params, evaluated_args):
                    new_env.declare(param, arg)
                try:
                    return e(func.body, new_env)
                except ReturnException as re:
                    # Both return and yield statements return from the function
                    return re.value
            # All built-in functions are now handled in the __builtin__ case above
            else:
                raise ValueError(f"Unknown function {name}")
        case Return(expr):
            # When a return is encountered, evaluate the expression and raise an exception to exit the current block.
            raise ReturnException(e(expr, env), is_yield=False)

        case Yield(expr):
            # When a yield is encountered, evaluate the expression and raise an exception to exit the entire function.
            raise ReturnException(e(expr, env), is_yield=True)

        # New evaluation rules for arrays, strings, and dictionaries
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
        case DictLiteral(keys, values):
            if len(keys) != len(values):
                raise ValueError("Number of keys must match number of values in dictionary literal")
            dict_obj = Dictionary()
            for i in range(len(keys)):
                key = e(keys[i], env)
                value = e(values[i], env)
                dict_obj.put(key, value)
            return dict_obj
        case DictGet(dict_expr, key):
            dict_obj = e(dict_expr, env)
            key_val = e(key, env)
            if not isinstance(dict_obj, Dictionary):
                raise ValueError(f"Cannot get key from a {type(dict_obj).__name__} value")
            return dict_obj.get(key_val)



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
