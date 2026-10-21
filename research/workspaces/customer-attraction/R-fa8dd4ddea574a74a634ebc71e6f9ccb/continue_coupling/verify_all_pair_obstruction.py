"""Independent exact audit of the inherited all-pair obstruction candidate.

No search-generator, LP solver, or customer-attraction engine is imported.
The abstract point is NOT asserted to be a common-client payoff table or SPE.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tree_coupling/all_pair_identities_obstruction_candidate.json'


def reconstruct():
    obj = json.loads(SOURCE.read_text())
    m, p = obj['n'], obj['p']
    assert (m, p) == (3, 6)
    actions = {tuple(r['history']): r['action'] for r in obj['strategy_actions']}
    histories = [h for d in range(m) for h in product(range(p), repeat=d)]
    assert len(actions) == len(histories) and set(actions) == set(histories)
    assert all(0 <= a < p for a in actions.values())
    def counts(h):
        return tuple(h.count(a) for a in range(p))
    def terminal(h):
        while len(h) < m:
            h += (actions[h],)
        return counts(h)
    qs = sorted({counts(h) for h in product(range(p), repeat=m)})
    vertices = [(q, a) for q in qs for a in range(p) if q[a]]
    y = {(tuple(r['q']), r['a']): Q(r['value']) for r in obj['y']}
    assert set(y) == set(vertices) and len(obj['y']) == len(vertices)
    assert min(y.values()) >= 0
    types = list(range(1, 1 << p))
    def cover(A):
        if not A:
            return Q(0)
        q = tuple((m - len(A) + 1 if a == min(A) else 1) if a in A else 0 for a in range(p))
        return sum(q[a] * y[q, a] for a in A)
    return obj, m, p, actions, histories, terminal, qs, vertices, y, types, cover


def main():
    obj, m, p, actions, histories, terminal, qs, vertices, y, types, cover = reconstruct()
    source = obj['source_customer_weights']
    assert len(source) == len(types) and all(isinstance(w, int) and w >= 0 for w in source)
    def source_pay(q, a):
        return sum(Q(source[B-1], sum(q[c] for c in range(p) if B >> c & 1)) for B in types if B >> a & 1)
    graph_slacks, source_slacks = [], []
    for h in histories:
        a = actions[h]
        q = terminal(h)
        for b in range(p):
            r = terminal(h + (b,))
            graph_slacks.append(y[q, a] - y[r, b])
            source_slacks.append(source_pay(q, a) - source_pay(r, b))
    assert min(graph_slacks) >= 0
    assert min(source_slacks) >= 0
    assert tuple(obj['root']) == terminal(())
    dilution_slacks = []
    for q, a in vertices:
        for r, b in vertices:
            if b != a or q == r:
                continue
            kappa = max(Q(sum(r[c] for c in range(p) if B >> c & 1), sum(q[c] for c in range(p) if B >> c & 1)) for B in types if B >> a & 1)
            dilution_slacks.append(kappa * y[r, a] - y[q, a])
    assert min(dilution_slacks) >= 0
    pair_checks = 0
    support_checks = 0
    for q, a in vertices:
        A = tuple(c for c in range(p) if q[c])
        total = sum(q[c] * y[q, c] for c in A)
        assert total == cover(A)
        support_checks += 1
        if len(A) != 2:
            continue
        b = next(c for c in A if c != a)
        r, s = q[a], q[b]
        assert m*r*y[q,a] == r*cover((a,)) + s*(cover(A)-cover((b,)))
        pair_checks += 1
    # Full signed-common-client identities for a three-label support.
    # J=0 follows independently by the seven nonempty membership modes.
    violations = []
    for A in combinations(range(p), 3):
        q = tuple(int(a in A) for a in range(p))
        for a in A:
            b, c = (x for x in A if x != a)
            residual = 6*y[q,a] - (2*cover((a,)) + cover(tuple(sorted((a,b))))-cover((b,)) + cover(tuple(sorted((a,c))))-cover((c,)) + 2*cover(A)-2*cover(tuple(sorted((b,c)))))
            if residual:
                violations.append({'support': list(A), 'a': a, 'residual': str(residual)})
    qroot = terminal(())
    W = sum(qroot[a]*y[qroot,a] for a in range(p) if qroot[a])
    O = cover(tuple(obj['target']))
    assert W == 1 and O == Q(27,13) and O > 2*W
    assert violations
    print(json.dumps({'exact': True, 'vertices': len(vertices), 'histories': len(histories), 'abstract_graph_comparisons': len(graph_slacks), 'source_unit_game_SPE_comparisons': len(source_slacks), 'sharp_dilution_comparisons': len(dilution_slacks), 'two_support_identity_checks': pair_checks, 'support_conservation_checks': support_checks, 'W': str(W), 'comparison_coverage': str(O), 'triple_identity_violations': violations, 'scope': 'Abstract all-two-support template obstruction; not a common-client payoff table and not an SPE counterexample.'}, indent=2))


if __name__ == '__main__':
    main()
