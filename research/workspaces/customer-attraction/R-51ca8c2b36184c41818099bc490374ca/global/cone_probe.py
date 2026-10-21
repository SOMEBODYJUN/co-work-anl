"""LP diagnostics for fixed complete strategies; no float result is a theorem."""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def arrays(instance, certificate):
    k, m = instance.topic_count, instance.players
    membership = np.array([[int(mask & (1 << a) != 0) for a in range(k)]
                           for mask in range(1, 1 << k)])
    branches = {}
    rows = []
    def utility(counts, action):
        loads = membership @ counts
        return np.divide(membership[:, action], loads,
                         out=np.zeros(len(loads)), where=loads != 0)
    def walk(history):
        if len(history) == m:
            return np.bincount(history, minlength=k)
        options = [walk(history + (a,)) for a in range(k)]
        chosen = certificate.actions[history]
        chosen_utility = utility(options[chosen], chosen)
        for a in range(k):
            rows.append(chosen_utility - utility(options[a], a))
            branches[history, a] = utility(options[a], a)
        return options[chosen]
    actual = walk(())
    c = (membership @ actual != 0).astype(float)
    v = np.zeros((k, len(c)))
    history = ()
    while len(history) < m:
        for a in range(k):
            v[a] += branches[history, a]
        history += (certificate.actions[history],)
    return np.asarray(rows), c, v, membership


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--players', type=int, default=3)
    p.add_argument('--topics', type=int, default=5)
    p.add_argument('--samples', type=int, default=100)
    p.add_argument('--seed', type=int, default=90230)
    p.add_argument('--output')
    args = p.parse_args()
    rng = random.Random(args.seed)
    global_best = float('inf')
    for sample in range(args.samples):
        customers = []
        for mask in range(1, 1 << args.topics):
            # Private and pair clients receive higher probability than dense types.
            size = mask.bit_count()
            weight = rng.randrange(0, 9) if size <= 2 else rng.choice([0, 0, 0, 1, 2])
            if weight:
                customers.append(CustomerType(frozenset(a for a in range(args.topics)
                                                       if mask & (1 << a)), weight))
        instance = Instance(tuple(map(str, range(args.topics))), tuple(customers), args.players)
        solver = ExactSPESolver(instance)
        targets = sorted(solver.outcomes(), key=instance.welfare)[:3]
        for target in targets:
            certificate = solver.certificate(target)
            gamma, c, v, membership = arrays(instance, certificate)
            for support in combinations(range(args.topics), min(args.players, args.topics)):
                o = (membership[:, support].sum(axis=1) != 0).astype(float)
                obj = (args.players - 1) * c + v[list(support)].sum(axis=0) - args.players * o
                lp = linprog(obj, A_ub=-gamma, b_ub=np.zeros(len(gamma)),
                             A_eq=[c], b_eq=[1], bounds=(0, None), method='highs')
                if not lp.success:
                    raise RuntimeError(lp.message)
                if lp.fun < global_best - 1e-8:
                    global_best = lp.fun
                    print(json.dumps({'sample': sample, 'slack': lp.fun,
                                      'actual': list(target), 'portfolio': support}), flush=True)
                if lp.fun < -1e-7:
                    weights = [Fraction(float(w)).limit_denominator(1000000) for w in lp.x]
                    output = {'m': args.players, 'k': args.topics, 'portfolio': support,
                              'float_slack': lp.fun, 'weights': [str(w) for w in weights],
                              'certificate': certificate.to_dict()}
                    if args.output:
                        Path(args.output).write_text(json.dumps(output, indent=2) + '\n')
                    return


if __name__ == '__main__':
    main()
