"""Definition-level exact audit of one proposed universal static equivalence."""
from fractions import Fraction as F
from itertools import combinations

labels = "ABC"
types = [("A", 6), ("AB", 6), ("BC", 8), ("C", 6)]
customers = [set(t) for t, n in types for _ in range(n)]
f = [sum(F(1) for x in customers if a in x) for a in labels]
H = [[sum((F(1, 2) for x in customers if a in x and b in x), F())
      for b in labels] for a in labels]
K = [[f[i] - H[i][j] for j in range(3)] for i in range(3)]
p = [F(4, 14), F(3, 14), F(7, 14)]
q = [F(), F(5, 6), F(1, 6)]
lam = [F(1, 2), F(), F(1, 2)]

def mv(A, x):
    return [sum((a * b for a, b in zip(row, x)), F()) for row in A]

def det(A):
    if len(A) == 1:
        return A[0][0]
    return sum(((-1)**j * A[0][j] * det([r[:j]+r[j+1:] for r in A[1:]])
                for j in range(len(A))), F())

assert len(customers) == 26
assert f == [12, 14, 14]
assert H == [[6, 3, 0], [3, 7, 4], [0, 4, 7]]
assert K == [[6, 9, 12], [11, 7, 10], [14, 10, 7]]
assert [det([row[:i] for row in H[:i]]) for i in range(1, 4)] == [6, 33, 135]
assert mv(K, p) == [F(135, 14)] * 3
assert mv(K, q) == [F(19, 2), F(15, 2), F(19, 2)]
assert mv(list(map(list, zip(*K))), lam) == [F(10), F(19, 2), F(19, 2)]
assert F(135, 14) - F(19, 2) == F(1, 7)
print("Exact audit passed: J self-response 135/14; true minimax 19/2; gap 1/7.")
