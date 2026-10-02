from pwn import *
from fastecdsa.curve import P256
from sage.all import *
import json
b = P256.b
a = P256.a
p = P256.p
E= EllipticCurve(GF(p), [a,b])
G = E(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
                    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)
Point_bing = E(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
h = inverse_mod(2,n)
g = h*Point_bing
assert g * 2 == Point_bing
io = remote("socket.cryptohack.org",13382)
payload = {
    'private_key':2, 
    'host':'www.bing.com',
    'curve':'secp256r1',
    'generator': [int(g[0]),int(g[1])]
}
io.sendline(json.dumps(payload).encode())
io.interactive()