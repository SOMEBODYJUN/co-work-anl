"""Exact, lift-independent terminal off-diagonal rows for the five-index model.

Imports neither a canonical equilibrium solver nor an indexed-row evaluator.
The direct nested per-index implementation and compact histogram formula must
agree separately on every frozen atom.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'


def rows(atom, direct=False):
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    out = {}
    for family, field, arity, fixed, last in [
            ('AB', 'AB_hist', 3, 'AB', 2),
            ('AE', 'AE_hist', 3, 'AE', 2),
            ('Sbranch', 'second_hist', 4, 'A', 3)]:
        hist = atom[field]
        types = tuple(product((0, 1), repeat=arity))
        data = [ty for ty, n in zip(types, hist) for _ in range(n)]
        assert len(data) == 5
        prefix = sum(bits[x] for x in fixed)
        for position in range(arity):
            name = family + ':5:offdiag:' + str(position)
            if direct:
                # Each term is a genuine last player's same-history deviation.
                out[name] = sum((
                    F(data[i][last] - data[j][position],
                      prefix + sum(data[i][:last]) + 1)
                    for i in range(5) for j in range(5) if i != j), F(0))
            else:
                menu_count = sum(n * ty[position] for n, ty in zip(hist, types))
                out[name] = sum((
                    F(n * (4 * ty[last] - menu_count + ty[position]),
                      prefix + sum(ty[:last]) + 1)
                    for n, ty in zip(hist, types)), F(0))
    return out


def audit():
    primal = json.loads(SOURCE.read_text())['primal']
    totals = {}
    for atom in primal['atoms']:
        compact = rows(atom)
        assert compact == rows(atom, direct=True)
        mass = F(atom['mass_numerator'], primal['denominator'])
        for name, value in compact.items():
            totals[name] = totals.get(name, F(0)) + mass * value
    negatives = {name: str(value) for name, value in totals.items() if value < 0}
    assert set(negatives) == {'AB:5:offdiag:1', 'AE:5:offdiag:1',
                              'Sbranch:5:offdiag:1', 'Sbranch:5:offdiag:2'}
    return {'identity': 'off-diagonal terminal common-catalog closure',
            'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'source_atoms': len(primal['atoms']),
            'all_atoms_compact_equals_raw_indices': True,
            'rows': {name: str(value) for name, value in totals.items()},
            'negative_rows': negatives,
            'conclusion': 'No full pure SPE can have these exact frozen customer marginals and the named branch meanings; this does not settle half coverage.'}


if __name__ == '__main__':
    report = audit()
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
