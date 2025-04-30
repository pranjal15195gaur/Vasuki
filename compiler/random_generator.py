"""
Custom random number generator for Vasuki language.
Implements a time-based Linear Congruential Generator (LCG) for random number generation.
"""

import time

# Constants for the LCG algorithm
# Using parameters from the "Numerical Recipes" LCG
# These values have been proven to have good statistical properties
MULTIPLIER = 1664525
INCREMENT = 1013904223
MODULUS = 2**32  # 32-bit modulus

# Global state for the random generator
_seed = None
_last_value = None

def _initialize():
    """Initialize the random generator with a time-based seed if not already initialized."""
    global _seed, _last_value
    if _seed is None:
        # Use current time in nanoseconds as seed
        # This ensures high randomness even for rapid consecutive calls
        _seed = int(time.time() * 1000000)
        # Add some additional entropy from process time
        _seed = (_seed + int(time.process_time() * 1000000)) % MODULUS
        _last_value = _seed

def seed(value=None):
    """
    Seed the random number generator.
    
    Args:
        value: The seed value. If None, uses current time.
    """
    global _seed, _last_value
    if value is None:
        # Use current time in nanoseconds
        value = int(time.time() * 1000000)
    _seed = value % MODULUS
    _last_value = _seed

def _next_random():
    """
    Generate the next random value using LCG algorithm.
    
    Returns:
        A random integer between 0 and MODULUS-1.
    """
    global _last_value
    
    # Initialize if not already done
    if _last_value is None:
        _initialize()
    
    # LCG formula: X_(n+1) = (a * X_n + c) mod m
    _last_value = (MULTIPLIER * _last_value + INCREMENT) % MODULUS
    return _last_value

def random():
    """
    Generate a random float between 0.0 and 1.0.
    
    Returns:
        A random float in [0.0, 1.0).
    """
    return _next_random() / MODULUS

def randint(a, b):
    """
    Generate a random integer between a and b, inclusive.
    
    Args:
        a: The lower bound.
        b: The upper bound.
        
    Returns:
        A random integer in [a, b].
    """
    if a > b:
        a, b = b, a
    range_size = b - a + 1
    # Scale the random value to the desired range
    return a + (_next_random() % range_size)

def uniform(a, b):
    """
    Generate a random float between a and b.
    
    Args:
        a: The lower bound.
        b: The upper bound.
        
    Returns:
        A random float in [a, b).
    """
    if a > b:
        a, b = b, a
    # Scale the random value to the desired range
    return a + (b - a) * random()
