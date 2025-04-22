from parser import parse
from bytecode_pure import BytecodeGenerator, BytecodeVM
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_bytecode.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Read the input file
    try:
        with open(filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    
    try:
        # Parse the code
        ast = parse(code)
        print("AST formed successfully")
        
        # Generate bytecode
        generator = BytecodeGenerator()
        bytecode = generator.generate(ast)
        print("\nBytecode generated:")
        print(bytecode)
        
        # Run the bytecode
        print("\nRunning the program:")
        vm = BytecodeVM(bytecode)
        result = vm.run()
        
        print("\nExecution complete.")
        if result is not None:
            print("Result:", result)
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
