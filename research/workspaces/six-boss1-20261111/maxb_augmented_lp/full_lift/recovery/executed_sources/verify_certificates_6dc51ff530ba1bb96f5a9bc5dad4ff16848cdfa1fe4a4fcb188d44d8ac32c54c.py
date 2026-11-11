"""Independent exact verification of the entire22297 by21021 common-X LP.

Standard library only. No assembly, recovery, numerical or lift-builder
imports. Rebuilds all1387 lift rows from literal labels and old descriptors,
checks full-coordinate Farkas elimination, and verifies every primal/dual
coordinate and all11164 canonical auxiliaries when certificates are given.
"""
from collections import defaultdict, Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
REPO = WORK.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'
M, N, ORIG, ADDM, ADDN = 20910, 20585, 4849, 1387, 436
PINS = {
    BASE / 'exact_matrix.json.gz': '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30',
    BASE / 'augmented_lp_exact.json': 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932',
    BASE / 'exact_dual_certificate.json': '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3',
    WORK / 'terminal_response_cycles/max_b_symbolic_lift.json': '52129dc848cf47f569f61442962a01aec61c6317531be0d24837d41071c96a5c',
    WORK / 'terminal_response_cycles/max_b_exact_certificate.json': 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664',
    WORK / 'actual_pair_20910/symbolic_rows.json.gz': '423bf2c92d9c85c7e6086a193365ed80cd2427d7f7ee406972e1faf1813ea62f',
}


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as f: return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def rat(v): return Q(v)


def dot(row, x): return sum((rat(v) * x[j] for j, v in row if x[j]), Q())


def frozen(x): return tuple(map(frozen, x)) if isinstance(x, list) else x


def add(row, j, v):
    row[j] = row.get(j, Q()) + v
    if not row[j]: del row[j]


def encode(row): return [[j, str(v)] for j, v in sorted(row.items()) if v]


def remap(j):
    assert 0 <= j < ORIG + ADDN
    return j if j < ORIG else N + j - ORIG


def name_in_full(name):
    name = list(name)
    if name[0] in ('overlap-at-most-X', 'overlap-at-most-query'): name[1] = remap(name[1])
    return 'common-max-B:' + json.dumps(name, ensure_ascii=False, separators=(',', ':'))


