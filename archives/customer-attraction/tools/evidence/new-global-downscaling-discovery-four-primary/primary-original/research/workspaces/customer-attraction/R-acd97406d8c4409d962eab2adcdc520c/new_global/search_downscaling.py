"""Search a precise obstruction to shrinking customers missed by an SPE outcome.
This tests an auxiliary reduction, never the half-coverage conjecture.
"""
import json,random,sys
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
rng=random.Random(615100)
for case in range(10000):
    n=4;m=3
    raw=[(mask,rng.randrange(0,9)) for mask in range(1,1<<n)]
    raw=[(mask,w) for mask,w in raw if w]
    base=Instance(tuple(map(str,range(n))),tuple(CustomerType(frozenset(a for a in range(n) if mask>>a&1),2*w) for mask,w in raw),m)
    solver=ExactSPESolver(base)
    for target in solver.outcomes():
        covered=lambda mask:any(target[a] and mask>>a&1 for a in range(n))
        if all(covered(mask) for mask,w in raw):continue
        small=Instance(base.topics,tuple(CustomerType(c.topics,c.multiplicity if any(target[a] for a in c.topics) else c.multiplicity//2) for c in base.customers),m)
        other=ExactSPESolver(small)
        if target not in other.outcomes():
            cert=solver.certificate(target)
            verify_certificate(base,cert).assert_valid()
            result={'purpose':'auxiliary no-entry downscaling reduction counterexample; not half-coverage','seed':615100,'case':case,'original':base.to_dict(),'scaled':small.to_dict(),'target':target,'original_certificate':cert.to_dict(),'scaled_outcomes':[list(x) for x in sorted(other.outcomes())]}
            print(json.dumps(result,indent=2))
            sys.exit()
    if case%100==0:print('case',case,file=sys.stderr)
