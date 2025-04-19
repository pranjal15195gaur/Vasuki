import re

def array_slice(arr, start, end=None, step=1):
    """
    Return a slice of the array from start to end with the given step.
    
    Args:
        arr: The array to slice.
        start: The start index (1-based).
        end: The end index (1-based, exclusive). If None, slice to the end of the array.
        step: The step size.
        
    Returns:
        A slice of the array.
        
    Raises:
        ValueError: If start or end are invalid.
    """
    # Convert to 0-based indexing
    start_0 = start - 1
    
    if start_0 < 0:
        raise ValueError(f"Start index {start} out of range (must be >= 1)")
    
    if end is None:
        # Slice to the end
        return arr[start_0::step]
    else:
        # Convert end to 0-based indexing (exclusive)
        end_0 = end - 1
        
        if end_0 < start_0:
            raise ValueError(f"End index {end} must be greater than or equal to start index {start}")
        
        return arr[start_0:end_0:step]

def string_slice(s, start, end=None, step=1):
    """
    Return a slice of the string from start to end with the given step.
    
    Args:
        s: The string to slice.
        start: The start index (1-based).
        end: The end index (1-based, exclusive). If None, slice to the end of the string.
        step: The step size.
        
    Returns:
        A slice of the string.
        
    Raises:
        ValueError: If start or end are invalid.
    """
    return array_slice(s, start, end, step)

def array_join(arr, delimiter=""):
    """
    Join the elements of the array with the given delimiter.
    
    Args:
        arr: The array to join.
        delimiter: The delimiter to use.
        
    Returns:
        A string containing the joined elements.
    """
    # Convert all elements to strings
    str_arr = [str(item) for item in arr]
    return delimiter.join(str_arr)

def array_filter(arr, predicate_func):
    """
    Filter the array using the given predicate function.
    
    Args:
        arr: The array to filter.
        predicate_func: A function that takes an element and returns a boolean.
        
    Returns:
        A new array containing only the elements for which predicate_func returns True.
    """
    result = []
    for item in arr:
        if predicate_func(item):
            result.append(item)
    return result

def array_map(arr, map_func):
    """
    Apply the given function to each element of the array.
    
    Args:
        arr: The array to map.
        map_func: A function that takes an element and returns a new element.
        
    Returns:
        A new array containing the results of applying map_func to each element.
    """
    result = []
    for item in arr:
        result.append(map_func(item))
    return result

def array_reduce(arr, reduce_func, initial=None):
    """
    Reduce the array to a single value using the given function.
    
    Args:
        arr: The array to reduce.
        reduce_func: A function that takes two arguments (accumulator and current value) and returns a new accumulator.
        initial: The initial value of the accumulator. If None, the first element of the array is used.
        
    Returns:
        The final value of the accumulator.
        
    Raises:
        ValueError: If the array is empty and no initial value is provided.
    """
    if not arr and initial is None:
        raise ValueError("Cannot reduce an empty array without an initial value")
    
    if initial is None:
        result = arr[0]
        arr = arr[1:]
    else:
        result = initial
    
    for item in arr:
        result = reduce_func(result, item)
    
    return result

def array_sort(arr, reverse=False, key_func=None):
    """
    Sort the array in-place.
    
    Args:
        arr: The array to sort.
        reverse: If True, sort in descending order.
        key_func: A function that takes an element and returns a key to sort by.
        
    Returns:
        The sorted array.
    """
    # Create a new sorted array
    if key_func is None:
        result = sorted(arr, reverse=reverse)
    else:
        result = sorted(arr, key=key_func, reverse=reverse)
    
    # Copy the sorted elements back to the original array
    for i in range(len(arr)):
        arr[i] = result[i]
    
    return arr

def array_reverse(arr):
    """
    Reverse the array in-place.
    
    Args:
        arr: The array to reverse.
        
    Returns:
        The reversed array.
    """
    # Create a new reversed array
    result = arr[::-1]
    
    # Copy the reversed elements back to the original array
    for i in range(len(arr)):
        arr[i] = result[i]
    
    return arr

def array_find(arr, item):
    """
    Find the index of the first occurrence of item in the array.
    
    Args:
        arr: The array to search.
        item: The item to find.
        
    Returns:
        The 1-based index of the first occurrence of item, or 0 if not found.
    """
    try:
        # Convert to 1-based indexing
        return arr.index(item) + 1
    except ValueError:
        return 0

def array_find_last(arr, item):
    """
    Find the index of the last occurrence of item in the array.
    
    Args:
        arr: The array to search.
        item: The item to find.
        
    Returns:
        The 1-based index of the last occurrence of item, or 0 if not found.
    """
    # Reverse the array and search from the beginning
    reversed_arr = arr[::-1]
    try:
        # Convert to 1-based indexing
        return len(arr) - reversed_arr.index(item)
    except ValueError:
        return 0

def array_count(arr, item):
    """
    Count the number of occurrences of item in the array.
    
    Args:
        arr: The array to search.
        item: The item to count.
        
    Returns:
        The number of occurrences of item in the array.
    """
    return arr.count(item)

def array_unique(arr):
    """
    Return a new array with duplicate elements removed.
    
    Args:
        arr: The array to process.
        
    Returns:
        A new array with duplicate elements removed.
    """
    result = []
    seen = set()
    for item in arr:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def string_match(s, pattern):
    """
    Check if the string matches the regular expression pattern.
    
    Args:
        s: The string to check.
        pattern: The regular expression pattern.
        
    Returns:
        True if the string matches the pattern, False otherwise.
    """
    return bool(re.match(pattern, s))

def string_search(s, pattern):
    """
    Search for the regular expression pattern in the string.
    
    Args:
        s: The string to search.
        pattern: The regular expression pattern.
        
    Returns:
        The 1-based index of the first match, or 0 if not found.
    """
    match = re.search(pattern, s)
    if match:
        # Convert to 1-based indexing
        return match.start() + 1
    else:
        return 0

def string_replace(s, pattern, replacement):
    """
    Replace all occurrences of the regular expression pattern in the string.
    
    Args:
        s: The string to process.
        pattern: The regular expression pattern.
        replacement: The replacement string.
        
    Returns:
        A new string with all occurrences of the pattern replaced.
    """
    return re.sub(pattern, replacement, s)

def string_split(s, pattern):
    """
    Split the string by the regular expression pattern.
    
    Args:
        s: The string to split.
        pattern: The regular expression pattern.
        
    Returns:
        An array of substrings.
    """
    return re.split(pattern, s)

def string_match_all(s, pattern):
    """
    Find all matches of the regular expression pattern in the string.
    
    Args:
        s: The string to search.
        pattern: The regular expression pattern.
        
    Returns:
        An array of matched substrings.
    """
    return re.findall(pattern, s)
