#!/usr/bin/env python3
"""Independent exact preparation checker: stdlib only, no builder imports.

New columns are rebuilt from actual source shares, genuine budget costs and
all true tails. The complete v5 prefix is compared as literal JSON objects.
No optimizer, candidate, face, project-module import or LP release is used.
"""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BITS = list(itertools.product((0, 1), repeat=9))
TARGETS = {**{'A' + str(j): j - 1 for j in range(1, 7)}, 'X': 6, 'C': 8}
COUNTS = Counter()
BASE_SHA = '12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
BASE_MANIFEST = 'b49d8bba4197fc6d656005770dace9c5a777816b5e3eaa1105565fb23db51a27'
EXPECTED = [
    ('source2_lambda_strip', 230, 'a3f42d72be4ebecd15f8f74315103ae90bb940d4031fa712211219e2c75f96a4', 'cb6f952edef0f8278fd671cc6ef1f38f7fd47a59d094c008dba9d1376ddc5fac'),
    ('source2_lambda_anchor_complete', 160, '43e6c3db3e1631932af72f839dd2e46d7454d23d1884cdc9105cd1609d0821fc', 'a2a7bca9b52d37e6c92f3c67daff0a7c0b7fdd4e9caf50d358bae02eeb2eb48c'),
    ('later_sources_lambda_cells', 550, '275e95c2a650aa90bbc86b225cc75a125b5184d27d2b5b3b6e667e9de486643c', '22fb5d0f5af953ac6a7c74faadca5ab9ba5703e30d83445b27085a26900de0e6'),
    ('source2_conditional_redistribution', 180, '9cfbe8eb409b6fd505ea1663183a3a3220602222952a5ba0291e13398578285a', 'cbcec20f5897e4b445cb256d55093a1d9db8e2de4a0b00d766a6ab24af2d74be'),
    ('main_root270_strict_outside', 1, '403776eb344d9c14bd3dfa5e0c779d11eb2dc0c52f7155d05fdb910481c43c52', 'a803b4704af3c6a1528deca3f67350a4becab6375133f036058cfba867d37eff'),
]
BASE_BLOCKS = [
    ('inherited1002', 0, 1001), ('source2_nested', 1002, 1002),
    ('source2_reweighted', 1003, 1018), ('all_source_nested', 1019, 1049),
    ('all_source_joint_reweighted', 1050, 1585), ('ordered_cells', 1586, 1766),
    ('source2_cap_coupled', 1767, 1794), ('source2_minimal_cap', 1795, 1822),
    ('all_source_minimal_cap', 1823, 2918), ('ordered_minimal_cap', 2919, 3055),
]
MINIMUM_TABLES = {}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def objhash(obj):
    data = (json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode()
    return hashlib.sha256(data).hexdigest()


def save(name, obj):
    assert not (HERE / 'freeze_manifest.json').exists(), 'Already frozen'
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def audit_pins():
    pins = read(HERE / 'source_pins.json')
    for rec in pins['files']:
        path = REPO / rec['path']
        assert digest(path) == rec['sha256'], rec['path']
        assert path.stat().st_size == rec['bytes'], rec['path']
    assert digest(WS / 'visible_maximum_joint_v5/exact_input.json') == BASE_SHA
    assert digest(WS / 'visible_maximum_joint_v5/freeze_manifest.json') == BASE_MANIFEST
    for name, count, manifest_sha, family_sha in EXPECTED:
        folder = WS / name
        assert digest(folder / 'freeze_manifest.json') == manifest_sha
        filename = 'ROOT270_STRICT_C_OUTSIDE.json' if count == 1 else 'exact_family.json'
        assert digest(folder / filename) == family_sha
        manifest = read(folder / 'freeze_manifest.json')
        entries = manifest.get('artifacts', manifest.get('files'))
        if isinstance(entries, list):
            recorded = {r['path']: r['sha256'] for r in entries}
        else:
            recorded = entries
        assert recorded[filename] == family_sha
        assert recorded['proof.md'] == digest(folder / 'proof.md')
    COUNTS['source_pins_per_pass'] = len(pins['files'])


def complete(a):
    if isinstance(a, list):
        assert len(a) == 513 and all(isinstance(x, str) for x in a)
        return [Q(x) for x in a]
    assert isinstance(a, dict)
    assert all(str(int(k)) == k and 0 <= int(k) <= 512 for k in a)
    assert all(isinstance(x, str) for x in a.values())
    return [Q(a.get(str(k), '0')) for k in range(513)]


def canonical_caps(i, q0, tau):
    return tuple(q0 / 2 + tau[j-i-1]
                 + sum((q0 * tau[l-i-1] / ((7-l) * (8-l)) for l in range(j+1, 6)), Q())
                 for j in range(i+1, 6))


@lru_cache(maxsize=None)
def minimum(i, p, t, q, source_weight, tau, beta):
    """Sum individual budget terms, not a formula imported from a source.

    q is a legal indexed-query mean or its certified pure-union weakening.
    Each actual payoff uses the branch's final load; each internal deviation
    query uses its own worst-case number of later providers.
    """
    records = []
    for tail in itertools.product((0, 1), repeat=6-i):
        middle = tail[:-1]
        z = tail[-1]
        load = p + t + sum(tail)
        actual_source = Q(t, load) if load else Q()
        actual_terminal = Q(z, load) if load else Q()
        value = source_weight * actual_source
        value -= actual_terminal
        for pos, member in enumerate(middle):
            actual_internal = Q(member, load) if load else Q()
            value -= tau[pos] * actual_internal
            value += beta[pos] * member
        value += z
        value += q / (p + t + sum(middle) + 1)
        for pos, j in enumerate(range(i+1, 6)):
            query_denominator = p + t + sum(middle[:pos]) + 7 - j
            value += tau[pos] * q / query_denominator
        records.append((tail, value))
    best = min(v for _, v in records)
    tails = tuple(t for t, v in records if v == best)
    COUNTS['independent_true_tail_costs'] += len(records)
    COUNTS['independent_conditional_minima'] += 1
    COUNTS['all_weak_minimum_occurrences'] += len(tails)
    key = '|'.join(map(str, [i, p, t, q, source_weight, tau, beta]))
    MINIMUM_TABLES[key] = {'source': i, 'p': p, 't': t, 'q': str(q),
        'source_IC_weight': str(source_weight), 'tau': list(map(str, tau)),
        'beta': list(map(str, beta)), 'minimum': str(best),
        'all_attainers': [list(t) for t in tails],
        'all_costs': [{'tail': list(t), 'cost': str(v)} for t, v in records]}
    return best


@lru_cache(maxsize=None)
def ordered_G(i, p, source_weight, tau, beta):
    values = []
    for d in range(7):
        total = Q()
        if d < 6:
            total += (6-d) * minimum(i, p, 0, Q(d, 5), source_weight, tau, beta)
        if d > 0:
            total += d * minimum(i, p, 1, Q(d-1, 5), source_weight, tau, beta)
        values.append(total / 6)
    assert values[0] == 0
    g = min(values[1:])
    assert g == values[1] and all(v > g for v in values[2:])
    COUNTS['ordered_all_seven_multiplicity_values'] += 7
    COUNTS['ordered_unique_d1_endpoint_checks'] += 1
    return g


def direct_vector(i, target, ordered, source_weight, tau, beta, mu=Q()):
    S = 1 + sum(beta, Q())
    assert source_weight >= 0 and all(x >= 0 for x in tau) and all(x >= 0 for x in beta)
    answer = []
    for bits in BITS:
        actual = bits[:6]
        load = sum(actual)
        share = Q(actual[i-1], load) if load else Q()
        p, o, c = sum(actual[:i-1]), bits[7], bits[8]
        if ordered:
            lower = o * ordered_G(i, p, source_weight, tau, beta)
        else:
            lower = minimum(i, p, bits[TARGETS[target]], Q(o, 6), source_weight, tau, beta)
        answer.append(source_weight * share - lower + mu * c)
    answer.append(S - mu)
    return answer


def column_contract(folder, base=False):
    data = read(folder / ('exact_input.json' if base else 'coordinate_contract.json'))
    order = data.get('bit_order', data.get('customer_bits'))
    assert order == ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'x', 'o', 'c']
    cols = data.get('atom_columns') if base else data.get('columns', data.get('customer_columns'))
    if base:
        assert len(cols) == 512
        for k, bits in enumerate(BITS):
            assert cols[k]['index'] == k and cols[k]['old_index'] == k // 2
            assert cols[k]['a'] == list(bits[:6])
            assert [cols[k]['x'], cols[k]['o'], cols[k]['c']] == list(bits[6:])
    else:
        assert len(cols) in (512, 513)
        for k, bits in enumerate(BITS):
            assert cols[k].get('column', cols[k].get('index')) == k
            assert cols[k]['bits'] == list(bits)
        if len(cols) == 513:
            assert cols[512] == {'column': 512, 'kind': 'independent_K'}
    assert data.get('K_column', 512) == 512
    COUNTS['column_contract_checks'] += 513


