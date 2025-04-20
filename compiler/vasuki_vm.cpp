// vasuki_vm.cpp
#include "vasuki_vm.h"
#include <cmath>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <iomanip>

namespace vasuki {

// Value methods
std::string Value::toString() const {
    if (isNull()) {
        return "null";
    } else if (isBool()) {
        return getBool() ? "true" : "false";
    } else if (isInt()) {
        return std::to_string(getInt());
    } else if (isFloat()) {
        std::ostringstream ss;
        ss << std::fixed << std::setprecision(6) << getFloat();
        std::string str = ss.str();
        // Remove trailing zeros
        str.erase(str.find_last_not_of('0') + 1, std::string::npos);
        if (str.back() == '.') {
            str.pop_back();
        }
        return str;
    } else if (isString()) {
        return getString();
    } else if (isArray()) {
        std::ostringstream ss;
        ss << "[";
        auto arr = getArray();
        for (size_t i = 0; i < arr->size(); i++) {
            if (i > 0) ss << ", ";
            ss << (*arr)[i].toString();
        }
        ss << "]";
        return ss.str();
    } else if (isDict()) {
        std::ostringstream ss;
        ss << "{";
        auto dict = getDict();
        bool first = true;
        for (const auto& [key, val] : *dict) {
            if (!first) ss << ", ";
            first = false;
            ss << key << ": " << val.toString();
        }
        ss << "}";
        return ss.str();
    } else if (isFunction()) {
        return "<function>";
    }
    return "<unknown>";
}

Value Value::operator+(const Value& other) const {
    if (isString() || other.isString()) {
        return Value(toString() + other.toString());
    } else if (isFloat() || other.isFloat()) {
        double a = isNumber() ? (isInt() ? getInt() : getFloat()) : 0;
        double b = other.isNumber() ? (other.isInt() ? other.getInt() : other.getFloat()) : 0;
        return Value(a + b);
    } else if (isInt() && other.isInt()) {
        return Value(getInt() + other.getInt());
    } else if (isArray() && other.isArray()) {
        auto result = std::make_shared<std::vector<Value>>(*getArray());
        auto otherArr = other.getArray();
        result->insert(result->end(), otherArr->begin(), otherArr->end());
        return Value(*result);
    }
    throw std::runtime_error("Cannot add values of these types");
}

Value Value::operator-(const Value& other) const {
    if (isFloat() || other.isFloat()) {
        double a = isNumber() ? (isInt() ? getInt() : getFloat()) : 0;
        double b = other.isNumber() ? (other.isInt() ? other.getInt() : other.getFloat()) : 0;
        return Value(a - b);
    } else if (isInt() && other.isInt()) {
        return Value(getInt() - other.getInt());
    }
    throw std::runtime_error("Cannot subtract values of these types");
}

Value Value::operator*(const Value& other) const {
    if (isFloat() || other.isFloat()) {
        double a = isNumber() ? (isInt() ? getInt() : getFloat()) : 0;
        double b = other.isNumber() ? (other.isInt() ? other.getInt() : other.getFloat()) : 0;
        return Value(a * b);
    } else if (isInt() && other.isInt()) {
        return Value(getInt() * other.getInt());
    } else if (isString() && other.isInt()) {
        std::string result;
        std::string str = getString();
        int64_t count = other.getInt();
        for (int64_t i = 0; i < count; i++) {
            result += str;
        }
        return Value(result);
    }
    throw std::runtime_error("Cannot multiply values of these types");
}

Value Value::operator/(const Value& other) const {
    if (other.isNumber() && (other.isInt() ? other.getInt() == 0 : other.getFloat() == 0)) {
        throw std::runtime_error("Division by zero");
    }

    if (isFloat() || other.isFloat()) {
        double a = isNumber() ? (isInt() ? getInt() : getFloat()) : 0;
        double b = other.isNumber() ? (other.isInt() ? other.getInt() : other.getFloat()) : 0;
        return Value(a / b);
    } else if (isInt() && other.isInt()) {
        return Value(getInt() / other.getInt());
    }
    throw std::runtime_error("Cannot divide values of these types");
}

Value Value::operator%(const Value& other) const {
    if (other.isNumber() && (other.isInt() ? other.getInt() == 0 : other.getFloat() == 0)) {
        throw std::runtime_error("Modulo by zero");
    }

    if (isInt() && other.isInt()) {
        return Value(getInt() % other.getInt());
    } else if (isFloat() || other.isFloat()) {
        double a = isNumber() ? (isInt() ? getInt() : getFloat()) : 0;
        double b = other.isNumber() ? (other.isInt() ? other.getInt() : other.getFloat()) : 0;
        return Value(std::fmod(a, b));
    }
    throw std::runtime_error("Cannot perform modulo on values of these types");
}

bool Value::operator==(const Value& other) const {
    if (isNull() && other.isNull()) return true;
    if (isBool() && other.isBool()) return getBool() == other.getBool();
    if (isInt() && other.isInt()) return getInt() == other.getInt();
    if (isFloat() && other.isFloat()) return getFloat() == other.getFloat();
    if (isInt() && other.isFloat()) return getInt() == other.getFloat();
    if (isFloat() && other.isInt()) return getFloat() == other.getInt();
    if (isString() && other.isString()) return getString() == other.getString();
    return false;
}

bool Value::operator!=(const Value& other) const {
    return !(*this == other);
}

bool Value::operator<(const Value& other) const {
    if (isInt() && other.isInt()) return getInt() < other.getInt();
    if (isFloat() && other.isFloat()) return getFloat() < other.getFloat();
    if (isInt() && other.isFloat()) return getInt() < other.getFloat();
    if (isFloat() && other.isInt()) return getFloat() < other.getInt();
    if (isString() && other.isString()) return getString() < other.getString();
    throw std::runtime_error("Cannot compare values of these types");
}

bool Value::operator<=(const Value& other) const {
    return *this < other || *this == other;
}

bool Value::operator>(const Value& other) const {
    return !(*this <= other);
}

bool Value::operator>=(const Value& other) const {
    return !(*this < other);
}

// Environment methods
void Environment::declare(const std::string& name, const Value& value) {
    variables[name] = value;
}

void Environment::assign(const std::string& name, const Value& value) {
    if (variables.find(name) != variables.end()) {
        variables[name] = value;
    } else if (parent) {
        parent->assign(name, value);
    } else {
        throw std::runtime_error("Variable '" + name + "' not defined");
    }
}

Value Environment::lookup(const std::string& name) {
    if (variables.find(name) != variables.end()) {
        return variables[name];
    } else if (parent) {
        return parent->lookup(name);
    } else {
        throw std::runtime_error("Variable '" + name + "' not defined");
    }
}

bool Environment::contains(const std::string& name) const {
    if (variables.find(name) != variables.end()) {
        return true;
    } else if (parent) {
        return parent->contains(name);
    }
    return false;
}

// VasukiVM methods
VasukiVM::VasukiVM() : globalEnv(std::make_shared<Environment>()), ip(0) {
    setupBuiltins();
}

// Helper methods
Value VasukiVM::pop() {
    if (stack.empty()) {
        std::cerr << "Warning: Stack underflow, returning null" << std::endl;
        return Value(nullptr);
    }
    Value value = stack.back();
    stack.pop_back();
    return value;
}

void VasukiVM::push(const Value& value) {
    stack.push_back(value);
}

uint8_t VasukiVM::readByte() {
    if (static_cast<size_t>(ip) >= bytecode.size()) {
        throw std::runtime_error("Bytecode read out of bounds");
    }
    // Direct access for better performance
    return bytecode[ip++];
}

uint16_t VasukiVM::readShort() {
    uint16_t value = readByte();
    value |= (static_cast<uint16_t>(readByte()) << 8);
    return value;
}

int32_t VasukiVM::readInt() {
    // Optimized version that reads 4 bytes at once when possible
    if (static_cast<size_t>(ip + 3) < bytecode.size()) {
        int32_t value = bytecode[ip] |
                      (static_cast<int32_t>(bytecode[ip + 1]) << 8) |
                      (static_cast<int32_t>(bytecode[ip + 2]) << 16) |
                      (static_cast<int32_t>(bytecode[ip + 3]) << 24);
        ip += 4;
        return value;
    } else {
        // Fallback to byte-by-byte reading
        int32_t value = readByte();
        value |= (static_cast<int32_t>(readByte()) << 8);
        value |= (static_cast<int32_t>(readByte()) << 16);
        value |= (static_cast<int32_t>(readByte()) << 24);
        return value;
    }
}

Value VasukiVM::readConstant() {
    uint8_t index = readByte();
    if (index >= constants.size()) {
        throw std::runtime_error("Constant index out of bounds");
    }
    return constants[index];
}

std::string VasukiVM::readString() {
    uint16_t index = readShort();
    if (index >= names.size()) {
        throw std::runtime_error("String index out of bounds");
    }
    return names[index];
}

void VasukiVM::loadBytecode(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Error: Could not open file: " + filename);
    }

