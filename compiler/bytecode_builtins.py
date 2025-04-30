# bytecode_builtins.py
# Implements the built-in functions for the bytecode VM

import time
import random as py_random
from bytecode_extended import OC, BytecodeVM

# Initialize the random seed with current time for true randomness
py_random.seed(int(time.time()))

# Dictionary mapping built-in function names to their implementations
BUILTIN_FUNCTIONS = {
    # Array operations
    "push": lambda vm, args: handle_push(vm, args),
    "pop": lambda vm, args: handle_pop(vm, args),
    "length": lambda vm, args: handle_length(vm, args),

    # String operations
    "substring": lambda vm, args: handle_substring(vm, args),
    "uppercase": lambda vm, args: handle_uppercase(vm, args),
    "lowercase": lambda vm, args: handle_lowercase(vm, args),
    "contains": lambda vm, args: handle_contains(vm, args),
    "startswith": lambda vm, args: handle_startswith(vm, args),
    "endswith": lambda vm, args: handle_endswith(vm, args),
    "replace": lambda vm, args: handle_replace(vm, args),
    "trim": lambda vm, args: handle_trim(vm, args),
    "split": lambda vm, args: handle_split(vm, args),

    # Type checking
    "is_int": lambda vm, args: handle_is_type(vm, args, "int"),
    "is_float": lambda vm, args: handle_is_type(vm, args, "float"),
    "is_string": lambda vm, args: handle_is_type(vm, args, "string"),
    "is_bool": lambda vm, args: handle_is_type(vm, args, "bool"),
    "is_array": lambda vm, args: handle_is_type(vm, args, "array"),
    "is_dict": lambda vm, args: handle_is_type(vm, args, "dict"),
    "is_function": lambda vm, args: handle_is_type(vm, args, "function"),
    "get_type": lambda vm, args: handle_get_type(vm, args),

    # Type conversion
    "to_int": lambda vm, args: handle_to_type(vm, args, "int"),
    "to_float": lambda vm, args: handle_to_type(vm, args, "float"),
    "to_string": lambda vm, args: handle_to_type(vm, args, "string"),
    "to_bool": lambda vm, args: handle_to_type(vm, args, "bool"),

    # Dictionary operations
    "dict": lambda vm, args: handle_dict_create(vm, args),
    "dict_put": lambda vm, args: handle_dict_put(vm, args),
    "dict_get": lambda vm, args: handle_dict_get(vm, args),
    "dict_contains": lambda vm, args: handle_dict_contains(vm, args),
    "dict_remove": lambda vm, args: handle_dict_remove(vm, args),
    "dict_keys": lambda vm, args: handle_dict_keys(vm, args),
    "dict_values": lambda vm, args: handle_dict_values(vm, args),
    "dict_items": lambda vm, args: handle_dict_items(vm, args),
    "dict_size": lambda vm, args: handle_dict_size(vm, args),
    "dict_clear": lambda vm, args: handle_dict_clear(vm, args),

    # I/O operations
    "read_line": lambda vm, args: handle_read(vm, args, "line"),
    "read_int": lambda vm, args: handle_read(vm, args, "int"),
    "read_float": lambda vm, args: handle_read(vm, args, "float"),
    "read_ints": lambda vm, args: handle_read_multiple(vm, args, "int"),
    "read_floats": lambda vm, args: handle_read_multiple(vm, args, "float"),
    "read_lines": lambda vm, args: handle_read_multiple(vm, args, "line"),
    "read_all": lambda vm, args: handle_read_all(vm, args),

    # Math operations
    "max": lambda vm, args: max(args),
    "min": lambda vm, args: min(args),

    # Random number generation
    "random": lambda vm, args: handle_random(vm, args),
    "random_int": lambda vm, args: handle_random_int(vm, args),
    "random_float": lambda vm, args: handle_random_float(vm, args),
    "random_range": lambda vm, args: handle_random_range(vm, args),
    "random_choice": lambda vm, args: handle_random_choice(vm, args),
    "random_seed": lambda vm, args: handle_random_seed(vm, args),
}

# Helper functions for built-in function implementations

def handle_push(vm, args):
    if len(args) != 2:
        raise ValueError("push() requires 2 arguments: array and element")
    array, element = args
    if not isinstance(array, list):
        raise TypeError(f"First argument to push() must be an array, got {type(array)}")
    array.append(element)
    return array

