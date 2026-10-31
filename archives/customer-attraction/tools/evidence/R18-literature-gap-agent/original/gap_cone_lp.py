from __future__ import annotations
import sys,json,importlib.util
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from random import Random
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('cagcone',ROOT/'tests/audits/customer_attraction_strategy_lp.py');m=importlib.util.module_from_spec(spec);sys.modules['cagcone']=m;spec.loader.exec_module(m)

def optimize(cone,support,a):
    vr=m.coverage_row(cone.topics,support);ur=m.payoff_row(cone.topics,cone.root,a)
    obj=tuple(v-w-cone.players*u for v,w,u in zip(vr,cone.welfare,ur))
    res=linprog(-np.array(obj,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return None
    vals=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(vals) or m.dot(cone.welfare,vals)!=1:
        vals=cone.recover_vertex(res.x)
    if vals is None or not cone.verify(vals) or m.dot(cone.welfare,vals)!=1:return None
    val=m.dot(obj,vals)
    if val>0:
        clones=m.integer_clones(vals)
        assert m.independently_verify(cone,clones)
        ins=m.instance_from_clones(cone.topics,cone.players,clones)
        return {'m':cone.players,'p':cone.topics,'types':clones,'target_action':a,'q':cone.root,'support':support,'positive_objective':str(val),'w':ins.welfare(cone.root),'opt':ins.optimal_welfare(),'u':str(ins.topic_payoff(a,cone.root)),'actions':[{'history':h,'action':b} for h,b in cone.actions.items()]}
    return None

if __name__=='__main__':
    rng=Random(6198922)
    summaries=[]
    for players,topics,rounds in [(3,4,100),(3,6,100),(4,5,60),(5,7,15)]:
        num=0
        seeds=list(m.structural_seeds(topics,players))
        for i in range(rounds):
            if i<len(seeds):r=seeds[i]
            else:r=tuple(rng.choice([0,0,0,1,2,3,5,8]) for _ in range(2**topics-1))
            ins=m.instance_from_clones(topics,players,r);sol=m.ExactSPESolver(ins)
            qs=sorted(sol.worst_outcomes())
            for target in rng.sample(qs,min(2,len(qs))):
                cone=m.cone_from_solver(sol,target,rng,random_ties=True)
                for support in combinations(range(topics),min(players,topics)):
                    for a,q in enumerate(target):
                        if not q:continue
                        num+=1;x=optimize(cone,support,a)
                        if x:
                            dest=HERE/'gap_cone_counterexample.json';dest.write_text(json.dumps(x,indent=2));print(json.dumps({k:v for k,v in x.items() if k!='actions'}),flush=True);sys.exit()
            if i%10==0:print('progress',players,topics,i,num,flush=True)
        summaries.append({'m':players,'p':topics,'cones_limit':rounds*2,'lps':num})
    (HERE/'gap_cone_summary.json').write_text(json.dumps(summaries,indent=2))
