"""Finite attack on the five-player LAST full-menu sufficient bridge.

Exact all-history SPE enumeration is supplied by the canonical solver.  Menu
values use scipy solely to discover a violating rational candidate.  No finite
negative search certifies the general bridge.
"""
from pathlib import Path
import sys, json, random
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver


def menu_matrix(inst, prefix):
    k = inst.topic_count
    return np.array([[sum(c.multiplicity / (1 + sum(a in c.topics for a in prefix) + (b in c.topics))
                         for c in inst.customers if t in c.topics)
                      for b in range(k)] for t in range(k)])


def value(matrix):
    k = len(matrix)
    out = linprog([0.]*k + [1.], A_ub=np.c_[matrix, -np.ones(k)], b_ub=np.zeros(k),
                  A_eq=[[1.]*k+[0.]], b_eq=[1.], bounds=[(0,None)]*k+[(None,None)],
                  method='highs')
    assert out.success
    return out.fun


def main():
    rng = random.Random(546515)
    best = None
    best_individual = 0
    for j in range(150):
        k = 6 if j < 50 else 7 if j < 100 else 8
        cs = tuple(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), rng.randint(1,15))
                   for mask in range(1,1<<k) if mask.bit_count() <= 3 and rng.random() < .16)
        inst = Instance(tuple(map(str,range(k))), cs, 5)
        solver = ExactSPESolver(inst)
        candidates = list(solver.ordered_outcomes(min(solver.worst_outcomes())))
        rng.shuffle(candidates)
        for path in candidates[:25]:
            W = inst.welfare(inst.counts(path))
            M = value(menu_matrix(inst,path[:-1]))
            ratio = 5*M/W if W else 0
            profit = min(inst.player_payoffs(path))
            individual_ratio = M / float(profit) if profit else 0
            actual_extra = max(sum(c.multiplicity/(1+sum(a in c.topics for a in path))
                                   for c in inst.customers if t in c.topics)
                               for t in range(k))
            if actual_extra > float(profit)+1e-8:
                Path(__file__).with_name('pure_actual_extra_candidate.json').write_text(
                    json.dumps(dict(index=j, menu_value=M, W=W, minimum_profit=str(profit),
                                    actual_extra=actual_extra, path=path, game=inst.to_dict()),indent=2)+'\n')
                print('PURE ACTUAL EXTRA failure',j,actual_extra,profit,path,flush=True)
            if individual_ratio > best_individual:
                best_individual = individual_ratio
                print(json.dumps(dict(kind='individual-record', index=j,
                                     individual_ratio=individual_ratio, ratio=ratio,
                                     path=path, minimum_profit=str(profit), menu_value=M)),flush=True)
            if individual_ratio > 1+1e-8:
                target = Path(__file__).with_name('last_menu_individual_candidate.json')
                target.write_text(json.dumps(dict(index=j, ratio=ratio,
                    individual_ratio=individual_ratio, menu_value=M, W=W,
                    path=path, game=inst.to_dict()),indent=2)+'\n')
            if best is None or ratio > best['ratio']:
                best = dict(index=j, ratio=ratio, individual_ratio=individual_ratio,
                            minimum_profit=str(profit), menu_value=M, W=W, path=list(path),
                            game=inst.to_dict())
                print(json.dumps({key:val for key,val in best.items() if key != 'game'}), flush=True)
            if ratio > 1 + 1e-8:
                target = Path(__file__).with_name('last_menu_candidate.json')
                target.write_text(json.dumps(best,indent=2)+'\n')
                return
    Path(__file__).with_name('last_menu_probe.json').write_text(json.dumps(best,indent=2)+'\n')


if __name__ == '__main__':
    main()
