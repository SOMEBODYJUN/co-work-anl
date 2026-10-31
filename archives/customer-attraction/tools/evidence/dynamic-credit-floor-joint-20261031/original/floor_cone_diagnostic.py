from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog
ROOT=Path.cwd();sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import Instance,ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,independently_verify,serializable
HERE=Path(__file__).resolve().parent
best=-100;cnt=0
for path in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
 try:ins=Instance.from_dict(json.loads(path.read_text()))
 except:continue
 k=ins.topic_count;m=ins.players
 if k>6 or m>4:continue
 solver=ExactSPESolver(ins)
 targets=sorted(solver.outcomes(),key=lambda c:(ins.welfare(c),min(ins.topic_payoffs(c)[a] for a in range(k) if c[a])))[:2]
 for target in targets:
  cert=solver.certificate(target);cone=StrategyCone(k,m,dict(cert.actions));cnt+=1
  for t in range(k):
   if not target[t]:continue
   pr=payoff_row(k,target,t)
   for support in combinations(range(k),min(k,m)):
    cover=coverage_row(k,support);obj=tuple(x-(2*m-1)*y for x,y in zip(cover,pr))
    res=linprog(-np.array(obj,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:continue
    val=-res.fun
    if val>best:best=val;arg=(path.name,target,t,support)
    if val<=1e-8:continue
    values=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
    if not cone.verify(values) or dot(cone.welfare,values)!=1:values=cone.recover_vertex(res.x)
    if values is None or not cone.verify(values) or dot(cone.welfare,values)!=1:continue
    value=dot(obj,values)
    if value<=0:continue
    clones=integer_clones(values);candidate=instance_from_clones(k,m,clones)
    assert independently_verify(cone,clones)
    certificate=StrategyCertificate(cone.actions,cone.root);verify_certificate(candidate,certificate).assert_valid()
    report={'scope':'counterexample to individual OPT/(2m-1) floor only','source':path.name,'instance':candidate.to_dict(),'strategy':certificate.to_dict(),'player_topic':t,'W':candidate.welfare(target),'OPT':candidate.optimal_welfare(),'u':candidate.topic_payoff(t,target),'slack':(2*m-1)*candidate.topic_payoff(t,target)-candidate.optimal_welfare(),'portfolio':support,'clones':clones,'value':value}
    (HERE/'floor_cone_counterexample.json').write_text(json.dumps(serializable(report),indent=2)+'\n');print(json.dumps(serializable(report),indent=2));raise SystemExit
print('no positive',cnt,best,arg)
