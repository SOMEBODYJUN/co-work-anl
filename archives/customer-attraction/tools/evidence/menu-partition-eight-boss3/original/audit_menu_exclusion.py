"""Independent exact expansion of the off-diagonal indexed-menu identity.

No import of the discovery script or canonical row evaluator.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]


def expanded(prefix, branches, pos, menu):
    """Return K-1 utility sum minus all actual i != j floor comparisons."""
    count = len(branches)
    remaining = len(branches[0]) - pos
    actual = sum((F(row[pos], prefix + sum(row)) if row[pos] else F(0)
                  for row in branches), F(0))
    query = F(0)
    for i, row in enumerate(branches):
        denom = prefix + sum(row[:pos]) + remaining
        for j, other in enumerate(branches):
            if i != j:
                query += F(other[menu], denom)
    return (count - 1) * actual - query


def factored(prefix, branches, pos, menu):
    count = len(branches)
    remaining = len(branches[0]) - pos
    actual = sum((F(row[pos], prefix + sum(row)) if row[pos] else F(0)
                  for row in branches), F(0))
    inverse = [F(1, prefix + sum(row[:pos]) + remaining) for row in branches]
    menu_size = sum(row[menu] for row in branches)
    return ((count - 1) * actual - menu_size * sum(inverse)
            + sum(row[menu] * inv for row, inv in zip(branches, inverse)))


def main():
    checks = 0
    # All ordered index memberships for 1..3 indices and 2..4 branch positions.
    for k in range(1, 4):
        for length in range(2, 5):
            for flat in product((0, 1), repeat=k * length):
                branches = [flat[i*length:(i+1)*length] for i in range(k)]
                for prefix in range(3):
                    for pos in range(1, length):
                        for menu in range(length):
                            assert expanded(prefix, branches, pos, menu) == factored(
                                prefix, branches, pos, menu)
                            checks += 1
    cert = json.loads((ROOT / 'evidence/certificates/customer_attraction/'
                      'five_player_indexed_bound.json').read_text())['primal']
    kinds = list(product((0, 1), repeat=3))
    total = F(0)
    for atom in cert['atoms']:
        bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
        branches = [kind for kind, n in zip(kinds, atom['AE_hist']) for _ in range(n)]
        assert len(branches) == 5
        coefficient = expanded(bits['A'] + bits['E'], branches, pos=2, menu=1)
        assert coefficient == factored(bits['A'] + bits['E'], branches, pos=2, menu=1)
        total += F(atom['mass_numerator'], cert['denominator']) * coefficient
    expected = F(-2350274614365061193348939000536717958363,
                 10160684453437026820024983718703677270992)
    assert total == expected < 0
    report = {'status': 'passed', 'identity_checks': checks,
              'frozen_437_point_AE_last_off_R': str(total),
              'scope': 'identity and explicit relaxed-point obstruction; not an SPE counterexample'}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
