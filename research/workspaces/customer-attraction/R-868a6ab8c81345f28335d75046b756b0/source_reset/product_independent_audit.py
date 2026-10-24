"""Independent Fraction audit of the exact product-L nonadditivity witness.

No author implementation or canonical SPE solver is imported. The only
external input is the author's supplied complete strategy certificate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
CERT = HERE.parent / 'dynamic_matching' / 'product_transfer_certificate.json'
BASE = (frozenset('B'), frozenset('AB'), frozenset('C'),
        frozenset('AC'), frozenset('AC'))
CAT = 'ABC'
VECTORS = tuple(''.join(v) for v in product(CAT, repeat=2))


def utility(path, role, interests):
    return sum((F(1, sum(a in inc for a in path))
                for inc in interests if path[role] in inc), F(0))


def unit_component():
    rows = []
    floors = []
    for a in CAT:
        br_value = max(utility(('B', a, b), 2, BASE) for b in CAT)
        br = [b for b in CAT if utility(('B', a, b), 2, BASE) == br_value]
        floors.append(min(utility(('B', a, b), 1, BASE) for b in br))
        for b in br:
            path = ('B', a, b)
            rows.append(dict(second=a, last=b,
                             d=utility(path, 0, BASE),
                             v=utility(path, 1, BASE),
                             last_u=utility(path, 2, BASE)))
    theta = max(floors)
    assert theta == F(3, 2)
    assert [(r['second'], r['last'], r['d'], r['v']) for r in rows] == [
        ('A', 'C', F(3, 2), F(3, 2)),
        ('B', 'C', F(1), F(1)),
        ('C', 'A', F(3, 2), F(2)),
        ('C', 'C', F(2), F(3, 2))]
    assert all(r['d'] >= r['v'] / 2 + F(1, 2) for r in rows)
    single_l = min(r['d'] for r in rows if r['v'] >= theta)
    assert single_l == F(3, 2)
    return rows, theta, single_l


def product_interests():
    # Every local client gets its own component label; all ten are distinct.
    return tuple(frozenset(a for a in VECTORS if a[k] in inc)
                 for k in range(2) for inc in BASE)


def main():
    component_rows, theta, single_l = unit_component()
    incs = product_interests()
    raw_rows, floors = [], []
    for a in VECTORS:
        best = max(utility(('BB', a, b), 2, incs) for b in VECTORS)
        br = [b for b in VECTORS if utility(('BB', a, b), 2, incs) == best]
        floors.append(min(utility(('BB', a, b), 1, incs) for b in br))
        for b in br:
            path = ('BB', a, b)
            row = dict(second=a, last=b,
                       d=utility(path, 0, incs), v=utility(path, 1, incs),
                       last_u=utility(path, 2, incs))
            assert row['d'] >= row['v'] / 2 + 1
            raw_rows.append(row)
    product_theta = max(floors)
    assert product_theta == 2 * theta == 3
    assert len(raw_rows) == 16
    filtered = [r for r in raw_rows if r['v'] >= product_theta]
    product_l = min(r['d'] for r in filtered)
    assert product_l == F(5, 2) < 2 * single_l
    witness = next(r for r in filtered if (r['second'], r['last']) == ('BC', 'CA'))
    assert (witness['d'], witness['v'], witness['last_u']) == (F(5, 2), F(3), F(9, 2))

    payload = json.loads(CERT.read_text())
    declared = payload['instance']
    assert tuple(declared['topics']) == VECTORS and declared['players'] == 3
    declared_inc = tuple(frozenset(VECTORS[a] for a in row['topics'])
                         for row in declared['customers']
                         for _ in range(row['multiplicity']))
    assert declared_inc == incs
    policy = {tuple(r['history']): r['action'] for r in payload['policy']}
    expected = {h for depth in range(3) for h in product(VECTORS, repeat=depth)}
    assert set(policy) == expected and len(policy) == 91
    assert all(a in VECTORS for a in policy.values())

    def finish(h):
        h = tuple(h)
        while len(h) < 3:
            h += (policy[h],)
        return h

    comparisons = 0
    min_slack = None
    for h in sorted(expected, key=lambda a: (len(a), a)):
        role = len(h)
        actual_u = utility(finish(h), role, incs)
        for a in VECTORS:
            slack = actual_u - utility(finish(h + (a,)), role, incs)
            assert slack >= 0, (h, a, slack)
            min_slack = slack if min_slack is None else min(min_slack, slack)
            comparisons += 1
    assert comparisons == 819 and min_slack == 0
    assert finish(('BB',)) == ('BB', 'BC', 'CA')
    actual = finish(())
    actual_payoffs = [utility(actual, i, incs) for i in range(3)]
    actual_w = sum(any(a in inc for a in actual) for inc in incs)
    optimum = max(sum(any(a in inc for a in z) for inc in incs)
                  for z in product(VECTORS, repeat=3))
    assert actual == ('CC', 'AA', 'BB')
    assert actual_payoffs == [F(4), F(3), F(3)]
    assert actual_w == optimum == 10
    out = dict(
        status='PASS: exact product-L nonadditivity; not a half or SM counterexample',
        certificate_sha256=hashlib.sha256(CERT.read_bytes()).hexdigest(),
        component_theta=theta, component_L_B=single_l,
        component_terminal_BR_rows=component_rows,
        product_theta=product_theta, product_terminal_BR_rows=len(raw_rows),
        product_SPE_filtered_rows=len(filtered), product_L_BB=product_l,
        product_all_BR_rows=raw_rows, product_minimum_witness=witness,
        full_policy_histories=len(expected), full_policy_comparisons=comparisons,
        minimum_slack=min_slack, actual=actual, payoffs=actual_payoffs,
        W=actual_w, OPT=optimum,
        proof_scope='All-product-two-remaining-player threshold proved analytically in review')
    text = json.dumps(out, default=str, ensure_ascii=False, indent=2) + '\n'
    (HERE / 'product_independent_audit.json').write_text(text)
    print(json.dumps({k: v for k, v in out.items() if 'rows' not in k},
                     default=str, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
