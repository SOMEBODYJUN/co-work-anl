"""Attack the potential bound (m-1)u_last <= W using genuine complete SPE cones."""
from cone_search import Game
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np


def best_last_path(game, weights, rng):
    values, welfare, outcomes, floors, _ = game.solve(weights, rng)
    @lru_cache(None)
    def visit(q, d):
        if sum(q) == game.m - 1:
            a = next(a for a in range(game.k) if game.terminals[d][a] > q[a])
            return values[d, a], (a,)
        options = []
        for a, child in enumerate(game.children[q]):
            if d in outcomes[child] and values[d, a] >= floors[q] - 2e-8:
                val, path = visit(child, d)
                options.append((val, (a,) + path))
        return max(options)
    root = (0,) * game.k
    result = []
    for d in outcomes[root]:
        val, path = visit(root, int(d))
        result.append((val / welfare[d] if welfare[d] else 0, int(d), path))
    return max(result)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--starts', type=int, default=12)
    ap.add_argument('--steps', type=int, default=6)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    game = Game(args.topics, args.players)
    rng = np.random.default_rng(42378)
    best = 0
    for start in range(args.starts):
        if start == 0:
            weights = np.zeros(len(game.types))
            # Generalized residual/root-tax seed.
            for mask, value in [(1, 12), (2, 8), (4, 4), (8, 8), (17, 6), (33, 6),
                                (20, 3), (36, 3), (49, 6), (50, 2), (52, 1), (56, 2)]:
                weights[mask - 1] = value
        else:
            weights = rng.exponential(1, len(game.types))
            weights[rng.random(len(weights)) < .85] = 0
        for step in range(args.steps):
            incoming, target, path = best_last_path(game, weights, rng)
            matrix, target, choices, w, opt = game.cone(weights, rng, forced_target=target, forced_path=path)
            last = path[-1]
            objective = game.pay[target, last] / game.scale
            result = game.optimize(matrix, target, objective)
            assert result.success
            share = -result.fun
            new_ratio = float(max(game.opt_rows @ result.x))
            record = {'start': start, 'step': step, 'incoming_last_share': incoming,
                      'last_share': share, 'ratio': new_ratio, 'target': game.terminals[target],
                      'path': path, 'rows': len(matrix)}
            print(json.dumps(record), flush=True)
            if share > best + 1e-8:
                best = share
                args.output.write_text(json.dumps({'topics': game.k, 'players': game.m,
                     'status': 'floating candidate, not certified', 'record': record,
                     'weights': result.x.tolist(),
                     'choices': [{'prefix': q, 'target': d, 'action': a, 'children': children}
                                 for (q, d), (a, children) in choices.items()]}))
            weights = result.x


if __name__ == '__main__':
    main()
