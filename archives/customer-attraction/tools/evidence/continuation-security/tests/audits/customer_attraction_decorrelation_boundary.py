"""Definition-level replay of an adaptive-response decorrelation obstruction.

The floating LPs used in scratch research are not imported. This audit reads the
existing integer customer instance and full ordered policy, checks every SPE
node with integer-scaled unit-customer utilities, and verifies the four exact
cross-branch values. It does not test or decide the mixed-security SPE bridge.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text())
    p, n = data['m'], data['n']
    if (p, n) != (12, 4):
        raise AssertionError('unexpected source scope')
    weights = tuple((int(mask), weight) for mask, weight in data['weights'].items())
    if len(weights) != (1 << p) - 1 or any(weight <= 0 for mask, weight in weights):
        raise AssertionError('source is not positive unit-customer multiplicities')
    actions = {tuple(row['history']): row['action'] for row in data['policy']}
    expected = {h for depth in range(n) for h in product(range(p), repeat=depth)}
    if len(actions) != len(data['policy']) or set(actions) != expected:
        raise AssertionError('policy does not enumerate all ordered histories')
    if any(a not in range(p) for a in actions.values()):
        raise AssertionError('invalid source action')

    @lru_cache(None)
    def terminal(history):
        h = history
        while len(h) < n:
            h += (actions[h],)
        return h

    @lru_cache(None)
    def utilities(sorted_terminal):
        # lcm(1,2,3,4)=12 makes all legal final utilities exact integers.
        out = [0] * p
        selected = tuple(set(sorted_terminal))
        for mask, weight in weights:
            denominator = sum((mask >> a) & 1 for a in sorted_terminal)
            if denominator:
                contribution = weight * (12 // denominator)
                for a in selected:
                    if (mask >> a) & 1:
                        out[a] += contribution
        return tuple(out)

    comparisons = 0
    for h, a in actions.items():
        actual = utilities(tuple(sorted(terminal(h))))[a]
        for b in range(p):
            alternative = utilities(tuple(sorted(terminal(h + (b,)))))[b]
            comparisons += 1
            if alternative > actual:
                raise AssertionError(('non-SPE node', h, a, b, actual, alternative))

    a, b = 4, 9
    ca, cb = terminal((a,))[1:], terminal((b,))[1:]
    if (ca, cb) != ((2, 3, 11), (6, 7, 3)):
        raise AssertionError('unexpected continuation')
    table = tuple(tuple(F(utilities(tuple(sorted((q,) + c)))[q], 12)
                        for c in (ca, cb)) for q in (a, b))
    if table != ((F(6135342), F(6135349)), (F(6135349), F(6135345))):
        raise AssertionError(('unexpected cross values', table))
    adaptive = (table[0][0] + table[1][1]) / 2
    independent = sum(sum(row) for row in table) / 4
    if adaptive - independent != -F(11, 4):
        raise AssertionError('decorrelation gap')
    root = terminal(())
    root_utility = F(utilities(tuple(sorted(root)))[root[0]], 12)
    if root != (8, 4, 5, 0) or root_utility != 6135345:
        raise AssertionError('unexpected actual root')
    actual_background = root[1:]
    menu_values = tuple(
        F(99999, 100000) * F(utilities(tuple(sorted((q,) + actual_background)))[q], 12)
        + F(1, 100000) * F(utilities(tuple(sorted((q,) + cb)))[q], 12)
        for q in range(p))
    if max(menu_values) != root_utility:
        raise AssertionError('free-menu mixture fails claimed root cap')
    report = {'claim': 'CA-ADAPTIVE-DECORRELATION-NO',
                      'ordered_nodes': len(actions), 'all_action_comparisons': comparisons,
                      'customers': sum(w for mask, w in weights),
                      'actual_root': root, 'root_utility': str(root_utility),
                      'deviation_themes': (a, b), 'true_continuations': (ca, cb),
                      'payoff_matrix': [[str(x) for x in row] for row in table],
                      'adaptive_mean': str(adaptive), 'independent_mean': str(independent),
                      'adaptive_minus_independent': str(adaptive - independent),
                      'free_menu_cap': str(max(menu_values)),
                      'scope': 'A counterexample to universal decorrelation, not to half coverage or the mixed-security bridge.',
                      'sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in (SOURCE, Path(__file__).resolve())}}
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as handle:
            handle.write(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
