# High Bit Noise (Lattice) — Cryptohack

**Category:** Learning With Errors (LWE) — High Noise / MS Rounding  
**Difficulty:** Medium-Hard

---

## Challenge Overview

Another LWE instance, but with **high noise** where the message is encoded in the **most significant bits** (MSB) rather than LSB. Parameters:
- Dimension `n = 64`
- Plaintext modulus `p = 257`
- Ciphertext modulus `q = 0x10001 = 65537`
- Error bound `error_bound = ⌊(q/p)/2⌋ = 127`
- **Scaling factor** `Δ = ⌈q/p⌉ = 255`

The secret `S ∈ Z_qⁿ` is known (given). We are given:
- `A ∈ Z_qⁿ`
- `b = ⟨A, S⟩ + error + m·Δ (mod q)` where `error ∈ [-127, 127]`, `m ∈ Z_p`

Goal: Recover message `m`.

---

## Vulnerability

**Message in high bits** → rounding attack.

The ciphertext is:
```
b = ⟨A, S⟩ + error + m·Δ  (mod q)
```

Subtract the inner product:
```
x = (b - ⟨A, S⟩) mod q
```

Since `Δ ≈ q/p`, we have `m·Δ ≈ m·q/p`. The error `error ∈ [-127, 127]` is small compared to `Δ ≈ 255`.

Divide by `Δ` and round:
```
m ≈ round(x / Δ) mod p
```

This works because:
```
x = error + m·Δ  (mod q)
x/Δ = m + error/Δ  (mod q/Δ)
```
Since `|error/Δ| < 127/255 ≈ 0.5`, rounding recovers `m` exactly.

---

## Attack Flow

1. Compute inner product `⟨A, S⟩ mod q`
2. Compute `x = (b - ⟨A, S⟩) mod q`
3. Compute `Δ = round(q/p)`
4. Message `m = round(x / Δ) mod p`

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
delta = int(round(q / p))  # 255

S = [55542, 19411, 34770, 6739, 63198, 63821, 5900, 32164, 51223, 38979,
     24459, 10936, 17256, 20215, 35814, 42905, 53656, 17000, 1834, 51682,
     43780, 22391, 33012, 61667, 37447, 16404, 58991, 61772, 44888, 43199,
     32039, 26885, 17206, 62186, 58387, 57048, 38393, 29306, 58001, 57199,
     33472, 56572, 53429, 62593, 14134, 40522, 25106, 34325, 37646, 43688,
     14259, 24197, 33427, 43977, 18322, 38877, 55093, 12466, 16869, 25413,
     54773, 59532, 62694, 13948]

A = [13759, 12750, 38163, 63722, 39130, 22935, 58866, 48803, 15933, 64995,
     60517, 64302, 42432, 32000, 22058, 58123, 53993, 33790, 35783, 61333,
     53431, 43016, 60795, 25781, 28091, 11212, 64592, 11385, 24690, 40658,
     35307, 63583, 60365, 60359, 32568, 35417, 22078, 38207, 16331, 53636,
     28734, 30436, 18170, 15939, 966, 48519, 41621, 36371, 41836, 4026,
     33536, 57062, 52428, 59850, 476, 43354, 61614, 32243, 42518, 19733,
     63464, 29357, 56039, 15013]

b = 44007

# Inner product mod q
inner = sum(a*s for a,s in zip(A, S)) % q

# Difference
x = (b - inner) % q

# MS rounding
m = round(x / delta) % p
print(f"Message: {m}")
```

---

## Why This Works

| Parameter | Value | Role |
|-----------|-------|------|
| `q` | 65537 | Ciphertext modulus |
| `p` | 257 | Message space |
| `Δ = ⌈q/p⌉` | 255 | Scaling factor (≈ q/p) |
| `error_bound` | 127 | Noise magnitude |
| `Δ/2` | 127.5 | Rounding threshold |

Since `error_bound = ⌊Δ/2⌋`, the error is **strictly less than half the scaling factor**. Rounding `x/Δ` always gives the correct `m`.

This is the **"rounding" variant of LWE** (used in schemes like Round5, SABER). The message is in the MSB, noise in LSB.

---

## Comparison: Low Bit vs High Bit

| Aspect | Low Bit Noise | High Bit Noise |
|--------|---------------|----------------|
| Message encoding | LSB: `b = ⟨A,S⟩ + e·p + m` | MSB: `b = ⟨A,S⟩ + e + m·Δ` |
| Decryption | `m = (b - ⟨A,S⟩) mod p` | `m = round((b - ⟨A,S⟩)/Δ) mod p` |
| Noise growth | Additive in `Z_p` | Additive in `Z_q` |
| Correctness condition | `|e·p + m| < q/2` | `|e| < Δ/2` |

---

## References

- [Cryptohack - High Bit Noise](https://cryptohack.org/challenges/high_bit_noise/)
- **Regev, O.** "On lattices, learning with errors, random linear codes, and cryptography." *J. ACM* 56 (2009).
- **Banerjee, A. et al.** "Pseudorandom functions and lattices." *ECRYPT 2012* — Rounding LWE.
- [SABER / Round5 KEM](https://www.esat.kuleuven.be/cosic/pqcrypto/saber/) — MSB encoding
- [LWE Variants](https://eprint.iacr.org/2012/230.pdf)