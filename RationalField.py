from IntegerTools import *
import math

class RationalField:  # Creates field of rational numbers with standard arithmetic rules (no decimals)

    def simplify(self, x):  # Simplifies a rational number
        sign = lambda z: 1 if z >= 0 else -1
        return [sign(x[1])*int(x[0] / gcd(x[0], x[1])), sign(x[1])*int(x[1] / gcd(x[0], x[1]))]

    def add(self, x, y):
        return self.simplify([x[0] * y[1] + x[1] * y[0], x[1] * y[1]])

    def addinv(self, x):
        return [-x[0], x[1]]

    def multiply(self, x, y):
        return self.simplify([x[0] * y[0], x[1] * y[1]])

    def multinv(self, x):
        if x[1] != 0:
            return [x[1], x[0]]
        else:
            return None

    def identify(self, x):  # Natural identification of integers as subset of rationals.
        if type(x) == list:
            return x
        elif type(x) == int:
            return [x, 1]

    def zero(self): # Returns the zero element of the field
        return [0, 1]

    def one(self): # Returns the zero element of the field
        return [1, 1]

    def tostring(self, r):
        r = self.simplify(r)
        if r[1] == 1:
            return r[0]
        else:
            return f"{r[0]}/{r[1]}"
        
    def type(self):
        return "Rational"