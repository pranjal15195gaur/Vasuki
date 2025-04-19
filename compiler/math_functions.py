import math
import random

def sqrt(x):
    """
    Calculate the square root of a number.

    Args:
        x: The number to calculate the square root of.

    Returns:
        The square root of x.

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(x)

def pow(x, y):
    """
    Calculate x raised to the power of y.

    Args:
        x: The base.
        y: The exponent.

    Returns:
        x raised to the power of y.
    """
    return math.pow(x, y)

def log(x, base=math.e):
    """
    Calculate the logarithm of x with the given base.

    Args:
        x: The number to calculate the logarithm of.
        base: The base of the logarithm (default: e).

    Returns:
        The logarithm of x with the given base.

    Raises:
        ValueError: If x <= 0 or base <= 0 or base == 1.
    """
    if x <= 0:
        raise ValueError("Cannot calculate logarithm of a non-positive number")
    if base <= 0 or base == 1:
        raise ValueError("Invalid logarithm base")

    if base == math.e:
        return math.log(x)
    elif base == 10:
        return math.log10(x)
    else:
        return math.log(x) / math.log(base)

def log10(x):
    """
    Calculate the base-10 logarithm of x.

    Args:
        x: The number to calculate the logarithm of.

    Returns:
        The base-10 logarithm of x.

    Raises:
        ValueError: If x <= 0.
    """
    return log(x, 10)

def sin(x):
    """
    Calculate the sine of x (x in radians).

    Args:
        x: The angle in radians.

    Returns:
        The sine of x.
    """
    return math.sin(x)

def cos(x):
    """
    Calculate the cosine of x (x in radians).

    Args:
        x: The angle in radians.

    Returns:
        The cosine of x.
    """
    return math.cos(x)

def tan(x):
    """
    Calculate the tangent of x (x in radians).

    Args:
        x: The angle in radians.

    Returns:
        The tangent of x.
    """
    return math.tan(x)

def asin(x):
    """
    Calculate the arc sine of x.

    Args:
        x: The value to calculate the arc sine of.

    Returns:
        The arc sine of x, in radians.

    Raises:
        ValueError: If x is outside the range [-1, 1].
    """
    if x < -1 or x > 1:
        raise ValueError("asin(x) requires -1 <= x <= 1")
    return math.asin(x)

def acos(x):
    """
    Calculate the arc cosine of x.

    Args:
        x: The value to calculate the arc cosine of.

    Returns:
        The arc cosine of x, in radians.

    Raises:
        ValueError: If x is outside the range [-1, 1].
    """
    if x < -1 or x > 1:
        raise ValueError("acos(x) requires -1 <= x <= 1")
    return math.acos(x)

def atan(x):
    """
    Calculate the arc tangent of x.

    Args:
        x: The value to calculate the arc tangent of.

    Returns:
        The arc tangent of x, in radians.
    """
    return math.atan(x)

def atan2(y, x):
    """
    Calculate the arc tangent of y/x, respecting the signs of both arguments.

    Args:
        y: The y-coordinate.
        x: The x-coordinate.

    Returns:
        The arc tangent of y/x, in radians.
    """
    return math.atan2(y, x)

def degrees(x):
    """
    Convert angle x from radians to degrees.

    Args:
        x: The angle in radians.

    Returns:
        The angle in degrees.
    """
    return math.degrees(x)

def radians(x):
    """
    Convert angle x from degrees to radians.

    Args:
        x: The angle in degrees.

    Returns:
        The angle in radians.
    """
    return math.radians(x)

def floor(x):
    """
    Return the floor of x, the largest integer less than or equal to x.

    Args:
        x: The number to calculate the floor of.

    Returns:
        The floor of x.
    """
    return math.floor(x)

def ceil(x):
    """
    Return the ceiling of x, the smallest integer greater than or equal to x.

    Args:
        x: The number to calculate the ceiling of.

    Returns:
        The ceiling of x.
    """
    return math.ceil(x)

def round(x, ndigits=0):
    """
    Round x to the nearest integer or to ndigits decimal places.

    Args:
        x: The number to round.
        ndigits: The number of decimal places to round to (default: 0).

    Returns:
        The rounded number.
    """
    import builtins
    return builtins.round(x, ndigits)

def abs(x):
    """
    Return the absolute value of x.

    Args:
        x: The number to calculate the absolute value of.

    Returns:
        The absolute value of x.
    """
    if isinstance(x, int) or isinstance(x, float):
        return -x if x < 0 else x
    else:
        raise ValueError("abs: argument must be a number")

def gcd(a, b):
    """
    Calculate the greatest common divisor of a and b.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The greatest common divisor of a and b.
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """
    Calculate the least common multiple of a and b.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The least common multiple of a and b.
    """
    return abs(a * b) // gcd(a, b) if a and b else 0

def is_prime(n):
    """
    Check if n is a prime number.

    Args:
        n: The number to check.

    Returns:
        True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def factorial(n):
    """
    Calculate the factorial of n.

    Args:
        n: The number to calculate the factorial of.

    Returns:
        The factorial of n.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def random_int(a, b):
    """
    Generate a random integer between a and b, inclusive.

    Args:
        a: The lower bound.
        b: The upper bound.

    Returns:
        A random integer between a and b, inclusive.
    """
    return random.randint(a, b)

def random_float():
    """
    Generate a random float between 0 and 1.

    Returns:
        A random float between 0 and 1.
    """
    return random.random()

def random_uniform(a, b):
    """
    Generate a random float between a and b.

    Args:
        a: The lower bound.
        b: The upper bound.

    Returns:
        A random float between a and b.
    """
    return random.uniform(a, b)

def bit_and(a, b):
    """
    Perform a bitwise AND operation on a and b.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The result of a & b.
    """
    return a & b

def bit_or(a, b):
    """
    Perform a bitwise OR operation on a and b.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The result of a | b.
    """
    return a | b

def bit_xor(a, b):
    """
    Perform a bitwise XOR operation on a and b.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The result of a ^ b.
    """
    return a ^ b

def bit_not(a):
    """
    Perform a bitwise NOT operation on a.

    Args:
        a: The number.

    Returns:
        The result of ~a.
    """
    return ~a

def bit_shift_left(a, n):
    """
    Perform a left shift operation on a by n bits.

    Args:
        a: The number to shift.
        n: The number of bits to shift by.

    Returns:
        The result of a << n.
    """
    return a << n

def bit_shift_right(a, n):
    """
    Perform a right shift operation on a by n bits.

    Args:
        a: The number to shift.
        n: The number of bits to shift by.

    Returns:
        The result of a >> n.
    """
    return a >> n
