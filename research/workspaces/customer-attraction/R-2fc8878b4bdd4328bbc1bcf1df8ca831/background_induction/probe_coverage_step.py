"""Exact finite probe of a stronger first-step coverage opportunity condition.

This is a search, not a proof. It preserves all root actions and terminal SPE
outcomes of each child through the set-valued background solver.
"""
import importlib.util
import json
from pathlib import Path
from fractions import Fraction
import random
import argparse

HERE = Path(__file__).parent
REPO = HERE.parents[4]
SOURCE = REPO / "research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py"
spec = importlib.util.spec_from_file_location("background_oracle", SOURCE)
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


def audit(q, r, prefix, weights):
    sol = oracle.BackgroundSolver(q, r, prefix, weights)
    bgmask = sum(1 << a for a in range(q) if prefix[a])
    fresh = {mask: w for mask, w in weights.items() if not mask & bgmask}
    best_new = max(
        sum(w for mask, w in fresh.items() if any(c[a] and mask >> a & 1 for a in range(q)))
        for c in sol.terminals
    )
    best = None
    witness = None
    for a in range(q):
        first = sum(w for mask, w in fresh.items() if mask >> a & 1)
        remain = {mask: w for mask, w in fresh.items() if not mask >> a & 1}
        remopt = max(
            sum(w for mask, w in remain.items() if any(c[z] and mask >> z & 1 for z in range(q)))
            for c in oracle.compositions(r - 1, q)
        )
        e = tuple(int(z == a) for z in range(q))
        child = sol.solve(e)
        while child:
            bit = child & -child
            child -= bit
            idx = bit.bit_length() - 1
            pay = sol.pays[idx][a]
            if pay < sol.thresholds[(0,) * q]:
                continue
            u = Fraction(pay, sol.scale)
            gap = u + first + remopt - best_new
            if best is None or gap < best:
                best = gap
                witness = dict(q=q, r=r, prefix=prefix, weights=weights, first=a,
                               terminal=sol.terminals[idx], u=str(u), new_first=first,
                               remopt=remopt, opt_new=best_new, gap=str(gap))
    return best, witness


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--q", type=int, default=6)
    p.add_argument("--r", type=int, default=4)
    p.add_argument("--trials", type=int, default=1000)
    p.add_argument("--seed", type=int, default=9137007)
    args = p.parse_args()
    rng = random.Random(args.seed)
    best = None
    for trial in range(args.trials):
        prefix = [0] * args.q
        for _ in range(rng.randrange(5)):
            prefix[rng.randrange(args.q)] += 1
        masks = rng.sample(range(1, 1 << args.q), rng.randrange(args.q, min(3 * args.q, 1 << args.q)))
        weights = {mask: rng.randrange(1, 25) for mask in masks}
        gap, witness = audit(args.q, args.r, prefix, weights)
        if best is None or gap < best:
            best = gap
            print(trial, str(best), flush=True)
        if gap < 0:
            witness.update(trial=trial, seed=args.seed,
                           scope="Counterexample to the first-step sufficient condition only")
            (HERE / "coverage_step_counterexample.json").write_text(json.dumps(witness, indent=2) + "\n")
            print(json.dumps(witness, indent=2))
            break
