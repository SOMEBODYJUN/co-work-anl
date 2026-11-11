#!/usr/bin/env python3
"""Independent literal-client audit.  Does not import the row generator.

Enumerate every optimal incidence word, actual incidence word and X bit.
Compute the exchanged union directly by deleting labelled optimum slots;
then independently reconstruct every stored row on H=1,X=0/1 atoms.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
FINAL = WORK / 'common_x_joint_lp/final/exact_matrix.json.gz'
PIN = '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7'


def main():
    rows = json.loads((HERE / 'candidate_rows_and_certificates.json').read_text())
    evidence = json.loads((HERE / 'old_row_evidence.json').read_text())
    assert sha256(FINAL.read_bytes()).hexdigest() == PIN
    with gzip.open(FINAL, 'rt') as f:
        matrix = json.load(f)
    descriptors = {i: c for i, c in enumerate(matrix['columns']) if c['kind'] == 'hist'}
    xc = {c['hist_column']: i for i, c in enumerate(matrix['columns']) if c['kind'] == 'common-X-mass'}
    assert len(descriptors) == 16 and set(descriptors) == set(xc)
    assert matrix['normalization'] == ['1' if i in descriptors else '0' for i in range(21021)]
    old_rows = {r['row_index']: r['row'] for r in evidence['X_bounds']}
    for i, row in old_rows.items():
        assert row == matrix['rows'][i]
    del matrix

    # Each I denotes removed OCCURRENCE positions, not distinct labels.
    deletion_masks = {k: [sum(1 << i for i in I) for I in combinations(range(6), k)]
                      for k in range(1, 7)}
    literal, table = {}, []
    deletion_checks = 0
    for b in range(64):
        d = b.bit_count()
        for k in range(1, 7):
            for v in (0, 1):
                score = 0
                for removed in deletion_masks[k]:
                    old_covered = int(bool(b))
                    new_covered = int(bool(b & (63 ^ removed)) or bool(v))
                    score += old_covered - new_covered
                    deletion_checks += 1
                closed = (comb(6 - d, k - d) if 1 <= d <= k and not v else 0)
                if not d and v:
                    closed -= comb(6, k)
                assert score == closed
                literal[b, k, v] = score
    for d in range(7):
        b = (1 << d) - 1
        for k in range(1, 7):
            table.append({'d': d, 'k': k, 'outside_V_coefficient': literal[b, k, 0],
                          'inside_V_coefficient': literal[b, k, 1]})

    # All 64 optimal-bit words, 64 actual-bit words, two X values and all
    # 63 valid selections are tested; no restriction to the represented d=1.
    full_domain_checks = 0
    by_d = Counter()
    for b, actual, xbit, selection in product(range(64), range(64), (0, 1), range(63)):
        d = b.bit_count()
        selected_actual = bool(actual & selection)
        k = 1 + selection.bit_count()
        v = int(selected_actual or xbit)
        if d == 0:
            from_H_X = -comb(6, k) * (1 if selected_actual else xbit)
        elif d <= k and not selected_actual:
            from_H_X = comb(6 - d, k - d) * (1 - xbit)
        else:
            from_H_X = 0
        assert from_H_X == literal[b, k, v]
        full_domain_checks += 1
        by_d[d] += 1

    six_union_checks = 0
    for b, actual, xbit, omitted in product(range(64), range(64), (0, 1), range(7)):
        selected_actual_mask = 63 if omitted == 6 else 63 ^ (1 << omitted)
        actual_hit = bool(actual & selected_actual_mask)
        literal_union = actual_hit or (xbit if omitted != 6 else False)
        closed = int(bool(b)) - int(actual_hit) - int(omitted != 6 and not actual_hit) * xbit
        assert closed == int(bool(b)) - int(literal_union)
        six_union_checks += 1

    projected_checks = coefficient_checks = certificate_checks = 0
    for rec in rows['rows']:
        sparse = {i: Fraction(v) for i, v in rec['row']}
        rebuilt = {}
        for h, c in descriptors.items():
            actual = sum((ch == '1') << i for i, ch in enumerate(c['actual_bits']))
            b = (1 << c['d']) - 1
            values = []
            for xbit in (0, 1):
                actual_hit = bool(actual & rec['actual_mask'])
                if rec['family'] == 'averaged_k_exchange':
                    k = rec['new_label_slots']
                    v = int(actual_hit or xbit)
                    # Direct deletion sum, independent of closed-form coefficients.
                    value = sum(int(bool(b)) - int(bool(b & (63 ^ I)) or v)
                                for I in deletion_masks[k])
                else:
                    v = actual_hit or (xbit if rec['includes_X'] else False)
                    value = int(bool(b)) - int(v)
                assert sparse.get(h, 0) + xbit * sparse.get(xc[h], 0) == value
                values.append(value)
                projected_checks += 1
            if values[0]:
                rebuilt[h] = Fraction(values[0])
            if values[1] != values[0]:
                rebuilt[xc[h]] = Fraction(values[1] - values[0])
        # Equality as sparse maps checks all 21021 coordinates, including zeros.
        assert rebuilt == sparse
        coefficient_checks += 21021
        certified = {}
        for i, value in rec['old_row_multipliers']:
            q = Fraction(value)
            assert q > 0
            for j, a in old_rows[i]:
                certified[j] = certified.get(j, Fraction()) + q * Fraction(a)
        for j, value in rec['nonnegative_column_multipliers']:
            q = Fraction(value)
            assert q > 0
            certified[j] = certified.get(j, Fraction()) + q
        assert {j: a for j, a in certified.items() if a} == sparse
        certificate_checks += 1
    assert full_domain_checks == 516096
    assert six_union_checks == 57344
    assert projected_checks == 2240 and certificate_checks == 70
    # Invalid k=7 is not rescued by aliases being allowed: seven singleton
    # labels give a legal counterexample to a universal seven-union <= OPT6.
    seven_singletons = [{i} for i in range(7)]
    optimum6 = max(len(set().union(*(seven_singletons[i] for i in I)))
                  for I in combinations(range(7), 6))
    union7 = len(set().union(*seven_singletons))
    assert (optimum6, union7) == (6, 7)
    result = {
        'status': 'PASS_INDEPENDENT_LITERAL_CLIENT_AND_ALL70_CONIC_CERTIFICATES',
        'matrix_sha256': PIN,
        'candidate_package_sha256': sha256((HERE / 'candidate_rows_and_certificates.json').read_bytes()).hexdigest(),
        'independent_auditor_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'generator_imported': False, 'optimizer_calls': 0, 'point_files_read': 0,
        'literal_deleted_slot_comparisons': deletion_checks,
        'all_optimum_actual_X_selection_cases': full_domain_checks,
        'all_d_covered': list(range(7)), 'cases_by_d': dict(sorted(by_d.items())),
        'six_of_seven_literal_union_cases': six_union_checks,
        'projected_H1_X0_or_1_atoms': projected_checks,
        'full_coordinate_equalities_checked': coefficient_checks,
        'exact_nonnegative_certificates': certificate_checks,
        'generic_coefficient_table': table,
        'k7_exclusion_witness': {'seven_singleton_labels': 7, 'OPT6': optimum6, 'union_of_all7': union7},
        'zero_hist_and_X_zero_atoms_retained': True,
        'aliases_and_repeats': 'No distinctness assumption; deletion uses six indexed occurrence positions.',
    }
    target = HERE / 'literal_audit.json'
    assert not target.exists(), 'refuse overwrite'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'generic_coefficient_table'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
