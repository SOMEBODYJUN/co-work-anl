"""Derive exact global-maximum root cuts retaining binary certificate residuals.

The 192 columns are the complete local coefficient universe, not games.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent'
spec = importlib.util.spec_from_file_location('binary_tail_source', SOURCE/'binary_tail_pareto.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
certificate_path = SOURCE/'binary_tail_exact_1999.json'
certificate = json.loads(certificate_path.read_text())
weights = {name:F(value) for name,value in certificate['multipliers'].items()}
A, B = F(1999,1000), F(5,3)


def quotient(n,d):
    return F(n,d) if n else F(0)


rho = {}
for t, tail, e in product(range(2), product(range(2),repeat=4), range(5)):
    values = []
    for auxiliary in product(range(2),repeat=3):
        names,rows,target,V = module.coefficients(t,tail+auxiliary,e)
        value = (B if t else A)*V-target-sum(weights.get(name,0)*row for name,row in zip(names,rows))
        assert value >= 0
        values.append(value)
    rho[t,tail,e] = min(values)

states = list(product(range(2),product(range(2),repeat=4),range(6)))
feature_names = ['bare0','bare1','bare2','bare3','negative_retained_binary','last_query','root_profit','T_size']
features, objectives = [], []
for t,tail,j in states:
    n = sum(tail)
    V = quotient(n,t+n)
    z = quotient(t,t+n)
    target,credit = F(0),F(0)
    for included in range(2):
        count = j if included else 5-j
        if not count:
            continue
        e = j-included
        target += F(count,5)*quotient(e,t+e)
        credit += F(count,5)*rho[t,tail,e]
    base = (B if t else A)*V-target-credit
    last = quotient(j,t+sum(tail[:3])+1)-5*quotient(tail[3],t+n)
    features.append(list(map(F,tail))+[-base,last,z,F(t)])
    objectives.append(F(int(j>0)))


def solve_exact(matrix, rhs):
    work = [list(row)+[b] for row,b in zip(matrix,rhs)]
    size = len(work)
    for c in range(size):
        pivot = next(r for r in range(c,size) if work[r][c])
        work[c],work[pivot] = work[pivot],work[c]
        q = work[c][c]
        work[c] = [v/q for v in work[c]]
        for r in range(size):
            if r != c and work[r][c]:
                q = work[r][c]
                work[r] = [x-q*y for x,y in zip(work[r],work[c])]
    return [row[-1] for row in work]


def exact_cut(ratio):
    array = np.array(features,dtype=float)
    result = linprog(-np.array(objectives,dtype=float),
                     A_ub=array[:,:7].T,b_ub=[1]*4+[0,0,float(ratio)],
                     A_eq=array[:,7:].T,b_eq=[1],bounds=(0,None),method='highs')
    assert result.success
    dual_float = -np.concatenate((result.ineqlin.marginals,result.eqlin.marginals))
    support = [i for i,value in enumerate(dual_float) if abs(value)>1e-8]
    residual = array@dual_float-np.array(objectives,dtype=float)
    active = np.flatnonzero(abs(residual)<1e-8)
    _,_,pivots = qr(array[active][:,support].T,pivoting=True)
    selected = active[pivots[:len(support)]]
    solution = solve_exact([[features[i][j] for j in support] for i in selected],
                           [objectives[i] for i in selected])
    dual = [F(0)]*len(feature_names)
    for i,value in zip(support,solution):
        dual[i] = value
    assert all(v>=0 for v in dual[:7])
    residuals = [sum(x*y for x,y in zip(row,dual))-obj for row,obj in zip(features,objectives)]
    assert min(residuals)>=0
    root_coefficient = dual[6]
    size_coefficient = sum(dual[:4])+dual[7]
    return {'ratio_for_basis':str(ratio),
            'multipliers':{name:str(value) for name,value in zip(feature_names,dual) if value},
            'row':{'O':1,'root_u':str(root_coefficient),'K':str(size_coefficient)},
            'minimum_residual':str(min(residuals)),
            'zero_residuals':sum(v==0 for v in residuals),
            'selected_types':[[states[i][0],list(states[i][1]),states[i][2]] for i in selected]}


if __name__ == '__main__':
    report = {'scope':'all 192 local coefficient types; not finite SPE enumeration',
              'binary_source':str(certificate_path.relative_to(ROOT)),
              'binary_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
              'rho_types':len(rho),'universe_size':len(states),
              'cuts':[exact_cut(F(11,50)),exact_cut(F(13,50))]}
    target = HERE/'retained_binary_capacity_certificate.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
