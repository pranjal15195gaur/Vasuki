import os
import subprocess
import sys
import glob

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

def test_example(example_file):
    """Test a single example file with run_bytecode.py"""
    print(f"\nTesting {example_file}...")
    
    command = ["python", "compiler/run_bytecode.py", example_file]
    stdout, stderr, exit_code = run_command(command)
    
    success = exit_code == 0
    
    if success:
        print(f"✅ SUCCESS: {example_file}")
    else:
        print(f"❌ FAILED: {example_file}")
        print(f"Error: {stderr}")
    
    return {
        "example": example_file,
        "success": success,
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    }

def main():
    # Get all example files
    example_files = glob.glob("compiler/examples/*.vasuki")
    
    # Results storage
    results = []
    
    # Test each example
    for example in example_files:
        result = test_example(example)
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
                print(f"  - {result['example']}")
                error_lines = result['stderr'].strip().split('\n')
                if error_lines:
                    # Print just the first few lines of the error
                    print(f"    Error: {error_lines[0]}")
                    if len(error_lines) > 1:
                        print(f"           {error_lines[1]}")

if __name__ == "__main__":
    main()
