"""Exact suffix probe for a scalable binary bank code; not a whole-game SPE."""
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver


def build(d, h, x=1, y=1, shared=False):
    codes = [(0,) + bits for bits in product(range(2), repeat=d-1)]
    k = len(codes)
    bank = {(a, b, z) for a in range(d) for b in range(2) for z in range(h)}
    coverage, names = [], []
    for kind in ('C', 'A', 'B', 'L'):
        for i, code in enumerate(codes):
            core = {('x', i, z) for z in range(x)}
            omit = {('y', (i//2 if shared else i), z) for z in range(y)}
            own = {(a, code[a], z) for a in range(d) for z in range(h)}
            coverage.append({'C': core, 'A': core | omit,
                             'B': core | omit | own, 'L': bank-own}[kind])
            names.append(f'{kind}{i}')
    return Instance.from_topic_sets(coverage, k+4, names), codes


def main():
    rows = []
    for d, h, x, y, shared in [(2, 18, 1, 1, False), (3, 18, 1, 1, False),
                              (3, 36, 2, 3, True), (4, 18, 1, 1, True)]:
        game, codes = build(d, h, x, y, shared)
        k = len(codes)
        solver = ExactSPESolver(game)
        i = 0
        prefix = tuple(j for j in range(k) if j != i) + (k+i, 3*k+i)
        desired = prefix + (3*k+i, 2*k+i, 2*k+i)
        counts = game.counts(prefix)
        target = game.counts(desired, terminal=True)
        outcomes = solver.outcomes(counts)
        floor = solver.threshold(counts)
        u = game.topic_payoff(3*k+i, target)
        last_prefix = desired[:-1]
        last_value = game.topic_payoff(2*k+i, target)
        last_comparisons = []
        frozen_comparisons = []
        for a in range(game.topic_count):
            q = game.counts(last_prefix + (a,), terminal=True)
            last_comparisons.append(game.topic_payoff(a, q) <= last_value)
            q_frozen = game.counts(prefix+(a, 2*k+i, 2*k+i), terminal=True)
            frozen_comparisons.append(game.topic_payoff(a, q_frozen) <= u)
        child_rows = []
        for a in range(game.topic_count):
            child = game.counts(prefix+(a,))
            candidates = solver.outcomes(child)
            low = min(game.topic_payoff(a, q) for q in candidates)
            child_rows.append({'action': game.topics[a], 'minimum_SPE_payoff': str(low),
                               'exceeds_desired': low > u})
        # Directly audit every possible pure-SPE continuation after each B_j
        # deviation: both remaining actors choose bank-bearing actions, the
        # final bank-coordinate loads are 2/2, and neither can choose B_j.
        balanced_audit = []
        for j in range(k):
            if j == i:
                continue
            child = game.counts(prefix+(2*k+j,))
            for q in solver.outcomes(child):
                suffix = tuple(a for a in range(game.topic_count)
                               for _ in range(q[a]-child[a]))
                patterns = []
                for a in prefix + (2*k+j,) + suffix:
                    if 2*k <= a < 3*k:
                        patterns.append(codes[a-2*k])
                    elif 3*k <= a < 4*k:
                        patterns.append(tuple(1-z for z in codes[a-3*k]))
                assert len(patterns) == 4
                assert all(sum(p[a] for p in patterns) == 2 for a in range(d))
                assert 2*k+j not in suffix
                low = game.topic_payoff(2*k+j, q)
                assert low >= Fraction(d*h, 2) + Fraction(x, 2)
                balanced_audit.append(True)
        rows.append({'d': d, 'k': k, 'h': h, 'x': x, 'y': y, 'shared_omissions': shared,
                     'prefix': [game.topics[a] for a in prefix],
                     'desired_suffix': ['L0','B0','B0'],
                     'desired_in_outcomes': target in outcomes,
                     'desired_loader_payoff': str(u), 'true_threshold': str(floor),
                     'all_true_last_rows_pass': all(last_comparisons),
                     'all_frozen_loader_rows_pass': all(frozen_comparisons),
                     'all_Bj_continuations_bank_balanced': all(balanced_audit),
                     'Bj_continuations_checked': len(balanced_audit),
                     'actions': child_rows, 'stats': solver.stats.__dict__})
    output = Path(__file__).with_name('code_bank_suffix_probe.json')
    output.write_text(json.dumps(rows, indent=2)+'\n')
    print(json.dumps([{key: row[key] for key in ('d','x','y','desired_in_outcomes',
                      'desired_loader_payoff','true_threshold')} for row in rows], indent=2))


if __name__ == '__main__':
    main()
