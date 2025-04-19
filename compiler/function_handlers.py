from compiler.data_structures.heap import MinHeap, MaxHeap, PriorityQueue
from compiler.data_structures.set import Set
from compiler.math_functions import *
from compiler.array_operations import *

def handle_priority_queue_functions(name, evaluated_args):
    """Handle priority queue functions."""
    if name == "priority_queue":
        # Create a new priority queue
        if len(evaluated_args) not in [0, 1]:
            raise ValueError("priority_queue expects 0 or 1 arguments: priority_queue([is_min])")
        is_min = True
        if len(evaluated_args) == 1:
            is_min = bool(evaluated_args[0])
        return PriorityQueue(is_min)
    elif name == "priority_queue_enqueue":
        # Add an item to the priority queue
        if len(evaluated_args) != 2:
            raise ValueError("priority_queue_enqueue expects 2 arguments: priority_queue_enqueue(queue, item)")
        queue, item = evaluated_args
        if not isinstance(queue, PriorityQueue):
            raise ValueError("priority_queue_enqueue: first argument must be a priority queue")
        queue.enqueue(item)
        return queue
    elif name == "priority_queue_dequeue":
        # Remove and return the highest-priority item
        if len(evaluated_args) != 1:
            raise ValueError("priority_queue_dequeue expects 1 argument: priority_queue_dequeue(queue)")
        queue = evaluated_args[0]
        if not isinstance(queue, PriorityQueue):
            raise ValueError("priority_queue_dequeue: argument must be a priority queue")
        return queue.dequeue()
    elif name == "priority_queue_peek":
        # Return the highest-priority item without removing it
        if len(evaluated_args) != 1:
            raise ValueError("priority_queue_peek expects 1 argument: priority_queue_peek(queue)")
        queue = evaluated_args[0]
        if not isinstance(queue, PriorityQueue):
            raise ValueError("priority_queue_peek: argument must be a priority queue")
        return queue.peek()
    elif name == "priority_queue_is_empty":
        # Check if the priority queue is empty
        if len(evaluated_args) != 1:
            raise ValueError("priority_queue_is_empty expects 1 argument: priority_queue_is_empty(queue)")
        queue = evaluated_args[0]
        if not isinstance(queue, PriorityQueue):
            raise ValueError("priority_queue_is_empty: argument must be a priority queue")
        return queue.is_empty()
    elif name == "priority_queue_size":
        # Get the number of items in the priority queue
        if len(evaluated_args) != 1:
            raise ValueError("priority_queue_size expects 1 argument: priority_queue_size(queue)")
        queue = evaluated_args[0]
        if not isinstance(queue, PriorityQueue):
            raise ValueError("priority_queue_size: argument must be a priority queue")
        return queue.size()

