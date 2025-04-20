#include "vasuki_vm.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <cstdio>
#include <chrono>
#include <iomanip>

namespace fs = std::filesystem;

// Function to compile a Vasuki file to bytecode
bool compileVasukiFile(const std::string& inputFile, const std::string& outputFile, bool verbose = false) {
    if (verbose) {
        std::cout << "Compiling " << inputFile << " to bytecode..." << std::endl;
    }

    // Use the Python compiler to generate bytecode
    // Set up the Python path to include the parent directory
    std::string command = "PYTHONPATH=.. python3 ../compiler.py \"" + inputFile + "\" \"" + outputFile + "\"";
    int result = std::system(command.c_str());

    if (result != 0) {
        std::cerr << "Compilation failed for " << inputFile << std::endl;
        std::cerr << "Command used: " << command << std::endl;
        return false;
    }

    if (verbose) {
        std::cout << "Compilation successful." << std::endl;
    }

    return true;
}

// Function to run a Vasuki file
bool runVasukiFile(const std::string& filePath, bool verbose = false, bool dumpBytecode = false) {
    std::cout << "\n=== Running " << filePath << " ===\n" << std::endl;

    // Generate a temporary bytecode file
    std::string bytecodeFile = filePath + ".bytecode";

    // Compile the Vasuki file to bytecode
    if (!compileVasukiFile(filePath, bytecodeFile, verbose)) {
        return false;
    }

    try {
        // Create a VM instance
        vasuki::VasukiVM vm;

        // Load the bytecode
        vm.loadBytecode(bytecodeFile);

        // Dump the bytecode if requested
        if (dumpBytecode) {
            std::cout << "Bytecode for " << filePath << ":" << std::endl;
            vm.dumpBytecode();
            std::cout << std::endl;
        }

        // Execute the bytecode
        std::cout << "Execution output:" << std::endl;
        auto start = std::chrono::high_resolution_clock::now();
        vasuki::Value result = vm.execute();
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end - start;

        // Print the result if it's not null
        if (!result.isNull()) {
            std::cout << "\nResult: " << result.toString() << std::endl;
        }

        // Print execution time
        std::cout << "\nExecution time: " << std::fixed << std::setprecision(6) << elapsed.count() << " seconds" << std::endl;

        // Dump the final stack state if verbose
        if (verbose) {
            std::cout << "\nFinal stack state:" << std::endl;
            vm.dumpStack();
        }

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

// Function to run all Vasuki files in a directory
void runAllVasukiFiles(const std::string& directory, bool verbose = false, bool dumpBytecode = false) {
    std::cout << "Running all Vasuki files in " << directory << std::endl;

    int totalFiles = 0;
    int successfulFiles = 0;

    try {
        for (const auto& entry : fs::recursive_directory_iterator(directory)) {
            if (entry.is_regular_file() && entry.path().extension() == ".vasuki") {
                totalFiles++;
                if (runVasukiFile(entry.path().string(), verbose, dumpBytecode)) {
                    successfulFiles++;
                }
                std::cout << "\n--------------------------------------------------\n" << std::endl;
            }
        }

        std::cout << "Summary: " << successfulFiles << " of " << totalFiles << " files executed successfully." << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error scanning directory: " << e.what() << std::endl;
    }
}

int main(int argc, char* argv[]) {
    bool verbose = false;
    bool dumpBytecode = false;
    std::string path;

    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "-v" || arg == "--verbose") {
            verbose = true;
        } else if (arg == "-d" || arg == "--dump-bytecode") {
            dumpBytecode = true;
        } else if (arg == "-h" || arg == "--help") {
            std::cout << "Usage: " << argv[0] << " [options] [directory|file]" << std::endl;
            std::cout << "Options:" << std::endl;
            std::cout << "  -v, --verbose        Enable verbose output" << std::endl;
            std::cout << "  -d, --dump-bytecode  Dump bytecode before execution" << std::endl;
            std::cout << "  -h, --help           Show this help message" << std::endl;
            std::cout << std::endl;
            std::cout << "If a directory is provided, all .vasuki files in that directory will be run." << std::endl;
            std::cout << "If a file is provided, only that file will be run." << std::endl;
            std::cout << "Default: Running all files in ../presentation/" << std::endl;
            return 0;
        } else {
            path = arg;
        }
    }

    // Default to running all files in the presentation directory
    if (path.empty()) {
        path = "../presentation";
    }

    if (fs::is_directory(path)) {
        runAllVasukiFiles(path, verbose, dumpBytecode);
    } else {
        runVasukiFile(path, verbose, dumpBytecode);
    }

    return 0;
}