def handle_pop(vm, args):
    if len(args) != 1:
        raise ValueError("pop() requires 1 argument: array")
    array = args[0]
    if not isinstance(array, list):
        raise TypeError(f"Argument to pop() must be an array, got {type(array)}")
    if not array:
        raise ValueError("Cannot pop from an empty array")
    return array.pop()

def handle_length(vm, args):
    if len(args) != 1:
        raise ValueError("length() requires 1 argument: collection")
    collection = args[0]
    if isinstance(collection, list):
        return len(collection)
    elif isinstance(collection, str):
        return len(collection)
    elif hasattr(collection, "size"):
        return collection.size
    else:
        raise TypeError(f"Cannot get length of {type(collection)}")

def handle_substring(vm, args):
    if len(args) < 2 or len(args) > 3:
        raise ValueError("substring() requires 2 or 3 arguments: string, start, [length]")
    string = args[0]
    start = args[1]
    if not isinstance(string, str):
        raise TypeError(f"First argument to substring() must be a string, got {type(string)}")
    if not isinstance(start, int):
        raise TypeError(f"Second argument to substring() must be an integer, got {type(start)}")
    if len(args) == 3:
        length = args[2]
        if not isinstance(length, int):
            raise TypeError(f"Third argument to substring() must be an integer, got {type(length)}")
        return string[start:start+length]
    else:
        return string[start:]

def handle_uppercase(vm, args):
    if len(args) != 1:
        raise ValueError("uppercase() requires 1 argument: string")
    string = args[0]
    if not isinstance(string, str):
        raise TypeError(f"Argument to uppercase() must be a string, got {type(string)}")
    return string.upper()

def handle_lowercase(vm, args):
    if len(args) != 1:
        raise ValueError("lowercase() requires 1 argument: string")
    string = args[0]
    if not isinstance(string, str):
        raise TypeError(f"Argument to lowercase() must be a string, got {type(string)}")
    return string.lower()

def handle_contains(vm, args):
    if len(args) != 2:
        raise ValueError("contains() requires 2 arguments: string/array/dict, element/substring/key")
    collection, element = args
    if isinstance(collection, str):
        if not isinstance(element, str):
            raise TypeError(f"Second argument to contains() must be a string when first argument is a string, got {type(element)}")
        return element in collection
    elif isinstance(collection, list):
        return element in collection
    elif hasattr(collection, "contains"):
        return collection.contains(element)
    else:
        raise TypeError(f"First argument to contains() must be a string, array, or dictionary, got {type(collection)}")

def handle_startswith(vm, args):
    if len(args) != 2:
        raise ValueError("startswith() requires 2 arguments: string, prefix")
    string, prefix = args
    if not isinstance(string, str):
        raise TypeError(f"First argument to startswith() must be a string, got {type(string)}")
    if not isinstance(prefix, str):
        raise TypeError(f"Second argument to startswith() must be a string, got {type(prefix)}")
    return string.startswith(prefix)

def handle_endswith(vm, args):
    if len(args) != 2:
        raise ValueError("endswith() requires 2 arguments: string, suffix")
    string, suffix = args
    if not isinstance(string, str):
        raise TypeError(f"First argument to endswith() must be a string, got {type(string)}")
    if not isinstance(suffix, str):
        raise TypeError(f"Second argument to endswith() must be a string, got {type(suffix)}")
    return string.endswith(suffix)

def handle_replace(vm, args):
    if len(args) != 3:
        raise ValueError("replace() requires 3 arguments: string, old, new")
    string, old, new = args
    if not isinstance(string, str):
        raise TypeError(f"First argument to replace() must be a string, got {type(string)}")
    if not isinstance(old, str):
        raise TypeError(f"Second argument to replace() must be a string, got {type(old)}")
    if not isinstance(new, str):
        raise TypeError(f"Third argument to replace() must be a string, got {type(new)}")
    return string.replace(old, new)

def handle_trim(vm, args):
    if len(args) != 1:
        raise ValueError("trim() requires 1 argument: string")
    string = args[0]
    if not isinstance(string, str):
        raise TypeError(f"Argument to trim() must be a string, got {type(string)}")
    return string.strip()

