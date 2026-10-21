"""Attack the stronger common-monotone-submodular-moment half conjecture.

This is not a CAG counterexample search: accepted moment vectors need not have
nonnegative customer realizations. Full Markov policies specify actions at
every count prefix, hence at every ordered history. LP values are only reported
after direct Fraction feasibility checks. No claim of global LP optimality is
needed for this finite search.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import json
import random
import time
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent


def subsets(mask):
    r = mask
    while True:
        yield r
        if not r:
            return
        r = (r-1) & mask


def counts(total, p):
    if p == 1:
        yield (total,)
    else:
        for q0 in range(total+1):
            for r in counts(total-q0, p-1):
                yield (q0,)+r


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=5)
    parser.add_argument('--topics', type=int, default=7)
    parser.add_argument('--samples', type=int, default=40)
    parser.add_argument('--seed', type=int, default=749811)
    parser.add_argument('--output', default='submodular_probe.json')
    args = parser.parse_args()
    n, p = args.players, args.topics
    masks = [s for s in range(1, 1 << p) if s.bit_count() <= n]
    mi = {s: i for i, s in enumerate(masks)}
    dim = len(masks)
    zero = (F(0),)*dim
    def kr(s):
        if not s:
            return zero
        return tuple(F(i == mi[s]) for i in range(dim))
    def sub(a, b):
        return tuple(x-y for x, y in zip(a, b))
    @lru_cache(None)
    def payoff(q, a):
        support = sum(1 << b for b in range(p) if q[b])
        def f(typ):
            return F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
        row = [F(0)]*dim
        for s in subsets(support):
            if s:
                row[mi[s]] = -sum(((-1)**(s.bit_count()-d.bit_count())*f(support & ~d) for d in subsets(s)), F(0))
        return tuple(row)
    # Store only nonzero terms for utility evaluation during policy generation.
    sparse_payoff = {}
    for q in counts(n, p):
        for a in range(p):
            if q[a]:
                sparse_payoff[(q, a)] = [(i, v) for i, v in enumerate(payoff(q, a)) if v]
    base_rows = []
    for s in [0]+masks:
        if s.bit_count() < n:
            for a in range(p):
                if not s >> a & 1:
                    base_rows.append(sub(kr(s | (1 << a)), kr(s)))
        if s.bit_count() <= n-2:
            for a in range(p):
                if s >> a & 1:
                    continue
                for b in range(a+1, p):
                    if not s >> b & 1:
                        base_rows.append(tuple(x+y-z-w for x, y, z, w in zip(kr(s | (1 << a)), kr(s | (1 << b)), kr(s), kr(s | (1 << a) | (1 << b)))))
    rng = random.Random(args.seed)
    seen = set()
    records = []
    best = F(0)
    best_witness = None
    started = time.time()
    for sample in range(args.samples):
        # Sum of concave nondecreasing transforms of modular nonnegative terms.
        terms = []
        for _ in range(rng.randrange(3, 10)):
            weights = [rng.choice([0, 0, 1, 2, 3, 5, 8]) for a in range(p)]
            cap = rng.randint(1, max(1, sum(weights)))
            terms.append((weights, cap))
        c = tuple(F(sum(min(cap, sum(weights[a] for a in range(p) if s >> a & 1)) for weights, cap in terms)) for s in masks)
        assert all(dot(row, c) >= 0 for row in base_rows)
        if not any(c):
            continue
        terminal = {q: q for q in counts(n, p)}
        actions = {}
        for k in range(n-1, -1, -1):
            for q in counts(k, p):
                candidates = []
                for a in range(p):
                    child = tuple(q[b]+(a == b) for b in range(p))
                    z = terminal[child]
                    u = sum((v*c[i] for i, v in sparse_payoff[(z, a)]), F(0))
                    candidates.append((u, a, z))
                maximum = max(x[0] for x in candidates)
                _, a, z = rng.choice([x for x in candidates if x[0] == maximum])
                actions[q], terminal[q] = a, z
        key = tuple(actions[q] for k in range(n) for q in counts(k, p))
        if key in seen:
            continue
        seen.add(key)
        gamma = set()
        for q, a in actions.items():
            for b in range(p):
                child = tuple(q[d]+(b == d) for d in range(p))
                row = sub(payoff(terminal[q], a), payoff(terminal[child], b))
                if any(row):
                    gamma.add(row)
        gamma = sorted(gamma)
        assert all(dot(row, c) >= 0 for row in gamma)
        rows = base_rows+gamma
        root = terminal[(0,)*p]
        rootmask = sum(1 << a for a in range(p) if root[a])
        targets = sorted((sum(1 << a for a in chosen) for chosen in combinations(range(p), min(n, p))),
                         key=lambda s: c[mi[s]], reverse=True)
        matrix = -np.array(rows, dtype=float)
        eq = np.array([kr(rootmask)], dtype=float)
        sample_best = F(0)
        for target in targets:
            res = linprog(-np.array(kr(target), dtype=float), A_ub=matrix, b_ub=np.zeros(len(rows)),
                          A_eq=eq, b_eq=[1], bounds=(0, None), method='highs')
            if not res.success:
                continue
            w = tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
            if not (all(x >= 0 for x in w) and dot(kr(rootmask), w) == 1 and all(dot(row, w) >= 0 for row in rows)):
                continue
            value = w[mi[target]]
            sample_best = max(value, sample_best)
            if value > best:
                best = value
                best_witness = {'sample': sample, 'root': root, 'target': target,
                                'actions_by_counts': [{'q': q, 'a': a} for q, a in actions.items()],
                                'moments': {str(s): str(w[i]) for i, s in enumerate(masks) if w[i]},
                                'exact_value': str(value), 'true_customer_realizability': 'not_claimed'}
                print(json.dumps({'new_exact_feasible_value': str(value), 'sample': sample, 'target': target}), flush=True)
            if best > 2:
                break
        records.append({'sample': sample, 'distinct_policy': len(seen), 'gamma_rows': len(gamma), 'largest_exact_feasible_value': str(sample_best)})
        if best > 2:
            break
    out = {'players': n, 'topics': p, 'samples_requested': args.samples, 'seed': args.seed,
           'relaxation': 'one truncated monotone submodular C, common Shapley map, all full-history Markov-policy incentives; no dilution constraints',
           'general_half_status': 'OPEN', 'finite_policies': len(seen), 'records': records,
           'best_exact_feasible_value': str(best), 'best_witness': best_witness, 'elapsed_seconds': time.time()-started}
    (BASE/args.output).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('records', 'best_witness')}), flush=True)


if __name__ == '__main__':
    main()
