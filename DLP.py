
from sage.all import *
from math import isqrt

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

 