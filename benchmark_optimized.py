#!/usr/bin/env python3
"""
Benchmark script for comparing normal Vasuki run vs optimized bytecode Vasuki run.
"""

import os
import time
import subprocess
import statistics

# Files to benchmark
files = [
    "compiler/presentation/boolean_test.vasuki",
    "compiler/presentation/dynamic_closures.vasuki",
    "compiler/presentation/if_else_cond.vasuki",
    "compiler/presentation/dict_methods_test.vasuki",
    "compiler/presentation/functions.vasuki"
]

# Number of iterations for each benchmark
iterations = 5

def run_benchmark(file_path, mode):
    """Run a benchmark for a file in the specified mode."""
    times = []

    print(f"Benchmarking {file_path} in {mode} mode...")

    for i in range(iterations):
        if mode == "normal":
            # Since we don't have run_vasuki_fixed.py, use the regular VM as baseline
            start_time = time.time()
            subprocess.run(["./run_vasuki_vm.sh", file_path], stdout=subprocess.DEVNULL)
            end_time = time.time()
        elif mode == "bytecode":
            # Regular bytecode Vasuki run
            start_time = time.time()
            subprocess.run(["./run_vasuki_vm.sh", file_path], stdout=subprocess.DEVNULL)
            end_time = time.time()
        else:
            # Optimized bytecode Vasuki run
            start_time = time.time()
            subprocess.run(["./run_vasuki_direct.sh", file_path], stdout=subprocess.DEVNULL)
            end_time = time.time()

        execution_time = end_time - start_time
        times.append(execution_time)
        print(f"  Run {i+1}: {execution_time:.6f} seconds")

    # Calculate average time
    average_time = statistics.mean(times)
    print(f"  Average time: {average_time:.6f} seconds")

    return average_time

def main():
    """Main function."""
    # Create results file
    with open("benchmark_optimized_results.csv", "w") as f:
        f.write("File,Regular VM (s),Optimized VM (s),Speedup Factor\n")

    # Run benchmarks
    for file_path in files:
        filename = os.path.basename(file_path)

        # Run regular bytecode mode benchmark
        regular_time = run_benchmark(file_path, "bytecode")

        # Run optimized bytecode mode benchmark
        optimized_time = run_benchmark(file_path, "optimized")

        # Calculate speedup factor
        if optimized_time > 0:
            speedup = regular_time / optimized_time
        else:
            speedup = "N/A"

        # Add to results file
        with open("benchmark_optimized_results.csv", "a") as f:
            f.write(f"{filename},{regular_time:.6f},{optimized_time:.6f},{speedup:.2f}\n")

        print("-" * 40)

    print("Benchmark completed. Results saved to benchmark_optimized_results.csv")

if __name__ == "__main__":
    main()
