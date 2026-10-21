"""Test the stronger min-SPE-welfare >= min-PNE-welfare bridge.
Exploration only. Reproduce from repository root; emits JSON, never overwrites assets.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import sys, json, random
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate


def counts_from_tuple(t, k):
    return tuple(t.count(a) for a in range(k))


def pnes(instance):
    k, m = instance.topic_count, instance.players
    found=[]
    for t in combinations_with_replacement(range(k),m):
        q=counts_from_tuple(t,k)
        u=instance.topic_payoffs(q)
        okay=True
        for a in range(k):
            if not q[a]: continue
            for b in range(k):
                r=list(q);r[a]-=1;r[b]+=1
                if instance.topic_payoffs(r)[b]>u[a]:
                    okay=False;break
            if not okay:break
        if okay:found.append(q)
    assert found
    return found


def main():
    rng=random.Random(419032)
    trials=0
    for m,k,runs in [(2,3,300),(3,4,500),(4,5,500),(5,7,300)]:
        for run in range(runs):
            # Sparse random incidence types, including private types.
            mask_weights={}
            for _ in range(rng.randrange(3,16)):
                mask=rng.randrange(1,1<<k)
                mask_weights[mask]=rng.randrange(1,15)
            ins=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w) for mask,w in sorted(mask_weights.items())),m)
            solver=ExactSPESolver(ins)
            sw=solver.minimum_welfare()
            pn=pnes(ins)
            pw=min(map(ins.welfare,pn))
            trials+=1
            if sw<pw:
                target=min(solver.worst_outcomes())
                cert=solver.certificate(target_counts=target)
                report=verify_certificate(ins,cert);report.assert_valid()
                result={'status':'bridge-refuted','seed':419032,'trials':trials,'m':m,'k':k,'instance':ins.to_dict(),'spe_welfare':sw,'min_pne_welfare':pw,'all_pne_counts':pn,'opt':ins.optimal_welfare(),'certificate':cert.to_dict()}
                print(json.dumps(result,ensure_ascii=False,indent=2));return
        print(json.dumps({'progress':trials,'m':m,'k':k}),file=sys.stderr,flush=True)
    print(json.dumps({'status':'no-counterexample-in-finite-run','seed':419032,'trials':trials}))

if __name__=='__main__':main()
