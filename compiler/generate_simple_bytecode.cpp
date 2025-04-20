#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <output_file> <message>" << std::endl;
        return 1;
    }

    std::string outputFile = argv[1];
    std::string message = argv[2];

    // Create bytecode
    std::vector<uint8_t> bytecode;

    // PUSH_STRING 0
    bytecode.push_back(4);  // PUSH_STRING
    bytecode.push_back(0);  // String index (low byte)
    bytecode.push_back(0);  // String index (high byte)

    // PRINT
    bytecode.push_back(42); // PRINT

    // PUSH_INT 42
    bytecode.push_back(2);  // PUSH_INT
    bytecode.push_back(42); // Value (low byte)
    bytecode.push_back(0);  // Value (byte 2)
    bytecode.push_back(0);  // Value (byte 3)
    bytecode.push_back(0);  // Value (high byte)

    // HALT
    bytecode.push_back(0);  // HALT

    // Create names
    std::vector<std::string> names = {message};

    // Write bytecode to file
    std::ofstream file(outputFile, std::ios::binary);
    if (!file) {
        std::cerr << "Error: Could not open file " << outputFile << " for writing" << std::endl;
        return 1;
    }

    // Write bytecode size
    uint32_t bytecodeSize = bytecode.size();
    file.write(reinterpret_cast<char*>(&bytecodeSize), sizeof(bytecodeSize));

    // Write bytecode
    file.write(reinterpret_cast<char*>(bytecode.data()), bytecode.size());

    // Write constants size (0)
    uint32_t constantsSize = 0;
    file.write(reinterpret_cast<char*>(&constantsSize), sizeof(constantsSize));

    // Write names size
    uint32_t namesSize = names.size();
    file.write(reinterpret_cast<char*>(&namesSize), sizeof(namesSize));

    // Write names
    for (const auto& name : names) {
        uint32_t nameSize = name.size();
        file.write(reinterpret_cast<char*>(&nameSize), sizeof(nameSize));
        file.write(name.c_str(), nameSize);
    }

    file.close();
    std::cout << "Bytecode written to " << outputFile << std::endl;

    return 0;
}
