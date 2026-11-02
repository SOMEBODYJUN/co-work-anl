"""Exact falsification attempt of universal omitted-customer privatization P0.

Randomness proposes instances only. Every rejection of an owner assignment uses
exact all-outcome BI, allowing independently reselected full ordered subtrees.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import random
import json
import argparse
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver
from customer_attraction.model import CustomerType
from customer_attraction.certificate import verify_certificate


def run(trials, seed):
    rng = random.Random(seed)
    tested = 0
    for trial in range(trials):
        p, m = 5, 3
        active = [B for B in range(1, 1 << p) if rng.random() < .24]
        if not active:
            continue
        cs = tuple(CustomerType(frozenset(a for a in range(p) if B >> a & 1)) for B in active)
        I = Instance(tuple(f'T{a}' for a in range(p)), cs, m)
        if I.optimal_welfare() != I.customer_count:
            continue
        sig = [frozenset(j for j,c in enumerate(cs) if a in c.topics) for a in range(p)]
        if len(set(sig)) != p:
            continue
        solver = ExactSPESolver(I)
        for q in sorted(solver.outcomes(), key=I.welfare):
            occupied = {a for a in range(p) if q[a]}
            missed = [c for c in cs if not occupied & c.topics]
            if not any(len(c.topics) > 1 for c in missed):
                continue
            assignments = list(product(*[sorted(c.topics) for c in missed]))
            retained = [c for c in cs if occupied & c.topics]
            tested += 1
            survives = False
            assignment_log = []
            for owners in assignments:
                J = Instance(I.topics, tuple(retained + [CustomerType(frozenset([a])) for a in owners]), m)
                other = ExactSPESolver(J)
                ok = q in other.outcomes()
                assignment_log.append({'owners': owners, 'target_realizable': ok,
                                       'root_threshold': str(other.threshold((0,)*p))})
                if ok:
                    survives = True
                    break
            if not survives:
                cert = solver.certificate(q)
                verify_certificate(I,cert).assert_valid()
                return {'claim': 'P0 universal omitted-unit privatization preserving some complete SPE terminal',
                        'status':'EXACT COUNTEREXAMPLE CANDIDATE; not independently reviewed; not a half counterexample',
                        'seed':seed,'trial':trial,'tested_original_terminals':tested,
                        'instance':I.to_dict(),'original_strategy':cert.to_dict(),
                        'original_target_counts':q,'original_W':I.welfare(q),'original_OPT':I.optimal_welfare(),
                        'missed_topics':[sorted(c.topics) for c in missed],
                        'all_assignment_rejections':assignment_log}
    return {'claim':'P0','status':'NO COUNTEREXAMPLE IN FINITE PROPOSALS; no universal conclusion',
            'seed':seed,'trials':trials,'tested_original_terminals':tested}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--trials',type=int,default=300)
    ap.add_argument('--seed',type=int,default=20261024)
    ap.add_argument('--output')
    a=ap.parse_args();r=run(a.trials,a.seed)
    if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('original_strategy','all_assignment_rejections')}))
