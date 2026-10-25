"""Exact reweighting of the old four-tail certificate for five-player prefixes.

Only backgrounds p=0,1 are needed; on this domain both old aggregate corrections can be dropped.
Float LP identifies an active system; the certificate is then independently
recovered and checked over the entire 256-state rational coefficient domain.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

names=['K_C','K_D','K_Q','K_R','K_S','E','P','current_IC',
       'Q_query_S','R_query_C','R_query_S','S_query_B']
def div(a,b): return F(a,b) if a else F(0)
def row(p,bits):
    a,b,c,d,q,r,s=bits;k=a+b+c+d;t=d+q+r+s
    u1,u2,u3,u4=[div(z,p+k) for z in (a,b,c,d)]
    v=a+b;w=a+b+c
    D=(p+1)*(p+2)*(p+3)*(p+4)
    delta2=F(1,p+1)-F(1,p+v+1)
    delta3=F(1,p+1)-F(1,p+w+1)
    H=u3+u4+F(c,(p+a+b+1)*(p+a+b+2))
    rr=[u2-F(z,p+a+3) for z in (c,d,q,r,s)]
    rr += [4*u4+delta3,2*H+delta2,u1-div(d,p+t),
           div(q,p+t)-F(s,p+d+3),div(r,p+t)-F(c,p+d+q+2),
           div(r,p+t)-F(s,p+d+q+2),div(s,p+t)-F(b,p+d+q+r+1)]
    return rr,div(k,p+k)


# Complete exact aggregation checks replacing the arbitrary-background corrections.
for p in (0,1):
    for v in range(3):
        for e in range(5):
            pair=F(e*(4-e),3*(p+v+1))+F(e*(e-1),3*(p+v+2))
            tax=F(1,p+1)-F(1,p+v+1)
            assert pair+tax-div(e,p+e)>=0
    for v in range(4):
        for e in range(5):
            tax=F(1,p+1)-F(1,p+v+1)
            assert F(e,p+v+1)+tax-div(e,p+e)>=0
states=[(p,b) for p in (0,1) for b in product((0,1),repeat=7)]
data=[row(*s) for s in states]
constraints=[rr+[-V] for rr,V in data]
eq=[F(0)]*13;eq[5]=eq[6]=F(1)
lp=linprog([0.]*12+[1.],A_ub=np.array(constraints,float),b_ub=np.zeros(256),
           A_eq=[list(map(float,eq))],b_eq=[1.],bounds=(0,None),method='highs')
assert lp.success
active=[eq]+[c for c in constraints if abs(sum(float(v)*x for v,x in zip(c,lp.x)))<1e-8]
basis={};independent=[]
for i,rr in enumerate(active):
    v=list(map(F,rr))
    for pivot,br in sorted(basis.items()):
        factor=v[pivot]
        if factor:v=[a-factor*b for a,b in zip(v,br)]
    pivot=next((j for j,a in enumerate(v) if a),None)
    if pivot is not None:
        v=[a/v[pivot] for a in v];basis[pivot]=v;independent.append(i)
    if len(independent)==13:break
assert len(independent)==13
mat=[list(map(F,active[i]))+[F(i==0)] for i in independent]
for col in range(13):
    pivot=next(i for i in range(col,13) if mat[i][col])
    mat[col],mat[pivot]=mat[pivot],mat[col]
    factor=mat[col][col];mat[col]=[x/factor for x in mat[col]]
    for i in range(13):
        if i!=col and mat[i][col]:
            factor=mat[i][col];mat[i]=[a-factor*b for a,b in zip(mat[i],mat[col])]
exact=[r[-1] for r in mat]
weights=exact[:12];beta=exact[-1]
assert all(w>=0 for w in weights) and weights[5]+weights[6]==1
residues=[]
for (p,bits),(rr,V) in zip(states,data):
    rho=beta*V-sum(w*v for w,v in zip(weights,rr))
    assert rho>=0,(p,bits,rho)
    residues.append({'p':p,'bits':list(bits),'rho':str(rho)})
assert beta<F(1499,750)
out={'status':'PASS exact 256-state binary-background four-tail certificate',
     'scope':'Exactly four remaining providers after a one-provider prefix in the original five-player game; p_x in {0,1}.',
     'beta':str(beta),'old_beta':'1499/750','strict_improvement':str(F(1499,750)-beta),
     'weights':{n:str(w) for n,w in zip(names,weights)},'source':'four_remaining_profit_bound.md, twelve legal rows with P/E corrections omitted only on p=0,1',
     'zero_residues':sum(r['rho']=='0' for r in residues),'residues':residues,
     'warning':'New weights do not preserve the old RHOMIN residual. No HALF5 proof and no arbitrary-background assertion.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='residues'}))
