"""Search genuine count-dependent six-player SPE with seven legal themes.

All customer masks have continuous nonnegative mass during LP search. Any
strict positive gap at a rational vertex can be scaled to unit customers.
The policy is defined on every count state (hence every ordered history),
and each IC row compares genuine recursively selected child outcomes.
"""
import argparse
import itertools
import json
import time

import numpy as np
from scipy.optimize import linprog


def count_vectors(k, n):
    states = [[] for _ in range(n + 1)]
    for d in range(n + 1):
        for xs in itertools.combinations_with_replacement(range(k), d):
            q = [0] * k
            for x in xs:
                q[x] += 1
            states[d].append(tuple(q))
    return states


class Game:
    def __init__(self, k=7, n=6):
        self.k, self.n = k, n
        self.masks = np.arange(1, 1 << k)
        self.hits = ((self.masks[:, None] & (1 << np.arange(k))) > 0).astype(float)
        states = count_vectors(k, n)
        self.states = [q for row in states for q in row]
        self.sid = {q: i for i, q in enumerate(self.states)}
        self.layers = [[self.sid[q] for q in layer] for layer in states]
        self.term = self.layers[-1]
        self.tid = {sid: ti for ti, sid in enumerate(self.term)}
        self.child = np.zeros((len(self.states), k), dtype=np.int32)
        for d in range(n):
            for s in self.layers[d]:
                q = self.states[s]
                for a in range(k):
                    qn = list(q)
                    qn[a] += 1
                    self.child[s, a] = self.sid[tuple(qn)]
        self.u = np.zeros((len(self.term), k, len(self.masks)), dtype=float)
        self.cover = np.zeros((len(self.term), len(self.masks)), dtype=float)
        for ti, sid in enumerate(self.term):
            q = np.array(self.states[sid])
            denom = self.hits @ q
            self.u[ti] = np.divide(self.hits.T, denom, out=np.zeros((k, len(self.masks))), where=denom > 0)
            self.cover[ti] = (denom > 0).astype(float)

    def solve_policy(self, weights, jitter=0, rng=None):
        rng = rng or np.random.default_rng(0)
        outcome = np.full(len(self.states), -1, dtype=np.int32)
        action = np.full(len(self.states), -1, dtype=np.int32)
        for s in self.term:
            outcome[s] = self.tid[s]
        for d in range(self.n - 1, -1, -1):
            for s in self.layers[d]:
                cand = outcome[self.child[s]]
                values = np.einsum('ij,j->i', self.u[cand, np.arange(self.k)], weights)
                if jitter:
                    values += rng.uniform(-jitter, jitter, self.k)
                a = int(np.argmax(values))
                action[s] = a
                outcome[s] = cand[a]
        return action, outcome

    def policy_lp(self, action, outcome, maxiter=100000):
        all_rows = []
        for d in range(self.n):
            for s in self.layers[d]:
                a = action[s]
                own = self.u[outcome[s], a]
                for v in range(self.k):
                    if v == a:
                        continue
                    alt = self.u[outcome[self.child[s, v]], v]
                    all_rows.append(alt - own)
        Aub = np.array(all_rows)
        actual_ti = outcome[0]
        best = None
        for omit in range(self.k):
            objective = 1 - (self.masks == (1 << omit)).astype(float) - 2 * self.cover[actual_ti]
            res = linprog(-objective, A_ub=Aub, b_ub=np.zeros(len(Aub)),
                          A_eq=np.ones((1, len(self.masks))), b_eq=np.array([1.0]),
                          bounds=(0, None), method='highs', options={'maxiter': maxiter})
            if not res.success:
                raise RuntimeError(res.message)
            gap = -res.fun
            if best is None or gap > best[0]:
                best = (gap, omit, res.x, actual_ti)
        return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=50)
    ap.add_argument('--seed', type=int, default=28491)
    ap.add_argument('--output', default='count_policy_lp_result.json')
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    g = Game()
    print('states', len(g.states), 'nonterm', len(g.states) - len(g.term), 'types', len(g.masks), flush=True)
    bestgap = -float('inf')
    begin = time.time()
    for t in range(args.trials):
        if t % 4 == 0:
            support = rng.choice(len(g.masks), size=rng.integers(7, 55), replace=False)
            w = np.zeros(len(g.masks))
            w[support] = rng.gamma(rng.uniform(0.2, 2), 1, len(support))
            w /= w.sum()
        elif t % 4 == 1:
            w = rng.gamma(0.1, 1, len(g.masks))
            w /= w.sum()
        elif t % 4 == 2:
            w = rng.gamma(1, 1, len(g.masks))
            w /= w.sum()
        else:
            # singleton-heavy starting games make low coverage equilibria possible
            w = rng.gamma(0.05, 1, len(g.masks))
            w[[i - 1 for i in (1 << np.arange(g.k))]] += rng.gamma(1, 1, g.k)
            w /= w.sum()
        act, out = g.solve_policy(w, rng=rng)
        gap, omit, x, ti = g.policy_lp(act, out)
        if gap > bestgap + 1e-9:
            bestgap = gap
            print('best', t, 'gap', round(gap, 9), 'time', round(time.time() - begin, 1),
                  'actual', g.states[g.term[ti]], 'omit', omit, 'support', sum(x > 1e-9), flush=True)
            with open(args.output, 'w') as f:
                json.dump({'seed': args.seed, 'trial': t, 'gap': gap, 'omit': omit,
                           'actual': g.states[g.term[ti]], 'weights': x.tolist(),
                           'action': act.tolist()}, f)
        if gap > 1e-8:
            break


if __name__ == '__main__':
    main()
