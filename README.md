[Storage-Tasks Project]

This repository contains four main folders, each dedicated to a specific data processing or algorithmic task. Below you'll find descriptions and instructions for each section.

---

## 1. Counting Bin Numbers

### Purpose

Efficiently count unique unsigned 32-bit integers from large binary files, using bitmaps to minimize memory usage. Includes tools for generating deterministic test data and analyzing memory overhead.

### Files

- counting.py: Explains UInt32, memory overhead, and bitset solution for counting unique numbers.
- generate_deterministic_file.py: Generates a binary file of uint32_t integers for testing.

### Instructions

1. Generate test data:
   python generate_deterministic_file.py
2. Run the counting logic (see counting.py for algorithm details).

---

## 2. Fizz Buzz

### Purpose

Implements and benchmarks branchless FizzBuzz algorithms in Python, avoiding conditionals and loops.

### Files

- fizz_buzz_main.py: Branchless FizzBuzz implementation using tuples and recursion.
- benchmark.py: Compares performance of two FizzBuzz implementations using timeit.

### Instructions

1. Run the branchless FizzBuzz:
   python fizz_buzz_main.py
2. Benchmark both implementations:
   python benchmark.py

---

## 3. Big Data Analyze

### Purpose

Efficiently analyze massive compressed JSON arrays (16+ GB) using iterative streaming with ijson and bz2, avoiding out-of-memory errors.

### Files

- determine_structure.py: Streams and counts disk models from a large bz2-compressed JSON array using ijson.
- bigf_json_bz2: The compressed data file (rename as needed).
- notes.txt: Additional notes.

### Instructions

1. (Optional) Download the data file using wget or the built-in Python function
2. Run the analysis:
   python determine_structure.py

---

## Requirements

See requirements.txt for dependencies.

---

## General Notes

- All scripts require Python 3.7+.
- For large files, ensure you have sufficient disk space and memory.
- For compressed files, install ijson and requests as needed.
