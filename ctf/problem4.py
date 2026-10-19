from sage.all import *
from sage.numerical.mip import MixedIntegerLinearProgram

R, C = 7, 15

rows = [[2], [1,1], [1,1,1], [1,12],
        [1,1,1,3], [1,1,1,1], [2]]

cols = [[2,2], [1,1,1], [1,1,1,1], [1,1,1], [3],
        [1], [1], [1], [1], [1], [1], [1,1], [2], [3], [2]]

# Generate all patterns matching a clue
def patterns(n, clue):
    result = []

    def gen(k, pos, line):
        if k == len(clue):
            result.append(line + [0] * (n - len(line)))
            return

        size = clue[k]
        remaining = sum(clue[k+1:]) + len(clue) - k - 1

        for start in range(pos, n - size - remaining + 1):
            new_line = line + [0] * (start - len(line)) + [1] * size
            gen(k + 1, start + size + 1, new_line)

    gen(0, 0, [])
    return result


p = MixedIntegerLinearProgram()
x = p.new_variable(binary=True)

# Row patterns
for i in range(R):
    opts = patterns(C, rows[i])
    y = p.new_variable(binary=True)

    p.add_constraint(sum(y[k] for k in range(len(opts))) == 1)

    for j in range(C):
        p.add_constraint(
            x[i,j] == sum(y[k] * opts[k][j] for k in range(len(opts)))
        )

# Column patterns
for j in range(C):
    opts = patterns(R, cols[j])
    y = p.new_variable(binary=True)

    p.add_constraint(sum(y[k] for k in range(len(opts))) == 1)

    for i in range(R):
        p.add_constraint(
            x[i,j] == sum(y[k] * opts[k][i] for k in range(len(opts)))
        )

# Solve and print
p.solve()

for i in range(R):
    print("".join("█" if p.get_values(x[i,j]) > 0.5 else "." for j in range(C)))
    