def handle_split(vm, args):
    if len(args) != 2:
        raise ValueError("split() requires 2 arguments: string, delimiter")
    string, delimiter = args
    if not isinstance(string, str):
        raise TypeError(f"First argument to split() must be a string, got {type(string)}")
    if not isinstance(delimiter, str):
        raise TypeError(f"Second argument to split() must be a string, got {type(delimiter)}")
    return string.split(delimiter)

def handle_is_type(vm, args, type_name):
    if len(args) != 1:
        raise ValueError(f"is_{type_name}() requires 1 argument: value")
    value = args[0]
    vm.stack.append(value)
    vm.stack.append(type_name)
    vm.bytecode.add(OC.TYPE_CHECK, type_name)
    return vm.stack.pop()

def handle_get_type(vm, args):
    if len(args) != 1:
        raise ValueError("get_type() requires 1 argument: value")
    value = args[0]
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, list):
        return "array"
    elif hasattr(value, "items"):  # Dictionary-like
        return "dict"
    elif hasattr(value, "params"):  # Function-like
        return "function"
    else:
        return "unknown"

def handle_to_type(vm, args, type_name):
    if len(args) != 1:
        raise ValueError(f"to_{type_name}() requires 1 argument: value")
    value = args[0]
    vm.stack.append(value)
    vm.bytecode.add(OC.TYPE_CONVERT, type_name)
    return vm.stack.pop()

def handle_dict_create(vm, args):
    if len(args) != 0:
        raise ValueError("dict() requires 0 arguments")
    vm.bytecode.add(OC.DICT, 0)
    return vm.stack.pop()

