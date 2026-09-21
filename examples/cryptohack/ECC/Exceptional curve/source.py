from Crypto.Cipher import AES
import sys
sys.path.append("/home/han-sui/Sagemath_wizard")
from Crypto.Util.Padding import pad, unpad
from random import randint
import hashlib
from sage.all import *
from CS_function import decrypt_flag
FLAG = b'crypto{??????????????????????}'




def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()[0]

''''
def encrypt_flag(flag):
    # Bob's public key
    b_x = 0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38
    b_y = 0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf
    B = E(b_x, b_y)
    # Calculate shared secret
    A, nA = gen_public_key()
    print(f'Public Key: {A}')
    secret = shared_secret(B, nA)
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    # Prepare encryption to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data
'''

# Curve params
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

# Define curve
E = EllipticCurve(GF(p), [a, b])

# Protect against Pohlig-Hellman Algorithm
assert is_prime(E.order())
b_x = 0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38
b_y = 0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf
B = E(b_x, b_y)

'''''
encrypted_flag = encrypt_flag(FLAG)
print(encrypted_flag)
'''''
iv=  '719700b2470525781cc844db1febd994'
encrypted_flag= '335470f413c225b705db2e930b9d460d3947b3836059fb890b044e46cbb343f0'

Generator =  E(3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005,4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850)
Public_Key= E(4748198372895404866752111766626421927481971519483471383813044005699388317650395315193922226704604937454742608233124831870493636003725200307683939875286865,2421873309002279841021791369884483308051497215798017509805302041102468310636822060707350789776065212606890489706597369526562336256272258544226688832663757)
#knowing: Public_Key = Private_key * G retrieve Private key by turning it into Public_key = n*G --> DLP prob
#butt it's too big so no bsgs / pohlig hellman
def lift(P, E, p):
    # lift point P from old curve to a new curve
    Px, Py = map(ZZ, P.xy())
    for point in E.lift_x(Px, all=True):
         # take the matching one of the 2 points corresponding to this x on the p-adic curve
        _, y = map(ZZ, point.xy())
        if y % p == Py:
            return point
E_adic = EllipticCurve(Qp(p), [a+p*13, b+p*37]) 
G = p * lift(Generator, E_adic, p)
P = p * lift(Public_Key, E_adic, p)

# Calculate discrete log
Gx, Gy = G.xy()
Px, Py = P.xy()
found_key = int(GF(p)((Px / Py) / (Gx / Gy)))
secret = shared_secret(B, found_key)
print(decrypt_flag(secret, iv,encrypted_flag))

#smart attack where E.order == p