def handle_set_functions(name, evaluated_args):
    """Handle set functions."""
    if name == "set":
        # Create a new set
        return Set()
    elif name == "set_add":
        # Add an item to the set
        if len(evaluated_args) != 2:
            raise ValueError("set_add expects 2 arguments: set_add(set, item)")
        set_obj, item = evaluated_args
        if not isinstance(set_obj, Set):
            raise ValueError("set_add: first argument must be a set")
        set_obj.add(item)
        return set_obj
    elif name == "set_remove":
        # Remove an item from the set
        if len(evaluated_args) != 2:
            raise ValueError("set_remove expects 2 arguments: set_remove(set, item)")
        set_obj, item = evaluated_args
        if not isinstance(set_obj, Set):
            raise ValueError("set_remove: first argument must be a set")
        return set_obj.remove(item)
    elif name == "set_contains":
        # Check if the set contains an item
        if len(evaluated_args) != 2:
            raise ValueError("set_contains expects 2 arguments: set_contains(set, item)")
        set_obj, item = evaluated_args
        if not isinstance(set_obj, Set):
            raise ValueError("set_contains: first argument must be a set")
        return set_obj.contains(item)
    elif name == "set_clear":
        # Clear the set
        if len(evaluated_args) != 1:
            raise ValueError("set_clear expects 1 argument: set_clear(set)")
        set_obj = evaluated_args[0]
        if not isinstance(set_obj, Set):
            raise ValueError("set_clear: argument must be a set")
        set_obj.clear()
        return set_obj
    elif name == "set_size":
        # Get the number of items in the set
        if len(evaluated_args) != 1:
            raise ValueError("set_size expects 1 argument: set_size(set)")
        set_obj = evaluated_args[0]
        if not isinstance(set_obj, Set):
            raise ValueError("set_size: argument must be a set")
        return len(set_obj)
    elif name == "set_union":
        # Return the union of two sets
        if len(evaluated_args) != 2:
            raise ValueError("set_union expects 2 arguments: set_union(set1, set2)")
        set1, set2 = evaluated_args
        if not isinstance(set1, Set) or not isinstance(set2, Set):
            raise ValueError("set_union: both arguments must be sets")
        return set1.union(set2)
    elif name == "set_intersection":
        # Return the intersection of two sets
        if len(evaluated_args) != 2:
            raise ValueError("set_intersection expects 2 arguments: set_intersection(set1, set2)")
        set1, set2 = evaluated_args
        if not isinstance(set1, Set) or not isinstance(set2, Set):
            raise ValueError("set_intersection: both arguments must be sets")
        return set1.intersection(set2)
    elif name == "set_difference":
        # Return the difference of two sets
        if len(evaluated_args) != 2:
            raise ValueError("set_difference expects 2 arguments: set_difference(set1, set2)")
        set1, set2 = evaluated_args
        if not isinstance(set1, Set) or not isinstance(set2, Set):
            raise ValueError("set_difference: both arguments must be sets")
        return set1.difference(set2)
    elif name == "set_is_subset":
        # Check if set1 is a subset of set2
        if len(evaluated_args) != 2:
            raise ValueError("set_is_subset expects 2 arguments: set_is_subset(set1, set2)")
        set1, set2 = evaluated_args
        if not isinstance(set1, Set) or not isinstance(set2, Set):
            raise ValueError("set_is_subset: both arguments must be sets")
        return set1.is_subset(set2)
    elif name == "set_is_superset":
        # Check if set1 is a superset of set2
        if len(evaluated_args) != 2:
            raise ValueError("set_is_superset expects 2 arguments: set_is_superset(set1, set2)")
        set1, set2 = evaluated_args
        if not isinstance(set1, Set) or not isinstance(set2, Set):
            raise ValueError("set_is_superset: both arguments must be sets")
        return set1.is_superset(set2)
    elif name == "set_to_list":
        # Convert the set to a list
        if len(evaluated_args) != 1:
            raise ValueError("set_to_list expects 1 argument: set_to_list(set)")
        set_obj = evaluated_args[0]
        if not isinstance(set_obj, Set):
            raise ValueError("set_to_list: argument must be a set")
        return set_obj.to_list()

