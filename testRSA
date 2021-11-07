import math
import rsa
p = rsa.generate_prime(512)
q = rsa.generate_prime(512)
n = p * q
e = rsa.get_public_key()
key = rsa.create_private_key(p,q)

test = input("Input something ")

test = test.encode('utf-8')
print(test)
result = int.from_bytes(test, "big")
print("un encypted value")
print(result)
testEncrypt = rsa.encrypt(result,n,e)
length = len(str(testEncrypt))
print("encrypted value ")
print(testEncrypt)
#testDecrypt = rsa.decrypt(testEncrypt,n,key)
print("key is ")
print(key)
print("n is ")
print(n)
whatever = (5 ** e) % n
print(whatever)
testDecrypt = ((whatever ** key) % n)
print("decrypted value ")
print(testDecrypt)
length2 = len(str(testDecrypt))

#result2 = testEncrypt.to_bytes(length, byteorder="big")
#output = result2.decode('ISO-8859-1')
#result2 = rsa.decrypt(result2,n,key)

#result3 = testDecrypt.to_bytes(length2, "big")
#output2 = result3.decode('ISO-8859-1')
#print(output)
#print(output2)
