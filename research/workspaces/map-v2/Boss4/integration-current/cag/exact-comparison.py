"""Independent finite algebra for Boss4's two-package integration review.

Run with standard-library Python; never imports source solvers or edits registered source assets. Only this review JSON is written.
All-B conclusions use exact coefficient signs/rank identities, not sampling B.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement as cwr
from functools import cache
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'work.py').is_file() and (p / 'archives/customer-attraction').is_dir())
OUT = Path(__file__).resolve().parent


def sigma(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    return min(set(range(0, 3) if h[1] < 3 else range(3, 6)) - set(h))


def leaf(h):
    return h if len(h) == 3 else leaf(h + (sigma(h),))


NEW = {
    0: [((), 3, F(1, 6)), ((0,), 0, F(1, 6)), ((0,), 1, F(1, 6)),
        ((1,), 0, F(1, 6)), ((0, 2), 0, F(1, 6)), ((1, 3), 0, F(1, 3))],
    1: [((), 3, F(1, 3)), ((0,), 1, F(1, 3)), ((0, 3), 1, F(1, 3)), ((0, 5), 1, F(1, 3))],
    2: [((), 4, F(1, 3)), ((0,), 1, F(1, 3)), ((0, 3), 2, F(2, 3)), ((4, 0), 2, F(1, 3))],
    3: [((), 3, F(1, 3)), ((0,), 1, F(1, 3)), ((0, 2), 3, F(1, 3)), ((0, 3), 3, F(1, 3))],
    4: [((), 4, F(1, 3)), ((0,), 1, F(1, 3)), ((0, 2), 4, F(1, 3))],
    5: [((), 5, F(1, 3)), ((0,), 1, F(1, 3)), ((0, 2), 5, F(1, 3)), ((0, 3), 5, F(1, 3))],
}
OLD = {
    0: [((), 3, F(1, 7)), ((0,), 0, F(4, 21)), ((0,), 1, F(1, 6)), ((1,), 0, F(1, 6)),
        ((0, 2), 0, F(1, 14)), ((0, 2), 3, F(2, 21)), ((1, 3), 0, F(1, 3))],
    1: [((), 3, F(1, 6)), ((0,), 1, F(1, 3)), ((3,), 1, F(1, 12)), ((4,), 1, F(1, 12)),
        ((0, 3), 1, F(1, 4)), ((0, 4), 1, F(1, 12))],
    2: [((), 2, F(1, 12)), ((), 3, F(1, 6)), ((), 4, F(1, 12)), ((0,), 2, F(7, 24)),
        ((1,), 2, F(1, 24)), ((3,), 2, F(1, 24)), ((0, 3), 2, F(3, 8)),
        ((0, 5), 2, F(1, 12)), ((1, 4), 0, F(1, 24))],
    3: NEW[3], 4: NEW[4], 5: NEW[5],
}


def residual(a, mask, weights):
    # Exact symbolic coordinates in basis 1/(b+1),1/(b+2),1/(b+3).
    r = [F() for _ in range(4)]
    likes = lambda a: bool(mask & (1 << a))
    hits = lambda z: sum(likes(a) for a in z)
    actual_hits = hits(leaf(()))
    r[actual_hits] += F(actual_hits, 3)
    if likes(a):
        for other in (1, 2, 3):
            r[hits((0, other, a))] -= F(1, 3)
    for h, d, w in weights[a]:
        assert w > 0 and d != sigma(h)
        if likes(sigma(h)):
            r[hits(leaf(h))] -= w
        if likes(d):
            r[hits(leaf(h + (d,)))] += w
    assert r[0] == 0
    c1, c2, c3 = r[1:]
    # Numerator in ascending powers of b.
    return r[1:], [6*c1+3*c2+2*c3, 5*c1+4*c2+3*c3, c1+c2+c3]


poly_rows = []
positive_by_degree = [0, 0, 0]
old_zero = []
for a, m in product(range(6), range(1, 64)):
    basis, numerator = residual(a, m, NEW)
    assert min(numerator) >= 0
    positive_by_degree = [n + int(v > 0) for n, v in zip(positive_by_degree, numerator)]
    poly_rows.append(dict(query=a, mask=m, reciprocal_coefficients=list(map(str, basis)),
                          numerator=list(map(str, numerator))))
    old_basis, _ = residual(a, m, OLD)
    v = sum((x / i for i, x in enumerate(old_basis, 1)), F())
    assert v >= 0
    old_zero.append((a, m, v))
assert positive_by_degree == [64, 64, 0]
old_bad_basis, old_bad_num = residual(1, 2, OLD)
assert old_bad_num == [0, F(-1, 2), F(-1, 6)]
# This numerator is -b*(b+3)/6, i.e. -b/[6(b+1)(b+2)].


THEMES = tuple((i, j) for i in range(2) for j in range(2, 5)) + tuple((i,) for i in range(5))
RANK = {p: 10-i for i, p in enumerate(((1, 1), (1, 2), (1, 3), (2, 2), (1, 4),
                                    (2, 3), (2, 4), (3, 3), (3, 4), (4, 4)))}


def loads(c):
    return tuple(sum(n for a, n in enumerate(c) if x in THEMES[a]) for x in range(5))


def add(c, a):
    return c[:a] + (c[a] + 1,) + c[a+1:]


def ordinal(a, c):
    l = loads(c)
    return RANK[tuple(sorted(l[x] for x in THEMES[a]))]


@cache
def outcomes(c):
    if sum(c) == 4:
        return frozenset((c,))
    branches = [outcomes(add(c, a)) for a in range(6)]
    threshold = max(min(ordinal(a, z) for z in branches[a]) for a in range(6))
    return frozenset(z for a in range(6) for z in branches[a] if ordinal(a, z) >= threshold)


representatives = ['555', '455', '345', '255', '245', '244', '234', '55', '45', '25', '24', '0']
expected = [set(x.split()) for x in [
    '0 1', '0', '0 1 2', '0 1', '0', '0', '0 1 2', '01', '00 01 02 13 23',
    '04 13', '03 04 05 13 23', '045 123 135 145 155 234 244 245']]
table = []
for h_text, wanted in zip(representatives, expected):
    c = tuple(h_text.count(str(a)) for a in range(6))
    got = {''.join(str(a)*(z[a]-c[a]) for a in range(6)) for z in outcomes(c)}
    assert got == wanted, (h_text, got, wanted)
    table.append(dict(history=h_text, completions=sorted(got)))
root_outcomes = outcomes((0,)*6)
spectra = Counter(tuple(sorted(loads(z))) for z in root_outcomes)
assert set(spectra) == {(1, 1, 2, 2, 2), (1, 1, 1, 2, 3)}

main_policy = {}
def realize(h, c, target):
    if len(h) == 4:
        assert c == target
        return
    branches = [outcomes(add(c, a)) for a in range(6)]
    threshold = max(min(ordinal(a, z) for z in branches[a]) for a in range(6))
    chosen = min(a for a in range(6) if target in branches[a] and ordinal(a, target) >= threshold)
    main_policy[h] = chosen
    for a in range(6):
        z = target if a == chosen else min(branches[a], key=lambda z: (ordinal(a, z), z))
        realize(h+(a,), add(c, a), z)


realize((), (0,)*6, (1, 1, 1, 1, 0, 0))
full_policy = {}
@cache
def canonical(h):
    if len(h) == 4:
        return h
    leaves = [canonical(h+(a,)) for a in range(11)]
    def rank(a):
        c = tuple(leaves[a].count(j) for j in range(11))
        return ordinal(a, c)
    chosen = max(range(6), key=rank)
    full_policy[h] = chosen
    return leaves[chosen]


def graft(h):
    if len(h) == 4:
        return
    if all(a < 6 for a in h):
        full_policy[h] = main_policy[h]
        for a in range(11):
            graft(h+(a,))
    else:
        canonical(h)


graft(())
@cache
def full_leaf(h):
    return h if len(h) == 4 else full_leaf(h+(full_policy[h],))


def actual_payoff(z, i, B):
    l = loads(tuple(z.count(a) for a in range(11)))
    return sum((F(1, B+l[x]) for x in THEMES[z[i]]), F())


audits = []
for B in (3, 4, 10):
    n = 0
    minimum = None
    for h, a in full_policy.items():
        u = actual_payoff(full_leaf(h), len(h), B)
        for d in range(11):
            delta = u - actual_payoff(full_leaf(h+(d,)), len(h), B)
            assert delta >= 0
            minimum = delta if minimum is None else min(minimum, delta)
            n += 1
    def f(a, bg, past=()):
        return sum((F(1, B+1+sum(x in THEMES[d] for d in bg+past)) for x in THEMES[a]), F())
    V = F(3, 2*(B+2)) + F(1, 2*(B+3))
    lower = min(sum((f(a, bg)/6 for a in range(6)), F()) for bg in cwr(range(11), 3))
    caps = [(f(a, (0, 4, 2))+f(a, (0, 4, 5)))/2 for a in range(11)]
    assert lower == V == max(caps)
    # After actual 0 and 1, pure query/competition 5 match at V_3.
    V3 = F(2, B+2)
    assert min(f(5, (d,), (0, 1)) for d in range(11)) == V3
    assert max(f(a, (5,), (0, 1)) for a in range(11)) == V3
    z = full_leaf(())
    assert z == (0, 1, 2, 3)
    u = [actual_payoff(z, i, B) for i in range(4)]
    V4 = F(1, B+1)+F(1, B+2)
    values = [V, V, V3, V4]
    D = [u[i]+(3-i)*values[i+1]-(4-i)*values[i] for i in range(3)]
    assert D[0] == F(-1, 2*(B+2)*(B+3))
    assert D[0]+D[1] == F(1, (B+1)*(B+2))
    assert sum(D) == sum(u)-4*V == F(2*(B+4), (B+1)*(B+2)*(B+3))
    assert F(1, B+4)+F(1, B+5)-F(1, B+1) == F(B*B+2*B-11, (B+1)*(B+4)*(B+5)) > 0
    audits.append(dict(B=B, histories=len(full_policy), comparisons=n, min_slack=str(minimum),
                       actual=list(z), static_V=str(V), V3=str(V3), u=list(map(str, u)),
                       D=list(map(str, D)), total_strong_balance=str(sum(D))))

# Check the frozen zero-background exact output against this independent algebra.
frozen_path = ROOT/'archives/customer-attraction/tools/evidence/root-fixed-group-common-static-dual/primary-original/c87d6242f66b0cbb8703/group_common_dual_exact.json'
frozen = json.loads(frozen_path.read_text())
for row in frozen['queries']:
    got = {str(m): str(v) for a, m, v in old_zero if a == row['query'] and v}
    assert got == row['residual']
assert frozen['strategy_actions_checked_for_definition'] == [
    [list(h), sigma(h)] for d in range(3) for h in product(range(6), repeat=d)]
floating = json.loads((ROOT/'archives/customer-attraction/tools/evidence/root-fixed-group-common-static-dual/primary-original/f3611f7c9fc0cdf8a24d/simple_common_dual_groups.json').read_text())
negative_float = [v for row in floating['lambda'] for v in row if v < 0]
assert len(negative_float) == 14

# The 113-customer root is in the identical fixed-policy cone.  Recheck its
# complete IC and saved rational saddle certificates without running any LP.
MASS = {4:3, 13:1, 14:3, 20:2, 23:1, 27:15, 29:8, 30:8, 31:4, 32:3,
        34:2, 43:8, 45:13, 46:7, 49:3, 51:7, 53:7, 54:10, 59:8}
def payoff113(a, z):
    return sum((F(w, sum(bool(m & (1 << d)) for d in z))
                for m, w in MASS.items() if m & (1 << a)), F())
ties113 = 0
for depth in range(3):
    for h in product(range(6), repeat=depth):
        for d in range(6):
            slack = payoff113(sigma(h), leaf(h))-payoff113(d, leaf(h+(d,)))
            assert slack >= 0
            ties113 += slack == 0
assert ties113 == 91 and sum(MASS.values()) == 113
u113 = [payoff113(a, leaf(())) for a in leaf(())]
assert u113 == [F(95, 3), F(110, 3), F(110, 3)]
q113 = [sum((payoff113(a, (0, d, a))/3 for d in (1, 2, 3)), F()) for a in range(6)]
saved = json.loads((ROOT/'archives/customer-attraction/tools/evidence/R2f6-security-20261031/original/local_slope_check.json').read_text())
saved113 = next(row for row in saved if row['instance'] == 'local_security_increment')
for cert in saved113['certificates']:
    h = tuple(cert['history'])
    p = [F(x) for x in cert['p']]
    Q = [(tuple(row['background']), F(row['probability'])) for row in cert['Q']]
    value = F(cert['value'])
    assert sum(p) == 1 and min(p) >= 0 and sum(w for bg,w in Q) == 1 and min(w for bg,w in Q) >= 0
    lower = min(sum((p[a]*payoff113(a, h+bg+(a,)) for a in range(6)), F())
                for bg in cwr(range(6), 2-len(h)))
    upper = max(sum((w*payoff113(a, h+bg+(a,)) for bg,w in Q), F()) for a in range(6))
    assert lower == upper == value
V113 = F(saved113['certificates'][0]['value'])
V113next = F(saved113['certificates'][1]['value'])
D113 = u113[0]+2*V113next-3*V113
increment113 = V113next-V113
assert increment113 == F(885147385, 10233939282) > 0
assert -D113/increment113 == F(3426993456, 885147385)

# Current endpoints/evidence, against the five final edge files. No work.py/Git.
registry = json.loads((ROOT/'research/registry.json').read_text())
objects = {v['object_id']: v for v in registry['objects']}
sha = lambda data: hashlib.sha256(data).hexdigest()
pins = {oid: sha(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        for oid, obj in objects.items()}
edge_dirs = [ROOT/'map/edges'/d for d in ('boss3-fixed-q-background-3a-5cb2a2ccf4c1dd62', 'customer-attraction-3a-3a-8ee01d9bcec0bab9')]
edge_checks = []
for directory in edge_dirs:
    for p in sorted(directory.glob('*.json')):
        e = json.loads(p.read_text())
        assert all(pins[k] == v for k, v in e['endpoint_pins'].items())
        assert all(sha((ROOT/k).read_bytes()) == v for k, v in e['evidence_pins'].items())
        edge_checks.append(dict(edge_id=e['edge_id'], kind=e['kind'],
                                endpoint_pins=e['endpoint_pins'], evidence_pins=e['evidence_pins']))
assert len(edge_checks) == 5
task_checks = []
for d in ('boss3-fixed-q-background-3a-5cb2a2ccf4c1dd62', 'customer-attraction-3a-3a-8ee01d9bcec0bab9'):
    task = json.loads((ROOT/'research/operations/map-v2/tasks'/f'{d}.json').read_text())
    assert all(pins[k] == v for k,v in task['definition']['input_pins'].items())
    task_checks.append(dict(task_id=d, input_pins=task['definition']['input_pins']))

result = dict(polynomial_positive_coefficients=positive_by_degree, polynomial_rows=poly_rows,
              old_query1_mask2_numerator=list(map(str, old_bad_num)), old_zero_residuals_match_frozen=True,
              negative_discovery_float_entries=len(negative_float), main_orbit_table=table,
              all_root_terminal_count=len(root_outcomes), spectra=[dict(loads=k, count=v) for k,v in sorted(spectra.items())],
              full_policy_audits=audits, current_edge_checks=edge_checks, current_task_checks=task_checks,
              root113=dict(IC_comparisons=258, IC_ties=ties113, u=list(map(str,u113)),
                           fixed_Q_query_caps=list(map(str,q113)), V=str(V113), Vnext=str(V113next),
                           D1=str(D113), increment=str(increment113), finite_slope_threshold=str(-D113/increment113),
                           saved_saddle_certificates_independently_verified=3))
(OUT/'exact-comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('polynomial_rows', 'current_edge_checks', 'current_task_checks')}, ensure_ascii=False, indent=2))