    // Read bytecode size
    uint32_t bytecodeSize;
    file.read(reinterpret_cast<char*>(&bytecodeSize), sizeof(bytecodeSize));

    // Read bytecode
    bytecode.resize(bytecodeSize);
    file.read(reinterpret_cast<char*>(bytecode.data()), bytecodeSize);

    // Read constants size
    uint32_t constantsSize;
    file.read(reinterpret_cast<char*>(&constantsSize), sizeof(constantsSize));

    // Read constants
    constants.resize(constantsSize);
    for (uint32_t i = 0; i < constantsSize; i++) {
        uint8_t type;
        file.read(reinterpret_cast<char*>(&type), sizeof(type));

        switch (type) {
            case 0: // Null
                constants[i] = Value(nullptr);
                break;
            case 1: // Boolean
                {
                    uint8_t value;
                    file.read(reinterpret_cast<char*>(&value), sizeof(value));
                    constants[i] = Value(value != 0);
                }
                break;
            case 2: // Integer
                {
                    int64_t value;
                    file.read(reinterpret_cast<char*>(&value), sizeof(value));
                    constants[i] = Value(value);
                }
                break;
            case 3: // Float
                {
                    double value;
                    file.read(reinterpret_cast<char*>(&value), sizeof(value));
                    constants[i] = Value(value);
                }
                break;
            case 4: // String
                {
                    uint32_t length;
                    file.read(reinterpret_cast<char*>(&length), sizeof(length));
                    std::string value(length, '\0');
                    file.read(&value[0], length);
                    constants[i] = Value(value);
                }
                break;
        }
    }

    // Read names size
    uint32_t namesSize;
    file.read(reinterpret_cast<char*>(&namesSize), sizeof(namesSize));

