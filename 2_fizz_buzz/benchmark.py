import timeit
import sys

# Increase recursion limit just in case, though 100 is fine
sys.setrecursionlimit(1500)

setup_code = """
def fizz_buzz_1(n=1):
    div_by_3 = "A" * (not (n % 3))
    div_by_5 = "B" * (not (n % 5))
    result = (div_by_3 + div_by_5) or n
    (n < 100) and fizz_buzz_1(n + 1)

def fizz_buzz_2(n=1):
    part_a = ("A", "", "")[n % 3]
    part_b = ("B", "", "", "", "")[n % 5]
    combined = part_a + part_b
    result = (str(n), combined)[bool(combined)]
    dispatch = (lambda x: None, fizz_buzz_2)
    dispatch[n < 100](n + 1)
"""

# Run each function 10,000 times and measure the total time
time_1 = timeit.timeit("fizz_buzz_1()", setup=setup_code, number=10000)
time_2 = timeit.timeit("fizz_buzz_2()", setup=setup_code, number=10000)

print(f"Implementation 1 (Short-Circuit): {time_1:.4f} seconds")
print(f"Implementation 2 (Branchless/Tuples): {time_2:.4f} seconds")