"""Parent audit of a new 557-row rational point, without its pricing code.

Reuses the previously reviewed 437-row definition evaluator. Reconstructs all
120 added rows as literal one-client sums over indices. This checks a necessary
condition relaxation, not SPE completion or optimal coverage of a real catalog.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
ACTOR = HERE.parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ACTOR / 'round4_pricing/exact_primal_overlap1.json'


def old_evaluator():
    source = ROOT / 'tests/audits/customer_attraction_five_indexed.py'
    body = []
    for node in ast.parse(source.read_text()).body:
        if isinstance(node, ast.ImportFrom) and node.module == 'pathlib':
            break
        body.append(node)
    ns = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(source), 'exec'), ns)
    return ns['evaluate']


def literal_added(atom):
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    rows = {}
    orbit_names = ('all_equal', 'query_equal', 'first_branch', 'second_branch', 'all_distinct')
    for family, field, arity, prefix in (
        ('AB', 'AB_hist', 3, 'AB'), ('AE', 'AE_hist', 3, 'AE'),
        ('Sbranch', 'second_hist', 4, 'A')
    ):
        cells = list(product((0, 1), repeat=arity))
        states = [s for s, count in zip(cells, atom[field]) for _ in range(count)]
        assert len(states) == 5
        base = sum(bits[t] for t in prefix)
        for pos in range(arity):
            total = F(0)
            for i, s in enumerate(states):
                denominator = base + sum(s[:-1]) + 1
                for j, t in enumerate(states):
                    if i != j:
                        total += F(s[-1] - t[pos], denominator)
            rows[f'{family}:5:offdiag:{pos}'] = total
        for u, v in combinations_with_replacement(range(arity), 2):
            totals = dict.fromkeys(orbit_names, F(0))
            for i, s in enumerate(states):
                p = base + sum(s[:-2])
                a, b = s[-2:]
                H = (F(a+b, p+a+b) if a+b else F(0)) + F(a, (p+1)*(p+2))
                for j, t in enumerate(states):
                    for k, z in enumerate(states):
                        if i == j == k:
                            orbit = 'all_equal'
                        elif j == k:
                            orbit = 'query_equal'
                        elif i == j:
                            orbit = 'first_branch'
                        elif i == k:
                            orbit = 'second_branch'
                        else:
                            orbit = 'all_distinct'
                        cost = F(t[u]+z[v], p+1)-F(t[u]*z[v], (p+1)*(p+2))
                        totals[orbit] += H-cost
            for orbit, value in totals.items():
                rows[f'{family}:pair:{u}{v}:{orbit}'] = value
    assert len(rows) == 120
    return rows


def audit():
    cert = json.loads(SOURCE.read_text())
    evaluate = old_evaluator()
    totals = {name: F(0) for name in cert['slacks']}
    W = O = F(0)
    min_mass = None
    for atom in cert['atoms']:
        bits = tuple(map(int, atom['bits']))
        assert len(bits) == 10 and set(bits) <= {0, 1}
        histograms = [atom[k] for k in ('AB_hist', 'AE_hist', 'second_hist')]
        assert [len(h) for h in histograms] == [8, 8, 16]
        assert all(sum(h) == 5 and all(type(n) is int and n >= 0 for n in h) for h in histograms)
        d = sum(histograms[0][4:])
        assert d == sum(histograms[1][4:]) == sum(histograms[2][8:])
        assert len(atom['menus_lh']) == 3
        for ell, intersection in atom['menus_lh']:
            assert type(ell) is int and type(intersection) is int
            assert 0 <= intersection <= d and 0 <= ell-intersection <= 5-d
        mass = F(atom['exact_mass'])
        assert mass > 0
        min_mass = mass if min_mass is None else min(mass, min_mass)
        rows = evaluate(bits, histograms, atom['menus_lh'], True)
        assert len(rows) == 437
        added = literal_added(atom)
        assert set(rows).isdisjoint(added)
        rows.update(added)
        assert set(rows) == set(totals)
        for name, value in rows.items():
            totals[name] += mass*value
        W += mass*int(any(bits[:5]))
        O += mass*int(d > 0)
    assert W == F(cert['welfare']) == 1
    assert O == F(cert['comparison_cover']) > 2
    assert all(value >= 0 for value in totals.values())
    assert all(value == F(cert['slacks'][name]) for name, value in totals.items())
    assert O-2 == F(cert['gap_above_two'])
    return {
        'scope': 'Exact necessary-row feasibility only; no SPE completion or actual OPT claim',
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'positive_atoms': len(cert['atoms']), 'rows': len(totals),
        'previously_reviewed_definition_rows': 437, 'new_rows_rebuilt_as_literal_sums': 120,
        'welfare': str(W), 'comparison_cover': str(O), 'comparison_float': float(O),
        'gap_above_two': str(O-2), 'minimum_slack': str(min(totals.values())),
        'zero_slacks': sum(v == 0 for v in totals.values()),
        'all_reported_slacks_equal_independent_reconstruction': True,
        'minimum_positive_mass': str(min_mass),
    }


if __name__ == '__main__':
    report = audit()
    HERE.mkdir(exist_ok=True)
    HERE.joinpath('audit_full_primal.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
