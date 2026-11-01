"""Diagnostic only: lawful background-profit inequalities, not SPE realization.

Symmetrize six comparison labels; columns are (actual 6-bit mask, comparison
degree e). Every query averages over distinct uniformly permuted comparison
labels, with optional repetitions and any actual-action multiset.
"""
from itertools import combinations_with_replacement, combinations, product
from math import comb
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

M = 6
cols = [(a, e) for a in range(64) for e in range(7) if a or e]
bits = np.array([[(a >> i) & 1 for a, e in cols] for i in range(M)])
loads = bits.sum(axis=0)
pay = np.divide(bits, loads, out=np.zeros(bits.shape), where=loads != 0)
covered = (loads > 0).astype(float)
opt = np.array([float(e > 0) for a, e in cols])
rows, names, descriptors = [], [], []

def add(name, lhs, descriptor):
    names.append(name)
    rows.append(lhs)
    descriptors.append(descriptor)

for i in range(M):
    b = bits[:i].sum(axis=0)
    r = M-i
    for j in range(M):
        add(f'safe:{i}:actual:{j}', bits[j] / (b+r) - pay[i],('safe',i,j))
    add(f'safe:{i}:optimal', np.array([e/6 for a,e in cols])/(b+r)-pay[i],('safe',i,None))

def partitions(n, minimum=1):
    if n == 0:
        yield ()
    else:
        for first in range(minimum, n+1):
            for rest in partitions(n-first, first):
                yield (first,) + rest

def opt_hits(e, mult):
    d = len(mult)
    out = {}
    for patt in product((0,1), repeat=d):
        k = sum(patt)
        prob = F(comb(6-d,e-k),comb(6,e)) if 0 <= e-k <= 6-d else F(0)
        hits = sum(v*z for v,z in zip(mult,patt))
        out[hits] = out.get(hits,F(0))+prob
    return out

for r, C in [(2,F(3,2)), (3,F(5,3)), (4,F(1499,750))]:
    cut = M-r
    b = bits[:cut].sum(axis=0)
    tailpay = pay[cut:].sum(axis=0)
    for o in range(r+1):
        for mult in partitions(o):
            distributions = {e: opt_hits(e,mult) for e in range(7)}
            for acts in combinations_with_replacement(range(M),r-o):
                actual = sum((bits[j] for j in acts),start=np.zeros(len(cols)))
                lhs = np.zeros(len(cols))
                for k,(a,e) in enumerate(cols):
                    for hit,prob in distributions[e].items():
                        z = actual[k]+hit
                        lhs[k] += float(prob)*z/(b[k]+z) if z else 0
                add(f'profit:{r}:{acts}:{mult}',lhs-float(C)*tailpay,('profit',r,acts,mult))
                if r == 2:
                    tax = bits[cut]/((b+1)*(b+2))
                    add(f'tax:{acts}:{mult}',lhs-tailpay-tax,('tax',r,acts,mult))

result = linprog(covered, A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                 A_eq=opt.reshape(1,-1), b_eq=[1], bounds=(0,None),
                 method='highs')
print(json.dumps({'status':result.message, 'rows':len(rows), 'cols':len(cols),
                  'min_W':result.fun, 'nonzero':[(cols[i],float(x))
                  for i,x in enumerate(result.x) if x>1e-8]},indent=2))

def exact_coefficient(desc, a, e):
    bit = [(a>>i)&1 for i in range(6)]
    load = sum(bit)
    payoff = [F(z,load) if load else F(0) for z in bit]
    kind = desc[0]
    if kind == 'safe':
        _,i,j = desc
        query = F(e,6) if j is None else F(bit[j])
        return query/(sum(bit[:i])+6-i)-payoff[i]
    _,r,acts,mult = desc
    b = sum(bit[:6-r])
    d = sum(bit[j] for j in acts)
    lhs = sum((prob*F(d+hit,b+d+hit) if d+hit else F(0)
               for hit,prob in opt_hits(e,mult).items()),F(0))
    v = sum(payoff[6-r:])
    if kind == 'profit':
        return lhs-{2:F(3,2),3:F(5,3),4:F(1499,750)}[r]*v
    return lhs-v-F(bit[6-r],(b+1)*(b+2))

if __name__ == '__main__' and '--audit' in __import__('sys').argv:
    from pathlib import Path
    point = {(a,e):F(float(x)).limit_denominator(10**8)
             for (a,e),x in zip(cols,result.x) if x>1e-8}
    slacks = [-sum((mass*exact_coefficient(desc,a,e)
                   for (a,e),mass in point.items()),F(0)) for desc in descriptors]
    assert min(slacks) >= 0
    assert sum(mass for (a,e),mass in point.items() if e) == 1
    exact_w = sum(mass for (a,e),mass in point.items() if a)
    assert exact_w < F(1,2)
    record = {'status':'EXACT_FEASIBLE_RELAXATION_POINT_NOT_SPE',
              'rows':len(rows),'columns':len(cols),'O':'1','W':str(exact_w),
              'ratio_O_over_W':str(1/exact_w),'minimum_slack':str(min(slacks)),
              'point':[{'actual_mask':a,'comparison_degree':e,'mass':str(mass)}
                       for (a,e),mass in point.items()],
              'slacks':[{'name':name,'slack':str(slack)} for name,slack in zip(names,slacks)]}
    path = Path(__file__).with_name('background_profit_relaxation_exact_point.json')
    path.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('point','slacks')},indent=2))

if __name__ == '__main__' and '--solve' in __import__('sys').argv:
    from customer_attraction.model import Instance, CustomerType
    from customer_attraction.exact import ExactSPESolver
    from math import lcm
    import time
    masses = {a:F(float(x)).limit_denominator(10**8)/6
              for (a,e),x in zip(cols,result.x) if x>1e-8}
    den = lcm(*(z.denominator for z in masses.values()))
    inst = Instance(tuple(f'A{i}' for i in range(6))+tuple(f'T{i}' for i in range(6)),
        tuple(CustomerType(frozenset([j+6]+[i for i in range(6) if a>>i&1]),
                           int(mass*den)) for a,mass in masses.items() for j in range(6)),6)
    solver = ExactSPESolver(inst)
    started = time.time()
    worst = solver.minimum_welfare()
    replay = {'status':'REALIZED_CATALOG_COMPLETE_EXACT_SPE_ENUMERATION',
                      'exact_seconds':time.time()-started,'stats':solver.stats.__dict__,
                      'customers':inst.customer_count,'min_W':worst,
                      'ratio':str(F(inst.customer_count,worst)),
                      'worst_counts':list(min(solver.worst_outcomes())),
                      'proposed_path_SPE':(1,1,1,1,1,1,0,0,0,0,0,0) in solver.outcomes()}
    from pathlib import Path
    Path(__file__).with_name('background_profit_realized_instance.json').write_text(json.dumps(inst.to_dict(),indent=2)+'\n')
    Path(__file__).with_name('background_profit_realization_replay.json').write_text(json.dumps(replay,indent=2)+'\n')
    print(json.dumps(replay,indent=2))
