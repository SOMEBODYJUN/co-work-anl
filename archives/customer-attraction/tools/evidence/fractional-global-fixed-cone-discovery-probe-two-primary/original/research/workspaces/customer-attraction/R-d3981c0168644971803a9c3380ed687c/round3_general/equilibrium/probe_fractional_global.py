"""Targeted falsification of the all-p fractional *global* payment.

Uses exactly the already certified 36-customer formal strategy and its known
bad integer-decorrelation p=(X2+Y2)/2; varies customer multiplicities over its
full strategy cone. Numerical LP proposes a witness; exact checking is separate.
This is not an enumeration of games or a proof of a universal inequality.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
cert = json.loads((ROOT/'evidence/certificates/customer_attraction/aggregate_theta_failure.json').read_text())
policy = {tuple(a['history']): a['action'] for a in cert['strategy']['actions']}
m, k = 3, 6
types = list(range(1,1<<k))
p = [F(int(a in (2,5)),2) for a in range(k)]

def leaf(history):
    h=list(history)
    while len(h)<m: h.append(policy[tuple(h)])
    return tuple(h)

def load(mask, profile): return sum((mask>>a)&1 for a in profile)
def utility(mask, profile, i):
    return F((mask>>profile[i])&1,load(mask,profile)) if load(mask,profile) else F(0)

z=leaf(())
gamma=[]
for depth in range(m):
    for h in product(range(k),repeat=depth):
        actual=leaf(h)
        for a in range(k):
            alt=leaf(h+(a,))
            gamma.append([utility(mask,actual,depth)-utility(mask,alt,depth) for mask in types])

fractional=[]
for mask in types:
    px=sum(p[a] for a in range(k) if (mask>>a)&1)
    val=F(0)
    for i in range(m):
        mu=F(0)
        for a in range(k):
            y=leaf(z[:i]+(a,)); B=y[:i]+y[i+1:]
            mu+=p[a]*load(mask,B)
        val+=px/(1+mu)
    fractional.append(val)
welfare=[F(bool(load(mask,z))) for mask in types]
gap=[a-b for a,b in zip(fractional,welfare)]
res=linprog(-np.array(list(map(float,gap))),A_ub=-np.array(gamma,dtype=float),b_ub=np.zeros(len(gamma)),A_eq=np.ones((1,len(types))),b_eq=[1.],bounds=(0,None),method='highs')
report={'candidate':'all-p fractional global payment sum_i F_i(p)<=W', 'fixed_strategy_source':'aggregate_theta_failure.json', 'p':list(map(str,p)), 'status':res.message}
if res.success:
    report['numerical_max_gap']=-res.fun
    proposed={mask:F(float(x)).limit_denominator(10**6) for mask,x in zip(types,res.x) if x>1e-9}
    den=1
    from math import lcm,gcd
    from functools import reduce
    for w in proposed.values(): den=lcm(den,w.denominator)
    counts={mask:int(w*den) for mask,w in proposed.items()}
    common=reduce(gcd,counts.values())
    counts={mask:w//common for mask,w in counts.items()}
    exact_gap=sum(g*w for g,w in zip(gap,[counts.get(mask,0) for mask in types]))
    min_ic=min(sum(g*w for g,w in zip(row,[counts.get(mask,0) for mask in types])) for row in gamma)
    report.update(counts=counts,exact_gap=str(exact_gap),minimum_exact_ic=str(min_ic),unit_customers=sum(counts.values()),exact_witness=bool(exact_gap>0 and min_ic>=0))
(OUT/'fractional_global_probe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
