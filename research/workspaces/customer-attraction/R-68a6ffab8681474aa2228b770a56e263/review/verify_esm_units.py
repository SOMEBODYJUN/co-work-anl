"""Independent complete-history, explicit-unit validation of the ESM obstruction.

No author checker, equilibrium solver, or claimed numerical output is used.
Only the raw customer multiplicities and complete action table are read.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'attack/potential_tax/esm_exact_obstruction.json'


def main():
    raw = json.loads(SOURCE.read_text())
    m, p = raw['players'], len(raw['topics'])
    assert m == 3 and p == 5
    clients = [frozenset(t['topics']) for t in raw['customers']
               for _ in range(t['multiplicity'])]
    assert all(isinstance(t['multiplicity'], int) and t['multiplicity'] > 0
               for t in raw['customers'])
    coverage = [frozenset(x for x, likes in enumerate(clients) if a in likes)
                for a in range(p)]
    assert len(set(coverage)) == p
    policy = {(): raw['root_action']}
    policy.update({(a,): raw['second_actions'][a] for a in range(p)})
    policy.update({(a, b): raw['last_actions'][a][b]
                   for a, b in product(range(p), repeat=2)})
    histories = [h for d in range(m) for h in product(range(p), repeat=d)]
    assert set(policy) == set(histories)
    assert all(a in range(p) for a in policy.values())

    def finish(h):
        while len(h) < m:
            h += (policy[h],)
        return h

    def utilities(leaf):
        result = [F() for _ in leaf]
        for likes in clients:
            covered_by = [i for i, a in enumerate(leaf) if a in likes]
            if covered_by:
                for i in covered_by:
                    result[i] += F(1, len(covered_by))
        return result

    def welfare(leaf):
        return sum(any(a in likes for a in leaf) for likes in clients)

    def harmonic(n):
        return sum((F(1, j) for j in range(1, n+1)), F())

    def phi(prefix, suffix):
        return sum((harmonic(sum(a in likes for a in prefix+suffix))
                    -harmonic(sum(a in likes for a in prefix))
                    for likes in clients), F())

    all_ic = []
    for h in histories:
        u = utilities(finish(h))[len(h)]
        for a in range(p):
            all_ic.append(u-utilities(finish(h+(a,)))[len(h)])
    assert min(all_ic) >= 0
    actual = finish(())
    u = utilities(actual)
    all_leaves = list(product(range(p), repeat=m))
    P = max(phi((), leaf) for leaf in all_leaves)
    PA = max(phi((), leaf) for leaf in all_leaves if actual[0] in leaf)
    safe = F(len(coverage[actual[0]]), m)
    loss = P-PA
    violation = loss-(u[0]-safe)
    assert violation > 0
    W = welfare(actual)
    OPT = max(welfare(leaf) for leaf in all_leaves)
    tax = F()
    margins = []
    for i, action in enumerate(actual):
        prefix = actual[:i]
        r = m-i
        Farrival = F()
        si = F()
        for likes in clients:
            b = sum(a in likes for a in prefix)
            if action in likes:
                Farrival += F(1, b+1)
                si += F(1, b+r)
        tax += Farrival-si
        tails = list(product(range(p), repeat=r))
        Pi = max(phi(prefix, tail) for tail in tails)
        PiA = max(phi(prefix, tail) for tail in tails if action in tail)
        margins.append(u[i]-si-(Pi-PiA))
    assert sum(u) == W
    assert sum(margins) == W+tax-P
    assert (len(clients), actual, u, P, PA, safe, violation, W, OPT, tax) == (
        621, (0, 1, 2), [F(166), F(190), F(190)], F(801), F(754),
        F(120), F(1), 546, 621, F(647, 2))
    report = {
        'status': 'PASS',
        'scope': 'complete SPE counterexample to general local ESM at three-player zero background; not six-player half, not total potential counterexample',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'explicit_unit_customers': len(clients),
        'complete_ordered_histories': len(histories),
        'full_ic_comparisons': len(all_ic),
        'minimum_ic_slack': str(min(all_ic)),
        'actual_path': list(actual), 'actual_payoffs': list(map(str, u)),
        'all_ordered_comparison_tuples': len(all_leaves),
        'P3': str(P), 'P3_containing_A': str(PA),
        'forcing_loss': str(loss), 'actual_surplus': str(u[0]-safe),
        'ESM_violation': str(violation), 'W': W, 'OPT3': OPT,
        'copy_tax': str(tax), 'total_potential_margin': str(W+tax-P),
        'local_ESM_margins': list(map(str, margins)),
    }
    HERE.joinpath('esm_units_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
