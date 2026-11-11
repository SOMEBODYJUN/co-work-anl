"""Exact new face/uniqueness and genuine query calculations; no optimizer."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / 'archives/customer-attraction/tools/evidence/global-security-budgets/original/evidence/certificates/customer_attraction'


def payoff(clients, a, rivals):
    return sum((F(1, 1 + sum(b in interests for b in rivals))
                for interests in clients if a in interests), F(0))


def queries(clients, actions, players):
    def terminal(h):
        while len(h) < players:
            h += (actions[h],)
        return h
    z = terminal(())
    matrices = []
    for i in range(players):
        rivals = []
        for b in range(6):
            dev = terminal(z[:i] + (b,))
            rivals.append(dev[:i] + dev[i + 1:])
        matrices.append([[payoff(clients, a, B) for B in rivals] for a in range(6)])
    return z, matrices


def quadratic(M, p):
    return sum((p[a] * p[b] * M[a][b] for a, b in product(range(6), repeat=2)), F(0))


def det(matrix):
    A = [[F(v) for v in row] for row in matrix]
    ans = F(1)
    for j in range(len(A)):
        k = next(k for k in range(j, len(A)) if A[k][j])
        if k != j:
            A[k], A[j] = A[j], A[k]
            ans = -ans
        pivot = A[j][j]
        ans *= pivot
        for k in range(j + 1, len(A)):
            factor = A[k][j] / pivot
            for l in range(j + 1, len(A)):
                A[k][l] -= factor * A[j][l]
    return ans


def check36():
    X, Y = range(3), range(3, 6)
    clients = [frozenset((a, b)) for a in X for b in Y]
    clients += [frozenset(I + J) for I in combinations(X, 2)
                for J in combinations(Y, 2) for _ in range(3)]
    data = json.loads((CERT / 'onpath_budget_failure.json').read_text())
    actions = {tuple(row['history']): row['action'] for row in data['strategy']['actions']}
    z, matrices = queries(clients, actions, 3)
    assert z == (0, 3, 4) and len(clients) == 36
    rows = {B: [payoff(clients, a, B) for a in range(6)]
            for B in product(range(6), repeat=2)}
    dual = list(combinations(X, 2)) + list(combinations(Y, 2))
    assert all(sum((rows[B][a] for B in dual), F(0))/6 == 10 for a in range(6))
    # For optimal p every positive-dual row is tight. The within-group
    # coefficients are (9,9,12), hence tightness is 3p_j=sum(group p).
    for group in [X, Y]:
        for B in combinations(group, 2):
            omitted = next(a for a in group if a not in B)
            expected = [F(10) for _ in range(6)]
            for a in group:
                expected[a] = 12 if a == omitted else 9
            assert rows[B] == expected
    pure_classes = {'repeated': set(), 'same_group_distinct': set(), 'cross_group': set()}
    for B, row in rows.items():
        kind = 'repeated' if B[0] == B[1] else ('same_group_distinct' if B[0]//3 == B[1]//3 else 'cross_group')
        # Both group-uniform endpoints have the same payoff for every row.
        ux = sum(row[:3])/3
        uy = sum(row[3:])/3
        assert ux == uy
        pure_classes[kind].add(ux)
    assert pure_classes == {'repeated': {F(37,3)}, 'same_group_distinct': {F(10)}, 'cross_group': {F(97,9)}}
    # p(lambda)=v+lambda*w; save all exact coefficients, not point sampling.
    v = [F(0)]*3 + [F(1,3)]*3
    w = [F(1,3)]*3 + [-F(1,3)]*3
    coefficients = []
    for M in matrices:
        c0 = quadratic(M, v)
        c2 = quadratic(M, w)
        c1 = sum((M[a][b]*(v[a]*w[b]+w[a]*v[b]) for a,b in product(range(6),repeat=2)), F(0))
        coefficients.append([c0, c1, c2])
    assert coefficients == [[F(10),F(0),F(0)], [F(97,9),-F(7,9),F(0)], [F(97,9),F(0),F(0)]]
    G = [F(34)-sum(c[0] for c in coefficients), -sum(c[1] for c in coefficients), -sum(c[2] for c in coefficients)]
    assert G == [F(22,9),F(7,9),F(0)]
    return {'optimal_face':'lambda*Unif(X)+(1-lambda)*Unif(Y), 0<=lambda<=1',
            'static_class_values': {k:list(v) for k,v in pure_classes.items()},
            'C_coefficients_constant_linear_quadratic':coefficients,
            'G_coefficients_constant_linear_quadratic':G, 'query_matrices':matrices,
            'optimal_value':10, 'on_path':z}


def check89():
    weights = {5:16,10:1,11:11,15:8,22:1,23:2,24:2,26:1,33:1,
               35:5,40:4,46:2,52:1,53:4,54:14,56:2,61:10,62:4}
    clients = [frozenset(a for a in range(6) if mask>>a&1)
               for mask, count in weights.items() for _ in range(count)]
    data = json.loads((CERT/'global_decorrelation_failure.json').read_text())
    actions = {tuple(row['history']):row['action'] for row in data['strategy']['actions']}
    p = list(map(F,data['security']['primary']))
    value = F(data['security']['value'])
    rows = {B:[payoff(clients,a,B) for a in range(6)] for B in product(range(6),repeat=3)}
    means = {B:sum(p[a]*row[a] for a in range(6)) for B,row in rows.items()}
    assert min(means.values()) == value
    dual = [(tuple(d['rivals']),F(d['probability'])) for d in data['security']['dual']]
    assert sum(q for B,q in dual) == 1 and all(q>0 for B,q in dual)
    dual_rows = [sum(q*rows[B][a] for B,q in dual) for a in range(6)]
    assert dual_rows == [value,value,value,value,F(414135,26546),value]
    assert {tuple(sorted(B)) for B in means if means[B] == value} == {B for B,q in dual}
    support = [0,1,2,3,5]
    matrix12 = [[12*rows[B][a] for a in support] for B,q in dual]
    assert all(v.denominator == 1 for row in matrix12 for v in row)
    determinant = det(matrix12)
    assert determinant == -6103716000
    z, matrices = queries(clients,actions,4)
    assert z == (2,5,0,0)
    C = [quadratic(M,p) for M in matrices]
    assert C == [F(5250625730573,264258793500),F(510157878527,26425879350),F(508643,26546),F(508643,26546)]
    G = F(85)-sum(C)
    assert G == F(1982965123157,264258793500)>0
    return {'unique_optimal_query':p, 'value':value, 'active_backgrounds':[B for B,q in dual],
            'positive_dual':dual, 'dual_pure_query_values':dual_rows,
            '12_times_active_5_by_5':matrix12, 'determinant':determinant,
            'on_path':z, 'C_at_unique_optimum':C,'G_at_unique_optimum':G,
            'query_matrices':matrices}


if __name__ == '__main__':
    result = {'scope':'exact arithmetic for the new optimal-face/uniqueness/budget comparisons; original full SPE certificates reused',
              'case36':check36(), 'case89':check89(),
              'input_sha256':{name:hashlib.sha256((CERT/name).read_bytes()).hexdigest()
                              for name in ['onpath_budget_failure.json','global_decorrelation_failure.json']}}
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
