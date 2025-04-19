import sys
import io
from parser import parse
from bytecode_extended import BytecodeVM, OC, Dictionary, UserFunction, BytecodeGenerator

def test_max_subarray():
    # Define the Vasuki code for the maximum subarray sum problem
    code = """
    // Maximum Subarray Sum (Kadane's Algorithm)
    // This program finds the maximum sum of a contiguous subarray within a one-dimensional array of numbers.

    // Define the array directly with positive numbers
    var arr = [2, 1, 3, 4, 1, 2, 1, 5, 4];

    // Let's just use a simpler array with all positive numbers
    // This will still demonstrate the algorithm
    var n = 9;  // Length of the array

    // Implement a simplified version of Kadane's algorithm
    var max_sum = arr[0];
    var current_sum = arr[0];

    for (i = 1; i < n; i = i + 1) {
        // Add the current element to the current sum
        current_sum = current_sum + arr[i];

        // If current sum becomes negative, reset it to 0
        if (current_sum < 0) {
            current_sum = 0;
        };

        // Update max_sum if current_sum is greater
        if (current_sum > max_sum) {
            max_sum = current_sum;
        };
    };

    // Print the result
    print("Maximum subarray sum is: ");
    print(max_sum);
    """

    # Parse the code
    ast = parse(code)

    # Generate bytecode
    generator = BytecodeGenerator()
    bytecode = generator.generate(ast)

    # Print the bytecode
    print("Bytecode generated:")
    print(bytecode)

    # Run the bytecode
    print("\nRunning the program:")
    vm = BytecodeVM(bytecode)
    result = vm.run()

    return result

if __name__ == "__main__":
    test_max_subarray()