def handle_array_string_functions(name, evaluated_args):
    """Handle array and string functions."""
    if name == "array_slice":
        # Return a slice of the array
        if len(evaluated_args) not in [2, 3, 4]:
            raise ValueError("array_slice expects 2-4 arguments: array_slice(array, start[, end[, step]])")
        arr = evaluated_args[0]
        start = evaluated_args[1]
        end = None if len(evaluated_args) < 3 else evaluated_args[2]
        step = 1 if len(evaluated_args) < 4 else evaluated_args[3]
        
        if not isinstance(arr, list):
            raise ValueError("array_slice: first argument must be an array")
        if not isinstance(start, int):
            raise ValueError("array_slice: second argument must be an integer")
        if end is not None and not isinstance(end, int):
            raise ValueError("array_slice: third argument must be an integer")
        if not isinstance(step, int):
            raise ValueError("array_slice: fourth argument must be an integer")
        
        return array_slice(arr, start, end, step)
    elif name == "string_slice":
        # Return a slice of the string
        if len(evaluated_args) not in [2, 3, 4]:
            raise ValueError("string_slice expects 2-4 arguments: string_slice(string, start[, end[, step]])")
        s = evaluated_args[0]
        start = evaluated_args[1]
        end = None if len(evaluated_args) < 3 else evaluated_args[2]
        step = 1 if len(evaluated_args) < 4 else evaluated_args[3]
        
        if not isinstance(s, str):
            raise ValueError("string_slice: first argument must be a string")
        if not isinstance(start, int):
            raise ValueError("string_slice: second argument must be an integer")
        if end is not None and not isinstance(end, int):
            raise ValueError("string_slice: third argument must be an integer")
        if not isinstance(step, int):
            raise ValueError("string_slice: fourth argument must be an integer")
        
        return string_slice(s, start, end, step)
    elif name == "array_join":
        # Join the elements of the array with the given delimiter
        if len(evaluated_args) not in [1, 2]:
            raise ValueError("array_join expects 1-2 arguments: array_join(array[, delimiter])")
        arr = evaluated_args[0]
        delimiter = "" if len(evaluated_args) < 2 else evaluated_args[1]
        
        if not isinstance(arr, list):
            raise ValueError("array_join: first argument must be an array")
        if not isinstance(delimiter, str):
            raise ValueError("array_join: second argument must be a string")
        
        return array_join(arr, delimiter)
    elif name == "array_filter":
        # Filter the array using the given predicate function
        if len(evaluated_args) != 2:
            raise ValueError("array_filter expects 2 arguments: array_filter(array, predicate_func)")
        arr, func = evaluated_args
        
        if not isinstance(arr, list):
            raise ValueError("array_filter: first argument must be an array")
        if not callable(func):
            raise ValueError("array_filter: second argument must be a function")
        
        return array_filter(arr, func)
    elif name == "array_map":
        # Apply the given function to each element of the array
        if len(evaluated_args) != 2:
            raise ValueError("array_map expects 2 arguments: array_map(array, map_func)")
        arr, func = evaluated_args
        
        if not isinstance(arr, list):
            raise ValueError("array_map: first argument must be an array")
        if not callable(func):
            raise ValueError("array_map: second argument must be a function")
        
        return array_map(arr, func)
    elif name == "array_reduce":
        # Reduce the array to a single value using the given function
        if len(evaluated_args) not in [2, 3]:
            raise ValueError("array_reduce expects 2-3 arguments: array_reduce(array, reduce_func[, initial])")
        arr = evaluated_args[0]
        func = evaluated_args[1]
        initial = None if len(evaluated_args) < 3 else evaluated_args[2]
        
        if not isinstance(arr, list):
            raise ValueError("array_reduce: first argument must be an array")
        if not callable(func):
            raise ValueError("array_reduce: second argument must be a function")
        
        return array_reduce(arr, func, initial)
    elif name == "array_sort":
        # Sort the array
        if len(evaluated_args) not in [1, 2, 3]:
            raise ValueError("array_sort expects 1-3 arguments: array_sort(array[, reverse[, key_func]])")
        arr = evaluated_args[0]
        reverse = False if len(evaluated_args) < 2 else bool(evaluated_args[1])
        key_func = None if len(evaluated_args) < 3 else evaluated_args[2]
        
        if not isinstance(arr, list):
            raise ValueError("array_sort: first argument must be an array")
        if key_func is not None and not callable(key_func):
            raise ValueError("array_sort: third argument must be a function")
        
        return array_sort(arr, reverse, key_func)
    elif name == "array_reverse":
        # Reverse the array
        if len(evaluated_args) != 1:
            raise ValueError("array_reverse expects 1 argument: array_reverse(array)")
        arr = evaluated_args[0]
        
        if not isinstance(arr, list):
            raise ValueError("array_reverse: argument must be an array")
        
        return array_reverse(arr)
    elif name == "array_find":
        # Find the index of the first occurrence of item in the array
        if len(evaluated_args) != 2:
            raise ValueError("array_find expects 2 arguments: array_find(array, item)")
        arr, item = evaluated_args
        
        if not isinstance(arr, list):
            raise ValueError("array_find: first argument must be an array")
        
        return array_find(arr, item)
    elif name == "array_find_last":
        # Find the index of the last occurrence of item in the array
        if len(evaluated_args) != 2:
            raise ValueError("array_find_last expects 2 arguments: array_find_last(array, item)")
        arr, item = evaluated_args
        
        if not isinstance(arr, list):
            raise ValueError("array_find_last: first argument must be an array")
        
        return array_find_last(arr, item)
    elif name == "array_count":
        # Count the number of occurrences of item in the array
        if len(evaluated_args) != 2:
            raise ValueError("array_count expects 2 arguments: array_count(array, item)")
        arr, item = evaluated_args
        
        if not isinstance(arr, list):
            raise ValueError("array_count: first argument must be an array")
        
        return array_count(arr, item)
    elif name == "array_unique":
        # Return a new array with duplicate elements removed
        if len(evaluated_args) != 1:
            raise ValueError("array_unique expects 1 argument: array_unique(array)")
        arr = evaluated_args[0]
        
        if not isinstance(arr, list):
            raise ValueError("array_unique: argument must be an array")
        
        return array_unique(arr)
    elif name == "string_match":
        # Check if the string matches the regular expression pattern
        if len(evaluated_args) != 2:
            raise ValueError("string_match expects 2 arguments: string_match(string, pattern)")
        s, pattern = evaluated_args
        
        if not isinstance(s, str):
            raise ValueError("string_match: first argument must be a string")
        if not isinstance(pattern, str):
            raise ValueError("string_match: second argument must be a string")
        
        return string_match(s, pattern)
    elif name == "string_search":
        # Search for the regular expression pattern in the string
        if len(evaluated_args) != 2:
            raise ValueError("string_search expects 2 arguments: string_search(string, pattern)")
        s, pattern = evaluated_args
        
        if not isinstance(s, str):
            raise ValueError("string_search: first argument must be a string")
        if not isinstance(pattern, str):
            raise ValueError("string_search: second argument must be a string")
        
        return string_search(s, pattern)
    elif name == "string_replace":
        # Replace all occurrences of the regular expression pattern in the string
        if len(evaluated_args) != 3:
            raise ValueError("string_replace expects 3 arguments: string_replace(string, pattern, replacement)")
        s, pattern, replacement = evaluated_args
        
        if not isinstance(s, str):
            raise ValueError("string_replace: first argument must be a string")
        if not isinstance(pattern, str):
            raise ValueError("string_replace: second argument must be a string")
        if not isinstance(replacement, str):
            raise ValueError("string_replace: third argument must be a string")
        
        return string_replace(s, pattern, replacement)
    elif name == "string_split":
        # Split the string by the regular expression pattern
        if len(evaluated_args) != 2:
            raise ValueError("string_split expects 2 arguments: string_split(string, pattern)")
        s, pattern = evaluated_args
        
        if not isinstance(s, str):
            raise ValueError("string_split: first argument must be a string")
        if not isinstance(pattern, str):
            raise ValueError("string_split: second argument must be a string")
        
        return string_split(s, pattern)
    elif name == "string_match_all":
        # Find all matches of the regular expression pattern in the string
        if len(evaluated_args) != 2:
            raise ValueError("string_match_all expects 2 arguments: string_match_all(string, pattern)")
        s, pattern = evaluated_args
        
        if not isinstance(s, str):
            raise ValueError("string_match_all: first argument must be a string")
        if not isinstance(pattern, str):
            raise ValueError("string_match_all: second argument must be a string")
        
        return string_match_all(s, pattern)

