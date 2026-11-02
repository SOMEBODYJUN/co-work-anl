"""Finite attacks on root-actual-position full-menu inequality M_i<=u_i.
No assertion that a failed search proves the universal conjecture.
"""
from fractions import Fraction as F
from pathlib import Path
import json, random, sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver, _increment

def kernel(inst,q):
    return tuple(sum((F(c.multiplicity,1+sum(q[t] for t in c.topics))
                      for c in inst.customers if a in c.topics),F())
                 for a in range(inst.topic_count))

def value(columns):
    d=len(columns[0])
    mat=np.array(columns,dtype=float)
    res=linprog([0.]*d+[-1.],A_ub=np.column_stack((-mat,np.ones(len(mat)))),
                b_ub=np.zeros(len(mat)),A_eq=[[1.]*d+[0.]],b_eq=[1.],
                bounds=[(0,None)]*d+[(None,None)],method='highs')
    if not res.success: raise RuntimeError(res.message)
    return res.fun*-1,res.x[:-1]

def attack(inst,rng):
    sol=ExactSPESolver(inst);roots=sol.outcomes()
    for target in sorted(roots,key=inst.welfare)[:3]:
        p=(0,)*inst.topic_count
        while sum(p)<inst.players:
            actions=[a for a in range(inst.topic_count)
                     if target in sol._solve(_increment(p,a)) and
                     sol._utility(target,a)>=sol.threshold(p)]
            a=min(actions,key=lambda a:sol._utility(target,a));u=sol._utility(target,a)
            children=[]
            for b in range(inst.topic_count):
                if b==a: children.append([target]);continue
                qs=[q for q in sol._solve(_increment(p,b)) if sol._utility(q,b)<=u]
                assert qs
                children.append(qs)
            for repeat in range(3):
                qs=[target if b==a else rng.choice(ch) for b,ch in enumerate(children)]
                for ascent in range(5):
                    ks=[kernel(inst,q) for q in qs];v,dual=value(ks)
                    if v>float(u)+1e-8:
                        pp=tuple(F(float(x)).limit_denominator(10**6) for x in dual)
                        pp=tuple(x/sum(pp) for x in pp)
                        lower=min(sum(x*y for x,y in zip(pp,k)) for k in ks)
                        if lower>u:
                            return dict(instance=inst.to_dict(),prefix=p,target=target,
                                        current_action=a,u=str(u),columns=qs,
                                        query=list(map(str,pp)),exact_lower=str(lower))
                    new=[max(ch,key=lambda q:sum(float(x)*y for x,y in zip(kernel(inst,q),dual)))
                         for ch in children]
                    if new==qs: break
                    qs=new
            p=_increment(p,a)

def main():
    rng=random.Random(518726)
    for trial in range(400):
        d=rng.choice([4,5,6]);m=rng.choice([4,5,6,7]);cs=[]
        for mask in range(1,1<<d):
            if rng.random()<(.6 if mask.bit_count()<3 else .08):
                cs.append(CustomerType(frozenset(t for t in range(d) if mask>>t&1),rng.randrange(1,21)))
        inst=Instance(tuple(map(str,range(d))),tuple(cs),m);bad=attack(inst,rng)
        if bad:
            out=dict(trial=trial,**bad);print(json.dumps(out,indent=2),flush=True)
            Path(__file__).with_name('menu_violation.json').write_text(json.dumps(out,indent=2));return
        if trial%10==0: print('checked',trial,flush=True)
    print('No finite counterexample',flush=True)
if __name__=='__main__':main()
