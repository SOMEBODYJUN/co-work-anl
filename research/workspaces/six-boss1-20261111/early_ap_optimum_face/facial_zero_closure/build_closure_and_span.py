"""Exact facial zero propagation and AP39 signed-span continuation.

Seeds are ONLY strict complementary slackness from the pinned exact dual
and exact opposite row pairs of the complete necessary matrix. No zero of
the displayed primal is used as a premise. All coordinates, including all
16 histograms and 420 old overlap auxiliaries, remain in the ambient space.

This standalone standard-library script never invokes an optimizer. Any
new equality/zero is accompanied by its derivation. A successful identity
does not treat those generators as positive weights in the original dual.
"""
from fractions import Fraction as Q
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


def write(name, obj):
    path = HERE / name
    if path.exists():
        raise FileExistsError(path)
    if path.suffix == '.gz':
        with path.open('xb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
                compressed.write((json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n').encode())
    else:
        with path.open('x') as stream:
            json.dump(obj, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


@lru_cache(maxsize=None)
def q(value):
    return Q(value)


def row_signature(encoded, sign=1):
    canonical = [[j, str(sign * q(value))] for j, value in sorted(encoded)]
    return sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()


def add_scaled(target, source, factor):
    for k, value in source.items():
        result = target.get(k, Q()) + factor * value
        if result:
            target[k] = result
        else:
            target.pop(k, None)


def reconstruct_annihilator(column, reductions, records):
    answer = {column: Q(1)}
    pending = {}
    for p, factor in reductions:
        pending[p] = pending.get(p, Q()) - factor
    for record in reversed(records):
        amount = pending.pop(record['pivot'], Q())
        if not amount:
            continue
        amount /= record['scale']
        add_scaled(answer, {record['column']: Q(1)}, amount)
        for p, factor in record['reductions']:
            pending[p] = pending.get(p, Q()) - amount * factor
    assert not any(pending.values())
    return answer


def main():
    started = time.monotonic()
    for name, expected in PINS.items():
        assert sha(WORK / name) == expected
    matrix = read(WORK / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz')
    dual = read(WORK / 'maxb_augmented_lp/full_lift/recovery/exact_dual_certificate.json')
    primal = read(WORK / 'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json')
    package = read(WORK / 'early_x_anchor_queries/rows_51.json')
    assert len(matrix['rows']) == M and len(matrix['columns']) == N
    rows = matrix['rows']
    lam = {i: q(v) for i, v in dual['row_multipliers']}
    residual = list(map(q, dual['residuals']))
    assert len(lam) == 463 and min(lam.values()) > 0
    assert len(residual) == N and min(residual) >= 0
    initial_zero = {j for j, value in enumerate(residual) if value > 0}
    assert len(initial_zero) == 5379
    positive = []
    negative = []
    hashes = []
    minus_hashes = []
    groups = {}
    for i, encoded in enumerate(rows):
        positive.append([j for j, a in encoded if q(a) > 0])
        negative.append([j for j, a in encoded if q(a) < 0])
        assert len(positive[-1]) + len(negative[-1]) == len(encoded)
        h = row_signature(encoded)
        nh = row_signature(encoded, -1)
        hashes.append(h)
        minus_hashes.append(nh)
        groups.setdefault(h, []).append(i)
    opposite_groups = []
    visited = set()
    opposite_rows = set()
    equality_source = {i: {'kind': 'positive_old_dual_row', 'row_multiplier': str(v)} for i, v in lam.items()}
    for i, h in enumerate(hashes):
        nh = minus_hashes[i]
        if h in visited or nh not in groups:
            continue
        left, right = groups[h], groups[nh]
        # Hashes are only an index: confirm all members by exact coefficients.
        left_rep = {j: q(a) for j, a in rows[left[0]]}
        right_rep = {j: q(a) for j, a in rows[right[0]]}
        assert left_rep == {j: -a for j, a in right_rep.items()}
        for k in left:
            assert {j: q(a) for j, a in rows[k]} == left_rep
        for k in right:
            assert {j: q(a) for j, a in rows[k]} == right_rep
        group_id = len(opposite_groups)
        opposite_groups.append({'group_id': group_id, 'left_rows': left,
                                'right_rows': right, 'zero_row_group': not left_rep,
                                'all_pairs_representation': 'Cartesian product of left_rows and right_rows; opposite coefficients checked exactly'})
        for k in left:
            opposite_rows.add(k)
            equality_source.setdefault(k, {'kind': 'opposite_original_rows', 'partner_row': right[0], 'group_id': group_id})
        for k in right:
            opposite_rows.add(k)
            equality_source.setdefault(k, {'kind': 'opposite_original_rows', 'partner_row': left[0], 'group_id': group_id})
        visited.update((h, nh))
    initial_equalities = set(lam) | opposite_rows
    known_zero = set(initial_zero)
    known_equalities = set(initial_equalities)
    column_sources = {j: {'kind': 'positive_old_dual_residual', 'residual': str(residual[j])} for j in initial_zero}
    steps = []
    rounds = []
    round_number = 0
    while True:
        round_number += 1
        before = len(known_zero)
        before_steps = len(steps)
        for i in range(M):
            pos = [j for j in positive[i] if j not in known_zero]
            neg = [j for j in negative[i] if j not in known_zero]
            if not pos and not neg:
                known_equalities.add(i)
                equality_source.setdefault(i, {'kind': 'all_support_columns_forced_zero'})
                continue
            reason = None
            if not pos and neg:
                reason = 'remaining_coefficients_strictly_negative_in_original_inequality'
                forced = neg
            elif i in known_equalities and pos and not neg:
                reason = 'remaining_coefficients_strictly_positive_in_proven_equality'
                forced = pos
            if reason is None:
                continue
            premises = [j for j, _ in rows[i] if j in known_zero]
            step_id = len(steps)
            step = {'step': step_id, 'round': round_number, 'rule': reason,
                    'original_row_index': i, 'original_row_name': matrix['row_names'][i],
                    'original_row': rows[i], 'known_zero_premise_columns': premises,
                    'new_forced_zero_columns': forced,
                    'conclusion_row_is_equality': True}
            if i in known_equalities:
                step['previous_row_equality_source'] = equality_source[i]
            steps.append(step)
            for j in forced:
                assert j not in known_zero
                known_zero.add(j)
                column_sources[j] = {'kind': 'facial_sign_propagation', 'step': step_id}
            known_equalities.add(i)
            equality_source.setdefault(i, {'kind': 'forced_zero_by_original_negative_row', 'step': step_id})
        rounds.append({'round': round_number, 'new_zero_columns': len(known_zero) - before,
                       'new_proof_steps': len(steps) - before_steps,
                       'known_zero_columns': len(known_zero)})
        print(json.dumps({'event': 'facial_closure_round', **rounds[-1], 'seconds': time.monotonic() - started}), flush=True)
        if len(known_zero) == before:
            break
    # Complete the equality list after the final newly forced coordinate.
    for i, encoded in enumerate(rows):
        if all(j in known_zero for j, _ in encoded):
            known_equalities.add(i)
            equality_source.setdefault(i, {'kind': 'all_support_columns_forced_zero'})
    assert all(column_sources[j]['kind'] != 'displayed_primal_zero' for j in known_zero)

    closure = {
        'status': 'EXACT_FACIAL_ZERO_CLOSURE', 'source_sha256': PINS,
        'initial_positive_dual_rows': sorted(lam),
        'initial_positive_residual_zero_columns': sorted(initial_zero),
        'all_exact_opposite_row_groups': opposite_groups,
        'opposite_row_count': len(opposite_rows),
        'initial_equality_rows': sorted(initial_equalities),
        'proof_steps': steps, 'rounds': rounds,
        'known_zero_columns': sorted(known_zero),
        'column_provenance': [[j, column_sources[j]] for j in sorted(known_zero)],
        'known_equality_rows': sorted(known_equalities),
        'row_equality_provenance': [[i, equality_source[i]] for i in sorted(known_equalities)],
        'ambient_column_count': N, 'rows_retained': M,
        'all16_histograms_retained': True, 'primal_support_zeros_used_as_premises': False,
        'meaning': 'Every listed equality and zero follows for every feasible point with objective W10.',
    }
    write('closure_certificate.json.gz', closure)

    # Equalities with equal projected rows modulo forced-zero coordinates are
    # the same generator in the quotient. Record every reduction explicitly.
    representatives = []
    projected_by_signature = {}
    reductions = []
    for i in sorted(known_equalities):
        projected = {j: q(a) for j, a in rows[i] if j not in known_zero}
        if not projected:
            reductions.append({'row': i, 'kind': 'supported_on_proven_zero_columns'})
            continue
        first = min(projected)
        scale = projected[first]
        signature = tuple((j, value / scale) for j, value in sorted(projected.items()))
        if signature in projected_by_signature:
            representative, representative_scale = projected_by_signature[signature]
            reductions.append({'row': i, 'kind': 'proportional_modulo_proven_zero_columns',
                               'representative': representative, 'scale': str(scale / representative_scale)})
        else:
            projected_by_signature[signature] = (i, scale)
            representatives.append(i)
            reductions.append({'row': i, 'kind': 'retained_generator'})
    normalization = list(map(q, matrix['normalization']))
    x = [q(c['weight']) for c in primal['columns']]
    ap = package['rows'][39]
    assert ap['name'] == ['common-X-early-arbitrary-anchor-AP', 3, 'A', 5]
    cut = {j: q(v) for j, v in ap['row']}
    alpha = sum((v * x[j] for j, v in cut.items()), Q())
    assert alpha < 0
    assert all(x[j] == 0 for j in known_zero)  # validation only, never a seed
    for i in known_equalities:
        assert sum((q(a) * x[j] for j, a in rows[i]), Q()) == 0
    unforced = [j for j in range(N) if j not in known_zero]
    unforced.sort(key=lambda j: (0 if j >= 20601 else 1 if j >= 4849 else 2, j))
    n = len(representatives)
    eq = {j: {} for j in unforced}
    for k, i in enumerate(representatives):
        for j, a in rows[i]:
            if j in eq:
                eq[j][k] = q(a)
    unique = []
    seen_equations = {}
    all_equations = []
    for j in unforced:
        encoded = dict(eq[j])
        rhs = cut.get(j, Q()) - alpha * normalization[j]
        if rhs:
            encoded[n] = rhs
        all_equations.append([j, [[k, str(v)] for k, v in sorted(encoded.items())]])
        if not encoded:
            continue
        scale = encoded[min(encoded)]
        signature = tuple((k, v / scale) for k, v in sorted(encoded.items()))
        if signature in seen_equations:
            continue
        seen_equations[signature] = j
        unique.append((j, encoded))
    write('expanded_span_inputs.json.gz', {
        'closure_certificate_sha256': sha(HERE / 'closure_certificate.json.gz'),
        'known_zero_columns': sorted(known_zero),
        'all_known_equality_rows': sorted(known_equalities),
        'generator_row_reductions': reductions,
        'retained_generator_rows': representatives, 'unknowns': n,
        'alpha': str(alpha), 'rhs_index': n,
        'all_unforced_column_equations': all_equations,
        'unique_equation_columns': [j for j, _ in unique],
        'all21021_ambient_coordinates_retained': True,
    })
    print(json.dumps({'event': 'expanded_span_start', 'known_zero_columns': len(known_zero),
                      'known_equalities': len(known_equalities), 'generator_rows': n,
                      'unforced_columns': len(unforced), 'unique_equations': len(unique),
                      'seconds': time.monotonic() - started}), flush=True)
    basis, records = {}, []
    failure = None
    last_log = time.monotonic()
    for processed, (j, encoded) in enumerate(unique, 1):
        current = dict(encoded)
        operations = []
        while current:
            pivot = min(current)
            if pivot == n:
                failure = (j, current[n], operations)
                break
            if pivot not in basis:
                scale = current[pivot]
                normalized = {k: v / scale for k, v in current.items()}
                basis[pivot] = normalized
                records.append({'pivot': pivot, 'column': j, 'scale': scale,
                                'reductions': operations, 'row': normalized})
                break
            factor = current[pivot]
            operations.append((pivot, factor))
            add_scaled(current, basis[pivot], -factor)
        if failure:
            break
        if time.monotonic() - last_log > 15:
            print(json.dumps({'event': 'expanded_span_progress', 'processed': processed,
                              'total': len(unique), 'rank': len(basis),
                              'seconds': time.monotonic() - started}), flush=True)
            last_log = time.monotonic()
    write('expanded_elimination_trace.json.gz', {
        'basis': [{'pivot': r['pivot'], 'input_column': r['column'],
                   'normalization_scale': str(r['scale']),
                   'reductions': [[p, str(v)] for p, v in r['reductions']],
                   'normalized_augmented_equation': [[k, str(v)] for k, v in sorted(r['row'].items())]}
                  for r in records],
        'rank': len(basis), 'processed_unique_equations': processed,
        'unique_equation_count': len(unique), 'unknowns': n,
    })
    common = {'closure_certificate_sha256': sha(HERE / 'closure_certificate.json.gz'),
              'source_sha256': PINS, 'alpha': str(alpha),
              'initial_zero_columns': len(initial_zero), 'final_zero_columns': len(known_zero),
              'initial_equality_rows': len(initial_equalities), 'final_equality_rows': len(known_equalities),
              'retained_generator_rows': n, 'rank': len(basis),
              'optimizer_calls': 0, 'primal_support_used_as_prior': False,
              'strict_dual_bound_not_derived': True,
              'new_equalities_not_treated_as_original_positive_dual_weights': True,
              'seconds': time.monotonic() - started}
    if failure:
        j, contradiction, operations = failure
        witness = reconstruct_annihilator(j, operations, records)
        assert set(witness).isdisjoint(known_zero)
        for i in known_equalities:
            assert sum((q(a) * witness.get(k, Q()) for k, a in rows[i]), Q()) == 0
        norm_value = sum((normalization[k] * v for k, v in witness.items()), Q())
        direction = [witness.get(k, Q()) - norm_value * x[k] for k in range(N)]
        assert sum((a * b for a, b in zip(normalization, direction)), Q()) == 0
        assert all(direction[k] == 0 for k in known_zero)
        for i in known_equalities:
            assert sum((q(a) * direction[k] for k, a in rows[i]), Q()) == 0
        change = sum((v * direction[k] for k, v in cut.items()), Q())
        assert change == contradiction != 0
        write('expanded_span_obstruction.json', {
            **common, 'status': 'EXACT_NOT_IN_FACIALLY_CLOSED_SIGNED_SPAN',
            'failed_column': j, 'nonzero_contradiction': str(contradiction),
            'column_annihilator': [[k, str(v)] for k, v in sorted(witness.items())],
            'annihilator_normalization_value': str(norm_value),
            'normalization_preserving_algebraic_direction': [[k, str(v)] for k, v in enumerate(direction) if v],
            'AP39_directional_change': str(change),
            'failure_reductions': [[p, str(v)] for p, v in operations],
            'processed_unique_equations': processed,
            'whole_optimum_face_feasibility': 'NOT_DECIDED',
            'direction_not_claimed_feasible': True,
            'finite_failed_proof_channel': 'Old positive dual equalities, every exact opposite-row equality, and full negative/same-sign zero closure.'
        })
        print(json.dumps({**common, 'status': 'EXACT_NOT_IN_FACIALLY_CLOSED_SIGNED_SPAN',
                          'witness_support': len(witness), 'direction_support': sum(bool(v) for v in direction),
                          'contradiction': str(contradiction)}), flush=True)
    else:
        solution = [Q()] * n
        for pivot in sorted(basis, reverse=True):
            encoded = basis[pivot]
            solution[pivot] = encoded.get(n, Q()) - sum((v * solution[k] for k, v in encoded.items() if pivot < k < n), Q())
        beta = {i: v for i, v in zip(representatives, solution) if v}
        delta = [cut.get(j, Q()) - alpha * normalization[j] for j in range(N)]
        for i, weight in beta.items():
            for j, a in rows[i]:
                delta[j] -= weight * q(a)
        assert all(value == 0 for j, value in enumerate(delta) if j not in known_zero)
        write('expanded_signed_identity.json', {
            **common, 'status': 'EXACT_WHOLE_W10_FACE_AP39_IDENTITY',
            'identity': 'AP39 = alpha*normalization + signed proven-face equalities + signed proven-zero coordinates',
            'row_coefficients': [[i, str(v)] for i, v in sorted(beta.items())],
            'proven_zero_column_coefficients': [[j, str(v)] for j, v in enumerate(delta) if v],
            'all21021_coefficients_checked': True,
            'whole_W10_optimum_face_AP39_value': str(alpha),
            'whole_W10_optimum_face_excluded_by_AP39': True,
            'strict_quantitative_improvement_requires_a_separate_positive_face_exposure_certificate': True,
        })
        print(json.dumps({**common, 'status': 'EXACT_WHOLE_W10_FACE_AP39_IDENTITY',
                          'row_coefficients': len(beta), 'zero_column_coefficients': sum(bool(v) for v in delta)}), flush=True)


if __name__ == '__main__':
    main()
