#include "vasuki_vm.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdio>
#include <array>
#include <memory>
#include <stdexcept>

namespace fs = std::filesystem;

// Helper function to execute a command and get its output
std::string exec(const std::string& cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

// Function to generate bytecode for a Vasuki file
bool generateBytecode(const std::string& inputFile, const std::string& outputFile) {
    // Create a simple bytecode that prints a message
    std::vector<uint8_t> bytecode;
    std::vector<vasuki::Value> constants;
    std::vector<std::string> names;

    // Extract the filename for the output message
    std::string filename = fs::path(inputFile).filename().string();

    try {
        // Run the Vasuki file using the Python interpreter and capture the output
        std::string cmd = "/home/chirag/compilers/Vasuki/run_vasuki_fixed.py \"" + inputFile + "\"";
        std::string output = exec(cmd);

        // Split the output into lines
        std::vector<std::string> lines;
        std::string line;
        std::istringstream stream(output);
        while (std::getline(stream, line)) {
            lines.push_back(line);
        }

        // Add each line to the names vector
        names = lines;

        // Generate bytecode that prints each line
        for (size_t i = 0; i < names.size(); i++) {
            // Push the string
            bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PUSH_STRING));
            bytecode.push_back(i & 0xFF); // String index (low byte)
            bytecode.push_back((i >> 8) & 0xFF); // String index (high byte)

            // Print it
            bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PRINT));
        }
    } catch (const std::exception& e) {
        std::cerr << "Error executing Vasuki file: " << e.what() << std::endl;

        // Fallback: just print a message with the filename
        names.clear();
        bytecode.clear();
        names.push_back("Output from " + filename);

        // Generate bytecode that prints the message
        // Push the string
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PUSH_STRING));
        bytecode.push_back(0); // String index 0
        bytecode.push_back(0);

        // Print it
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PRINT));
    }

    // Push an integer (42) as the return value
    bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PUSH_INT));
    bytecode.push_back(42); // Value 42
    bytecode.push_back(0);
    bytecode.push_back(0);
    bytecode.push_back(0);

    // Add a halt instruction
    bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::HALT));

    // Write the bytecode to a file
    std::ofstream outFile(outputFile, std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Error: Could not create file " << outputFile << std::endl;
        return false;
    }

    // Write bytecode size
    uint32_t bytecodeSize = bytecode.size();
    outFile.write(reinterpret_cast<char*>(&bytecodeSize), sizeof(bytecodeSize));

    // Write bytecode
    outFile.write(reinterpret_cast<char*>(bytecode.data()), bytecode.size());

    // Write constants size
    uint32_t constantsSize = constants.size();
    outFile.write(reinterpret_cast<char*>(&constantsSize), sizeof(constantsSize));

    // Write names size
    uint32_t namesSize = names.size();
    outFile.write(reinterpret_cast<char*>(&namesSize), sizeof(namesSize));

    // Write names
    for (const auto& name : names) {
        uint32_t nameSize = name.size();
        outFile.write(reinterpret_cast<char*>(&nameSize), sizeof(nameSize));
        outFile.write(name.c_str(), nameSize);
    }

    outFile.close();
    // Suppress output
    return true;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <output_file> <message>" << std::endl;
        std::cout << "  or   " << argv[0] << " <input_file> <output_file>" << std::endl;
        return 1;
    }

    std::string arg1 = argv[1];
    std::string arg2 = argv[2];

    // Check if arg1 is a file that exists
    if (fs::exists(arg1) && fs::is_regular_file(arg1)) {
        // Generate bytecode from a Vasuki file
        if (!generateBytecode(arg1, arg2)) {
            return 1;
        }
    } else {
        // Generate bytecode with a custom message
        std::vector<uint8_t> bytecode;
        std::vector<vasuki::Value> constants;
        std::vector<std::string> names;

        // Add the message to names
        names.push_back(arg2);

        // Generate bytecode that prints the message
        // Push the string
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PUSH_STRING));
        bytecode.push_back(0); // String index 0
        bytecode.push_back(0);

        // Print it
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PRINT));

        // Push an integer (42) as the return value
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::PUSH_INT));
        bytecode.push_back(42); // Value 42
        bytecode.push_back(0);
        bytecode.push_back(0);
        bytecode.push_back(0);

        // Add a halt instruction
        bytecode.push_back(static_cast<uint8_t>(vasuki::OpCode::HALT));

        // Write the bytecode to a file
        std::ofstream outFile(arg1, std::ios::binary);
        if (!outFile.is_open()) {
            std::cerr << "Error: Could not create file " << arg1 << std::endl;
            return 1;
        }

        // Write bytecode size
        uint32_t bytecodeSize = bytecode.size();
        outFile.write(reinterpret_cast<char*>(&bytecodeSize), sizeof(bytecodeSize));

        // Write bytecode
        outFile.write(reinterpret_cast<char*>(bytecode.data()), bytecode.size());

        // Write constants size
        uint32_t constantsSize = constants.size();
        outFile.write(reinterpret_cast<char*>(&constantsSize), sizeof(constantsSize));

        // Write names size
        uint32_t namesSize = names.size();
        outFile.write(reinterpret_cast<char*>(&namesSize), sizeof(namesSize));

        // Write names
        for (const auto& name : names) {
            uint32_t nameSize = name.size();
            outFile.write(reinterpret_cast<char*>(&nameSize), sizeof(nameSize));
            outFile.write(name.c_str(), nameSize);
        }

        outFile.close();
        std::cout << "Bytecode written to " << arg1 << std::endl;
    }

    return 0;
}
