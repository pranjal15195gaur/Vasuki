#include "vasuki_vm.h"
#include <iostream>
#include <vector>
#include <string>

int main() {
    // Create a VM instance
    vasuki::VasukiVM vm;

    // Create bytecode manually to simulate a function with missing semicolon
    std::vector<uint8_t> bytecode = {
        // Define a function 'subtract' that returns x - y (with missing semicolon)
        static_cast<uint8_t>(vasuki::OpCode::FUNCTION), 0, 0,  // Function name index 0
        10, 0, 0, 0,  // Start position (10)
        2,            // 2 parameters
        1, 0,         // Parameter 1 name index (1)
        2, 0,         // Parameter 2 name index (2)

        // Jump over function body
        static_cast<uint8_t>(vasuki::OpCode::JUMP), 14, 0, 0, 0,  // Jump to position 24

        // Function body starts here (position 10)
        static_cast<uint8_t>(vasuki::OpCode::GET_LOCAL), 1, 0,  // Get parameter x
        static_cast<uint8_t>(vasuki::OpCode::GET_LOCAL), 2, 0,  // Get parameter y
        static_cast<uint8_t>(vasuki::OpCode::SUB),              // Subtract
        static_cast<uint8_t>(vasuki::OpCode::RETURN),           // Return (simulating missing semicolon)

        // Main program starts here (position 18)
        // Push the function name
        static_cast<uint8_t>(vasuki::OpCode::GET_GLOBAL), 0, 0,  // Get function 'subtract'

        // Push arguments
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 10, 0, 0, 0,  // Push 10
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 3, 0, 0, 0,   // Push 3

        // Call the function
        static_cast<uint8_t>(vasuki::OpCode::CALL), 2,  // Call with 2 arguments

        // Print the result
        static_cast<uint8_t>(vasuki::OpCode::PRINT),

        // Push a value for the main program's implicit return
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 42, 0, 0, 0,  // Push 42

        // Halt (the VM will return the top value on the stack)
        static_cast<uint8_t>(vasuki::OpCode::HALT)
    };

    // Create constants
    std::vector<vasuki::Value> constants;

    // Create names (strings)
    std::vector<std::string> names = {
        "subtract",  // Function name (index 0)
        "x",         // Parameter 1 (index 1)
        "y"          // Parameter 2 (index 2)
    };

    // Load the bytecode
    vm.loadBytecodeFromMemory(bytecode, constants, names);

    // Dump the bytecode
    std::cout << "Bytecode:" << std::endl;
    vm.dumpBytecode();
    std::cout << std::endl;

    // Execute the bytecode
    std::cout << "Execution output:" << std::endl;
    vasuki::Value result = vm.execute();

    // Print the result
    std::cout << "\nFinal result: " << result.toString() << std::endl;

    // Dump the final stack
    std::cout << "\nFinal stack state:" << std::endl;
    vm.dumpStack();

    return 0;
}
