# 🧙‍♂️ SageMath Wizard

**SageMath Wizard** is an algebraic cryptanalysis and computational number theory library for Python and SageMath. It provides standalone primitives, optimized arithmetic structures, and automated attacks against classical public-key schemes and lattice-based problems.

---

## 📦 Library Architecture

The library is structured into six foundational modules under `src/`:

| Module | Description |
|--------|-------------|
| **`num_theory.py`** | Core modular arithmetic, Extended Euclidean algorithm, Chinese Remainder Theorem (CRT), fast exponentiation, Legendre/Jacobi symbols, Miller-Rabin primality testing |
| **`dlp.py`** | Discrete logarithm solvers: Baby-Step Giant-Step (BSGS), Pollard's ρ cycle finding (Floyd/Brent), Pohlig-Hellman subgroup decomposition |
| **`ecc.py`** | Elliptic curve arithmetic: Short Weierstrass (`y² = x³ + ax + b`) and Montgomery curves, projective/affine point arithmetic, order calculation, constant-time scalar multiplication via Montgomery Ladder, ECDLP solvers (BSGS, Pohlig-Hellman, Pollard's ρ) |
| **`rsa.py`** | RSA key generation, Wiener's continued fractions attack (small `d < ⅓N^0.25`), Hastad's Broadcast attack via CRT, Franklin-Reiter Related Message attack via polynomial GCD, Pollard's p-1 factoring |
| **`lattice.py`** | Gram-Schmidt Orthogonalization (GSO), LLL reduction wrapper, Babai's Nearest Plane / Rounding for CVP, Kannan's embedding, low-density knapsack/subset-sum solvers |
| **`cs_function.py`** | Cryptographic utilities: PKCS#7 padding verification, AES-CBC decryption with SHA1 key derivation, Floyd cycle detection |

---

## 📁 Project Structure

```
sagemath_wizard/
├── src/                          # Core library
│   ├── __init__.py               # Package exports
│   ├── num_theory.py             # Algebraic & arithmetic primitives
│   ├── dlp.py                    # Discrete logarithm solvers
│   ├── ecc.py                    # Elliptic curve arithmetic & ECDLP
│   ├── rsa.py                    # RSA attacks & factoring
│   ├── lattice.py                # Lattice reduction & geometry of numbers
│   └── cs_function.py            # Crypto utilities & serialization
├── ctf/                          # Cryptohack CTF challenges (documented, not solved)
│   ├── ecc/
│   │   ├── curveball/            # ECC invalid curve / generator manipulation
│   │   ├── prosign3/             # ECDSA nonce reuse / time-based signing
│   │   ├── exceptional_curve/    # Smart's attack (anomalous curve, E.order() == p)
│   │   └── microtransaction/     # ECDH + Pohlig-Hellman (smooth order)
│   ├── rsa/
│   │   └── broken_rsa/           # Small exponent e=16, Coppersmith/unpad attack
│   └── lattice/
│       ├── backpack/             # Merkle-Hellman knapsack (LLL)
│       ├── low_bit_noise/        # LWE with low-bit noise
│       ├── high_bit_noise/       # LWE with high-bit noise (MS rounding)
│       └── find_the_lattice/     # NTRU-like encryption (LLL on [1,h;0,q])
└── README.md                     # This file
```

---

## ⚙️ Installation & Setup

Ensure you have [Conda](https://docs.conda.io/en/latest/) installed, then create an environment with SageMath and Python 3.11:

```bash
# Clone the repository
git clone https://github.com/HansSui/Sagemath_wizard.git
cd sagemath_wizard

# Create and activate Conda environment
conda create -n sagemath-wizard -c conda-forge sage python=3.11 pycryptodome pytest -y
conda activate sagemath-wizard
```

> **Note:** SageMath must be installed via conda-forge for proper `sage.all` imports. Pure Python fallback is not supported for core algorithms.

---

## 🚀 Quick Start

```python
from src import *

# Number theory
d, x, y = extended_euclid(240, 46)      # d=2, x=-9, y=47
inv = inv_mod(3, 11)                     # 4
crt_result = CRT([2, 3], [3, 5])         # 23

# Discrete log (DLP)
BSGS(g, h, p)                            # Baby-Step Giant-Step
Pohlig_hellman(g, h, p)                  # Smooth order
Pollard_rho(g, h, p)                     # Generic, O(√n) memory

# Elliptic curves
curve = ECC(a=1, b=4, p=99061670249353652702595159229088680425828208953931838069069584252923270946291)
G = Point(curve, x, y)
order = FindOrder(G)
secret = Pohlig_hellman_ECC(Q, G)        # ECDLP via Pohlig-Hellman

# RSA attacks
d = wiener(e, n)                         # Small private exponent
m = Hastad_broadcast([n1, n2, n3], 3, [c1, c2, c3])  # Broadcast attack

# Lattice reduction
basis = Gram_Schmidt(matrix)
LLL_reduced = basis.LLL()                # SageMath built-in
```

---

## 📚 CTF Challenges (`ctf/`)

Each challenge in `ctf/` contains:
- **`source.py`** — Challenge source code (server-side logic)
- **`output.txt`** — Captured public parameters / ciphertexts
- **`solve.py`** — Solution script (where available)
- **`flow.md`** — Writeup / attack flow explanation

> **These are documented for educational purposes only. Solutions are not executed here.**

### ECC Challenges
| Challenge | Category | Technique |
|-----------|----------|-----------|
| `curveball` | Invalid curve attack | Generator manipulation, `Q = d·G` forgery |
| `prosign3` | ECDSA nonce reuse | Time-based signing, signature malleability |
| `exceptional_curve` | Smart's attack | Anomalous curve (`E.order() == p`), p-adic lift |
| `microtransaction` | ECDH + Pohlig-Hellman | Smooth curve order, small private key (64-bit) |

### RSA Challenges
| Challenge | Category | Technique |
|-----------|----------|-----------|
| `broken_rsa` | Small exponent | `e=16`, Coppersmith / Franklin-Reiter |

### Lattice Challenges
| Challenge | Category | Technique |
|-----------|----------|-----------|
| `backpack` | Merkle-Hellman knapsack | LLL on public key basis |
| `low_bit_noise` | LWE (low noise) | Babai's CVP / LLL |
| `high_bit_noise` | LWE (high noise) | MS rounding / lattice embedding |
| `find_the_lattice` | NTRU-like | LLL on `[[1, h], [0, q]]` |

---

## 🧪 Testing

Run the test suite (if available):

```bash
pytest -v
```

---

## 📖 References

- **SageMath Documentation** — https://doc.sagemath.org/
- **Cryptohack** — https://cryptohack.org/
- **Handbook of Applied Cryptography** — Menezes, van Oorschot, Vanstone
- **An Introduction to Mathematical Cryptography** — Hoffstein, Pipher, Silverman

---

## ⚠️ Disclaimer

This library is for **educational and research purposes only**. The CTF challenges are reproduced from Cryptohack for learning. Do not use against production systems without authorization.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.