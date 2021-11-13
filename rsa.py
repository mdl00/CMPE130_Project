import random
import timeit

# Compute x^y mod p
def power(x, y, p):
    res = 1      # Initialize result
    # Update x if x >= p
    x = x % p      
    while y > 0:
        if y & 1:   #If y have the last bit of 1 (is odd number)
            res = (res*x) % p   

        y >>= 1       #bit shift right, or y/2
        x = x*x % p     

    return res

# Use Miller Rabin Algorithm to check if number is prime
def is_rabin_miller(d, n):
    a = random.randint(2, n-2)  # Pick a random number in range [2, n-2]
    x = power(a, d, n)          # Compute a^d%n and store in x

    if x == 1 or x == n - 1:    
        return True

    #Recompute quotient and remainder
    while d != n - 1:
        x = x*x % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    return False

# because Miller is a probability-based algorithm
# people suggest checking a number is prime with this algorithm about 40 times
# check a number is prime
def is_prime(n, k=40):
    # Handle base cases
    if n < 2:
        return False      
    elif n == 2 or n == 3:
        return True
    elif n % 2 == 0:            
        return False       

    d = n - 1
    #Find r such that n = 2^d * r + 1 for some r >= 1
    while (d % 2 == 0):
        d = int(d // 2)     #Get the whole part of d/2

    # Miller test
    for i in range(k):
        if not is_rabin_miller(d, n):
            return False

    return True

#Obtain a large random number
def generate_large_number(bit_len):
    p = random.getrandbits(bit_len) # generate random bits
    #Apply a mask to set MSB and LSB to 1
    p |= (1 << bit_len - 1) | 1
    return p

#generates a prime number given a certain number of bits
#It will create a random value relative to the given bits and run that value through a primality test
#returns a value that passes through the rabin miller primality test
def generate_prime(bit_len=1024):
    n = 4   # initial phase
    #Generate a large number until it is prime
    while not is_prime(n, 40):
        n = generate_large_number(bit_len)
    return n


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



#Computing ax + by = gcd(a , b), also known as bezout's theorem
#Returns the GCD of e and z
def extended_euclidean_algorithm(e, z):
    x,y, u,v = 0,1, 1,0
    while e != 0:
        #we obtain the quotient q by performing integer division, and the remainder r
        q, r = z//e, z%e
        #we calculate the new values of u and v, temporarily stored in m and n
        #the new values are obtained by subtracting the quotient * the new value from the old value
        m, n = x - u * q, y - v * q
        #swapping the new values into the intended variables
        z,e, x,y, u,v = e,r, u,v, m,n
        gcd = z
    #returns gcd(a, b), x, and y
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