    // Read names
    names.resize(namesSize);
    for (uint32_t i = 0; i < namesSize; i++) {
        uint32_t length;
        file.read(reinterpret_cast<char*>(&length), sizeof(length));
        names[i].resize(length);
        file.read(&names[i][0], length);
    }
}

void VasukiVM::loadBytecodeFromMemory(const std::vector<uint8_t>& bytecodeData,
                                     const std::vector<Value>& constantsData,
                                     const std::vector<std::string>& namesData) {
    bytecode = bytecodeData;
    constants = constantsData;
    names = namesData;
    ip = 0;
}

Value VasukiVM::executeBuiltin(const std::string& name, const std::vector<Value>& args) {
    if (builtins.find(name) != builtins.end()) {
        return builtins[name](args);
    }
    throw std::runtime_error("Builtin function '" + name + "' not found");
}

void VasukiVM::setupBuiltins() {
    // print function
    builtins["print"] = [](const std::vector<Value>& args) {
        for (size_t i = 0; i < args.size(); i++) {
            if (i > 0) std::cout << " ";
            std::cout << args[i].toString();
        }
        std::cout << std::endl;
        return Value(nullptr);
    };

    // length function
    builtins["length"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("length() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (arg.isString()) {
            return Value(static_cast<int64_t>(arg.getString().length()));
        } else if (arg.isArray()) {
            return Value(static_cast<int64_t>(arg.getArray()->size()));
        } else if (arg.isDict()) {
            return Value(static_cast<int64_t>(arg.getDict()->size()));
        }

        throw std::runtime_error("length() requires a string, array, or dictionary");
    };

    // uppercase function
    builtins["uppercase"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("uppercase() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (!arg.isString()) {
            throw std::runtime_error("uppercase() requires a string argument");
        }

        std::string result = arg.getString();
        std::transform(result.begin(), result.end(), result.begin(), ::toupper);
        return Value(result);
    };

    // lowercase function
    builtins["lowercase"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("lowercase() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (!arg.isString()) {
            throw std::runtime_error("lowercase() requires a string argument");
        }

        std::string result = arg.getString();
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return Value(result);
    };

    // type function
    builtins["type"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("type() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (arg.isNull()) return Value("null");
        if (arg.isBool()) return Value("boolean");
        if (arg.isInt()) return Value("integer");
        if (arg.isFloat()) return Value("float");
        if (arg.isString()) return Value("string");
        if (arg.isArray()) return Value("array");
        if (arg.isDict()) return Value("dictionary");
        if (arg.isFunction()) return Value("function");

        return Value("unknown");
    };

    // to_string function
    builtins["to_string"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("to_string() requires exactly 1 argument");
        }

        return Value(args[0].toString());
    };

    // to_int function
    builtins["to_int"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("to_int() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (arg.isInt()) {
            return arg;
        } else if (arg.isFloat()) {
            return Value(static_cast<int64_t>(arg.getFloat()));
        } else if (arg.isString()) {
            try {
                return Value(static_cast<int64_t>(std::stoll(arg.getString())));
            } catch (const std::exception&) {
                throw std::runtime_error("Cannot convert string to integer");
            }
        } else if (arg.isBool()) {
            return Value(static_cast<int64_t>(arg.getBool() ? 1 : 0));
        }

        throw std::runtime_error("Cannot convert to integer");
    };

    // to_float function
    builtins["to_float"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("to_float() requires exactly 1 argument");
        }

        const Value& arg = args[0];
        if (arg.isFloat()) {
            return arg;
        } else if (arg.isInt()) {
            return Value(static_cast<double>(arg.getInt()));
        } else if (arg.isString()) {
            try {
                return Value(std::stod(arg.getString()));
            } catch (const std::exception&) {
                throw std::runtime_error("Cannot convert string to float");
            }
        } else if (arg.isBool()) {
            return Value(arg.getBool() ? 1.0 : 0.0);
        }

        throw std::runtime_error("Cannot convert to float");
    };

    // split function
    builtins["split"] = [](const std::vector<Value>& args) {
        if (args.size() < 1 || args.size() > 2) {
            throw std::runtime_error("split() requires 1 or 2 arguments");
        }

        const Value& str = args[0];
        if (!str.isString()) {
            throw std::runtime_error("split() requires a string as first argument");
        }

        std::string delimiter = " ";
        if (args.size() == 2) {
            const Value& delim = args[1];
            if (!delim.isString()) {
                throw std::runtime_error("split() requires a string as second argument");
            }
            delimiter = delim.getString();
        }

        std::string s = str.getString();
        std::vector<Value> result;

        // Add a dummy value at index 0 to make array 1-indexed
        result.push_back(Value(nullptr));

        size_t pos = 0;
        std::string token;
        while ((pos = s.find(delimiter)) != std::string::npos) {
            token = s.substr(0, pos);
            result.push_back(Value(token));
            s.erase(0, pos + delimiter.length());
        }
        result.push_back(Value(s));

        return Value(result);
    };

    // dict_keys function
    builtins["dict_keys"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("dict_keys() requires exactly 1 argument");
        }

        const Value& dict = args[0];
        if (!dict.isDict()) {
            throw std::runtime_error("dict_keys() requires a dictionary argument");
        }

        std::vector<Value> keys;
        // Add a dummy value at index 0 to make array 1-indexed
        keys.push_back(Value(nullptr));

        for (const auto& [key, _] : *dict.getDict()) {
            keys.push_back(Value(key));
        }

        return Value(keys);
    };

    // dict_values function
    builtins["dict_values"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("dict_values() requires exactly 1 argument");
        }

        const Value& dict = args[0];
        if (!dict.isDict()) {
            throw std::runtime_error("dict_values() requires a dictionary argument");
        }

        std::vector<Value> values;
        // Add a dummy value at index 0 to make array 1-indexed
        values.push_back(Value(nullptr));

        for (const auto& [_, val] : *dict.getDict()) {
            values.push_back(val);
        }

        return Value(values);
    };

    // dict_clear function
    builtins["dict_clear"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("dict_clear() requires exactly 1 argument");
        }

        const Value& dict = args[0];
        if (!dict.isDict()) {
            throw std::runtime_error("dict_clear() requires a dictionary argument");
        }

        dict.getDict()->clear();
        return Value(nullptr);
    };

    // dict_size function
    builtins["dict_size"] = [](const std::vector<Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("dict_size() requires exactly 1 argument");
        }

        const Value& dict = args[0];
        if (!dict.isDict()) {
            throw std::runtime_error("dict_size() requires a dictionary argument");
        }

        return Value(static_cast<int64_t>(dict.getDict()->size()));
    };
}

