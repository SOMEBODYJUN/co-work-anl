"""Exact arithmetic check of the finite-kernel optimization; no SPE solver imported."""
from fractions import Fraction as F
import json


def solve(matrix, rhs):
    n = len(rhs)
    a = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [x / d for x in a[j]]
        for i in range(n):
            if i != j:
                d = a[i][j]
                a[i] = [x - d*y for x, y in zip(a[i], a[j])]
    return [a[i][-1] for i in range(n)]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def check(T, P, g, b, gamma):
    n = len(T)
    assert all(sum(row) == 1 and min(row) >= 0 for row in T)
    assert max(g) <= gamma and min(b) >= 0
    M = [[F(i == j) - T[i][j]/2 for j in range(n)] for i in range(n)]
    v = solve(M, [(g[i]+b[i]-P[i]/2)/2 for i in range(n)])
    h = [P[i]/2+v[i] for i in range(n)]
    objectives = []
    for source in range(n):
        r = [F(i == source) for i in range(n)]
        Mt = [[M[j][i] for j in range(n)] for i in range(n)]
        p = solve(Mt, [x/2 for x in r])
        pT = [sum(p[i]*T[i][j] for i in range(n)) for j in range(n)]
        assert sum(p) == 1 and min(p) >= 0
        assert all(pT[i] <= 2*p[i] for i in range(n))
        assert [2*p[i]-pT[i] for i in range(n)] == r
        objective = (dot(pT, P)-dot(p, P))/2+gamma-dot(p, g)-dot(p, b)
        assert objective == gamma-h[source]
        objectives.append(objective)
    assert min(objectives) == gamma-max(h)
    return h, objectives


def main():
    T = [[F(0), F(1)], [F(1), F(0)]]
    P, g = [F(2), F(4)], [F(1), F(1,2)]
    h, objectives = check(T, P, g, [F(0), F(0)], F(1))
    assert h == [F(1,2), F(1)]
    assert objectives == [F(1,2), F(0)]
    J = [P[i]/2-g[i] for i in range(2)]
    assert J.index(max(J)) == 1 and g[1] < max(g)
    # Directly verify every actual action in this two-player complete SPE.
    sizes = [F(2), F(1)]
    follower = [1, 0]
    for first in range(2):
        values = [sizes[a]/(1+F(a == first)) for a in range(2)]
        assert values[follower[first]] == max(values)
    root_values = [sizes[a]/(1+F(follower[a] == a)) for a in range(2)]
    assert root_values == [F(2), F(1)]
    assert max(root_values) == root_values[0]
    K = [max(sizes[a]/(1+F(a == first)) for a in range(2)) for first in range(2)]
    assert P == [2*x for x in K]
    # The full-slot (A,B) load is one per client.
    assert g == [sizes[a]/2 for a in range(2)]

    T3 = [[F(1,2), F(1,3), F(1,6)],
          [F(0), F(1,4), F(3,4)],
          [F(2,5), F(0), F(3,5)]]
    checks = 0
    for shift in range(7):
        check(T3, [F(shift-2), F(3,2), F(-shift,3)],
              [F(1), F(2,3), F(1,5)], [F(0), F(shift,7), F(1,3)], F(1))
        checks += 3
    print(json.dumps({'status': 'exact checks passed', 'basis_restarts': checks+2,
        'real_two_player_kernel': True, 'strictly_weaker_than_full_price_J_condition': True,
        'six_player_bank_or_covariance_mapping_proved': False}, indent=2))


if __name__ == '__main__':
    main()
