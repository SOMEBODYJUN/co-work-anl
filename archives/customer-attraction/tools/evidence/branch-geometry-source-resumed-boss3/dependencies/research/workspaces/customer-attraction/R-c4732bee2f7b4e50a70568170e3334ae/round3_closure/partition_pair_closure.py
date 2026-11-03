"""Lift-independent pair-query credibility, split by three-index equality.

Only necessary inequalities of genuine two-remaining-player SPE nodes are
claimed. Frozen marginal atoms are not strategies. Every coefficient is
checked with exact Fraction arithmetic against literal branch/query triples.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
ACTOR = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
AUGMENTED = ACTOR / 'continuation_completion/frozen_support_augmented.json'
PARTITIONS = ('all_equal', 'query_equal', 'first_branch', 'second_branch', 'all_distinct')


def partition(i, j, k):
    if i == j == k:
        return 'all_equal'
    if j == k:
        return 'query_equal'
    if i == j:
        return 'first_branch'
    if i == k:
        return 'second_branch'
    return 'all_distinct'


def query_cost(p, b, c, overlap=2):
    return F(b + c, p + 1) - F(overlap * b * c, (p + 1) * (p + 2))


def compact_costs(q, p, b, c, B, C, K, overlap=2):
    """Sum pair comparison costs for each fixed branch i, over each orbit."""
    d = (p + 1) * (p + 2)
    return {
        'all_equal': query_cost(p, b, c, overlap),
        'query_equal': F(B - b + C - c, p + 1) - F(overlap * (K - b*c), d),
        'first_branch': F((q - 1)*b + C - c, p + 1) - F(overlap*b*(C-c), d),
        'second_branch': F(B - b + (q - 1)*c, p + 1) - F(overlap*(B-b)*c, d),
        'all_distinct': F((q - 2)*(B - b + C - c), p + 1)
                        - F(overlap*((B-b)*(C-c) - (K-b*c)), d),
    }


def rows(atom, direct=False, overlap=2):
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    out = {}
    for family, field, arity, fixed in [('AB', 'AB_hist', 3, 'AB'),
                                       ('AE', 'AE_hist', 3, 'AE'),
                                       ('Sbranch', 'second_hist', 4, 'A')]:
        hist = atom[field]
        types = tuple(product((0, 1), repeat=arity))
        data = [ty for ty, n in zip(types, hist) for _ in range(n)]
        q = len(data)
        assert q >= 3
        prefix = sum(bits[x] for x in fixed)
        counts = dict(zip(PARTITIONS, (1, q-1, q-1, q-1, (q-1)*(q-2))))
        for u, v in combinations_with_replacement(range(arity), 2):
            B = sum(ty[u] for ty in data)
            C = sum(ty[v] for ty in data)
            K = sum(ty[u]*ty[v] for ty in data)
            values = dict.fromkeys(PARTITIONS, F(0))
            for i, ty in enumerate(data):
                p = prefix + sum(ty[:-2])
                first, last = ty[-2:]
                H = F(first + last, p + first + last) if first + last else F(0)
                H += F(first, (p+1)*(p+2))
                if direct:
                    for j, k in product(range(q), repeat=2):
                        values[partition(i, j, k)] += H - query_cost(p, data[j][u], data[k][v], overlap)
                else:
                    costs = compact_costs(q, p, ty[u], ty[v], B, C, K, overlap)
                    for name in PARTITIONS:
                        values[name] += counts[name]*H - costs[name]
            for name, value in values.items():
                out[f'{family}:pair:{u}{v}:{name}'] = value
    return out


def audit():
    src = json.loads(SOURCE.read_text())['primal']
    aug = json.loads(AUGMENTED.read_text())
    reports = {}
    for label, atoms in [('original_64_atoms', src['atoms']), ('augmented_42_atoms', aug['atoms'])]:
        totals = {}
        for atom in atoms:
            compact = rows(atom)
            assert compact == rows(atom, direct=True)
            strong = rows(atom, overlap=1)
            assert strong == rows(atom, direct=True, overlap=1)
            assert all(strong[name] <= compact[name] for name in compact)
            compact.update({'strong:' + name: value for name, value in strong.items()})
            mass = (F(atom['exact_mass']) if 'exact_mass' in atom else
                    F(atom['mass_numerator'], src['denominator']))
            for name, value in compact.items():
                totals[name] = totals.get(name, F(0)) + mass*value
        negative = {name: str(v) for name, v in totals.items() if v < 0}
        reports[label] = {'atoms': len(atoms), 'row_count': len(totals),
                          'negative_rows': negative, 'negative_count': len(negative),
                          'all_rows': {name: str(v) for name, v in totals.items()}}
    return {'scope': 'Necessary pair-query closure only, not an SPE or a general half-coverage proof',
            'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'augmented_sha256': hashlib.sha256(AUGMENTED.read_bytes()).hexdigest(),
            'all_compact_coefficients_equal_literal_index_sums': True,
            'degenerate_orbit_audit': audit_orbits(),
            'reports': reports}


def audit_orbits():
    checks = 0
    for q in (1, 2, 3, 5):
        for data in product(tuple(product((0, 1), repeat=2)), repeat=q):
            B = sum(ty[0] for ty in data)
            C = sum(ty[1] for ty in data)
            K = sum(ty[0]*ty[1] for ty in data)
            for p in (0, 1, 9):
                for overlap in (1, 2):
                    compact = compact_costs(q, p, *data[0], B, C, K, overlap)
                    direct = dict.fromkeys(PARTITIONS, F(0))
                    counts = dict.fromkeys(PARTITIONS, 0)
                    for j, k in product(range(q), repeat=2):
                        name = partition(0, j, k)
                        direct[name] += query_cost(p, data[j][0], data[k][1], overlap)
                        counts[name] += 1
                    assert compact == direct
                    assert list(counts.values()) == [1, q-1, q-1, q-1, (q-1)*(q-2)]
                    checks += 1
    return {'q_values': [1, 2, 3, 5], 'background_loads': [0, 1, 9],
            'overlap_coefficients': [1, 2], 'exact_checks': checks,
            'all_empty_orbit_costs_equal_zero': True}


if __name__ == '__main__':
    report = audit()
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({**report, 'reports': {k: {n: v for n, v in r.items() if n != 'all_rows'}
                     for k, r in report['reports'].items()}}, indent=2))
