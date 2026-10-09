from sage.all import *


def dotProduct(a, b):
    return a.dot_product(b)


def Calculate_Basis(a):
    return sqrt(a.dot_product(a))


def Gram_Schmidt(A: Matrix, normalize=False):
    A = Matrix(A)
    vector_base = []
    vector_base.append(A[0])
    for i in range(1, A.nrows()):
        current = A[i]
        for j in range(i-1, -1, -1):
            mu = (dotProduct(current, vector_base[j]) / dotProduct(vector_base[j], vector_base[j])) * vector_base[j]
            current -= mu
        if normalize:
            current = current / current.norm()
        vector_base.append(current)
    return vector_base