Value VasukiVM::execute() {
    // Reset instruction pointer
    ip = 0;

    // Pre-allocate stack space for better performance
    stack.reserve(1024);

    // Use direct access to bytecode for better performance
    const uint8_t* code = bytecode.data();
    const size_t code_size = bytecode.size();

    // Main execution loop
    while (static_cast<size_t>(ip) < code_size) {
        // Read the opcode
        OpCode opcode = static_cast<OpCode>(readByte());

        // Execute the instruction
        switch (opcode) {
            case OpCode::HALT:
                // Return the top value on the stack or null if stack is empty
                if (stack.empty()) {
                    // Suppress output
                    return Value(nullptr);
                } else {
                    // Suppress output
                    return stack.back();
                }

            case OpCode::NOP:
                // No operation
                break;

            case OpCode::PUSH_INT: {
                int64_t value = readInt();
                push(Value(value));
                break;
            }

            case OpCode::PUSH_FLOAT: {
                // Read a float constant
                Value constant = readConstant();
                if (!constant.isFloat()) {
                    throw std::runtime_error("Expected float constant");
                }
                push(constant);
                break;
            }

            case OpCode::PUSH_STRING: {
                // Read a string constant
                std::string str = readString();
                push(Value(str));
                break;
            }

            case OpCode::PUSH_BOOL: {
                bool value = readByte() != 0;
                push(Value(value));
                break;
            }

            case OpCode::PUSH_NULL:
                push(Value(nullptr));
                break;

            case OpCode::PUSH_CONSTANT: {
                Value constant = readConstant();
                push(constant);
                break;
            }

            case OpCode::PUSH_TRUE:
                push(Value(true));
                break;

            case OpCode::PUSH_FALSE:
                push(Value(false));
                break;

            case OpCode::POP:
                pop();
                break;

            case OpCode::POP_N: {
                uint8_t count = readByte();
                for (uint8_t i = 0; i < count; i++) {
                    pop();
                }
                break;
            }

            case OpCode::DUP: {
                if (stack.empty()) {
                    throw std::runtime_error("Cannot duplicate empty stack");
                }
                push(stack.back());
                break;
            }

            case OpCode::ADD: {
                Value b = pop();
                Value a = pop();
                push(a + b);
                break;
            }

            case OpCode::SUB: {
                Value b = pop();
                Value a = pop();
                push(a - b);
                break;
            }

            case OpCode::MUL: {
                Value b = pop();
                Value a = pop();
                push(a * b);
                break;
            }

            case OpCode::DIV: {
                Value b = pop();
                Value a = pop();
                push(a / b);
                break;
            }

            case OpCode::MOD: {
                Value b = pop();
                Value a = pop();
                push(a % b);
                break;
            }

            case OpCode::NEG: {
                Value a = pop();
                if (a.isInt()) {
                    push(Value(-a.getInt()));
                } else if (a.isFloat()) {
                    push(Value(-a.getFloat()));
                } else {
                    throw std::runtime_error("Cannot negate non-numeric value");
                }
                break;
            }

            case OpCode::POW: {
                Value b = pop();
                Value a = pop();

                if (a.isInt() && b.isInt()) {
                    push(Value(static_cast<int64_t>(std::pow(a.getInt(), b.getInt()))));
                } else {
                    double base = a.isInt() ? a.getInt() : a.getFloat();
                    double exponent = b.isInt() ? b.getInt() : b.getFloat();
                    push(Value(std::pow(base, exponent)));
                }
                break;
            }

            case OpCode::EQ: {
                Value b = pop();
                Value a = pop();
                push(Value(a == b));
                break;
            }

            case OpCode::NEQ: {
                Value b = pop();
                Value a = pop();
                push(Value(a != b));
                break;
            }

            case OpCode::LT: {
                Value b = pop();
                Value a = pop();
                push(Value(a < b));
                break;
            }

            case OpCode::LTE: {
                Value b = pop();
                Value a = pop();
                push(Value(a <= b));
                break;
            }

            case OpCode::GT: {
                Value b = pop();
                Value a = pop();
                push(Value(a > b));
                break;
            }

            case OpCode::GTE: {
                Value b = pop();
                Value a = pop();
                push(Value(a >= b));
                break;
            }

            case OpCode::AND: {
                Value b = pop();
                Value a = pop();

                if (!a.isBool() || !b.isBool()) {
                    throw std::runtime_error("AND requires boolean operands");
                }

                push(Value(a.getBool() && b.getBool()));
                break;
            }

            case OpCode::OR: {
                Value b = pop();
                Value a = pop();

                if (!a.isBool() || !b.isBool()) {
                    throw std::runtime_error("OR requires boolean operands");
                }

                push(Value(a.getBool() || b.getBool()));
                break;
            }

            case OpCode::NOT: {
                Value a = pop();

                if (!a.isBool()) {
                    throw std::runtime_error("NOT requires a boolean operand");
                }

                push(Value(!a.getBool()));
                break;
            }

            case OpCode::GET_GLOBAL: {
                std::string name = readString();
                try {
                    push(globalEnv->lookup(name));
                } catch (const std::runtime_error& e) {
                    std::cerr << "Warning: " << e.what() << ", returning null" << std::endl;
                    push(Value(nullptr));
                }
                break;
            }

            case OpCode::SET_GLOBAL: {
                std::string name = readString();
                Value value = pop();
                globalEnv->assign(name, value);
                push(value);  // Push the value back for assignment expressions
                break;
            }

            case OpCode::DEFINE_GLOBAL: {
                std::string name = readString();
                Value value = pop();
                globalEnv->declare(name, value);
                break;
            }

            case OpCode::GET_LOCAL: {
                if (callStack.empty()) {
                    std::cerr << "Warning: Cannot access local variable outside of function, returning null" << std::endl;
                    push(Value(nullptr));
                    break;
                }

                std::string name = readString();
                try {
                    push(callStack.back().environment->lookup(name));
                } catch (const std::runtime_error& e) {
                    std::cerr << "Warning: " << e.what() << ", returning null" << std::endl;
                    push(Value(nullptr));
                }
                break;
            }

            case OpCode::SET_LOCAL: {
                if (callStack.empty()) {
                    throw std::runtime_error("Cannot set local variable outside of function");
                }

                std::string name = readString();
                Value value = pop();
                callStack.back().environment->assign(name, value);
                push(value);  // Push the value back for assignment expressions
                break;
            }

            case OpCode::DEFINE_LOCAL: {
                if (callStack.empty()) {
                    throw std::runtime_error("Cannot define local variable outside of function");
                }

                std::string name = readString();
                Value value = pop();
                callStack.back().environment->declare(name, value);
                break;
            }

            case OpCode::JUMP: {
                int32_t offset = readInt();
                std::cout << "JUMP: Jumping from " << ip << " by offset " << offset << " to " << (ip + offset) << std::endl;
                ip += offset;
                break;
            }

            case OpCode::JUMP_IF_FALSE: {
                int32_t offset = readInt();
                Value condition = pop();

                if (!condition.isBool()) {
                    throw std::runtime_error("Condition must be a boolean");
                }

                if (!condition.getBool()) {
                    ip += offset;
                }
                break;
            }

            case OpCode::JUMP_IF_TRUE: {
                int32_t offset = readInt();
                Value condition = pop();

                if (!condition.isBool()) {
                    throw std::runtime_error("Condition must be a boolean");
                }

                if (condition.getBool()) {
                    ip += offset;
                }
                break;
            }

            case OpCode::CALL:
            case OpCode::TAIL_CALL: {
                // Check if this is a tail call
                bool isTail = (opcode == OpCode::TAIL_CALL) || isTailCall(ip - 1);
                uint8_t argCount = readByte();

                // Pop arguments from the stack in reverse order
                std::vector<Value> args(argCount);
                for (int i = argCount - 1; i >= 0; i--) {
                    args[i] = pop();
                }

                // Pop the function value
                Value functionValue = pop();

                // Debug output
                std::cout << (isTail ? "Tail calling" : "Calling") << " function with "
                          << static_cast<int>(argCount) << " arguments" << std::endl;

                if (functionValue.isFunction()) {
                    // User-defined function
                    auto function = functionValue.getFunction();

                    // Debug output
                    std::cout << "  User-defined function with " << function->params.size() << " parameters" << std::endl;

                    // Check argument count
                    if (args.size() != function->params.size()) {
                        throw std::runtime_error("Function called with wrong number of arguments");
                    }

                    if (isTail && !callStack.empty()) {
                        // Perform tail call optimization
                        optimizeTailCall(function, args);
                    } else {
                        // Create a new environment for the function call
                        auto env = std::make_shared<Environment>(function->closure);

                        // Bind arguments to parameters
                        for (size_t i = 0; i < args.size(); i++) {
                            env->declare(function->params[i], args[i]);
                            std::cout << "  Parameter '" << function->params[i] << "' = " << args[i].toString() << std::endl;
                        }

                        // Save the current instruction pointer
                        int returnAddress = ip;

                        // Jump to the function body
                        ip = function->startPos;

                        // Debug output
                        std::cout << "  Jumping to position " << ip << std::endl;

                        // Push a new call frame
                        callStack.push_back(CallFrame(returnAddress, env, function));
                    }
                } else if (functionValue.isString()) {
                    // Builtin function
                    std::string name = functionValue.getString();
                    std::cout << "  Builtin function '" << name << "'" << std::endl;
                    Value result = executeBuiltin(name, args);
                    push(result);
                } else {
                    std::cerr << "Warning: Cannot call non-function value, returning null" << std::endl;
                    push(Value(nullptr));
                }
                break;
            }

            case OpCode::RETURN: {
                // Get the return value
                Value returnValue = pop();

                // Suppress debug output
                if (callStack.empty()) {
                    // Return from the top level
                    return returnValue;
                }

                // Pop the call frame
                CallFrame frame = callStack.back();
                callStack.pop_back();

                // Restore the instruction pointer
                ip = frame.returnAddress;

                // Push the return value onto the stack
                push(returnValue);
                break;
            }

            case OpCode::FUNCTION: {
                std::string name = readString();
                int startPos = readInt();
                uint8_t paramCount = readByte();

                // Read parameter names
                std::vector<std::string> params(paramCount);
                for (uint8_t i = 0; i < paramCount; i++) {
                    params[i] = readString();
                }

                // Create the function object
                auto env = callStack.empty() ? globalEnv : callStack.back().environment;
                auto function = std::make_shared<Function>(startPos, params, env);

                // Store the function in the current environment
                if (callStack.empty()) {
                    globalEnv->declare(name, Value(function));
                } else {
                    callStack.back().environment->declare(name, Value(function));
                }

                // Debug output
                std::cout << "Defined function '" << name << "' with " << static_cast<int>(paramCount) << " parameters" << std::endl;

                break;
            }

            case OpCode::LIST: {
                uint16_t count = readShort();

                // Pop elements from the stack in reverse order
                std::vector<Value> elements(count);
                for (int i = count - 1; i >= 0; i--) {
                    elements[i] = pop();
                }

                // Create the list
                push(Value(elements));
                break;
            }

            case OpCode::DICT: {
                uint16_t count = readShort();

                // Pop key-value pairs from the stack
                std::unordered_map<std::string, Value> dict;
                for (uint16_t i = 0; i < count; i++) {
                    Value value = pop();
                    Value key = pop();

                    if (!key.isString()) {
                        throw std::runtime_error("Dictionary keys must be strings");
                    }

                    dict[key.getString()] = value;
                }

                // Create the dictionary
                push(Value(dict));
                break;
            }

            case OpCode::GET_PROPERTY: {
                Value index = pop();
                Value object = pop();

                if (object.isArray()) {
                    if (!index.isInt()) {
                        throw std::runtime_error("Array index must be an integer");
                    }

                    auto array = object.getArray();
                    int64_t i = index.getInt();

                    if (i < 0 || i >= static_cast<int64_t>(array->size())) {
                        throw std::runtime_error("Array index out of bounds");
                    }

                    push((*array)[i]);
                } else if (object.isDict()) {
                    if (!index.isString()) {
                        throw std::runtime_error("Dictionary key must be a string");
                    }

                    auto dict = object.getDict();
                    std::string key = index.getString();

                    if (dict->find(key) == dict->end()) {
                        throw std::runtime_error("Dictionary key not found: " + key);
                    }

                    push((*dict)[key]);
                } else if (object.isString()) {
                    if (!index.isInt()) {
                        throw std::runtime_error("String index must be an integer");
                    }

                    std::string str = object.getString();
                    int64_t i = index.getInt();

                    if (i < 0 || i >= static_cast<int64_t>(str.length())) {
                        throw std::runtime_error("String index out of bounds");
                    }

                    push(Value(std::string(1, str[i])));
                } else {
                    throw std::runtime_error("Cannot get property of non-indexable value");
                }
                break;
            }

            case OpCode::SET_PROPERTY: {
                Value value = pop();
                Value index = pop();
                Value object = pop();

                if (object.isArray()) {
                    if (!index.isInt()) {
                        throw std::runtime_error("Array index must be an integer");
                    }

                    auto array = object.getArray();
                    int64_t i = index.getInt();

                    if (i < 0 || i >= static_cast<int64_t>(array->size())) {
                        throw std::runtime_error("Array index out of bounds");
                    }

                    (*array)[i] = value;
                    push(value);
                } else if (object.isDict()) {
                    if (!index.isString()) {
                        throw std::runtime_error("Dictionary key must be a string");
                    }

                    auto dict = object.getDict();
                    std::string key = index.getString();

                    (*dict)[key] = value;
                    push(value);
                } else {
                    throw std::runtime_error("Cannot set property of non-indexable value");
                }
                break;
            }

            case OpCode::PRINT: {
                Value value = pop();
                std::cout << value.toString();
                // Only add a newline if the string doesn't end with one
                if (value.isString()) {
                    std::string str = value.getString();
                    if (str.empty() || str.back() != '\n') {
                        std::cout << std::endl;
                    }
                } else {
                    std::cout << std::endl;
                }
                break;
            }

            default:
                throw std::runtime_error("Unknown opcode: " + std::to_string(static_cast<int>(opcode)));
        }
    }

    // If we reach here, we've run out of bytecode without a HALT instruction
    return stack.empty() ? Value(nullptr) : stack.back();
}

