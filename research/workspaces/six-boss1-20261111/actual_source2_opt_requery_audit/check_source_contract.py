#!/usr/bin/env python3
"""Independent source/template audit. Standard library; never loads builder code.

The coefficient oracle below starts from a single covered client's terminal
share, including literal six/30-index sums. It reads only static source data.
It does not bind a point or assemble a fixed-point/full8192 matrix.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
SRC = WS / 'actual_source2_opt_requery'
ACTUAL = tuple('A%d' % j for j in range(1, 7))
TAILS = ('R3', 'R4', 'R5', 'R6')
NEW = ('Q',) + TAILS
OLD = ACTUAL + ('X', 'Omean')
QUERIES = ACTUAL + ('X',) + NEW + ('Omean',)
EXPECTED_COUNTS = {
    'IC_SOURCE2': 1, 'CAP': 5, 'ACTUAL_SAFE': 29, 'MAX': 5,
    'MX': 5, 'NEW_SAFE': 52, 'NEW_PAIR': 91, 'ACTUAL_RC': 55,
}


def read(name):
    return json.loads((SRC / name).read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(bit, prefix, followers):
    """One customer's actual share when the queried player's bit is bit."""
    assert bit in (0, 1) and prefix >= 0 and followers >= 0
    return F(1, prefix + 1 + followers) if bit else F(0)


def payoff(sequence, position):
    return share(sequence[position], sum(sequence[:position]),
                 sum(sequence[position + 1:]))


def two_query_cost(first, second, prefix):
    # U(first, second) + f(second), evaluated as literal shares.
    return share(first, prefix, second) + share(second, prefix, 0)


def weak_menu(o):
    # Endpoint used only after proving monotonicity in actual menu count d.
    return (o, 0, 0, 0, 0, 0)


def weak_pair(labels, membership, o, prefix):
    if labels[0] == labels[1] == 'Omean':
        menu = weak_menu(o)
        return sum((two_query_cost(menu[i], menu[j], prefix)
                    for i in range(6) for j in range(6) if i != j), F(0)) / 30
    if 'Omean' in labels:
        label = labels[0] if labels[1] == 'Omean' else labels[1]
        return sum((two_query_cost(membership[label], bit, prefix)
                    for bit in weak_menu(o)), F(0)) / 6
    return two_query_cost(membership[labels[0]], membership[labels[1]], prefix)


def expected_rhs(row):
    family = row['family']
    if family == 'IC_SOURCE2': return {'u2': '1'}
    if family == 'CAP': return {'K': '1'}
    if family == 'ACTUAL_SAFE': return {'u%d' % row['source']: '1'}
    if family == 'MAX': return {'F_X': '1'}
    if family == 'MX': return {'u5': '1'}
    if family == 'ACTUAL_RC': return {'u5': '1', 'F_X': '1'}
    return {}


def literal_triple(row, atom, q, tail):
    a = tuple(atom['a'])
    o, x = atom['o'], atom['x']
    assert len(a) == 6 and len(tail) == 4
    assert all(v in (0, 1) for v in a + (x, o, q) + tuple(tail))
    pure = dict(zip(ACTUAL, a))
    pure.update(X=x, Q=q)
    pure.update(zip(TAILS, tail))
    sequence = (a[0], q) + tuple(tail)
    family = row['family']
    labels = row['queries']
    rhs = expected_rhs(row)
    b_atom = sum((payoff(a, int(k[1:]) - 1) for k in rhs if k.startswith('u')), F(0))
    if 'F_X' in rhs: b_atom += share(x, sum(a[:4]), 0)
    b_K = F(int('K' in rhs))
    if family == 'IC_SOURCE2':
        A = payoff(sequence, 1)
    elif family == 'CAP':
        A = F(pure[labels[0]])
    elif family == 'ACTUAL_SAFE':
        j = row['source']
        A = share(pure[labels[0]], sum(a[:j-1]), 6-j)
    elif family == 'MAX':
        A = share(pure[labels[0]], sum(a[:4]), 0)
    elif family == 'MX':
        A = share(pure[labels[0]], sum(a[:4]), x)
    elif family == 'NEW_SAFE':
        j = row['source']
        menu = weak_menu(o) if labels[0] == 'Omean' else (pure[labels[0]],)
        cost = sum((share(bit, sum(sequence[:j-1]), 6-j) for bit in menu), F(0)) / len(menu)
        A = cost - payoff(sequence, j-1)
    elif family == 'NEW_PAIR':
        prefix = sum(sequence[:4])
        wallet = payoff(sequence, 4) + payoff(sequence, 5)
        # g(R5,R5) is the loss of R5's share when one covering rival is added.
        wallet += share(tail[2], prefix, 0) - share(tail[2], prefix, 1)
        A = weak_pair(labels, pure, o, prefix) - wallet
    elif family == 'ACTUAL_RC':
        A = weak_pair(labels, pure, o, sum(a[:4]))
    else:
        raise AssertionError(family)
    return A, b_atom, b_K


def signature(family, queries=(), source=None):
    labels = tuple(queries)
    if family in ('NEW_PAIR', 'ACTUAL_RC'):
        labels = tuple(sorted(labels, key=QUERIES.index))
    return family, source, labels


def expected_signatures():
    out = {signature('IC_SOURCE2')}
    for family in ('CAP', 'MAX', 'MX'):
        out.update(signature(family, [label]) for label in NEW)
    out.update(signature('ACTUAL_SAFE', [label], j)
               for label in TAILS for j in range(1, 7))
    out.update(signature('ACTUAL_SAFE', ['Q'], j) for j in (1, 3, 4, 5, 6))
    out.update(signature('NEW_SAFE', [label], j)
               for j in range(3, 7) for label in QUERIES)
    out.update(signature('NEW_PAIR', pair)
               for pair in combinations_with_replacement(QUERIES, 2))
    out.update(signature('ACTUAL_RC', pair)
               for pair in combinations_with_replacement(QUERIES, 2)
               if any(label in NEW for label in pair))
    assert len(out) == 243
    return out


def main():
    catalog = read('row_catalogue.json')
    rows = catalog['rows']
    assert len(rows) == 243 and catalog['genuine_rows'] == 243
    assert Counter(r['family'] for r in rows) == EXPECTED_COUNTS
    assert catalog['family_counts'] == EXPECTED_COUNTS
    assert tuple(catalog['query_descriptors']) == QUERIES
    assert tuple(catalog['old_roles']) == OLD and tuple(catalog['new_roles']) == NEW
    signatures = [signature(r['family'], r['queries'], r.get('source')) for r in rows]
    assert len(set(signatures)) == 243 and set(signatures) == expected_signatures()
    assert len(set(r['name'] for r in rows)) == 243
    assert [r['index'] for r in rows] == list(range(243))
    by_name = {r['name']: r for r in rows}
    for r in rows:
        assert r['rhs'] == expected_rhs(r)
        extension = r['queries'] == ['Q'] and (
            r['family'] in ('CAP', 'MAX', 'MX') or
            r['family'] == 'ACTUAL_SAFE')
        assert r['own_Q_extension'] == extension
        marker = ('distinct30_union' if r['queries'] == ['Omean', 'Omean'] else
                  'six_union' if 'Omean' in r['queries'] else 'pure_same_outer_index')
        assert r['inner_averaging'] == marker
    assert sum(r['own_Q_extension'] for r in rows) == 8
    assert [r['name'] for r in rows if r['inner_averaging'] == 'distinct30_union'] == ['NEW_PAIR|Omean|Omean']
    assert 'ACTUAL_SAFE_j2|Q' not in by_name
    assert 'ACTUAL_RC|Omean|Omean' not in by_name
    samples = read('literal_samples.json')
    assert samples['state_count'] == 12 and samples['rows_per_state'] == 243
    scalar_checks = 0
    for state in samples['states']:
        cs = state['coefficients']
        assert len(cs) == 243 and {c['row'] for c in cs} == set(by_name)
        for stored in cs:
            got = literal_triple(by_name[stored['row']], state['atom'], state['q'], state['tail'])
            want = tuple(F(stored[k]) for k in ('A', 'b_atom', 'b_K'))
            assert got == want, (state['id'], stored['row'], got, want)
            scalar_checks += 3
    assert scalar_checks == 8748

    # These exact finite checks validate the mean-cost reduction itself, not an LP.
    mean_states = mixed_states = 0
    for D in range(1, 6):
        for menu in product((0, 1), repeat=6):
            d = sum(menu); o = int(d != 0)
            literal = sum((two_query_cost(menu[i], menu[j], D-1)
                           for i in range(6) for j in range(6) if i != j), F(0)) / 30
            assert literal == F(d, 3*D) - F(d*(d-1), 30*D*(D+1))
            assert literal >= F(o, 3*D)
            mean_states += 1
            for t in (0, 1):
                actual = sum((two_query_cost(t, bit, D-1) for bit in menu), F(0)) / 6
                endpoint = sum((two_query_cost(t, bit, D-1) for bit in weak_menu(o)), F(0)) / 6
                assert actual >= endpoint
                assert endpoint == F(t, D) + F(o, 6*D) - F(t*o, 6*D*(D+1))
                mixed_states += 1
        for t, x in product((0, 1), repeat=2):
            assert two_query_cost(t, x, D-1) - share(t, D-1, x) == share(x, D-1, 0)
    omitted_safe_states = 0
    for a1, q, *tail in product((0, 1), repeat=6):
        assert share(q, a1, sum(tail)) >= share(q, a1, 4)
        omitted_safe_states += 1
    terminal_states = 0
    for sequence in product((0, 1), repeat=6):
        assert share(sequence[5], sum(sequence[:5]), 0) == payoff(sequence, 5)
        prefix = sum(sequence[:4]); y, z = sequence[4:]
        wallet = payoff(sequence, 4) + payoff(sequence, 5) + share(y, prefix, 0) - share(y, prefix, 1)
        pair = two_query_cost(y, z, prefix) - wallet
        own_safe5 = share(y, prefix, 1) - payoff(sequence, 4)
        assert pair == own_safe5
        terminal_states += 1

    # Signed coefficient identities for arbitrary (including negative) minima.
    moment_cases = 0
    for a0, a1 in product((F(-7, 3), F(-1), F(0), F(2, 5), F(11)), repeat=2):
        for o in (0, 1):
            delta = max(a1-a0, F(0)); gamma = max(a0-a1, F(0))
            m = a0 + delta*o/6 - gamma*o
            assert m == (a0 if not o else min((5*a0+a1)/6, a1))
            for q in (0, 1):
                aq = a1 if q else a0
                assert -aq + delta*q - gamma*q + a0 == 0
            assert -delta*o/6 + gamma*o - a0 == -m
            moment_cases += 1

    template = read('symbolic_template.json')
    release = read('main_point_release_template.json')
    assert template['optimizer_calls'] == 0 and template['matrix_constructed'] is False
    for key in ('fixed_input', 'fixed_matrix', 'fixed_rhs', 'full8192_matrix', 'certificate', 'projection_weights'):
        assert template[key] is None
    for key, value in release.items():
        if key not in ('status', 'source_history', 'required_common_X_semantics'):
            assert value is None, (key, value)
    assert template['state']['old_full_domain_size'] == 256
    assert template['state']['new_states_per_old_type'] == 32
    assert template['state']['eventual_projection_state_count'] == 8192

    sources = ['derivation.md', 'symbolic_coefficients.py', 'row_catalogue.json',
               'audit_interface.json', 'symbolic_template.json',
               'main_point_release_template.json', 'literal_samples.json']
    result = {
        'status': 'PASS_INDEPENDENT_SOURCE_CATALOGUE_AND_STATIC_SAMPLES',
        'genuine_rows': 243, 'family_counts': EXPECTED_COUNTS,
        'core_rows': 235, 'own_Q_additions': 8,
        'sample_states': 12, 'sample_row_triples': 2916,
        'exact_sample_scalar_comparisons': scalar_checks,
        'literal_distinct30_menu_states': mean_states,
        'literal_mixed_mean_menu_states': mixed_states,
        'omitted_source2_SAFE_Q_bit_states': omitted_safe_states,
        'terminal_zero_and_own_PAIR_duplicate_states': terminal_states,
        'signed_moment_identity_test_cases': moment_cases,
        'source_sha256': {str((SRC/n).relative_to(REPO)): digest(SRC/n) for n in sources},
        'source_claim': 'Every stated row is necessary for complete ordered-history pure SPE with one full-catalog f_P maximizer at actual P; any six legal query labels and their union suffice.',
        'no_fixed_point_bound': True, 'no_matrix_assembled': True,
        'no_optimizer_or_builder_or_Main_execution': True,
        'future_dimensions': {'nu_columns': '32*s', 'mass_equations': 's',
                              'q_moment_rows': '2*s', 'raw_inequalities': '243+2*s'},
        'future_universal_projection_domain': 'All 256 old types and all 8192 new states, including o=0 and all-zero; full q-moment interval retained.',
        'outstanding_errors': [],
        'not_claimed': ['fixed-point feasibility/infeasibility', 'Farkas certificate',
                        'full 8192-state coefficient matrix audit', 'complete SPE realization',
                        'new numerical welfare bound or best-known status'],
    }
    (HERE / 'source_audit_result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'genuine_rows', 'sample_row_triples',
                      'exact_sample_scalar_comparisons', 'literal_distinct30_menu_states',
                      'literal_mixed_mean_menu_states', 'outstanding_errors')}, indent=2))


if __name__ == '__main__':
    main()
