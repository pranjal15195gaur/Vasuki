#include "vasuki_vm.h"
#include <iostream>
#include <vector>
#include <string>

int main(int argc, char* argv[]) {
    // Create a VM instance
    vasuki::VasukiVM vm;

    // Bytecode file to load
    std::string bytecodeFile = "test_bytecode.bin";

    // If a file is specified as an argument, use that instead
    if (argc > 1) {
        bytecodeFile = argv[1];
    }

    // Load the bytecode
    try {
        vm.loadBytecode(bytecodeFile);
    } catch (const std::exception& e) {
        std::cerr << "Error loading bytecode: " << e.what() << std::endl;
        return 1;
    }

    // Check if verbose mode is enabled
    bool verbose = false;
    for (int i = 2; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "-v" || arg == "--verbose") {
            verbose = true;
            break;
        }
    }

    // Dump the bytecode if verbose mode is enabled
    if (verbose) {
        std::cout << "Bytecode:" << std::endl;
        vm.dumpBytecode();
        std::cout << std::endl;
    }

    // Execute the bytecode
    // Add markers for output extraction, but they will be removed by the script
    std::cout << "-------------------" << std::endl;
    vasuki::Value result = vm.execute();
    std::cout << "-------------------" << std::endl;

    // Print the result and stack state if verbose mode is enabled
    if (verbose) {
        std::cout << "\nFinal result: " << result.toString() << std::endl;
        std::cout << "\nFinal stack state:" << std::endl;
        vm.dumpStack();
    }

    return 0;
}
