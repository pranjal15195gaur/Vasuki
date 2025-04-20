// vasuki_vm.h
#ifndef VASUKI_VM_H
#define VASUKI_VM_H

#include <vector>
#include <string>
#include <unordered_map>
#include <variant>
#include <memory>
#include <functional>
#include <iostream>
#include <stack>
#include <fstream>

namespace vasuki {

// OpCode enum for bytecode instructions
enum class OpCode : uint8_t {
    HALT = 0,
    NOP = 1,
    PUSH_INT = 2,
    PUSH_FLOAT = 3,
    PUSH_STRING = 4,
    PUSH_BOOL = 5,
    PUSH_NULL = 6,
    POP = 7,
    POP_N = 8,
    DUP = 9,
    ADD = 10,
    SUB = 11,
    MUL = 12,
    DIV = 13,
    MOD = 14,
    NEG = 15,
    POW = 16,
    EQ = 17,
    NEQ = 18,
    LT = 19,
    LTE = 20,
    GT = 21,
    GTE = 22,
    AND = 23,
    OR = 24,
    NOT = 25,
    GET_GLOBAL = 26,
    SET_GLOBAL = 27,
    DEFINE_GLOBAL = 28,
    GET_LOCAL = 29,
    SET_LOCAL = 30,
    DEFINE_LOCAL = 31,
    JUMP = 32,
    JUMP_IF_FALSE = 33,
    JUMP_IF_TRUE = 34,
    CALL = 35,
    RETURN = 36,
    FUNCTION = 37,
    LIST = 38,
    DICT = 39,
    GET_PROPERTY = 40,
    SET_PROPERTY = 41,
    PRINT = 42,
    PUSH_CONSTANT = 43,
    PUSH_TRUE = 44,
    PUSH_FALSE = 45,
    TAIL_CALL = 46  // New opcode for tail call optimization
};

// Forward declarations
class Value;
class Function;
class Environment;

// Value types that can be stored in the VM
using ValueVariant = std::variant<
    std::nullptr_t,
    bool,
    int64_t,
    double,
    std::string,
    std::shared_ptr<std::vector<Value>>,  // Array
    std::shared_ptr<std::unordered_map<std::string, Value>>,  // Dictionary
    std::shared_ptr<Function>  // Function
>;

// Represents a value in the VM
class Value {
public:
    ValueVariant value;

    Value() : value(nullptr) {}
    Value(std::nullptr_t) : value(nullptr) {}
    Value(bool b) : value(b) {}
    Value(int i) : value(static_cast<int64_t>(i)) {}
    Value(int64_t i) : value(i) {}
    Value(double d) : value(d) {}
    Value(const std::string& s) : value(s) {}
    Value(const char* s) : value(std::string(s)) {}

    // Array constructor
    Value(const std::vector<Value>& arr) :
        value(std::make_shared<std::vector<Value>>(arr)) {}

    // Dictionary constructor
    Value(const std::unordered_map<std::string, Value>& dict) :
        value(std::make_shared<std::unordered_map<std::string, Value>>(dict)) {}

    // Function constructor
    Value(std::shared_ptr<Function> func) : value(func) {}

    // Type checking
    bool isNull() const { return std::holds_alternative<std::nullptr_t>(value); }
    bool isBool() const { return std::holds_alternative<bool>(value); }
    bool isInt() const { return std::holds_alternative<int64_t>(value); }
    bool isFloat() const { return std::holds_alternative<double>(value); }
    bool isString() const { return std::holds_alternative<std::string>(value); }
    bool isArray() const { return std::holds_alternative<std::shared_ptr<std::vector<Value>>>(value); }
    bool isDict() const { return std::holds_alternative<std::shared_ptr<std::unordered_map<std::string, Value>>>(value); }
    bool isFunction() const { return std::holds_alternative<std::shared_ptr<Function>>(value); }
    bool isNumber() const { return isInt() || isFloat(); }

    // Value getters
    bool getBool() const { return std::get<bool>(value); }
    int64_t getInt() const { return std::get<int64_t>(value); }
    double getFloat() const { return std::get<double>(value); }
    std::string getString() const { return std::get<std::string>(value); }
    std::shared_ptr<std::vector<Value>> getArray() const {
        return std::get<std::shared_ptr<std::vector<Value>>>(value);
    }
    std::shared_ptr<std::unordered_map<std::string, Value>> getDict() const {
        return std::get<std::shared_ptr<std::unordered_map<std::string, Value>>>(value);
    }
    std::shared_ptr<Function> getFunction() const {
        return std::get<std::shared_ptr<Function>>(value);
    }

    // Conversion to string for printing
    std::string toString() const;

    // Operators
    Value operator+(const Value& other) const;
    Value operator-(const Value& other) const;
    Value operator*(const Value& other) const;
    Value operator/(const Value& other) const;
    Value operator%(const Value& other) const;
    bool operator==(const Value& other) const;
    bool operator!=(const Value& other) const;
    bool operator<(const Value& other) const;
    bool operator<=(const Value& other) const;
    bool operator>(const Value& other) const;
    bool operator>=(const Value& other) const;
};

// Represents a function in the VM
class Function {
public:
    int startPos;
    std::vector<std::string> params;
    std::shared_ptr<Environment> closure;

    Function(int startPos, const std::vector<std::string>& params,
             std::shared_ptr<Environment> closure)
        : startPos(startPos), params(params), closure(closure) {}
};

// Environment for variable storage with parent scoping
class Environment {
private:
    std::unordered_map<std::string, Value> variables;
    std::shared_ptr<Environment> parent;

public:
    Environment() : parent(nullptr) {}
    Environment(std::shared_ptr<Environment> parent) : parent(parent) {}

    void declare(const std::string& name, const Value& value);
    void assign(const std::string& name, const Value& value);
    Value lookup(const std::string& name);
    bool contains(const std::string& name) const;
};

// Call frame for function calls
struct CallFrame {
    int returnAddress;
    std::shared_ptr<Environment> environment;
    std::shared_ptr<Function> function;

    CallFrame(int returnAddress, std::shared_ptr<Environment> env, std::shared_ptr<Function> func)
        : returnAddress(returnAddress), environment(env), function(func) {}
};

// The Virtual Machine
class VasukiVM {
private:
    std::vector<uint8_t> bytecode;
    std::vector<Value> constants;
    std::vector<std::string> names;

    std::vector<Value> stack;
    std::vector<CallFrame> callStack;
    std::shared_ptr<Environment> globalEnv;

    int ip;  // Instruction pointer

    // Built-in functions
    std::unordered_map<std::string, std::function<Value(const std::vector<Value>&)>> builtins;

    // Helper methods
    Value pop();
    void push(const Value& value);
    void setupBuiltins();
    Value executeBuiltin(const std::string& name, const std::vector<Value>& args);
    uint8_t readByte();
    uint16_t readShort();
    int32_t readInt();
    Value readConstant();
    std::string readString();
    bool isTailCall(size_t currentPos);
    void optimizeTailCall(std::shared_ptr<Function> function, const std::vector<Value>& args);

public:
    VasukiVM();

    void loadBytecode(const std::string& filename);
    void loadBytecodeFromMemory(const std::vector<uint8_t>& bytecode,
                               const std::vector<Value>& constants,
                               const std::vector<std::string>& names);

    Value execute();
    void dumpStack() const;
    void dumpBytecode() const;
};

} // namespace vasuki

#endif // VASUKI_VM_H