def handle_dict_put(vm, args):
    if len(args) != 3:
        raise ValueError("dict_put() requires 3 arguments: dict, key, value")
    dict_obj, key, value = args
    if not hasattr(dict_obj, "put"):
        raise TypeError(f"First argument to dict_put() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.stack.append(key)
    vm.stack.append(value)
    vm.bytecode.add(OC.DICT_SET)
    return vm.stack.pop()

def handle_dict_get(vm, args):
    if len(args) != 2:
        raise ValueError("dict_get() requires 2 arguments: dict, key")
    dict_obj, key = args
    if not hasattr(dict_obj, "get"):
        raise TypeError(f"First argument to dict_get() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.stack.append(key)
    vm.bytecode.add(OC.DICT_GET)
    return vm.stack.pop()

def handle_dict_contains(vm, args):
    if len(args) != 2:
        raise ValueError("dict_contains() requires 2 arguments: dict, key")
    dict_obj, key = args
    if not hasattr(dict_obj, "contains"):
        raise TypeError(f"First argument to dict_contains() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.stack.append(key)
    vm.bytecode.add(OC.DICT_CONTAINS)
    return vm.stack.pop()

def handle_dict_remove(vm, args):
    if len(args) != 2:
        raise ValueError("dict_remove() requires 2 arguments: dict, key")
    dict_obj, key = args
    if not hasattr(dict_obj, "remove"):
        raise TypeError(f"First argument to dict_remove() must be a dictionary, got {type(dict_obj)}")
    return dict_obj.remove(key)

def handle_dict_keys(vm, args):
    if len(args) != 1:
        raise ValueError("dict_keys() requires 1 argument: dict")
    dict_obj = args[0]
    if not hasattr(dict_obj, "keys"):
        raise TypeError(f"Argument to dict_keys() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.bytecode.add(OC.DICT_KEYS)
    return vm.stack.pop()

def handle_dict_values(vm, args):
    if len(args) != 1:
        raise ValueError("dict_values() requires 1 argument: dict")
    dict_obj = args[0]
    if not hasattr(dict_obj, "values"):
        raise TypeError(f"Argument to dict_values() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.bytecode.add(OC.DICT_VALUES)
    return vm.stack.pop()

def handle_dict_items(vm, args):
    if len(args) != 1:
        raise ValueError("dict_items() requires 1 argument: dict")
    dict_obj = args[0]
    if not hasattr(dict_obj, "items"):
        raise TypeError(f"Argument to dict_items() must be a dictionary, got {type(dict_obj)}")
    vm.stack.append(dict_obj)
    vm.bytecode.add(OC.DICT_ITEMS)
    return vm.stack.pop()

def handle_dict_size(vm, args):
    if len(args) != 1:
        raise ValueError("dict_size() requires 1 argument: dict")
    dict_obj = args[0]
    if not hasattr(dict_obj, "size"):
        raise TypeError(f"Argument to dict_size() must be a dictionary, got {type(dict_obj)}")
    return dict_obj.size

def handle_dict_clear(vm, args):
    if len(args) != 1:
        raise ValueError("dict_clear() requires 1 argument: dict")
    dict_obj = args[0]
    if not hasattr(dict_obj, "clear"):
        raise TypeError(f"Argument to dict_clear() must be a dictionary, got {type(dict_obj)}")
    dict_obj.clear()
    return dict_obj

def handle_read(vm, args, read_type):
    if len(args) != 0:
        raise ValueError(f"read_{read_type}() requires 0 arguments")
    vm.bytecode.add(OC.READ, read_type)
    return vm.stack.pop()

def handle_read_multiple(vm, args, read_type):
    if len(args) != 1:
        raise ValueError(f"read_{read_type}s() requires 1 argument: count")
    count = args[0]
    if not isinstance(count, int):
        raise TypeError(f"Argument to read_{read_type}s() must be an integer, got {type(count)}")
    result = []
    for _ in range(count):
        vm.bytecode.add(OC.READ, read_type)
        result.append(vm.stack.pop())
    return result

def handle_read_all(vm, args):
    if len(args) != 0:
        raise ValueError("read_all() requires 0 arguments")
    result = []
    try:
        while True:
            vm.bytecode.add(OC.READ, "line")
            line = vm.stack.pop()
            if not line:
                break
            result.append(line)
    except EOFError:
        pass
    return result

# Random number generation functions

def handle_random(vm, args):
    """Generate a random float between 0 and 1"""
    if len(args) != 0:
        raise ValueError("random() requires 0 arguments")
    return py_random.random()

def handle_random_int(vm, args):
    """Generate a random integer between 0 and 2^31-1"""
    if len(args) != 0:
        raise ValueError("random_int() requires 0 arguments")
    return py_random.randint(0, 2**31-1)

def handle_random_float(vm, args):
    """Generate a random float between 0 and 1"""
    if len(args) != 0:
        raise ValueError("random_float() requires 0 arguments")
    return py_random.random()

def handle_random_range(vm, args):
    """Generate a random integer between min and max (inclusive)"""
    if len(args) != 2:
        raise ValueError("random_range() requires 2 arguments: min, max")
    min_val, max_val = args
    if not isinstance(min_val, int):
        raise TypeError(f"First argument to random_range() must be an integer, got {type(min_val)}")
    if not isinstance(max_val, int):
        raise TypeError(f"Second argument to random_range() must be an integer, got {type(max_val)}")
    return py_random.randint(min_val, max_val)

def handle_random_choice(vm, args):
    """Randomly select an element from an array"""
    if len(args) != 1:
        raise ValueError("random_choice() requires 1 argument: array")
    array = args[0]
    if not isinstance(array, list):
        raise TypeError(f"Argument to random_choice() must be an array, got {type(array)}")
    if not array:
        raise ValueError("Cannot choose from an empty array")
    # Vasuki uses 1-based indexing, but Python uses 0-based indexing
    # So we need to adjust the indices
    return array[py_random.randint(0, len(array)-1)]

def handle_random_seed(vm, args):
    """Set the random seed"""
    if len(args) != 1:
        raise ValueError("random_seed() requires 1 argument: seed")
    seed = args[0]
    if not isinstance(seed, int):
        raise TypeError(f"Argument to random_seed() must be an integer, got {type(seed)}")
    py_random.seed(seed)
    return seed

# Extend the BytecodeVM class to handle built-in functions
def handle_builtin_function(vm, name, args):
    if name in BUILTIN_FUNCTIONS:
        return BUILTIN_FUNCTIONS[name](vm, args)
    else:
        raise ValueError(f"Unknown built-in function: {name}")

# Monkey patch the BytecodeVM class to handle built-in functions
original_run = BytecodeVM.run

def patched_run(self):
    # Store the original method
    self.handle_builtin_function = lambda name, args: handle_builtin_function(self, name, args)

    # Call the original method
    return original_run(self)

BytecodeVM.run = patched_run
