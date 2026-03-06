"""
Print numbers from 1 to 100,
for multiples of 3 print "A" instead of the number,
for multiples of 5 print "B" instead of the number,
and for multiples of both 3 and 5 print "AB" instead of the number.

The catch is that you can't use any conditionals or loops :)
"""

def branchless_fizzbuzz(n=1):
    # Use tuples because they are immutable and more memory efficient than lists.
    # on the right side we have index evaluation, which is O(1) and does not involve branching.
    part_a = ("A", "", "")[n % 3]
    part_b = ("B", "", "", "", "")[n % 5]
    combined = part_a + part_b
    
    # Same technique as above: Branchless fallback using boolean casting as an integer index
    # An empty string "" is Fals, which is the integer 0
    # A non-empty string like "A", "B", or "AB" is True, which is the integer 1.
    result = (str(n), combined)[bool(combined)]
    print(result)
    
    # Same technique as above: Branchless recursion using boolean casting as an integer index
    dispatch = (lambda x: None, branchless_fizzbuzz)
    dispatch[n < 100](n + 1)

if __name__ == "__main__":
    branchless_fizzbuzz()