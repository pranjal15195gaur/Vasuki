from top import e, dynamic_functions
from parser import parse
import unittest
import io
from contextlib import redirect_stdout

class TestDynamicFunctions(unittest.TestCase):
    def setUp(self):
        # Clear dynamic functions before each test
        dynamic_functions.clear()

    def test_basic_dynamic_function(self):
        code = "dynamic def test() { return 42; }; test()"
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 42)
        self.assertTrue("test" in dynamic_functions)

    def test_dynamic_function_with_params(self):
        code = """
        dynamic def add(a, b) {
            return a + b;
        };
        add(5, 3)
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 8)
        self.assertTrue("add" in dynamic_functions)

    def test_dynamic_function_shadowing(self):
        code = """
        dynamic def func() { return 1; };
        def func() { return 2; };
        func()
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 2)  # Static function shadows dynamic
        self.assertTrue("func" in dynamic_functions)

    def test_dynamic_function_in_nested_scope(self):
        code = """
        def outer() {
            dynamic def inner_func() { return 42; };
            return inner_func();
        };
        outer()
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 42)
        self.assertTrue("inner_func" in dynamic_functions)

    def test_dynamic_function_override(self):
        code = """
        dynamic def calc(a, b) { return a + b; };

        def test() {
            dynamic def calc(a, b) { return a * b; };
            return calc(5, 3);
        };

        var result1 = test();
        var result2 = calc(5, 3);
        result1 + result2
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 30)  # 15 (5*3) + 15 (5*3)

    def test_dynamic_function_recursion(self):
        code = """
        dynamic def factorial(n) {
            if (n <= 1) {
                return 1;
            };
            return n * factorial(n - 1);
        };

        factorial(5)
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 120)

    def test_dynamic_function_mutual_recursion(self):
        code = """
        dynamic def is_even(n) {
            if (n == 0) { return 1; };
            return is_odd(n - 1);
        };

        dynamic def is_odd(n) {
            if (n == 0) { return 0; };
            return is_even(n - 1);
        };

        is_even(10)
        """
        ast = parse(code)
        result = e(ast)
        self.assertEqual(result, 1)  # 10 is even

    def test_dynamic_function_print(self):
        f = io.StringIO()
        with redirect_stdout(f):
            code = """
            dynamic def print_message() {
                print(42);
            };
            print_message();
            """
            ast = parse(code)
            e(ast)
        output = f.getvalue()
        self.assertEqual(output, "42\n")

if __name__ == "__main__":
    unittest.main()
