"""Finite canonical-oracle attacks on terminal tax; no general theorem inferred."""
import json, random, time
from fractions import Fraction
from pathlib import Path
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def tax(inst,q):
    return sum((Fraction(c.multiplicity * load,load+1) for c in inst.customers
                if (load:=sum(q[j] for j in c.topics))),Fraction())

def run(inst):
    oracle=ExactSPESolver(inst)
    opt=inst.optimal_welfare()
    worst=max(oracle.outcomes(),key=lambda q:Fraction(opt-inst.welfare(q))-tax(inst,q))
    gap=Fraction(opt-inst.welfare(worst))-tax(inst,worst)
    return gap,worst,oracle

rng=random.Random(4005)
summary=[]
best=None
started=time.time()
for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
    try:
        inst=Instance.from_dict(json.loads(p.read_text()))
        gap,q,o=run(inst)
        summary.append({'file':str(p.relative_to(ROOT)),'gap':str(gap),'q':q})
    except (KeyError,ValueError) as ex:
        summary.append({'file':str(p.relative_to(ROOT)),'skip':str(ex)})
for it in range(1500):
    n=rng.choice((3,4,5))
    m=rng.choice((3,4,5,6))
    masks=rng.sample(range(1,1<<n),rng.randint(2,min(10,(1<<n)-1)))
    inst=Instance(tuple(map(str,range(n))),tuple(CustomerType(frozenset(j for j in range(n) if mask>>j&1),rng.randint(1,8)) for mask in masks),m)
    gap,q,o=run(inst)
    # normalize for comparable finite-input score.
    score=gap/max(1,inst.welfare(q))
    if best is None or score>best[0]:
        best=(score,gap,q,inst)
        print(json.dumps({'iteration':it,'best_score':str(score),'gap':str(gap),'q':q,'instance':inst.to_dict()}),flush=True)
    if gap>0:
        cert=o.certificate(q)
        (OUT/'tax_counterexample.json').write_text(json.dumps({'instance':inst.to_dict(),'gap':str(gap),'q':q,'certificate':cert.to_dict()},indent=2))
        break
(OUT/'tax_search_report.json').write_text(json.dumps({'existing':summary,'random_trials':it+1,'seed':4005,'best_score':str(best[0]),'best_gap':str(best[1]),'best_q':best[2],'best_instance':best[3].to_dict(),'seconds':time.time()-started},indent=2))
print('DONE',it+1,time.time()-started,flush=True)