void VasukiVM::dumpStack() const {
    std::cout << "Stack (" << stack.size() << " items):" << std::endl;
    for (size_t i = 0; i < stack.size(); i++) {
        std::cout << "  " << i << ": " << stack[i].toString() << std::endl;
    }
}

bool VasukiVM::isTailCall(size_t currentPos) {
    // Check if the current position is followed by a RETURN instruction
    if (currentPos + 1 < bytecode.size() &&
        static_cast<OpCode>(bytecode[currentPos + 1]) == OpCode::RETURN) {
        std::cout << "Detected tail call at position " << currentPos << std::endl;
        return true;
    }
    return false;
}

void VasukiVM::optimizeTailCall(std::shared_ptr<Function> function, const std::vector<Value>& args) {
    // Debug output
    std::cout << "  Performing tail call optimization" << std::endl;

    if (callStack.empty()) {
        std::cerr << "Warning: Cannot perform tail call optimization without a call frame" << std::endl;

        // Create a new environment for the function call
        auto env = std::make_shared<Environment>(function->closure);

        // Bind arguments to parameters
        for (size_t i = 0; i < args.size(); i++) {
            env->declare(function->params[i], args[i]);
            std::cout << "  Parameter '" << function->params[i] << "' = " << args[i].toString() << std::endl;
        }

        // Save the current instruction pointer
        int returnAddress = ip;

        // Jump to the function body
        ip = function->startPos;

        // Debug output
        std::cout << "  Jumping to position " << ip << std::endl;

        // Push a new call frame
        callStack.push_back(CallFrame(returnAddress, env, function));
        return;
    }

    // Get the current call frame
    CallFrame& frame = callStack.back();

    // Create a new environment for the function call
    auto env = std::make_shared<Environment>(function->closure);

    // Bind arguments to parameters
    for (size_t i = 0; i < args.size(); i++) {
        env->declare(function->params[i], args[i]);
        std::cout << "  Parameter '" << function->params[i] << "' = " << args[i].toString() << std::endl;
    }

    // Replace the current environment with the new one
    frame.environment = env;

    // Replace the current function with the new one
    frame.function = function;

    // Jump to the function body
    ip = function->startPos;

    // Debug output
    std::cout << "  Jumping to position " << ip << " (tail call)" << std::endl;
}

