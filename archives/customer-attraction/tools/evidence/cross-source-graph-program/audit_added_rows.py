"""New exact local audit; does not build the inherited graph or run its LP.

Execute only the SHA-bound primary's psi/build definitions against an empty
base on a formal histogram basis. Compare with literal binary-state pricing
and separately derived floor/capacity/optimal-replacement coefficients.
The formal basis includes inconsistent d/word combinations intentionally:
these are algebraic probes, never claimed to be clients or game instances.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
PAT = tuple(product((0, 1), repeat=3))
EXPECTED = {
    'original/cross_source_graph.py': '295b4f11935a8ca241cef50541b30078000f8e67bea4f2301a2032914e3cc249',
    'related/priced_hidden_reply.py': '3579b2eae0ad29e3a5b0c081f2c3833e9e55dc0dd740fbcafe0eb7239443c5f3',
    'related/cross_source_priced_optimum_exact.json': '955c456ad3381a8cdc72139ba9ccc73dfe70297183e72727ae6ad165dc80e947',
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def share(bit, load):
    return F(bit, load) if bit else F(0)


def load_bound_sources():
    for rel, expected in EXPECTED.items():
        assert digest((HERE / rel).read_bytes()) == expected, rel
    helper = {'__name__': 'audit_original_priced_helper'}
    exec(compile((HERE / 'related/priced_hidden_reply.py').read_bytes(),
                 'SHA-bound-priced-helper', 'exec'), helper)
    tree = ast.parse((HERE / 'original/cross_source_graph.py').read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name in ('psi', 'build')]
    assert [n.name for n in functions] == ['psi', 'build']
    return compile(ast.Module(body=functions, type_ignores=[]),
                   'SHA-bound-cross-source-psi-build-only', 'exec'), helper


CODE, HELPER = load_bound_sources()
SEEN_PRICES = set()


@lru_cache(None)
def literal_price(p, ell, t, q, alpha, beta, mu):
    """Independent literal 2^r minimization, not helper.projected()."""
    SEEN_PRICES.add((p, ell, t, q, alpha, beta, mu))
    candidates = []
    for hidden in product((0, 1), repeat=len(alpha)):
        total = p + t + sum(hidden)
        source_gain = share(t, total)
        bought_prices = sum((beta[j] + alpha[j] / (ell + 1)) * f
                            for j, f in enumerate(hidden))
        last_current = share(hidden[-1], total)
        last_deviated = F(q, p + t + sum(hidden[:-1]) + 1)
        candidates.append(source_gain + bought_prices
                          + mu * (last_deviated - last_current))
    result = min(candidates)
    assert result == HELPER['projected_by_count'](p, ell, t, q, alpha, beta, mu)
    return result


def source_rows(cols, flags):
    ns = {'F': F, 'product': product, 'lru_cache': lru_cache,
          'projected_by_count': HELPER['projected_by_count'],
          'sys': SimpleNamespace(argv=['audit-isolated-build', *flags]),
          'sb': SimpleNamespace(build=lambda: (cols, [], [], [], [])),
          'nr': SimpleNamespace(PAT=PAT, share=share)}
    exec(CODE, ns)
    _, names, rows, _, _ = ns['build']()
    return names, rows


def row_specs(optimum=False, priced=False):
    for i in range(6):
        for q in (1, 2):
            yield 'actual-floor:' + str((i, q)), ('floor', i, q)
    for q in (1, 2):
        yield 'old-capacity:' + str(q), ('capacity', q)
    if optimum:
        for query in (*range(6), 'B', 'C'):
            yield 'OPT-one-replace:' + str(query), ('optimum', query)
    if priced:
        for i, tcol, qcol, mode, aa, mu in product(
                range(4), (1, 2), range(3), ('all', 'last'),
                (F(0), F(1, 8), F(1, 4), F(1, 2), F(1)),
                (F(0), F(1, 2), F(1), F(2))):
            alpha = tuple(aa if mode == 'all' or j == 4 - i else F(0)
                          for j in range(5 - i))
            label = 'old-priced:' + str((i, tcol, qcol, mode, aa, mu))
            yield label, ('priced', i, tcol, qcol, alpha, mu)


def reference(c, spec):
    kind = spec[0]
    if c['kind'] == 'K':
        return F(6) if kind == 'capacity' else F(0)
    if c['kind'] != 'hist':
        return F(0)
    actual = tuple(map(int, c['actual_bits']))
    total = sum(actual)
    # Weights n_w describe six indexed labels, not six independent customers.
    counts = c['hist']
    assert len(counts) == 8 and sum(counts) == 6
    if kind == 'floor':
        _, i, q = spec
        safe_load = sum(actual[:i]) + (6 - i)
        deviation = sum(F(n * word[q], safe_load)
                        for word, n in zip(PAT, counts))
        return 6 * share(actual[i], total) - deviation
    if kind == 'capacity':
        return -sum(F(n * word[spec[1]]) for word, n in zip(PAT, counts))
    if kind == 'optimum':
        query = spec[1]
        # Six copies of |P|-|A_i cap P|-6|A_i outside O|, or the
        # sum of this inequality over the six B/C labels respectively.
        memberships = ([(actual[query], 6)] if isinstance(query, int)
                       else [(w[1 if query == 'B' else 2], n)
                             for w, n in zip(PAT, counts)])
        return sum(F(n * ((1 - bit) if c['d'] == 1
                          else (-6 * bit if c['d'] == 0 else 0)))
                   for bit, n in memberships)
    _, i, tcol, qcol, alpha, mu = spec
    r = 5 - i
    paid_actual = 6 * (share(actual[i], total)
                       + sum(alpha) * share(actual[5], total))
    minimum = sum(n * literal_price(sum(actual[:i]), sum(actual[:5]),
                                   w[tcol], w[qcol], alpha, (F(0),) * r, mu)
                  for w, n in zip(PAT, counts) if n)
    return paid_actual - minimum


def basis(d_classes=None):
    cols = [{'kind': 'K'}]
    for a, k in product(product((0, 1), repeat=6), range(8)):
        hist = [6 if j == k else 0 for j in range(8)]
        for d in (d_classes if d_classes is not None else (6 * PAT[k][0],)):
            cols.append({'kind': 'hist', 'actual_bits': ''.join(map(str, a)),
                         'hist': hist, 'd': d})
    cols += [{'kind': 'joint-reply'}, {'kind': 'overlap'}]
    return cols


def audit_basis(cols, flags, families):
    names, rows = source_rows(cols, flags)
    specs = dict(row_specs('--optimum' in flags, '--priced' in flags))
    assert names == list(specs)
    checks = 0
    counts = Counter()
    for name, row in zip(names, rows):
        spec = specs[name]
        if spec[0] not in families:
            continue
        for c, value in zip(cols, row):
            assert value == reference(c, spec), (name, c, value)
            checks += 1
        counts[spec[0]] += 1
    return {'basis_columns': len(cols), 'row_families': dict(counts),
            'coefficient_comparisons': checks}


def point_check(path, flags):
    point = json.loads(path.read_bytes())
    fullcols = point['columns']
    ys = [F(c['weight']) for c in fullcols]
    assert min(ys) >= 0
    # Added rows have only K and histogram coefficients. This reduction does
    # not assert any inherited hidden-column consistency or IC constraints.
    cols = [c for c in fullcols if c['kind'] in ('K', 'hist')]
    assert cols[0]['kind'] == 'K'
    for c in cols[1:]:
        assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
        assert len(c['hist']) == 8 and sum(c['hist']) == 6
        assert all(isinstance(n, int) and n >= 0 for n in c['hist'])
        assert c['d'] == sum(n * w[0] for n, w in zip(c['hist'], PAT))
    assert sum(w > 0 for w in ys) == point['positive_columns']
    norm = sum(F(c['weight']) for c in cols[1:] if c['d'] > 0)
    welfare = sum(F(c['weight']) for c in cols[1:] if '1' in c['actual_bits'])
    assert norm == F(point['O']) == 1
    assert welfare == F(point['W']) < F(1, 2)
    # Historical strict_half_gap is O-2W, not O/2-W.
    assert F(point['strict_half_gap']) == norm - 2 * welfare
    names, rows = source_rows(cols, flags)
    specs = dict(row_specs('--optimum' in flags, '--priced' in flags))
    weights = [F(c['weight']) for c in cols]
    slacks = []
    for name, row in zip(names, rows):
        expected = [reference(c, specs[name]) for c in cols]
        assert row == expected
        value = sum(v * w for v, w in zip(row, weights))
        slacks.append({'name': name, 'slack': str(value)})
    summary = {'input_sha256': digest(path.read_bytes()),
               'all_columns_parsed': len(fullcols),
               'column_kinds': dict(Counter(c['kind'] for c in fullcols)),
               'all_weights_nonnegative': True,
               'positive_columns': sum(w > 0 for w in ys),
               'histogram_columns': len(cols) - 1,
               'O': str(norm), 'W': str(welfare),
               'O_minus_2W': str(norm - 2 * welfare),
               'added_rows_checked': len(slacks),
               'coefficient_comparisons': len(slacks) * len(cols),
               'negative': [s for s in slacks if F(s['slack']) < 0],
               'family_minimum': {prefix: str(min(F(s['slack']) for s in slacks
                                                if s['name'].startswith(prefix)))
                                  for prefix in sorted({s['name'].split(':')[0]
                                                        for s in slacks})}}
    return summary, slacks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--split-point', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=HERE)
    args = parser.parse_args()
    assert digest(args.split_point.read_bytes()) == 'b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a'
    regular = audit_basis(basis(), ['--priced'], {'floor', 'capacity', 'priced'})
    optimum = audit_basis(basis((0, 1, 2)), ['--optimum'], {'optimum'})
    current, current_slacks = point_check(
        HERE / 'related/cross_source_priced_optimum_exact.json',
        ['--priced', '--optimum'])
    old, old_slacks = point_check(args.split_point, [])
    assert current['added_rows_checked'] == 982 and not current['negative']
    assert [(s['name'], s['slack']) for s in old['negative']] == [
        ('actual-floor:(5, 1)', '-10278684531697071124608039179627/1344370606668255760206057578355825'),
        ('actual-floor:(5, 2)', '-11764212870687656756855220643451/1344370606668255760206057578355825')]
    r_counts = Counter(len(k[4]) for k in SEEN_PRICES)
    report = {
        'status': 'PASS',
        'scope': 'New exact local audit of appended rows on a formal affine histogram basis and two fixed rational points; no inherited graph build, original main, LP solve, game or SPE verification.',
        'frozen_sha256': EXPECTED,
        'regular_basis': regular, 'optimum_formal_basis': optimum,
        'literal_pricing': {
            'distinct_parameter_keys': len(SEEN_PRICES),
            'keys_by_follower_count': dict(sorted(r_counts.items())),
            'binary_states_evaluated': sum(2 ** len(k[4]) for k in SEEN_PRICES),
            'sorted_candidates_compared': sum(2 * len(k[4]) for k in SEEN_PRICES)},
        'cross_point': current, 'split_point': old,
        'row_count_by_cli_mode': {'default': 3959, 'optimum': 3967,
                                  'priced': 4919, 'priced_optimum': 4927},
        'row_count_status': '3945 inherited rows supplied by the separately reviewed split builder; these totals are arithmetic, not four original-main executions.'}
    args.out.mkdir(parents=True, exist_ok=True)
    for name, value in [('audit-report.json', report),
                        ('added-row-slacks.json', {'cross_point': current_slacks,
                                                   'split_point': old_slacks})]:
        (args.out / name).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
