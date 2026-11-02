"""One fixed complete policy, arbitrary customer types: direct Mpath attack.

The tested claim is Mpath <= W/m, including every actual-prefix action column.
LP success requires independent rational recovery and full IC verification;
LP failure is not a mathematical certificate of the tested claim.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import math
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json'
OUT = Path(__file__).with_suffix('.json')
d = json.loads(SOURCE.read_text())
nodes = d['nodes']
m = d['instance']['players']
k = len(d['instance']['topics'])
types = list(range(1, 1 << k))
membership = np.array([[(B >> a) & 1 for a in range(k)] for B in types], dtype=np.int64)
L = math.lcm(*range(1, m + 2))

def uc(a, q):
    loads = membership @ np.array(q)
    out = np.zeros(len(types), dtype=np.int64)
    hit = membership[:, a].astype(bool)
    assert np.all(loads[hit] > 0)
    out[hit] = L // loads[hit]
    return out

rows = {}
reachable = set()
todo = [d['root']]
while todo:
    ni = todo.pop()
    if ni in reachable:
        continue
    reachable.add(ni)
    v = nodes[ni]
    if sum(v['counts']) == m:
        assert v['target'] == v['counts'] and v['action'] is None
        continue
    a = v['action']
    assert len(v['children']) == k
    assert nodes[v['children'][a]]['target'] == v['target']
    prescribed = uc(a, v['target'])
    for b, ci in enumerate(v['children']):
        child = nodes[ci]
        expected = list(v['counts'])
        expected[b] += 1
        assert child['counts'] == expected
        row = prescribed - uc(b, child['target'])
        if np.any(row):
            key = tuple(row)
            rows.setdefault(key, (ni, b))
        todo.append(ci)
assert len(reachable) == len(nodes)
IC = np.array(list(rows), dtype=float) / L

actual_nodes = []
ni = d['root']
while sum(nodes[ni]['counts']) < m:
    actual_nodes.append(ni)
    ni = nodes[ni]['children'][nodes[ni]['action']]
actual = nodes[ni]['target']
covered = (membership @ np.array(actual) > 0).astype(float)
columns = [nodes[ci]['target'] for ni in actual_nodes for ci in nodes[ni]['children']]
column_prices = np.array([1.0 / (1 + membership @ np.array(q)) for q in columns])

def cone_lp(p):
    px = membership @ np.array(p)
    gap = column_prices * px[None, :] - covered[None, :] / m
    A = np.vstack([np.column_stack([-IC, np.zeros(len(IC))]),
                   np.column_stack([-gap, np.ones(len(gap))])])
    res = linprog(np.r_[np.zeros(len(types)), -1.0], A_ub=A,
                  b_ub=np.zeros(len(A)), A_eq=[np.r_[np.ones(len(types)), 0.0]],
                  b_eq=[1.0], bounds=[(0, None)]*len(types)+[(None, None)],
                  method='highs')
    return res

def query_lp(w):
    K = np.array([[float(np.dot(membership[:, a]*w, col)) for col in column_prices] for a in range(k)])
    res = linprog(np.r_[np.zeros(k), -1.0], A_ub=np.column_stack([-K.T, np.ones(len(columns))]),
                  b_ub=np.zeros(len(columns)), A_eq=[np.r_[np.ones(k), 0]], b_eq=[1],
                  bounds=[(0, None)]*k+[(None, None)], method='highs')
    return res

experiments = []
starts = [[F(1, k)]*k, [F(1,4) if a in (2,3,6,7) else F() for a in range(k)]]
best = None
for start_no, p in enumerate(starts):
    # This is a focused bilinear attack of one policy cone, not a policy scan.
    for step in range(3):
        res = cone_lp(p)
        if not res.success:
            experiments.append(dict(start=start_no, step=step, status=res.message))
            break
        w = res.x[:-1]
        gap = float(res.x[-1])
        experiments.append(dict(start=start_no, step=step, p=list(map(str,p)),
                                floating_gap=gap, weight_support=[types[j] for j,x in enumerate(w) if x>1e-8]))
        if best is None or gap > best[0]:
            best = (gap, p, w)
        if gap > 1e-8:
            break
        qr = query_lp(w)
        assert qr.success
        p = [F(float(x)).limit_denominator(1000000) for x in qr.x[:-1]]
        total = sum(p)
        p = [x/total for x in p]
        if p == [F(s) for s in experiments[-1]['p']]:
            break
    if best and best[0] > 1e-8:
        break

gap, p, w = best
report = dict(status='FLOATING_PROPOSAL_ONLY' if gap>1e-8 else 'NO_STRICT_PROPOSAL_FROM_ONE_FIXED_POLICY_CONE',
              tested_claim='Mpath <= W/m', source=str(SOURCE.relative_to(ROOT)),
              players=m, topics=k, dag_nodes=len(nodes), unique_IC_rows=len(IC),
              nonempty_customer_types=len(types), actual_prefix_menu_columns=len(columns),
              experiments=experiments, best_floating_gap=gap,
              warning='Negative numerical result does not prove the cone restriction or the general candidate.')
if gap > 1e-8:
    report['proposal_p'] = list(map(str,p))
    report['proposal_w'] = {str(types[j]):str(F(float(x)).limit_denominator(10**8)) for j,x in enumerate(w) if x>1e-9}
OUT.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