def parent_contract(base, scaling, catalog):
    assert base['variables'] == 513 and base['K_column'] == 512
    assert base['nonnegative_columns'] == list(range(513))
    assert base['equality_count'] == 2 and len(base['equalities']) == 2
    oeq = {'name': 'OPT_union_normalization',
           'a': {str(k): '1' for k, b in enumerate(BITS) if b[7]}, 'rhs': '1'}
    ceq = {'name': 'C_maximum_size',
           'a': {**{str(k): '1' for k, b in enumerate(BITS) if b[8]}, '512': '-1'}, 'rhs': '0'}
    assert base['equalities'] == [oeq, ceq]
    assert base['objective'] == {str(k): '1' for k, b in enumerate(BITS) if any(b[:6])}
    assert base['inequality_convention'] == 'a dot z >= rhs'
    assert len(base['raw_rows']) == base['raw_inequality_count'] == 3056
    assert scaling['raw_order'] == [r['name'] for r in base['raw_rows']]
    assert list(scaling['raw_scales']) == scaling['raw_order']
    assert len(catalog) == len(scaling['raw_scales']) == 3056
    assert scaling['exact_coefficients_numerically_divided'] is False
    for k, row in enumerate(base['raw_rows']):
        assert catalog[k]['raw_index'] == k and catalog[k]['name'] == row['name']
        assert catalog[k]['numerical_divisor'] == scaling['raw_scales'][row['name']]
        assert Q(scaling['raw_scales'][row['name']]) > 0
        complete(row['a'])
    assert Counter(r['rhs'] for r in base['raw_rows']) == {'0': 3026, '-1': 30}
    COUNTS['independent_equality_columns'] = 1026
    COUNTS['independent_objective_columns'] = 513


