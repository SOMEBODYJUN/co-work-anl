"""Find small exact-candidate cross-label repairs on one fixed strategy graph."""
from fractions import Fraction
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from probe_common_coverage import setup

BASE=Path(__file__).resolve().parent

def main():
    obj,vs,graph,pair,equal,root,objective,mat=setup()
    n,p=obj['n'],obj['p'];vid={v:i for i,v in enumerate(vs)}
    covers={}
    for q,a in vs:
        A=tuple(b for b in range(p) if q[b])
        if A not in covers:
            r=np.zeros(len(vs))
            for b in A:r[vid[q,b]]=q[b]
            covers[A]=r
    ids=[];names=[]
    for a in range(p):
        for b in range(p):
            if a==b:continue
            q=tuple(2*(i==a)+(i==b) for i in range(p))
            row=np.zeros(len(vs));row[vid[q,a]]=6
            row-=2*covers[(a,)]+covers[tuple(sorted([a,b]))]-covers[(b,)]
            ids.append(row);names.append([a,b])
    aub=np.vstack([graph,pair])
    def solve(selected):
        eq=np.vstack([root,equal]+[ids[i][None,:] for i in selected])
        sol=linprog(-objective,A_ub=aub,b_ub=np.zeros(len(aub)),A_eq=eq,b_eq=np.r_[1,np.zeros(len(eq)-1)],bounds=(0,None),method='highs')
        return sol,eq
    selected=list(range(len(ids)));sol,eq=solve(selected)
    print('all_pairs',-sol.fun)
    for i in selected.copy():
        new=[j for j in selected if j!=i]
        s,e=solve(new)
        if s.success and -s.fun<=2+1e-8:selected=new;sol,eq=s,e
    print('selected', [names[i] for i in selected], 'value',-sol.fun)
    # Preserve HiGHS dual in exact-rational candidate format for a separate checker.
    # scipy minimization dual: objective = <= dual*A + = dual*A, with <= dual<=0.
    # To bound max target by beta root, negate scipy dual signs.
    cert={'beta':str(Fraction(float(-sol.fun)).limit_denominator(1000000)),
          'selected_pair_identities':[names[i] for i in selected],
          'graph_pair_multipliers':[{'row':i,'coefficient':str(Fraction(float(-v)).limit_denominator(1000000))} for i,v in enumerate(sol.ineqlin.marginals) if abs(v)>1e-9],
          'equality_multipliers':[{'row':i,'coefficient':str(Fraction(float(-v)).limit_denominator(1000000))} for i,v in enumerate(sol.eqlin.marginals) if abs(v)>1e-9],
          'lower_bound_residual':[{'vertex':i,'coefficient':str(Fraction(float(v)).limit_denominator(1000000))} for i,v in enumerate(sol.lower.marginals) if abs(v)>1e-9]}
    (BASE/'pair_repair_candidate.json').write_text(json.dumps(cert,indent=2)+'\n')

if __name__=='__main__':main()