def handle_math_functions(name, evaluated_args):
    """Handle math functions."""
    if name == "sqrt":
        if len(evaluated_args) != 1:
            raise ValueError("sqrt expects 1 argument: sqrt(x)")
        x = evaluated_args[0]
        return sqrt(x)
    elif name == "pow":
        if len(evaluated_args) != 2:
            raise ValueError("pow expects 2 arguments: pow(x, y)")
        x, y = evaluated_args
        return pow(x, y)
    elif name == "log":
        if len(evaluated_args) not in [1, 2]:
            raise ValueError("log expects 1-2 arguments: log(x[, base])")
        x = evaluated_args[0]
        base = math.e if len(evaluated_args) < 2 else evaluated_args[1]
        return log(x, base)
    elif name == "log10":
        if len(evaluated_args) != 1:
            raise ValueError("log10 expects 1 argument: log10(x)")
        x = evaluated_args[0]
        return log10(x)
    elif name == "sin":
        if len(evaluated_args) != 1:
            raise ValueError("sin expects 1 argument: sin(x)")
        x = evaluated_args[0]
        return sin(x)
    elif name == "cos":
        if len(evaluated_args) != 1:
            raise ValueError("cos expects 1 argument: cos(x)")
        x = evaluated_args[0]
        return cos(x)
    elif name == "tan":
        if len(evaluated_args) != 1:
            raise ValueError("tan expects 1 argument: tan(x)")
        x = evaluated_args[0]
        return tan(x)
    elif name == "asin":
        if len(evaluated_args) != 1:
            raise ValueError("asin expects 1 argument: asin(x)")
        x = evaluated_args[0]
        return asin(x)
    elif name == "acos":
        if len(evaluated_args) != 1:
            raise ValueError("acos expects 1 argument: acos(x)")
        x = evaluated_args[0]
        return acos(x)
    elif name == "atan":
        if len(evaluated_args) != 1:
            raise ValueError("atan expects 1 argument: atan(x)")
        x = evaluated_args[0]
        return atan(x)
    elif name == "atan2":
        if len(evaluated_args) != 2:
            raise ValueError("atan2 expects 2 arguments: atan2(y, x)")
        y, x = evaluated_args
        return atan2(y, x)
    elif name == "degrees":
        if len(evaluated_args) != 1:
            raise ValueError("degrees expects 1 argument: degrees(x)")
        x = evaluated_args[0]
        return degrees(x)
    elif name == "radians":
        if len(evaluated_args) != 1:
            raise ValueError("radians expects 1 argument: radians(x)")
        x = evaluated_args[0]
        return radians(x)
    elif name == "floor":
        if len(evaluated_args) != 1:
            raise ValueError("floor expects 1 argument: floor(x)")
        x = evaluated_args[0]
        return floor(x)
    elif name == "ceil":
        if len(evaluated_args) != 1:
            raise ValueError("ceil expects 1 argument: ceil(x)")
        x = evaluated_args[0]
        return ceil(x)
    elif name == "round":
        if len(evaluated_args) not in [1, 2]:
            raise ValueError("round expects 1-2 arguments: round(x[, ndigits])")
        x = evaluated_args[0]
        ndigits = 0 if len(evaluated_args) < 2 else evaluated_args[1]
        return round(x, ndigits)
    elif name == "abs":
        if len(evaluated_args) != 1:
            raise ValueError("abs expects 1 argument: abs(x)")
        x = evaluated_args[0]
        return abs(x)
    elif name == "gcd":
        if len(evaluated_args) != 2:
            raise ValueError("gcd expects 2 arguments: gcd(a, b)")
        a, b = evaluated_args
        return gcd(a, b)
    elif name == "lcm":
        if len(evaluated_args) != 2:
            raise ValueError("lcm expects 2 arguments: lcm(a, b)")
        a, b = evaluated_args
        return lcm(a, b)
    elif name == "is_prime":
        if len(evaluated_args) != 1:
            raise ValueError("is_prime expects 1 argument: is_prime(n)")
        n = evaluated_args[0]
        return is_prime(n)
    elif name == "factorial":
        if len(evaluated_args) != 1:
            raise ValueError("factorial expects 1 argument: factorial(n)")
        n = evaluated_args[0]
        return factorial(n)

