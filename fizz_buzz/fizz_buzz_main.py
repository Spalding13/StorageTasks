"""
Print numbers from 1 to 100,
for multiples of 3 print "A" instead of the number,
for multiples of 5 print "B" instead of the number,
and for multiples of both 3 and 5 print "AB" instead of the number.

The catch is that you can't use any conditionals or loops :)
"""

def fizz_buzz(n=1):
    div_by_3 = "A" * (not (n % 3))
    div_by_5 = "B" * (not (n % 5))
    
    print((div_by_3 + div_by_5) or n)
    
    (n < 100) and fizz_buzz(n + 1)

fizz_buzz()