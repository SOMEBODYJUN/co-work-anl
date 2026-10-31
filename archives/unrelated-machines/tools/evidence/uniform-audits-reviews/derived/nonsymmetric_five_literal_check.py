from fractions import Fraction as F

x = [F(1, 3)] * 3 + [F(1, 2)] * 2
Y = [[F(0) for _ in x] for _ in x]
for e, value in enumerate(x):
    Y[e][e] = value
for a in range(3):
    Y[3][a] = F(1, 3)
    Y[a][3] = Y[a][4] = F(1, 6)
R = [[1, 1, 0, 0, 0], [0, 0, 1, 0, 0],
     [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]

def mv(A, v):
    return [sum((a * b for a, b in zip(row, v)), F(0)) for row in A]

def cone(v, mass, parts):
    return (all(value >= 0 for value in v)
            and all(sum(v[e] for e in part) == mass for part in parts))

for e in range(5):
    column = [row[e] for row in Y]
    assert cone(column, x[e], [[0, 1, 2], [3, 4]])
    assert cone([a - b for a, b in zip(x, column)], 1 - x[e],
                [[0, 1, 2], [3, 4]])
    assert cone(mv(R, column), x[e], [[0, 1], [2, 3]])
xp = mv(R, x)
new_a0_column = mv(R, [row[0] + row[1] for row in Y])
assert xp[2] - new_a0_column[2] == F(-1, 6)
