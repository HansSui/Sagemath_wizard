# 🧙‍♂️ SageMath Wizard

**SageMath Wizard** is an algebraic cryptanalysis and computational number theory library for Python and SageMath. It provides standalone primitives, optimized arithmetic structures, and automated attacks against classical public-key schemes and lattice-based problems.

---

## 📦 Library Architecture

The library is structured into six foundational modules:

* **`NumTheory.py` (Algebraic & Arithmetic Primitives):** Core modular arithmetic, Extended Euclidean algorithm, Chinese Remainder Theorem (CRT), fast exponentiation, Legendre/Jacobi symbols, and Miller-Rabin primality testing.
* **`DLP.py` (Discrete Logarithm Solvers):** Generic and specialized DLP/ECDLP engines including Baby-Step Giant-Step (BSGS), Pollard's $\rho$ cycle finding with Floyd/Brent partition, and Pohlig-Hellman subgroup decomposition.
* **`ECC.py` (Elliptic Curve Arithmetic):** Short Weierstrass curve implementations ($y^2 = x^3 + ax + b$), projective/affine point arithmetic, order calculation, and constant-time scalar multiplication via **Montgomery Ladder**.
* **`RSA.py` (Factoring & Algebraic Attacks):** RSA key generation, Wiener's continued fractions attack for small private exponents ($d < \frac{1}{3}N^{0.25}$), Hastad's Broadcast attack via CRT, and Franklin-Reiter Related Message attack via polynomial GCD.
* **`lattice.py` (Lattice Reduction & Geometry of Numbers):** Gram-Schmidt Orthogonalization (GSO), **Lenstra–Lenstra–Lovász (LLL)** reduction wrapper, Babai's Nearest Plane / Rounding algorithm for Closest Vector Problem (CVP), Kannan's embedding technique, and low-density Knapsack/Subset-Sum solvers.
* **`CS_function.py` (Utility & Serialization Helpers):** Cryptographic utility pipelines, bitwise manipulation, byte-to-integer conversions, and padding verifications.

---

## ⚙️ Installation & Setup

Ensure you have [Conda](https://docs.conda.io/en/latest/) installed, then create an environment with SageMath and Python 3.11:

```bash
# Clone the repository
git clone [https://github.com/HansSui/sagemath_wizard.git](https://github.com/HansSui/sagemath_wizard.git)
cd sagemath_wizard

# Create and activate Conda environment
conda create -n sagemath-wizard -c conda-forge sage python=3.11 pycryptodome pytest -y
conda activate sagemath-wizard
