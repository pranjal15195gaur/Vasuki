import sys
from parser import parse
from bytecode_pure import BytecodeGenerator, BytecodeVM

def test_simple_function():
    # Test a simple function call
    code = """
    def add(a, b) {
        return a + b;
    };

    print(add(5, 10));
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_nested_function():
    # Test the example from the prompt
    code = """
    def f(x) {
        return x + 1;
    };

    def g(y) {
        return f(y + 1);
    };

    print(g(42));
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_closure():
    # Test a closure function
    code = """
    def f(g){
        var x = 17;
        var y = 5;

        def s(){
            return x + y + g();
        };

        return s;
    };

    def const42(){
        return 42;
    };

    def const84(){
        return 84;
    };

    var s1 = f(const42);
    var s2 = f(const84);
    print(s2());
    print(s1());
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_loop():
    # Test a while loop
    code = """
    var sum = 0;
    var i = 1;
    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    };
    print(sum);
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_recursive_factorial():
    # Test a recursive factorial function
    code = """
    def factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        };
    };

    print(factorial(5));
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_recursive_fibonacci():
    # Test a recursive fibonacci function
    code = """
    def fibonacci(n) {
        if (n <= 1) {
            return n;
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2);
        };
    };

    print(fibonacci(10));
    """

    try:
        ast = parse(code)
        print("AST formed:")
        from pprint import pprint
        pprint(ast)

        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)

        # Run the bytecode
        vm = BytecodeVM(bytecode)
        result = vm.run()
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "function":
            test_simple_function()
        elif test_name == "nested":
            test_nested_function()
        elif test_name == "closure":
            test_closure()
        elif test_name == "loop":
            test_loop()
        elif test_name == "factorial":
            test_recursive_factorial()
        elif test_name == "fibonacci":
            test_recursive_fibonacci()
        else:
            print(f"Unknown test: {test_name}")
    else:
        print("Running all tests...")
        print("\n=== Testing Simple Function ===")
        test_simple_function()
        print("\n=== Testing Nested Function ===")
        test_nested_function()
        print("\n=== Testing Closure ===")
        test_closure()
        print("\n=== Testing Loop ===")
        test_loop()
        print("\n=== Testing Recursive Factorial ===")
        test_recursive_factorial()
        print("\n=== Testing Recursive Fibonacci ===")
        test_recursive_fibonacci()
