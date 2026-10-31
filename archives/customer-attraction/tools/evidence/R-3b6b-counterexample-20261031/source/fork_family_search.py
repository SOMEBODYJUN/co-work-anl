"""Generalized residual fork family. Finite numerical exploration only."""
from cone_search import Game
import argparse
import json
from pathlib import Path
import numpy as np


def family_weights(game, forks, branches, a, p, q=1.):
    """A split into fork-private pieces; each B has private p and shared q."""
    assert game.k == 1 + forks + branches
    weights = np.zeros(len(game.types))
    fork_mask = sum(1 << i for i in range(1, forks + 1))
    for d in range(1, forks + 1):
        weights[(1 | (1 << d)) - 1] = a
    for b in range(forks + 1, game.k):
        weights[(1 << b) - 1] = p
        weights[(fork_mask | (1 << b)) - 1] = q
    return weights


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--forks', type=int, default=2)
    ap.add_argument('--branches', type=int, default=4)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    game = Game(1 + args.forks + args.branches, args.players)
    rng = np.random.default_rng(3912)
    best = 0.
    records = []
    for a in np.arange(.25, 5.01, .25):
        for p in np.arange(0, 6.01, .25):
            weights = family_weights(game, args.forks, args.branches, a, p)
            _, welfare, outcomes, _, target = game.solve(weights, rng)
            ratio = max(game.opt_rows @ weights) / welfare[target]
            if ratio > best + 1e-8:
                best = ratio
                record = {'a': a, 'p': p, 'q': 1, 'ratio': ratio,
                          'target': game.terminals[target], 'root_outcomes': len(outcomes[(0,) * game.k])}
                records.append(record)
                print(json.dumps(record), flush=True)
    args.output.write_text(json.dumps({'players': args.players, 'forks': args.forks,
                                       'branches': args.branches, 'best': best, 'records': records}, indent=2))


if __name__ == '__main__':
    main()
