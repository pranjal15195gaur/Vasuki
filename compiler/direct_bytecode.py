#!/usr/bin/env python3
"""
Direct Bytecode Generator for Vasuki

This module generates bytecode directly from the AST without running the Python interpreter.
"""

import sys
import os
import struct
from compiler.parser import parse
from compiler.top import Environment

# OpCodes for the Vasuki VM (must match the C++ VM)
class OpCode:
    HALT = 0
    NOP = 1
    PUSH_INT = 2
    PUSH_FLOAT = 3
    PUSH_STRING = 4
    PUSH_BOOL = 5
    PUSH_NULL = 6
    POP = 7
    POP_N = 8
    DUP = 9
    ADD = 10
    SUB = 11
    MUL = 12
    DIV = 13
    MOD = 14
    NEG = 15
    POW = 16
    EQ = 17
    NEQ = 18
    LT = 19
    LTE = 20
    GT = 21
    GTE = 22
    AND = 23
    OR = 24
    NOT = 25
    GET_GLOBAL = 26
    SET_GLOBAL = 27
    DEFINE_GLOBAL = 28
    GET_LOCAL = 29
    SET_LOCAL = 30
    DEFINE_LOCAL = 31
    JUMP = 32
    JUMP_IF_FALSE = 33
    JUMP_IF_TRUE = 34
    CALL = 35
    RETURN = 36
    FUNCTION = 37
    LIST = 38
    DICT = 39
    GET_PROPERTY = 40
    SET_PROPERTY = 41
    PRINT = 42
    PUSH_CONSTANT = 43
    PUSH_TRUE = 44
    PUSH_FALSE = 45

