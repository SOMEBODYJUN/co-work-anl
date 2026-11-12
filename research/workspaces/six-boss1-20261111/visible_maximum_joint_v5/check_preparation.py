#!/usr/bin/env python3
"""Independent literal/scalar checks; standard library, no source-code imports.

--stage1 reads only explicitly approved frozen packages and separates
Main-reviewed append sources from frozen sources still awaiting Main review.
--assembled is unavailable until Main supplies the final complete release.
The latter preserves each full source row and does not prune on any value.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = HERE.parents[3]
FINAL_RELEASE_SHA256 = '653e43d66feda8874fef8230fe95d689aa00378bca327284ddee43fcf300f821'
COORDINATES = ('variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns',
               'objective', 'equalities', 'equality_count', 'inequality_convention')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def names_digest(rows):
    encoded = (json.dumps([r['name'] for r in rows], ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def field_at(record, keys):
    for key in keys:
        record = record[key]
    return record


def bits(column):
    return [(column >> shift) & 1 for shift in range(8, -1, -1)]


def share(member, load_count):
    if load_count == 0:
        assert member == 0
        return F(0)
    return F(member, load_count)


def exact_columns(rows):
    checked = 0
    for row in rows:
        assert isinstance(row['rhs'], str)
        F(row['rhs'])
        for column, value in row['a'].items():
            assert str(int(column)) == column and 0 <= int(column) < 513
            assert isinstance(value, str)
            F(value)
        for column in range(513):
            F(row['a'].get(str(column), '0'))
            checked += 1
    return checked


def check_base(base, scales):
    assert base['variables'] == 513 and base['K_column'] == 512
    assert base['bit_order'] == ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'x', 'o', 'c']
    assert base['nonnegative_columns'] == list(range(513))
    assert len(base['atom_columns']) == 512
    for index, atom in enumerate(base['atom_columns']):
        b = bits(index)
        assert atom == {'index': index, 'old_index': index // 2, 'a': b[:6], 'x': b[6], 'o': b[7], 'c': b[8]}
    assert base['equality_count'] == len(base['equalities']) == 2
    opt, size = base['equalities']
    assert opt['name'] == 'OPT_union_normalization' and opt['rhs'] == '1'
    assert size['name'] == 'C_maximum_size' and size['rhs'] == '0'
    for col in range(513):
        b = bits(col) if col < 512 else [0] * 9
        assert F(base['objective'].get(str(col), '0')) == int(any(b[:6]))
        assert F(opt['a'].get(str(col), '0')) == b[7]
        assert F(size['a'].get(str(col), '0')) == (b[8] if col < 512 else -1)
    rows = base['raw_rows']
    assert len(rows) == base['raw_inequality_count'] == 1586
    assert scales['raw_order'] == [r['name'] for r in rows]
    assert set(scales['raw_scales']) == set(scales['raw_order'])
    assert len(set(scales['raw_order'])) == 1586
    for row in rows:
        divisor = scales['raw_scales'][row['name']]
        assert isinstance(divisor, str) and F(divisor) > 0
        if 'numerical_divisor' in row:
            assert row['numerical_divisor'] == divisor
    assert Counter(r['rhs'] for r in rows) == {'0': 1556, '-1': 30}
    return exact_columns(rows)


def check_ordered(rows):
    assert Counter(r['source'] for r in rows) == {1: 119, 2: 40, 3: 16, 4: 6}
    checked = 0
    for row in rows:
        i = row['source']
        theta = {int(j): F(v) for j, v in row['theta_by_source'].items()}
        assert set(theta) == set(range(i + 1, 6))
        s, n, ci = F(row['s']), 6 - i, F(7 - i, 2)
        a = F(25) + sum(theta.values(), F(0)) - s
        assert a > 0 and s >= 0 and all(v >= 0 for v in theta.values())
        for j in theta:
            assert theta[j] + sum((theta[h] / (6 * (7 - h) * (8 - h)) for h in theta if h > j), F(0)) <= F(5, 12)
        assert (s <= 9 if i >= 2 else all(s <= 15 + 5 * v for v in theta.values()))
        loss = max([F(0)] + [theta[j] + sum((theta[h] / (5 * (7 - h) * (8 - h)) for h in theta if h > j), F(0)) - F(2, 5) for j in theta])
        assert F(row['loss_L']) == loss
        assert F(row['source_IC_weight']) == a and F(row['K_weight']) == ci
        assert row['outer_average_divisor'] == '6' and row['inner_average_divisor'] == '5'
        assert row['inner_excludes_same_index'] is True and row['terminal_BR_average_weight'] == '1'
        g = {}
        for p in range(i):
            D = p + n + 1
            g[p] = (ci + F(24, D) + F(1, p + 1) - s / min(D, 5)
                    + sum((theta[j] / (p + 7 - j) for j in theta), F(0))) / 6
            if p == 0:
                g[p] -= F(5, 6) * loss
            assert F(row['G_by_prefix_load'][str(p)]) == g[p]
        for col in range(513):
            if col == 512:
                expected = ci
            else:
                b = bits(col)
                expected = a * share(b[i - 1], sum(b[:6])) - b[7] * g[sum(b[:i - 1])]
            assert F(row['a'][str(col)]) == expected, (row['name'], col)
            checked += 1
    assert checked == 92853
    return checked


def check_coupled(rows):
    assert len(rows) == 28 and all(r['source'] == 2 for r in rows)
    star = [F(12425, 31104), F(175, 432), F(5, 12)]
    checked = 0
    for row in rows:
        e, s = [F(v) for v in row['e3_e4_e5']], F(row['s'])
        assert len(e) == 3 and all(v >= 0 for v in e) and 0 <= s <= 9
        theta = [x + y for x, y in zip(star, e)]
        gamma = [e[0] + e[1] / 72 + e[2] / 36, e[1] + e[2] / 36, e[2]]
        a, hk = 25 + sum(theta) - s, F(5, 2) + sum(gamma)
        free = hk - s / 5
        for j in range(3):
            later = sum((e[h] / (72 if h == 1 else 36) for h in range(j + 1, 3)), F(0))
            assert F(4, 5) * e[j] + later <= F(3, 10) + star[j] / 5
            assert F(3, 4) * e[j] + later + s / 20 <= F(7, 10) + star[j] / 4
        assert [F(v) for v in row['theta3_theta4_theta5']] == theta
        assert [F(v) for v in row['middle_CAP_weights']] == [F(1, 2) + g for g in gamma]
        assert F(row['source_IC_weight']) == a > 0
        assert F(row['true_tail_K_weight']) == hk and F(row['C_size_free_multiplier']) == free
        assert row['forced_label'] == 'C_maximum_size_K' and row['C_size_equality'] == '|C|-K=0'
        assert row['terminal_CAP_weight'] == row['terminal_BR_average_weight'] == '1'
        for col in range(513):
            if col == 512:
                expected = s / 5
                before_free, ec = hk, F(-1)
            else:
                b = bits(col)
                p, c, o = b[0], b[8], b[7]
                B = F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1))
                B += sum((theta[j - 3] * F(o, 6 * (p + (j - 2) * c + 7 - j)) for j in (3, 4, 5)), F(0))
                expected = a * share(b[1], sum(b[:6])) - B
                before_free, ec = expected - free * c, F(c)
            assert before_free + free * ec == expected
            assert F(row['a'][str(col)]) == expected, (row['name'], col)
            checked += 1
    assert checked == 14364
    return checked


def check_minimal_c_only(rows):
    assert len(rows) == 28 and all(r['source'] == 2 for r in rows)
    checked, negative_free = 0, []
    for row in rows:
        tau, s = [F(v) for v in row['tau3_tau4_tau5']], F(row['s'])
        assert len(tau) == 3 and all(v >= 0 for v in tau) and 0 <= s <= 9
        beta = [F(1, 12) + tau[0] + tau[1] / 72 + tau[2] / 36,
                F(1, 12) + tau[1] + tau[2] / 36, F(1, 12) + tau[2]]
        a, hk = 25 + sum(tau) - s, 1 + sum(beta)
        free = hk - s / 5  # Signed free equality; never demand free >= 0.
        for j in range(3):
            later = sum((tau[h] / (72 if h == 1 else 36) for h in range(j + 1, 3)), F(0))
            assert F(4, 5) * tau[j] + later <= F(43, 60)
            assert F(3, 4) * tau[j] + later + s / 20 <= F(67, 60)
        assert [F(v) for v in row['middle_CAP_weights']] == beta
        assert F(row['source_IC_weight']) == a >= 16
        assert F(row['true_tail_K_weight']) == hk
        assert F(row['C_size_free_multiplier']) == free
        assert row['forced_label'] == 'C_maximum_size_K' and row['C_size_equality'] == '|C|-K=0'
        assert row['terminal_CAP_weight'] == row['terminal_BR_average_weight'] == '1'
        if free < 0:
            negative_free.append({'name': row['name'], 'signed_C_multiplier': str(free)})
        for col in range(513):
            if col == 512:
                expected, before_free, ec = s / 5, hk, F(-1)
            else:
                b = bits(col)
                p, c, o = b[0], b[8], b[7]
                B = F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1))
                B += sum((tau[j - 3] * F(o, 6 * (p + (j - 2) * c + 7 - j)) for j in (3, 4, 5)), F(0))
                expected = a * share(b[1], sum(b[:6])) - B
                before_free, ec = expected - free * c, F(c)
            assert before_free + free * ec == expected
            assert F(row['a'][str(col)]) == expected, (row['name'], col)
            checked += 1
    assert checked == 14364
    assert any(r['signed_C_multiplier'] == '-11/20' for r in negative_free)
    return checked, negative_free


def check_minimal_general_or_ordered(rows, ordered):
    """Rebuild the two final source formulas, retaining S and min(D,5)."""
    per_source_vertices = {1: 90, 2: 28, 3: 12, 4: 5, 5: 2}
    multiplier = 1 if ordered else 8
    assert Counter(r['source'] for r in rows) == {i: count * multiplier for i, count in per_source_vertices.items()}
    q0 = F(1, 5) if ordered else F(1, 6)
    parameter_cache, vertices, role_sequences = {}, {i: set() for i in range(1, 6)}, {}
    checked = 0
    for row_index, row in enumerate(rows):
        i = row['source']
        field = 'tau_by_source' if ordered else 'tau_by_true_source'
        tau = {int(j): F(v) for j, v in row[field].items()}
        assert set(tau) == set(range(i + 1, 6)) and all(v >= 0 for v in tau.values())
        s = F(row['s'])
        assert s >= 0 and (i == 1 or s <= 9)
        a = F(25) + sum(tau.values(), F(0)) - s
        beta = {j: q0 / 2 + tau[j] + sum((q0 * tau[h] / ((7 - h) * (8 - h)) for h in tau if h > j), F(0)) for j in tau}
        S = 1 + sum(beta.values(), F(0))
        assert a > 0 and F(row['source_IC_weight']) == a
        assert {int(j): F(v) for j, v in row['middle_CAP_weights'].items()} == beta
        assert row['terminal_CAP_weight'] == row['terminal_BR_average_weight'] == '1'
        for j in tau:
            assert beta[j] - tau[j] / 5 <= F(4, 5)
            assert beta[j] - tau[j] / 4 + s / 20 <= (F(5, 4) if i == 1 else F(6, 5))
        if i == 1:
            for j in tau:
                for k in tau:
                    if j < k:
                        assert beta[j] + beta[k] - (tau[j] + tau[k]) / 4 + s / 20 <= 2
        key = (i, tuple(tau.items()), s)
        vertices[i].add(key)
        if key not in parameter_cache:
            costs = {}
            for p in range(i):
                D = p + 7 - i
                if ordered:
                    costs[p] = (S + F(24, D) - s / min(D, 5) + F(1, p + 1)
                                + sum((tau[j] / (p + 7 - j) for j in tau), F(0))) / 6
                else:
                    for t in (0, 1):
                        for o in (0, 1):
                            costs[p, t, o] = (S * t + F(24 * t, D) - s * F(t, min(D, 5))
                                + F(o, 6 * (p + 1 + (6 - i) * t))
                                + sum((tau[j] * F(o, 6 * (p + (j - i) * t + 7 - j)) for j in tau), F(0)))
            parameter_cache[key] = costs
        costs = parameter_cache[key]
        if ordered:
            assert F(row['K_weight']) == S and row['uses_C_size_equality'] is False
            assert row['outer_average_divisor'] == '6' and row['inner_average_divisor'] == '5'
            assert row['inner_excludes_same_index'] is True
            assert {int(p): F(v) for p, v in row['G_by_prefix_load'].items()} == costs
        else:
            assert row['raw_row_index'] == row_index and row['C_size_equality_eliminated'] is False
            assert row['H_denominator'] == 'min(p+7-source,5)' and F(row['total_K_weight']) == S
            assert [F(v) for v in row['parameters']] == list(tau.values()) + [s]
            role = row['forced_target']
            role_sequences.setdefault(key, []).append(role)
            role_column = int(role[1:]) - 1 if role.startswith('A') else {'X': 6, 'C': 8}[role]
        for column in range(513):
            if column == 512:
                expected = S
            else:
                b = bits(column)
                p = sum(b[:i - 1])
                minimum = b[7] * costs[p] if ordered else costs[p, b[role_column], b[7]]
                expected = a * share(b[i - 1], sum(b[:6])) - minimum
            assert F(row['a'][str(column)]) == expected, (row['name'], column)
            checked += 1
    assert {i: len(values) for i, values in vertices.items()} == per_source_vertices
    if not ordered:
        roles = [f'A{i}' for i in range(1, 7)] + ['X', 'C']
        assert all(sequence == roles for sequence in role_sequences.values())
    assert checked == (70281 if ordered else 562248)
    return checked


def check_source_coordinate_schema(package, coords, family, base):
    """Independent schema interpretation, without importing the builder."""
    assert coords['variables'] == 513 and coords['bit_order'] == base['bit_order']
    if package == 'ordered_minimal_cap':
        assert coords['all_512_types_lexicographic'] is True
        assert coords['K_is_independent'] is True and coords['uses_C_equality'] is False
        assert coords['raw_scale_terminal_BR_average'] == '1' and coords['numeric_positive_divisor'] == '25'
        assert len(coords['columns']) == 513
        decoded = []
        for col, stored in enumerate(coords['columns']):
            if col == 512:
                assert stored == {'column': 512, 'kind': 'independent_K'}
                assert stored['column'] == family['K_column'] == base['K_column']
            else:
                expected_bits = bits(col)
                assert set(stored) == {'column', 'bits', 'type_string'}
                assert stored['column'] == col and stored['bits'] == expected_bits
                assert stored['type_string'] == format(col, '09b')
                decoded.append({'index': col, 'old_index': col // 2, 'a': expected_bits[:6],
                                'x': expected_bits[6], 'o': expected_bits[7], 'c': expected_bits[8]})
        assert decoded == base['atom_columns']
        adapter = 'explicit_columns_bits_and_independent_K_record'
    else:
        assert package in {'all_source_ordered_menu_cells', 'source2_cap_coupled_internal_safe',
                           'source2_minimal_cap_safe', 'all_source_minimal_cap_safe'}
        for key in ('K_column', 'atom_columns'):
            assert coords[key] == base[key], (package, key)
        if 'nonnegative_columns' in coords:
            assert coords['nonnegative_columns'] == base['nonnegative_columns']
        if 'C_size_equality' in coords:
            equality = coords['C_size_equality']
            assert equality['rhs'] == '0'
            assert all(F(equality['a'].get(str(c), '0')) == (F(c & 1) if c < 512 else -1) for c in range(513))
        if package == 'all_source_ordered_menu_cells':
            assert coords['normalization_used'] is False and coords['C_size_equality_used'] is False
        if package == 'all_source_minimal_cap_safe':
            assert coords['C_equality_not_used_in_general_rows'] is True
            assert coords['legal_forced_targets'] == [f'A{i}' for i in range(1, 7)] + ['X', 'C']
            assert coords['numerical_divisor'] == '25'
        adapter = 'canonical_atom_columns_and_K_column'
    return {'adapter': adapter, 'all_512_atom_routes_checked': True,
            'independent_K_route_checked': True, 'source_bytes_modified': False}


def check_raw_identity_statistics(rows):
    seen, zero_rows, duplicates = {}, [], []
    for index, row in enumerate(rows):
        vector = tuple(F(row['a'].get(str(j), '0')) for j in range(513))
        key = (vector, F(row['rhs']))
        if not any(vector) and key[1] == 0:
            zero_rows.append({'raw_index': index, 'name': row['name']})
        if key in seen:
            first = seen[key]
            duplicates.append({'raw_index': index, 'name': row['name'],
                               'first_raw_index': first, 'first_name': rows[first]['name']})
        else:
            seen[key] = index
    diagnostic = load(HERE / 'raw_identity_diagnostics.json')
    assert diagnostic['raw_rows'] == len(rows)
    assert diagnostic['zero_rows'] == zero_rows and diagnostic['duplicate_rows'] == duplicates
    assert diagnostic['duplicate_count'] == len(duplicates)
    assert diagnostic['distinct_nonzero_affine_rows'] == sum(bool(any(vector)) or rhs != 0 for vector, rhs in seen)
    assert diagnostic['rhs_counts'] == dict(Counter(r['rhs'] for r in rows))
    assert diagnostic['all_raw_rows_retained'] and diagnostic['diagnostic_only'] and not diagnostic['pruning_performed']
    return {'raw_zero_rows': zero_rows, 'raw_duplicate_rows': len(duplicates),
            'distinct_nonzero_affine_rows_diagnostic_only': diagnostic['distinct_nonzero_affine_rows'],
            'all_zero_and_duplicate_rows_retained': True}


def check_general_C_identity(families_by_name, combined_rows):
    c_rows = families_by_name['source2_minimal_cap_safe']['rows']
    general_rows = [row for row in families_by_name['all_source_minimal_cap_safe']['rows']
                    if row['source'] == 2 and row['forced_target'] == 'C']
    c_lookup = {(tuple(F(v) for v in row['tau3_tau4_tau5']), F(row['s'])): row for row in c_rows}
    assert len(c_lookup) == len(general_rows) == 28
    raw_indices = {row['name']: index for index, row in enumerate(combined_rows)}
    records = []
    for row in general_rows:
        key = (tuple(F(row['tau_by_true_source'][str(j)]) for j in (3, 4, 5)), F(row['s']))
        c_row = c_lookup[key]
        mu = F(c_row['C_size_free_multiplier'])
        assert F(row['total_K_weight']) == F(c_row['true_tail_K_weight'])
        for column in range(513):
            ec = F(column & 1) if column < 512 else F(-1)
            assert F(row['a'][str(column)]) - F(c_row['a'][str(column)]) + mu * ec == 0
        records.append({'general_name': row['name'], 'C_only_name': c_row['name'],
                        'general_raw_index': raw_indices[row['name']], 'C_only_raw_index': raw_indices[c_row['name']],
                        'signed_mu': str(mu), 'full_columns_checked': 513, 'all_residuals_exactly_zero': True})
    output = {'status': 'PASS_ALL28_GENERAL_TO_C_ONLY_SIGNED_EQUALITY_IDENTITIES',
              'identity': 'R_general = R_C_only - mu*(|C|-K)', 'columns_checked': 14364,
              'both_complete_families_retained': True, 'new_equality_elimination': False,
              'optimizer_calls': 0, 'records': records}
    (HERE / 'source2_general_C_identity_checks.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'identities': 28, 'columns_checked': 14364, 'both_complete_families_retained': True}


def check_spec(spec, base, require_main_review=True):
    package = spec['package']
    for name, expected in spec['files'].items():
        assert Path(name).name == name
        assert digest(WS / package / name) == expected, (package, name)
    if require_main_review:
        assert spec['main_source_review_complete'] is True
        assert digest(WS / spec['main_check_file']) == spec['main_check_sha256']
    else:
        assert spec['main_source_review_complete'] is False
        assert spec['main_check_file'] is None and spec['main_check_sha256'] is None
    family = load(WS / package / 'exact_family.json')
    manifest = load(WS / package / 'freeze_manifest.json')
    assert field_at(manifest, spec['manifest_family_sha_path']) == spec['files']['exact_family.json']
    assert field_at(manifest, spec['manifest_raw_count_path']) == spec['raw_count']
    coords = load(WS / package / 'coordinate_contract.json')
    assert spec['rows_key'] == 'rows' and isinstance(family['rows'], list)
    rows = family['rows']
    assert len(rows) == family[spec['count_key']] == spec['raw_count']
    assert family['variables'] == 513 and family['K_column'] == 512 and family['optimizer_calls'] == 0
    assert names_digest(rows) == spec['row_order_sha256']
    coordinate_check = check_source_coordinate_schema(package, coords, family, base)
    for row in rows:
        assert set(row['a']) == {str(j) for j in range(513)}
        assert row['rhs'] == '0' and row['numerical_divisor'] == '25'
        assert row[spec['terminal_BR_weight_field']] == '1'
    inspected = exact_columns(rows)
    reconstructed, negative_free = 0, []
    if package == 'all_source_ordered_menu_cells':
        reconstructed = check_ordered(rows)
    elif package == 'source2_cap_coupled_internal_safe':
        reconstructed = check_coupled(rows)
    elif package == 'source2_minimal_cap_safe':
        reconstructed, negative_free = check_minimal_c_only(rows)
    elif package == 'all_source_minimal_cap_safe':
        reconstructed = check_minimal_general_or_ordered(rows, ordered=False)
    elif package == 'ordered_minimal_cap':
        reconstructed = check_minimal_general_or_ordered(rows, ordered=True)
    else:
        raise AssertionError(f'Unapproved complete family: {package}')
    return family, {'package': package, 'raw_rows': len(rows), 'all_column_values_examined': inspected,
                    'independent_formula_columns_reconstructed': reconstructed,
                    'raw_scale': 'terminal BR mean weight 1', 'positive_numerical_divisor': '25',
                    'source_IC_weight_is_not_the_numerical_divisor': True,
                    'uses_C_equality_in_source': spec['uses_C_equality_in_source'],
                    'additional_C_equality_elimination': False,
                    'signed_negative_free_multipliers_retained': negative_free,
                    'coordinate_check': coordinate_check,
                    'Main_final_source_review_complete': require_main_review}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--stage1', action='store_true')
    mode.add_argument('--assembled', action='store_true')
    args = parser.parse_args()
    assert not (HERE / 'freeze_manifest.json').exists(), 'Never replace frozen checks.'
    contract = load(HERE / 'preparation_contract.json')
    for path, expected in contract['direct_read_pins'].items():
        assert digest(REPO / path) == expected, path
    base = load(WS / contract['baseline']['package'] / 'exact_input.json')
    old_scales = load(WS / contract['baseline']['package'] / 'numerical_scaling.json')
    baseline_columns = check_base(base, old_scales)
    specs = contract['known_append_sources']
    release = None
    if args.assembled:
        release_path = HERE / 'final_release.json'
        if not release_path.is_file():
            raise SystemExit('WAITING_MAIN_FINAL_RELEASE: complete preparation check is unavailable.')
        assert digest(release_path) == FINAL_RELEASE_SHA256
        release = load(release_path)
        assert release['status'] == 'MAIN_RELEASED_COMPLETE_SOURCE_ASSEMBLY'
        assert release['owner'] == 'Boss1/Main' and release['assembly_authorized'] is True
        assert release['optimizer_authorized'] is release['freeze_authorized'] is False
        assert release['final_source_review_complete'] is True
        assert digest(HERE / 'source_review.md') == release['final_source_review_sha256']
        assert (HERE / 'source_review.md').read_text(encoding='utf-8').startswith('# FINAL_COMPLETE_SOURCE_REVIEW\n')
        assert release['baseline'] == contract['baseline']
        assert release['append_sources'][:len(specs)] == specs
        decisions = release['pending_source_decisions']
        assert set(decisions) == {p['id'] for p in contract['pending_sources']}
        pending_names = []
        for pending in contract['pending_sources']:
            decision = decisions[pending['id']]
            assert isinstance(decision['include'], bool)
            if pending['required_in_final_input']:
                assert decision['include'] is True
            if decision['include']:
                if pending['package'] is not None:
                    assert decision['package'] == pending['package']
                pending_names.append(decision['package'])
            else:
                assert decision['main_reason']
        assert len(pending_names) == len(set(pending_names))
        assert {s['package'] for s in release['append_sources'][len(specs):]} == set(pending_names)
        assert len(release['append_sources']) == len(specs) + len(pending_names)
        specs = release['append_sources']
    families, checks = [], []
    for spec in specs:
        family, result = check_spec(spec, base)
        families.append(family)
        checks.append(result)
    report = {
        'status': 'PASS_STAGE1_KNOWN_SOURCE_CONTRACTS' if args.stage1 else 'PASS_COMPLETE_LITERAL_PREPARATION',
        'optimizer_calls': 0, 'builder_or_source_code_imported': False,
        'baseline_raw_rows': 1586, 'baseline_full_columns_examined': baseline_columns,
        'columns': 513, 'atom_columns': 512, 'equalities': 2, 'old_rhs_minus_one_rows': 30,
        'baseline_positive_scale_strings': 1586, 'source_checks': checks,
        'known_prefix_raw_subtotal_only': contract['known_prefix_subtotal'],
        'final_raw_count': None, 'complete_input_generated': False, 'final_input_frozen': False,
        'point_values_loaded_or_bound': False, 'support_restriction': False, 'fixed_K': False,
        'source_rows_selected_by_values': False, 'in_progress_source_directories_read': False,
        'mathematical_scope': ('Frozen source formulas and literal routing. Stage1 reports pending sources separately; assembled mode binds Main full domain/true-cost checks for every admitted complete family. Main supplies complete source geometry and true hidden-state proof checks. This checker independently rebuilds every appended formula coefficient and verifies literal complete-source assembly.'),
        'half_status': 'OPEN',
    }
    filename = 'stage1_known_source_check.json'
    if args.stage1:
        assert contract['final_raw_count'] is None
        assert not (HERE / 'exact_input.json').exists()
        report['pending_sources'] = contract['pending_sources']
        pending_checks = []
        for spec in contract.get('reviewable_frozen_pending_sources', []):
            _, pending_check = check_spec(spec, base, require_main_review=False)
            pending_checks.append(pending_check)
        report['reviewable_frozen_pending_source_checks'] = pending_checks
    else:
        inp = load(HERE / 'exact_input.json')
        rows = inp['raw_rows']
        total = release['final_raw_count']
        assert total == 3056 == 1586 + sum(spec['raw_count'] for spec in specs)
        assert len(rows) == inp['raw_inequality_count'] == total
        assert rows[:1586] == base['raw_rows']
        assert inp['baseline_metadata'] == {k: v for k, v in base.items() if k != 'raw_rows'}
        assert inp['source_bindings'] == release
        assert inp['source_pins_sha256'] == digest(HERE / 'source_pins.json')
        assert inp['source_review_sha256'] == release['final_source_review_sha256']
        assert inp['coordinate_adapter_checks_sha256'] == digest(HERE / 'coordinate_adapter_checks.json')
        assert inp['optimizer_calls'] == 0 and inp['preparation_only']['optimization_authorized'] is False
        for key in COORDINATES:
            assert inp[key] == base[key], key
        scales = load(HERE / 'numerical_scaling.json')
        assert scales['raw_order'] == [r['name'] for r in rows]
        assert len(scales['raw_scales']) == len(set(scales['raw_order'])) == total
        assert scales['raw_order'][:1586] == old_scales['raw_order']
        assert scales['baseline_scaling_metadata'] == {k: v for k, v in old_scales.items() if k not in ('raw_order', 'raw_scales')}
        for row in rows[:1586]:
            assert scales['raw_scales'][row['name']] == old_scales['raw_scales'][row['name']]
        start = 1586
        expected_metadata = []
        catalog = load(HERE / 'row_catalog.json')
        assert catalog[:1586] == load(WS / contract['baseline']['package'] / 'row_catalog.json')
        for spec, family in zip(specs, families):
            source_rows = family['rows']
            assert rows[start:start + len(source_rows)] == source_rows
            expected_metadata.append({'package': spec['package'], 'metadata': {k: v for k, v in family.items() if k != 'rows'}})
            for index, row in enumerate(source_rows):
                assert scales['raw_scales'][row['name']] == row['numerical_divisor'] == '25'
                entry = {k: v for k, v in row.items() if k != 'a'}
                entry.update(raw_index=start + index, source_row_index=index,
                             source_package=spec['package'], stored_coefficient_entries=513)
                assert catalog[start + index] == entry
            start += len(source_rows)
        assert start == total and inp['source_family_metadata'] == expected_metadata
        for name in ('column_routing.json', 'column_routing.tsv'):
            assert (HERE / name).read_bytes() == (WS / contract['baseline']['package'] / name).read_bytes()
        for path, expected in load(HERE / 'source_pins.json')['sources'].items():
            assert digest(REPO / path) == expected, path
        assert all(isinstance(v, str) and F(v) > 0 for v in scales['raw_scales'].values())
        assert Counter(r['rhs'] for r in rows)['-1'] == 30
        assert rows[45] == base['raw_rows'][45] and rows[45]['a'] == {}
        assert sum(result['independent_formula_columns_reconstructed'] for result in checks) == 1470 * 513
        report.update(check_raw_identity_statistics(rows))
        by_package = {spec['package']: family for spec, family in zip(specs, families)}
        report['source2_general_C_equality_identity'] = check_general_C_identity(by_package, rows)
        report.update(final_raw_count=total, complete_input_generated=True,
                      input_sha256=digest(HERE / 'exact_input.json'),
                      total_full_columns_examined=baseline_columns + sum(c['all_column_values_examined'] for c in checks),
                      appended_formula_columns_reconstructed=1470 * 513,
                      all_source_row_dictionaries_and_order_literal=True)
        filename = 'literal_check_result.json'
    for path, expected in contract['direct_read_pins'].items():
        assert digest(REPO / path) == expected, path
    report['checker_sha256'] = digest(HERE / 'check_preparation.py')
    (HERE / filename).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
