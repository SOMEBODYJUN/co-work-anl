"""Retain one genuine maximum-root branch jointly with the actual path.

Discovery only: no full SPE, no theorem from an optimizer status.
Atoms: actual bits A..E, maximum-root branch bits C0,H,I,J,L, and
optimal five-topic membership multiplicity d. Exactly 6144 atoms.
"""
from pathlib import Path
from itertools import product, combinations_with_replacement
from fractions import Fraction as F
import json, numpy as np
from scipy.optimize import linprog

P=[tuple(range(5)),tuple(range(5,10))]
ATOMS=[(b,d) for b in product((0,1),repeat=10) for d in range(6)]
def q(n,d): return F(n,d) if n else F(0)

def rows(bits,d):
    b=list(bits); K=F(b[5]); O=F(d>0); out={}
    us=[[q(b[i],sum(b[j] for j in path)) for i in path] for path in P]
    out['root-to-max']=us[0][0]-us[1][0]
    for i in range(10):out[f'max-size:{i}']=K-b[i]
    out['max-size:opt']=5*K-d
    for pidx,path in enumerate(P):
        u=us[pidx]
        for pos in range(0 if pidx==0 else 1,5):
            pref=sum(b[i] for i in path[:pos]); rem=5-pos
            for j in range(10):out[f'{pidx}:IC:{pos}:{j}']=u[pos]-q(b[j],pref+rem)
            out[f'{pidx}:opt:{pos}']=5*u[pos]-q(d,pref+rem)
            out[f'{pidx}:O:{pos}']=5*rem*u[pos]+q(pref,pref+rem)-O
        pref=sum(b[i] for i in path[:3]); H=u[3]+u[4]+q(b[path[3]],(pref+1)*(pref+2))
        out[f'{pidx}:r2:O']=F(5,2)*H+q(pref,pref+1)-O
        out[f'{pidx}:r2:opt']=10*H-q(d*(5-d),pref+1)-q(d*(d-1),pref+2)
        for j,k in combinations_with_replacement(range(10),2):
            x,y=b[j],b[k]
            out[f'{pidx}:r2:pair:{j}:{k}']=H-q(x+y-2*x*y,pref+1)-q(2*x*y,pref+2)
        bg=sum(b[i] for i in path[:2]); g3=q(d*(5-d)*(4-d),2*(bg+1))+q(d*(d-1)*(5-d),bg+2)+q(d*(d-1)*(d-2),2*(bg+3))
        out[f'{pidx}:r3:opt']=50*sum(u[2:])-3*g3
        bg=b[path[0]];g4=q(d*(d-1),bg+d-1)+q((5-d)*d,bg+d)
        out[f'{pidx}:r4:opt']=7495*sum(u[1:])-750*g4
        out[f'{pidx}:r4:binary']=29985*sum(u[1:])-4985*(bg-u[0])-3000*g4
    return out

def run():
    cols=[rows(b,d) for b,d in ATOMS];names=list(cols[0]); R=np.array([[float(c[n]) for c in cols] for n in names])
    W=np.array([float(any(b[:5])) for b,d in ATOMS]);O=np.array([float(d>0) for b,d in ATOMS])
    ans=linprog(-O,A_ub=-R,b_ub=np.zeros(len(names)),A_eq=W.reshape(1,-1),b_eq=[1.],bounds=(0,None),method='highs')
    result={'status':ans.message,'scope':__doc__,'atoms':len(ATOMS),'rows':len(names)}
    if ans.success:
        result.update(value=float(-ans.fun),minimum_slack=float((R@ans.x).min()),support=[{'bits':list(ATOMS[i][0]),'d':ATOMS[i][1],'mass':float(x)} for i,x in enumerate(ans.x) if x>1e-9],dual={names[i]:float(-x) for i,x in enumerate(ans.ineqlin.marginals) if x< -1e-9})
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({k:v for k,v in result.items() if k not in ('support','dual')},indent=2))
if __name__=='__main__':run()
