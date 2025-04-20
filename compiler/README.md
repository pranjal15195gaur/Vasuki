# Vasuki Virtual Machine

This is a C++ implementation of a virtual machine for the Vasuki programming language. The VM executes bytecode generated from Vasuki source code.

## Features

- Complete implementation of all Vasuki language features
- Support for various data types: null, boolean, integer, float, string, array, dictionary, function
- Arithmetic and logical operations
- Variable declaration and assignment
- Control flow (if/else, loops)
- Function definition and calling
- Arrays and dictionaries
- String operations
- Special feature: missing semicolons act as return statements
- Tail call optimization for recursive functions

## Files

- `vasuki_vm.h` - Header file defining the VM classes and interfaces
- `vasuki_vm.cpp` - Implementation of the VM
- `test_vm.cpp` - Test program to run Vasuki files
- `simple_test.cpp` - Simple test of basic VM functionality
- `semicolon_test.cpp` - Test of function calls
- `missing_semicolon_test.cpp` - Test of the missing semicolon feature
- `tail_optimization.cpp` - Test of tail call optimization

## Building

To build all test programs:

```bash
make
```

To build a specific test:

```bash
make simple_test
make missing_semicolon_test
make tail_optimization
```

## Running Tests

To run a specific test:

```bash
./simple_test
./missing_semicolon_test
./tail_optimization 1000  # Test tail call optimization with 1000 recursive calls
```

To test a Vasuki file (requires Python compiler):

```bash
./test_vm path/to/file.vasuki
```

## VM Architecture

The VM is a stack-based virtual machine that executes bytecode instructions. It has the following components:

- **Stack**: Used for operands and results of operations
- **Bytecode**: The instructions to execute
- **Constants**: Constant values used by the bytecode
- **Names**: String identifiers (variable names, function names, etc.)
- **Environment**: Stores variables and their values
- **Call Stack**: Manages function calls and returns

## Bytecode Instructions

The VM supports a wide range of bytecode instructions, including:

- Stack operations (PUSH, POP, DUP)
- Arithmetic operations (ADD, SUB, MUL, DIV, MOD)
- Logical operations (AND, OR, NOT)
- Comparison operations (EQ, NEQ, LT, LTE, GT, GTE)
- Variable operations (GET_GLOBAL, SET_GLOBAL, DEFINE_GLOBAL, GET_LOCAL, SET_LOCAL, DEFINE_LOCAL)
- Control flow (JUMP, JUMP_IF_FALSE, JUMP_IF_TRUE)
- Function operations (CALL, TAIL_CALL, RETURN, FUNCTION)
- Data structure operations (LIST, DICT, GET_PROPERTY, SET_PROPERTY)
- I/O operations (PRINT)

## Built-in Functions

The VM provides several built-in functions:

- `print`: Print values to the console
- `length`: Get the length of a string, array, or dictionary
- `uppercase`: Convert a string to uppercase
- `lowercase`: Convert a string to lowercase
- `type`: Get the type of a value
- `to_string`: Convert a value to a string
- `to_int`: Convert a value to an integer
- `to_float`: Convert a value to a float
- `split`: Split a string into an array
- `dict_keys`: Get the keys of a dictionary
- `dict_values`: Get the values of a dictionary
- `dict_clear`: Clear a dictionary
- `dict_size`: Get the size of a dictionary

## Special Features

### Missing Semicolon Feature

One of the unique features of Vasuki is that missing semicolons act as return statements. This is implemented in the VM by treating the last expression in a block as a return value if there is no explicit return statement.

### Tail Call Optimization

The VM implements tail call optimization for recursive functions. This allows recursive functions to execute without growing the call stack, which prevents stack overflow for deeply recursive functions.

A tail call is a function call that is the last operation before returning from the current function. The VM detects tail calls and replaces the current stack frame with the new one instead of adding a new frame.
