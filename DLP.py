
from sage.all import *
from math import isqrt
from CS_function import Floyd_cycle
def BSGS(g, h, p):
    F = GF(p)
    h= F(h)
    g = F(g)
    q = g.multiplicative_order()
    m = isqrt(q)+1
    Baby_Step = {}
    curr = F(1)
    for i in range(1,m):
        Baby_Step[curr] = i
        curr*= g
    g_inv_mod = g**-m
    Giant_step = h
    for i in range(1,m):
        for Giant_step in Baby_Step:
            j= Baby_Step[Giant_step]
            return (j*m + i)%p
        Giant_step*=g_inv_mod
    return None

def PohligHellmanPrime(g,h,N,p,e):
    g_base = g^(N/p)
    x_p = 0
    h_current = h
    for i in range(0,e-1):
        h_base = (h_current)^(N/(p^(i+1)))
        x_k = BSGS(g_base, h_base, p)
        x_p = x_p + x_k* (p^i)
        h_current = h_current* g^(-x_k* (p^i))
    return x_p%(p^e)

def Pohlig_hellman(g,h,p):
    F = GF(p)
    g = F(g)
    h = F(h)
    SubFactor= g.multiplicative_order()
    N = factor(SubFactor)
    Remainder =[]
    Moduli = []
    for i, j in N:
        q_i = i^j
        x_i = PohligHellmanPrime(g,h,N,i,j)
        Remainder.append(x_i)
        Moduli.append(q_i)
    x= CRT(Remainder, Moduli)
    return x%SubFactor
def Pollard_rho(g,h,p):
    n = multiplicative_order(g)
    x,k,l = 1,0,0
    x_p, k_p, l_p = x,k,l
    def f(state):
        x,k,l = state
        subnet = x%3
        if subnet == 0:
            return ((x*h)% p, k , (l+1)%n)
        elif subnet ==1:
            return ((x*x)%p, (2*k)%n, (2*l)%n)
        else:
            return ((x*g)%p,(k+1)%n,l)
    x0 = (1,0,0)
    (x, k, l), (x_prime, k_prime, l_prime) = Floyd_cycle(f, x0)
    delta_l = (l_prime - l) % n
    delta_k = (k - k_prime) % n
    if math.gcd(delta_l, n) == 1:
        return (delta_k * pow(delta_l, -1, n)) % n
    else:
        return None
        