def literal_lift(old, lift, pairs):
    """Literal independent reconstruction, in full21021-column coordinates."""
    hist = {}; own = defaultdict(dict); b4 = defaultdict(dict)
    for j, c in enumerate(old['columns'][:ORIG]):
        if c['kind'] == 'hist': h = j; hist[h] = c
        elif c['kind'] == 'joint-reply': own[h][frozen(c['group']), tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']][tuple(c['hidden']) + (c['ell'] // 6,)] = j
    assert len(hist) == 16
    xc = {}; yc = {}; masses = {}
    for k, c in enumerate(lift['new_columns'], N):
        h = c['hist_column']; assert h in hist
        if c['kind'] == 'common-X-mass':
            assert k < N + 16 and h not in xc
            xc[h] = k
        else:
            assert c['kind'] == 'X-query-overlap-upper' and k >= N + 16
            token = frozen(c['query_token']); assert (h, token) not in yc
            yc[h, token] = k
            if token[0] == 'H': marginal = {j: Q(1) for s, j in b4[h].items() if s[token[1]]}
            else:
                slot = int(token[0] == 'Z'); group = token[1]
                marginal = {j: Q(1) for (g, state), j in own[h].items() if g == group and state[slot]}
            assert encode(marginal) == c['query_marginal']
            masses[h, token] = marginal
    assert set(xc) == set(hist) and len(yc) == 420
    actions = [('A', k) for k in range(6)] + [(k, i) for k in ('T', 'B', 'C') for i in range(6)]
    for k in ('R', 'Z'):
        actions += [(k, f, i, j) for f in range(2) for i in range(6) for j in range(6) if f or i != j]
    actions += [('H', 0), ('H', 1)]
    assert len(actions) == len(set(actions)) == 158
    orbits = defaultdict(list)
    for q in actions:
        key = q if q[0] in ('A', 'H') else (q[0],) if q[0] in ('T', 'B', 'C') else (q[0], q[1], int(q[2] == q[3]))
        orbits[key].append(q)
    assert len(orbits) == 17
    rebuilt = {}
    for h in hist: rebuilt['X-at-most-hist', h] = {h: Q(1), xc[h]: Q(-1)}
    for (h, token), k in yc.items():
        compressed = k - N + ORIG
        rebuilt['overlap-at-most-X', compressed] = {xc[h]: Q(1), k: Q(-1)}
        row = dict(masses[h, token]); row[k] = Q(-1)
        rebuilt['overlap-at-most-query', compressed] = row
    income = [{} for k in range(6)]; tax = {}; bx = {}
    for h, c in hist.items():
        bits = tuple(map(int, c['actual_bits'])); p = sum(bits[:4]); total = sum(bits)
        for k in range(6):
            if bits[k]: income[k][h] = Q(1, total)
        if bits[4]: tax[h] = Q(1, (p + 1) * (p + 2))
        bx[xc[h]] = Q(1, p + 1)
    terms = 0
    for orbit, queries in orbits.items():
        maximum = dict(bx); cap = dict(income[4]); scale = Q(1, len(queries))
        for h, c in hist.items():
            bits = tuple(map(int, c['actual_bits'])); p = sum(bits[:4]); d = (p + 1) * (p + 2)
            words = [w for w, count in zip(product((0, 1), repeat=3), c['hist']) for i in range(count)]
            assert len(words) == 6
            for q in queries:
                if q[0] == 'A': token = ('bit', bits[q[1]])
                elif q[0] in ('T', 'B', 'C'): token = ('bit', words[q[1]][('T', 'B', 'C').index(q[0])])
                elif q[0] == 'H': token = q
                else:
                    kind, f, i, j = q
                    token = (kind, (f, int(i == j), words[i], words[j]))
                if token[0] == 'bit':
                    if token[1]:
                        add(maximum, h, -scale / (p + 1)); add(cap, h, -scale / (p + 1)); add(cap, xc[h], scale / d)
                else:
                    for j, v in masses[h, token].items():
                        add(maximum, j, -scale * v / (p + 1)); add(cap, j, -scale * v / (p + 1))
                    add(cap, yc[h, token], scale / d)
                terms += 1
        rebuilt[('maximum-B',) + orbit] = maximum
        rebuilt[('X-caps-query',) + orbit] = cap
    for k in range(6):
        row = dict(income[k])
        for h, c in hist.items(): add(row, xc[h], -Q(1, sum(map(int, c['actual_bits'][:k])) + 6 - k))
        rebuilt['actual-safe-X', k + 1] = row
    row = {0: Q(1)}
    for j in xc.values(): row[j] = Q(-1)
    rebuilt['capacity-X',] = row
    assert len(pairs['rows']) == 490
    for record in pairs['rows']:
        row = {j: Q(v) for j, v in record['sparse_original4849_row']}
        for j, v in income[5].items(): add(row, j, -v)
        for j, v in tax.items(): add(row, j, -v)
        for j, v in bx.items(): add(row, j, v)
        rebuilt['common-B-pair', record['orbit_id']] = row
    assert len(rebuilt) == 1387
    return rebuilt, hist, xc, yc, terms


def direct_compact(hist):
    row = {0: Q(1)}
    for h, c in hist.items():
        bits = tuple(map(int, c['actual_bits'])); p = sum(bits[:4]); total = sum(bits); d = (p + 1) * (p + 2)
        b = sum(w[1] * count for w, count in zip(product((0, 1), repeat=3), c['hist']))
        cc = sum(w[2] * count for w, count in zip(product((0, 1), repeat=3), c['hist']))
        bc = sum(w[1] * w[2] * count for w, count in zip(product((0, 1), repeat=3), c['hist']))
        u = Q(bits[4], total) if bits[4] else Q(); v = Q(bits[5], total) if bits[5] else Q()
        rho = Q(12 * bits[5] + 24 * bits[4] + 6 * cc - (p + 2) * (p + 9), d)
        add(row, h, 64 * u + 24 * v - Q(12 * bits[5], p + 1) - Q(8 * b + 26 * cc, 3 * (p + 1)) + Q(8 * bc, 3 * d) + max(Q(), rho))
    return encode(row)


def dual_residual(matrix, cert):
    lower = Q(cert['normalization_multiplier'])
    result = [Q(c) - lower * Q(a) for c, a in zip(matrix['objective'], matrix['normalization'])]
    seen = set()
    for i, value in cert['row_multipliers']:
        assert type(i) is int and 0 <= i < M + ADDM and i not in seen
        seen.add(i); weight = Q(value); assert weight > 0
        for j, a in matrix['rows'][i]: result[j] -= weight * rat(a)
    assert min(result) >= 0 and result == list(map(Q, cert['residuals']))
    return lower, result


def canonical(matrix, x, epi, zz, xb):
    used = set()
    for j, i in epi['thresholds']:
        assert x[j] == max(Q(), -dot([[k, v] for k, v in matrix['rows'][i] if k < ORIG], x))
        used.add(j)
    assert len(used) == 7954
    for r in zz['auxiliaries']:
        j = r['column']; assert j not in used; used.add(j)
        assert x[j] == min(dot([[k, v] for k, v in matrix['rows'][i] if k < ORIG], x)
                           for i in (r['q_upper_row'], r['v_upper_row']))
    assert used == set(range(4849, 15593))
    for r in xb['auxiliaries']:
        assert x[r['column']] == min(x[r['x_column']], dot(r['query_marginal'], x))
    assert len(xb['auxiliaries']) == 420
    return {'old_max': 7954, 'old_min': 2790, 'common_X_min': 420, 'total': 11164}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--structure-only', action='store_true'); parser.add_argument('--output', default=str(HERE))
    args = parser.parse_args(); out = Path(args.output).resolve()
    assert out == HERE or out.is_relative_to(HERE)
    started = time.monotonic()
    for path, pin in PINS.items(): assert sha(path) == pin, str(path)
    manifest = read(HERE / 'inputs_manifest.json')
    for record in manifest['source_files']: assert sha(REPO / record['path']) == record['sha256'], record['path']
    for name, pin in manifest['generated_inputs'].items(): assert sha(HERE / name) == pin, name
    old = read(BASE / 'exact_matrix.json.gz'); matrix = read(HERE / 'exact_matrix.json.gz')
    assert len(matrix['rows']) == len(matrix['row_names']) == M + ADDM
    assert len(matrix['columns']) == len(matrix['objective']) == len(matrix['normalization']) == N + ADDN
    assert matrix['rows'][:M] == old['rows'] and matrix['row_names'][:M] == old['row_names']
    for name in ('columns', 'objective', 'normalization'): assert matrix[name][:N] == old[name]
    assert matrix['objective'][N:] == matrix['normalization'][N:] == ['0'] * ADDN
    assert sum(map(len, matrix['rows'])) == 3296061
    for i, row in enumerate(matrix['rows']):
        seen = set()
        for j, value in row:
            assert type(j) is int and 0 <= j < N + ADDN and j not in seen and rat(value), (i, j)
            seen.add(j)
    lift = read(WORK / 'terminal_response_cycles/max_b_symbolic_lift.json')
    pairs = read(WORK / 'actual_pair_20910/symbolic_rows.json.gz')
    assert matrix['columns'][N:] == lift['new_columns']
    rebuilt, hist, xc, yc, terms = literal_lift(old, lift, pairs)
    coefficients = 0
    for i, record in enumerate(lift['rows']):
        expected = encode(rebuilt[tuple(record['name'])])
        assert expected == [[remap(j), value] for j, value in record['row']]
        assert matrix['rows'][M + i] == expected
        assert matrix['row_names'][M + i] == name_in_full(record['name'])
        coefficients += len(expected)
    assert coefficients == 87264
    xb = read(HERE / 'maxb_envelope_structure.json')
    assert xb['core_columns'] == list(range(N, N + 16)) == list(xc.values())
    assert xb['hist_to_x'] == [[h, j] for h, j in xc.items()]
    assert len(xb['auxiliaries']) == 420
    negative_y = defaultdict(list)
    for i in range(M, M + ADDM):
        for j, value in matrix['rows'][i]:
            if j >= N + 16 and rat(value) < 0: negative_y[j].append((i, rat(value)))
    for record in xb['auxiliaries']:
        j = record['column']; c = matrix['columns'][j]
        assert record['x_column'] == xc[c['hist_column']] and record['query_marginal'] == c['query_marginal']
        assert negative_y[j] == [(record['x_upper_row'], Q(-1)), (record['query_upper_row'], Q(-1))]
        assert matrix['rows'][record['x_upper_row']] == [[record['x_column'], '1'], [j, '-1']]
        assert matrix['rows'][record['query_upper_row']] == record['query_marginal'] + [[j, '-1']]
    assert set(negative_y) == set(range(N + 16, N + ADDN))
    assert len(matrix['columns'][15593:N]) == 4992
    assert {c['kind'] for c in matrix['columns'][15593:N]} == {'actual4-R-shared624-conditional-mass'}
    assert all(matrix['rows'][i + 1] == [[j, str(-rat(v))] for j, v in matrix['rows'][i]] for i in range(19662, 20286, 2))
    cert = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json'); combination = {}
    for record in cert['row_multipliers']:
        i = record['row_index']; weight = Q(record['multiplier'])
        assert weight > 0 and record['name'] == lift['rows'][i]['name']
        for j, value in matrix['rows'][M + i]: add(combination, j, weight * rat(value))
    for record in cert['new_nonnegativity_multipliers']:
        j = remap(record['column']); weight = Q(record['multiplier'])
        assert weight > 0 and matrix['columns'][j] == record['descriptor']
        add(combination, j, weight)
    assert all(j < ORIG for j in combination) and len(combination) == 17
    projected = [[j, str(v / 3)] for j, v in sorted(combination.items())]
    assert projected == cert['sparse_original4849_row_K_normalized'] == direct_compact(hist)
    projection = read(HERE / 'full_coordinate_farkas_projection.json')
    assert projection['projected_row'] == projected and projection['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    old_point = read(BASE / 'augmented_lp_exact.json'); old_x = [Q(c['weight']) for c in old_point['columns']] + [Q()] * ADDN
    assert min(old_x) >= 0
    old_slacks = [dot(row, old_x) for row in old['rows']]; assert min(old_slacks) >= 0
    assert sum((Q(a) * v for a, v in zip(matrix['normalization'], old_x)), Q()) == 1
    old_w = sum((Q(a) * v for a, v in zip(matrix['objective'], old_x)), Q()); assert old_w == Q(old_point['W'])
    value = dot(projected, old_x); assert value == Q(cert['K_normalized_point_value']) == Q(projection['old_point_value']) < 0
    inherited = read(HERE / 'inherited_dual_lower_bound.json'); old_dual = read(BASE / 'exact_dual_certificate.json')
    lower, residual = dual_residual(matrix, inherited)
    assert lower == old_w and inherited['row_multipliers'] == old_dual['row_multipliers']
    assert all(i < M for i, value in inherited['row_multipliers'])
    assert residual[N:] == [Q()] * ADDN and residual[:N] == list(map(Q, old_dual['residuals']))
    assert inherited['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    assert sum((Q(v) * old_slacks[i] for i, v in inherited['row_multipliers']), Q()) == 0
    assert sum((a * b for a, b in zip(residual, old_x)), Q()) == 0
    epi = read(HERE / 'epigraph_structure.json'); zz = read(HERE / 'zz_envelope_structure.json')
    canonical(matrix, old_x, epi, zz, xb)
    zeros = [h for h in hist if not old_x[h]]; assert len(zeros) == 6
    summary = {'status': 'PASS', 'verifier_sha256': sha(Path(__file__)), 'rows': M + ADDM, 'columns': N + ADDN,
               'nonzeros': 3296061, 'old_rows_unchanged': M, 'old_column_descriptors_unchanged': N,
               'literal_new_rows_rebuilt': 1387, 'literal_new_coefficients_rebuilt': coefficients,
               'literal_hist_query_terms': terms, 'all158_labels_and17_single_orbits': True, 'all490_pair_orbits': True,
               'new_descriptors_checked': 436, 'shared_X_core_columns': 16, 'canonical_new_min_columns': 420,
               'all_new_min_occurrences_have_correct_monotonicity': True,
               'all4992_shared624_columns_and312_equalities_retained': True, 'old10744_auxiliaries_retained': True,
               'zero_histograms_retained': zeros, 'fixed_point_rhs_substitutions': 0,
               'compactcut_not_separately_appended': True, 'full_coordinate_Farkas_new436_coefficients_zero': True,
               'full_coordinate_Farkas_old15736_auxiliary_coefficients_zero': True,
               'Farkas_projection_matches_independent_hist_formula': True,
               'fixed_old_point_has_no_common_X_extension': True, 'old_point_projection_value': str(value),
               'old_primal_rows_reverified': M, 'inherited_dual_columns_checked': N + ADDN,
               'inherited_lower_bound': str(lower), 'new436_dual_residuals_zero': True,
               'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'),
               'scope': 'Complete common-X fixed16-hist necessary LP; no complete SPE realization or original half theorem.'}
    if not args.structure_only:
        point = read(out / 'augmented_lp_exact.json'); x = [Q(c['weight']) for c in point['columns']]
        assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == matrix['columns']
        assert len(x) == N + ADDN and min(x) >= 0
        assert sum((Q(a) * v for a, v in zip(matrix['normalization'], x)), Q()) == 1
        w = sum((Q(a) * v for a, v in zip(matrix['objective'], x)), Q()); assert w == Q(point['W']) and w >= lower
        slacks = [dot(row, x) for row in matrix['rows']]; assert min(slacks) >= 0
        canonical_counts = canonical(matrix, x, epi, zz, xb)
        dual = read(out / 'exact_dual_certificate.json'); new_lower, new_residual = dual_residual(matrix, dual)
        assert new_lower == w and dual['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
        assert sum((Q(v) * slacks[i] for i, v in dual['row_multipliers']), Q()) == 0
        assert sum((a * b for a, b in zip(new_residual, x)), Q()) == 0
        audit = read(out / 'primal_exact_audit.json')
        assert list(map(Q, audit['row_slacks'])) == slacks and Q(audit['W']) == w and Q(audit['old_W']) == lower
        recovery = audit['recovery']; selected = read(out / ('primal_' + recovery['attempt'] + '_recovery_inputs.json'))
        support = selected['support']; assert support == recovery['support']; local = [x[j] for j in support]
        for equation in selected['selected_equations']:
            assert sum((Q(a) * local[j] for j, a in equation if j < len(support)), Q()) == sum((Q(a) for j, a in equation if j == len(support)), Q())
        summary.update(status='EXACT_OPTIMUM_VERIFIED', W=str(w), W_float=float(w), same_optimum=w == lower,
                       exact_increase=str(w - lower), increase_float=float(w - lower), strict_half_gap=str(1 - 2 * w),
                       all_primal_rows_checked=len(slacks), all_dual_columns_checked=len(new_residual),
                       canonical_checks=canonical_counts, minimum_primal_slack=str(min(slacks)),
                       positive_dual_rows=len(dual['row_multipliers']), compactcut_slack=str(dot(projected, x)),
                       primal_sha256=sha(out / 'augmented_lp_exact.json'), dual_sha256=sha(out / 'exact_dual_certificate.json'))
    summary['seconds'] = time.monotonic() - started
    name = 'structure_and_lower_verification.json' if args.structure_only else 'certificate_verification.json'
    destination = out / name; assert not destination.exists()
    destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__': main()
