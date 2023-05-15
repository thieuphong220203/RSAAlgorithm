import math
import random
import time

def choose_prime_number():
    #choose number in range [100,1000]
    # n = random.randrange(1000,10000)
    n = random.randrange(100,500)
    #check the number whether is prime or not
    while not is_prime(n):
        n = random.randrange(100,500)
    return n

#checkPrime Function
def is_prime(n):
    '''
    use for loop from 2 to sqrt(n) if we find any number i such that n % i == 0 
    then we conclude n is not prime and return false 
    '''
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n))+1):
        if n % i ==0:
            return False
    return True

#Find Greatest Common divisor
def gcd(a,b):
    if b == 0:
        return a
    return gcd(b, a % b)

#find inverse of a mod n (explain in 521H0136_1.py)
def find_mod_inverse(a,m):
    gcd,y,x = extended_Euclid_algorithm(m,a%m)
    if gcd != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        while x < 0:
            x = x + m
    return x

#extended euclid algorithm for finding inverse
def extended_Euclid_algorithm(a,n):
    if n == 0:
        return a,1,1
    gcd,x1,y1 = extended_Euclid_algorithm(n,a%n) #recursive 
   #formula proof in 1.5.2 (Extended Euclid Algorithm finding modula inverse)
    x = y1 
    y = x1 - (a//n)*y1
    return (gcd,x,y)

def find_e(phi_n):
    #(n,e) is public key of rsa algorithm 
    '''
        e must be integer
        1 < e < phi(n) - 1
        e and phi(n) must be co-prime --> gcd(e,phi(n)) = 1
    '''
    e = random.randrange(1,(phi_n))
    #check e and phi_n is whether co-prime or not prime
    while(gcd(e,phi_n) != 1):
        #if e is not co-prime --> choose another one
        e = random.randrange(1,(phi_n))
    return e

#create key
def create_key_pair(p,q):
    if p == q:
        p = choose_prime_number()
    
    n = p * q
    #find phi(n): phi(n) which p,q is prime --> phi(q) = q - 1 and phi(p) = p - 1
    phi = (p-1) * (q-1)
    e = find_e(phi)
    #find d using: e*d = 1 = gcd(e,phi(n)) --> d is the inverse of e modulo phi(n) --> using extended algorithm7 
    d = find_mod_inverse(e,phi)
    return ((e,n),(d,n))

def encrypt(pk, mess):
    #use public key (e,n) to encrypt message
    public_key, n = pk
    c = []
    for char in mess:
        #use the public key to encrypt the Unicode code point
        # encrypted_code_point = pow(ord(char), public_key, n)
        #ord function to convert character to unicode code
        #encrypt mess: c = m^e(mod n)
        encrypted_code_point = (ord(char) ** public_key) % n
        
        c.append(encrypted_code_point)
    return c

def decrypt(pk, c):
    #use private key (d,n) to decrypt message
    private_key, n = pk
    # plain = [chr(pow(char, private_key, n)) for char in c]
    #chr: convert unicode code to the character
    m = []
    for char in c:
        # dec = pow(char, private_key, n)
        dec = (char ** private_key) %n
        m.append(chr(dec))
    return ''.join(m) #join the character to form a origin mess

#=================================Implement==========================================

#Initialize p, q (prime)
p = choose_prime_number()
q = choose_prime_number()

#create public and private key
public_key, private_key = create_key_pair(p,q)

#
print("p=",p)
print("q=",q)
print("public key: ", public_key)
print("private key: ", private_key)

# Encrypt a message
start_time = time.time()
message = "Can u hear me"
c = encrypt(public_key, message)
print("message need sending:", message)
print("Message after encryption c: ", c)


# # Decrypt the message
decrypted_message = decrypt(private_key,c)
print("Message after decryption m': ", decrypted_message)

end_time = time.time()

print("Encrypt and Decrypt method taken time: ", end_time-start_time,"second.")
