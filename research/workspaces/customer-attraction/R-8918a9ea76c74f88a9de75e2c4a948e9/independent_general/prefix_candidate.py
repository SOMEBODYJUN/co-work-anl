"""Attack a fully quantified prefix inequality; finite evidence only."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json, random, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

def residual_opt(inst, p):
    k = inst.players - sum(p)
    missing = [c for c in inst.customers if not any(p[t] for t in c.topics)]
    return max(sum(c.multiplicity for c in missing if c.topics.intersection(a))
               for n in range(min(k, inst.topic_count)+1)
               for a in combinations(range(inst.topic_count),n))

def check(inst):
    solver = ExactSPESolver(inst)
    solver.outcomes()
    for p, outs in solver._outcomes.items():
        opt = residual_opt(inst,p)
        wp = inst.welfare(p)
        for q in outs:
            delta = inst.welfare(q)-wp
            u = sum((q[t]-p[t])*x for t,x in enumerate(inst.topic_payoffs(q)))
            if opt > delta+u:
                return dict(instance=inst.to_dict(),prefix=p,outcome=q,opt=opt,
                            delta=delta,u=str(u),defect=str(opt-delta-u))

def main():
    rng=random.Random(51983)
    for trial in range(3000):
        d=rng.choice([3,4,5])
        m=rng.choice([3,4,5,6])
        cs=[CustomerType(frozenset(t for t in range(d) if b>>t&1),rng.randrange(1,13))
            for b in range(1,1<<d)]
        cs=[c for c in cs if c.multiplicity]
        inst=Instance(tuple(map(str,range(d))),tuple(cs),m)
        bad=check(inst)
        if bad:
            print(json.dumps(dict(trial=trial,**bad),indent=2),flush=True)
            return
        if trial%100==0: print('checked',trial,flush=True)
    print('No finite counterexample',flush=True)

if __name__=='__main__': main()
