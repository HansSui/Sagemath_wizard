"""
SageMath Wizard - Algebraic Cryptanalysis & Computational Number Theory Library

Core modules:
- num_theory: Modular arithmetic, CRT, primality testing, Legendre/Jacobi symbols
- dlp: Discrete logarithm solvers (BSGS, Pollard's ρ, Pohlig-Hellman)
- ecc: Elliptic curve arithmetic (Weierstrass, Montgomery), ECDLP solvers
- rsa: RSA attacks (Wiener, Hastad, Franklin-Reiter, factoring)
- lattice: LLL reduction, CVP (Babai), knapsack/subset-sum solvers
- cs_function: Crypto utilities (AES, padding, cycle detection)
"""

from .num_theory import (
    GCD, GCD_binary, extended_euclid, inv_mod, CRT,
    legendre_sympol, Tonelli_Shank, Jacobi_Sympol,
    isPrime, Miller_Rabin_Test, test_convergent
)
from .dlp import BSGS, Pohlig_hellman, Pollard_rho
from .ecc import (
    ECC, Point, MontgomeryECC, MontgomeryPoint,
    FindOrder, BSGS_ECC, Pohlig_hellman_ECC, Pollard_Rho_ECC,
    decrypt_flag
)
from .rsa import RSA, Small_e, Hastad_broadcast, wiener, Pollard_p, d_small
from .lattice import dotProduct, Calculate_Basis, Gram_Schmidt
from .coppersmith import (
    coppersmith_univariate_modular,
    coppersmith_univariate_integer,
    coppersmith_howgrave_graham,
    coppersmith_small_message,
    coppersmith_small_d,
)
from .cs_function import is_pkcs7_padded, decrypt_flag as cs_decrypt_flag, Floyd_cycle

__all__ = [
    # num_theory
    'GCD', 'GCD_binary', 'extended_euclid', 'inv_mod', 'CRT',
    'legendre_sympol', 'Tonelli_Shank', 'Jacobi_Sympol',
    'isPrime', 'Miller_Rabin_Test', 'test_convergent',
    # dlp
    'BSGS', 'Pohlig_hellman', 'Pollard_rho',
    # ecc
    'ECC', 'Point', 'MontgomeryECC', 'MontgomeryPoint',
    'FindOrder', 'BSGS_ECC', 'Pohlig_hellman_ECC', 'Pollard_Rho_ECC',
    'decrypt_flag',
    # rsa
    'RSA', 'Small_e', 'Hastad_broadcast', 'wiener', 'Pollard_p', 'd_small',
    # lattice
    'dotProduct', 'Calculate_Basis', 'Gram_Schmidt',
# coppersmith
    'coppersmith_univariate_modular', 'coppersmith_univariate_integer',
    'coppersmith_howgrave_graham',
    'coppersmith_small_message', 'coppersmith_small_d',
    # cs_function
    'is_pkcs7_padded', 'cs_decrypt_flag', 'Floyd_cycle',
]

__version__ = '0.1.0'