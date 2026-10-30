"""Literal independent Fraction audit of four dynamic-seat path barriers."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'evidence/runs/2026-10-10/customer_attraction_six_maxima_seat_obstructions.json'


def audit():
    package = json.loads(DATA.read_text())
    assert package['maximal_count'] == 6
    assert {row['n'] for row in package['obstructions']} == {5, 6, 7, 8}
    assert len(package['obstructions']) == 4
    reports = []
    literal_count = seat_checks = join_checks = 0
    for row in package['obstructions']:
        n, path = row['n'], row['path']
        assert len(path) == n-1 and all(0 <= j < 6 for j in path)
        weights = {int(I): w for I, w in row['incidence_weights'].items()}
        assert all(1 <= I <= 62 and type(w) is int and w > 0 for I, w in weights.items())
        customers = tuple(I for I, w in weights.items() for _ in range(w))
        literal_count += len(customers)
        maxima = tuple(frozenset(x for x, I in enumerate(customers) if I >> j & 1) for j in range(6))
        assert len(set(maxima)) == 6
        assert all(not (a != b and a < b) for a in maxima for b in maxima)
        assert not set.intersection(*(set(a) for a in maxima))
        union = frozenset.union(*maxima)
        assert len(union) == len(customers) == row['total_mass']
        portfolio = row['optimal_support']
        assert len(portfolio) <= n
        assert frozenset.union(*(maxima[j] for j in portfolio)) == union
        # Exhaust all legal theme supports as a second OPT calculation.
        OPT = max(len(frozenset.union(*(maxima[j] for j in support)))
                  for k in range(1, min(n, 6)+1) for support in combinations(range(6), k))
        assert OPT == len(customers)
        p, floors = [0] * 6, []
        for t in range(n):
            r = n-t
            seats = []
            for j in range(6):
                shared = sum((F(w, sum(p[k] for k in range(6) if I >> k & 1)+r)
                              for I, w in weights.items() if I.bit_count() >= 2 and I >> j & 1), F(0))
                seats.extend(F(weights.get(1 << j, 0), p[j]+k)+shared for k in range(1, r+1))
            assert len(seats) == 6*r
            floor = sorted(seats, reverse=True)[r-1]
            seat_checks += len(seats)
            floors.append(floor)
            # Calculate all immediate joins from individually expanded unit customers.
            loads = tuple(sum(p[j] for j in range(6) if I >> j & 1) for I in customers)
            joins = tuple(sum((F(1, loads[x]+1) for x in theme), F(0)) for theme in maxima)
            assert max(joins) >= max(seats) >= floor
            join_checks += 6
            if t < n-1:
                p[path[t]] += 1
        assert floors == list(map(F, row['floors']))
        assert sum(floors) == F(row['floor_sum'])
        assert sum(floors)/OPT == F(row['budget_ratio']) < F(1, 2)
        reports.append({'n': n, 'OPT': OPT, 'floor_sum': str(sum(floors)),
                        'budget_ratio': str(sum(floors)/OPT), 'customer_types': len(weights)})
    assert seat_checks == 600 and join_checks == 156
    paths = ['research/current/customer_attraction/model.md',
             'research/current/customer_attraction/six_maxima_seat_obstructions.md',
             'tests/audits/customer_attraction_six_maxima_seat_obstructions.py',
             str(DATA.relative_to(ROOT))]
    return {'status': 'passed exact mechanism obstructions; no SPE welfare counterexample claimed',
            'cases': reports, 'literal_unit_customers': literal_count,
            'exact_seat_values': seat_checks, 'literal_immediate_join_checks': join_checks,
            'source_sha256': {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('refusing to overwrite existing output')
    report = json.dumps(audit(), indent=2)
    print(report)
    if args.output:
        args.output.write_text(report+'\n')


if __name__ == '__main__':
    main()
