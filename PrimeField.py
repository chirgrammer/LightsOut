from IntegerTools import *
import math


class PrimeField:
    def __init__(self, prime):
        if isprime(prime):
            self.prime = prime

    def add(self, x, y):
        return (x + y) % self.prime

    def addinv(self, x):
        return (-x) % self.prime

    def multiply(self, x, y):
        return (x * y) % self.prime

    def multinv(self, x):
        if x % self.prime != 0:
            return (findsol(x, self.prime, 1)[0] % self.prime)
        else:
            return None

    def order(self, x):
        ordr = 1
        if x != 0:
            y = x
            while y != 1:
                ordr += 1
                y = self.Multiply(y, x)
        return ordr

    def identify(self, x):  # Returns the representative between 0 and prime-1 of x
        return x % self.prime

    def zero(self):  # Returns the zero element of the field
        return 0

    def one(self):  # Returns the zero element of the field
        return 1

    def tostring(self, a): # Returns "a".
        a = self.identify(a)
        return a
    
    def type(self):
        return f"{self.prime}"
