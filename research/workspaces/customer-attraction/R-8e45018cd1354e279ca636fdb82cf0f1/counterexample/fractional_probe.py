"""Attack only a proposed fractional-background bridge in sampled full SPE cones."""
from pathlib import Path
import sys,json,random,time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import instance_from_clones,integer_clones,structural_seeds,serializable,dot,independently_verify
from cone_attack_credible_variants import credible_cone
OUT=Path(__file__).resolve().parent/'fractional_probe';OUT.mkdir(exist_ok=True)
rng=random.Random(21010951);p,m=7,5

def opt(cone,a):
    obj=tuple(F(m,m+(m-1)*sum(cone.root[b] for b in range(p) if mask>>b&1)) if mask>>a&1 else F(0) for mask in range(1,1<<p))
    res=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:return None
    vals=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
    if not(cone.verify(vals) and dot(cone.welfare,vals)==1):vals=cone.recover_vertex(res.x)
    if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:return None
    beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
    mu=tuple(F(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals)
    dualok=all(x>=0 for x in mu) and all(beta*w-sum(x*r[j] for x,r in zip(mu,cone.rows))>=v for j,(w,v) in enumerate(zip(cone.welfare,obj)))
    return {'a':a,'value':dot(obj,vals),'score':F(2*m-1,2)*dot(obj,vals),'clones':integer_clones(vals),'dual_bound':beta if dualok else None}

seeds=list(structural_seeds(p,m))
# Two duplicate large labels yield equilibrium policies with a split actual path.
dup=[0]*((1<<p)-1);dup[2]=m
for a in range(2,p):dup[(1<<a)-1]=1
seeds.append(tuple(dup))
records=[];best=F(0);started=time.monotonic();current=None
for step in range(18):
    if step%3==0:current=seeds[(step//3)%len(seeds)]
    ins=instance_from_clones(p,m,current);solver=ExactSPESolver(ins)
    worst=solver.worst_outcomes()
    target=max(worst,key=lambda q:(sum(c>0 for c in q),-max(q),q))
    cone,stats=credible_cone(solver,target,rng,('uniform_credible','max_credible_payoff','max_credible_welfare')[step%3])
    probes=[r for a in range(p) if (r:=opt(cone,a)) is not None]
    top=max(probes,key=lambda x:x['score'])
    current=top['clones'];assert independently_verify(cone,current)
    verify_certificate(instance_from_clones(p,m,current),StrategyCertificate(cone.actions,cone.root)).assert_valid()
    record={'step':step,'source':ins.to_dict(),'root':cone.root,'stats':stats,'query_scores':[{k:v for k,v in r.items() if k!='clones'} for r in probes],'top':top}
    if top['score']>best:
        best=top['score'];record['strategy']=StrategyCertificate(cone.actions,cone.root).to_dict()
        (OUT/'best.json').write_text(json.dumps(serializable(record),indent=2)+'\n')
    records.append(record)
    (OUT/'results.json').write_text(json.dumps(serializable({'scope':'sampled m5p7 complete SPE cones; auxiliary fractional bridge only','seed':21010951,'records':records}),indent=2)+'\n')
    print(json.dumps(serializable({'step':step,'root':cone.root,'score':top['score'],'best':best,'dual_bounds':[r['dual_bound'] for r in probes],'elapsed':time.monotonic()-started})),flush=True)
    if best>1:break
