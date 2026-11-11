"""Small ordered five-tail envelope at the six real root deviations.

The scalar weights are common across all six deviations. The hidden membership
tuple keeps all five real tail positions, their true floor comparisons, actual
terminal prices, optional topic capacities, and the frozen five-tail remainder.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json
import numpy as np
from scipy.optimize import linprog
from root_envelope import input_data,OUT,KAP,q

def solve(capacity=True,own_queries=True,fixed_queries=True,other_comparisons=True,return_model=False):
    a,h,K,u,mass,rem,bycount,diag=input_data('discounted_augmented_lp/augmented_lp_exact.json','a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505')
    cm=defaultdict(F)
    for x in h:
        w=F(x['weight']);d=x['d']
        if not w:continue
        for t in (0,1):
            pr=F(d if t else 6-d,6)
            if pr:cm[x['actual_bits'],d,t]+=w*pr
    contexts=sorted(cm)
    parameters=[('gamma',)]
    parameters += [('price',i) for i in range(5)]
    if capacity:parameters += [('capacity',i) for i in range(5)]
    if fixed_queries:parameters += [('floor-actual',i,j) for i in range(5) for j in range(6)]
    if other_comparisons:parameters += [('floor-other-opt',i) for i in range(5)]
    parameters += [('floor-root-topic',i) for i in range(5)]
    if own_queries:parameters += [('floor-own-tail',i,j) for i in range(5) for j in range(5) if i!=j]
    n=len(parameters);pindex={p:i for i,p in enumerate(parameters)}
    c=[F(0)]*(n+len(contexts));c[0]=-KAP*K
    for p,i in pindex.items():
        if p[0]=='price':c[i]=u[5]
        if p[0]=='capacity':c[i]=K
    A=[];B=[];metadata=[];exact_rows=[]
    for k,context in enumerate(contexts):
        actual,d,t=context;ab=tuple(map(int,actual));ell=sum(ab[:5]);comp=d-t;w=cm[context]
        c[n+k]=-w;c[0]-=w*q(comp,d)
        for e in product((0,1),repeat=5):
            z=sum(e);v=[q(x,t+z) for x in e];r=q(t,t+z);cols=[F(0)]*n
            cols[0]=-2*q(z,t+z)+rem[t,''.join(map(str,e)),comp]
            for p,i in pindex.items():
                kind=p[0]
                if kind=='price':cols[i]=q(e[p[1]],ell+1)
                elif kind=='capacity':cols[i]=F(e[p[1]])
                elif kind.startswith('floor-'):
                    pos=p[1];den=t+sum(e[:pos])+5-pos
                    if kind=='floor-actual':ic=v[pos]-q(ab[p[2]],den)
                    elif kind=='floor-other-opt':ic=5*v[pos]-q(comp,den)
                    elif kind=='floor-root-topic':ic=v[pos]-q(t,den)
                    elif kind=='floor-own-tail':ic=v[pos]-q(e[p[2]],den)
                    else:raise AssertionError(kind)
                    cols[i]=-ic
            row=[-x for x in cols]+[F(int(j==k)) for j in range(len(contexts))]
            A.append([float(x) for x in row]);B.append(float(r));exact_rows.append((cols,r))
            metadata.append({'context_index':k,'tail':''.join(map(str,e))})
    res=linprog(np.array([float(x) for x in c]),A_ub=np.array(A),b_ub=np.array(B),
                bounds=[(0,None)]*n+[(None,None)]*len(contexts),method='highs')
    assert res.success,res.message
    pars=[F(float(v)).limit_denominator(10**10) for v in res.x[:n]]
    lhs=u[0]+sum(c[i]*pars[i] for i in range(n));rhs_min=F(0);mins=[]
    for k,context in enumerate(contexts):
        values=[r+sum(v*p for v,p in zip(cols,pars)) for cols,r in exact_rows[32*k:32*(k+1)]]
        best=min(values);lhs+=c[n+k]*best
        mins.append({'context':list(context),'mass':str(cm[context]),'minimum':str(best),
                     'tail_argmin':[f'{i:05b}' for i,x in enumerate(values) if x==best]})
    result={'capacity':capacity,'own_queries':own_queries,'fixed_queries':fixed_queries,'other_comparisons':other_comparisons,
        'parameter_count':n,'context_count':len(contexts),'row_count':len(A),'float_min_slack':float(res.fun+float(u[0])),
        'exact_chosen_row_slack':str(lhs),'parameter_names':[list(p) for p in parameters],'parameters':[str(p) for p in pars],
        'positive_parameters':[{'name':list(p),'value':str(v)} for p,v in zip(parameters,pars) if v],
        'context_minima':mins,'float_primal':res.x.tolist(),'float_dual':res.ineqlin.marginals.tolist(),
        'float_lower_marginals':res.lower.marginals.tolist(),'matrix_row_metadata':metadata,
        'input_sha256':diag['input_sha256']}
    if return_model:
        return result,{'parameters':parameters,'contexts':contexts,'context_mass':cm,
                       'c':c,'rows':exact_rows,'u':u,'K':K,'metadata':metadata}
    return result

def main():
    r=solve();(OUT/'ordered_root_envelope_discovery.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('float_primal','float_dual','matrix_row_metadata','context_minima','float_lower_marginals','parameters','parameter_names')},indent=2))
if __name__=='__main__':main()
