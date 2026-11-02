"""Exact construction audit; no finite check proves universal repair or HALF.

Rebuild one established complete SPE and its max-future initialization without
importing the author's flow code. Also check a strictly separated abstract
triangular routing contract, explicitly not certified as game data.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def price_check(atoms, base, profits, prices):
    """Atoms are (owner, b, terminal_mass_vector)."""
    fine = F()
    grouped = defaultdict(list)
    for owner, b, K in atoms:
        if b == 0:
            assert all(v == 0 for v in K)
            continue
        assert sum(K, F()) == b
        q = sum((prices[l] * K[l] / b for l in range(len(prices))), F())
        fine += b * min(prices[owner], q)
        grouped[owner].append((b, q))
    coarse = F()
    rebate = F()
    for owner, rows in grouped.items():
        b = sum((z[0] for z in rows), F())
        qbar = sum((bb * q for bb, q in rows), F()) / b
        coarse += b * min(prices[owner], qbar)
        D = sum((bb * max(F(), prices[owner] - q) for bb, q in rows), F())
        E = sum((bb * max(F(), q - prices[owner]) for bb, q in rows), F())
        rebate += min(D, E)
    assert coarse - fine == rebate >= 0
    rhs = sum((prices[l] * (2 * profits[l] - base[l])
               for l in range(len(prices))), F())
    return fine, coarse, rhs, rebate


def real_fixture():
    src = ROOT / ('research/workspaces/customer-attraction/'
                  'R-a0bb57fa24044a8794bc7991918a19c6/static_matching/'
                  'static_matching_counterexample.json')
    raw = json.loads(src.read_text())
    instance = raw['instance']
    clients = [set(z['topics']) for z in instance['customers']
               for _ in range(z.get('multiplicity', 1))]
    m, k = instance['players'], len(instance['topics'])
    policy = {tuple(row['history']): row['action']
              for row in raw['certificate']['actions']}

    def finish(g):
        while len(g) < m:
            g += (policy[g],)
        return g

    def load(leaf, x):
        return sum(a in clients[x] for a in leaf)

    def payoff(leaf, i):
        return sum((F(1, load(leaf, x)) for x, v in enumerate(clients)
                    if leaf[i] in v), F())

    checks = 0
    for depth in range(m):
        for g in product(range(k), repeat=depth):
            for a in range(k):
                assert payoff(finish(g), depth) >= payoff(finish(g + (a,)), depth)
                checks += 1
    B, T = finish(()), (0, 1, 4, 5)
    cb = [load(B, x) for x in range(len(clients))]
    ct = [load(T, x) for x in range(len(clients))]
    opt = max(sum(any(a in v for a in z) for v in clients)
              for z in combinations_with_replacement(range(k), m))
    assert sum(bool(z) for z in ct) == opt
    u = [payoff(B, i) for i in range(m)]
    Hx = [[F() for _ in clients] for _ in range(m)]
    d = [F() for _ in range(m)]
    initial, Iinitial = {}, []
    coordinates = {}
    for i in range(m):
        W = finish(B[:i] + (T[i],))
        for x, v in enumerate(clients):
            if T[i] not in v:
                continue
            p = F(1, ct[x])
            delta = cb[x] + 1 - int(B[i] in v)
            pb = F()
            for l in range(m):
                if l != i and B[l] in v and T[l] not in v:
                    value = p / delta
                    pb += value
                    Hx[l][x] += value
            r = p - pb
            edges = {j: min(p, F(1, delta)) / load(W, x)
                     for j in range(i + 1, m)
                     if W[j] in v and B[j] not in v}
            q = sum(edges.values(), F())
            amount = min(r, q)  # established max-future admissible corner
            coordinates[i, x] = [r - amount, amount]
            d[i] += r - amount
            for j, edgecap in edges.items():
                mass = amount * edgecap / q
                assert 0 <= mass <= edgecap
                if mass == 0:
                    continue
                if cb[x]:
                    Iinitial.append((x, mass))
                else:
                    initial[i, x, j] = (W[:j], mass)
        assert d[i] <= u[i]
    H = [sum(row, F()) for row in Hx]
    J = [F() for _ in range(m)]
    for x in range(len(clients)):
        if not cb[x]:
            continue
        mass = sum((z for xx, z in Iinitial if xx == x), F())
        remain = [F(int(B[l] in clients[x]), cb[x]) - Hx[l][x]
                  for l in range(m)]
        assert all(z >= 0 for z in remain)
        assert mass <= sum(remain, F())
        if mass:
            for l in range(m):
                J[l] += mass * remain[l] / sum(remain, F())
    A = [d[l] + H[l] + J[l] for l in range(m)]
    assert all(A[l] <= 2 * u[l] for l in range(m))

    def propagate(theta):
        incoming = defaultdict(F)
        K = {a: [F() for _ in range(m)] for a in initial}
        untagged_current = [F() for _ in range(m)]
        for a, (g, b) in initial.items():
            incoming[a, g] += b * (1 - theta.get(a, F()))
        for l in range(m):
            keys = [key for key in incoming if len(key[1]) == l and incoming[key]]
            bynode = defaultdict(F)
            for a, g in keys:
                bynode[g, a[1]] += incoming[a, g]
            for (g, x), mass in bynode.items():
                assert mass * load(finish(g), x) <= 1
            for a, g in keys:
                x = a[1]
                mass = incoming[a, g]
                V = finish(g)
                reset = finish(B[:l] + (V[l],))
                den = load(reset, x)
                new = [j for j in range(l + 1, m)
                       if reset[j] in clients[x] and V[j] not in clients[x]]
                current = mass * (den - len(new)) / den
                assert current >= 0
                K[a][l] += current
                untagged_current[l] += current
                for j in new:
                    incoming[a, reset[:j]] += mass / den
        assert all(untagged_current[l] == sum((z[l] for z in K.values()), F())
                   for l in range(m))  # full tracking at every role
        for a, (_, b) in initial.items():
            assert sum(K[a], F()) == b * (1 - theta.get(a, F()))
            assert all(K[a][l] == 0 for l in range(a[0] + 1))
        return K

    K = propagate({})
    # Deliberately heterogeneous independent atom fractions; no universal-cap
    # claim follows from this arbitrary choice.
    theta = {a: F(index % 3, 3) for index, a in enumerate(initial)}
    scaled = propagate(theta)
    retained = [F() for _ in range(m)]
    F0 = [A[l] + sum((z[l] for z in K.values()), F()) for l in range(m)]
    for a, (_, b) in initial.items():
        retained[a[0]] += theta[a] * b
        for l in range(m):
            assert scaled[a][l] == (1 - theta[a]) * K[a][l]
        i, x, _ = a
        coordinates[i, x][0] += theta[a] * b
        coordinates[i, x][1] -= theta[a] * b
    F1 = [A[l] + retained[l] + sum((z[l] for z in scaled.values()), F())
          for l in range(m)]
    assert sum(F0, F()) == sum(F1, F()) == opt
    for l in range(m):
        expected = F0[l] + retained[l] - sum((theta[a] * K[a][l] for a in K), F())
        assert F1[l] == expected
    atoms = [(a[0], initial[a][1], K[a]) for a in initial]
    atoms.append((0, F(), [F() for _ in range(m)]))
    price_checks = 0
    for lam in product([F(), F(1, 2), F(1)], repeat=m):
        price_check(atoms, A, u, lam)
        price_checks += 1
    assert price_check(atoms, A, u, [F(1)] * m)[3] == 0
    return {'source': str(src.relative_to(ROOT)), 'complete_history_IC_checks': checks,
            'unit_clients': len(clients), 'm': m, 'B': B, 'T': T, 'OPT': opt,
            'positive_R_initial_edge_atoms': len(initial),
            'atom_mass': [str(initial[a][1]) for a in initial],
            'atom_K': [[str(z) for z in K[a]] for a in initial],
            'full_tracking_per_role': True, 'u': list(map(str, u)),
            'A': list(map(str, A)), 'old_cost': list(map(str, F0)),
            'arbitrary_scaled_cost': list(map(str, F1)),
            'arbitrary_scaling_meets_caps': all(F1[l] <= 2 * u[l] for l in range(m)),
            'price_identity_checks': price_checks}


def abstract_strict_refinement():
    u = [F(1)] * 3
    A = [F(3, 2), F(2), F(1)]
    atoms = [(0, F(1, 2), [F(), F(1, 2), F()]),
             (0, F(1, 2), [F(), F(), F(1, 2)]),
             (0, F(), [F(), F(), F()])]
    fine, coarse, rhs, rebate = price_check(atoms, A, u, [F(1, 2), F(1), F()])
    assert (fine, coarse, rhs, rebate) == (F(1, 4), F(1, 2), F(1, 4), F(1, 4))
    # Old ratio repair requires y<=1/2 and y>=1, whereas atom repair below works.
    newcost = [F(2), F(2), F(3, 2)]
    assert all(v <= 2 for v in newcost)
    for lam in product([F(), F(1, 2), F(1), F(2)], repeat=3):
        f, _, r, _ = price_check(atoms, A, u, lam)
        assert f <= r
    return {'scope': 'abstract triangular routing contract; not SPE-certified',
            'coarse_cut_LHS': str(coarse), 'fine_cut_LHS': str(fine),
            'common_RHS': str(rhs), 'exact_dispersion_rebate': str(rebate),
            'successful_atom_cost': list(map(str, newcost)),
            'zero_atom_included': True}


if __name__ == '__main__':
    result = {'status': 'construction identities audited; no universal repair claim',
              'real_complete_SPE_fixture': real_fixture(),
              'strict_linear_refinement': abstract_strict_refinement()}
    target = HERE / 'atom_retraction_audit.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
