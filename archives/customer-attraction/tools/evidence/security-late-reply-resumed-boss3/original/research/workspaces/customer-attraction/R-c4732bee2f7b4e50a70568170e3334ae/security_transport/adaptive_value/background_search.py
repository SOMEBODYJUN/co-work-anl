"""Exploration only: aggregate static security for arbitrary fixed incumbents.

This enlarges the background class beyond root instances. Float computations
discover candidates; they do not certify exact inequalities.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json
import random
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def run(seed=173, iterations=10000, topics=6, players=3):
    rng = random.Random(seed)
    types = np.array([[int(mask >> a & 1) for a in range(topics)]
                      for mask in range(1, 1 << topics)], dtype=float)
    terms = list(combinations_with_replacement(range(topics), players))
    backs = list(combinations_with_replacement(range(topics), players - 1))
    tcounts = np.array([[z.count(a) for a in range(topics)] for z in terms])
    bcounts = np.array([[z.count(a) for a in range(topics)] for z in backs])
    loads = tcounts @ types.T
    bloads = bcounts @ types.T
    best = 100.
    for iteration in range(iterations):
        weights = np.array([rng.randint(0, 10) if rng.random() < .4 else 0
                            for _ in range(len(types))], dtype=float)
        # Arbitrary external load is deliberately an enlarged, auxiliary model.
        background = np.array([rng.randrange(8) for _ in range(len(types))])
        payoff = ((weights / np.where(loads > 0, background + loads, 1)) @ types)
        payoff *= (tcounts > 0)
        welfare = np.sum(weights * loads / np.where(loads > 0, background + loads, 1), axis=1)
        terminal_id = {tuple(c): i for i, c in enumerate(tcounts)}

        @lru_cache(None)
        def outcomes(prefix):
            if sum(prefix) == players:
                return frozenset([terminal_id[prefix]])
            children = []
            for a in range(topics):
                child = list(prefix)
                child[a] += 1
                children.append(outcomes(tuple(child)))
            floor = max(min(payoff[j, a] for j in child)
                        for a, child in enumerate(children))
            return frozenset(j for a, child in enumerate(children) for j in child
                             if payoff[j, a] >= floor - 1e-10)

        outs = outcomes((0,) * topics)
        worst = min(outs, key=lambda i: welfare[i])
        matrix = ((weights / (background + 1 + bloads)) @ types)
        lp = linprog(np.r_[np.zeros(topics), -1],
                     A_ub=np.c_[-matrix, np.ones(len(backs))],
                     b_ub=np.zeros(len(backs)),
                     A_eq=np.array([[1] * topics + [0]]), b_eq=[1],
                     bounds=[(0, None)] * topics + [(None, None)], method='highs')
        if not lp.success:
            raise RuntimeError(lp.message)
        value = lp.x[-1]
        ratio = welfare[worst] / value if value else float('inf')
        if ratio < best:
            best = ratio
            print(iteration, 'ratio', ratio, 'target', players, flush=True)
            data = {'seed': seed, 'iteration': iteration, 'topics': topics,
                    'players': players, 'rows': [dict(mask=i+1, weight=int(w),
                    background=int(b)) for i, (w, b) in enumerate(zip(weights, background)) if w],
                    'terminal': terms[worst], 'remaining_total': float(welfare[worst]),
                    'static_value_float': value, 'query_float': lp.x[:-1].tolist(),
                    'ratio_float': ratio}
            Path(__file__).with_name('background_search_best.json').write_text(json.dumps(data, indent=2))
        if ratio < players - 1e-7:
            break
    return best


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=10000)
    parser.add_argument('--seed', type=int, default=173)
    parser.add_argument('--topics', type=int, default=6)
    parser.add_argument('--players', type=int, default=3)
    args = parser.parse_args()
    run(args.seed, args.iterations, args.topics, args.players)
