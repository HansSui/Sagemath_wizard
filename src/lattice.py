from math import sqrt
from sage.all import *
def dotProduct(a:vector, b:vector) -> int:
    return sum(i*j for i, j in zip(a,b))
def Calculate_Basis(a:vector) -> float:
    return sqrt(sum(i*i for i in a))
def Gaussian_Elimination(a:Matrix)-> Matrix:
    a = Matrix(a)
    min = a[0][0]
    position = 0

    for i in range(0,a.nrows()):
        if min > a[i][0]:
            min = a[i][0]
            position = i

    swap_count = 0

    if position != 0:
        a[0], a[position] = a[position], a[0]
        swap_count += 1

    pivot = 0
    move = 1

    while (pivot < a.ncols() and move < a.nrows()):

        if a[pivot][pivot] == 0:
            found = False

            for j in range(move, a.nrows()):
                if a[j][pivot] != 0:
                    a[pivot], a[j] = a[j], a[pivot]
                    swap_count += 1
                    found = True
                    break

            if not found:
                pivot += 1
                continue

        for i in range(move, a.nrows()):
            if a[i][pivot] == 0:
                continue

            a[i] = a[i] - (a[i][pivot] / a[pivot][pivot]) * a[pivot]

        pivot += 1
        move += 1

    return a, swap_count

def determinant(a:Matrix)-> float:
    a,count = Gaussian_Elimination(a)
    value = 1
    for i in range(a.nrows()):
        for j in range(a.ncols()):
            if (i==j):
                value *= a[i][j]
    if count % 2 == 1:
        value = -value
    return value

def invert_matrix(a:Matrix) -> Matrix:
    h = determinant(a)

    if h == 0:
        raise ValueError("Matrix must be invertible")

    n = a.nrows()

    identity = matrix.identity(a.base_ring(), n)
    a = a.augment(identity)

    pivot = 0

    while pivot < n:

        if a[pivot][pivot] == 0:
            for j in range(pivot + 1, n):
                if a[j][pivot] != 0:
                    a[pivot], a[j] = a[j], a[pivot]
                    break

        a[pivot] = a[pivot] / a[pivot][pivot]

        for i in range(n):
            if i == pivot:
                continue

            if a[i][pivot] == 0:
                continue

            a[i] = a[i] - a[i][pivot] * a[pivot]

        pivot += 1

    return a[:, n:]

def Gram_Schmidt(A: Matrix, normalize=False):

    A = Matrix(A)
    vector_base = []

    vector_base.append(A[0])

    for i in range(1, A.nrows()):

        current = A[i]

        for j in range(i-1, -1, -1):

            muy = (dotProduct(current, vector_base[j]) /
                   dotProduct(vector_base[j], vector_base[j])) * vector_base[j]

            current -= muy

        if normalize:
            current = current / current.norm()

        vector_base.append(current)

    return vector_base