def parent_payments(base):
    results = []
    half_families = {'ALL_SOURCE_JOINT_REWEIGHTED_TRUE_INTERNAL_SAFE',
                     'ORDERED_OUTER6_INNER5_COMPLETE_CELL_VERTEX'}
    only_families = {'TRUE_SOURCE2_MAXIMUM_C_CAP_COUPLED_INTERNAL_SAFE',
                     'SOURCE2_MAXIMUM_C_MINIMAL_CAP_TRUE_INTERNAL_SAFE'}
    for k, row in enumerate(base['raw_rows']):
        if 'source_IC_weight' not in row:
            continue
        i, fam = row['source'], row['family']
        fields = ('theta_by_true_source', 'theta_by_source', 'tau_by_true_source', 'tau_by_source')
        mapping = next((row[f] for f in fields if f in row), None)
        if mapping is None:
            list_field = 'theta3_theta4_theta5' if 'theta3_theta4_theta5' in row else 'tau3_tau4_tau5'
            mapping = {str(j): v for j, v in zip(range(3, 6), row[list_field])}
        assert set(mapping) == {str(j) for j in range(i+1, 6)}
        tau = tuple(Q(mapping[str(j)]) for j in range(i+1, 6))
        aa, s = Q(row['source_IC_weight']), Q(row['s'])
        assert aa == 25 + sum(tau, Q()) - s
        assert aa >= 0 and all(t >= 0 for t in tau)
        assert row['terminal_BR_average_weight'] == '1'
        vec = complete(row['a'])
        if fam in half_families:
            S = Q(7-i, 2)
            assert Q(row['K_weight']) == S == vec[512]
            if fam == 'ALL_SOURCE_JOINT_REWEIGHTED_TRUE_INTERNAL_SAFE':
                assert row['middle_cap_weight'] == '1/2' and row['terminal_cap_weight'] == '1'
        else:
            q0 = Q(1, 5) if fam == 'ORDERED_OUTER6_INNER5_TRUE_BRANCH_MINIMAL_CAP' else Q(1, 6)
            betas = canonical_caps(i, q0, tau)
            stored = row['middle_CAP_weights']
            stored_values = tuple(Q(stored[str(j)]) for j in range(i+1, 6)) if isinstance(stored, dict) else tuple(map(Q, stored))
            assert betas == stored_values
            assert row['terminal_CAP_weight'] == '1'
            S = 1 + sum(betas, Q())
            if fam in only_families:
                mu = Q(row['C_size_free_multiplier'])
                assert Q(row['true_tail_K_weight']) == S
                assert row['C_size_equality'] == '|C|-K=0'
                assert mu == S - s / 5 and vec[512] == S - mu == s / 5
                COUNTS['base_C_free_equality_checks'] += 1
            else:
                key = 'total_K_weight' if 'total_K_weight' in row else 'K_weight'
                assert Q(row[key]) == S == vec[512]
        if 'G_by_prefix_load' in row:
            assert row['outer_average_divisor'] == '6' and row['inner_average_divisor'] == '5'
            assert row['inner_excludes_same_index'] is True
            assert set(row['G_by_prefix_load']) == {str(p) for p in range(i)}
            for col, bits in enumerate(BITS):
                load = sum(bits[:6]); share = Q(bits[i-1], load) if load else Q()
                value = aa * share - bits[7] * Q(row['G_by_prefix_load'][str(sum(bits[:i-1]))])
                assert value == vec[col]
                COUNTS['base_ordered_customer_columns_rebuilt'] += 1
        results.append({'raw_index': k, 'name': row['name'], 'family': fam,
                        'source_IC_weight': str(aa), 'K_column': str(vec[512]),
                        'source_weight_and_K_check': 'PASS'})
    assert len(results) == 2006
    COUNTS['base_real_source_IC_and_K_metadata_checks'] = len(results)
    return results


