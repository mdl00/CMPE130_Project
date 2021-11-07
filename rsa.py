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
 
#returns a random number generated fom 2 ^(n-1) + 1 and 2 ^ n - 1
def n_bit_random(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)
 
def get_low_prime(n):
    while True:
        candidate = n_bit_random(n)
 
         # Test divisibility by pre-generated
         # primes
        for divisor in low_primes:
            if candidate % divisor == 0 and divisor**2 <= candidate:
                break
        else: 
            return candidate
 
def is_rabin_miller(mrc):
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)

    def trail_composite(round_tester):
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
        if trail_composite(round_tester):
            return False
    return True
 
#generates a prime number given a certain number of bits
#It will create a random value relative to the given bits and run that value through a primality test
#returns a value that passes through the rabin miller primality test
def generate_prime(n):
 while True:                                    #loop forever until a prime number is found
     prime_candidate = get_low_prime(n)         #Random Value
     if not is_rabin_miller(prime_candidate):     
         continue
     else:
         return prime_candidate                 #If its prime, return the prime value


#encrypts a message given the message represented in an int value, n (p*q), and the public key
# m^e mod n
#returns the encrypted message
def encrypt(m, n, e):
    c = int((m**e) % n)
    return c

#decrypts a given message represented as a integer
# c^d mod n (typical RSA decryption formula)
#c is the message, d is the private key, n is the result of p * q
#returns the decrypted message
def decrypt(c, n, d):
    m = pow(c, d, n)
    return m



#ax + by = gcd(a , b)
#also known as bezout's theorem
#in our case we want to use this algorithim to find the gcd because it 
def extended_euclidean_algorithm(e, z):
    x,y, u,v = 0,1, 1,0
    while e != 0:
        q, r = z//e, z%e
        m, n = x - u * q, y - v * q
        z,e, x,y, u,v = e,r, u,v, m,n
        gcd = z
    return gcd, x, y


e = 65537
#a predefined constant. 65537 or 3 is the standard for e
def get_public_key():
    return e

#p and q are calculated during the creation of the server and can be changed when needed. (session key)
def create_private_key(p, q):
    e = get_public_key()
    z = (q-1)*(p-1)
    gcd, x, b = extended_euclidean_algorithm(e, z)  #gets the greatest common demoninator, the x from the equation(AKA the private key), and the remaning y from the equation.
    d = x                                          
    d = d % z                                       #This is for when D is negative
                                                    #-D = -D + k * phi #equation from a+k⋅m
    if(d < 0):                                      #Simply just increment k so that D becomes positive            
        d += z
    return d
