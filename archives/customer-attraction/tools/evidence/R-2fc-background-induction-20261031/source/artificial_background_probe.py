"""Attack P+Delta under artificial loads not represented by legal past topics.

This intentionally broadens the input class. Any discovered failure would be
an interface/quantifier obstruction, not a counterexample to the legal model.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import random
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).parent


def probe(q, trials, seed):
    rng = random.Random(seed)
    kinds = [(mask, b) for mask in range(1, 1 << q) for b in (0, 1, 2, 5)]
    member = np.array([[(mask >> a) & 1 for a in range(q)] for mask, _ in kinds])
    bg = np.array([b for _, b in kinds])
    fresh = (bg == 0).astype(float)
    coefficients = {}
    for a, b in product(range(q), repeat=2):
        total = bg + member[:, a] + member[:, b]
        coefficients[(a, b)] = np.divide(member, total[:, None], out=np.zeros(member.shape),
                                         where=total[:, None] != 0)
    for trial in range(trials):
        weights = np.array([rng.randrange(20) if rng.random() < .2 else 0 for _ in kinds])
        reply = []
        for a in range(q):
            vals = [coefficients[a, b][:, b] @ weights for b in range(q)]
            top = max(vals)
            reply.append(rng.choice([b for b in range(q) if abs(vals[b] - top) < 1e-8]))
        vals = [coefficients[a, reply[a]][:, a] @ weights for a in range(q)]
        top = max(vals)
        first = rng.choice([a for a in range(q) if abs(vals[a] - top) < 1e-8])
        last = reply[first]
        rows = []
        for a in range(q):
            on = coefficients[a, reply[a]][:, reply[a]]
            for t in range(q):
                rows.append(on - coefficients[a, t][:, t])
        on = coefficients[first, last][:, first]
        for t in range(q):
            rows.append(on - coefficients[t, reply[t]][:, t])
        rows = np.array(rows)
        profit = coefficients[first, last][:, first] + coefficients[first, last][:, last]
        new = fresh * (member[:, first] + member[:, last] > 0)
        for comp in combinations(range(q), 2):
            obj = profit + new - fresh * (member[:, comp].sum(axis=1) > 0)
            res = linprog(obj, A_ub=-rows, b_ub=np.zeros(len(rows)),
                          A_eq=[np.ones(len(kinds))], b_eq=[1.0], bounds=(0, None), method='highs')
            if res.success and res.fun < -1e-8:
                data = dict(scope='Artificial independent backgrounds only; not legal-model counterexample',
                            q=q, remaining=2, first=first, reply=reply, comparison=comp,
                            weights=[[mask, b, float(v)] for (mask, b), v in zip(kinds, res.x) if v > 1e-9],
                            objective=float(res.fun), seed=seed, trial=trial)
                (HERE / 'artificial_background_candidate.json').write_text(json.dumps(data, indent=2) + '\n')
                print('FOUND', json.dumps(data, indent=2), flush=True)
                return
        if trial % 25 == 0:
            print('trial', trial, 'no negative candidate', flush=True)
    print('completed', trials, 'no negative candidate', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', type=int, default=6)
    parser.add_argument('--trials', type=int, default=200)
    parser.add_argument('--seed', type=int, default=982327)
    args = parser.parse_args()
    probe(args.q, args.trials, args.seed)
