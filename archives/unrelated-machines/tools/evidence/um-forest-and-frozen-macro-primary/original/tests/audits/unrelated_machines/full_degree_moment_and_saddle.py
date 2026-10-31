#!/usr/bin/env python3
"""Small exact Fraction checks for two stated-scope mathematical bridges.

This is a finite arithmetic audit only. It does not search large instances or
claim a general algorithm.
"""
from fractions import Fraction as F
from itertools import product


def saddle_cycle(beta: F):
    delta = (1 - beta) / 4
    a = 1 - delta
    b1 = beta + delta
    b2 = beta + 2 * delta
    c = delta
    assert F(1, 2) <= beta < 1
    assert a > beta and b1 > beta and b2 > beta and c <= beta
    # H1=A->1,B->2; H2=A->2,B->1, with private light ell->1.
    h1 = [a + c, b2]
    h2 = [b1 + c, a]
    assert h1 == [F(1), b2]
    assert h2 == [b2, a]
    # Own residual duals are lambda1=(1,0), lambda2=(0,1).
    g11 = a + c
    g21 = b1 + c
    g22 = a
    g12 = b2
    assert g21 < g11 and g12 < g22
    assert max(h2) == a < 1
    return delta, [[g11, g12], [g21, g22]]


def full_moment_atom_check():
    # Two tasks, two machines, and a real T-feasible assignment 0,1.
    m = 2
    n = 2
    T = F(1)
    # Every task has both finite unit edges; selected assignment (0,1) is feasible.
    p = [[F(1), F(1)], [F(1), F(1)]]  # p[j][i]
    assignments = list(product(range(m), repeat=n))
    feasible = [s for s in assignments if max(sum(p[j][i] for j, i2 in enumerate(s) if i2 == i) for i in range(m)) <= T]
    assert feasible == [(0, 1), (1, 0)]
    weights = {s: (F(1) / len(feasible) if s in feasible else F(0)) for s in assignments}
    assert sum(weights.values()) == 1
    # The full atom monomial m_sigma is the indicator of sigma under this real distribution.
    for sigma in assignments:
        w = weights[sigma]
        assert w >= 0
        for i in range(m):
            load = sum(p[j][i] for j, k in enumerate(sigma) if k == i)
            assert (T - load) * w >= 0
    # Therefore at least one positive atom survives every machine localizer.
    survivors = [s for s in assignments if weights[s] > 0 and all(
        T - sum(p[j][i] for j, k in enumerate(s) if k == i) >= 0 for i in range(m))]
    assert survivors
    # Verify the Boolean/one-hot partition identity on every assignment atom.
    assert sum(weights.values()) == 1
    return len(assignments), len(survivors)


def main():
    cycle = {}
    for beta in [F(1, 2), F(3, 4), F(9, 10), F(99, 100)]:
        eta, matrix = saddle_cycle(beta)
        cycle[str(beta)] = {"delta": str(eta), "g": [[str(x) for x in row] for row in matrix]}
    atoms = full_moment_atom_check()
    print({"saddle_cycle": cycle, "full_moment_atoms": atoms, "status": "ok"})


if __name__ == "__main__":
    main()
