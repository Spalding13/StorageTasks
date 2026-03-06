"""
UInt32 is a data type that represents an unsigned 32-bit integer, 
meaning it only stores non-negative whole numbers ranging from 0 to 4,294,967,295.

Commonly used in programming, UInt32 is ideal for scenarios requiring a wide range of positive values. 
Its unsigned nature eliminates the need to account for negative numbers in calculations, streamlining logic and efficient memory use, 
especially in applications focused on hardware performance or large datasets.

Naming convention of uint32_t
u: Unsigned. This means there are no negative numbers. The value starts at 0.
int: Integer.
32: It occupies exactly 32 bits of memory. Since 1 byte is 8 bits, this means every single number takes up exactly 4 bytes.
_t: Just a naming convention meaning "type".
Each number in the range of 0 to 4,294,967,295. One number takes exactly 4 bytes of memory.

Python's standard int type is dynamic, from 28 bytes or more. 
This introduces memory overhead compared to fixed-size types like UInt32.
Since I am trying to count the number of unique numbers, I can use a set. Sets in
Python is implemented as a hash table. Inside it, each entry is stored as a follows:
- A cached hash value of the object (8 bytes on a 64-bit system).
- A pointer to the object (8 bytes on a 64-bit system).
That makes 8+8 = 16 bytes of overhead per entry in the set, in addition to the memory used by the object itself.

So, If I try to store 1 million numbers in a python set:
1 billion * (28 + 16) bytes = 44 million bytes = 44 GB of memory, which is not feasible.
Possible OOM (out of memory) Kill by the operating system.

Lets assume: little-endian because the product requires x86 architecture.

Solution: Create a bitmap array of size 4,294,967,295.
Each index in the bitmap corresponds to a number in the range of 0 to 4,294,967,295.
If the number is present, we set the corresponding bit to 1; otherwise, it remains 0.

Division and modulo operations are relatively slow for a CPU. 
Bitwise operations operate directly on the CPU registers in a single clock cycle.

Example:
Byte Index 0 (Holds nums 0-7):   [0 0 0 0 0 0 0 0]
Byte Index 1 (Holds nums 8-15):  [0 0 0 0 0 0 0 0]

We read 13. Which byte holds it?
13 // 8 = 1 -> this is the byte index.
How many full boxes did I completely fill up and skip past?
This becomes >> 3 (which is the same as dividing by 8).

13 % 8 = 5 -> this is the bit index within that byte.
"How many items are left over to put into the current box?
Modulo becomes & 7 (which is the same as modulo 8).
"""

import os
import time
import array # OPTIMIZATION 1: Replaced struct with array

def process_billion_integers(file_path):
    print(f"Allocating bitsets (1GB total)...")
    # 512 MB = 2^29 bytes. We allocate two of them.
    seen_at_least_once = bytearray(1 << 29)
    seen_multiple = bytearray(1 << 29)
    
    print(f"Processing file: {file_path}")
    start_time = time.time()
    
    with open(file_path, 'rb') as f:
        while True:
            # Create an empty C-style array of unsigned 32-bit integers ('I')
            chunk = array.array('I')
            
            try:
                # Read exactly 1,000,000 integers straight from the file into the array
                chunk.fromfile(f, 1_000_000)
            except EOFError:
                # This safely catches the end of the file when less than 1M ints remain
                pass
            
            if not chunk:
                break  # End of file
            
            for num in chunk:
                byte_index = num >> 3   # num // 8
                bit_offset = num & 7    # num % 8
                mask = 1 << bit_offset
                
                # Check if we have seen this number at least once
                if not (seen_at_least_once[byte_index] & mask):
                    # First time seeing it!
                    seen_at_least_once[byte_index] |= mask
                else:
                    # We've seen it before, so mark it in the multiple bitset
                    seen_multiple[byte_index] |= mask

    print(f"File reading and bitset population took: {time.time() - start_time:.2f} seconds")
    
    print("Counting bits... (Using C-level execution)")
    counting_start = time.time()
    
    # OPTIMIZATION 2: Calculate the results by counting bits at the C level
    unique_count = int.from_bytes(seen_at_least_once, byteorder='little').bit_count()
    multiple_count = int.from_bytes(seen_multiple, byteorder='little').bit_count()
        
    seen_only_once = unique_count - multiple_count
    
    print(f"Bit counting took: {time.time() - counting_start:.2f} seconds")
    
    return unique_count, seen_only_once

if __name__ == "__main__":
    test_file = "test_data.bin"
    
    if os.path.exists(test_file):
        unique, only_once = process_billion_integers(test_file)
        print("\n--- RESULTS ---")
        print(f"Task 1a (Unique numbers):        {unique}")
        print(f"Task 1b (Seen exactly once):     {only_once}")
    else:
        print(f"File '{test_file}' not found. Please provide the binary file.")