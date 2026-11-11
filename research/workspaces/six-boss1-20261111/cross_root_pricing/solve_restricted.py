"""Small restricted-column discovery only; never claims full-domain infeasibility."""
import argparse
from collections import defaultdict
from itertools import combinations_with_replacement
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

from contract import (HERE, RUN, F, WORDS, load_inputs, row_names, budgets,
                      single_root_local, directed_pair_cost, serialized_column,
                      POINT_SHA)


def seed_columns(contexts, random_count, seed):
    rng = np.random.default_rng(seed)
    common = {(one, (zero,) * 5) for one in range(32) for zero in range(32)}
    for j in range(random_count):
        if j % 3 == 0:
            # Mixed sparse/dense words are deliberately represented.
            p = float(rng.choice([.15, .3, .5, .7, .85]))
            bits = rng.random((6, 5)) < p
            ws = [int(''.join('1' if b else '0' for b in row), 2) for row in bits]
        else:
            ws = rng.integers(0, 32, size=6).tolist()
        common.add((ws[0], tuple(sorted(ws[1:]))))
    old = json.loads((RUN / 'background_root_bridge/ordered_root_exact_nonseparation.json').read_text())
    supports = defaultdict(lambda: [set(), set()])
    for v in old['support']:
        if F(v['mass']):
            supports[v['actual'], v['d']][v['root_membership']].add(int(v['tail'], 2))
    ans = []
    for context in contexts:
        extra = set(common)
        zero, one = supports.get(context, [set(), set()])
        for w in one:
            for tup in combinations_with_replacement(sorted(zero), 5):
                extra.add((w, tup))
        ans.append(sorted(extra))
    return ans


def build_float(data, names, contexts, columns):
    nr = len(names)
    cross_ids = [i for i, n in enumerate(names) if n[0] in ('cross-floor', 'cross-pair')]
    cross_names = [names[i] for i in cross_ids]
    # The pair matrix is the sum of both directed costs for two distinct roots.
    pair = np.zeros((len(cross_ids), 64, 64))
    for x in range(64):
        t, w = divmod(x, 32)
        for y in range(x, 64):
            s, v = divmod(y, 32)
            lhs = directed_pair_cost(t, w, s, v, cross_names)
            rhs = directed_pair_cost(s, v, t, w, cross_names)
            pair[:, x, y] = pair[:, y, x] = [float(a + b) for a, b in zip(lhs, rhs)]
    blocks = []
    objective = []
    eqblocks = []
    metadata = []
    for group, (actual, d) in enumerate(contexts):
        assert d == 1, 'This discovery specialization is only for the fixed d=1 point.'
        local = np.zeros((64, nr))
        root = np.zeros(64)
        for x in range(64):
            t, w = divmod(x, 32)
            r, b = single_root_local(actual, d, t, w, names, data['remainder'])
            local[x] = [float(v) for v in b]
            root[x] = float(r)
        cols = columns[group]
        idx = np.array([[32 + one] + list(zero) for one, zero in cols], dtype=int)
        block = local[idx].sum(axis=1).T
        for i in range(6):
            for j in range(i + 1, 6):
                block[cross_ids] += pair[:, idx[:, i], idx[:, j]]
        blocks.append(block)
        objective.extend(root[idx].sum(axis=1))
        eq = np.zeros((len(contexts), len(cols)))
        eq[group] = 1
        eqblocks.append(eq)
        metadata.extend(serialized_column((actual, d), one, zero) for one, zero in cols)
    return np.hstack(blocks), np.array(objective), np.hstack(eqblocks), metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--random-columns', type=int, default=800)
    parser.add_argument('--seed', type=int, default=61111)
    parser.add_argument('--basic', action='store_true')
    parser.add_argument('--output', default='restricted_discovery.json')
    args = parser.parse_args()
    started = time.time()
    data = load_inputs()
    names = row_names(not args.basic)
    contexts = list(data['masses'])
    cols = seed_columns(contexts, args.random_columns, args.seed)
    a, c, eq, metadata = build_float(data, names, contexts, cols)
    rhs = budgets(data, names)
    print(json.dumps({'phase': 'matrix_ready', 'columns': len(metadata), 'budget_rows': len(names),
                      'seconds': time.time() - started}), flush=True)
    result = linprog(c, A_ub=csr_matrix(a), b_ub=np.array([float(v) for v in rhs]),
                     A_eq=csr_matrix(eq), b_eq=np.array([float(v) for v in data['masses'].values()]),
                     bounds=(0, None), method='highs')
    output = {'status': result.message, 'success': bool(result.success),
              'scope': 'Restricted support discovery; infeasibility is NOT full-domain infeasibility.',
              'point_sha256': POINT_SHA, 'extended': not args.basic,
              'columns': len(metadata), 'budget_rows': len(names), 'contexts': len(contexts),
              'random_columns_requested': args.random_columns, 'seed': args.seed,
              'seconds': time.time() - started}
    if result.success:
        output.update({'root_cost_float': float(result.fun), 'actual_root_budget_float': float(data['u'][0]),
                       'root_slack_float': float(data['u'][0]) - float(result.fun),
                       'support': [{**metadata[j], 'mass_float': float(x)}
                                   for j, x in enumerate(result.x) if x > 1e-10],
                       'budget_slacks_float': result.ineqlin.residual.tolist(),
                       'budget_duals_float': result.ineqlin.marginals.tolist(),
                       'context_duals_float': result.eqlin.marginals.tolist(),
                       'row_names': [list(n) for n in names]})
    (HERE / args.output).write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: v for k, v in output.items()
                      if k not in ('support', 'budget_slacks_float', 'budget_duals_float',
                                   'context_duals_float', 'row_names')}, indent=2))


if __name__ == '__main__':
    main()
