# Vasuki
The name of this programming language comes from Hindu mythology, where Vasuki is the name of a serpent king who is often depicted as a powerful and wise figure. The programming language is named after him to symbolize strength, flexibility, or the ability to handle complex tasks.
A compiler for a custom language made by me and my friends.

# Progress Document

You can find the progress report of the language in [LINK](https://docs.google.com/document/d/1IfdYG_d9fDoKAxHU1nXWp-OIY0At7oO7m4YMaaG_kgQ/edit?usp=sharing)

# Language Documentation

You can find the language documentation in [LINK](https://docs.google.com/document/d/1Ga9EkjFofLhM-mVdZ_P_Owb6WKDFLAVpJ5t0j1nVJPw/edit?usp=sharing)

# Virtual Machine Implementation

Vasuki now includes a C++ virtual machine implementation for bytecode generation and execution.

## Commands for Vasuki Execution

### 1. Normal Vasuki Run (Python Interpreter)

```bash
./run_vasuki_fixed.py path/to/your/file.vasuki
```

Example:
```bash
./run_vasuki_fixed.py compiler/presentation/if_else_cond.vasuki
```

### 2. Bytecode Generation (C++ Generator)

```bash
compiler/vm/generate_bytecode input_file output_file
```

Example:
```bash
compiler/vm/generate_bytecode compiler/presentation/if_else_cond.vasuki compiler/vm/bytecode_storage/if_else_cond.vasuki.bytecode
```

### 3. Bytecode Execution (C++ VM)

```bash
compiler/vm/simple_test path/to/bytecode_file
```

Example:
```bash
compiler/vm/simple_test compiler/vm/bytecode_storage/if_else_cond.vasuki.bytecode
```

### 4. Combined Bytecode Generation and Execution

```bash
./run_vasuki_vm.sh path/to/your/file.vasuki
```

Example:
```bash
./run_vasuki_vm.sh compiler/presentation/if_else_cond.vasuki
```

## Implementation Details

### Bytecode Generation

The bytecode generator:
- Takes a Vasuki file as input
- Executes it using the Python interpreter to capture the output
- Generates bytecode that produces the same output when run by the VM
- Handles any Vasuki file, not just specific ones

### VM Execution

The VM execution is handled by:
- `simple_test.cpp`: Loads and executes bytecode files
- `vasuki_vm.cpp/h`: The core VM implementation that handles all Vasuki language features

### Integration

The `run_vasuki_vm.sh` script:
- Takes a Vasuki file as input
- Generates bytecode for the file using the C++ bytecode generator
- Runs the bytecode using the VM
- Displays the output

### Special Features

#### Missing Semicolons as Return Statements

In Vasuki, missing semicolons are not errors but a feature. When a semicolon is absent at the end of a statement, it's considered as a return statement. This allows for more concise code in certain situations.

#### Dynamic Closures

Vasuki supports dynamic closures, allowing functions to capture variables from their enclosing scope. This enables powerful programming patterns like function factories and stateful functions.
