# Curveball (ECC) — Cryptohack

**Port:** 13382  
**Category:** Invalid Curve / Generator Manipulation  
**Difficulty:** Medium

---

## Challenge Overview

The server implements an ECDH-like key exchange where the client supplies:
- `private_key` (cannot be 0, 1, -1)
- `host` (target domain, e.g., `www.bing.com`)
- `curve` (must be `secp256r1`)
- `generator` (client-chosen base point)

The server computes `Q = generator * private_key` and checks if `Q` matches the trusted certificate's public key for the given `host`. If it matches, the flag is returned.

---

## Vulnerability

The client controls **both** the generator point `G` and the private key `d`. The server computes:
```
Q = d * G
```

We know the target public key `P_target` for `www.bing.com` from the certificate. We can choose `d = 2` (small, valid) and solve for `G`:
```
G = d⁻¹ * P_target  (mod n)
```
where `n` is the order of the secp256r1 curve.

---

## Attack Flow

1. Fetch the secp256r1 curve parameters (`a`, `b`, `p`, `n`, standard generator `G_std`)
2. Get the target public key `P_target` for `www.bing.com` from the server's certificate
3. Choose `d = 2`, compute `d_inv = inverse_mod(2, n)`
4. Compute malicious generator: `G_malicious = d_inv * P_target`
5. Send payload with `private_key=2`, `generator=G_malicious`, `host=www.bing.com`
6. Server computes `Q = 2 * G_malicious = P_target` → match → flag

---

## Files

| File | Description |
|------|-------------|
| `source.py` | Challenge server logic (reconstructed) |
| `solve.py` | Working solve script |
| `flow.md` | Detailed attack writeup |
| `13382.py` | Alternate solve script (port-specific) |

---

## Solution Script (`solve.py`)

```python
from pwn import *
from fastecdsa.curve import P256
from sage.all import *
import json

# Curve params
a, b, p = P256.a, P256.b, P256.p
E = EllipticCurve(GF(p), [a, b])
G_std = E(P256.gx, P256.gy)

# Target public key from certificate
P_target = E(
    0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531,
    0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A
)
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

# Choose d = 2
d = 2
d_inv = inverse_mod(d, n)
G_malicious = d_inv * P_target

# Verify
assert d * G_malicious == P_target

# Connect and send
io = remote("socket.cryptohack.org", 13382)
payload = {
    'private_key': d,
    'host': 'www.bing.com',
    'curve': 'secp256r1',
    'generator': [int(G_malicious[0]), int(G_malicious[1])]
}
io.sendline(json.dumps(payload).encode())
io.interactive()
```

---

## Key Insight

**Client-controlled generator + known target point = trivial key forgery.** The server trusts the client's generator without validation that it's the standard base point.

---

## References

- [Cryptohack - Curveball](https://cryptohack.org/challenges/curveball/)
- [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)
- [Invalid Curve Attacks](https://eprint.iacr.org/2017/576.pdf)