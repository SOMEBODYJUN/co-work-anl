#!/usr/bin/env python3
"""Finite extra full-SPE cone attack for the static optimal matching candidate."""
from collections import Counter
from functools import lru_cache
from itertools import product
from math import lcm
from pathlib import Path
import json
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_static_opt_matching import StrategyCone, try_cone, root_path


def random_spe(p, m, w, rng):
    scale = lcm(*range(1, m + 1))
    types = [(mask, v) for mask, v in enumerate(w, 1) if v]
    @lru_cache(None)
    def payoff(q, a):
        bit = 1 << a
        return sum(v * (scale // sum(q[t] for t in range(p) if mask & (1 << t)))
                   for mask, v in types if mask & bit)
    terminal = {h: tuple(h.count(t) for t in range(p)) for h in product(range(p), repeat=m)}
    actions = {}
    for depth in range(m - 1, -1, -1):
        for h in product(range(p), repeat=depth):
            values = [payoff(terminal[h + (a,)], a) for a in range(p)]
            best = max(values)
            a = rng.choice([a for a, v in enumerate(values) if v == best])
            actions[h] = a
            terminal[h] = terminal[h + (a,)]
    return actions


def main():
    rng = random.Random(87129)
    processed = 0
    seen = set()
    start = time.time()
    for p, m, trials in [(3, 3, 100), (4, 4, 100), (5, 4, 120), (6, 4, 100)]:
        for j in range(trials):
            # Sparse rational-customer cones and ties, rather than dense generic NE.
            weights = [0] * (2**p - 1)
            for _ in range(rng.randrange(2, 10)):
                weights[rng.randrange(len(weights))] += rng.choice([1, 1, 2, 3])
            w = tuple(weights)
            actions = random_spe(p, m, w, rng)
            signature = tuple(sorted(actions.items()))
            if signature in seen:
                continue
            seen.add(signature)
            cone = StrategyCone(p, m, actions)
            assert cone.verify(w)
            root = root_path(actions, m)
            # Spend LP work on genuine non-PNE actual outcomes.
            q = tuple(root.count(a) for a in range(p))
            def direct(a, counts):
                return sum(v / sum(counts[t] for t in range(p) if mask & (1 << t))
                           for mask, v in enumerate(w, 1) if v and mask & (1 << a))
            non_ne = False
            for i, old in enumerate(root):
                old_u = direct(old, q)
                for a in range(p):
                    changed = list(q)
                    changed[old] -= 1
                    changed[a] += 1
                    if direct(a, changed) > old_u + 1e-8:
                        non_ne = True
                        break
            if not non_ne:
                continue
            processed += 1
            print(json.dumps({'cone': processed, 'p': p, 'm': m, 'trial': j,
                              'root': root, 'elapsed': round(time.time()-start,2)}), flush=True)
            found = try_cone(cone)
            if found:
                found['source_cone'] = {'random_seed': 87129, 'trial': j,
                                        'players': m, 'topics': p, 'seed_weights': w}
                target = Path(__file__).with_name('static_opt_matching_counterexample.json')
                target.write_text(json.dumps(found, indent=2) + '\n')
                print(json.dumps({'counterexample': str(target), 'matching': found['best_static_matching']}), flush=True)
                return
    print(json.dumps({'status': 'no_exact_counterexample_in_processed_cones',
                      'processed_nonPNE_cones': processed, 'elapsed': time.time()-start}))


if __name__ == '__main__':
    main()
