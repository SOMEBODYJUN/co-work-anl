#!/usr/bin/env python3
"""One pass over selected existing complete strategies for one weak-gap candidate.
No multiplier tuning, no claim to exhaust games or complete strategy cones.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import Instance,ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,independently_verify,serializable
HERE=Path(__file__).resolve().parent

def main():
    report={'scope':'selected complete-policy cones, single weak gap objective, finite diagnostic only','candidate':'OPT_m-W <= m u_i for every actual player','cones':0,'lps':0,'maximum_float':None,'counterexample':None};best=None;start=time.time()
    for path in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        ins=Instance.from_dict(json.loads(path.read_text()));k=ins.topic_count;m=ins.players
        if k>6 or m>4:continue
        solver=ExactSPESolver(ins)
        targets=sorted(solver.outcomes(),key=lambda c:(ins.welfare(c),min(ins.topic_payoffs(c)[a] for a in range(k) if c[a])))[:2]
        for target in targets:
            cert=solver.certificate(target);cone=StrategyCone(k,m,dict(cert.actions));report['cones']+=1
            for t in range(k):
                if not target[t]:continue
                pr=payoff_row(k,target,t)
                for support in combinations(range(k),min(k,m)):
                    cover=coverage_row(k,support);objective=tuple(x-m*y for x,y in zip(cover,pr))
                    res=linprog(-np.array(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs');report['lps']+=1
                    if not res.success:raise RuntimeError(res.message)
                    val=-res.fun
                    if best is None or val>best:best=val;report['maximum_float']=val;report['argmax']={'source':path.name,'terminal':target,'player_topic':t,'portfolio':support}
                    if val<=1+1e-8:continue
                    values=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
                    if not cone.verify(values) or dot(cone.welfare,values)!=1:values=cone.recover_vertex(res.x)
                    if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:continue
                    value=dot(objective,values)
                    if value<=1:continue
                    clones=integer_clones(values);candidate=instance_from_clones(k,m,clones)
                    assert independently_verify(cone,clones)
                    certificate=StrategyCertificate(cone.actions,cone.root);verify_certificate(candidate,certificate).assert_valid()
                    W=candidate.welfare(target);OPT=candidate.optimal_welfare();u=candidate.topic_payoff(t,target)
                    assert OPT-W>m*u
                    report['counterexample']={'source':path.name,'instance':candidate.to_dict(),'strategy':certificate.to_dict(),'player_topic':t,'W':W,'OPT':OPT,'u':u,'slack':W+m*u-OPT,'portfolio':support,'clones':clones,'normalized_objective':value}
                    report['elapsed_seconds']=time.time()-start
                    (HERE/'weak_gap_cone_probe_exact.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
                    print(json.dumps(serializable(report),indent=2));return
            print(json.dumps({'source':path.name,'cones':report['cones'],'lps':report['lps'],'maximum_float':best}),flush=True)
    report['elapsed_seconds']=time.time()-start
    (HERE/'weak_gap_cone_probe_exact.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps(serializable(report),indent=2))
if __name__=='__main__':main()
