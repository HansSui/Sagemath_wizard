#GCD 2 types
from sage.all import *
from math import isqrt
def GCD(a, b):
    while b:
        a,b = b,a%b
    return a

def isPrime(h):
    if h%2 ==0: return 0
    if h < 2: return 0
    for i in range(3,isqrt(h),2):
        if h% i ==0: return 0
    return 1
def GCD_binary(a,b):
    g =1
    while a%2 ==0 & b%2 ==0:
        a//=2
        b//=2
        g*=2
    while a!= 0:
        while a%2 ==0: a//=2
        while b%2 ==0: b//=2
        if a>= b: a = (a-b)//2
        else: b = (b-a)//2
    return g*b
def extended_euclid(a,b):
    s, old_s,t,old_t,r, old_r = 0,1,1,0,b,a
    while r != 0:
        q = round(old_r/r)
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    d,x,y = old_r, t,s
    return d,x,y
def inv_mod(a,m):
    d,x,y = extended_euclid(a,m)
    if d!= 1:
        return None
    else:
        return x%m
def CRT(a,b):
    #a = [divisors], b = [remainders]
    M = 1
    for i in b:
        M*=i
    x=0 
    Mi = []
    for i in b:
        Mi.append(M//i)
    yi = []
    for i in Mi:
        yi.append(inv_mod(i,M//i))
    for i in range(len(a)):
        x+= pow(a[i]*Mi[i]*yi[i],1,M)
    return x%M

#legendre sympol

def legendre_reverse(p,q):
    value = 1
    if p%3 == 4 and q%3 ==4:
        value= -1
    return value, q, p   #reverse

def legendre_2(q):
    return (-1)* (2**((q*q-1)//8)) #when p =2

def legendre_factor(p):
    if p.is_prime() == 0:
        factors= factor(p)
        return factors
    return None

def legendre_sympol(a,p):
    res = pow(a, (p-1)//2, p)
    return res - p if res > 1 else res

def randN_for_Shanks(p):
    F= GF(p)
    while True:
        n = randint(2, p-1)
        h = legendre_sympol(n,p)
        if h ==-1 :
            return F(n)

def Tonelli_Shank(a,p):
    if legendre_sympol(a,p) != 1: return None
    if p%3 ==4: return pow(a, (p+1)//4, p)
    n = randN_for_Shanks(p)
    M,e = p-1, 0
    while M % 2 ==0: 
        e+=1
        M/=2
    q= M
    y = pow(n,q,p)
    r = e
    x = pow(a, (q+1)//2, p)
    b = pow(a,q,p)
    while b%p != 1:
        m=1
        while pow(b,2**m, p) != 1:
            m+=1
        h = 2**(r-m-1)
        g = pow(y,h,p)
        y = pow(g,2, p)
        r =m
        x = pow(x*g,1,p)
        b = pow(b*y,1,p)
    return x

def Jacobi_Sympol(a,b):
    if n <= 0 or b%2 ==0: return 0
    j =1
    if a <0:
        a = -a 
        if b%4 ==3: j = -j
    while a != 0:
        while a%2 ==0:
            a/=2
            if b%8 ==3 or b%8 == 5: j =-j
            a,b = b,a
            if a%4 ==3 and b%4 ==3: j=-j
            a = a%b
        if b ==1: return j
        return 0
    
