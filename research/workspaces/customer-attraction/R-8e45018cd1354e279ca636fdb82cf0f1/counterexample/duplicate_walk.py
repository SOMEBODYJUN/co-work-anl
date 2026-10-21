"""Finite full-history cone walk; never a universal certificate.
Each candidate is reconstructed through the exact all-SPE outcome oracle.
The LP uses all customer-incidence types, then checks Fraction feasibility.
"""
from pathlib import Path
import sys,json,random,time
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import instance_from_clones,integer_clones,serializable
from cone_attack_credible_variants import credible_cone,exact_export
OUT=Path(__file__).resolve().parent/'duplicate_big'
OUT.mkdir(exist_ok=True)
rng=random.Random(21010651)
p,m=7,5
base=[0]*((1<<p)-1);base[2]=m
for a in range(2,p):base[(1<<a)-1]=1
current=tuple(base)
records=[];best=Fraction(0);started=time.monotonic()
for step in range(16):
    if step%4==0:current=tuple(base)
    instance=instance_from_clones(p,m,current);solver=ExactSPESolver(instance)
    target=max(solver.worst_outcomes(),key=lambda q:(sum(x>0 for x in q),-max(q),q))
    mode=('uniform_credible','max_credible_payoff','max_credible_welfare','min_credible_welfare')[step%4]
    cone,stats=credible_cone(solver,target,rng,mode)
    # comparison portfolio contains the concentrated action and four alternatives;
    # later walk steps can use a different actual root support.
    support=(0,2,3,4,5)
    result=cone.optimize(support)
    record={'step':step,'source':current,'mode':mode,'target':target,'statistics':stats,'rows':len(cone.rows)}
    if result['certified']:
        proof=exact_export(cone,result);ratio=proof['ratio']
        record.update(proof)
        current=integer_clones(result['values'])
        if ratio>best:
            best=ratio
            record['strategy']=StrategyCertificate(cone.actions,cone.root).to_dict()
            (OUT/'best_policy.json').write_text(json.dumps(serializable(record),indent=2)+'\n')
        # If the next source has many coincident topics, add small baseline
        # perturbations only if a fresh exact solver reconstructs the policy.
        if step%4==2:
            current=tuple(100*x+b for x,b in zip(current,base))
    else:record['failure']=result
    records.append(record)
    print(json.dumps(serializable({'step':step,'value':record.get('objective_value'),'actual_ratio':record.get('ratio'),'best':best,'rows':len(cone.rows),'elapsed':time.monotonic()-started})),flush=True)
    (OUT/'results.json').write_text(json.dumps(serializable({'scope':'16 sampled complete full-history m5p7 cones; no universal bound','seed':21010651,'records':records}),indent=2)+'\n')
