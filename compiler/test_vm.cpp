#include "vasuki_vm.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <cstdio>

namespace fs = std::filesystem;

// Function to compile a Vasuki file to bytecode
bool compileVasukiFile(const std::string& inputFile, const std::string& outputFile) {
    // Use the Python compiler to generate bytecode
    std::cout << "Compiling " << inputFile << " to bytecode..." << std::endl;
    std::string command = "python3 ../compiler.py " + inputFile + " " + outputFile;
    int result = std::system(command.c_str());

    if (result != 0) {
        std::cerr << "Compilation failed. Make sure the Python compiler is properly set up." << std::endl;
        std::cerr << "Command used: " << command << std::endl;
        return false;
    }

    std::cout << "Compilation successful." << std::endl;
    return true;
}

// Function to test a single Vasuki file
bool testVasukiFile(const std::string& filePath) {
    std::cout << "\n=== Testing " << filePath << " ===\n" << std::endl;

    // Generate a temporary bytecode file
    std::string bytecodeFile = filePath + ".bytecode";

    // Compile the Vasuki file to bytecode
    if (!compileVasukiFile(filePath, bytecodeFile)) {
        std::cerr << "Failed to compile " << filePath << std::endl;
        return false;
    }

    try {
        // Create a VM instance
        vasuki::VasukiVM vm;

        // Load the bytecode
        vm.loadBytecode(bytecodeFile);

        // Dump the bytecode for debugging
        std::cout << "Bytecode for " << filePath << ":" << std::endl;
        vm.dumpBytecode();
        std::cout << std::endl;

        // Execute the bytecode
        std::cout << "Execution output:" << std::endl;
        vasuki::Value result = vm.execute();

        // Print the result if it's not null
        if (!result.isNull()) {
            std::cout << "\nResult: " << result.toString() << std::endl;
        }

        // Dump the final stack state
        std::cout << "\nFinal stack state:" << std::endl;
        vm.dumpStack();

        // Clean up the temporary bytecode file
        std::remove(bytecodeFile.c_str());

        return true;
    } catch (const std::exception& e) {
        std::cerr << "Error executing " << filePath << ": " << e.what() << std::endl;
        // Clean up the temporary bytecode file
        std::remove(bytecodeFile.c_str());
        return false;
    }
}

// Function to test all Vasuki files in a directory
void testAllVasukiFiles(const std::string& directory) {
    std::cout << "Testing all Vasuki files in " << directory << std::endl;

    int totalFiles = 0;
    int successfulFiles = 0;

    try {
        for (const auto& entry : fs::recursive_directory_iterator(directory)) {
            if (entry.is_regular_file() && entry.path().extension() == ".vasuki") {
                totalFiles++;
                if (testVasukiFile(entry.path().string())) {
                    successfulFiles++;
                }
                std::cout << "\n--------------------------------------------------\n" << std::endl;
            }
        }

        std::cout << "Test summary: " << successfulFiles << " of " << totalFiles << " files executed successfully." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error scanning directory: " << e.what() << std::endl;
    }
}

// Function to test a specific Vasuki file
void testSpecificFile(const std::string& filePath) {
    if (fs::exists(filePath) && fs::is_regular_file(filePath) && fs::path(filePath).extension() == ".vasuki") {
        testVasukiFile(filePath);
    } else {
        std::cerr << "Error: " << filePath << " is not a valid Vasuki file." << std::endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " [directory|file]" << std::endl;
        std::cout << "  If a directory is provided, all .vasuki files in that directory will be tested." << std::endl;
        std::cout << "  If a file is provided, only that file will be tested." << std::endl;
        std::cout << "  Default: Testing all files in ../presentation/" << std::endl;

        // Default to testing all files in the presentation directory
        testAllVasukiFiles("../presentation");
    } else {
        std::string path = argv[1];

        if (fs::is_directory(path)) {
            testAllVasukiFiles(path);
        } else {
            testSpecificFile(path);
        }
    }

    return 0;
}
