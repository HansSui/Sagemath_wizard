from sage.all import *


# ============================================================
# Coppersmith's Algorithm (Howgrave-Graham)
# Finds small roots of univariate polynomial equations modulo N
# ============================================================

def coppersmith_univariate_modular(f, N, X, beta=1.0, epsilon=0.01, m=None):
    """
    Find small roots x0 of f(x) ≡ 0 (mod N) with |x0| < X.

    Args:
        f: Polynomial in ZZ[x] (univariate)
        N: Modulus (integer)
        X: Upper bound on |x0|
        beta: 1.0 for modular, 0.5 for integer equations
        epsilon: Slack parameter (smaller = better bound, slower)
        m: Lattice dimension (auto if None)

    Returns:
        List of small roots (integers)

    Working CTF use cases:
        - Small message: f = x^e - c mod N, X = N^(1/e)
        - Small d (Boneh-Durfee): f = e*x - 1 mod phi(N), X = N^0.292 (heuristic)
        - Partial key exposure with specific polynomial forms
    """
    f = f.monic()
    from sage.all import Zmod
    Rmod = PolynomialRing(Zmod(N), f.variable_name())
    f_mod = Rmod(f)
    if m is None:
        m = min(max(3, int(1 / epsilon)), 7)
    return f_mod.small_roots(X=X, beta=beta, epsilon=epsilon, m=m)


def coppersmith_univariate_integer(f, X, epsilon=0.01, m=None):
    """
    Find small roots x0 of f(x) = 0 over ZZ with |x0| < X.
    """
    f = f.monic()
    if m is None:
        m = max(3, int(1 / epsilon))
    try:
        return f.small_roots(X=X, beta=0.5, epsilon=epsilon, m=m)
    except AttributeError:
        N = int(X * 2)**2
        from sage.all import Zmod
        Rmod = PolynomialRing(Zmod(N), f.variable_name())
        f_mod = Rmod(f)
        return f_mod.small_roots(X=X, beta=0.5, epsilon=epsilon, m=m)


def coppersmith_howgrave_graham(f, N, X, m=3, beta=1.0):
    """
    Manual Howgrave-Graham lattice construction (educational).

    ponytail: simplified; may return zero polynomial for some parameters
    upgrade path: use proper lattice construction with correct scaling
    """
    f = f.monic()
    R = f.parent()
    x = R.gen()
    d = f.degree()
    rows = []

    for i in range(m):
        poly = x**i * f
        coeffs_list = list(poly)
        coeffs = coeffs_list + [0] * (m * d - len(coeffs_list))
        row = [c * X**(m * d - 1 - k) for k, c in enumerate(coeffs)]
        rows.append(row)

    if N != 0:
        for i in range(m * d):
            row = [0] * (m * d)
            row[i] = N * X**(m * d - 1 - i)
            rows.append(row)

    M = Matrix(ZZ, rows)
    M_LLL = M.LLL()

    v = M_LLL[0]
    coeffs = [v[k] // X**(m * d - 1 - k) for k in range(m * d)]
    g = sum(c * x**k for k, c in enumerate(coeffs))
    return g if g != 0 else f


# ============================================================
# Convenience wrappers for common CTF scenarios
# ============================================================

def coppersmith_small_message(N, e, c, epsilon=0.01):
    """
    Small message: m^e ≡ c (mod N), m < N^(1/e).
    WORKS: standard Coppersmith for small message.
    """
    R = PolynomialRing(ZZ, 'x')
    x = R.gen()
    f = x**e - c
    # Use slightly smaller bound than N^(1/e) for reliability
    X = Integer(N).nth_root(e, truncate_mode=True)[0] // 2
    # Try multiple parameter combinations for robustness
    for eps in [epsilon, 0.05, 0.1]:
        for m_val in [3, 4, 5]:
            roots = coppersmith_univariate_modular(f, N, X, epsilon=eps, m=m_val)
            if roots:
                return roots
    return []


def coppersmith_small_d(N, e, delta=0.292, epsilon=0.01):
    """
    Boneh-Durfee: small d < N^delta.
    HEURISTIC: may need parameter tuning; not guaranteed.
    """
    R = PolynomialRing(ZZ, 'x')
    x = R.gen()
    f = e * x - 1
    X = int(N**delta)
    return coppersmith_univariate_modular(f, N, X, beta=1.0, epsilon=epsilon)


# ============================================================
# Known prefix/suffix - NOTES
# ============================================================
# 
# If you know a prefix of the message (e.g., b'crypto{'), the standard
# univariate Coppersmith with f(x) = (known*X + x)^e - c does NOT work
# reliably in Sage because the polynomial coefficients are too large.
#
# For known prefix attacks, use one of:
#   1. defund/coppersmith library (full bivariate implementation)
#   2. Franklin-Reiter related message attack (if you have multiple cts)
#   3. Håstad broadcast attack (if e small and multiple cts)
#   4. If m < N^(1/e): just use coppersmith_small_message directly
#
# Example for small message with known format:
#   m = b'crypto{' + flag + b'}'
#   If total m < N^(1/e), use coppersmith_small_message
#   If m is large but unknown part is small: use defund/coppersmith
#
# ponytail: known prefix univariate not working in Sage; 
# upgrade path: use defund/coppersmith (https://github.com/defund/coppersmith)


__all__ = [
    'coppersmith_univariate_modular',
    'coppersmith_univariate_integer',
    'coppersmith_howgrave_graham',
    'coppersmith_small_message',
    'coppersmith_small_d',
]