"""Independent exact audit of facial closure and the whole-face AP39 identity.

Does not import the builder. Rechecks the old optimality certificate,
enumerates all opposite row pairs independently, replays every sign proof,
checks convergence, and verifies the signed identity on all 21021 columns.
This is an algebraic proof about the entire W10 optimum face, not a claim
of an improved quantitative dual bound or of SPE realizability.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
M, N = 22297, 21021
PINS = {
    'maxb_augmented_lp/full_lift/exact_matrix.json.gz': 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b',
    'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json': '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe',
    'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json': '4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f',
    'early_x_anchor_queries/rows_51.json': '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb',
}


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt') if path.suffix == '.gz' else path.open() as stream:
        return json.load(stream)


def write(name, value):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    if path.suffix == '.gz':
        with path.open('xb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
                compressed.write((json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    else:
        with path.open('x') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


@lru_cache(maxsize=None)
def f(value):
    return F(value)


def independent_digest(encoded, sign):
    # A different canonical byte format from the builder; exact matching is
    # checked after hashing, and the full matrix is scanned for completeness.
    text = '|'.join(str(j) + ':' + str(sign * f(v)) for j, v in sorted(encoded))
    return sha256(text.encode()).hexdigest()


def main():
    started = time.monotonic()
    for relative, expected in PINS.items():
        assert sha(WORK / relative) == expected
    matrix = read(WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz')
    primal = read(WORK / 'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json')
    dual = read(WORK / 'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json')
    package = read(WORK / 'early_x_anchor_queries/rows_51.json')
    closure = read(HERE / 'closure_certificate.json.gz')
    identity = read(HERE / 'expanded_signed_identity.json')
    span = read(HERE / 'expanded_span_inputs.json.gz')
    assert closure['source_sha256'] == identity['source_sha256'] == PINS
    assert identity['closure_certificate_sha256'] == span['closure_certificate_sha256'] == sha(HERE / 'closure_certificate.json.gz')
    assert identity['status'] == 'EXACT_WHOLE_W10_FACE_AP39_IDENTITY'
    assert closure['primal_support_zeros_used_as_premises'] is False
    rows = matrix['rows']
    assert len(rows) == len(matrix['row_names']) == M
    assert len(matrix['columns']) == len(primal['columns']) == N
    x = [f(c['weight']) for c in primal['columns']]
    assert min(x) >= 0
    for original, weighted in zip(matrix['columns'], primal['columns']):
        assert original == {k: v for k, v in weighted.items() if k != 'weight'}
    norm = list(map(f, matrix['normalization']))
    objective = list(map(f, matrix['objective']))
    assert len(norm) == len(objective) == N
    assert sum((a * b for a, b in zip(norm, x)), F()) == 1
    W = sum((a * b for a, b in zip(objective, x)), F())
    assert W == f(primal['W']) == f(dual['normalization_multiplier'])
    slacks = []
    row_hashes, negative_hashes, buckets = [], [], {}
    for i, row in enumerate(rows):
        assert len({j for j, _ in row}) == len(row)
        slack = sum((f(v) * x[j] for j, v in row if x[j]), F())
        assert slack >= 0
        slacks.append(slack)
        h = independent_digest(row, 1)
        nh = independent_digest(row, -1)
        row_hashes.append(h)
        negative_hashes.append(nh)
        buckets.setdefault(h, []).append(i)
    lam = {}
    residual = [a - W * b for a, b in zip(objective, norm)]
    for i, text in dual['row_multipliers']:
        value = f(text)
        assert 0 <= i < M and value > 0 and i not in lam
        lam[i] = value
        assert slacks[i] == 0
        for j, a in rows[i]:
            residual[j] -= value * f(a)
    assert residual == list(map(f, dual['residuals'])) and min(residual) >= 0
    Z0 = {j for j, value in enumerate(residual) if value > 0}
    assert len(lam) == 463 and len(Z0) == 5379
    assert all(x[j] == 0 for j in Z0)
    assert sorted(lam) == closure['initial_positive_dual_rows']
    assert sorted(Z0) == closure['initial_positive_residual_zero_columns']
    print(json.dumps({'event': 'independent_old_optimality_pass', 'rows': M,
                      'columns': N, 'seconds': time.monotonic() - started}), flush=True)

    expected_groups = set()
    expected_opposite_rows = set()
    visited = set()
    for i, h in enumerate(row_hashes):
        nh = negative_hashes[i]
        if h in visited or nh not in buckets:
            continue
        left, right = buckets[h], buckets[nh]
        representative = {j: f(a) for j, a in rows[left[0]]}
        for k in left:
            assert {j: f(a) for j, a in rows[k]} == representative
        for k in right:
            assert {j: -f(a) for j, a in rows[k]} == representative
        key = tuple(sorted((tuple(left), tuple(right))))
        expected_groups.add(key)
        expected_opposite_rows.update(left + right)
        visited.update((h, nh))
    actual_groups = set()
    group_for_row = {}
    for group in closure['all_exact_opposite_row_groups']:
        left, right = group['left_rows'], group['right_rows']
        key = tuple(sorted((tuple(left), tuple(right))))
        assert key not in actual_groups
        actual_groups.add(key)
        for i in left + right:
            group_for_row[i] = group['group_id']
    assert actual_groups == expected_groups
    assert len(expected_opposite_rows) == closure['opposite_row_count']
    E0 = set(lam) | expected_opposite_rows
    assert sorted(E0) == closure['initial_equality_rows']
    Z, E = set(Z0), set(E0)
    first_zero_step = {}
    for number, step in enumerate(closure['proof_steps']):
        assert step['step'] == number
        i = step['original_row_index']
        assert step['original_row'] == rows[i]
        assert step['original_row_name'] == matrix['row_names'][i]
        assert step['known_zero_premise_columns'] == [j for j, _ in rows[i] if j in Z]
        remainder = [(j, f(a)) for j, a in rows[i] if j not in Z]
        forced = step['new_forced_zero_columns']
        assert set(forced) == {j for j, _ in remainder} and len(forced) == len(remainder) > 0
        if step['rule'] == 'remaining_coefficients_strictly_negative_in_original_inequality':
            assert all(a < 0 for _, a in remainder)
        elif step['rule'] == 'remaining_coefficients_strictly_positive_in_proven_equality':
            assert i in E and all(a > 0 for _, a in remainder)
        else:
            raise AssertionError('Unrecognized propagation rule')
        for j in forced:
            assert j not in Z
            Z.add(j)
            first_zero_step[j] = number
        E.add(i)
    E |= {i for i, row in enumerate(rows) if all(j in Z for j, _ in row)}
    assert sorted(Z) == closure['known_zero_columns']
    assert sorted(E) == closure['known_equality_rows']
    assert all(x[j] == 0 for j in Z)
    assert all(slacks[i] == 0 for i in E)
    # Verify no further authorized rule can add another coordinate.
    for i, row in enumerate(rows):
        remaining = [f(a) for j, a in row if j not in Z]
        if remaining:
            assert any(a > 0 for a in remaining)
            if i in E:
                assert any(a < 0 for a in remaining)
    column_provenance = dict(closure['column_provenance'])
    assert set(column_provenance) == Z
    for j, provenance in column_provenance.items():
        if j in Z0:
            assert provenance == {'kind': 'positive_old_dual_residual', 'residual': str(residual[j])}
        else:
            assert provenance == {'kind': 'facial_sign_propagation', 'step': first_zero_step[j]}
    row_provenance = dict(closure['row_equality_provenance'])
    assert set(row_provenance) == E
    for i, source in row_provenance.items():
        if source['kind'] == 'positive_old_dual_row':
            assert i in lam and f(source['row_multiplier']) == lam[i]
        elif source['kind'] == 'opposite_original_rows':
            j = source['partner_row']
            assert i in expected_opposite_rows and j in expected_opposite_rows
            assert {k: f(a) for k, a in rows[i]} == {k: -f(a) for k, a in rows[j]}
        elif source['kind'] == 'forced_zero_by_original_negative_row':
            step = closure['proof_steps'][source['step']]
            assert step['original_row_index'] == i and all(j in Z for j, _ in rows[i])
        elif source['kind'] == 'all_support_columns_forced_zero':
            assert all(j in Z for j, _ in rows[i])
        else:
            raise AssertionError('Unrecognized row equality provenance')
    assert len(closure['proof_steps']) == 3384 and len(Z) == 9787 and len(E) == 6376
    print(json.dumps({'event': 'independent_facial_closure_pass', 'proof_steps': len(closure['proof_steps']),
                      'zero_columns': len(Z), 'equality_rows': len(E),
                      'seconds': time.monotonic() - started}), flush=True)

    # Independently reconstruct AP39 from literal histogram bits.
    C = [F()] * N
    histograms = [j for j, c in enumerate(matrix['columns']) if c['kind'] == 'hist']
    Xcols = [j for j, c in enumerate(matrix['columns']) if c['kind'] == 'common-X-mass']
    assert len(histograms) == len(Xcols) == 16
    for j in histograms:
        bits = list(map(int, matrix['columns'][j]['actual_bits']))
        b = bits[0] + bits[1]
        C[j] = (F(23, sum(bits)) if bits[2] else F()) - F(bits[5], b + 1)
    for j in Xcols:
        h = matrix['columns'][j]['hist_column']
        bits = list(map(int, matrix['columns'][h]['actual_bits']))
        b = bits[0] + bits[1]
        C[j] = -F(22, b + 4) + F(3 * bits[5], (b + 1) * (b + 4))
    encoded_C = [F()] * N
    for j, value in package['rows'][39]['row']:
        encoded_C[j] = f(value)
    assert encoded_C == C
    alpha = sum((a * b for a, b in zip(C, x)), F())
    assert alpha == f(identity['alpha']) == f(span['alpha']) < 0
    beta = {i: f(v) for i, v in identity['row_coefficients']}
    delta = {j: f(v) for j, v in identity['proven_zero_column_coefficients']}
    assert len(beta) == len(identity['row_coefficients']) == 223
    assert len(delta) == len(identity['proven_zero_column_coefficients']) == 5682
    assert set(beta).issubset(E) and set(delta).issubset(Z)
    combined = [alpha * a for a in norm]
    for i, weight in beta.items():
        for j, a in rows[i]:
            combined[j] += weight * f(a)
    for j, value in delta.items():
        combined[j] += value
    assert combined == C
    assert identity['strict_dual_bound_not_derived'] is True
    assert identity['new_equalities_not_treated_as_original_positive_dual_weights'] is True

    # Check that the quotient reduction did not discard an independent
    # equality: every omitted row differs from its representative only on Z.
    reps = span['retained_generator_rows']
    assert len(reps) == span['unknowns'] == 254
    assert len(set(reps)) == len(reps) and set(reps).issubset(E)
    assert span['known_zero_columns'] == sorted(Z)
    assert span['all_known_equality_rows'] == sorted(E)
    reduced_rows = span['generator_row_reductions']
    assert {r['row'] for r in reduced_rows} == E and len(reduced_rows) == len(E)
    for record in reduced_rows:
        i = record['row']
        projected = {j: f(a) for j, a in rows[i] if j not in Z}
        if record['kind'] == 'supported_on_proven_zero_columns':
            assert not projected
        elif record['kind'] == 'retained_generator':
            assert i in reps and projected
        elif record['kind'] == 'proportional_modulo_proven_zero_columns':
            k = record['representative']
            assert k in reps
            scale = f(record['scale'])
            assert projected == {j: scale * f(a) for j, a in rows[k] if j not in Z}
        else:
            raise AssertionError('Unknown quotient reduction')
    equations = span['all_unforced_column_equations']
    assert len(equations) == N - len(Z) == 11234
    assert {j for j, _ in equations} == set(range(N)) - Z
    expected_columns = {j: {} for j in range(N) if j not in Z}
    for k, i in enumerate(reps):
        for j, a in rows[i]:
            if j not in Z:
                expected_columns[j][k] = f(a)
    equations_by_column = {}
    for j, encoded in equations:
        expected = dict(expected_columns[j])
        rhs = C[j] - alpha * norm[j]
        if rhs:
            expected[len(reps)] = rhs
        assert expected == {k: f(v) for k, v in encoded}
        equations_by_column[j] = expected
    trace = read(HERE / 'expanded_elimination_trace.json.gz')
    prior_basis = {}
    for record in trace['basis']:
        current = dict(equations_by_column[record['input_column']])
        for p, text in record['reductions']:
            amount = f(text)
            assert p in prior_basis and current[p] == amount
            for k, value in prior_basis[p].items():
                result = current.get(k, F()) - amount * value
                if result:
                    current[k] = result
                else:
                    current.pop(k, None)
        p = record['pivot']
        assert p not in prior_basis and p == min(current)
        scale = f(record['normalization_scale'])
        assert current[p] == scale
        normalized = {k: value / scale for k, value in current.items()}
        assert normalized == {k: f(v) for k, v in record['normalized_augmented_equation']}
        prior_basis[p] = normalized
    assert len(prior_basis) == trace['rank'] == identity['rank'] == 254

    old_witness_columns = [20585, 20590, 20592, 20594, 20598]
    killed = [{'column': j, 'source': column_provenance[j]} for j in old_witness_columns if j in Z]
    assert killed
    support_sources = {
        'signed_row_coefficients': [{'row': i, 'coefficient': str(v), 'source': row_provenance[i]} for i, v in sorted(beta.items())],
        'signed_zero_column_coefficients': [{'column': j, 'coefficient': str(v), 'source': column_provenance[j]} for j, v in sorted(delta.items())],
    }
    write('identity_support_provenance.json.gz', support_sources)
    write('independent_full_checks.json.gz', {
        'old_primal_row_slacks_all22297': list(map(str, slacks)),
        'old_dual_residuals_all21021': list(map(str, residual)),
        'AP39_rebuilt_all21021': list(map(str, C)),
        'identity_reconstruction_all21021': list(map(str, combined)),
        'identity_differences_all21021': ['0'] * N,
        'final_forced_zero_columns': sorted(Z), 'final_proven_equality_rows': sorted(E),
        'old_five_column_obstruction_killed_coordinates': killed,
    })
    opposite_pair_count = sum(len(g['left_rows']) * len(g['right_rows']) for g in closure['all_exact_opposite_row_groups'] if not g['zero_row_group'])
    report = {
        'status': 'PASS_EXACT_WHOLE_W10_OPTIMUM_FACE_EXCLUDED_BY_AP39',
        'source_sha256': PINS, 'dimensions': [M, N],
        'old_primal_rows_reverified': M, 'old_dual_columns_reverified': N,
        'all_original_column_descriptors_preserved': N,
        'opposite_groups_independently_rebuilt': len(expected_groups),
        'exact_opposite_row_pairs': opposite_pair_count,
        'rows_in_global_opposite_pairs': len(expected_opposite_rows),
        'initial_equalities': len(E0), 'sign_proof_steps_replayed': len(closure['proof_steps']),
        'initial_forced_zero_columns': len(Z0), 'new_forced_zero_columns': len(Z - Z0),
        'final_forced_zero_columns': len(Z), 'final_proven_equality_rows': len(E),
        'closure_convergence_checked_on_all_rows': M,
        'original_five_column_obstruction_killed_coordinates': killed,
        'all16_histograms_retained': True,
        'zero_histogram_columns_retained': [1, 59, 366, 449, 524, 574],
        'displayed_primal_zeros_used_as_premises': False,
        'retained_equality_representatives': len(reps),
        'all_unforced_column_equations_rebuilt': len(equations),
        'basis_rows_replayed': len(prior_basis),
        'signed_identity_row_coefficients': len(beta),
        'signed_identity_forced_zero_coefficients': len(delta),
        'signed_identity_coefficients_verified': N,
        'old_W10': str(W), 'old_W10_float': float(W),
        'whole_W10_optimum_face_AP39_value': str(alpha),
        'whole_W10_optimum_face_AP39_value_float': float(alpha),
        'whole_W10_optimum_face_excluded_by_AP39': True,
        'strict_quantitative_lower_bound_derived': False,
        'original_dual_positive_weights_not_assumed_for_new_generators': True,
        'new_exact_optimum_claim': False, 'SPE_claim': False, 'optimizer_calls': 0,
        'closure_certificate_sha256': sha(HERE / 'closure_certificate.json.gz'),
        'expanded_identity_sha256': sha(HERE / 'expanded_signed_identity.json'),
        'verifier_sha256': sha(Path(__file__)),
        'seconds': time.monotonic() - started,
        'scope': 'Every W10-optimal point of the complete fixed16-hist common-X necessary LP violates AP39; no numerical bound for the appended system is certified here.'
    }
    write('independent_audit.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
