"""Diagnose a general pairwise extra-query budget on specified full-policy cones.

All policies are complete canonical SPE certificates on their original inputs.
The LP varies all customer types for the same full ordered policy, including
zero weights. Numerical separation candidates require exact reconstruction.
No positive finite result proves a universal claim.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def load():
    for path in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        inp=ROOT/'examples/customer_attraction'/path.name
        if not inp.exists(): continue
        try:
            inst=Instance.from_dict(json.loads(inp.read_text()))
            if inst.topic_count>8 or inst.players>5: continue
            raw=json.loads(path.read_text()); raw=raw.get('strategy',raw.get('certificate',raw))
            cert=StrategyCertificate.from_dict(raw)
            check=verify_certificate(inst,cert)
            if check.valid: yield path.name, inst, cert
        except (ValueError,KeyError,TypeError): continue


def cone(inst,cert):
    m,k=inst.players,inst.topic_count
    types=list(range(1,1<<k)); scale=math.lcm(*range(1,m+2))
    bits=np.array([[(t>>a)&1 for a in range(k)] for t in types],dtype=int)
    @lru_cache(None)
    def term(h): return h if len(h)==m else term(h+(cert.actions[h],))
    @lru_cache(None)
    def loads(z): return bits[:,list(z)].sum(axis=1)
    @lru_cache(None)
    def pay(a,z):
        return np.array([scale//v if flag else 0 for flag,v in zip(bits[:,a],loads(z))],dtype=int)
    actual=term(())
    cover=(loads(actual)>0).astype(int)
    rows=[]
    for h,a in cert.actions.items():
        z=term(h); chosen=pay(a,z)
        for b in range(k):
            if a!=b: rows.append(chosen-pay(b,term(h+(b,))))
    gamma=np.unique(np.array(rows,dtype=int),axis=0)
    endpoint=[[term(actual[:i]+(a,)) for a in range(k)] for i in range(m)]
    query=np.array([[[[scale//(1+l) if flag else 0 for flag,l in zip(bits[:,q],loads(endpoint[i][a]))] for q in range(k)] for a in range(k)] for i in range(m)])
    return types,scale,actual,cover,gamma,query


def exact_vertex(x, cover, gamma):
    support=np.flatnonzero(x>1e-8).tolist()
    active=gamma[np.abs(gamma@x)<1e-7][:,support]
    # Fraction Gaussian elimination uses independent active equalities only.
    rows = [(cover[support].tolist(), F(1))] + [(r.tolist(), F(0)) for r in active]
    basis = {}
    for raw, rhs in rows:
        row = list(map(F,raw)) + [rhs]
        for pivot in sorted(basis):
            coeff = row[pivot]
            if coeff:
                row = [v-coeff*u for v,u in zip(row,basis[pivot])]
        nz = next((j for j,v in enumerate(row[:-1]) if v), None)
        if nz is None:
            if row[-1]: return None
            continue
        scale = row[nz]; row = [v/scale for v in row]
        basis[nz]=row
        if len(basis)==len(support): break
    if len(basis)!=len(support): return None
    sol=[F(0)]*len(support)
    for pivot in sorted(basis,reverse=True):
        row=basis[pivot]
        sol[pivot]=row[-1]-sum((row[j]*sol[j] for j in range(pivot+1,len(support))),F(0))
    out=[F(0)]*len(x)
    for i,v in zip(support,sol): out[i]=v
    if any(v<0 for v in out): return None
    if sum((F(int(c))*v for c,v in zip(cover,out)),F(0))!=1: return None
    if any(sum((F(int(a))*v for a,v in zip(row,out)),F(0))<0 for row in gamma): return None
    return out


def main():
    report=[]
    for name,inst,cert in load():
        types,scale,actual,c,g,q=cone(inst,cert)
        k=inst.topic_count
        best=None
        for a in range(k):
            for b in range(a+1,k):
                target=(q[:,b,a,:]+q[:,a,b,:]).sum(axis=0)/scale-2*c
                result=linprog(-target,A_ub=csr_matrix(-g),b_ub=np.zeros(len(g)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
                if not result.success: raise RuntimeError((name,result.message))
                gap=float(target@result.x)
                if best is None or gap>best[0]: best=(gap,a,b,result.x,target)
        if best is None: continue
        gap,a,b,x,target=best
        item=dict(name=name,players=inst.players,topics=k,full_policy_histories=len(cert.actions),distinct_incentive_rows=len(g),types=len(types),actual=list(actual),max_numerical_pair_gap=gap,pair=[a,b])
        if gap>1e-7:
            w=exact_vertex(x,c,g)
            if w is not None:
                numerator=(q[:,b,a,:]+q[:,a,b,:]).sum(axis=0)-2*scale*c
                egap=sum((F(int(v),scale)*z for v,z in zip(numerator,w)),F(0))
                item['exact_gap']=str(egap)
                item['weights']={str(t):str(v) for t,v in zip(types,w) if v}
                # Exact full uniform pair query, including its diagonals.
                full=(q[:,a,a,:]+q[:,b,b,:]+q[:,b,a,:]+q[:,a,b,:]).sum(axis=0)
                item['uniform_pair_G_minus_W']=str(sum((F(int(v),4*scale)*z for v,z in zip(full,w)),F(0))-1)
                if egap>0: item['status']='EXACT_PAIRWISE_BUDGET_COUNTEREXAMPLE_CONE_POINT'
            if 'status' not in item:item['status']='NUMERICAL_CANDIDATE_ONLY'
        else:item['status']='SPECIFIED_CONE_NUMERICAL_NO_PAIR_SEPARATION'
        report.append(item)
        print(name,item['status'],gap,flush=True)
        Path(__file__).with_name('pair_budget_diagnostic.json').write_text(json.dumps(dict(scope='Specified complete-policy cones only. Pairwise budget is stronger than weak all-p push budget, menu bridge, and half.',results=report),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
