#include "vasuki_vm.h"
#include <iostream>
#include <vector>
#include <string>
#include <chrono>

// Function to measure execution time
template<typename Func>
double measureExecutionTime(Func func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    return elapsed.count();
}

// Function to create a VM with a recursive countdown function
void setupCountdownVM(vasuki::VasukiVM& vm, bool useTailCall, int countdownFrom = 1000) {
    // Create bytecode for a recursive countdown function
    std::vector<uint8_t> bytecode;

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

    bytecode.push_back(GET_LOCAL);
    bytecode.push_back(2);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);
    bytecode.push_back(PRINT);

    // if n <= 0 return n
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
    bytecode.push_back(15);
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Return n
    bytecode.push_back(GET_LOCAL);
    bytecode.push_back(2);
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

    // Call countdown(n-1)
    if (useTailCall) {
        bytecode.push_back(TAIL_CALL);
    } else {
        bytecode.push_back(CALL);
    }
    bytecode.push_back(1);

    // Add return for tail call
    if (useTailCall) {
        bytecode.push_back(RETURN);
    }

    // Main program continues here (position 50)
    // Call countdown with a large number
    bytecode.push_back(PUSH_STRING);
    bytecode.push_back(4);
    bytecode.push_back(0);

    bytecode.push_back(PRINT);

    bytecode.push_back(GET_GLOBAL);
    bytecode.push_back(1);
    bytecode.push_back(0);

    bytecode.push_back(PUSH_INT);
    bytecode.push_back(countdownFrom & 0xFF);  // Lower 8 bits
    bytecode.push_back((countdownFrom >> 8) & 0xFF);  // Next 8 bits
    bytecode.push_back((countdownFrom >> 16) & 0xFF);  // Next 8 bits
    bytecode.push_back((countdownFrom >> 24) & 0xFF);  // Upper 8 bits

    bytecode.push_back(CALL);
    bytecode.push_back(1);

    bytecode.push_back(PRINT);

    bytecode.push_back(HALT);

    // Create constants
    std::vector<vasuki::Value> constants;

    // Create names
    std::vector<std::string> names = {
        "Testing tail call optimization...",
        "countdown",
        "n",
        "Countdown: ",
        useTailCall ? "Using tail call optimization" : "Without tail call optimization"
    };

    // Load the bytecode
    vm.loadBytecodeFromMemory(bytecode, constants, names);
}

int main(int argc, char* argv[]) {
    // Parse command line arguments
    int countdownFrom = 1000;
    if (argc > 1) {
        countdownFrom = std::stoi(argv[1]);
    }

    // Create VMs
    vasuki::VasukiVM vmWithoutTailCall;
    vasuki::VasukiVM vmWithTailCall;

    // Setup VMs
    setupCountdownVM(vmWithoutTailCall, false);
    setupCountdownVM(vmWithTailCall, true);

    // We need to recreate the bytecode with the correct countdown value
    setupCountdownVM(vmWithoutTailCall, false, countdownFrom);
    setupCountdownVM(vmWithTailCall, true, countdownFrom);

    // Run without tail call optimization
    std::cout << "Running countdown(" << countdownFrom << ") without tail call optimization..." << std::endl;
    double timeWithoutTailCall = 0;
    try {
        timeWithoutTailCall = measureExecutionTime([&]() {
            vmWithoutTailCall.execute();
        });
        std::cout << "Time without tail call optimization: " << timeWithoutTailCall << " seconds" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error without tail call optimization: " << e.what() << std::endl;
    }

    // Run with tail call optimization
    std::cout << "\nRunning countdown(" << countdownFrom << ") with tail call optimization..." << std::endl;
    double timeWithTailCall = 0;
    try {
        timeWithTailCall = measureExecutionTime([&]() {
            vmWithTailCall.execute();
        });
        std::cout << "Time with tail call optimization: " << timeWithTailCall << " seconds" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error with tail call optimization: " << e.what() << std::endl;
    }

    // Compare results
    if (timeWithoutTailCall > 0 && timeWithTailCall > 0) {
        double speedup = timeWithoutTailCall / timeWithTailCall;
        std::cout << "\nTail call optimization speedup: " << speedup << "x" << std::endl;
    }

    return 0;
}
