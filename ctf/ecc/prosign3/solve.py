from ecdsa.ecdsa import generator_192,Public_key, Private_key, Signature
from hashlib import sha1
from pwn import *
import json




g = generator_192
n = g.order()
io = remote("socket.cryptohack.org",13381)
payload1 = {
    'option' : 'sign_time'
}
io.sendline(json.dumps(payload1).encode())
h = io.recvuntil(b"}").decode()
data = json.loads(h[h.find("{"):])
msg = data['msg']
r = data['r']
s = data['s']
payload2 = {
    'option' :'verify',
    'msg': msg,
    'r': r,
    's': s
}
io.sendline(json.dumps(payload2).encode())
res = io.recvuntil(b"}").decode()
io.interactive()
