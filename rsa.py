import math
 
message = int(input("Enter the message to be encrypted: ")) 
 
p = 11
q = 7
e = 3
n = p*q
phi = (p-1)*(q-1)
 
def encrypt(m):
    c = int(math.pow(m,e) % n)
    return c

def decrypt(c):
    d = 1
    while (d*e % 60 is not 1 and d < 100000):
        d = d + 1
    print("d is calculated to be: ", d);
    m = int(math.pow(c,d) % n)
    return m
 
print("Original Message is: ", message)
c = encrypt(message)
print("Encrypted message is: ", c);
m = decrypt(c);
print("Decrypted message is: ", m);