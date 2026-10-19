from sage.all import *
from sage.numerical.mip import MixedIntegerLinearProgram
A = matrix(ZZ, [
    [-5, -8,  0, -1, -1, -4],
    [-5, -6,  5, -7, -8, -6],
    [-2, -1,  8, -8, -2,  5],
    [-1,  6,  0, -8, -3,  5],
    [ 2,  0, -4, -2,  2, -5],
    [-6,  4, -5,  3,  3,  0],
    [34, -8, -9, 12, 12, -8],
    [30, -8, -1, 16, 39,  2],
    [ 9,  5, 29, -11, -9, -7],
    [-37, -3, -58, 12, -4, 32],
    [ 4, -30, -12, 6, 35, -10],
    [-30, 22, -56, 0, -42, 25]
])

b = vector(ZZ, [-18, -1, 83, 37, -8, -85, 156, 231, 142, -340, 96, -426])
p = MixedIntegerLinearProgram(maximization=False)
s = p.new_variable(integer=True, nonnegative=False)

for j in range(6):
    p.add_constraint(s[j] >= -10)
    p.add_constraint(s[j] <= 10)

for i in range(12):
    expr = sum(A[i, j] * s[j] for j in range(6)) - b[i]
    p.add_constraint(expr >= -1)
    p.add_constraint(expr <= 1)

p.solve()

s_val = [round(p.get_values(s[j])) for j in range(6)]
e_val = [b[i] - sum(A[i, j] * s_val[j] for j in range(6))
         for i in range(12)]

print("Vector s:", s_val)
print("Errors e_i:", e_val)