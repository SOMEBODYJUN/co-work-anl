"""Can reweighting the old 64 atom support survive terminal completion rows?

This tests a fixed atom support only. A support-wide exact dual is stronger than
excluding the old single frozen mass vector, but is not a general theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
source=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
audit=ROOT/'tests/audits/customer_attraction_five_indexed.py'
namespace={}
# The row functions have no external dependencies or heavy all-type enumeration.
exec(audit.read_text().split('\nfrom pathlib import Path\nfrom collections')[0],namespace)
old=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/continuation_completion/offdiagonal_closure.py'
spec=importlib.util.spec_from_file_location('frozen_closure_source',old)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def recover(A,b,x):
    n=A.shape[1];support=np.flatnonzero(x>1e-8)
    basis={}
    for row,rhs in zip(A,b):
        v=[F(row[j]) for j in support]+[F(rhs)]
        for pivot in sorted(basis):
            a=v[pivot]
            if a:v=[a1-a*a2 for a1,a2 in zip(v,basis[pivot])]
        pivot=next((j for j,a in enumerate(v[:-1]) if a),None)
        if pivot is not None:
            a=v[pivot];basis[pivot]=[a1/a for a1 in v]
        elif v[-1]:return None
        if len(basis)==len(support):break
    if len(basis)!=len(support):return None
    v=[F(0)]*len(support)
    for pivot in sorted(basis,reverse=True):
        row=basis[pivot];v[pivot]=row[-1]-sum(row[j]*v[j] for j in range(pivot+1,len(support)))
    out=[F(0)]*n
    for j,a in zip(support,v):out[int(j)]=a
    return out


def main():
    atoms=json.loads(source.read_text())['primal']['atoms'];columns=[]
    for atom in atoms:
        bits=tuple(map(int,atom['bits']))
        hist=[atom[field] for field in ('AB_hist','AE_hist','second_hist')]
        rows=namespace['evaluate'](bits,hist,atom['menus_lh'],include_second_correlations=True)
        assert len(rows)==437
        closure=module.rows(atom)
        assert closure==module.rows(atom,direct=True)
        rows.update(closure);columns.append(rows)
    names=tuple(columns[0]);G=np.array([[c[name] for c in columns] for name in names],dtype=object)
    w=np.array([int(any(int(b) for b in atom['bits'][:5])) for atom in atoms],dtype=object)
    objective=np.array([int(sum(n*t[0] for n,t in zip(atom['AB_hist'],namespace['types']))>0)
                        for atom in atoms],dtype=object)
    floatG=np.array(G,dtype=float)
    result=linprog(-np.array(objective,dtype=float),A_ub=-floatG,b_ub=np.zeros(len(names)),
                   A_eq=[np.array(w,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
    report={'scope':'fixed old 64-atom support with all 437 old rows plus 10 terminal offdiagonal rows',
            'universal_bound_proved':False,'floating_optimum':float(-result.fun)}
    beta=F(float(-result.eqlin.marginals[0])).limit_denominator(10**9)
    dual=[F(float(-x)).limit_denominator(10**9) for x in result.ineqlin.marginals]
    residual=[beta*w[j]-sum(mu*G[i,j] for i,mu in enumerate(dual))-objective[j]
              for j in range(len(atoms))]
    if all(mu>=0 for mu in dual) and all(x>=0 for x in residual):
        report.update({'exact_upper_bound':str(beta),'exact_dual':{name:str(mu) for name,mu in zip(names,dual) if mu},
                       'minimum_dual_residual':str(min(residual))})
    active=np.abs(floatG@result.x)<1e-7
    A=np.concatenate([w[None,:],G[active]]);b=[1]+[0]*int(sum(active))
    primal=recover(A,b,result.x)
    if primal is not None and min(primal)>=0 and sum(w[j]*primal[j] for j in range(len(atoms)))==1:
        slacks=[sum(G[i,j]*primal[j] for j in range(len(atoms))) for i in range(len(names))]
        assert min(slacks)>=0
        value=sum(objective[j]*primal[j] for j in range(len(atoms)))
        report.update({'exact_primal_value':str(value),'exact_reweighting':[str(x) for x in primal],
                       'exact_optimality_verified':str(value)==report.get('exact_upper_bound')})
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