class BytecodeGenerator:
    """
    Generates bytecode directly from the AST.
    """
    def __init__(self):
        self.bytecode = []
        self.constants = []
        self.names = []
        self.string_pool = {}  # Map of strings to their indices
        self.current_scope = []  # Stack of scopes for variable lookup
        self.loops = []  # Stack of loop information for break/continue
        self.functions = {}  # Map of function names to their bytecode offsets
        
    def add_string(self, string):
        """Add a string to the string pool and return its index."""
        if string in self.string_pool:
            return self.string_pool[string]
        
        index = len(self.names)
        self.names.append(string)
        self.string_pool[string] = index
        return index
    
    def emit(self, opcode, *args):
        """Emit an opcode and its arguments to the bytecode."""
        self.bytecode.append(opcode)
        for arg in args:
            if isinstance(arg, int):
                # For integers, we need to emit 4 bytes (little-endian)
                self.bytecode.append(arg & 0xFF)
                self.bytecode.append((arg >> 8) & 0xFF)
                self.bytecode.append((arg >> 16) & 0xFF)
                self.bytecode.append((arg >> 24) & 0xFF)
            else:
                self.bytecode.append(arg)
    
    def emit_print(self):
        """Emit a print instruction."""
        self.emit(OpCode.PRINT)
    
    def emit_push_string(self, string):
        """Emit a push string instruction."""
        index = self.add_string(string)
        self.emit(OpCode.PUSH_STRING, index & 0xFF, (index >> 8) & 0xFF)
    
    def emit_push_int(self, value):
        """Emit a push int instruction."""
        self.emit(OpCode.PUSH_INT, value & 0xFF, (value >> 8) & 0xFF, 
                 (value >> 16) & 0xFF, (value >> 24) & 0xFF)
    
    def emit_push_float(self, value):
        """Emit a push float instruction."""
        # Convert float to bytes and extract the bytes
        bytes_val = struct.pack('<d', value)
        for b in bytes_val:
            self.bytecode.append(b)
    
    def emit_push_bool(self, value):
        """Emit a push bool instruction."""
        if value:
            self.emit(OpCode.PUSH_TRUE)
        else:
            self.emit(OpCode.PUSH_FALSE)
    
    def emit_push_null(self):
        """Emit a push null instruction."""
        self.emit(OpCode.PUSH_NULL)
    
    def emit_binary_op(self, op):
        """Emit a binary operation instruction."""
        if op == '+':
            self.emit(OpCode.ADD)
        elif op == '-':
            self.emit(OpCode.SUB)
        elif op == '*':
            self.emit(OpCode.MUL)
        elif op == '/':
            self.emit(OpCode.DIV)
        elif op == '%':
            self.emit(OpCode.MOD)
        elif op == '**':
            self.emit(OpCode.POW)
        elif op == '==':
            self.emit(OpCode.EQ)
        elif op == '!=':
            self.emit(OpCode.NEQ)
        elif op == '<':
            self.emit(OpCode.LT)
        elif op == '<=':
            self.emit(OpCode.LTE)
        elif op == '>':
            self.emit(OpCode.GT)
        elif op == '>=':
            self.emit(OpCode.GTE)
        elif op == 'and':
            self.emit(OpCode.AND)
        elif op == 'or':
            self.emit(OpCode.OR)
    
    def emit_unary_op(self, op):
        """Emit a unary operation instruction."""
        if op == '-':
            self.emit(OpCode.NEG)
        elif op == 'not':
            self.emit(OpCode.NOT)
    
    def generate_bytecode(self, ast):
        """Generate bytecode for an AST."""
        self._generate_node(ast)
        self.emit(OpCode.HALT)
        return self.bytecode, self.constants, self.names
    
    def _generate_node(self, node):
        """Generate bytecode for a node in the AST."""
        node_type = node['type']
        
        if node_type == 'program':
            for statement in node['body']:
                self._generate_node(statement)
        
        elif node_type == 'number':
            value = node['value']
            if isinstance(value, int):
                self.emit_push_int(value)
            else:
                self.emit_push_float(value)
        
        elif node_type == 'string':
            self.emit_push_string(node['value'])
        
        elif node_type == 'boolean':
            self.emit_push_bool(node['value'])
        
        elif node_type == 'null':
            self.emit_push_null()
        
        elif node_type == 'binary':
            # Generate code for the left and right operands
            self._generate_node(node['left'])
            self._generate_node(node['right'])
            # Generate code for the operation
            self.emit_binary_op(node['operator'])
        
        elif node_type == 'unary':
            # Generate code for the operand
            self._generate_node(node['operand'])
            # Generate code for the operation
            self.emit_unary_op(node['operator'])
        
        elif node_type == 'var':
            # Variable reference
            name = node['name']
            # Check if it's a local variable
            for scope in reversed(self.current_scope):
                if name in scope:
                    index = scope[name]
                    self.emit(OpCode.GET_LOCAL, index)
                    return
            # If not found, it's a global variable
            index = self.add_string(name)
            self.emit(OpCode.GET_GLOBAL, index & 0xFF, (index >> 8) & 0xFF)
        
        elif node_type == 'assign':
            # Assignment
            name = node['name']
            # Generate code for the value
            self._generate_node(node['value'])
            # Check if it's a local variable
            for scope in reversed(self.current_scope):
                if name in scope:
                    index = scope[name]
                    self.emit(OpCode.SET_LOCAL, index)
                    return
            # If not found, it's a global variable
            index = self.add_string(name)
            self.emit(OpCode.SET_GLOBAL, index & 0xFF, (index >> 8) & 0xFF)
        
        elif node_type == 'let':
            # Variable declaration
            name = node['name']
            # Generate code for the value
            self._generate_node(node['value'])
            # Add to the current scope
            if not self.current_scope:
                self.current_scope.append({})
            index = len(self.current_scope[-1])
            self.current_scope[-1][name] = index
            self.emit(OpCode.DEFINE_LOCAL, index)
        
        elif node_type == 'if':
            # If statement
            # Generate code for the condition
            self._generate_node(node['condition'])
            # Emit a jump-if-false instruction (we'll patch the jump address later)
            jump_if_false_pos = len(self.bytecode)
            self.emit(OpCode.JUMP_IF_FALSE, 0, 0)  # Placeholder for jump address
            
            # Generate code for the then branch
            self._generate_node(node['then'])
            
            if 'else' in node:
                # Emit a jump instruction to skip the else branch (we'll patch the jump address later)
                jump_pos = len(self.bytecode)
                self.emit(OpCode.JUMP, 0, 0)  # Placeholder for jump address
                
                # Patch the jump-if-false address
                else_pos = len(self.bytecode)
                self.bytecode[jump_if_false_pos + 1] = else_pos & 0xFF
                self.bytecode[jump_if_false_pos + 2] = (else_pos >> 8) & 0xFF
                
                # Generate code for the else branch
                self._generate_node(node['else'])
                
                # Patch the jump address
                end_pos = len(self.bytecode)
                self.bytecode[jump_pos + 1] = end_pos & 0xFF
                self.bytecode[jump_pos + 2] = (end_pos >> 8) & 0xFF
            else:
                # Patch the jump-if-false address
                end_pos = len(self.bytecode)
                self.bytecode[jump_if_false_pos + 1] = end_pos & 0xFF
                self.bytecode[jump_if_false_pos + 2] = (end_pos >> 8) & 0xFF
        
        elif node_type == 'while':
            # While loop
            # Record the start position of the loop
            start_pos = len(self.bytecode)
            
            # Generate code for the condition
            self._generate_node(node['condition'])
            
            # Emit a jump-if-false instruction (we'll patch the jump address later)
            jump_if_false_pos = len(self.bytecode)
            self.emit(OpCode.JUMP_IF_FALSE, 0, 0)  # Placeholder for jump address
            
            # Push loop information for break/continue
            self.loops.append({'start': start_pos, 'breaks': []})
            
            # Generate code for the body
            self._generate_node(node['body'])
            
            # Emit a jump back to the start of the loop
            self.emit(OpCode.JUMP, start_pos & 0xFF, (start_pos >> 8) & 0xFF)
            
            # Patch the jump-if-false address
            end_pos = len(self.bytecode)
            self.bytecode[jump_if_false_pos + 1] = end_pos & 0xFF
            self.bytecode[jump_if_false_pos + 2] = (end_pos >> 8) & 0xFF
            
            # Patch any break statements
            loop_info = self.loops.pop()
            for break_pos in loop_info['breaks']:
                self.bytecode[break_pos + 1] = end_pos & 0xFF
                self.bytecode[break_pos + 2] = (end_pos >> 8) & 0xFF
        
        elif node_type == 'for':
            # For loop
            # Generate code for the initializer
            if 'init' in node:
                self._generate_node(node['init'])
            
            # Record the start position of the loop
            start_pos = len(self.bytecode)
            
            # Generate code for the condition
            if 'condition' in node:
                self._generate_node(node['condition'])
            else:
                # If no condition, use true
                self.emit_push_bool(True)
            
            # Emit a jump-if-false instruction (we'll patch the jump address later)
            jump_if_false_pos = len(self.bytecode)
            self.emit(OpCode.JUMP_IF_FALSE, 0, 0)  # Placeholder for jump address
            
            # Push loop information for break/continue
            update_pos = None
            self.loops.append({'start': start_pos, 'breaks': [], 'updates': []})
            
            # Generate code for the body
            self._generate_node(node['body'])
            
            # Record the position for the update
            update_pos = len(self.bytecode)
            
            # Generate code for the update
            if 'update' in node:
                self._generate_node(node['update'])
            
            # Emit a jump back to the start of the loop
            self.emit(OpCode.JUMP, start_pos & 0xFF, (start_pos >> 8) & 0xFF)
            
            # Patch the jump-if-false address
            end_pos = len(self.bytecode)
            self.bytecode[jump_if_false_pos + 1] = end_pos & 0xFF
            self.bytecode[jump_if_false_pos + 2] = (end_pos >> 8) & 0xFF
            
            # Patch any break statements
            loop_info = self.loops.pop()
            for break_pos in loop_info['breaks']:
                self.bytecode[break_pos + 1] = end_pos & 0xFF
                self.bytecode[break_pos + 2] = (end_pos >> 8) & 0xFF
            
            # Patch any continue statements
            for continue_pos in loop_info.get('updates', []):
                self.bytecode[continue_pos + 1] = update_pos & 0xFF
                self.bytecode[continue_pos + 2] = (update_pos >> 8) & 0xFF
        
        elif node_type == 'break':
            # Break statement
            if not self.loops:
                raise Exception("Break statement outside of loop")
            
            # Emit a jump instruction (we'll patch the jump address later)
            break_pos = len(self.bytecode)
            self.emit(OpCode.JUMP, 0, 0)  # Placeholder for jump address
            
            # Record the position of the break statement
            self.loops[-1]['breaks'].append(break_pos)
        
        elif node_type == 'continue':
            # Continue statement
            if not self.loops:
                raise Exception("Continue statement outside of loop")
            
            # Emit a jump instruction to the start of the loop
            if 'updates' in self.loops[-1]:
                # For loops: jump to the update
                continue_pos = len(self.bytecode)
                self.emit(OpCode.JUMP, 0, 0)  # Placeholder for jump address
                self.loops[-1]['updates'].append(continue_pos)
            else:
                # While loops: jump to the condition
                start_pos = self.loops[-1]['start']
                self.emit(OpCode.JUMP, start_pos & 0xFF, (start_pos >> 8) & 0xFF)
        
        elif node_type == 'call':
            # Function call
            # Generate code for the function
            self._generate_node(node['callee'])
            
            # Generate code for the arguments
            for arg in node['arguments']:
                self._generate_node(arg)
            
            # Emit a call instruction with the number of arguments
            self.emit(OpCode.CALL, len(node['arguments']))
        
        elif node_type == 'function':
            # Function declaration
            name = node['name']
            params = node['parameters']
            body = node['body']
            
            # Emit a jump instruction to skip the function body (we'll patch the jump address later)
            jump_pos = len(self.bytecode)
            self.emit(OpCode.JUMP, 0, 0)  # Placeholder for jump address
            
            # Record the position of the function
            func_pos = len(self.bytecode)
            self.functions[name] = func_pos
            
            # Create a new scope for the function
            self.current_scope.append({})
            
            # Add parameters to the scope
            for i, param in enumerate(params):
                self.current_scope[-1][param] = i
            
            # Generate code for the function body
            self._generate_node(body)
            
            # Emit a return instruction if the function doesn't end with one
            if not self.bytecode or self.bytecode[-1] != OpCode.RETURN:
                self.emit_push_null()
                self.emit(OpCode.RETURN)
            
            # Restore the previous scope
            self.current_scope.pop()
            
            # Patch the jump address
            end_pos = len(self.bytecode)
            self.bytecode[jump_pos + 1] = end_pos & 0xFF
            self.bytecode[jump_pos + 2] = (end_pos >> 8) & 0xFF
            
            # Emit a function instruction
            index = self.add_string(name)
            self.emit(OpCode.FUNCTION, index & 0xFF, (index >> 8) & 0xFF, 
                     func_pos & 0xFF, (func_pos >> 8) & 0xFF, len(params))
        
        elif node_type == 'return':
            # Return statement
            if 'value' in node:
                self._generate_node(node['value'])
            else:
                self.emit_push_null()
            self.emit(OpCode.RETURN)
        
        elif node_type == 'block':
            # Block statement
            for statement in node['body']:
                self._generate_node(statement)
        
        elif node_type == 'print':
            # Print statement
            self._generate_node(node['expression'])
            self.emit_print()
        
        elif node_type == 'list':
            # List literal
            for element in node['elements']:
                self._generate_node(element)
            self.emit(OpCode.LIST, len(node['elements']))
        
        elif node_type == 'dict':
            # Dictionary literal
            for key, value in node['entries']:
                self._generate_node(key)
                self._generate_node(value)
            self.emit(OpCode.DICT, len(node['entries']))
        
        elif node_type == 'property':
            # Property access
            self._generate_node(node['object'])
            index = self.add_string(node['property'])
            self.emit(OpCode.GET_PROPERTY, index & 0xFF, (index >> 8) & 0xFF)
        
        elif node_type == 'property_assign':
            # Property assignment
            self._generate_node(node['object'])
            self._generate_node(node['value'])
            index = self.add_string(node['property'])
            self.emit(OpCode.SET_PROPERTY, index & 0xFF, (index >> 8) & 0xFF)
        
        else:
            raise Exception(f"Unknown node type: {node_type}")

