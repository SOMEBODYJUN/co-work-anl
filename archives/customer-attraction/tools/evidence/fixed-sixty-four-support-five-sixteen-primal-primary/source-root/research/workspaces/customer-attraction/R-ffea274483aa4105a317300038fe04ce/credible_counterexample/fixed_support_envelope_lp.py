"""Fixed 64-atom support only: original 437 + 10 known + 69 cross rows.
Floating LP proposes a point; Fraction recovery certifies every reported primal.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('older_closure',ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.py')
new=load('new_coupling',HERE/'coupling_envelope_check.py')

columns=[]
for atom in new.atoms:
    bits=tuple(map(int,atom['bits']));hist=[atom[field] for field in ('AB_hist','AE_hist','second_hist')]
    rows=old.namespace['evaluate'](bits,hist,atom['menus_lh'],include_second_correlations=True)
    assert len(rows)==437
    rows.update(old.module.rows(atom));assert len(rows)==447
    env=new.rows(atom);rows.update({'cross_envelope:'+k:v for k,v in env.items()})
    # All 25 (i,j) cross-menu comparisons, without dropping diagonal terms.
    for g in ('AB','AE','second'):
        own,inv=new.source_terms(atom,g);iv=sum(inv[0]+inv[1],F(0))
        for target,counts in new.target_counts(atom).items():
            if target.startswith(g+'_'):continue
            rows['cross_full:'+g+':'+target]=5*own-sum(counts)*iv
    columns.append(rows)
names=tuple(columns[0]);G=np.array([[c[name] for c in columns] for name in names],dtype=object)
w=np.array([int(any(int(b) for b in atom['bits'][:5])) for atom in new.atoms],dtype=object)
obj=np.array([int(sum(n*t[0] for n,t in zip(atom['AB_hist'],new.triples))>0) for atom in new.atoms],dtype=object)
floatG=np.array(G,dtype=float)
res=linprog(-np.array(obj,dtype=float),A_ub=-floatG,b_ub=np.zeros(len(names)),A_eq=[np.array(w,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
assert res.success,res.message
report={'scope':'Only the frozen 64 customer-atom support; 437 original + 10 known intra-family offdiag + 23 cross full + 46 cross envelope rows','universal_claim':False,'rows':len(names),'floating_optimum':float(-res.fun)}
active=np.abs(floatG@res.x)<1e-7
A=np.concatenate([w[None,:],G[active]]);b=[1]+[0]*int(sum(active))
primal=old.recover(A,b,res.x)
if primal is not None:
    assert min(primal)>=0 and sum(x*y for x,y in zip(w,primal))==1
    slacks=[sum(G[i,j]*primal[j] for j in range(len(primal))) for i in range(len(names))]
    assert min(slacks)>=0
    value=sum(x*y for x,y in zip(obj,primal))
    report.update({'exact_primal_value':str(value),'exact_primal_float':float(value),'gap_above_two':str(value-2),'nonzero_masses':sum(x>0 for x in primal),'minimum_slack':str(min(slacks)),'exact_reweighting':[str(x) for x in primal],'new_row_slacks':{name:str(v) for name,v in zip(names,slacks) if name.startswith('cross_')}})
# A directly recovered rational dual is included only if every inequality passes.
beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**9)
dual=[F(float(-x)).limit_denominator(10**9) for x in res.ineqlin.marginals]
residual=[beta*w[j]-sum(mu*G[i,j] for i,mu in enumerate(dual))-obj[j] for j in range(len(new.atoms))]
if min(dual)>=0 and min(residual)>=0:
    report.update({'exact_dual_bound':str(beta),'exact_dual':{name:str(v) for name,v in zip(names,dual) if v},'minimum_dual_residual':str(min(residual)),'exact_optimality_verified':primal is not None and beta==value})
else:report['exact_optimality_verified']=False
HERE.joinpath('fixed_support_envelope_lp.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('exact_reweighting','new_row_slacks','exact_dual')},indent=2))
