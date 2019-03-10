import itertools
from typing import Iterator

def iter_primes() -> Iterator[int]:
     # An iterator of all numbers between 2 and
     # +infinity
     numbers = itertools.count(2)

     # Generate primes forever
     while True:
         # Get the first number from the iterator
         # (always a prime)
         prime = next(numbers)
         yield prime

         # This code iteratively builds up a chain
         # of filters...
         numbers = filter(prime.__rmod__, numbers)

for p in iter_primes():
    if p > 1000:
        break
    print(p)
