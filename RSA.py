from sage.all import *
#RSA function
def RSA(factors,e,ct,N): #general function
    totient =1
    
    for i,j in factors:
        temp = i**(j-1)*i -1
        value+= temp
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
    # Convert e/n into a continued fraction
    cf = continued_fraction(e/n)
    convergents = cf.convergents()
    for kd in convergents:
        k = kd.numerator()
        d = kd.denominator()
        # Check if k and d meet the requirements
        if k == 0 or d%2 == 0 or e*d % k != 1:
            continue
        phi = (e*d - 1)/k
        # Create the polynomial
        x = PolynomialRing(RationalField(), 'x').gen()
        f = x^2 - (n-phi+1)*x + n
        roots = f.roots()
        # Check if polynomial as two roots
        if len(roots) != 2:
            continue
        # Check if roots of the polynomial are p and q
        p,q = int(roots[0][0]), int(roots[1][0])
        if p*q == n:
            return d
    return None