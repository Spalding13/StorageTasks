import struct
import time
import os

def generate_mock_data(filename="test_data.bin"):
    """
    Generates a deterministic binary file of uint32_t integers.
    Used to sanity-check the bitset counting logic before running against the 4GB prod file.
    
    Expected totals:
    - Unique numbers (1a): 2,000,001
    - Seen exactly once (1b): 1,000,000
    """
    start = time.time()
    
    with open(filename, 'wb') as f:
        # Group 1: 1M numbers appearing exactly once (Range: 1 to 1,000,000)
        # These should count towards both 1a and 1b.
        for i in range(1, 1_000_001):
            f.write(struct.pack('<I', i))
            
        # Group 2: 1M numbers appearing exactly twice (Range: 2,000,000 to 2,999,999)
        # These should count towards 1a, but be disqualified from 1b.
        for i in range(2_000_000, 3_000_000):
            packed = struct.pack('<I', i)
            f.write(packed)
            f.write(packed)  # force duplicate
            
        # Group 3: Mass duplication stress test.
        # Writing '4,000,000' five million times.
        # This adds exactly 1 to the unique count (1a), and 0 to the seen-once count (1b).
        chunk = struct.pack('<I', 4_000_000) * 10000 
        for _ in range(500):
            f.write(chunk)

    mb_size = os.path.getsize(filename) / (1024 * 1024)
    print(f"Mock data generated: {mb_size:.2f} MB in {time.time() - start:.2f}s")
    print("Run counting.py to verify against expected totals.")

if __name__ == "__main__":
    generate_mock_data()