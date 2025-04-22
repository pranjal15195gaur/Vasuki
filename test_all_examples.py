import os
import subprocess
import sys

def run_command(command):
    """Run a command and return the result and exit code"""
    try:
        result = subprocess.run(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def test_example(example_file, interpreter_script):
    """Test a single example file with the specified interpreter script"""
    print(f"\nTesting {example_file} with {interpreter_script}...")
    
    command = ["python", interpreter_script, example_file]
    stdout, stderr, exit_code = run_command(command)
    
    success = exit_code == 0
    
    if success:
        print(f"✅ SUCCESS: {example_file} with {interpreter_script}")
    else:
        print(f"❌ FAILED: {example_file} with {interpreter_script}")
        print(f"Error: {stderr}")
    
    return {
        "example": example_file,
        "interpreter": interpreter_script,
        "success": success,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    }

def main():
    # Get all example files
    examples_dir = os.path.join("compiler", "examples")
    example_files = [
        os.path.join(examples_dir, f) 
        for f in os.listdir(examples_dir) 
        if f.endswith(".vasuki")
    ]
    
    # Interpreters to test
    interpreters = [
        os.path.join("compiler", "main.py"),
        os.path.join("compiler", "run_bytecode.py")
    ]
    
    # Results storage
    results = []
    
    # Test each example with each interpreter
    for example in example_files:
        for interpreter in interpreters:
            result = test_example(example, interpreter)
            results.append(result)
    
    # Print summary
    print("\n\n=== SUMMARY ===")
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    print(f"Total tests: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    
    # Print failed tests
    if total_count - success_count > 0:
        print("\nFailed tests:")
        for result in results:
            if not result["success"]:
                print(f"  - {result['example']} with {result['interpreter']}")
                print(f"    Error: {result['stderr'][:100]}...")

if __name__ == "__main__":
    main()
