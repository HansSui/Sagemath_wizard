from math import sqrt

class Vector:
    def __init__(self, v):
        self.v = v
    def __str__(self):
        return str(self.v)
    def __add__(self,other):
        value =[]
        for i,j in zip(self.v, other.v):
            value.append(i+j)
        return Vector(value)
    def __sub__(self,other):
        value = []
        for i,j in zip(self.v,other.v):
            value.append(i-j)
        return Vector(value)
    def calculate_basis(self):
        value =0
        for i in self.v:
            value += i*i
        return sqrt(value)
    def dot_product(self,v2):
        value =0
        for i,j in zip(self.v,v2.v):
            value+= i*j
        return value

class Matrix:
    def __init__(self,m):
        if isinstance(m[0],Vector):
            self.m = m
        else:
            self.m = []
            for i in m:
                self.m.append(Vector(i))
    def __str__(self):
        return str([i.v for i in self.m])
    def __add__(self,other):
        value = []
        for i,j in zip(self.m, other.m):
            value.append(i+j)
        return Matrix(value)
    def __sub__(self,other):
        value = []
        for i,j in zip(self.m, other.m):
            value.append(i-j)
        return Matrix(value)
    def Transpose(self):
        value = []
        for i in range(len(self.m[0].v)):
            temp = []
            for j in range(len(self.m)):
                temp.append(self.m[j].v[i])
            value.append(Vector(temp))
        return Matrix(value)
    def __mul__(self,other):
        if isinstance(other,int):
            value = []
            for i in self.m:
                temp =[]
                for j in i.v:
                    temp.append(j * other)
                value.append(Vector(temp))
            return Matrix(value)

        m1 = len(self.m)
        n1 = len(self.m[0].v)
        m2 = len(other.m)
        if (n1 != m2):
            raise ValueError("Matrix can't be multiplied")
        H = other.Transpose()
        value = []
        for i in range(m1):
            temp = []
            for j in range(len(H.m)):
                temp.append(self.m[i].dot_product(H.m[j]))
            value.append(Vector(temp))
        return Matrix(value)
    def Lattice_Reduction(self,delta= 0.75):
        reduced = self.LLL(delta)
        self.m = reduced.m
        return self
    def Gaussian_elimination(self):
        m = len(self.m)
        n = len(self.m[0].v)

        pivot_row = 0
        for j in range(n):
            if pivot_row >= m:
                break

            # 1. Find pivot row with largest value in column j
            max_row = pivot_row
            for i in range(pivot_row + 1, m):
                if abs(self.m[i].v[j]) > abs(self.m[max_row].v[j]):
                    max_row = i

            # If column has only zeros, move to next column
            if abs(self.m[max_row].v[j]) < 1e-12:
                continue

            # 2. Swap current row with best pivot row
            self.m[pivot_row], self.m[max_row] = self.m[max_row], self.m[pivot_row]

            # 3. Eliminate entries below the pivot row
            for i in range(pivot_row + 1, m):
                if abs(self.m[i].v[j]) > 1e-12:
                    factor = self.m[i].v[j] / self.m[pivot_row].v[j]
                    self.m[i] = self.m[i] - (self.m[pivot_row] * factor)
                    self.m[i].v[j] = 0.0  # Clean floating-point artifacts

            pivot_row += 1
        return self
    def calculate_det(self):
        self.Gaussian_elimination()
        det =1
        for i in range(len(self.m)):
            for j in range(len(self.m[i].v)):
                if i==j:
                    det*= self.m[i].v[j]
        return det
    def Gram_Schmidt(self, normalize=False):
        """Computes orthogonal (or orthonormal) basis vectors.

        Formula: u_i = v_i - sum_{j < i} ( (v_i . u_j) / (u_j . u_j) ) * u_j
        """
        ortho_basis = []

        for v in self.m:
        # Start with a copy of current vector
            u = Vector(list(v.v))

        # Subtract projections onto all previously calculated basis vectors
            for u_prev in ortho_basis:
                denom = u_prev.dot_product(u_prev)
                if denom > 1e-12:  # Avoid division by zero
                    mu = v.dot_product(u_prev) / denom
                    u = u - (u_prev * mu)

        if normalize:
            norm = u.calculate_basis()
            if norm > 1e-12:
                u = u * (1.0 / norm)

        ortho_basis.append(u)

        return Matrix(ortho_basis)
    