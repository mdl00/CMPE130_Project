import random
import timeit
# List of low primes. Source: https://en.wikipedia.org/wiki/List_of_prime_numbers
low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349,
                     353, 359, 367, 373, 379, 383, 389,	397,
                     401, 409]
 
def nBitRandom(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)
 
def getLowLevelPrime(n):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
 
         # Test divisibility by pre-generated
         # primes
        for divisor in low_primes:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else: return pc
 
def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True
 
def generatePrime(n):
 while True:
     prime_candidate = getLowLevelPrime(n)
     if not isMillerRabinPassed(prime_candidate):
         continue
     else:
         return n

def generatePubKey(p, q):
    n = p*q
    z = (p-1)*(q-1)
    e = nBitRandom(2048)
    while (e >= n or extendedEuclideanAlgorithm(e, z) != 1):
         e = nBitRandom(2048)
    return e
 
def calculatePrivKey(p, q, e):
    n = p*q
    z = (p-1)*(q-1)
    d = nBitRandom(2048)
    while (int((d*e) % z) != 1 or d >= n):
        d = nBitRandom(2048)
    return d

def encrypt(m, n, e):
    c = int((m**e) % n)
    return c

def decrypt(c, n, d):
    m = int((c**d) % n)
    return m

#ax + by = gcd(a , b)
#also known as bezout's theorem
#in our case we want to use this algorithim to find the gcd because it 
def extendedEuclideanAlgorithm(e, z):
    x,y, u,v = 0,1, 1,0
    while e != 0:
        q, r = z//e, z%e
        m, n = x - u * q, y - v * q
        z,e, x,y, u,v = e,r, u,v, m,n
        gcd = z
    return gcd, x, y

p = generatePrime(2048)
q = generatePrime(2048)
e = 65537
z = (q-1)*(p-1)
gcd, a, b = extendedEuclideanAlgorithm(e, z)
d = a
d = d % z
if(d < 0):
    d += z
#d = calculatePrivKey(p, q, e)
print("Public key is ", e)
print("Private key is ", d)
