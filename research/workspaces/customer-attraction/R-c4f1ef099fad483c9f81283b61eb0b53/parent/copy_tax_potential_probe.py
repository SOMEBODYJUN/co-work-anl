"""Attack P_m <= W + maximal-self-copy tax in exact full count policies.

A positive rational witness refutes only this stronger auxiliary candidate.
Floating failure to find a witness is not evidence of a universal theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json,sys
import numpy as np
from scipy.optimize import linprog
import mixed_pair as mix
from six_stress import exact_solve
HERE=Path(__file__).resolve().parent
M=6;P=7
TYPES=np.array(list(product((0,1),repeat=P))[1:],dtype=np.int64)
H=np.array([sum(60//j for j in range(1,k+1)) for k in range(M+1)])


def comps(n,k):
    if k==1:yield (n,);return
    for x in range(n+1):
        for tail in comps(n-x,k-1):yield (x,)+tail


FINALS=tuple(comps(M,P))
LOAD=np.array([TYPES@np.array(q) for q in FINALS])
POT=H[LOAD]
U=np.array([TYPES.T*(60//np.maximum(z,1))[None,:] for z in LOAD])
FI={q:i for i,q in enumerate(FINALS)}


def policy(weights):
    chosen={}
    @lru_cache(None)
    def leaf(q):
        if sum(q)==M:return FI[q]
        opts=[]
        for a in range(P):
            z=list(q);z[a]+=1;opts.append(leaf(tuple(z)))
        winner=max(range(P),key=lambda a:int(U[opts[a],a]@weights))
        chosen[q]=winner
        return opts[winner]
    leaf((0,)*P)
    rows=[]
    for q,winner in chosen.items():
        prescribed=leaf(q)
        for a in range(P):
            if a==winner:continue
            z=list(q);z[a]+=1;other=leaf(tuple(z))
            rows.append(U[prescribed,winner]-U[other,a])
    q=(0,)*P;actual=[]
    for i in range(M):
        a=chosen[q];actual.append(a);z=list(q);z[a]+=1;q=tuple(z)
    union=(TYPES[:,actual].sum(axis=1)>0).astype(np.int64)
    tax=np.zeros(len(TYPES),dtype=np.int64);prior=np.zeros(len(TYPES),dtype=np.int64)
    for i,a in enumerate(actual):
        aa=TYPES[:,a];tax+=aa*((60//(prior+1))-(60//(prior+M-i)));prior+=aa
    return np.array(rows),chosen,actual,60*union+tax


def main():
    rng=np.random.default_rng(61246)
    records=[]
    for trial in range(30):
        weights=np.zeros(len(TYPES),dtype=np.int64)
        for k in range(20):weights[int(rng.integers(len(TYPES)))]+=int(rng.integers(1,31))
        rows,chosen,actual,credit=policy(weights)
        targets=[int(np.argmax(POT@weights))]+[FI[tuple(6*int(i==a) for i in range(P))] for a in range(P)]
        targets+=list(map(int,rng.choice(len(FINALS),8,replace=False)))
        best=0
        for target in dict.fromkeys(targets):
            objective=POT[target]-credit
            sol=linprog(-objective.astype(float),A_ub=-rows.astype(float),b_ub=np.zeros(len(rows)),
                        A_eq=[np.ones(len(TYPES))],b_eq=[1],bounds=(0,None),method='highs')
            assert sol.success,sol.message
            best=max(best,-sol.fun)
            if sol.fun<-1e-7:
                ids=np.flatnonzero(sol.x>1e-8)
                eqs=[[F(int(row[j])) for j in ids]+[F()] for row in rows if abs(float(row@sol.x))<1e-8]
                eqs.append([F(1)]*len(ids)+[F(1)])
                vals=exact_solve(eqs,len(ids));xx=[F()]*len(TYPES)
                for j,v in zip(ids,vals):xx[j]=v
                assert min(xx)>=0 and sum(xx)==1
                assert all(sum(F(int(c))*v for c,v in zip(row,xx))>=0 for row in rows)
                gap=sum(F(int(c))*v for c,v in zip(objective,xx));assert gap>0
                out={'status':'exact full-SPE auxiliary-candidate counterexample; NOT a half counterexample',
                     'candidate':'maximum harmonic potential <= actual W + maximal-self-copy tax',
                     'm':M,'catalog_size':P,'seed':61246,'trial':trial,'actual_actions':actual,
                     'comparison_counts':FINALS[target],'gap_scaled60':str(gap),'verified_IC_rows':len(rows),
                     'customer_types':[{'members':list(map(int,t)),'mass':str(v)} for t,v in zip(TYPES,xx) if v],
                     'count_policy':[{'prefix':q,'action':a} for q,a in sorted(chosen.items())]}
                (HERE/'copy_tax_potential_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
                print(json.dumps({k:v for k,v in out.items() if k not in ('customer_types','count_policy')},indent=2),flush=True);return
        records.append({'trial':trial,'actual_actions':actual,'largest_discovered_gap_scaled60':float(best)})
        print('trial',trial,'actual',actual,'max_auxiliary_gap60',best,flush=True)
    (HERE/'copy_tax_potential_probe.json').write_text(json.dumps({'scope':'finite floating fixed-policy-cone attack; no universal conclusion',
        'm':M,'catalog_size':P,'seed':61246,'numpy_version':np.__version__,'trials':records,'refutation_found':False},indent=2)+'\n')
    print('No refutation in stated fixed-policy probes. No universal conclusion.',flush=True)


if __name__=='__main__':main()
