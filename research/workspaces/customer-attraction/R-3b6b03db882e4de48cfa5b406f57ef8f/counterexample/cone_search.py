"""Finite SPE cone attack; floats generate candidates, integer rows retain exact semantics.

The selected strategy is fully history dependent: a memoized pair (prefix counts,
desired terminal) is expanded to each ordered history independently. No count-only
policy restriction is imposed. This program does not certify floating LP points.
"""
import argparse
from functools import lru_cache
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for x in range(n + 1):
            for tail in compositions(n - x, k - 1):
                yield (x,) + tail


class Game:
    def __init__(self, k, m):
        self.k, self.m = k, m
        self.scale = lcm(*range(1, m + 1))
        self.types = np.arange(1, 1 << k)
        self.inc = ((self.types[:, None] >> np.arange(k)) & 1).astype(np.int16)
        self.states = [list(compositions(n, k)) for n in range(m + 1)]
        self.terminals = self.states[m]
        self.tidx = {q: i for i, q in enumerate(self.terminals)}
        qarray = np.array(self.terminals)
        denominators = qarray @ self.inc.T
        inv = np.zeros(denominators.shape, dtype=np.int16)
        np.floor_divide(self.scale, denominators, out=inv, where=denominators != 0)
        self.pay = inv[:, None, :] * self.inc.T[None, :, :]
        self.cov = (denominators > 0).astype(np.int16)
        self.children = {}
        for layer in self.states[:-1]:
            for q in layer:
                self.children[q] = [q[:a] + (q[a] + 1,) + q[a + 1:] for a in range(k)]
        self.opt_supports = list(combinations(range(k), min(k, m)))
        self.opt_rows = np.array([(self.inc[:, support].sum(axis=1) > 0).astype(int)
                                  for support in self.opt_supports])

    def solve(self, weights, rng, tol=2e-8):
        values = self.pay @ weights / self.scale
        welfare = self.cov @ weights
        outcomes = {q: np.array([self.tidx[q]], dtype=int) for q in self.terminals}
        floors = {}
        for layer in reversed(self.states[:-1]):
            for q in layer:
                kids = [outcomes[c] for c in self.children[q]]
                floor = max(values[ids, a].min() for a, ids in enumerate(kids))
                floors[q] = floor
                outcomes[q] = np.unique(np.concatenate([ids[values[ids, a] >= floor - tol]
                                                       for a, ids in enumerate(kids)]))
        root = (0,) * self.k
        outs = outcomes[root]
        worst = np.min(welfare[outs])
        targets = outs[welfare[outs] <= worst + tol]
        target = int(rng.choice(targets))
        return values, welfare, outcomes, floors, target

    def cone(self, weights, rng, target_mode='worst', forced_target=None, forced_path=None):
        values, welfare, outcomes, floors, target = self.solve(weights, rng)
        root = (0,) * self.k
        if target_mode == 'random':
            target = int(rng.choice(outcomes[root]))
        elif target_mode == 'second':
            outs = outcomes[root]
            minimum = min(welfare[outs])
            candidates = outs[welfare[outs] > minimum + 2e-8]
            if len(candidates):
                target = int(rng.choice(candidates))
        if forced_target is not None:
            target = forced_target
        planned = {}
        q_plan = root
        for a in forced_path or ():
            planned[q_plan] = a
            q_plan = self.children[q_plan][a]
        rows = []
        choices = {}

        @lru_cache(None)
        def expand(q, desired):
            if sum(q) == self.m:
                return
            kids = self.children[q]
            admissible = [a for a, c in enumerate(kids)
                          if desired in outcomes[c] and values[desired, a] >= floors[q] - 2e-8]
            action = planned[q] if desired == target and q in planned else int(rng.choice(admissible))
            assert action in admissible
            next_targets = []
            for a, c in enumerate(kids):
                if a == action:
                    new = desired
                else:
                    ids = outcomes[c]
                    low = values[ids, a].min()
                    possibles = ids[values[ids, a] <= low + 2e-8]
                    # Prefer a large continuation coverage, punishing the mover
                    # without automatically concentrating all other players.
                    new = int(rng.choice(possibles))
                    row = self.pay[desired, action] - self.pay[new, a]
                    if row.any():
                        rows.append(row)
                next_targets.append(new)
                expand(c, new)
            choices[q, desired] = (action, tuple(next_targets))

        expand(root, target)
        matrix = np.unique(np.array(rows, dtype=np.int16), axis=0)
        return matrix, target, choices, float(welfare[target]), float(max(self.opt_rows @ weights))

    def optimize(self, matrix, target, objective, private_floor=0.):
        bounds = [(0, None)] * len(self.types)
        for a in range(self.k):
            bounds[(1 << a) - 1] = (private_floor, None)
        return linprog(-objective.astype(float), A_ub=-matrix.astype(float),
                       b_ub=np.zeros(len(matrix)), A_eq=[self.cov[target]], b_eq=[1.],
                       bounds=bounds, method='highs')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--starts', type=int, default=10)
    ap.add_argument('--steps', type=int, default=8)
    ap.add_argument('--seed', type=int, default=41236)
    ap.add_argument('--target-mode', choices=['worst', 'random', 'second'], default='worst')
    ap.add_argument('--private-floor', type=float, default=0.)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    game = Game(args.topics, args.players)
    rng = np.random.default_rng(args.seed)
    best, records = 0., []
    for start in range(args.starts):
        if start % 3 == 0:
            weights = np.zeros(len(game.types))
            weights[0] = args.players
            for a in range(1, args.topics):
                weights[(1 << a) - 1] = 1.
            weights += rng.random(len(weights)) * (0 if start == 0 else .02)
        elif start % 3 == 1:
            weights = rng.exponential(1, len(game.types))
            weights[rng.random(len(weights)) < .9] = 0
        else:
            weights = rng.exponential(1, len(game.types))
            weights *= np.exp(-game.inc.sum(axis=1))
        seen = set()
        for step in range(args.steps):
            tic = time.time()
            matrix, target, choices, w, opt = game.cone(weights, rng, args.target_mode if step == 0 else 'worst')
            true_ratio = opt / w if w else 1.
            # Pick current best optimum; try two other supports to escape ties.
            support_values = game.opt_rows @ weights
            indices = [int(np.argmax(support_values))]
            indices += list(map(int, rng.choice(len(game.opt_rows), min(2, len(game.opt_rows)), replace=False)))
            candidates = []
            for idx in indices:
                result = game.optimize(matrix, target, game.opt_rows[idx], args.private_floor)
                if result.success:
                    new_values = game.opt_rows @ result.x
                    candidates.append((max(new_values), result, int(np.argmax(new_values))))
            if not candidates:
                print(json.dumps({'start': start, 'step': step, 'status': 'no feasible LP with private floor'}), flush=True)
                break
            ratio, result, idx = max(candidates, key=lambda t: t[0])
            record = {'start': start, 'step': step, 'incoming_ratio': true_ratio,
                      'ratio': ratio, 'target': game.terminals[target],
                      'rows': len(matrix), 'states': len(choices), 'seconds': time.time() - tic}
            records.append(record)
            print(json.dumps(record), flush=True)
            if ratio > best + 1e-8:
                best = ratio
                payload = {'topics': args.topics, 'players': args.players, 'seed': args.seed,
                           'status': 'floating candidate, not certified', 'record': record,
                           'weights': result.x.tolist(), 'support': game.opt_supports[idx],
                           'choices': [{'prefix': q, 'target': d, 'action': a, 'children': children}
                                       for (q, d), (a, children) in choices.items()],
                           'records': records}
                args.output.write_text(json.dumps(payload))
            weights = result.x
            signature = tuple(np.rint(weights * 1e7).astype(int))
            if signature in seen and step > 2:
                break
            seen.add(signature)
    print(json.dumps({'best': best, 'LPs': 3 * len(records)}), flush=True)


if __name__ == '__main__':
    main()
