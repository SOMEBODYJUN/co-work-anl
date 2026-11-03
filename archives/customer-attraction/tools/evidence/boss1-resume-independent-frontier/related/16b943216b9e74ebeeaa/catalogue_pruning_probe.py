from itertools import product
from random import Random
import json
from pathlib import Path
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate

OUT=Path(__file__).parent

def restrict(instance, support):
    support=tuple(support)
    remap={a:i for i,a in enumerate(support)}
    types={}
    for c in instance.customers:
        b=frozenset(remap[a] for a in c.topics if a in remap)
        if b:
            types[b]=types.get(b,0)+c.multiplicity
    return Instance(tuple(instance.topics[a] for a in support),tuple(CustomerType(b,r) for b,r in types.items()),instance.players)

def run():
    rng=Random(20261023)
    tested=0
    for m,t,attempts in [(2,3,300),(3,3,1000),(3,4,1000),(4,4,500)]:
        for z in range(attempts):
            customers=tuple(CustomerType(frozenset(a for a in range(t) if mask>>a&1),r)
                            for mask in range(1,1<<t) if (r:=rng.randrange(7)))
            inst=Instance(tuple(chr(65+a) for a in range(t)),customers,m)
            solver=ExactSPESolver(inst)
            for counts in sorted(solver.outcomes()):
                support=tuple(a for a,x in enumerate(counts) if x)
                if len(support)==t:
                    continue
                small=restrict(inst,support)
                target=tuple(counts[a] for a in support)
                tested+=1
                if target not in ExactSPESolver(small).outcomes():
                    cert=solver.certificate(counts)
                    report=verify_certificate(inst,cert)
                    report.assert_valid()
                    result={'tested':tested,'m':m,'t':t,'sample':z,'instance':inst.to_dict(),'target':counts,
                            'support':support,'restricted':small.to_dict(),'restricted_outcomes':sorted(ExactSPESolver(small).outcomes()),
                            'certificate':cert.to_dict()}
                    (OUT/'catalogue_pruning_failure.json').write_text(json.dumps(result,indent=2))
                    print(json.dumps({k:v for k,v in result.items() if k!='certificate'},indent=2))
                    return
    print('No failure among',tested,'sampled outcomes')

if __name__=='__main__':
    run()
