# If-Else Statements in Vasuki Bytecode

This document explains how if-else statements are implemented in the Vasuki bytecode.

## Overview

If-else statements in Vasuki allow for conditional execution of code. The bytecode implementation uses jump instructions to control the flow of execution.

## Syntax

```
if (condition) {
    // then branch
} else if (condition2) {
    // else-if branch
} else {
    // else branch
};
```

## Bytecode Implementation

The bytecode implementation of if-else statements uses the following opcodes:

- `JF` (Jump if False): Jumps to a specified instruction if the condition is false
- `JMP` (Jump): Unconditionally jumps to a specified instruction

## How It Works

1. Evaluate the condition and push the result onto the stack
2. Use a `JF` instruction to jump to the else branch if the condition is false
3. Execute the then branch
4. Use a `JMP` instruction to jump to the end of the if-else statement
5. For else-if branches, repeat steps 1-4 for each branch
6. For the else branch, simply execute the code

## Example

Consider the following Vasuki code:

```
if (num > 0) {
    print("Positive");
} else if (num < 0) {
    print("Negative");
} else {
    print("Zero");
};
```

This would be compiled to the following bytecode:

```
0: (OC.GET, 'num')
1: (OC.PUSH, 0)
2: (OC.GT, None)
3: (OC.JF, 7)
4: (OC.PUSH, 'Positive')
5: (OC.PRINT, None)
6: (OC.JMP, 16)
7: (OC.GET, 'num')
8: (OC.PUSH, 0)
9: (OC.LT, None)
10: (OC.JF, 14)
11: (OC.PUSH, 'Negative')
12: (OC.PRINT, None)
13: (OC.JMP, 16)
14: (OC.PUSH, 'Zero')
15: (OC.PRINT, None)
16: ...
```

## Nested If-Else Statements

Nested if-else statements work the same way, with each level of nesting having its own set of jump instructions.

## Implementation Details

The implementation of if-else statements in the bytecode generator is in the `visit_If` method of the `BytecodeGenerator` class in `bytecode_pure.py`. The method handles the following:

1. Evaluating the condition
2. Generating code for the then branch
3. Generating code for the else-if branches
4. Generating code for the else branch
5. Setting up the jump instructions to control the flow of execution

## Testing

You can test if-else statements with the following examples:

1. `if_test.vasuki`: A simple test of if-else statements
2. `if_complex.vasuki`: A more complex test with multiple else-if branches and nested if-else statements

Run these examples with the `run_bytecode.py` script:

```
python run_bytecode.py if_test.vasuki
python run_bytecode.py if_complex.vasuki
```