void VasukiVM::dumpBytecode() const {
    std::cout << "Bytecode (" << bytecode.size() << " bytes):" << std::endl;

    for (size_t i = 0; i < bytecode.size();) {
        std::cout << std::setw(4) << i << ": ";

        // Print the opcode
        OpCode opcode = static_cast<OpCode>(bytecode[i++]);
        std::cout << std::setw(15) << std::left;

        switch (opcode) {
            case OpCode::HALT:
                std::cout << "HALT";
                break;

            case OpCode::NOP:
                std::cout << "NOP";
                break;

            case OpCode::PUSH_INT:
                if (i + 3 < bytecode.size()) {
                    int32_t value = bytecode[i] | (bytecode[i+1] << 8) | (bytecode[i+2] << 16) | (bytecode[i+3] << 24);
                    std::cout << "PUSH_INT " << value;
                    i += 4;
                } else {
                    std::cout << "PUSH_INT <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::PUSH_FLOAT:
                if (i < bytecode.size()) {
                    uint8_t index = bytecode[i++];
                    if (index < constants.size() && constants[index].isFloat()) {
                        std::cout << "PUSH_FLOAT " << constants[index].getFloat();
                    } else {
                        std::cout << "PUSH_FLOAT <invalid constant>";
                    }
                } else {
                    std::cout << "PUSH_FLOAT <incomplete>";
                }
                break;

            case OpCode::PUSH_STRING:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "PUSH_STRING \"" << names[index] << "\"";
                    } else {
                        std::cout << "PUSH_STRING <invalid index>";
                    }
                } else {
                    std::cout << "PUSH_STRING <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::PUSH_BOOL:
                if (i < bytecode.size()) {
                    bool value = bytecode[i++] != 0;
                    std::cout << "PUSH_BOOL " << (value ? "true" : "false");
                } else {
                    std::cout << "PUSH_BOOL <incomplete>";
                }
                break;

            case OpCode::PUSH_NULL:
                std::cout << "PUSH_NULL";
                break;

            case OpCode::PUSH_CONSTANT:
                if (i < bytecode.size()) {
                    uint8_t index = bytecode[i++];
                    if (index < constants.size()) {
                        std::cout << "PUSH_CONSTANT " << constants[index].toString();
                    } else {
                        std::cout << "PUSH_CONSTANT <invalid index>";
                    }
                } else {
                    std::cout << "PUSH_CONSTANT <incomplete>";
                }
                break;

            case OpCode::PUSH_TRUE:
                std::cout << "PUSH_TRUE";
                break;

            case OpCode::PUSH_FALSE:
                std::cout << "PUSH_FALSE";
                break;

            case OpCode::POP:
                std::cout << "POP";
                break;

            case OpCode::POP_N:
                if (i < bytecode.size()) {
                    uint8_t count = bytecode[i++];
                    std::cout << "POP_N " << static_cast<int>(count);
                } else {
                    std::cout << "POP_N <incomplete>";
                }
                break;

            case OpCode::DUP:
                std::cout << "DUP";
                break;

            case OpCode::ADD:
                std::cout << "ADD";
                break;

            case OpCode::SUB:
                std::cout << "SUB";
                break;

            case OpCode::MUL:
                std::cout << "MUL";
                break;

            case OpCode::DIV:
                std::cout << "DIV";
                break;

            case OpCode::MOD:
                std::cout << "MOD";
                break;

            case OpCode::NEG:
                std::cout << "NEG";
                break;

            case OpCode::POW:
                std::cout << "POW";
                break;

            case OpCode::EQ:
                std::cout << "EQ";
                break;

            case OpCode::NEQ:
                std::cout << "NEQ";
                break;

            case OpCode::LT:
                std::cout << "LT";
                break;

            case OpCode::LTE:
                std::cout << "LTE";
                break;

            case OpCode::GT:
                std::cout << "GT";
                break;

            case OpCode::GTE:
                std::cout << "GTE";
                break;

            case OpCode::AND:
                std::cout << "AND";
                break;

            case OpCode::OR:
                std::cout << "OR";
                break;

            case OpCode::NOT:
                std::cout << "NOT";
                break;

            case OpCode::GET_GLOBAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "GET_GLOBAL " << names[index];
                    } else {
                        std::cout << "GET_GLOBAL <invalid index>";
                    }
                } else {
                    std::cout << "GET_GLOBAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::SET_GLOBAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "SET_GLOBAL " << names[index];
                    } else {
                        std::cout << "SET_GLOBAL <invalid index>";
                    }
                } else {
                    std::cout << "SET_GLOBAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::DEFINE_GLOBAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "DEFINE_GLOBAL " << names[index];
                    } else {
                        std::cout << "DEFINE_GLOBAL <invalid index>";
                    }
                } else {
                    std::cout << "DEFINE_GLOBAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::GET_LOCAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "GET_LOCAL " << names[index];
                    } else {
                        std::cout << "GET_LOCAL <invalid index>";
                    }
                } else {
                    std::cout << "GET_LOCAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::SET_LOCAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "SET_LOCAL " << names[index];
                    } else {
                        std::cout << "SET_LOCAL <invalid index>";
                    }
                } else {
                    std::cout << "SET_LOCAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::DEFINE_LOCAL:
                if (i + 1 < bytecode.size()) {
                    uint16_t index = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    if (index < names.size()) {
                        std::cout << "DEFINE_LOCAL " << names[index];
                    } else {
                        std::cout << "DEFINE_LOCAL <invalid index>";
                    }
                } else {
                    std::cout << "DEFINE_LOCAL <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::JUMP:
                if (i + 3 < bytecode.size()) {
                    int32_t offset = bytecode[i] | (bytecode[i+1] << 8) | (bytecode[i+2] << 16) | (bytecode[i+3] << 24);
                    std::cout << "JUMP " << offset;
                    i += 4;
                } else {
                    std::cout << "JUMP <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::JUMP_IF_FALSE:
                if (i + 3 < bytecode.size()) {
                    int32_t offset = bytecode[i] | (bytecode[i+1] << 8) | (bytecode[i+2] << 16) | (bytecode[i+3] << 24);
                    std::cout << "JUMP_IF_FALSE " << offset;
                    i += 4;
                } else {
                    std::cout << "JUMP_IF_FALSE <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::JUMP_IF_TRUE:
                if (i + 3 < bytecode.size()) {
                    int32_t offset = bytecode[i] | (bytecode[i+1] << 8) | (bytecode[i+2] << 16) | (bytecode[i+3] << 24);
                    std::cout << "JUMP_IF_TRUE " << offset;
                    i += 4;
                } else {
                    std::cout << "JUMP_IF_TRUE <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::CALL:
                if (i < bytecode.size()) {
                    uint8_t argCount = bytecode[i++];
                    std::cout << "CALL " << static_cast<int>(argCount);
                } else {
                    std::cout << "CALL <incomplete>";
                }
                break;

            case OpCode::TAIL_CALL:
                if (i < bytecode.size()) {
                    uint8_t argCount = bytecode[i++];
                    std::cout << "TAIL_CALL " << static_cast<int>(argCount);
                } else {
                    std::cout << "TAIL_CALL <incomplete>";
                }
                break;

            case OpCode::RETURN:
                std::cout << "RETURN";
                break;

            case OpCode::FUNCTION:
                if (i + 1 < bytecode.size()) {
                    uint16_t nameIndex = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;

                    if (i + 3 < bytecode.size()) {
                        int32_t startPos = bytecode[i] | (bytecode[i+1] << 8) | (bytecode[i+2] << 16) | (bytecode[i+3] << 24);
                        i += 4;

                        if (i < bytecode.size()) {
                            uint8_t paramCount = bytecode[i++];

                            if (nameIndex < names.size()) {
                                std::cout << "FUNCTION " << names[nameIndex] << " " << startPos << " " << static_cast<int>(paramCount) << " params";

                                // Skip parameter names
                                i += paramCount * 2;
                            } else {
                                std::cout << "FUNCTION <invalid name index>";
                            }
                        } else {
                            std::cout << "FUNCTION <incomplete>";
                        }
                    } else {
                        std::cout << "FUNCTION <incomplete>";
                        i = bytecode.size();
                    }
                } else {
                    std::cout << "FUNCTION <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::LIST:
                if (i + 1 < bytecode.size()) {
                    uint16_t count = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    std::cout << "LIST " << count;
                } else {
                    std::cout << "LIST <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::DICT:
                if (i + 1 < bytecode.size()) {
                    uint16_t count = bytecode[i] | (bytecode[i+1] << 8);
                    i += 2;
                    std::cout << "DICT " << count;
                } else {
                    std::cout << "DICT <incomplete>";
                    i = bytecode.size();
                }
                break;

            case OpCode::GET_PROPERTY:
                std::cout << "GET_PROPERTY";
                break;

            case OpCode::SET_PROPERTY:
                std::cout << "SET_PROPERTY";
                break;

            case OpCode::PRINT:
                std::cout << "PRINT";
                break;

            default:
                std::cout << "UNKNOWN " << static_cast<int>(opcode);
                break;
        }

        std::cout << std::endl;
    }
}

} // namespace vasuki