def pure_query_index_identity():
    # This uses all 64 actual membership patterns. Exclusion is by index.
    for menu in itertools.product((0, 1), repeat=6):
        d = sum(menu); o = int(d > 0)
        assert sum((Q(b, 6) for b in menu), Q()) - Q(o, 6) == Q(d-o, 6) >= 0
        COUNTS['pure_six_index_weakening_identities'] += 1
        for k in range(6):
            value = sum((Q(menu[l], 5) for l in range(6) if l != k), Q())
            assert value == Q(d-menu[k], 5)
            COUNTS['ordered_actual_five_index_identities'] += 1


def get_original_metadata(row):
    # Explicit vector fields are kept in the immutable source file; all other
    # fields must be retained exactly by the schema adapter.
    return {k: v for k, v in row.items() if k not in ('a', 'raw_coefficients', 'coefficients_divided_by_25')}


def check_new_sources(base):
    packs, row_checks, budget_checks, equality_checks = [], [], [], []
    for package, count, manifest_sha, family_sha in EXPECTED:
        folder = WS / package
        if count == 1:
            data = read(folder / 'ROOT270_STRICT_C_OUTSIDE.json')
            rows = [data]
            b = Q(883952004100291, 8438786930961360)
            c0 = Q(37482242363557, 1875285984658080)
            eta = Q(1087978231314917, 84387869309613600)
            assert data['name'] == 'ROOT270_STRICT_C_OUTSIDE' and data['numerical_divisor'] == '1'
            assert Q(data['C_outside_remainder']) == eta
            expected = []
            for bits in BITS:
                load = sum(bits[:6]); share = Q(bits[0], load) if load else Q()
                expected.append(share - c0 * bits[7] - eta * bits[8] * (1-bits[7]))
            expected.append(-b)
            old = complete(base['raw_rows'][868]['a'])
            assert base['raw_rows'][868]['name'] == 'ROOT270_TRUE_BRANCH_P25'
            for k, bits in enumerate(BITS):
                assert expected[k] - old[k] == -eta * bits[8] * (1-bits[7])
            assert expected[512] == old[512]
            assert complete(data['a']) == expected
            packs.append((package, rows, None))
            row_checks.append({'package': package, 'source_row_index': 0, 'id': data['name'],
                'columns_checked': 513, 'unequal_columns': 0,
                'K_coefficient': str(expected[512]), 'formula': 'actual u1-bK-cO-eta*c*(1-o)',
                'rebuilt_vector_sha256': objhash(list(map(str, expected)))})
            COUNTS['new_legal_source_columns'] += 513
            COUNTS['root_old868_difference_columns'] = 513
            continue
        column_contract(folder)
        data = read(folder / 'exact_family.json'); rows = data['rows']; assert len(rows) == count
        catalog = read(folder / 'row_catalog.json') if (folder / 'row_catalog.json').exists() else None
        lookup = {}
        if package.startswith('source2_lambda'):
            domain = read(folder / 'parameter_domains.json')['families']
            assert set(domain) == {'six_mean', 'ordered_five'}
            vertices = {(fam, v['id']): v for fam, group in domain.items() for v in group['vertices']}
            assert len(vertices) == (46 if count == 230 else 32)
            assert catalog and [r['id'] for r in catalog] == [r['id'] for r in rows]
        elif package == 'later_sources_lambda_cells':
            cells = {c['id']: c for c in read(folder / 'parameter_domains.json')['cells']}
            vertices = {(cell['id'], v['id']): v for cell in cells.values() for v in cell['vertices']}
            assert len(cells) == 24 and len(vertices) == 110
        else:
            cases = {c['id']: c for c in read(folder / 'exact_envelopes.json')['cases']}
            assert set(cases) == {'pure_q6_s0', 'pure_q6_sstar', 'pure_q6_s9',
                                  'ordered_q5_s0', 'ordered_q5_sstar', 'ordered_q5_s9'}
        for number, row in enumerate(rows):
            mu = Q(); q0 = Q(); target = None
            if package.startswith('source2_lambda'):
                family = row['family']; ordered = family == 'ordered_five'; i = 2
                assert family in ('six_general', 'six_C_only', 'ordered_five')
                q0 = Q(1, 5 if ordered else 6)
                domain_name = 'ordered_five' if ordered else 'six_mean'
                vertex = vertices[(domain_name, row['vertex'])]
                params = list(map(Q, vertex['point'])); tau = tuple(params[:3]); lam = params[3]
                aa = lam + sum(tau, Q()); beta = canonical_caps(i, q0, tau); S = 1 + sum(beta, Q())
                target = row['target']
                if family == 'six_C_only':
                    assert target == 'C'; mu = sum(beta, Q())
                elif not ordered:
                    assert target in TARGETS
                cat = catalog[number]
                assert cat['q0'] == str(q0) and cat['parameters'] == vertex['point']
                assert cat['vertex'] == row['vertex'] and cat['target'] == target
                assert Q(cat['source_IC_weight']) == aa
                assert tuple(map(Q, cat['middle_caps'])) == beta
                assert Q(cat['K_coefficient']) == S - mu
                assert cat['uses_C_equality'] == (family == 'six_C_only')
                assert Q(cat.get('free_C_equality_multiplier', '0')) == mu
                actual = complete(row['raw_coefficients'])
                assert [x / 25 for x in actual] == complete(row['coefficients_divided_by_25'])
                key = (row['vertex'], family, target)
                lookup[key] = (actual, mu)
                pair = (row['vertex'], 'six_general', 'C') if family == 'six_C_only' else None
            elif package == 'later_sources_lambda_cells':
                assert row['raw_row_index'] == number
                i = row['source']; q0 = Q(row['q0']); family = row['kind']; ordered = family == 'ordered'
                assert i in (3, 4, 5) and family in ('six_general', 'six_C_only', 'ordered')
                assert q0 == Q(1, 5 if ordered else 6)
                vertex = vertices[(row['cell'], row['vertex_id'])]
                cell = cells[row['cell']]
                assert cell['source'] == i and cell['q0'] == str(q0)
                assert vertex['coordinates'] == row['coordinates']
                assert vertex['lambda_value'] == row['lambda_value']
                assert set(row['tau_by_true_source']) == {str(j) for j in range(i+1, 6)}
                tau = tuple(Q(row['tau_by_true_source'][str(j)]) for j in range(i+1, 6))
                lam = Q(row['lambda_value']); assert tuple(map(Q, row['coordinates'])) == tau + (lam,)
                aa = lam + sum(tau, Q()); beta = canonical_caps(i, q0, tau); S = 1 + sum(beta, Q())
                target = row['forced_target']
                if family == 'six_C_only':
                    assert target == 'C'; mu = sum(beta, Q())
                assert Q(row['source_IC_weight']) == aa
                assert {str(j): str(beta[j-i-1]) for j in range(i+1, 6)} == row['middle_CAP_weights']
                assert row['terminal_CAP_weight'] == row['terminal_query_average_weight'] == '1'
                assert Q(row['K_weight']) == S - mu
                assert Q(row['free_C_equality_multiplier']) == mu
                assert row['numeric_positive_divisor'] == '25'
                actual = complete(row['a'])
                assert catalog[number] == {k: v for k, v in row.items() if k != 'a'}
                key = (row['cell'], row['vertex_id'], family, target); lookup[key] = (actual, mu)
                pair = (row['cell'], row['vertex_id'], 'six_general', 'C') if family == 'six_C_only' else None
            else:
                assert row['source'] == 2 and row['sense'] == '>=' and row['rhs'] == '0'
                i = 2; case = cases[row['case']]; ordered = row['mode'] == 'ordered'
                assert row['mode'] == case['mode'] and row['mode'] in ('pure', 'ordered')
                q0 = Q(case['q0']); assert q0 == Q(1, 5 if ordered else 6)
                s = Q(case['s']); assert s in (Q(0), Q(61273, 6912), Q(9))
                delta = Q(row['delta']); assert 0 <= delta <= Q(5977, 6912)
                tau = (Q(0), Q(5977, 6912) - delta, Q(43, 48) + delta)
                aa = 25 + sum(tau, Q()) - s; beta = canonical_caps(i, q0, tau); S = 1 + sum(beta, Q())
                weights = row['weights']
                assert weights['tau'] == {str(j): str(tau[j-3]) for j in range(3, 6)}
                assert weights['beta'] == {str(j): str(beta[j-3]) for j in range(3, 6)}
                assert Q(weights['source_IC']) == aa and Q(weights['K_before_C_equality']) == S
                assert weights['last_cap'] == weights['last_query_mean'] == '1'
                target = row['target']; family = 'ordered' if ordered else 'six_C_only' if target == 'C-only' else 'six_general'
                if target == 'C-only':
                    target = 'C'; mu = S - s / 5
                    assert Q(row['C_equality_multiplier']) == mu
                else:
                    assert row['C_equality_multiplier'] is None
                assert row['numeric_divisor'] == '25'
                actual = complete(row['a'])
                key = (row['case'], row['delta'], family, target); lookup[key] = (actual, mu)
                pair = (row['case'], row['delta'], 'six_general', 'C') if family == 'six_C_only' else None
            expected = direct_vector(i, target, ordered, aa, tau, beta, mu)
            assert actual == expected, (package, number, row['id'])
            if pair is not None:
                # Pure C is emitted immediately before its C-only partner.
                assert pair in lookup, (package, pair)
                original = lookup[pair][0]
                difference = [expected[k] - original[k] for k in range(513)]
                assert difference == [mu * b[8] for b in BITS] + [-mu]
                equality_checks.append({'package': package, 'id': row['id'],
                                        'signed_multiplier': str(mu), 'checked_columns': 513,
                                        'identity': 'C_only - general_C = mu*(c,-1)', 'status': 'PASS'})
                COUNTS['new_C_free_equality_columns'] += 513
            row_checks.append({'package': package, 'source_row_index': number, 'id': row['id'],
                'columns_checked': 513, 'unequal_columns': 0,
                'source_IC_weight': str(aa), 'K_coefficient': str(expected[512]),
                'free_C_equality_multiplier': str(mu),
                'rebuilt_vector_sha256': objhash(list(map(str, expected)))})
            budget_checks.append({'package': package, 'source_row_index': number,
                'id': row['id'], 'source': i, 'q0': str(q0),
                'tau_by_true_source': {str(j): str(tau[j-i-1]) for j in range(i+1, 6)},
                'source_IC_weight': str(aa), 'middle_caps': list(map(str, beta)),
                'terminal_cap_and_query_weights': ['1', '1'], 'K_before_C_equality': str(S),
                'signed_C_equality_multiplier': str(mu), 'final_K_column': str(S-mu),
                'status': 'PASS_FROM_TRUE_BUDGETS'})
            COUNTS['new_legal_source_columns'] += 513
        packs.append((package, rows, catalog))
    assert COUNTS['new_legal_source_columns'] == 1121 * 513
    return packs, row_checks, budget_checks, equality_checks


