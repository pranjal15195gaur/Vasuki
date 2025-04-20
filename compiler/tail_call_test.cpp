#include "vasuki_vm.h"
#include <iostream>
#include <vector>
#include <string>
#include <chrono>

int main() {
    // Create a VM
    vasuki::VasukiVM vm;

    // Create bytecode for a recursive countdown function
    std::vector<uint8_t> bytecode;
    std::vector<vasuki::Value> constants;
    std::vector<std::string> names = {
        "Testing tail call optimization...",
        "countdown",
        "n",
        "Counting down: ",
        "Result: "
    };

    // OpCodes
    const uint8_t HALT = 0;
    const uint8_t PUSH_INT = 2;
    const uint8_t PUSH_STRING = 4;
    const uint8_t GET_LOCAL = 29;
    const uint8_t JUMP = 32;
    const uint8_t JUMP_IF_FALSE = 33;
    const uint8_t CALL = 35;
    const uint8_t TAIL_CALL = 46;
    const uint8_t RETURN = 36;
    const uint8_t FUNCTION = 37;
    const uint8_t GET_GLOBAL = 26;
    const uint8_t PRINT = 42;
    const uint8_t LTE = 20;
    const uint8_t SUB = 11;

    // Push a string
    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Print the string
    bytecode.push_back(PRINT);

    // Define a countdown function
    bytecode.push_back(FUNCTION);
    bytecode.push_back(1);
    bytecode.push_back(0);
    bytecode.push_back(20);  // Start position
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(1);   // 1 parameter
    bytecode.push_back(2);
    bytecode.push_back(0);   // Parameter name index

    // Jump over function body
    bytecode.push_back(JUMP);
    bytecode.push_back(40);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Function body starts here (position 20)
    // Print n
    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(3);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);

    bytecode.push_back(GET_LOCAL);
    bytecode.push_back(2);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);

    // if n <= 0 return 0
    bytecode.push_back(GET_LOCAL);
    bytecode.push_back(2);
    bytecode.push_back(0);

    bytecode.push_back(PUSH_INT);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(LTE);

    bytecode.push_back(JUMP_IF_FALSE);
    bytecode.push_back(10);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Return 0
    bytecode.push_back(PUSH_INT);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(RETURN);

    // else return countdown(n-1)
    bytecode.push_back(GET_GLOBAL);
    bytecode.push_back(1);
    bytecode.push_back(0);

    bytecode.push_back(GET_LOCAL);
    bytecode.push_back(2);
    bytecode.push_back(0);

    bytecode.push_back(PUSH_INT);
    bytecode.push_back(1);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(SUB);

    // Call countdown(n-1) with tail call optimization
    bytecode.push_back(TAIL_CALL);
    bytecode.push_back(1);

    bytecode.push_back(RETURN);

    // Main program continues here (position 60)
    // Call countdown(5)
    bytecode.push_back(GET_GLOBAL);
    bytecode.push_back(1);
    bytecode.push_back(0);

    bytecode.push_back(PUSH_INT);
    bytecode.push_back(5);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(CALL);
    bytecode.push_back(1);

    // Print the result
    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(4);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);
    bytecode.push_back(PRINT);

    // Push a value for the main program's implicit return
    bytecode.push_back(PUSH_INT);
    bytecode.push_back(42);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Halt
    bytecode.push_back(HALT);

    // Load the bytecode
    vm.loadBytecodeFromMemory(bytecode, constants, names);

    // Execute the bytecode
    std::cout << "Executing bytecode..." << std::endl;

    // First run to define the function
    vm.execute();

    // Reset the bytecode and run again
    bytecode.clear();

    // Call countdown(5)
    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);

    bytecode.push_back(GET_GLOBAL);
    bytecode.push_back(1);
    bytecode.push_back(0);

    bytecode.push_back(PUSH_INT);
    bytecode.push_back(5);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    bytecode.push_back(CALL);
    bytecode.push_back(1);

    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(4);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);
    bytecode.push_back(PRINT);

    bytecode.push_back(HALT);

    // Load the new bytecode
    vm.loadBytecodeFromMemory(bytecode, constants, names);

    // Execute the bytecode
    vasuki::Value result = vm.execute();

    // Print the result
    std::cout << "Final result: " << result.toString() << std::endl;

    return 0;
}
