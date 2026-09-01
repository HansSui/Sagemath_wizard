from sage.all import *
from NumTheory import GCD_binary, test_convergent
#RSA function
def RSA(totient,e,ct,N): #general function
    #totient
    d= pow(e,-1,totient)
    plaintext = pow(ct,d,N)
    return plaintext

def Small_e(N,e,ct):
    plaintext =Integer(ct).nth_root(e, truncate_mode = True)
    return plaintext

def Hastad_broadcast(List_N, e,List_ct):
    h = crt(List_ct, List_N)
    return Integer(h).nth_root(e,truncate_mode = True)

def wiener(e, n):
    coef = continued_fraction(e/n)
    conv = coef.convergents()
    for frac in conv:
        k = frac.numerator()
        d = frac.denominator()
        if k ==0:
            continue
        if test_convergent(k,d,e,n):
            return d
            
#factor
def Pollard_p(N: int, B:int):
    a =2 
    p =1
    for j in range(2,B):
        a = pow(a,j,N)
        d = GCD_binary(a-1,N)
        if 1 < d <N:
            p = d 
            break
    if p ==1: ValueError("Increase the bound")
    return p, N//p
def d_small(N:int,e:int,d:int):
    k = d * e - 1
    if k % 2 != 0:
        return None

    t = k
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1

    primes_base = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for g in primes_base:
        x = pow(g, t, N)
        if x == 1 or x == N - 1:
            continue

        for _ in range(s):
            y = pow(x, 2, N)
            if y == 1:
                p = GCD_binary(x - 1, N)
                if 1 < p < N:
                    q = N // p
                    return p, q
                break
            if y == N - 1:
                break
            x = y

    return None
