"""Reproducible exploratory search; never treats a floating result as an SPE proof."""
import argparse
import json
import random
import time

from six_1.spe_dp import solve


def sample(rng, n):
    weights = [0] * (1 << n)
    classes = rng.choices(range(1, n + 1), weights=[5, 9, 7, 4, 2, 1, 1][:n], k=1)[0]
    density = rng.choice((0.1, 0.2, 0.35, 0.5, 0.75, 1.0))
    for mask in range(1, 1 << n):
        size = mask.bit_count()
        if rng.random() < density * (2 ** (-abs(size - classes))):
            weights[mask] = rng.choice([1, 2, 3, 5, 8, 13, 21, 34, 55])
    for a in range(n):
        if not any(w and mask & (1 << a) for mask, w in enumerate(weights)):
            weights[1 << a] = rng.randint(1, 13)
    return weights


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', type=int, default=981773)
    p.add_argument('--count', type=int, default=1000)
    p.add_argument('--topics', type=int, default=7)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    rng = random.Random(args.seed)
    best = (1.0, None, None)
    start = time.time()
    for trial in range(args.count):
        w = sample(rng, args.topics)
        result = solve(w)
        ratio = float(result['ratio'])
        if ratio < best[0]:
            best = (ratio, w, result)
            print(trial, ratio, 'W', result['min_welfare'], 'O', result['optimum'], 'time', round(time.time()-start, 1), flush=True)
            with open(args.out, 'w') as f:
                json.dump({'seed': args.seed, 'trial': trial, 'weights': w,
                           'ratio': ratio, 'result': result}, f, indent=2,
                          default=lambda o: int(o))
    print('done', best[0], 'seconds', time.time()-start, flush=True)


if __name__ == '__main__':
    main()
