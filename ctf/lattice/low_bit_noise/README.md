# Low Bit Noise (Lattice) — Cryptohack

**Category:** Learning With Errors (LWE) — Low Noise  
**Difficulty:** Medium

---

## Challenge Overview

This is an **LWE (Learning With Errors)** instance with small noise. Parameters:
- Dimension `n = 64`
- Plaintext modulus `p = 257`
- Ciphertext modulus `q = 0x10001 = 65537`
- Error bound `error_bound = ⌊(q/p)/2⌋ = ⌊65537/257 / 2⌋ = ⌊127.5⌋ = 127`

The secret `S ∈ Z_qⁿ` is known (given in source). We are given:
- `A ∈ Z_qⁿ` (public vector)
- `b = ⟨A, S⟩ + error * p + m (mod q)` where `error ∈ [-127, 127]` and `m ∈ Z_p`

Goal: Recover message `m`.

---

## Vulnerability

**Low noise** → error term is small relative to `q`. The message `m` is in the "low bits" of `b - ⟨A, S⟩`.

Since `b = ⟨A, S⟩ + error * p + m (mod q)`, we have:
```
b - ⟨A, S⟩ = error * p + m  (mod q)
```

Because `error ∈ [-127, 127]` and `m ∈ [0, 256]`, the value `error * p + m` is in `[-127*257, 127*257 + 256] ≈ [-32639, 32895]`.

Since `q = 65537`, this value is **centered around 0** (or `q`). Taking mod `q` and centering:
```
x = (b - ⟨A, S⟩) mod q
if x > q/2: x -= q
```
Then `x ≈ error * p + m`. Since `p = 257`, `x / p ≈ error + m/p`. The message `m` is the **remainder mod p**:
```
m = x mod p
```

Wait — but the source code shows:
```python
x = (b - time2Matrix(A,S)%q)%q
if x > q//2:
    x -= q
print(x%p)
```

This directly computes `x` (centered) and outputs `x % p`. Since `x = error * p + m`, we have `x % p = m`!

So the "challenge" is trivial if you have the secret `S` — you just compute the inner product and reduce mod `p`.

But in a real LWE scenario, `S` is secret. The challenge might be about **recovering `S` from multiple samples** or this is just a demonstration of the decryption step.

Looking at the source: `S` is hardcoded and given. So this is just the **decryption function** for an LWE encryption scheme.

---

## Attack Flow

1. Compute inner product `⟨A, S⟩ mod q`
2. Compute `x = (b - ⟨A, S⟩) mod q`, centered to `[-q/2, q/2]`
3. Message `m = x mod p`

---

## Files

| File | Description |
|------|-------------|
| `source.py` | LWE parameters, secret `S`, public `A`, ciphertext `b`, decryption |

---

## Solution

```python
from sage.all import *

n = 64
p = 257
q = 0x10001

S = (10082, 48747, 17960, 55638, 37012, 51876, 10128, 37750, 7608, 58952,
     33296, 25463, 38900, 85, 65248, 42153, 44966, 31594, 40676, 56828,
     30325, 38502, 65083, 7497, 2667, 54022, 24029, 32162, 57267, 12253,
     6668, 5181, 14906, 51655, 61347, 4722, 22227, 23606, 63183, 52860,
     1670, 31085, 42633, 47197, 7255, 16150, 9574, 62956, 26742, 57998,
     49467, 31224, 60073, 12730, 41419, 41042, 53032, 16339, 32913, 16351,
     34283, 47845, 3617, 35718)

A = (53751, 21252, 55954, 16345, 60990, 2822, 56279, 37048, 36153, 52141,
     2121, 56565, 48112, 43755, 12951, 22539, 29478, 28421, 62175, 10265,
     36378, 21305, 42402, 26359, 939, 60690, 1161, 65097, 34505, 19777,
     29652, 42868, 49148, 38296, 31916, 25606, 18700, 12655, 35631, 64674,
     29018, 21021, 14865, 40196, 14036, 40278, 37209, 35585, 34344, 33030,
     285, 58536, 56121, 40899, 24262, 62326, 57433, 5765, 24456, 28859,
     45170, 14799, 21567, 55484)

b = 11507

# Inner product mod q
inner = sum(a*s for a,s in zip(A, S)) % q

# Centered difference
x = (b - inner) % q
if x > q//2:
    x -= q

# Message
m = x % p
print(f"Message: {m}")  # Should be an integer in [0, 256]
```

---

## Connection to LWE

This is the **decryption** step of Regev's LWE encryption:
- Secret key: `S ∈ Z_qⁿ`
- Public key: `(A, b = A·S + e·p + m)` where `A ← Z_qⁿ`, `e ← χ` (small error)
- Decrypt: `m = (b - ⟨A, S⟩ mod q) mod p`

The error distribution `χ` is uniform in `[-B, B]` where `B = ⌊q/(2p)⌋`. This ensures correct decryption with high probability because `|e·p + m| < q/2`.

---

## References

- [Cryptohack - Low Bit Noise](https://cryptohack.org/challenges/low_bit_noise/)
- **Regev, O.** "On lattices, learning with errors, random linear codes, and cryptography." *J. ACM* 56 (2009): 1–40.
- [LWE Decryption](https://en.wikipedia.org/wiki/Learning_with_errors)
- [LWE Parameter Selection](https://eprint.iacr.org/2016/817.pdf)