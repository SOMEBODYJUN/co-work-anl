"""One targeted exact check of the saved 61-atom, 717-row point.

Reuse only the canonical old 437-row function prefix. Rebuild all added
10+110+160 coefficients here from literal index sums. Do not import or run
an old CLI, optimizer, column pricer, joint transport or full-game solver.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import Counter
import ast, hashlib, json

E = Path(__file__).resolve().parent
OUT = E / 'fixed-61-exact-check.json'
if OUT.exists():
    raise SystemExit('Successful check already exists; no repeated execution')
REPO = next(p for p in E.parents if (p / 'cleanup/OBJECTS.md').exists())
P = E / 'original/exact_primal_cross_pair.json'
assert hashlib.sha256(P.read_bytes()).hexdigest() == '7d58f6ca319c527bfd7b2922fb1178759a08c8e2cffdfa5a799d534704711197'
doc = json.loads(P.read_text())
old = REPO / 'archives/customer-attraction/tools/evidence/five-player-indexed/tests/audits/customer_attraction_five_indexed.py'
tree = ast.parse(old.read_text())
nodes = []
for node in tree.body:
    if isinstance(node, ast.ImportFrom) and node.module == 'pathlib':
        break
    nodes.append(node)
ns = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(old), 'exec'), ns)
SPEC = [('AB', 'AB_hist', 3, (0, 1)), ('AE', 'AE_hist', 3, (0, 4)),
        ('Sbranch', 'second_hist', 4, (0,))]
ORB = ['all_equal', 'query_equal', 'first_branch', 'second_branch', 'all_distinct']

def unpack(a):
    bits = tuple(map(int, a['bits']))
    assert len(bits) == 10 and all(v in (0, 1) for v in bits)
    groups = {}
    for tag, field, arity, fixed in SPEC:
        h = a[field]
        assert len(h) == 2**arity and all(type(v) is int and v >= 0 for v in h) and sum(h) == 5
        groups[tag] = [t for t, n in zip(product((0, 1), repeat=arity), h) for _ in range(n)]
    ds = [sum(t[0] for t in g) for g in groups.values()]
    assert len(set(ds)) == 1
    d = ds[0]
    assert len(a['menus_lh']) == 3
    for pair in a['menus_lh']:
        assert len(pair) == 2 and all(type(v) is int for v in pair)
        l, h = pair
        assert 0 <= h <= d and 0 <= l-h <= 5-d
    return bits, groups, d

def pattern(i, j, k):
    return 0 if i == j == k else 1 if j == k else 2 if i == j else 3 if i == k else 4

def literal_pairs(p, H, target, u, v):
    z = [F(0)] * 5
    for i, j, k in product(range(5), repeat=3):
        b, c = target[j][u], target[k][v]
        z[pattern(i, j, k)] += H[i] - F(b+c, p[i]+1) + F(b*c, (p[i]+1)*(p[i]+2))
    return z

allslack = {n: F(0) for n in doc['slacks']}
W = O = F(0)
domains = Counter()
atom_summary = []
for ai, a in enumerate(doc['atoms']):
    bits, groups, d = unpack(a)
    mass = F(a['exact_mass'])
    assert mass > 0
    rr = ns['evaluate'](bits, [a['AB_hist'], a['AE_hist'], a['second_hist']], a['menus_lh'], True)
    assert len(rr) == 437
    backgrounds, holds = {}, {}
    for tag, field, arity, fixed in SPEC:
        g = groups[tag]
        prefix = sum(bits[j] for j in fixed)
        p = [prefix + sum(t[:-2]) for t in g]
        H = [(F(t[-2]+t[-1], pp+t[-2]+t[-1]) if t[-2]+t[-1] else F(0))
             + F(t[-2], (pp+1)*(pp+2)) for t, pp in zip(g, p)]
        backgrounds[tag], holds[tag] = p, H
        lastp = [prefix + sum(t[:-1]) for t in g]
        for u in range(arity):
            rr[f'{tag}:5:offdiag:{u}'] = sum((F(g[i][-1]-g[j][u], lastp[i]+1)
                for i, j in product(range(5), repeat=2) if i != j), F(0))
        for u, v in combinations_with_replacement(range(arity), 2):
            for name, value in zip(ORB, literal_pairs(p, H, g, u, v)):
                rr[f'{tag}:pair:{u}{v}:{name}'] = value
    assert len(rr) == 557
    for source in ('AB', 'AE'):
        p, H = backgrounds[source], holds[source]
        # Both lexicographic expansions are grouped by the shared first bit.
        # All p within each such group are equal, so this literal pairing
        # has the same cost as every anchor-preserving pairing.
        for target, _, arity, _ in SPEC:
            if source == target:
                continue
            g = groups[target]
            assert [t[0] for t in groups[source]] == [t[0] for t in g]
            assert all(p[i] == p[j] for i, j in product(range(5), repeat=2)
                       if g[i][0] == g[j][0])
            for u, v in combinations_with_replacement(range(arity), 2):
                for name, value in zip(ORB, literal_pairs(p, H, g, u, v)):
                    rr[f'crosspair:{source}:{target}:{u}{v}:{name}'] = value
    assert len(rr) == 717 and set(rr) == set(allslack)
    for name in allslack:
        allslack[name] += mass * rr[name]
    covered = int(any(bits[:5]))
    W += mass * covered
    O += mass * int(d > 0)
    domains[d, covered] += 1
    atom_summary.append({'index': ai, 'd': d, 'actual_cover': covered, 'mass': str(mass)})
assert len(doc['atoms']) == doc['positive_atoms'] == 61
assert W == F(doc['welfare']) == 1 and O == F(doc['comparison_cover']) > 2
assert O-2 == F(doc['gap_above_two'])
assert min(allslack.values()) == F(doc['minimum_primal_slack']) == 0
assert all(F(doc['slacks'][name]) == value for name, value in allslack.items())
report = {
    'scope': 'Saved 61-atom 717-row necessary-condition point only; no SPE, true OPT or universal 717 upper bound',
    'input_sha256': hashlib.sha256(P.read_bytes()).hexdigest(),
    'old437_prefix_path': str(old.relative_to(REPO)),
    'old437_prefix_file_sha256': hashlib.sha256(old.read_bytes()).hexdigest(),
    'successful_invocations': 1, 'old_cli_invocations': 0, 'optimizer_invocations': 0,
    'full_universe_price_invocations': 0, 'joint_or_transport_invocations': 0,
    'atoms': 61, 'row_count': 717, 'reused_old_rows': 437,
    'new_literal_terminal_rows': 10, 'new_literal_same_family_rows': 110,
    'new_literal_constant_anchor_cross_rows': 160,
    'literal_terminal_terms': 61*10*20, 'literal_pair_terms': 61*(110+160)*125//5,
    'welfare': str(W), 'comparison_cover': str(O), 'gap_above_two': str(O-2),
    'minimum_slack': str(min(allslack.values())), 'negative_rows': 0,
    'zero_rows': [n for n, v in allslack.items() if not v],
    'all_saved_slacks_match': True,
    'atom_domains': {str(k): v for k, v in sorted(domains.items())},
    'atom_summary': atom_summary, 'slacks': {n: str(v) for n, v in allslack.items()}}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('slacks', 'atom_summary', 'zero_rows')}, ensure_ascii=False, indent=2))
