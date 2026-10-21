"""Independent exact set-valued backward induction; exploratory, not a proof.

All histories with a given action-count vector have the same *set* of attainable
SPE terminal count vectors. The selected continuation remains free at every
ordered history. Integer scaling L clears every final payoff denominator.
"""
import argparse
import functools
import hashlib
import json
import math
import random
import time


def solve(types, p, m):
    scale = math.lcm(*range(1, m + 1))

    @functools.lru_cache(None)
    def utils(c):
        load = [(mask, weight, sum(c[a] for a in range(p) if mask >> a & 1))
                for mask, weight in types]
        return tuple(sum(weight * (scale // n) for mask, weight, n in load
                         if n and mask >> a & 1)
                     for a in range(p))

    @functools.lru_cache(None)
    def rec(c):
        if sum(c) == m:
            return frozenset((c,))
        children = []
        threshold = 0
        for a in range(p):
            cc = list(c)
            cc[a] += 1
            outcomes = rec(tuple(cc))
            children.append(outcomes)
            threshold = max(threshold, min(utils(x)[a] for x in outcomes))
        return frozenset(x for a, outcomes in enumerate(children)
                         for x in outcomes if utils(x)[a] >= threshold)

    return rec((0,) * p), utils, scale


def instance(rng, mode):
    if mode == 'unit':
        # Exact replay of the initial 10,000-case exploration.
        m = rng.choice((3, 4, 5, 6))
        p = rng.randint(3, 6)
        n = rng.randint(3, 10)
        q = rng.randint(1, 4)
        sets = rng.sample(range(1, 1 << n), p - 1)
        types = {}
        for x in range(n):
            mask = sum(1 << a for a, s in enumerate(sets) if s >> x & 1)
            if mask:
                types[mask] = types.get(mask, 0) + 1
        types[1 << (p - 1)] = q
        return m, p, q, sorted(types.items())
    m = rng.choice((3, 4, 5, 6, 7))
    p = rng.randint(3, 7)
    q = rng.randint(1, 30)
    types = [(mask, rng.randint(1, 30)) for mask in range(1, 1 << (p - 1))
             if rng.random() < rng.choice((0.15, 0.3, 0.6, 1.0))]
    types.append((1 << (p - 1), q))
    return m, p, q, types


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=1301)
    ap.add_argument('--cases', type=int, default=10000)
    ap.add_argument('--mode', choices=('unit', 'weighted'), default='unit')
    ap.add_argument('--output')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    digest = hashlib.sha256()
    start = time.monotonic()
    stats = {'seed': args.seed, 'requested_cases': args.cases, 'mode': args.mode,
             'tested_cases': 0, 'unused_P_terminal_vectors': 0,
             'used_C_action_checks': 0, 'counterexample': None}
    for case in range(args.cases):
        m, p, q, types = instance(rng, args.mode)
        leaves, utils, scale = solve(types, p, m)
        digest.update(json.dumps([m, p, q, types], separators=(',', ':')).encode())
        digest.update(b'\n')
        stats['tested_cases'] += 1
        for c in leaves:
            if c[-1]:
                continue
            stats['unused_P_terminal_vectors'] += 1
            values = utils(c)
            for a in range(p - 1):
                if c[a]:
                    stats['used_C_action_checks'] += 1
                    if values[a] < q * scale:
                        stats['counterexample'] = {
                            'case': case, 'm': m, 'p': p, 'q': q,
                            'types': types, 'terminal_counts': c,
                            'payoffs_scaled': values, 'scale': scale}
                        break
            if stats['counterexample']:
                break
        if stats['counterexample']:
            break
    stats['input_sha256'] = digest.hexdigest()
    stats['elapsed_seconds'] = round(time.monotonic() - start, 3)
    text = json.dumps(stats, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
