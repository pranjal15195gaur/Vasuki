#include "vasuki_vm.h"
#include <iostream>
#include <vector>
#include <string>

int main() {
    // Create a VM instance
    vasuki::VasukiVM vm;
    
    // Create bytecode manually for a simple test of the missing semicolon feature
    std::vector<uint8_t> bytecode = {
        // Push two integers
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 10, 0, 0, 0,  // Push 10
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 5, 0, 0, 0,   // Push 5
        
        // Subtract them (10 - 5 = 5)
        static_cast<uint8_t>(vasuki::OpCode::SUB),
        
        // Print the result
        static_cast<uint8_t>(vasuki::OpCode::PRINT),
        
        // Push a string
        static_cast<uint8_t>(vasuki::OpCode::PUSH_STRING), 0, 0,  // String index 0
        
        // Print the string
        static_cast<uint8_t>(vasuki::OpCode::PRINT),
        
        // Push another value (42) - this simulates the last expression without a semicolon
        static_cast<uint8_t>(vasuki::OpCode::PUSH_INT), 42, 0, 0, 0,  // Push 42
        
        // Halt - the VM should return the top value on the stack (42)
        static_cast<uint8_t>(vasuki::OpCode::HALT)
    };
    
    // Create constants
    std::vector<vasuki::Value> constants;
    
    // Create names (strings)
    std::vector<std::string> names = {
        "This is a test of the missing semicolon feature"
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
