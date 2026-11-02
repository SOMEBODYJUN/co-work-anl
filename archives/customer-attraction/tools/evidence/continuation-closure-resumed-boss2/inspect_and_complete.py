"""Consume six recovered sources; complete only the six accidental float rows.

No original module is imported. No LP, full 437/447 matrix reconstruction,
exchangeable-catalog enumeration, or original main is run. Existing mature 447
input/audit and old indexed input remain dependencies rather than copied files.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
OLD = EVIDENCE / 'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
REWEIGHT = EVIDENCE / 'indexed-447-and-scaled-credit-primary/source-root/research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.json'
AUDIT447 = EVIDENCE / 'indexed-447-and-scaled-credit-primary/source-root/research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/audit_indexed_closure.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def descriptor(atom):
    return {key: atom[key] for key in
            ('bits', 'AB_hist', 'AE_hist', 'second_hist', 'menus_lh')}


def validate_atom(atom):
    assert set(atom['bits']) <= {'0', '1'} and len(atom['bits']) == 10
    d = None
    for field, arity in [('AB_hist', 3), ('AE_hist', 3), ('second_hist', 4)]:
        hist = atom[field]
        assert len(hist) == 2 ** arity
        assert all(type(n) is int and n >= 0 for n in hist) and sum(hist) == 5
        count = sum(n * ty[0] for n, ty in zip(hist, product((0, 1), repeat=arity)))
        if d is None:
            d = count
        assert count == d
    assert len(atom['menus_lh']) == 3
    for ell, h in atom['menus_lh']:
        assert type(ell) is int and type(h) is int
        assert 0 <= h <= d and 0 <= ell - h <= 5 - d
    return d


def six_own_t(primal):
    # These are expected terminal payoffs at a fixed named index i. Histograms
    # already include T at position 0. Uniform index selection gives factor 1/5.
    nodes = {
        'branch_AB': ('AB', 'AB_hist', 3),
        'branch_AE': ('AE', 'AE_hist', 3),
        'branch_S': ('A', 'second_hist', 4),
        'old_actual': ('ABC', 0, 2),
        'old_second': ('AEU', 1, 2),
        'old_third': ('ABE', 2, 2),
    }
    totals = {node: {'chosen': F(0), 'query': F(0), 'slack': F(0)} for node in nodes}
    contributing_terms = Counter()
    for atom in primal['atoms']:
        d = validate_atom(atom)
        mass = F(atom['mass_numerator'], primal['denominator'])
        bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
        for node, (prefix, field, arity) in nodes.items():
            if type(field) is int:
                ell, h = atom['menus_lh'][field]
                hist = [5 - d - ell + h, ell - h, d - h, h]
            else:
                hist = atom[field]
            for ty, n in zip(product((0, 1), repeat=arity), hist):
                if not n:
                    continue
                den = sum(bits[label] for label in prefix) + sum(ty[:-1]) + 1
                weight = mass * F(n, 5)
                totals[node]['chosen'] += weight * F(ty[-1], den)
                totals[node]['query'] += weight * F(ty[0], den)
                totals[node]['slack'] += weight * F(ty[-1] - ty[0], den)
                contributing_terms[node] += 1
    return totals, contributing_terms


def main():
    manifest = read(HERE / 'source-manifest.json')
    for source in manifest:
        path = HERE / 'original' / Path(source['path']).name
        assert path.stat().st_size == source['size'] and sha(path) == source['sha256']
    old = read(OLD)['primal']
    assert sha(OLD) == '18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
    assert len(old['atoms']) == 64
    for atom in old['atoms']:
        validate_atom(atom)

    exchange = read(HERE / 'original/exchangeable_last_closure.json')
    assert set(exchange) == {'scope', 'catalog_size', 'terminal_node_families',
        'checked_deviation_categories', 'negative_categories', 'failures',
        'node_chosen_payoffs', 'all_slacks'}
    exact, term_counts = six_own_t(old)
    float_keys = {node + ' -> T[i]' for node in exact}
    assert set(k for k, value in exchange['all_slacks'].items() if '.' in value or 'e' in value.lower()) == float_keys
    nodes = set(exchange['node_chosen_payoffs'])
    groups = ['T', 'AB:1', 'AB:2', 'AE:1', 'AE:2', 'S:1', 'S:2', 'S:3',
              'L_actual:1', 'L_second:1', 'L_third:1']
    expected = set()
    for node in nodes:
        expected.update(node + ' -> ' + label for label in 'ABCDEUVWXY')
        suffixes = ['any'] if node.startswith('fixed_') else ['i', 'j!=i']
        expected.update(node + ' -> ' + group + '[' + suffix + ']'
                        for group in groups for suffix in suffixes)
    assert set(exchange['all_slacks']) == expected
    assert len(nodes) == exchange['terminal_node_families'] == 9
    assert exchange['catalog_size'] == 65
    assert len(expected) == exchange['checked_deviation_categories'] == 255
    completions = []
    revised = {key: F(value) for key, value in exchange['all_slacks'].items()}
    for node, totals in exact.items():
        key = node + ' -> T[i]'
        assert totals['chosen'] == F(exchange['node_chosen_payoffs'][node])
        assert totals['slack'] == totals['chosen'] - totals['query'] > 0
        original = exchange['all_slacks'][key]
        decimal = F(original)
        binary = F.from_float(float(original))
        completions.append({'row': key, 'original_float_string': original,
            'exact_chosen_payoff': str(totals['chosen']),
            'exact_query_payoff': str(totals['query']),
            'exact_slack': str(totals['slack']),
            'decimal_string_minus_exact': str(decimal - totals['slack']),
            'binary_float_minus_exact': str(binary - totals['slack']),
            'decimal_difference_float': float(decimal - totals['slack']),
            'nonzero_histogram_terms': term_counts[node]})
        revised[key] = totals['slack']
    negative = {key: value for key, value in revised.items() if value < 0}
    assert len(negative) == exchange['negative_categories'] == len(exchange['failures']) == 14
    assert {entry['row'] for entry in exchange['failures']} == set(negative)
    for entry in exchange['failures']:
        assert set(entry) == {'row', 'slack', 'slack_float', 'chosen_payoff', 'deviation_payoff'}
        node = entry['row'].split(' -> ')[0]
        value = F(entry['slack'])
        assert value == revised[entry['row']] == F(entry['chosen_payoff']) - F(entry['deviation_payoff'])
        assert F(entry['chosen_payoff']) == F(exchange['node_chosen_payoffs'][node])
        assert float(value) == entry['slack_float']
    signs = Counter('negative' if value < 0 else 'zero' if value == 0 else 'positive'
                    for value in revised.values())

    off = read(HERE / 'original/offdiagonal_closure.json')
    assert set(off) == {'identity', 'source_sha256', 'source_atoms',
                       'all_atoms_compact_equals_raw_indices', 'rows', 'negative_rows', 'conclusion'}
    assert off['source_sha256'] == sha(OLD) and off['source_atoms'] == 64
    assert off['all_atoms_compact_equals_raw_indices'] is True
    off_values = {key: F(value) for key, value in off['rows'].items()}
    assert {key: str(value) for key, value in off_values.items() if value < 0} == off['negative_rows']
    # Compare saved exact same-family query totals with their factor-20 averages.
    off_links = {}
    for family, node, arity in [('AB', 'branch_AB', 3), ('AE', 'branch_AE', 3), ('Sbranch', 'branch_S', 4)]:
        query_group = 'S' if family == 'Sbranch' else family
        for pos in range(arity):
            key = f'{family}:5:offdiag:{pos}'
            query = 'T' if pos == 0 else query_group + ':' + str(pos)
            row = node + ' -> ' + query + '[j!=i]'
            assert off_values[key] == 20 * revised[row]
            off_links[key] = row

    aug = read(HERE / 'original/frozen_support_augmented.json')
    assert set(aug) == {'scope', 'row_count', 'source_support_types', 'positive_masses',
        'welfare', 'comparison_cover', 'ratio_float', 'gap_above_two', 'minimum_slack',
        'zero_slacks', 'atoms', 'slacks', 'conclusion'}
    expected_rows = set(old['rows']) | set(off_values)
    assert len(expected_rows) == aug['row_count'] == len(aug['slacks']) == 447
    assert set(aug['slacks']) == expected_rows
    saved_slacks = {key: F(value) for key, value in aug['slacks'].items()}
    assert min(saved_slacks.values()) == F(aug['minimum_slack']) == 0
    assert sum(value == 0 for value in saved_slacks.values()) == aug['zero_slacks'] == 50
    reweight = read(REWEIGHT)
    audit447 = read(AUDIT447)
    masses = list(map(F, reweight['exact_reweighting']))
    assert len(masses) == aug['source_support_types'] == 64
    assert len(aug['atoms']) == aug['positive_masses'] == sum(v > 0 for v in masses) == 42
    positive_indices = [i for i, v in enumerate(masses) if v]
    maps = []
    W = O = F(0)
    for new_index, (index, atom) in enumerate(zip(positive_indices, aug['atoms'])):
        assert set(atom) == {'bits', 'AB_hist', 'AE_hist', 'second_hist', 'menus_lh',
                            'mass_numerator', 'exact_mass'}
        assert descriptor(atom) == descriptor(old['atoms'][index])
        assert atom['mass_numerator'] is None
        assert F(atom['exact_mass']) == masses[index] > 0
        d = validate_atom(atom)
        W += masses[index] * int(any(map(int, atom['bits'][:5])))
        O += masses[index] * int(d > 0)
        maps.append({'saved_atom_index': new_index, 'old_support_index': index,
                     'exact_mass': str(masses[index])})
    assert W == F(aug['welfare']) == 1
    assert O == F(aug['comparison_cover']) == F(reweight['exact_primal_value'])
    assert O - 2 == F(aug['gap_above_two']) > 0 and float(O) == aug['ratio_float']
    # The mature 447 audit is not rerun; bind its already verified point and ten
    # exact added slacks to the newly recovered expanded report.
    mature_ten = audit447['new_row_totals']
    assert set(mature_ten) == set(off_values)
    assert all(F(mature_ten[key]) == saved_slacks[key] for key in mature_ten)

    report = {
        'scope': 'saved-source-consumption and six own-T exact completions only; no full matrix or LP rerun',
        'python': platform.python_version(),
        'primary_files': len(manifest), 'primary_sha256_all_match': True,
        'dependencies': [{'path': str(path.relative_to(EVIDENCE.parents[3])),
                          'bytes': path.stat().st_size, 'sha256': sha(path)}
                         for path in (OLD, REWEIGHT, AUDIT447)],
        'exchangeable': {'categories_consumed': 255, 'exact_source_categories': 249,
            'accidental_float_categories': 6, 'exact_completions': completions,
            'revised_sign_counts': dict(signs),
            'negative_report_internal_arithmetic_matches': True,
            'node_payoffs_consumed': len(nodes)},
        'offdiagonal': {'saved_rows_consumed': 10, 'negative_rows': off['negative_rows'],
            'saved_sum_equals_twenty_exchangeable_average': off_links,
            'new_literal_matrix_evaluations': 0},
        'augmented': {'atoms_all_fields_consumed': 42, 'old_support_types': 64,
            'positive_support_map': maps, 'saved_slacks_consumed': 447,
            'zero_saved_slacks': 50, 'positive_saved_slacks': 397,
            'W': str(W), 'O': str(O), 'gap_above_two': str(O - 2),
            'same_point_as_mature_447_audit': True,
            'ten_added_slacks_equal_mature_audit': True,
            'row_matrix_recomputed': False},
        'original_main_runs': 0, 'optimizer_calls': 0,
        'six_exact_rows_customer_atom_visits': 6 * len(old['atoms']),
        'six_exact_rows_nonzero_histogram_terms': sum(term_counts.values()),
    }
    (HERE / 'inspection-and-six-completions.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'primary_files': 6, 'exact_source_categories': 249,
        'float_rows_completed': 6, 'exchangeable_signs': dict(signs),
        'augmented_same_mature_point': True, 'augmented_saved_slacks': 447,
        'original_main_runs': 0, 'optimizer_calls': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