def handle_random_functions(name, evaluated_args):
    """Handle random number generation functions."""
    if name == "random_int":
        if len(evaluated_args) != 2:
            raise ValueError("random_int expects 2 arguments: random_int(a, b)")
        a, b = evaluated_args
        return random_int(a, b)
    elif name == "random_float":
        if len(evaluated_args) != 0:
            raise ValueError("random_float expects 0 arguments: random_float()")
        return random_float()
    elif name == "random_uniform":
        if len(evaluated_args) != 2:
            raise ValueError("random_uniform expects 2 arguments: random_uniform(a, b)")
        a, b = evaluated_args
        return random_uniform(a, b)

def handle_bitwise_functions(name, evaluated_args):
    """Handle bitwise operations."""
    if name == "bit_and":
        if len(evaluated_args) != 2:
            raise ValueError("bit_and expects 2 arguments: bit_and(a, b)")
        a, b = evaluated_args
        return bit_and(a, b)
    elif name == "bit_or":
        if len(evaluated_args) != 2:
            raise ValueError("bit_or expects 2 arguments: bit_or(a, b)")
        a, b = evaluated_args
        return bit_or(a, b)
    elif name == "bit_xor":
        if len(evaluated_args) != 2:
            raise ValueError("bit_xor expects 2 arguments: bit_xor(a, b)")
        a, b = evaluated_args
        return bit_xor(a, b)
    elif name == "bit_not":
        if len(evaluated_args) != 1:
            raise ValueError("bit_not expects 1 argument: bit_not(a)")
        a = evaluated_args[0]
        return bit_not(a)
    elif name == "bit_shift_left":
        if len(evaluated_args) != 2:
            raise ValueError("bit_shift_left expects 2 arguments: bit_shift_left(a, n)")
        a, n = evaluated_args
        return bit_shift_left(a, n)
    elif name == "bit_shift_right":
        if len(evaluated_args) != 2:
            raise ValueError("bit_shift_right expects 2 arguments: bit_shift_right(a, n)")
        a, n = evaluated_args
        return bit_shift_right(a, n)
