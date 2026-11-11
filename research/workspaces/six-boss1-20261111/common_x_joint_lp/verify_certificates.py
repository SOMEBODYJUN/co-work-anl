"""Independent standard-library audit of all 23625 rows and 21021 columns.

Does not import assembly, recovery, any row generator, numpy, or an optimizer.
Rebuilds H3/AP from literal queries and own facets from eight-cell elimination.
The 420 real overlaps are checked as core values, never as canonical minima.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
OLDM, ROWS, COLS = 22297, 23625, 21021
BASE = WORK / 'maxb_augmented_lp/full_lift'
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'maxb_h3_bridge/rows_17.json': '3c9d360cbb0313ae84b4be7add4f4b3f6b67ba57f71cb8f366a2341e8f128d8d',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
    'common_x_own_lift/own_facets.json': '711e0d2b1499784f26fce26d8cc7a7a985c618df52a125f91af61a168bfc70ba'}


def sha(p): return sha256(p.read_bytes()).hexdigest()


def read(p):
    with gzip.open(p, 'rt', encoding='utf-8') if p.suffix == '.gz' else p.open() as f:
        return json.load(f)


@lru_cache(maxsize=None)
def rat(v): return F(v)


def frozen(v): return tuple(map(frozen, v)) if isinstance(v, list) else v


def dot(row, x): return sum((rat(a) * x[j] for j, a in row if x[j]), F())


def sparse(row): return {j: rat(v) for j, v in row}


def combine(*terms):
    out = defaultdict(F)
    for factor, row in terms:
        for j, v in row.items(): out[j] += factor * v
    return {j: v for j, v in out.items() if v}


def enc(row): return [[j, str(v)] for j, v in sorted(row.items()) if v]


def descriptors(old):
    """Recover R/Z ownership from old upper rows, not legacy hist_column_old."""
    hist = {j: c for j, c in enumerate(old['columns'][:4849]) if c['kind'] == 'hist'}
    own = {}; covered = set(); legacy = {}
    for i, name in enumerate(old['row_names']):
        if not name.startswith('joint-state-upper:'): continue
        row = sparse(old['rows'][i])
        hp = [j for j, a in row.items() if a == 1 and j in hist]
        states = [j for j, a in row.items() if a == -1 and old['columns'][j]['kind'] == 'joint-reply']
        assert len(hp) == 1 and len(states) == 3 and len(row) == 4
        h = hp[0]; groups = {frozen(old['columns'][j]['group']) for j in states}; assert len(groups) == 1
        g = next(iter(groups)); atom = {}
        for j in states:
            c = old['columns'][j]; key = ''.join(map(str, c['state']))
            assert key not in atom and key in ('10', '01', '11')
            atom[key] = {j: F(1)}; covered.add(j)
            previous = legacy.setdefault(c['hist_column_old'], h); assert previous == h
        assert set(atom) == {'10', '01', '11'}
        atom['00'] = row; own[h, g] = (atom, i)
    assert len(own) == 194 and len(covered) == 582
    b4 = defaultdict(dict)
    for j, c in enumerate(old['columns'][:4849]):
        if c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            h = c['hist_column']; key = tuple(c['hidden']) + (c['ell'] // 6,)
            assert c['ell'] in (0, 6) and len(key) == 3 and key not in b4[h]
            b4[h][key] = j
    assert len(b4) == 16 and all(len(states) == 8 for states in b4.values())
    xc = {}; yc = {}; margins = {}
    for j, c in enumerate(old['columns'][20585:], 20585):
        h = c['hist_column']; assert h in hist
        if j < 20601:
            assert c['kind'] == 'common-X-mass' and h not in xc; xc[h] = j
        else:
            assert c['kind'] == 'X-query-overlap-upper'
            token = frozen(c['query_token']); assert (h, token) not in yc
            if token[0] == 'H': q = {k: F(1) for state, k in b4[h].items() if state[token[1]]}
            else:
                atoms = own[h, token[1]][0]
                q = combine((1, atoms['10' if token[0] == 'R' else '01']), (1, atoms['11']))
            assert enc(q) == c['query_marginal']; yc[h, token] = j; margins[h, token] = q
    assert set(xc) == set(hist) and len(yc) == 420
    return hist, own, b4, xc, yc, margins, legacy


def literal_queries():
    actions = [('A', k) for k in range(6)] + [(k, i) for k in ('T', 'B', 'C') for i in range(6)]
    for kind in ('R', 'Z'):
        actions.extend((kind, f, i, j) for f in range(2) for i in range(6) for j in range(6) if f or i != j)
    actions += [('H', 0), ('H', 1)]
    orbits = defaultdict(list)
    for q in actions:
        key = q if q[0] in ('A', 'H') else (q[0],) if q[0] in ('T', 'B', 'C') else (q[0], q[1], q[2] == q[3])
        orbits[key].append(q)
    assert len(actions) == 158 and len(orbits) == 17
    return {frozenset(v) for v in orbits.values()}


def bridge_row(player, constant, queries, hist, xc, yc, margins):
    row = defaultdict(F); r = 7 - player; weight = F(1, len(queries))
    for h, c in hist.items():
        bits = tuple(map(int, c['actual_bits'])); b = sum(bits[:player-1]); n = sum(bits)
        if bits[player-1]: row[h] += constant / n
        row[xc[h]] -= (constant - 1) / (b + r)
        words = [w for w, count in zip(product((0, 1), repeat=3), c['hist']) for _ in range(count)]
        assert len(words) == 6
        for q in queries:
            if q[0] == 'A': token = ('bit', bits[q[1]])
            elif q[0] in ('T', 'B', 'C'): token = ('bit', words[q[1]][('T', 'B', 'C').index(q[0])])
            elif q[0] == 'H': token = q
            else:
                kind, f, i, j = q; token = (kind, (f, int(i == j), words[i], words[j]))
            if token[0] == 'bit':
                qmass = {h: F(token[1])}; overlap = {xc[h]: F(token[1])}
            else:
                qmass = margins[h, token]; overlap = {yc[h, token]: F(1)}
            for j, a in qmass.items(): row[j] -= weight * a / (b + 1)
            for j, a in overlap.items(): row[j] += weight * (r - 1) * a / ((b + 1) * (b + r))
    return enc(row)


def reconstruct_own(old, hist, own, b4, xc, yc):
    results = []; comparisons = ((0, 3), (1, 2), (2, 1), (1, 3), (2, 3), (3, 0))
    inv = {j: (h, token) for (h, token), j in yc.items()}
    for block, jq in enumerate(range(20601, COLS, 2)):
        jr = jq + 1; h, tq = inv[jq]; hr, tr = inv[jr]; assert h == hr
        if tq[0] == 'R':
            assert tr == ('Z', tq[1]); masses, m00_row = own[h, tq[1]]
            key = ['own-RZ', h, old['columns'][jq]['query_token'][1]]; mass_eq = []
            assert combine(*[(1, x) for x in masses.values()]) == {h: F(1)}
        else:
            assert tq == ('H', 0) and tr == ('H', 1)
            masses = {''.join(map(str, (a, b))): {j: F(1) for s, j in b4[h].items() if s[:2] == (a, b)}
                      for a, b in product((0, 1), repeat=2)}
            key = ['B4-H1H2', h]; m00_row = None
            delta = combine(*[(1, x) for x in masses.values()], (-1, {h: F(1)}))
            k = list(hist).index(h); i = 5462 + 2 * k
            assert enc(delta) == old['rows'][i] and enc(combine((-1, delta))) == old['rows'][i+1]
            assert old['row_names'][i] == 'actualB-4-marginal:' + str(k)
            mass_eq = [i, i + 1]
        q = {jq: F(1)}; r = {jr: F(1)}; x = {xc[h]: F(1)}
        lows = [{}, combine((1, q), (-1, masses['10'])), combine((1, r), (-1, masses['01'])), combine((1, q), (1, r), (-1, x))]
        ups = [masses['11'], q, r, combine((1, masses['00']), (-1, x), (1, q), (1, r))]
        facets = [enc(combine((1, ups[u]), (-1, lows[l]))) for l, u in comparisons]
        margins = [combine((1, masses[s]), (1, masses['11'])) for s in ('10', '01')]
        upper_indices = []
        for j, marginal in zip((jq, jr), margins):
            i = 20926 + 2 * (j - 20601)
            assert old['rows'][i] == enc(combine((1, x), (-1, {j: F(1)})))
            assert old['rows'][i+1] == enc(combine((1, marginal), (-1, {j: F(1)})))
            upper_indices.extend((i, i+1))
        inherited = {(0, 0): masses['11'], (0, 1): q, (0, 2): r,
            (1, 0): combine((1, margins[0]), (-1, q)), (1, 1): masses['10'],
            (2, 0): combine((1, margins[1]), (-1, r)), (2, 2): masses['01'],
            (3, 1): combine((1, x), (-1, r)), (3, 2): combine((1, x), (-1, q)), (3, 3): masses['00']}
        assert len(inherited) == 10 and all(combine((1, ups[u]), (-1, lows[l])) == val for (l, u), val in inherited.items())
        results.append({'block': block, 'key': key, 'H_column': h, 'X_column': xc[h], 'yQ_column': jq,
            'yR_column': jr, 'mass_by_QR': {s: enc(masses[s]) for s in ('00', '10', '01', '11')},
            'old_upper_rows': upper_indices, 'mass_equality_rows': mass_eq, 'facets': facets})
    assert len(results) == 210 and sum(bool(b['mass_equality_rows']) for b in results) == 16
    return results


def auxiliary_audit(matrix, structure):
    maxima = dict(structure['max_thresholds']); minima = {r['column']: r for r in structure['min_auxiliaries']}
    assert set(maxima) == set(range(4849, 12803)) and set(minima) == set(range(12803, 15593))
    signs = defaultdict(lambda: [[], []]); ysigns = defaultdict(lambda: [[], []])
    for i, row in enumerate(matrix['rows']):
        for j, a in row:
            v = rat(a)
            if 4849 <= j < 15593: signs[j][int(v < 0)].append((i, v))
            if j >= 20601: ysigns[j][int(v < 0)].append((i, v))
    main_max_occ = main_min_occ = 0
    for j, i in maxima.items():
        assert signs[j][0] == [(i, F(1))] and signs[j][1]
        assert all(k < 4849 or k == j for k, a in matrix['rows'][i])
        assert all(k < OLDM and a < 0 for k, a in signs[j][1]); main_max_occ += len(signs[j][1])
    for j, r in minima.items():
        expected = [(r['q_upper_row'], F(-1)), (r['v_upper_row'], F(-1))]
        assert signs[j][1] == expected and signs[j][0]
        for i, _ in expected:
            assert all(k == j or (k < 4849 and rat(a) > 0) for k, a in matrix['rows'][i])
        assert all(k < OLDM and a > 0 for k, a in signs[j][0]); main_min_occ += len(signs[j][0])
    for j in range(4849, 15593): assert rat(matrix['objective'][j]) == rat(matrix['normalization'][j]) == 0
    for j in range(20601, COLS):
        assert ysigns[j][0] and ysigns[j][1]
        assert any(i >= 22365 for i, a in ysigns[j][1]), ('missing_own_negative_y', j)
        assert matrix['columns'][j]['semantic_upgrade']['canonical_min_permitted'] is False
    assert all(not (4849 <= j < 15593) for row in matrix['rows'][OLDM:] for j, a in row)
    return {'canonical_max': len(maxima), 'canonical_min': len(minima), 'total': len(maxima) + len(minima),
        'max_main_negative_occurrences': main_max_occ, 'min_main_positive_occurrences': main_min_occ,
        'promoted_real_y_with_new_negative_own_occurrences': 420, 'new_rows_old_auxiliary_occurrences': 0}


def check_dual(matrix, certificate):
    lower = F(certificate['normalization_multiplier'])
    residual = [rat(c) - lower * rat(b) for c, b in zip(matrix['objective'], matrix['normalization'])]
    seen = set()
    for i, text in certificate['row_multipliers']:
        assert type(i) is int and 0 <= i < ROWS and i not in seen; seen.add(i)
        multiplier = F(text); assert multiplier > 0
        for j, a in matrix['rows'][i]: residual[j] -= multiplier * rat(a)
    assert len(residual) == COLS and min(residual) >= 0 and residual == list(map(F, certificate['residuals']))
    assert certificate['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    return lower, residual


def canonical_old(matrix, x, structure):
    checked = set()
    for j, i in structure['max_thresholds']:
        assert x[j] == max(F(), -dot([(k, a) for k, a in matrix['rows'][i] if k < 4849], x)); checked.add(j)
    for r in structure['min_auxiliaries']:
        j = r['column']; assert j not in checked
        assert x[j] == min(dot([(k, a) for k, a in matrix['rows'][i] if k < 4849], x) for i in (r['q_upper_row'], r['v_upper_row']))
        checked.add(j)
    assert checked == set(range(4849, 15593)) and not checked.intersection(range(20601, COLS))
    return len(checked)


def eight_cells(x, blocks):
    witnesses = []
    for b in blocks:
        mass = {s: dot(a, x) for s, a in b['mass_by_QR'].items()}
        H, X, q, r = [x[b[k]] for k in ('H_column', 'X_column', 'yQ_column', 'yR_column')]
        assert min(mass.values()) >= 0 and sum(mass.values()) == H
        assert 0 <= X <= H and 0 <= q <= min(X, mass['10'] + mass['11']) and 0 <= r <= min(X, mass['01'] + mass['11'])
        lows = [F(), q - mass['10'], r - mass['01'], q + r - X]
        ups = [mass['11'], q, r, mass['00'] - X + q + r]
        beta = max(lows); assert all(beta <= u for u in ups)
        inside = {'00': X - q - r + beta, '10': q - beta, '01': r - beta, '11': beta}
        outside = {s: mass[s] - inside[s] for s in inside}
        assert min(inside.values()) >= 0 and min(outside.values()) >= 0 and sum(inside.values()) == X
        assert inside['10'] + inside['11'] == q and inside['01'] + inside['11'] == r
        assert sum(outside.values()) == H - X
        witnesses.append({'block': b['block'], 'key': b['key'], 'L': str(beta), 'U': str(min(ups)), 'beta': str(beta),
            'lower_candidates': list(map(str, lows)), 'upper_candidates': list(map(str, ups)),
            'X1_by_QR': {s: str(v) for s, v in inside.items()}, 'X0_by_QR': {s: str(v) for s, v in outside.items()},
            'all_four_upper_bounds_checked': True, 'all_eight_cells_nonnegative': True})
    return witnesses


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--structure-only', action='store_true')
    parser.add_argument('--output', default=str(HERE)); args = parser.parse_args()
    out = Path(args.output).resolve(); assert out == HERE or out.is_relative_to(HERE)
    started = time.monotonic()
    for name, pin in PINS.items(): assert sha(WORK / name) == pin, name
    manifest = read(HERE / 'inputs_manifest.json')
    for record in manifest['source_files']: assert sha(REPO / record['path']) == record['sha256'], record['path']
    for name, pin in manifest['generated_inputs'].items(): assert sha(HERE / name) == pin, name
    old = read(BASE / 'exact_matrix.json.gz'); matrix = read(HERE / 'exact_matrix.json.gz')
    structure = read(HERE / 'coordinate_structure.json')
    assert len(matrix['rows']) == len(matrix['row_names']) == ROWS
    assert len(matrix['columns']) == len(matrix['objective']) == len(matrix['normalization']) == COLS
    assert sum(map(len, matrix['rows'])) == 3308634
    assert matrix['rows'][:OLDM] == old['rows'] and matrix['row_names'][:OLDM] == old['row_names']
    assert matrix['objective'] == old['objective'] and matrix['normalization'] == old['normalization']
    assert matrix['columns'][:20601] == old['columns'][:20601]
    for j in range(20601, COLS):
        c = matrix['columns'][j]; assert {k: v for k, v in c.items() if k != 'semantic_upgrade'} == old['columns'][j]
        assert c['semantic_upgrade'] == structure['semantic_upgrade']
        assert c['semantic_upgrade']['effective_kind'] == 'real-common-X-query-overlap'
        assert c['semantic_upgrade']['recovery_role'] == 'core'
    core = list(range(4849)) + list(range(15593, COLS))
    assert structure['core_columns'] == core and len(core) == matrix['core_columns'] == 10277
    assert structure['auxiliary_columns'] == list(range(4849, 15593))
    assert structure['forbidden_canonical_min_columns'] == structure['real_overlap_columns'] == list(range(20601, COLS))
    assert set(core).isdisjoint(structure['auxiliary_columns']) and sorted(core + structure['auxiliary_columns']) == list(range(COLS))
    for i, row in enumerate(matrix['rows']):
        assert [j for j, v in row] == sorted({j for j, v in row})
        assert all(type(j) is int and 0 <= j < COLS and rat(a) for j, a in row), i
    hist, own, b4, xc, yc, margins, legacy = descriptors(old)
    assert len(hist) == 16 and structure['X_mass_columns'] == list(xc.values())
    assert structure['shared624_columns'] == list(range(15593, 20585))
    assert all(c['kind'] == 'actual4-R-shared624-conditional-mass' for c in matrix['columns'][15593:20585])
    for i in structure['shared624_equality_positive_rows']:
        assert matrix['rows'][i+1] == [[j, str(-rat(a))] for j, a in matrix['rows'][i]]
    orbits = literal_queries(); checks = []
    for source, start, path in [('H3', 22297, 'maxb_h3_bridge/rows_17.json'), ('early_AP', 22314, 'early_x_anchor_queries/rows_51.json')]:
        package = read(WORK / path); queries_by_player = defaultdict(list)
        for k, record in enumerate(package['rows']):
            player = 4 if source == 'H3' else record['actual_player']
            constant = {1: F(43), 2: F(65, 2), 3: F(23), 4: F(10)}[player]
            queries = [tuple(q) for q in record['query_members']]
            assert len(set(queries)) == record['orbit_size'] == len(queries)
            queries_by_player[player].append(frozenset(queries))
            expected = bridge_row(player, constant, queries, hist, xc, yc, margins)
            assert expected == record['row'] == matrix['rows'][start + k]
            assert matrix['row_names'][start+k] == json.dumps(record['name'], separators=(',', ':'))
        for player, groups in queries_by_player.items(): assert len(groups) == 17 and set(groups) == orbits
        checks.append({'source': source, 'rows': len(package['rows']), 'nonzeros': sum(len(r['row']) for r in package['rows'])})
    atoms = read(WORK / 'maxb_h3_bridge/atom_audit.json')
    assert len(atoms['records']) == 128
    for atom in atoms['records']:
        b, a, x, y, z, q = [atom[k] for k in ('b', 'a', 'x', 'y', 'z', 'q')]
        n = b + 1
        E = F(10*x, n+y+z) - F(9*x, n+2) - q*(F(x, n+2)+F(1-x, n)) - F(x-y, n+a) - F(2*(x-z), n+a) - F(z-q, n+x+y)
        assert E == F(atom['remainder']) == F(atom['closed_form_remainder']) and E >= 0
    reconstructed = reconstruct_own(old, hist, own, b4, xc, yc)
    package = read(WORK / 'common_x_own_lift/own_facets.json'); saved = read(HERE / 'own_blocks.json')
    for b, source, frozen_block in zip(reconstructed, package['blocks'], saved['blocks']):
        for key in ('block', 'key', 'H_column', 'X_column', 'yQ_column', 'yR_column', 'mass_by_QR', 'old_upper_rows'):
            assert b[key] == source[key] == frozen_block[key], (b['block'], key)
        assert frozen_block['joint_matrix_rows'] == list(range(22365 + 6*b['block'], 22371 + 6*b['block']))
        for facet, expected in enumerate(b['facets']):
            local = 6*b['block'] + facet; record = package['rows'][local]; i = 22365 + local
            assert expected == record['row'] == matrix['rows'][i] and record['name'] == matrix['row_names'][i]
            assert b['mass_equality_rows'] == record['mass_equality_rows']
    audit_aux = auxiliary_audit(matrix, structure)
    oldpoint = read(BASE / 'recovery/augmented_lp_exact.json'); xold = [F(c['weight']) for c in oldpoint['columns']]
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in oldpoint['columns']] == old['columns']
    assert len(xold) == COLS and min(xold) >= 0 and dot(list(enumerate(matrix['normalization'])), xold) == 1
    oldslacks = [dot(row, xold) for row in old['rows']]; assert min(oldslacks) >= 0
    oldW = dot(list(enumerate(matrix['objective'])), xold); assert oldW == F(oldpoint['W'])
    inherited = read(HERE / 'inherited_dual_lower_bound.json'); source_dual = read(BASE / 'recovery/exact_dual_certificate.json')
    lower, residual = check_dual(matrix, inherited)
    assert lower == oldW and inherited['row_multipliers'] == source_dual['row_multipliers']
    assert inherited['residuals'] == source_dual['residuals'] and inherited['zero_extended_row_range_half_open'] == [OLDM, ROWS]
    assert all(i < OLDM for i, value in inherited['row_multipliers'])
    assert all(F(value)*oldslacks[i] == 0 for i, value in inherited['row_multipliers'])
    assert all(r*x == 0 for r, x in zip(residual, xold)); assert canonical_old(matrix, xold, structure) == 10744
    zero_hist = [h for h in hist if not xold[h]]; assert zero_hist == [1, 59, 366, 449, 524, 574]
    newslacks = [dot(row, xold) for row in matrix['rows'][OLDM:]]
    diagnostics = {'point_sha256': PINS['maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json'],
        'scope': 'Only this fixed x,y,m point is evaluated. Negative fixed canonical y is not impossibility after reselection.',
        'new_row_slacks': list(map(str, newslacks)), 'negative_rows': [{'global_row': OLDM+k, 'name': matrix['row_names'][OLDM+k],
        'slack': str(v), 'slack_float': float(v)} for k, v in enumerate(newslacks) if v < 0]}
    summary = {'status': 'PASS', 'rows': ROWS, 'columns': COLS, 'nonzeros': 3308634,
        'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'), 'verifier_sha256': sha(Path(__file__)),
        'old_rows_unchanged': OLDM, 'unchanged_column_descriptors': 20601, 'explicitly_upgraded_real_y_descriptors': 420,
        'objective_and_normalization_unchanged': True, 'core_columns': 10277, 'auxiliary_columns': 10744,
        'bridge_rows_independently_rebuilt': checks, 'own_rows_independently_eliminated': 1260,
        'own_nonzeros_checked': 5718, 'own_blocks': 210, 'B4_mass_equalities_checked': 16,
        'all_420_marginals_rebuilt_from_raw_old_descriptors': True, 'legacy_hist_indices_not_used_as_full_indices': True,
        'legacy_to_full_hist_mapping': sorted(legacy.items()), 'all_16_hist_retained': True, 'six_old_zero_hist_retained': zero_hist,
        'shared624_hidden_columns_retained': 4992, 'shared624_equality_pairs_retained': 312,
        'auxiliary_sign_audit': audit_aux, 'old_primal_rows_reverified': OLDM,
        'inherited_dual_columns_checked': COLS, 'inherited_dual_rows_zero_extended': 1328,
        'inherited_lower_bound': str(lower), 'inherited_lower_float': float(lower),
        'fixed_old_point_negative_added_rows': len(diagnostics['negative_rows']), 'whole_W10_optimum_face_excluded': False,
        'optimizer_calls': 0, 'constructor_imported': False, 'recovery_imported': False,
        'scope': 'Fixed16-hist finite necessary LP and local own eight-cells. No full-catalog common law, full SPE, half theorem, or counterexample.'}
    if not args.structure_only:
        point = read(out / 'augmented_lp_exact.json'); x = [F(c['weight']) for c in point['columns']]
        assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == matrix['columns']
        assert len(x) == COLS and min(x) >= 0 and dot(list(enumerate(matrix['normalization'])), x) == 1
        W = dot(list(enumerate(matrix['objective'])), x); assert W == F(point['W']) and W >= lower
        slacks = [dot(row, x) for row in matrix['rows']]; assert min(slacks) >= 0
        assert canonical_old(matrix, x, structure) == 10744
        dual = read(out / 'exact_dual_certificate.json'); matched, rd = check_dual(matrix, dual); assert matched == W
        assert all(F(v)*slacks[i] == 0 for i, v in dual['row_multipliers']) and all(a*b == 0 for a, b in zip(rd, x))
        witnesses = eight_cells(x, reconstructed)
        audit = read(out / 'primal_exact_audit.json'); assert list(map(F, audit['row_slacks'])) == slacks and F(audit['W']) == W
        recovery = audit['recovery']; selected = read(out / ('primal_' + recovery['attempt'] + '_recovery_inputs.json'))
        support = selected['support']; assert support == recovery['support'] and set(support).issubset(core)
        assert selected['forbidden_canonical_min_columns'] == list(range(20601, COLS))
        local = [x[j] for j in support]; n = len(support)
        raw_core = recovery['core_solution_before_auxiliary_completion']
        assert [j for j, value in raw_core] == core
        assert all(F(value) == x[j] for j, value in raw_core)
        for equation in selected['selected_equations']:
            assert sum((F(v)*local[j] for j, v in equation if j < n), F()) == sum((F(v) for j, v in equation if j == n), F())
        for j in range(20601, COLS):
            assert x[j] == (local[support.index(j)] if j in support else 0)
        summary.update(status='EXACT_OPTIMUM_VERIFIED', W=str(W), W_float=float(W), exact_increase=str(W-lower),
            strict_half_gap=str(1-2*W), all_primal_rows_checked=ROWS, all_dual_columns_checked=COLS,
            canonical_checks=10744, real_y_preserved_from_core_recovery=420, own_eight_cell_witnesses=210,
            all_own_four_upper_bounds_checked=840, minimum_primal_slack=str(min(slacks)),
            primal_sha256=sha(out/'augmented_lp_exact.json'), dual_sha256=sha(out/'exact_dual_certificate.json'))
        dest = out/'own_eight_cell_witnesses.json'; assert not dest.exists()
        dest.write_text(json.dumps({'scope': 'Local own completions only; no full common law.', 'blocks': witnesses}, ensure_ascii=False, indent=2)+'\n')
    else:
        dest = HERE/'old_point_diagnostic.json'; assert not dest.exists()
        dest.write_text(json.dumps(diagnostics, ensure_ascii=False, indent=2)+'\n')
    summary['seconds'] = time.monotonic()-started
    dest = out/('structure_and_lower_verification.json' if args.structure_only else 'certificate_verification.json')
    assert not dest.exists(); dest.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__': main()
