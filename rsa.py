message = int(input("Enter the message to be encrypted: ")) 
 
p = 11
q = 13
e = 7
n = p*q
z = (p-1)*(q-1)
 
def encrypt(m):
    c = int((m**e) % n)
    return c

def decrypt(c):
    d = 1
    while (int((d*e) % z) is not 1 and d < 100000):
        d = d + 1
    m = int((c**d) % n)
    return m
 
print("Original Message is: ", message)
c = encrypt(message)
print("Encrypted message is: ", c);
m = decrypt(c);
print("Decrypted message is: ", m);
