from sage.all import *
from math import isqrt, gcd
from src.cs_function import Floyd_cycle

def BSGS(g, h, field_modulus):
    F = GF(field_modulus)
    h = F(h)
    g = F(g)
    q = g.multiplicative_order()
    m = isqrt(q) + 1
    baby_step = {}
    curr = F(1)
    for i in range(m):
        baby_step[curr] = i
        curr *= g
    g_inv_m = g ** -m
    curr = h
    for i in range(m):
        if curr in baby_step:
            j = baby_step[curr]
            return (j + i * m) % q
        curr *= g_inv_m
    return None

def PohligHellmanPrime(g, h, order, p, e, field_modulus):
    g_base = g ** (order // p)
    x_p = 0
    h_current = h
    for i in range(e):
        h_base = h_current ** (order // (p ** (i + 1)))
        x_k = BSGS(g_base, h_base, field_modulus)
        if x_k is None:
            return None
        x_p += x_k * (p ** i)
        h_current *= g ** (-x_k * (p ** i))
    return x_p % (p ** e)

def Pohlig_hellman(g, h, p):
    F = GF(p)
    g = F(g)
    h = F(h)
    order = g.multiplicative_order()
    factors = factor(order)
    remainders = []
    moduli = []
    for prime, exp in factors:
        modulus = prime ** exp
        x_i = PohligHellmanPrime(g, h, order, prime, exp, p)
        if x_i is None:
            return None
        remainders.append(x_i)
        moduli.append(modulus)
    x = CRT(remainders, moduli)
    return x % order

def Pollard_rho(g, h, p, max_retries=5):
    F = GF(p)
    g = F(g)
    h = F(h)
    n = g.multiplicative_order()
    def f(state):
        x, k, l = state
        subnet = int(x) % 3
        if subnet == 0:
            return (x * h, k, (l + 1) % n)
        elif subnet == 1:
            return (x * x, (2 * k) % n, (2 * l) % n)
        else:
            return (x * g, (k + 1) % n, l)
    for _ in range(max_retries):
        a = randint(1, n-1)
        b = randint(1, n-1)
        x0 = (g**a * h**b, a, b)
        tortoise = f(x0)
        hare = f(f(x0))
        while tortoise[0] != hare[0]:
            tortoise = f(tortoise)
            hare = f(f(hare))
        x_t, k_t, l_t = tortoise
        x_h, k_h, l_h = hare
        delta_l = (l_h - l_t) % n
        delta_k = (k_t - k_h) % n
        if gcd(delta_l, n) == 1:
            return (delta_k * pow(delta_l, -1, n)) % n
    return None