"""Independent exact arithmetic and original-facility cost audit.

Finite enumeration is implementation evidence, not a proof of a universal
theorem or of polynomial equilibrium search. Existing reports are immutable.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from multi_facility_spe.complement_reduction import compile_game, decode_ne, to_bounded_complement
from multi_facility_spe.two_exists import Instance
from multi_facility_spe.greedy_box import canonical_greedy, construct_on_path, verify_on_path

counts = dict(compilations=0, assignments=0, deviations=0, source_ne=0,
              greedy_comparisons=0, trajectory_comparisons=0,
              strict_steps=0, band_inputs=0, band_states=0,
              physical_conditional_cost_comparisons=0)
rng = random.Random(20261008)

def source_load(q, B, u, A, a):
    return [B[t] + sum((u[i] for i in range(len(u)) if t in A[i] and a[i] != t), F(0))
            for t in range(len(q))]

def source_cost(i, q, B, u, A, a):
    Y = source_load(q, B, u, A, a)
    return sum((Y[t] / q[t] for t in A[i] if t != a[i]), F(0))

def target_cost(i, q, private, w, a, target=None):
    # Independently choose facilities uniformly at the selected site; include self.
    t = a[i] if target is None else target
    other = private[t] + sum((w[j] for j in range(len(w)) if j != i and a[j] == t), F(0))
    return w[i] + other / q[t]

def physical_cost_audit(p, a, q, private, w):
    """Derive conditional costs from every labeled facility distribution."""
    layout = p['greedy']['layout']
    all_weights = tuple(F(x) for x in p['target']['weights'])
    m, n = len(q), len(w)
    site_assignment = tuple(a) + tuple(range(m)) + (m,)
    multiplicity = tuple(q) + (1,)
    probability = [tuple(F(1, multiplicity[s]) if t == s else F(0)
                         for t in layout) for s in site_assignment]
    for i, s in enumerate(site_assignment):
        current = sum((probability[i][f] *
                      (all_weights[i] + sum((all_weights[j]*probability[j][f]
                       for j in range(len(all_weights)) if j != i and probability[j][f]),F(0)))
                       for f in range(len(layout)) if probability[i][f]),F(0))
        for f,t in enumerate(layout):
            if t not in p['target']['A'][i]:
                continue
            conditional = all_weights[i] + sum((all_weights[j]*probability[j][f]
                          for j in range(len(all_weights)) if j != i and probability[j][f]),F(0))
            counts['physical_conditional_cost_comparisons'] += 1
            if i < n:
                assert conditional == target_cost(i,q,private,w,a,t)
                assert current == target_cost(i,q,private,w,a)
            else:
                assert conditional == current  # private customers' all facilities are equal

def source_rule(q, B, u, A, initial):
    a = list(initial)
    priority = sorted(range(len(u)), key=lambda i: (-max(q[t] for t in A[i]), -u[i], i))
    seen, steps = {tuple(a)}, 0
    while True:
        changed = False
        for i in priority:
            candidates = []
            current = source_cost(i, q, B, u, A, a)
            for t in A[i]:
                nxt = a.copy()
                nxt[i] = t
                candidates.append((source_cost(i, q, B, u, A, nxt), t))
            best, t = min(candidates)
            if best < current:
                a[i] = t
                assert tuple(a) not in seen
                seen.add(tuple(a))
                steps += 1
                changed = True
                break
        if not changed:
            return tuple(a), steps

def audit_source(q, B, u, A, eta, reverse):
    p = compile_game(q, B, u, A, eta, reverse_ties=reverse)
    counts['compilations'] += 1
    n, m = len(u), len(q)
    d, M = F(p['delta']), F(p['M'])
    w = tuple(F(x) for x in p['target']['weights'][:n])
    private = tuple(F(x) for x in p['target']['weights'][n:n+m])
    initial = tuple(p['greedy']['owners'][:n])
    mapping = p['abstract_to_source_site']
    invmap = {old: new for new, old in enumerate(mapping)}
    assert all(q[initial[i]] == max(q[t] for t in A[i]) for i in range(n))
    assert sorted(range(n), key=lambda i: ((1-w[i])/q[initial[i]], i)) == sorted(
        range(n), key=lambda i: (-max(q[t] for t in A[i]), -u[i], i))
    K = [sum((u[i]**2 for i in range(n) if t in A[i]), F(0)) for t in range(m)]
    Ytotal = sum(B, F(0)) + sum(((len(A[i])-1)*u[i] for i in range(n)), F(0))
    const = M*M*sum(q)/2 - M*Ytotal - sum((K[t]/(2*q[t]) for t in range(m)), F(0))
    for a in product(*A):
        counts['assignments'] += 1
        physical_cost_audit(p,a,q,private,w)
        Y = source_load(q, B, u, A, a)
        W = [private[t] + sum((w[i] for i in range(n) if a[i] == t), F(0)) for t in range(m)]
        X = [W[t]-q[t] for t in range(m)]
        assert all(X[t] == d*(q[t]*M-Y[t]) for t in range(m))
        assert all(d <= x <= F(1,2) for x in X)
        assert all((X[a[i]]-w[i])/q[a[i]] < (1-w[i])/q[initial[i]] for i in range(n))
        psi = sum(((Y[t]**2 + sum((u[i]**2 for i in range(n)
                   if t in A[i] and a[i] != t), F(0)))/(2*q[t]) for t in range(m)), F(0))
        phi = sum(((X[t]**2 - sum((w[i]**2 for i in range(n) if a[i] == t), F(0)))
                   /(2*q[t]) for t in range(m)), F(0))
        assert phi == d*d*(psi+const)
        sne = tne = True
        for i, s in enumerate(a):
            for t in A[i]:
                if t == s:
                    continue
                counts['deviations'] += 1
                nxt = list(a)
                nxt[i] = t
                sd = source_cost(i, q, B, u, A, nxt)-source_cost(i, q, B, u, A, a)
                td = target_cost(i, q, private, w, a, t)-target_cost(i, q, private, w, a)
                assert td == d*sd
                sne &= sd >= 0
                tne &= td >= 0
        assert sne == tne
        aa = [invmap[t] for t in a]
        if sne:
            counts['source_ne'] += 1
            assert decode_ne(p, aa) == list(a)
        else:
            try:
                decode_ne(p, aa)
            except ValueError:
                pass
            else:
                raise AssertionError('Decoder accepted a non-NE')
    if not reverse:
        inst = Instance(tuple(F(x) for x in p['target']['weights']),
                        tuple(frozenset(x) for x in p['target']['A']), m+1, p['target']['k'])
        layout, home, gamma, opening = canonical_greedy(inst)
        assert layout == tuple(p['greedy']['layout'])
        assert home == tuple(p['greedy']['owners'])
        assert gamma == 1 and opening == tuple(mapping)
        counts['greedy_comparisons'] += 1
        if n <= 5:
            layout2, assignment, audit = construct_on_path(inst)
            verify_on_path(inst, layout2, assignment)
            result, steps = source_rule(q, B, u, A, initial)
            assert tuple(assignment[:n]) == result
            assert audit['home_returns'] == 0 and audit['strict_improvements'] == steps
            counts['trajectory_comparisons'] += 1
            counts['strict_steps'] += steps

cases = [
    ([1], [F(0)], [], [], F(1,2)),
    ([3,1,2], [F(0),F(7,5),F(20)], [F(1,3),F(17),F(3,2)],
     [(0,1),(0,1,2),(2,)], F(1,2)),
    ([2,2], [F(0),F(0)], [F(1,2),F(3,4)], [(0,1),(0,1)], F(1,2)),
    ([2,1], [F(1,2**80),F(2**80)], [F(1,2**100),F(2**90),F(7,9)],
     [(0,1),(0,1),(0,1)], F(1,2**70)),
]
for _ in range(220):
    m = rng.randint(1,4)
    n = rng.randint(0,5)
    q = [rng.randint(1,3) for _ in range(m)]
    B = [F(rng.randint(0,8), rng.randint(1,5)) for _ in range(m)]
    u = [F(rng.randint(1,10), rng.randint(1,7)) for _ in range(n)]
    A = [tuple(sorted(rng.sample(range(m), rng.randint(1,m)))) for _ in range(n)]
    cases.append((q,B,u,A,rng.choice([F(1,2),F(1,7),F(1,101)])))
for q,B,u,A,eta in cases:
    for reverse in (False, True):
        audit_source(q,B,u,A,eta,reverse)

counterexample = None
for _ in range(700):
    m = rng.randint(2,4)
    n = rng.randint(1,5)
    q = sorted([rng.randint(1,3) for _ in range(m)], reverse=True)
    c = [rng.choice([F(0),F(1,4),F(1,2),F(3,4),F(1)]) for _ in range(m)]
    w = [rng.choice([F(1,4),F(1,2),F(3,4),F(2,3)]) for _ in range(n)]
    A = [tuple(sorted(rng.sample(range(m),rng.randint(1,m)))) for _ in range(n)]
    transformed = to_bounded_complement(q,c,w,A)
    B = [F(x) for x in transformed['source']['B']]
    M = F(transformed['M'])
    h = [row[0] for row in A]
    counts['band_inputs'] += 1
    for a in product(*A):
        counts['band_states'] += 1
        X = [c[t] + sum((w[i] for i in range(n) if a[i] == t),F(0))
             - sum((w[i] for i in range(n) if h[i] == t),F(0)) for t in range(m)]
        Y = source_load(q,B,w,A,a)
        assert all(Y[t] == q[t]*M-X[t] for t in range(m))
        assert all(0 <= x <= 1 for x in X) == all(q[t]*M-1 <= Y[t] <= q[t]*M for t in range(m))
        sne = True
        for i,s in enumerate(a):
            for t in A[i]:
                if s == t:
                    continue
                nxt = list(a)
                nxt[i] = t
                sd = source_cost(i,q,B,w,A,nxt)-source_cost(i,q,B,w,A,a)
                assert sd == X[t]/q[t]-(X[s]-w[i])/q[s]
                sne &= sd >= 0
        if sne and any(not 0 <= x <= 1 for x in X) and counterexample is None:
            counterexample = dict(q=q,c=list(map(str,c)),w=list(map(str,w)),A=A,
                                  a=a,X=list(map(str,X)),B=list(map(str,B)),M=str(M))

tiny = json.loads((ROOT/'examples/multi_facility/bounded_complement_outside_box.json').read_text())
q,c,w,A = tiny['q'],list(map(F,tiny['c'])),list(map(F,tiny['w'])),tiny['A']
a = tiny['outside_box_ne']
X = [c[t]+sum((w[i] for i in range(len(w)) if a[i]==t),F(0))
     -sum((w[i] for i in range(len(w)) if min(A[i])==t),F(0)) for t in range(len(q))]
assert X == [F(-1,4),F(1,4),F(3,4)]
assert all((X[a[i]]-w[i])/q[a[i]] < X[t]/q[t]
           for i in range(len(w)) for t in A[i] if t != a[i])
encoded = to_bounded_complement(q,c,w,A)
Y = source_load(q,list(map(F,encoded['source']['B'])),w,A,a)
assert Y == [F(9,4),F(7,4),F(5,4)]
assert Y[0] > F(encoded['upper_load'][0])

large = to_bounded_complement([2**80,1],[F(1,2),F(0)],[F(1,3)],[(0,1)])
assert len(large['source']['q']) == 2  # no expansion of a binary speed

paths = ['multi_facility_spe/complement_reduction.py',
         'multi_facility_spe/equal_light_flow.py',
         'tests/audits/kfac_complement_reduction.py',
         'tests/test_complement_reduction.py',
         'examples/multi_facility/complement_source_two_speed.json',
         'examples/multi_facility/bounded_complement_outside_box.json',
         'history/source/notes/multi_facility/complement_reduction_pro_report_2026-10-08.md']
result = dict(schema_version=1,python_version=platform.python_version(),seed=20261008,
              base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              replay_commands=['python3 tests/audits/kfac_complement_reduction.py'],
              source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
              counts=counts, random_unbounded_ne_outside_box=counterexample,
              minimal_band_boundary=dict(X=list(map(str,X)),Y=list(map(str,Y)),
                                         all_deviations_strictly_worse=True),
              binary_speed_import_bits=81,
              limitations=['Finite checks support the implementation; universal claims rely on the proof.',
                           'No equilibrium oracle, PLS hardness, or polynomial improvement bound is established.',
                           'Canonical code reuses only exact numeric I/O from equal_light_flow; it never calls its optimizer.',
                           'Reverse tie checks use a diagnostic alternative rule; canonical cross-checks use default ties.'])
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args = parser.parse_args()
if args.output:
    if args.output.exists():
        parser.error('Refusing to overwrite frozen evidence; choose a new output')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
