#!/usr/bin/env python3
"""Attack F_m(c_actual)<=W inside selected complete SPE cones.

This is a finite candidate diagnostic, never a universal proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import Instance,ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,dot,integer_clones,instance_from_clones,independently_verify,serializable
HERE=Path(__file__).resolve().parent

def counts(k,r):
    if k==1:
        yield (r,);return
    for j in range(r+1):
        for tail in counts(k-1,r-j):yield (j,)+tail

def row(k,c,q):
    ans=[]
    for mask in range(1,1<<k):
        a=sum(c[t] for t in range(k) if mask&(1<<t))
        d=sum(q[t] for t in range(k) if mask&(1<<t))
        ans.append(F(bool(d))+(F(d,a+d) if d and a else F()))
    return tuple(ans)

def main():
    report={'candidate':'coverage(d)+shared_cross_profit(c,d)<=2W','cones':0,'lps':0,'maximum':None,'counterexample':None}
    start=time.time();best=None
    paths=sorted((ROOT/'examples/customer_attraction').glob('*.json'))
    for path in paths:
        ins=Instance.from_dict(json.loads(path.read_text()));k=ins.topic_count;m=ins.players
        if k>6 or m>4:continue
        sol=ExactSPESolver(ins)
        targets=sorted(sol.outcomes(),key=lambda c:(ins.welfare(c),c))[:2]
        for target in targets:
            cert=sol.certificate(target);cone=StrategyCone(k,m,dict(cert.actions));report['cones']+=1
            for q in counts(k,m):
                obj=row(k,target,q)
                res=linprog(-np.asarray(obj,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.asarray([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs');report['lps']+=1
                if not res.success:raise RuntimeError(res.message)
                val=-res.fun
                if best is None or val>best:
                    best=val;report['maximum']=val;report['argmax']={'source':path.name,'terminal':target,'query':q}
                if val<=2+1e-8:continue
                values=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
                if not cone.verify(values) or dot(cone.welfare,values)!=1:values=cone.recover_vertex(res.x)
                if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:continue
                exact=dot(obj,values)
                if exact<=2:continue
                clones=integer_clones(values);cand=instance_from_clones(k,m,clones)
                assert independently_verify(cone,clones)
                certificate=StrategyCertificate(cone.actions,cone.root)
                verify_certificate(cand,certificate).assert_valid()
                report['counterexample']={'instance':cand.to_dict(),'strategy':certificate.to_dict(),'query':q,'W':cand.welfare(target),'F_query':dot(obj,clones),'normalized':exact,'source':path.name}
                report['elapsed']=time.time()-start
                (HERE/'signed_self_background_probe.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
                print(json.dumps(serializable(report),indent=2));return
        print(json.dumps({'source':path.name,'cones':report['cones'],'lps':report['lps'],'maximum':best}),flush=True)
    report['elapsed']=time.time()-start
    (HERE/'signed_self_background_probe.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps(serializable(report),indent=2))
if __name__=='__main__':main()
