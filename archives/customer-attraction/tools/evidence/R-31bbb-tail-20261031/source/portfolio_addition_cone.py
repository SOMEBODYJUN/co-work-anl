"""Finite full-policy cone attack on a sufficient static portfolio bridge.

No finite run is a proof.  A floating violation is only a discovery point.
Every SPE row uses the chosen continuation at each ordered history.
"""
from pathlib import Path
import argparse
from itertools import combinations
import json
import random
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def cone(instance, certificate, target, mode='portfolio'):
    p, m = instance.topic_count, instance.players
    masks = np.arange(1, 1 << p)
    incidence = ((masks[:, None] >> np.arange(p)) & 1).astype(float)
    cache = {}
    def terminal(h):
        if h not in cache:
            z = h
            while len(z) < m:
                z += (certificate.actions[z],)
            cache[h] = z
        return cache[h]
    def row(a, z):
        c = incidence[:, z].sum(axis=1)
        return incidence[:, a] / np.maximum(c, 1)
    actual = terminal(())
    c = incidence[:, actual].sum(axis=1)
    covered = (c > 0).astype(float)
    d = incidence[:, target].sum(axis=1)
    optimal = (d > 0).astype(float)
    addition = d / (1 + c)
    inequalities = []
    for h, a in certificate.actions.items():
        live = row(a, terminal(h))
        for b in range(p):
            if b != a:
                inequalities.append(np.r_[row(b, terminal(h + (b,))) - live, 0])
    # Strict uniqueness is stronger than needed, but makes every optimal
    # portfolio accounted for when a positive separator is recovered.
    if mode == 'portfolio':
        for size in range(1, min(m,p) + 1):
            for support in combinations(range(p), size):
                if support != target:
                    other = (incidence[:, support].sum(axis=1) > 0).astype(float)
                    inequalities.append(np.r_[other-optimal, 1])
    inequalities.append(np.r_[covered-addition*(m if mode=='maximum' else 1), 1])
    result = linprog(np.r_[np.zeros(len(masks)), -1],
                     A_ub=np.array(inequalities), b_ub=np.zeros(len(inequalities)),
                     A_eq=[np.r_[covered, 0]], b_eq=[1],
                     bounds=[(0,None)]*len(masks)+[(None,None)], method='highs')
    return result, actual


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--games',type=int,default=100)
    ap.add_argument('--topics',type=int,default=6)
    ap.add_argument('--players',type=int,default=4)
    ap.add_argument('--seed',type=int,default=10211)
    ap.add_argument('--mode',choices=['portfolio','maximum'],default='portfolio')
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();rng=random.Random(a.seed);best=-float('inf');checked=0;candidate=None
    for g in range(a.games):
        active=rng.sample(range(1,1<<a.topics),min(12,(1<<a.topics)-1))
        customers=tuple(CustomerType(frozenset(j for j in range(a.topics) if mask>>j&1),rng.randrange(1,16)) for mask in active)
        ins=Instance(tuple(map(str,range(a.topics))),customers,a.players)
        sol=ExactSPESolver(ins)
        targets=([(j,) for j in range(a.topics)] if a.mode=='maximum' else
                 [t for t in combinations(range(a.topics),a.players)
                  if ins.welfare(ins.counts(t))==ins.optimal_welfare()])
        for z in sol.worst_outcomes():
            cert=sol.certificate(z)
            for target in targets:
                checked+=1;r,actual=cone(ins,cert,target,a.mode)
                if r.success:
                    best=max(best,float(r.x[-1]))
                    if r.x[-1]>1e-7:
                        candidate=dict(instance=ins.to_dict(),certificate=cert.to_dict(),target=target,
                                       actual=actual,weights=r.x[:-1].tolist(),gap=float(r.x[-1]))
                        break
            if candidate:break
        if candidate:break
    out=dict(status='floating_candidate_requires_exact_audit' if candidate else 'no_floating_separator_in_finite_sample',
             games_processed=g+1,policy_target_pairs=checked,largest_gap=best,
             parameters=vars(a)|{'output':str(a.output)},candidate=candidate)
    with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k!='candidate'}))


if __name__=='__main__':main()