def generate_bytecode(input_file, output_file):
    """
    Generate bytecode for a Vasuki file.
    """
    # Read the source code
    with open(input_file, 'r') as f:
        code = f.read()
    
    # Parse the code
    ast = parse(code, os.path.basename(input_file))
    
    # Generate bytecode
    generator = BytecodeGenerator()
    bytecode, constants, names = generator.generate_bytecode(ast)
    
    # Write the bytecode to a file
    with open(output_file, 'wb') as f:
        # Write bytecode size
        f.write(struct.pack('<I', len(bytecode)))  # 4-byte unsigned int for size
        
        # Write bytecode
        for byte in bytecode:
            f.write(struct.pack('B', byte))  # 1-byte unsigned char
        
        # Write constants size
        f.write(struct.pack('<I', len(constants)))  # 4-byte unsigned int for size
        
        # Write constants
        # (Not implemented yet)
        
        # Write names size
        f.write(struct.pack('<I', len(names)))  # 4-byte unsigned int for size
        
        # Write names
        for name in names:
            encoded = name.encode('utf-8')
            f.write(struct.pack('<I', len(encoded)))  # 4-byte unsigned int for length
            f.write(encoded)
    
    print(f"Bytecode written to {output_file}")
    return True

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python direct_bytecode.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # If output file is not specified, use the input file name with .bytecode extension
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = os.path.join(
            "vm", "bytecode_storage",
            os.path.basename(input_file) + ".bytecode"
        )
    
    # Create the bytecode storage directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Generate bytecode
    if generate_bytecode(input_file, output_file):
        print(f"Successfully generated bytecode for {input_file}")
    else:
        print(f"Failed to generate bytecode for {input_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()
