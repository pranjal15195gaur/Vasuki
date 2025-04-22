# Terminal Input in Vasuki

This document explains how to use terminal input in Vasuki programs.

## Built-in Input Functions

Vasuki provides several built-in functions for reading input from the terminal:

1. `read_line()` - Reads a single line of text from the terminal
   ```
   var name = read_line();
   ```

2. `read_int()` - Reads a single integer from the terminal
   ```
   var age = read_int();
   ```

3. `read_float()` - Reads a single floating-point number from the terminal
   ```
   var price = read_float();
   ```

## Examples

### Simple Example

```
// Simple program to demonstrate terminal input

// Ask for the user's name
print("What is your name?");
var name = read_line();

// Ask for the user's age
print("How old are you?");
var age = read_int();

// Greet the user
print("Hello, " + name + "! In 10 years, you will be " + (age + 10) + " years old.");
```

### Advanced Example

```
// Advanced program to demonstrate all terminal input functions

// Function to test read_line
def test_read_line() {
    print("Enter a line of text:");
    var line = read_line();
    print("You entered: " + line);
};

// Function to test read_int
def test_read_int() {
    print("Enter an integer:");
    var num = read_int();
    print("You entered: " + num);
    print("Double of your number is: " + (num * 2));
};

// Function to test read_float
def test_read_float() {
    print("Enter a float:");
    var num = read_float();
    print("You entered: " + num);
    print("Half of your number is: " + (num / 2));
};

// Main function to run the tests
def main() {
    print("Testing input functions");
    print("---------------------");
    
    test_read_line();
    test_read_int();
    test_read_float();
    
    print("All tests completed!");
};

// Run the main function
main();
```

## Running Programs with Input

To run a Vasuki program that uses terminal input, use the `run_bytecode.py` script:

```
python run_bytecode.py your_program.vasuki
```

This script will:
1. Parse the Vasuki code
2. Generate bytecode
3. Execute the bytecode
4. Prompt for input when needed

## Implementation Details

Terminal input is implemented in the bytecode VM using the following components:

1. The READ opcode in the OC enum
2. The READ opcode handler in the BytecodeVM class
3. Built-in input functions (read_line, read_int, read_float)
4. Special handling in the CALL opcode handler for built-in functions

When a Vasuki program calls a built-in input function, the bytecode VM executes the corresponding Python input function and continues execution with the input value.
