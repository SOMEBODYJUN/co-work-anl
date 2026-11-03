"""Fixed 3-player group strategy: enlarged incumbent load cone exploration."""
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


TOPICS = 6
PLAYERS = 3


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(0, 3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def terminal(h):
    while len(h) < PLAYERS:
        h = h + (action(h),)
    return h


def run(iterations=200, max_background=5, seed=18, monotone=False):
    rng = np.random.default_rng(seed)
    loads_parameter = range(1, PLAYERS + 1) if monotone else range(max_background + 1)
    columns = [(mask, b) for b in loads_parameter for mask in range(1, 1 << TOPICS)]
    like = np.array([[mask >> a & 1 for mask, b in columns] for a in range(TOPICS)])
    background = np.array([b for mask, b in columns])

    def utility(a, z):
        load = like[list(z)].sum(axis=0)
        if monotone:
            return like[a] * (load <= background)
        denominator = background + load
        return like[a] / np.maximum(denominator, 1)

    rows = []
    histories = [h for d in range(PLAYERS) for h in product(range(TOPICS), repeat=d)]
    for h in histories:
        z = terminal(h)
        for a in range(TOPICS):
            za = terminal(h + (a,))
            rows.append(utility(action(h), z) - utility(a, za))
    gamma = np.array(rows)
    z = terminal(())
    root_total = sum(utility(a, z) for a in z)
    backs = list(combinations_with_replacement(range(TOPICS), PLAYERS - 1))
    if monotone:
        beta = np.array([like * ((1 + like[list(B)].sum(axis=0)) <= background) for B in backs])
    else:
        beta = np.array([like / (background + 1 + like[list(B)].sum(axis=0)) for B in backs])
    best = 0
    for it in range(iterations):
        p = rng.dirichlet(np.ones(TOPICS) * .8) if it else np.ones(TOPICS) / TOPICS
        for repeat in range(8):
            bp = np.einsum('bac,a->bc', beta, p)
            obj = np.r_[root_total, -PLAYERS]
            result = linprog(obj, A_ub=np.r_[np.c_[-gamma, np.zeros(len(gamma))],
                      np.c_[-bp, np.ones(len(backs))]],
                      b_ub=np.zeros(len(gamma) + len(backs)),
                      A_eq=np.array([[1.] * len(columns) + [0.]]), b_eq=[1.],
                      bounds=[(0, None)] * len(columns) + [(None, None)], method='highs')
            if not result.success:
                raise RuntimeError(result.message)
            gap = -result.fun
            if gap > best + 1e-10:
                best = gap
                print('best', best, 'iter', it, 'repeat', repeat, flush=True)
                data = {'model': 'monotone_step' if monotone else 'shifted_inverse',
                        'columns': [dict(mask=mask, parameter=b, weight=float(w))
                         for (mask, b), w in zip(columns, result.x[:-1]) if w > 1e-10],
                        'query_float': p.tolist(), 'gap_float': gap,
                        'remaining_total_float': root_total @ result.x[:-1],
                        'value_float': result.x[-1]}
                name = 'monotone_cone_best.json' if monotone else 'cone_search_best.json'
                Path(__file__).with_name(name).write_text(json.dumps(data, indent=2))
            # Ascend in the query player as well, retaining exact cone weights.
            mat = np.einsum('bac,c->ba', beta, result.x[:-1])
            primal = linprog(np.r_[np.zeros(TOPICS), -1],
                     A_ub=np.c_[-mat, np.ones(len(backs))], b_ub=np.zeros(len(backs)),
                     A_eq=np.array([[1.] * TOPICS + [0.]]), b_eq=[1.],
                     bounds=[(0, None)] * TOPICS + [(None, None)], method='highs')
            p = primal.x[:-1]
            if gap > 1e-7:
                return best
    print('completed max gap', best, flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=200)
    parser.add_argument('--max-background', type=int, default=5)
    parser.add_argument('--seed', type=int, default=18)
    parser.add_argument('--monotone', action='store_true')
    args = parser.parse_args()
    run(args.iterations, args.max_background, args.seed, args.monotone)
