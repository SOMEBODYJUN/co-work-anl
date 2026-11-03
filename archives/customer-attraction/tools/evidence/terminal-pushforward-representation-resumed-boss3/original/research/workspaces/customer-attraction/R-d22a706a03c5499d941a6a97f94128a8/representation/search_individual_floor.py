"""Exploratory float SPE-cone alternation for UI-HALF (not a certificate)."""
import argparse
import json
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def search(p, m, seeds, rounds):
    rng = np.random.default_rng(842318)
    masks = np.arange(1, 1 << p)
    incidence = ((masks[:, None] >> np.arange(p)) & 1).astype(float)
    O = incidence[:, :m].max(axis=1)
    all_states = []

    def states(n, k):
        if k == 1:
            yield (n,)
        else:
            for a in range(n + 1):
                for tail in states(n - a, k - 1):
                    yield (a,) + tail

    terminal = list(states(m, p))
    q_index = {q: i for i, q in enumerate(terminal)}
    loads = incidence @ np.array(terminal).T
    payoff_rows = np.divide(incidence[:, None, :], loads[:, :, None],
                            out=np.zeros((len(masks), len(terminal), p)),
                            where=loads[:, :, None] != 0)
    best = 1.0
    for seed in range(seeds):
        w = rng.integers(0, 8, len(masks)).astype(float)
        w[rng.random(len(masks)) < .55] = 0
        for iteration in range(rounds):
            pay = np.einsum('t,tqa->qa', w, payoff_rows)
            children = {}
            floors = {}

            @lru_cache(None)
            def outcomes(q):
                if sum(q) == m:
                    return frozenset([q_index[q]])
                sons = []
                lo = []
                for a in range(p):
                    nextq = list(q)
                    nextq[a] += 1
                    son = outcomes(tuple(nextq))
                    sons.append(son)
                    lo.append(min(pay[j, a] for j in son))
                floor = max(lo)
                children[q] = sons
                floors[q] = floor
                return frozenset(j for a, son in enumerate(sons) for j in son
                                 if pay[j, a] >= floor - 1e-9)

            root = (0,) * p
            outcomes(root)
            acts = {}

            def expand(h, q, target):
                if len(h) == m:
                    return
                allowed = [a for a in range(p)
                           if target in children[q][a]
                           and pay[target, a] >= floors[q] - 1e-9]
                a = int(rng.choice(allowed))
                acts[h] = a
                for b in range(p):
                    nextq = list(q)
                    nextq[b] += 1
                    j = target if b == a else min(children[q][b], key=lambda j: pay[j, b])
                    expand(h + (b,), tuple(nextq), j)

            target, action = min(((j, a) for a in range(p) for j in children[root][a]
                                  if pay[j, a] >= floors[root] - 1e-9),
                                 key=lambda ja: pay[ja])
            # Root action must be chosen consistently with the minimizing pair.
            expand((), root, target)
            feasible_root = [a for a in range(p) if target in children[root][a]
                             and pay[target, a] >= floors[root] - 1e-9]
            action = min(feasible_root, key=lambda a: pay[target, a])
            acts[()] = action
            # Rebuild root children for the newly prescribed root action.
            for b in range(p):
                nextq = list(root)
                nextq[b] += 1
                j = target if b == action else min(children[root][b], key=lambda j: pay[j, b])
                expand((b,), tuple(nextq), j)

            G = []

            def tree(h):
                if len(h) == m:
                    q = tuple(h.count(a) for a in range(p))
                    return q_index[q]
                leaves = [tree(h + (a,)) for a in range(p)]
                a = acts[h]
                current = payoff_rows[:, leaves[a], a]
                for b in range(p):
                    if b != a:
                        G.append(current - payoff_rows[:, leaves[b], b])
                return leaves[a]

            actual = tree(())
            cost = payoff_rows[:, actual, action]
            result = linprog(cost, A_ub=-np.array(G), b_ub=np.zeros(len(G)),
                             A_eq=[O], b_eq=[1], bounds=(0, None), method='highs')
            if not result.success:
                print(json.dumps({'p': p, 'm': m, 'seed': seed, 'iteration': iteration,
                                  'failure': result.message}), flush=True)
                break
            w = result.x
            if result.fun < best - 1e-8:
                best = result.fun
                print(json.dumps({'p': p, 'm': m, 'seed': seed, 'iteration': iteration,
                                  'individual_ratio': best, 'target': 1/(2*m),
                                  'support': int(np.count_nonzero(w > 1e-8))}), flush=True)
                Path(__file__).with_name(f'individual_candidate_{p}_{m}.json').write_text(
                    json.dumps({'p': p, 'm': m, 'weights': w.tolist(),
                                'actions': [[list(h), a] for h, a in acts.items()],
                                'root_action': action, 'ratio': best}))
            if best < 1/(2*m) - 1e-7:
                return
            # A small perturbation changes the compatible equilibrium selector.
            if iteration % 3 == 2:
                w += 1e-7 * rng.random(len(w))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=int, default=7)
    parser.add_argument('--players', type=int, default=5)
    parser.add_argument('--seeds', type=int, default=8)
    parser.add_argument('--rounds', type=int, default=10)
    args = parser.parse_args()
    search(args.topics, args.players, args.seeds, args.rounds)
