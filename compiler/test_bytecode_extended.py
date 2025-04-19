# test_bytecode_extended.py
# Tests for the extended bytecode functionality

import sys
from parser import parse
from bytecode_extended import BytecodeGenerator, BytecodeVM

def test_string_operations():
    # Test string operations
    code = """
    var greeting = "Hello";
    var name = "World";
    var message = greeting + ", " + name + "!";
    print(message);
    
    // Test string indexing
    print(message[0]);
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

def test_dictionary_operations():
    # Test dictionary operations
    code = """
    var dict = {"name": "John", "age": 30, "city": "New York"};
    print(dict["name"]);
    print(dict["age"]);
    print(dict["city"]);
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

def test_array_operations():
    # Test array operations
    code = """
    var numbers = [1, 2, 3, 4, 5];
    print(numbers[0]);
    print(numbers[2]);
    print(numbers[4]);
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

def test_type_operations():
    # Test type checking and conversion
    code = """
    var num = 42;
    var str = "42";
    var flt = 3.14;
    var bool = true;
    
    print(is_int(num));
    print(is_string(str));
    print(is_float(flt));
    print(is_bool(bool));
    
    print(to_int(str));
    print(to_string(num));
    print(to_float(num));
    print(to_bool(num));
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

def test_yield():
    # Test yield statement
    code = """
    def generator() {
        yield 1;
        yield 2;
        yield 3;
        return 4;
    };
    
    var gen = generator();
    print(gen());
    print(gen());
    print(gen());
    print(gen());
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

def test_dynamic_variables():
    # Test dynamic variables
    code = """
    dynamic var x = 10;
    
    def test() {
        print(x);
        x = 20;
        print(x);
    };
    
    test();
    print(x);
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

def test_dynamic_functions():
    # Test dynamic functions
    code = """
    dynamic def add(a, b) {
        return a + b;
    };
    
    def test() {
        print(add(10, 20));
        
        // Redefine the add function
        dynamic def add(a, b) {
            return a * b;
        };
        
        print(add(10, 20));
    };
    
    test();
    print(add(10, 20));
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

def test_labels_and_goto():
    # Test labels and goto
    code = """
    var i = 0;
    
    start:
    i = i + 1;
    print(i);
    if (i < 5) {
        goandreturn start;
    };
    
    start return;
    print("Done");
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

def test_input_operations():
    # Test input operations
    code = """
    print("Enter your name:");
    var name = read_line();
    print("Hello, " + name + "!");
    
    print("Enter your age:");
    var age = read_int();
    print("In 10 years, you will be " + to_string(age + 10) + " years old.");
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

        # Note: We won't run this test automatically since it requires user input
        print("\nSkipping execution (requires user input).")
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_string_methods():
    # Test string methods
    code = """
    var str = "Hello, World!";
    
    print(uppercase(str));
    print(lowercase(str));
    print(substring(str, 0, 5));
    print(contains(str, "World"));
    print(startswith(str, "Hello"));
    print(endswith(str, "World!"));
    print(replace(str, "World", "Universe"));
    print(trim("  Hello  "));
    print(split("a,b,c", ","));
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

def test_dictionary_methods():
    # Test dictionary methods
    code = """
    var dict = dict();
    dict_put(dict, "name", "John");
    dict_put(dict, "age", 30);
    dict_put(dict, "city", "New York");
    
    print(dict_get(dict, "name"));
    print(dict_contains(dict, "age"));
    print(dict_contains(dict, "country"));
    print(dict_keys(dict));
    print(dict_values(dict));
    print(dict_items(dict));
    print(dict_size(dict));
    
    dict_remove(dict, "city");
    print(dict_size(dict));
    
    dict_clear(dict);
    print(dict_size(dict));
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
        if test_name == "string":
            test_string_operations()
        elif test_name == "dict":
            test_dictionary_operations()
        elif test_name == "array":
            test_array_operations()
        elif test_name == "type":
            test_type_operations()
        elif test_name == "yield":
            test_yield()
        elif test_name == "dynamic_var":
            test_dynamic_variables()
        elif test_name == "dynamic_func":
            test_dynamic_functions()
        elif test_name == "labels":
            test_labels_and_goto()
        elif test_name == "input":
            test_input_operations()
        elif test_name == "string_methods":
            test_string_methods()
        elif test_name == "dict_methods":
            test_dictionary_methods()
        else:
            print(f"Unknown test: {test_name}")
    else:
        print("Running all tests...")
        print("\n=== Testing String Operations ===")
        test_string_operations()
        print("\n=== Testing Dictionary Operations ===")
        test_dictionary_operations()
        print("\n=== Testing Array Operations ===")
        test_array_operations()
        print("\n=== Testing Type Operations ===")
        test_type_operations()
        print("\n=== Testing Yield ===")
        test_yield()
        print("\n=== Testing Dynamic Variables ===")
        test_dynamic_variables()
        print("\n=== Testing Dynamic Functions ===")
        test_dynamic_functions()
        print("\n=== Testing Labels and Goto ===")
        test_labels_and_goto()
        print("\n=== Testing Input Operations ===")
        test_input_operations()
        print("\n=== Testing String Methods ===")
        test_string_methods()
        print("\n=== Testing Dictionary Methods ===")
        test_dictionary_methods()
