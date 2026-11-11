"""Independent standard-library exact structure, primal and dual verification.

Does not import assembly, recovery, the max-B lift, or a numerical library.
The old entire matrix is compared literally, the new row is rebuilt from
the 16 hist descriptors, and every required row and column is evaluated.
"""
from collections import Counter
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
WORK = HERE.parent
REPO = WORK.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'
PINS = {
    BASE / 'exact_matrix.json.gz': '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30',
    BASE / 'augmented_lp_exact.json': 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932',
    BASE / 'exact_dual_certificate.json': '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3',
    WORK / 'terminal_response_cycles/max_b_exact_certificate.json': 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664',
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def rat(s):
    return Q(s)


def dot(row, values):
    return sum((rat(a) * values[j] for j, a in row if values[j]), Q())


def emit(out, name, data):
    p = out / name
    assert not p.exists(), ('refuse_overwrite', str(p))
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def residuals(matrix, certificate):
    lower = Q(certificate['normalization_multiplier'])
    result = [Q(c) - lower * Q(a) for c, a in zip(matrix['objective'], matrix['normalization'])]
    seen = set()
    for i, v in certificate['row_multipliers']:
        assert type(i) is int and 0 <= i < len(matrix['rows']) and i not in seen
        seen.add(i)
        weight = Q(v)
        assert weight > 0
        for j, a in matrix['rows'][i]:
            result[j] -= weight * rat(a)
    assert min(result) >= 0
    assert result == list(map(Q, certificate['residuals']))
    return lower, result


def canonical_check(matrix, x, epi, zz):
    thresholds = dict(epi['thresholds'])
    assert len(thresholds) == 7954 and len(zz['auxiliaries']) == 2790
    auxiliary = set(thresholds)
    for j, i in thresholds.items():
        value = max(Q(), -dot([[k, a] for k, a in matrix['rows'][i] if k < 4849], x))
        assert x[j] == value, ('noncanonical_max', j)
    for record in zz['auxiliaries']:
        j = record['column']
        assert j not in auxiliary
        auxiliary.add(j)
        value = min(dot([[k, a] for k, a in matrix['rows'][i] if k < 4849], x)
                    for i in (record['q_upper_row'], record['v_upper_row']))
        assert x[j] == value, ('noncanonical_min', j)
    assert auxiliary == set(range(4849, 15593))
    return {'canonical_max_checked': len(thresholds), 'canonical_min_checked': len(zz['auxiliaries'])}


def analytical_row(columns):
    rebuilt = [[0, '1']]
    table = []
    for j, c in enumerate(columns[:4849]):
        if c['kind'] != 'hist':
            continue
        bits = tuple(map(int, c['actual_bits']))
        p = sum(bits[:4])
        n = sum(bits)
        denominator = (p + 1) * (p + 2)
        counts = c['hist']
        assert len(counts) == 8 and sum(counts) == 6
        d_b = sum(w[1] * count for w, count in zip(product((0, 1), repeat=3), counts))
        d_c = sum(w[2] * count for w, count in zip(product((0, 1), repeat=3), counts))
        d_bc = sum(w[1] * w[2] * count for w, count in zip(product((0, 1), repeat=3), counts))
        u = Q(bits[4], n) if bits[4] else Q()
        v = Q(bits[5], n) if bits[5] else Q()
        rho = Q(12 * bits[5] + 24 * bits[4] + 6 * d_c - (p + 2) * (p + 9), denominator)
        a = (64 * u + 24 * v - Q(12 * bits[5], p + 1)
             - Q(8 * d_b + 26 * d_c, 3 * (p + 1)) + Q(8 * d_bc, 3 * denominator)
             + max(Q(), rho))
        if a:
            rebuilt.append([j, str(a)])
        table.append({'column': j, 'descriptor': c, 'coefficient': str(a), 'kappa': str(rho)})
    assert len(table) == 16 and len(rebuilt) == 17
    return rebuilt, table


def universal_formula_check():
    checked = 0
    for p in range(5):
        d = (p + 1) * (p + 2)
        for a5, a6, x in product((0, 1), repeat=3):
            total = p + a5 + a6
            u = Q(a5, total) if a5 else Q()
            v = Q(a6, total) if a6 else Q()
            for n00 in range(7):
                for n01 in range(7 - n00):
                    for n10 in range(7 - n00 - n01):
                        n11 = 6 - n00 - n01 - n10
                        b, c, bc = Q(n10 + n11, 6), Q(n01 + n11, 6), Q(n11, 6)
                        cap_a = u - Q(a6, p + 1) + Q(a6 * x, d)
                        cap_c = u - c / (p + 1) + c * x / d
                        quote = v - Q(x, p + 1) + Q(a5 * x, d)
                        pair = u + Q(x, p + 1) - (b + c) / (p + 1) + bc / d
                        raw = 12 * cap_a + 36 * cap_c + 24 * quote - x + 16 * pair
                        base = 64 * u + 24 * v - Q(12 * a6, p + 1) - (16 * b + 52 * c) / (p + 1) + 16 * bc / d
                        rho = Q(12 * a6 + 24 * a5, d) + 36 * c / d - Q(8, p + 1) - 1
                        assert raw == base + rho * x
                        assert max(Q(), rho) - rho * x >= 0
                        checked += 1
    assert checked == 3360
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--structure-only', action='store_true')
    parser.add_argument('--output', default=str(HERE))
    args = parser.parse_args()
    out = Path(args.output).resolve()
    assert out == HERE or out.is_relative_to(HERE)
    started = time.monotonic()
    for p, pin in PINS.items():
        assert sha(p) == pin, str(p)
    inputs = read(HERE / 'inputs_manifest.json')
    for record in inputs['source_files']:
        p = REPO / record['path']
        assert sha(p) == record['sha256'], str(p)
    for name, pin in inputs['generated_inputs'].items():
        assert sha(HERE / name) == pin, name
    old = read(BASE / 'exact_matrix.json.gz')
    matrix = read(HERE / 'exact_matrix.json.gz')
    assert len(matrix['rows']) == len(matrix['row_names']) == 20911
    assert len(matrix['columns']) == len(matrix['objective']) == len(matrix['normalization']) == 20585
    assert matrix['rows'][:20910] == old['rows'] and matrix['row_names'][:20910] == old['row_names']
    for name in ('columns', 'objective', 'normalization'):
        assert matrix[name] == old[name]
    assert sum(map(len, matrix['rows'])) == 3208814
    for i, row in enumerate(matrix['rows']):
        seen = set()
        for j, a in row:
            assert type(j) is int and 0 <= j < 20585 and j not in seen, ('invalid_sparse_row', i, j)
            assert rat(a)
            seen.add(j)
    cut, mapping = analytical_row(matrix['columns'])
    certificate = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')
    assert matrix['rows'][20910] == cut == certificate['sparse_original4849_row_K_normalized']
    assert all(j < 4849 for j, a in cut)
    assert matrix['maxb_cut_row'] == 20910 and matrix['all_columns_nonnegative'] is True
    assert matrix['this_round_added'] == 1 and matrix['this_round_added_columns'] == 0
    assert matrix['maxb_cut_certificate_sha256'] == PINS[WORK / 'terminal_response_cycles/max_b_exact_certificate.json']
    full624 = matrix['columns'][15593:]
    assert len(full624) == 4992
    assert {c['kind'] for c in full624} == {'actual4-R-shared624-conditional-mass'}
    assert len({c['hist_column'] for c in full624}) == 16
    block_sizes = Counter((c['hist_column'], json.dumps(c['group']), tuple(c['state'])) for c in full624)
    assert len(block_sizes) == 312 and set(block_sizes.values()) == {16}
    assert all(matrix['rows'][i + 1] == [[j, str(-rat(a))] for j, a in matrix['rows'][i]]
               for i in range(19662, 20286, 2))
    literal_cases = universal_formula_check()
    old_point = read(BASE / 'augmented_lp_exact.json')
    old_x = [Q(c['weight']) for c in old_point['columns']]
    assert len(old_x) == 20585 and min(old_x) >= 0
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in old_point['columns']] == matrix['columns']
    old_slacks = [dot(row, old_x) for row in old['rows']]
    assert min(old_slacks) >= 0
    old_o = sum((Q(a) * v for a, v in zip(matrix['normalization'], old_x)), Q())
    old_w = sum((Q(a) * v for a, v in zip(matrix['objective'], old_x)), Q())
    assert old_o == 1 and old_w == Q(old_point['W'])
    cut_value = dot(cut, old_x)
    assert cut_value == Q(certificate['K_normalized_point_value']) < 0
    inherited = read(HERE / 'inherited_dual_lower_bound.json')
    old_dual = read(BASE / 'exact_dual_certificate.json')
    lower, residual = residuals(matrix, inherited)
    assert lower == old_w and inherited['row_multipliers'] == old_dual['row_multipliers']
    assert inherited['added_row_multiplier'] == [20910, '0']
    assert all(i < 20910 for i, a in inherited['row_multipliers'])
    assert inherited['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    assert sum((a * b for a, b in zip(residual, old_x)), Q()) == 0
    assert sum((Q(v) * old_slacks[i] for i, v in inherited['row_multipliers']), Q()) == 0
    epi = read(HERE / 'epigraph_structure.json')
    zz = read(HERE / 'zz_envelope_structure.json')
    old_canonical = canonical_check(matrix, old_x, epi, zz)
    hist = [record['column'] for record in mapping]
    zero_hist = [j for j in hist if old_x[j] == 0]
    assert len(zero_hist) == 6
    for j, c in enumerate(full624, 15593):
        if c['hist_column'] in zero_hist:
            assert old_x[j] == 0
    summary = {
        'status': 'PASS', 'verification': 'Independent standard-library exact verification; no construction or recovery imports.',
        'rows': 20911, 'columns': 20585, 'nonzeros': 3208814,
        'old_rows_unchanged': 20910, 'old_descriptors_unchanged': 20585,
        'old_objective_normalization_unchanged': True, 'added_row': 20910, 'added_nonzeros': 17,
        'independently_reconstructed_histograms': 16, 'zero_histograms_retained': zero_hist,
        'shared624_columns_retained': 4992, 'shared624_blocks_retained': 312,
        'all_old_10744_auxiliaries_retained': True, 'new_row_auxiliary_coefficients_zero': 15736,
        'universal_boolean_count_cases': literal_cases, 'fixed_point_rhs_substitutions': 0,
        'old_primal_rows_checked': 20910, 'inherited_dual_columns_checked': 20585,
        'inherited_lower_bound': str(lower), 'old_point_cut_value': str(cut_value),
        'old_point_cut_value_float': float(cut_value), 'old_canonical_auxiliary_checks': old_canonical,
        'matrix_sha256': sha(HERE / 'exact_matrix.json.gz'), 'verifier_sha256': sha(Path(__file__)),
        'scope': 'Fixed16-hist necessary LP; no complete SPE realization or six-player half theorem.'}
    if args.structure_only:
        summary['seconds'] = time.monotonic() - started
        emit(out, 'structure_and_lower_verification.json', summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
        return
    point = read(out / 'augmented_lp_exact.json')
    x = [Q(c['weight']) for c in point['columns']]
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == matrix['columns']
    assert len(x) == 20585 and min(x) >= 0
    assert sum((Q(a) * v for a, v in zip(matrix['normalization'], x)), Q()) == 1
    value = sum((Q(a) * v for a, v in zip(matrix['objective'], x)), Q())
    assert value == Q(point['W']) and value >= lower
    slacks = [dot(row, x) for row in matrix['rows']]
    assert min(slacks) >= 0
    canonical = canonical_check(matrix, x, epi, zz)
    dual = read(out / 'exact_dual_certificate.json')
    new_lower, new_residuals = residuals(matrix, dual)
    assert new_lower == value
    assert dual['matrix_sha256'] == sha(HERE / 'exact_matrix.json.gz')
    assert sum((Q(v) * slacks[i] for i, v in dual['row_multipliers']), Q()) == 0
    assert sum((a * b for a, b in zip(new_residuals, x)), Q()) == 0
    if (out / 'primal_exact_audit.json').exists():
        audit = read(out / 'primal_exact_audit.json')
        assert list(map(Q, audit['row_slacks'])) == slacks
        assert Q(audit['W']) == value and Q(audit['old_W']) == lower
        recovery = audit['recovery']
        inputs_file = out / ('primal_' + recovery['attempt'] + '_recovery_inputs.json')
        if inputs_file.exists():
            selected = read(inputs_file)
            support = selected['support']
            assert support == recovery['support']
            local = [x[j] for j in support]
            for equation in selected['selected_equations']:
                left = sum((Q(a) * local[j] for j, a in equation if j < len(support)), Q())
                right = sum((Q(a) for j, a in equation if j == len(support)), Q())
                assert left == right
    summary.update(status='EXACT_OPTIMUM_VERIFIED', W=str(value), W_float=float(value),
                   exact_increase=str(value - lower), increase_float=float(value - lower),
                   same_optimum=value == lower, strict_half_gap=str(1 - 2 * value),
                   new_row_slack=str(slacks[20910]), minimum_primal_slack=str(min(slacks)),
                   all_primal_rows_checked=len(slacks), all_dual_columns_checked=len(new_residuals),
                   positive_dual_rows=len(dual['row_multipliers']), new_canonical_auxiliary_checks=canonical,
                   primal_sha256=sha(out / 'augmented_lp_exact.json'), dual_sha256=sha(out / 'exact_dual_certificate.json'),
                   seconds=time.monotonic() - started)
    emit(out, 'certificate_verification.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