def check_assembled(base, base_scaling, base_catalog, packs):
    output = read(HERE / 'exact_input.json')
    scale = read(HERE / 'numerical_scaling.json')
    catalog = read(HERE / 'row_catalog.json')
    prov = read(HERE / 'provenance.json')
    rows = output['raw_rows']
    assert len(rows) == output['raw_inequality_count'] == 4177
    assert len(catalog) == len(prov['rows']) == 4177
    for key in ['variables', 'bit_order', 'atom_columns', 'K_column', 'nonnegative_columns',
                'objective', 'equalities', 'equality_count', 'inequality_convention']:
        assert output[key] == base[key], key
    assert output['parent_metadata'] == {k: v for k, v in base.items() if k != 'raw_rows'}
    assert output['parent_input_sha256'] == BASE_SHA and output['parent_manifest_sha256'] == BASE_MANIFEST
    assert output['source_pins_sha256'] == digest(HERE / 'source_pins.json')
    assert output['model_contract_sha256'] == digest(HERE / 'model_contract.json')
    assert output['source_admission_sha256'] == digest(HERE / 'source_admission.json')
    assert rows[:3056] == base['raw_rows']
    assert catalog[:3056] == base_catalog
    assert scale['raw_order'][:3056] == base_scaling['raw_order']
    assert list(scale['raw_scales'])[:3056] == list(base_scaling['raw_scales'])
    for name, val in base_scaling['raw_scales'].items():
        assert scale['raw_scales'][name] == val
    block_checks = []
    for name, first, last in BASE_BLOCKS:
        assert rows[first:last+1] == base['raw_rows'][first:last+1]
        block_checks.append({'block': name, 'first': first, 'last': last, 'rows': last-first+1,
                             'whole_objects_literal': True, 'old_scales_literal': True,
                             'all_columns': (last-first+1)*513, 'status': 'PASS'})
    index = 3056
    for package, originals, source_catalog in packs:
        first = index
        for source_index, original in enumerate(originals):
            row, cat, pr = rows[index], catalog[index], prov['rows'][index]
            root = package == 'main_root270_strict_outside'
            oid = original.get('id', original.get('name'))
            name = original['name'] if root else package + '::' + oid
            assert row['name'] == name
            if root:
                assert row == original
                numerical = '1'
            else:
                numerical = '25'
                if package.startswith('source2_lambda'):
                    a = {str(k): x for k, x in enumerate(original['raw_coefficients'])}
                    fam = original['family']
                elif package == 'source2_conditional_redistribution':
                    a = {str(k): x for k, x in enumerate(original['a'])}
                    fam = 'SOURCE2_CONDITIONAL_REDISTRIBUTION_' + original['mode'].upper()
                else:
                    a = original['a']; fam = original['kind']
                assert row['a'] == a and row['rhs'] == original.get('rhs', '0')
                assert row['family'] == fam and row['id'] == oid
                assert row['numerical_divisor'] == numerical
                assert row['source_row_metadata'] == get_original_metadata(original)
                assert row['source_row_id'] == oid and row['source_row_index'] == source_index
                assert row['source_row_object_sha256'] == objhash(original)
            assert cat['raw_index'] == index and cat['name'] == name
            assert cat['source_row_metadata'] == get_original_metadata(original)
            if source_catalog is not None:
                assert cat['original_source_catalog_entry'] == source_catalog[source_index]
            assert cat['source_row_object_sha256'] == objhash(original)
            assert cat['source_row_id'] == oid and cat['source_row_index'] == source_index
            assert pr['package'] == package and pr['source_row_index'] == source_index
            assert pr['source_row_id'] == oid and pr['source_row_metadata'] == get_original_metadata(original)
            assert pr['source_row_object_sha256'] == objhash(original)
            assert pr['row_object_sha256'] == objhash(row)
            assert scale['raw_order'][index] == name and scale['raw_scales'][name] == numerical
            index += 1
        block_checks.append({'block': package, 'first': first, 'last': index-1,
                             'rows': len(originals), 'all_columns': len(originals)*513,
                             'all_source_occurrences_and_metadata_preserved': True, 'status': 'PASS'})
    assert index == 4177 and len(set(scale['raw_order'])) == 4177
    assert scale['raw_order'] == [r['name'] for r in rows]
    assert list(scale['raw_scales']) == scale['raw_order']
    assert scale['exact_coefficients_numerically_divided'] is False
    assert Counter(r['rhs'] for r in rows) == {'0': 4147, '-1': 30}
    complete_rows, signature_counts, zero_rows = [], Counter(), []
    for k, row in enumerate(rows):
        vector = complete(row['a'])
        normal = list(map(str, vector)) + [str(Q(row['rhs']))]
        vector_sha = objhash(normal); signature_counts[vector_sha] += 1
        if not any(vector) and Q(row['rhs']) == 0:
            zero_rows.append(k)
        assert Q(scale['raw_scales'][row['name']]) > 0
        assert prov['rows'][k]['raw_index'] == k and prov['rows'][k]['name'] == row['name']
        assert prov['rows'][k]['row_object_sha256'] == objhash(row)
        if k < 3056:
            assert prov['rows'][k]['source_row_metadata'] == get_original_metadata(base['raw_rows'][k])
        complete_rows.append({'raw_index': k, 'name': row['name'], 'all_columns_checked': 513,
                              'raw_affine_vector_sha256': vector_sha,
                              'row_object_sha256': objhash(row), 'status': 'PASS'})
    COUNTS['all_complete_system_column_positions_checked'] = 4177*513
    COUNTS['base_literal_complete_column_positions'] = 3056*513
    diagnostics = {'diagnostic_only_no_filtering': True, 'raw_rows': len(rows),
                   'zero_raw_row_indices': zero_rows,
                   'distinct_affine_vectors_including_zero': len(signature_counts),
                   'duplicate_occurrences_retained': sum(n-1 for n in signature_counts.values()),
                   'rhs_minus_one_rows': [k for k, r in enumerate(rows) if r['rhs'] == '-1'],
                   'all512_atoms_and_independent_K_kept': True}
    save('all_raw_row_checks.json', complete_rows)
    save('block_literal_checks.json', block_checks)
    save('raw_identity_diagnostics.json', diagnostics)
    return digest(HERE / 'exact_input.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assembled', action='store_true')
    args = parser.parse_args()
    assert not (HERE / 'freeze_manifest.json').exists(), 'Frozen package is read-only; use a replay copy'
    audit_pins()
    base = read(WS / 'visible_maximum_joint_v5/exact_input.json')
    scale = read(WS / 'visible_maximum_joint_v5/numerical_scaling.json')
    catalog = read(WS / 'visible_maximum_joint_v5/row_catalog.json')
    column_contract(WS / 'visible_maximum_joint_v5', base=True)
    parent_contract(base, scale, catalog)
    base_payments = parent_payments(base)
    pure_query_index_identity()
    packs, row_checks, budget_checks, equality_checks = check_new_sources(base)
    matrix_sha = check_assembled(base, scale, catalog, packs) if args.assembled else None
    audit_pins()
    save('base_real_source_weight_checks.json', base_payments)
    save('new_source_column_checks.json', row_checks)
    save('new_source_budget_checks.json', budget_checks)
    save('new_C_signed_equality_checks.json', equality_checks)
    save('independent_true_cost_minima.json', list(MINIMUM_TABLES.values()))
    result = {'status': 'PASS_INDEPENDENT_COMPLETE_ASSEMBLED_INPUT' if args.assembled else 'PASS_INDEPENDENT_FROZEN_SOURCES_ONLY',
        'actual_agent_id': '/root/visible_joint_v6_prepare',
        'independence': 'stdlib-only; no builder or project-module imports; direct actual shares and complete genuine tails',
        'counts': dict(COUNTS), 'input_sha256': matrix_sha,
        'expected_raw_rows': 4177, 'new_raw_rows': 1121, 'base_raw_rows': 3056,
        'old_two_equalities_and_objective_independently_rebuilt': True,
        'old_early1050_scope': 'whole-object literal preservation; no invented uniform source-weight metadata',
        'all_old_positive_scale_strings_preserved': True,
        'all_new_real_source_IC_weights_checked_independently': True,
        'all_new_K_columns_and_C_signed_equalities_checked_independently': True,
        'optimizer_calls': 0, 'candidate_or_face_reads': 0,
        'LP_release_created_or_consumed': False, 'failures': []}
    save('independent_check_result.json' if args.assembled else 'source_only_check_result.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        if not (HERE / 'freeze_manifest.json').exists():
            path = HERE / 'failure_log.json'
            log = read(path) if path.exists() else {'events': []}
            log['events'].append({'program': 'check_independent.py', 'error_type': type(error).__name__,
                                  'message': str(error), 'resolved': False})
            save('failure_log.json', log)
        raise
