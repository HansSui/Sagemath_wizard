# Exceptional Curve (ECC) — Cryptohack

**Category:** Smart's Attack (Anomalous Curve)  
**Difficulty:** Hard

---

## Challenge Overview

The server uses an elliptic curve over a prime field `GF(p)` where the curve order equals the field characteristic:
```
#E(GF(p)) = p
```

Such curves are called **anomalous** (or *exceptional*). The discrete logarithm problem on anomalous curves can be solved in polynomial time using **Smart's attack** — lifting the curve to the p-adic numbers `Q_p` and exploiting the formal group isomorphism.

---

## Vulnerability

**Smart's Attack** (1999): For an anomalous curve `E/GF(p)` with `#E = p`:

1. Lift the curve `E` to a curve `Ẽ` over the p-adic integers `Z_p` (or `Q_p`)
2. Lift points `G, P` to `G̃, P̃` on `Ẽ`
3. The formal group logarithm gives an isomorphism `log: Ẽ₁(Q_p) → pZ_p` (kernel of reduction)
4. Compute `d = log(P̃) / log(G̃) mod p`

In practice (SageMath):
```python
E_adic = EllipticCurve(Qp(p), [a + p*α, b + p*β])  # arbitrary lift
G_adic = p * lift(G, E_adic, p)                    # multiply by p to land in kernel
P_adic = p * lift(P, E_adic, p)
d = (P_adic[0] / P_adic[1]) / (G_adic[0] / G_adic[1])  # formal group log ratio
```

---

## Attack Flow

1. **Identify anomalous curve**: `E.order() == p` (asserted in source)
2. **Get public parameters**: Generator `G`, Public Key `P = d*G`, Bob's public key `B`
3. **Lift to p-adics**: Use `Qp(p)` with arbitrary lift coefficients
4. **Multiply by `p`**: Maps points to kernel of reduction (formal group)
5. **Compute discrete log**: Ratio of formal group logarithms gives private key `d`
6. **Derive shared secret**: `S = d * B`
7. **Decrypt flag**: AES-CBC with SHA1-derived key

---

## Files

| File | Description |
|------|-------------|
| `source.py` | Challenge source with Smart's attack implementation |
| `output.txt` | Captured parameters: `p, a, b, G, P, B, iv, encrypted_flag` |

---

## Solution Script (`source.py` — key section)

```python
from sage.all import *

# Curve params from output.txt
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

E = EllipticCurve(GF(p), [a, b])
assert E.order() == p  # anomalous!

# Points from output.txt
G = E(3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005,
      4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850)

P = E(4748198372895404866752111766626421927481971519483471383813044005699388317650395315193922226704604937454742608233124831870493636003725200307683939875286865,
      2421873309002279841021791369884483308051497215798017509805302041102468310636822060707350789776065212606890489706597369526562336256272258544226688832663757)

B = E(0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38,
      0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf)

# Smart's attack: lift to Qp
E_adic = EllipticCurve(Qp(p), [a + p*13, b + p*37])  # arbitrary lift params

def lift(P, E_adic, p):
    Px, Py = map(ZZ, P.xy())
    for point in E_adic.lift_x(Px, all=True):
        _, y = map(ZZ, point.xy())
        if y % p == Py:
            return point

# Multiply by p to land in kernel of reduction (E₁)
G_adic = p * lift(G, E_adic, p)
P_adic = p * lift(P, E_adic, p)

# Formal group logarithm ratio = discrete log
Gx, Gy = G_adic.xy()
Px, Py = P_adic.xy()
d = int(GF(p)((Px / Py) / (Gx / Gy)))

# Derive shared secret and decrypt
shared_secret = (d * B).xy()[0]
# ... AES decryption with SHA1(shared_secret) ...
```

---

## Why It Works

| Step | Mathematical Justification |
|------|---------------------------|
| `#E = p` | Anomalous curve ⇒ formal group height 1 |
| Lift to `Q_p` | `E(Q_p)` has filtration `E₀ ⊃ E₁ ⊃ ...` where `E₁ ≅ pZ_p` |
| Multiply by `p` | `p·E(Q_p) ⊆ E₁` (kernel of reduction mod p) |
| `log(x) = x/y` | Formal group logarithm on `E₁` is `x/y` for `(x,y)` near identity |
| `d = log(P)/log(G)` | Isomorphism respects scalar multiplication |

---

## References

- [Cryptohack - Exceptional Curve](https://cryptohack.org/challenges/exceptional_curve/)
- **Smart, N. P.** "The discrete logarithm problem on elliptic curves of trace one." *J. Cryptology* 12 (1999): 193–196.
- [SageMath p-adic documentation](https://doc.sagemath.org/html/en/reference/padics/index.html)
- [Elliptic Curve Formal Groups](https://www.math.brown.edu/~jhs/Presentations/WyomingEllipticCurve.pdf)
- [Anomalous Curve Attacks](https://eprint.iacr.org/2003/197.pdf)