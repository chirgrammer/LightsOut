import math

def gcd(x,y): # Finds greatest common divisor of two integers via Euclid's algorithm
    x = abs(x)
    y = abs(y)
    tempint = x
    if x < y:
        x = y
        y = tempint
    while y != 0:
        tempint = x % y
        x = y
        y = tempint
    return x

def findsol(a,b,d): # Finds an integer solution to the integer equation ax+by = d if exists and returns none otherwise.
    a1 = abs(a)
    b1 = abs(b)
    g = gcd(a, b)
    if g != 0 and d % g != 0: # checks if a solution can exist when g is nonzero
        return None
    # Dealing with cases where at least one of a, b, d are zero.
    if g == 0 and d != 0:
        return None
    elif g == 0 and d == 0:
        return [1, 1]
    if a != 0 and b == 0 and d != 0:
        if d % a == 0:
            return [int(d/a), 0]
        else:
            return None
    if a == 0 and b != 0 and d != 0:
        if d % b == 0:
            return [0, int(d/b)]
        else:
            return None
    if d == 0:
        return [b, -a]
    # The above conditions take care of all cases where any of a, b, d are zero.
    # Hence, we proceed by Euclid's algorithm.
    m = int(d/g)
    quotientlist = []
    tempint = a1
    if a1 < b1:
        a1 = b1
        b1 = tempint
    while b1 != 0:
        quotientlist.append(math.floor(a1/b1))
        tempint = a1 % b1
        a1 = b1
        b1 = tempint
    # As none of a, b, d are zero, quotient list will always be nonempty with the last element being
    # extraneous.
    quotientlist.pop()
    # If the resulting list is empty then, either a | b or b | a. In this case, we solve the equation explicitly.
    if not quotientlist:
        if abs(a) > abs(b):
            c = int(a/b)
            return [m, m*(1-c)]
        else:
            c = int(b/a)
            return [m*(1-c), m]
    # Handling the general case when quotient list is nonempty by backwards Euclidean algorithm.
    c = 1
    d = -quotientlist.pop()
    temp = c
    while quotientlist:
        c = d
        d = temp-d*quotientlist.pop()
        temp = c
    if abs(a) > abs(b):
        return [c, d]
    else:
        return [d, c]

def isprime(z): # Input a positive integer and output whether it is prime or not
    for i in range(2, math.floor(math.sqrt(z))+1):
        if z % i == 0:
            return False
    return True

def generatePrimes(n): # Returns a list of the first n primes.
    primes = [2]
    currentInteger = 3
    isPrime = True
    while len(primes) < n:
        isPrime = True
        for p in primes:
            if currentInteger % p == 0:
                isPrime = False
        if isPrime:
            primes.append(currentInteger)
        currentInteger += 1
    return primes