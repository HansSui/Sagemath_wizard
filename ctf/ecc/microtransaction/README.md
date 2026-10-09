# Microtransaction (ECC) — Cryptohack

**Category:** ECDH + Pohlig-Hellman (Smooth Order)  
**Difficulty:** Medium

---

## Challenge Overview

Alice and Bob perform an ECDH key exchange on a custom curve with a **smooth order** (64-bit private keys, 256-bit prime field). The flag is encrypted with AES-CBC using a SHA1-derived key from the shared secret.

We are given:
- Curve parameters (`p, a, b, G`)
- Alice's public key `A_x` (x-coordinate only)
- Bob's public key `B_x` (x-coordinate only)
- Encrypted flag (`iv`, `ciphertext`)

We need to recover Alice's private key `n_a` to compute the shared secret `S = n_a * B`.

---

## Vulnerability

**Pohlig-Hellman on smooth curve order:**

The curve order `n = #E(GF(p))` factors into small primes:
```
n = 2^2 * 3 * 5 * 7 * 13 * 19 * 31 * 37 * 73 * 109 * 163 * 271 * 433 * 547 * 1093 * 1459 * 2917 * 3541 * 5419 * 12163 * 262657
```

Since `n` is smooth (largest factor ~262k), the discrete logarithm `n_a = log_G(A)` can be computed efficiently using **Pohlig-Hellman**:
1. For each prime power `p^e || n`, compute `n_a mod p^e`
2. Combine via Chinese Remainder Theorem

The private key `n_a` is also small (64-bit), but Pohlig-Hellman works regardless of key size when the group order is smooth.

---

## Attack Flow

1. **Reconstruct curve** from given parameters
2. **Lift x-coordinates** to points `A, B` using `E.lift_x()`
3. **Compute curve order** `n = E.order()` and factor it
4. **Pohlig-Hellman**: For each prime power factor `p^e`:
   - Reduce base point `G' = (n/p^e) * G` (order `p^e`)
   - Reduce target `A' = (n/p^e) * A`
   - Solve DLP in subgroup of order `p^e` (BSGS or brute force)
5. **CRT** to combine `n_a mod p^e` → `n_a mod n`
6. **Shared secret**: `S = n_a * B`
7. **Decrypt flag**: AES-CBC with `key = SHA1(S)[:16]`

---

## Files

| File | Description |
|------|-------------|
| `source.py` | Challenge source with Pohlig-Hellman solve |
| `output.txt` | Captured parameters: curve, `A_x`, `B_x`, `iv`, `ciphertext` |

---

## Solution Script (`source.py` — key section)

```python
from sage.all import *
from CS_function import decrypt_flag
from ECC import Pohlig_hellman_ECC

# Curve parameters from output.txt
p = 99061670249353652702595159229088680425828208953931838069069584252923270946291
a, b = 1, 4
E = EllipticCurve(GF(p), [a, b])
G = E(43190960452218023575787899214023014938926631792651638044680168600989609069200,
      20971936269255296908588589778128791635639992476076894152303569022736123671173)

# Public keys (x-coordinates only)
A_x = 87360200456784002948566700858113190957688355783112995047798140117594305287669
B_x = 6082896373499126624029343293750138460137531774473450341235217699497602895121

A = E.lift_x(A_x)
B = E.lift_x(B_x)
A = -A  # Note: source negates A for some reason

# Encrypted flag
iv = 'ceb34a8c174d77136455971f08641cc5'
ciphertext = 'b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453'

# Pohlig-Hellman on smooth order
order = E.order()
print("Order:", order)
print("Factorization:", factor(order))

# Recover Alice's private key
n_a = Pohlig_hellman_ECC(A, G)  # Uses BSGS + CRT internally

# Shared secret = n_a * B
shared_secret = (n_a * B).xy()[0]

# Decrypt flag
print(decrypt_flag(shared_secret, iv, ciphertext))
```

---

## Pohlig-Hellman Implementation (from `src/ecc.py`)

```python
def FindOrder(A: Point) -> int:
    # Uses SageMath's EllipticCurve.order()
    ...

def BSGS_ECC(A: Point, G: Point) -> int:
    n = FindOrder(G)
    m = ceil(sqrt(n))
    # Baby steps
    table = {j*G: j for j in range(m)}
    # Giant steps
    R = m * G
    curr = A
    for i in range(m):
        if curr in table:
            return (i*m + table[curr]) % n
        curr = curr - R

def SolveSubGroup(P, Q, p, e, n):
    # Solve DLP in subgroup of order p^e
    P_base = (n // p) * P
    gamma = (n // (p**e)) * P
    k_sub = 0
    for j in range(e):
        scaled = Q - k_sub * gamma
        H = (n // (p**(j+1))) * scaled
        z = BSGS_ECC(H, P_base)
        k_sub += z * (p**j)
    return k_sub

def Pohlig_hellman_ECC(Q: Point, P: Point) -> int:
    n = FindOrder(P)
    factors = factor(n)
    remainders, moduli = [], []
    for prime, exp in factors:
        modulus = prime**exp
        k_i = SolveSubGroup(P, Q, prime, exp, n)
        remainders.append(k_i)
        moduli.append(modulus)
    return CRT(remainders, moduli) % n
```

---

## Complexity

| Step | Complexity |
|------|------------|
| Curve order factoring | `O(√largest_factor)` — trivial for 262k |
| BSGS per subgroup | `O(√p^e)` — max `√262657 ≈ 512` |
| Total | Negligible (< 1 second) |

---

## References

- [Cryptohack - Microtransaction](https://cryptohack.org/challenges/microtransaction/)
- **Pohlig, S. & Hellman, M.** "An improved algorithm for computing logarithms over GF(p) and its cryptographic significance." *IEEE Trans. Inf. Theory* 24 (1978): 106–110.
- [ECDH Key Exchange](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
- [Smooth Group Order Attacks](https://crypto.stanford.edu/pbc/notes/ep/ph.html)