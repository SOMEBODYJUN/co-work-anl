"""Inverse LP attack. Positive optima require a separate exact certificate check."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import random
import sys

import numpy as np
from scipy.optimize import linprog

from customer_attraction import CustomerType, Instance, ExactSPESolver, verify_certificate


def payoff_row(signatures, history, action):
    return np.array([float(Fraction(1, sum(a in sig for a in history)))
                     if action in sig else 0.0 for sig in signatures])


def continue_from(history, cert, m):
    while len(history) < m:
        history += (cert.actions[history],)
    return history


def attack(instance, solver, terminal):
    k, m = instance.topic_count, instance.players
    signatures = [frozenset(a) for r in (1, 2) for a in combinations(range(k), r)]
    cert = solver.certificate(terminal)
    root_path = continue_from((), cert, m)
    root_row = payoff_row(signatures, root_path, root_path[0])
    rows = []
    for history, chosen in cert.actions.items():
        lhs = payoff_row(signatures, continue_from(history, cert, m), chosen)
        for action in range(k):
            rhs = payoff_row(signatures, continue_from(history + (action,), cert, m), action)
            rows.append(np.r_[rhs - lhs, 0.0])
    weights = np.array([next((c.multiplicity for c in instance.customers if c.topics == sig), 0)
                        for sig in signatures])
    for prefix in product(range(k), repeat=m-1):
        witness_rows = [payoff_row(signatures, prefix + (a,), a) for a in range(k)]
        witness = max(witness_rows, key=lambda row: row @ weights)
        rows.append(np.r_[-witness, 1.0])
    objective = np.r_[root_row, -1.0]
    lp = linprog(objective, A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                 A_eq=np.array([np.r_[np.ones(len(signatures)), 0.0]]), b_eq=np.array([1.0]),
                 bounds=[(0, None)] * (len(signatures)+1), method='highs')
    if lp.success and lp.fun < -1e-8:
        rational = [Fraction(float(x)).limit_denominator(100000) for x in lp.x[:-1]]
        import math
        scale = math.lcm(*(x.denominator for x in rational))
        customers = tuple(CustomerType(sig, int(x * scale))
                          for sig, x in zip(signatures, rational) if x)
        new = Instance(instance.topics, customers, m)
        report = verify_certificate(new, cert)
        exact = ExactSPESolver(new)
        exact.outcomes()
        theta = min(exact.threshold(q) for q in exact._outcomes if sum(q) == m-1)
        root_utility = new.player_payoffs(root_path)[0]
        return {'lp_gap': -lp.fun, 'instance': new.to_dict(), 'theta': str(theta),
                'root_utility': str(root_utility), 'path': root_path,
                'certificate_valid': report.valid, 'exact_gap': str(theta-root_utility),
                'certificate': cert.to_dict()}
    return None


def main():
    rng = random.Random(683591)
    count = 0
    for k, m, samples in [(4,3,300), (5,3,300), (6,3,500), (5,4,300), (6,4,300)]:
        signatures = [frozenset(a) for r in (1, 2) for a in combinations(range(k), r)]
        for sample in range(samples):
            customers = tuple(CustomerType(signature, rng.randint(1,20))
                              for signature in signatures if rng.random() < .6)
            instance = Instance(tuple(map(str, range(k))), customers, m)
            solver = ExactSPESolver(instance)
            for terminal in solver.outcomes():
                count += 1
                result = attack(instance, solver, terminal)
                if result is not None:
                    print(json.dumps(result), flush=True)
                    Path(sys.argv[1]).write_text(json.dumps({'attacks':count,'result':result},indent=2)+'\n')
                    return
        print('complete',k,m,samples,count,flush=True)
    Path(sys.argv[1]).write_text(json.dumps({'attacks':count,'result':None},indent=2)+'\n')


if __name__ == '__main__':
    main()
