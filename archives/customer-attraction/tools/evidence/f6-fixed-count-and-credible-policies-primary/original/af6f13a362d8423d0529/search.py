"""Exploratory fixed-policy/fixed-query LPs for the aggregate security bridge.

Floating discovery only. A positive gap must be separately recovered over Q.
No finite search proves a universal inequality. Writes only to this workspace.
"""
import argparse
from functools import lru_cache
from itertools import product, combinations_with_replacement
import json
from pathlib import Path
import time
import numpy as np
from scipy.optimize import linprog


def prepare(k, n):
    masks = np.arange(1, 1 << k)
    incidence = ((masks[:, None] >> np.arange(k)) & 1).astype(float)
    histories = [h for d in range(n + 1) for h in product(range(k), repeat=d)]
    decisions = histories[:-k ** n]
    counts = {h: np.bincount(h, minlength=k) for h in histories}
    @lru_cache(None)
    def payoff(c, a):
        denominator = incidence @ np.array(c)
        return np.divide(incidence[:, a], denominator, out=np.zeros(len(masks)), where=denominator > 0)
    backgrounds = []
    for tup in combinations_with_replacement(range(k), n - 1):
        c = np.bincount(tup, minlength=k)
        denominator = 1 + incidence @ c
        backgrounds.append(incidence / denominator[:, None])
    return incidence, histories, decisions, counts, payoff, np.array(backgrounds)


def cone(actions, data, k, n):
    incidence, histories, decisions, counts, payoff, _ = data
    terminal = {h: tuple(map(int, counts[h])) for h in histories if len(h) == n}
    rows = []
    for h in reversed(decisions):
        a = actions[h]
        terminal[h] = terminal[h + (a,)]
        own = payoff(terminal[h], a)
        rows.extend(own - payoff(terminal[h + (b,)], b) for b in range(k) if b != a)
    G = np.unique(np.round(rows, 12), axis=0)
    c = (incidence @ np.array(terminal[()]) > 0).astype(float)
    return G, c, terminal


def lp(G, c, beta, n):
    # Normalize root welfare, not total mass. This avoids all-interest shrinking.
    d = len(c)
    result = linprog(np.r_[np.zeros(d), -n],
        A_ub=np.vstack([np.c_[-G, np.zeros(len(G))], np.c_[-beta, np.ones(len(beta))]]),
        b_ub=np.zeros(len(G) + len(beta)), A_eq=np.array([np.r_[c, 0]]), b_eq=[1],
        bounds=[(0, None)] * (d + 1), method='highs')
    return result


def safety(w, backgrounds):
    matrix = backgrounds.transpose(0, 2, 1) @ w
    k = matrix.shape[1]
    result = linprog(np.r_[np.zeros(k), -1], A_ub=np.c_[-matrix, np.ones(len(matrix))],
        b_ub=np.zeros(len(matrix)), A_eq=np.array([np.r_[np.ones(k), 0]]), b_eq=[1],
        bounds=[(0, None)] * (k + 1), method='highs')
    return result.x[:k], result.x[-1]


def policy_from_weights(w, data, k, n, rng):
    _, histories, decisions, counts, payoff, _ = data
    terminal = {h: tuple(map(int, counts[h])) for h in histories if len(h) == n}
    actions = {}
    for h in reversed(decisions):
        values = np.array([payoff(terminal[h + (a,)], a) @ w for a in range(k)])
        a = int(rng.choice(np.flatnonzero(values >= max(values) - 1e-9)))
        actions[h] = a
        terminal[h] = terminal[h + (a,)]
    return actions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=int, default=4)
    parser.add_argument('--players', type=int, default=4)
    parser.add_argument('--iterations', type=int, default=300)
    parser.add_argument('--seed', type=int, default=81273)
    parser.add_argument('--mode', choices=['arbitrary', 'generated'], default='arbitrary')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    k, n = args.topics, args.players
    data = prepare(k, n)
    backgrounds = data[-1]
    best = -1
    seen = set()
    started = time.monotonic()
    report = dict(parameters=vars(args) | {'output': str(args.output)}, universal_proof=False,
                  best_gap=None, iterations_completed=0, positive_found=False)
    queue = []
    for it in range(args.iterations):
        if queue:
            w0 = queue.pop(0)
            actions = policy_from_weights(w0, data, k, n, rng)
        elif args.mode == 'arbitrary':
            actions = {h: int(rng.integers(k)) for h in data[2]}
        else:
            w0 = rng.integers(0, 4, (1 << k) - 1)
            w0 *= rng.random(len(w0)) < .35
            if not w0.any():
                w0[0] = 1
            actions = policy_from_weights(w0, data, k, n, rng)
        key = tuple(actions[h] for h in data[2])
        if key in seen:
            continue
        seen.add(key)
        G, c, terminal = cone(actions, data, k, n)
        queries = [np.ones(k) / k, rng.dirichlet(np.ones(k))]
        for p in queries:
            for alt in range(3):
                beta = backgrounds @ p
                r = lp(G, c, beta, n)
                if not r.success:
                    break
                gap = -r.fun - 1
                if gap > best + 1e-8:
                    best = gap
                    report.update(best_gap=float(gap), best_iteration=it,
                        root_counts=terminal[()], weights=r.x[:-1].tolist(), p=p.tolist(),
                        actions=[{'history': list(h), 'action': a} for h, a in actions.items()],
                        constraint_count=len(G), positive_found=bool(gap > 1e-7))
                    args.output.write_text(json.dumps(report, indent=2) + '\n')
                    print(json.dumps({'iteration': it, 'best_gap': best, 'root_counts': terminal[()]}), flush=True)
                p_new, value = safety(r.x[:-1], backgrounds)
                if np.max(abs(p_new - p)) < 1e-8:
                    break
                p = p_new
                if gap > 1e-7:
                    break
            if best > 1e-7:
                break
        report['iterations_completed'] = it + 1
        if best > 1e-7:
            break
        if it % 100 == 0:
            print(json.dumps({'iteration': it, 'elapsed': time.monotonic() - started}), flush=True)
    report.update(elapsed=time.monotonic() - started, distinct_policies=len(seen))
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('weights', 'p', 'actions')}), flush=True)


if __name__ == '__main__':
    main()
