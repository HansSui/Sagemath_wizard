from Crypto.Util.number import getPrime
from Crypto.Random import random
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
import hashlib
import os
from sage.all import *
import sys
sys.path.append("/home/han-sui/Sagemath_wizard")
from CS_function import decrypt_flag
from ECC import Pohlig_hellman_ECC
FLAG = b"crypto{???????????????????}"

'''''
def gen_key_pair(G, nbits):
    n = random.getrandbits(nbits)
    P = n*G
    return P.xy()[0], n
'''

def gen_shared_secret(P, n):
	S = n*P
	return S.xy()[0]
'''''

def encrypt_flag(shared_secret: int):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    # Prepare data to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data


# Efficient key exchange
nbits = 64
pbits = 256

# Curve parameters
p = getPrime(pbits)
a = 1
b = 4
E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]

print(f"Sending curve parameters:")
print(f"{E}")
print(f"Generator point: {G}\n")

# Generate key pairs
ax, n_a = gen_key_pair(G, nbits)
bx, n_b = gen_key_pair(G, nbits)

print(f"Alice sends public key: {ax}")
print(f"Bob sends public key: {bx}\n")
# Calculate point from Bob
B = E.lift_x(bx)
'''
p=99061670249353652702595159229088680425828208953931838069069584252923270946291
a = 1
b = 4
E = EllipticCurve(GF(p), [a,b])
Generator = E(43190960452218023575787899214023014938926631792651638044680168600989609069200,20971936269255296908588589778128791635639992476076894152303569022736123671173)
A_x = 87360200456784002948566700858113190957688355783112995047798140117594305287669
B_x = 6082896373499126624029343293750138460137531774473450341235217699497602895121
B = E.lift_x(B_x)
A = E.lift_x(A_x)
A = -A
# Encrypted flag with shared secret
'''''
shared_secret = gen_shared_secret(B,n_a)
encrypted_flag = encrypt_flag(shared_secret)

print(f"Alice sends encrypted_flag: {encrypted_flag}")
'''
iv ='ceb34a8c174d77136455971f08641cc5'
ciphertext = 'b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453'
order = E.order()
print("E.order() =", order)
print("Phân tích thừa số:", factor(order))
na = Pohlig_hellman_ECC()
secret = gen_shared_secret(B,na)
print(decrypt_flag(secret, iv,ciphertext))