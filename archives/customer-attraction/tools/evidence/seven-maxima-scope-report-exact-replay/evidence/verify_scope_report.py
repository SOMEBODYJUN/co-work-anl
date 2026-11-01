"""Informed independent exact algebra for the eight-field R566 scope report.

No author checker import, LP, game search, or SPE enumeration. The algebra is
reconstructed from the printed M/L/T inequalities, on their expanded literal
column domain. A separate runner may replay the unmodified author entry point.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
B = (Q(1, 21), Q(2, 37), Q(1, 16), Q(2, 27))
LAM = (Q(207, 355), Q(417, 710), Q(253, 426), Q(133, 213))


def remainder(incidence, early, omit_private=False):
    member = [bool(early & (1 << t)) for t in range(5)]
    member.append(bool(incidence & 1))  # actual final action is B_0
    load = sum(member)
    share = [Q(int(v), load) if load else Q(0) for v in member]
    linear = sum(LAM[t] * (share[t] - B[t]) for t in range(4))
    for j in range(1, 7):
        final_br = share[5] - Q(int(bool(incidence & (1 << j))), sum(member[:5]) + 1)
        multiplicity = int(bool(incidence & 1)) + int(bool(incidence & (1 << j)))
        background = sum(member[:4])
        tax = share[4] + share[5] + Q(int(member[4]), (background + 1) * (background + 2))
        if multiplicity:
            tax -= Q(multiplicity, background + multiplicity)
        linear += Q(8, 71) * final_br + Q(7, 71) * tax
    target = Q(int(load > 0)) - (Q(0) if omit_private and incidence == 64 else Q(1, 2))
    return target - linear, sum((1 << t) for t in range(6) if member[t])


def scan(incidences, omit_private=False):
    values = [(r, i, e, j) for i in incidences for e in range(32)
              for r, j in [remainder(i, e, omit_private)]]
    low = min(r for r, _, _, _ in values)
    def point(entry):
        r, i, e, j = entry
        return dict(I=i, E=e, J=j, residual=str(r))
    return dict(columns=len(values), minimum=str(low),
                minimizers=[point(v) for v in values if v[0] == low],
                negative_columns=[point(v) for v in values if v[0] < 0])


def main():
    original = json.loads((ROOT / 'original/dense_seven_scope_audit.json').read_text())
    dense_incidences = [i for i in range(1, 128) if i.bit_count() >= 2]
    dense = scan(dense_incidences)
    singleton6 = scan([64])
    singleton0 = scan([1])
    author_target = scan(dense_incidences + [64], omit_private=True)
    catalog = [set(range(6)), {0, 6}, {1, 6}, {2, 6}, {3, 6}, {4, 6}, {5, 6, 7}]
    universe = set(range(8))
    assert set.union(*catalog) == universe
    assert all(not (a <= b) for i, a in enumerate(catalog) for j, b in enumerate(catalog) if i != j)
    six_union = [(list(c), len(set.union(*(catalog[i] for i in c)))) for c in combinations(range(7), 6)]
    omit_sizes = [len(set.union(*(catalog[i] for i in range(7) if i != j))) for j in range(7)]
    private = [sorted(a - set.union(*(catalog[j] for j in range(7) if j != i))) for i, a in enumerate(catalog)]
    reconstructed = dict(dense_complete_columns=dense['columns'], dense_minimum=dense['minimum'],
                         singleton6_full_union_minimum=singleton6['minimum'],
                         seven_distinct_maximal_sets=[sorted(a) for a in catalog], unit_customers=len(universe),
                         OPT6=max(v for _, v in six_union), omit_the_only_private_maximum=omit_sizes[6],
                         counterexample_scope='coverage identity only; no SPE welfare claim')
    assert reconstructed == original
    assert author_target['columns'] == 3872 and author_target['minimum'] == dense['minimum']
    assert not dense['negative_columns'] and not author_target['negative_columns']
    assert len(singleton6['negative_columns']) == len(singleton0['negative_columns']) == 2
    assert singleton0['minimum'] == '-7905391/238321440'
    assert private == [[], [], [], [], [], [], [7]]
    assert omit_sizes == [8, 8, 8, 8, 8, 8, 7]
    # Valid static fractional cover for this one example, no strategy assumption.
    assert catalog[0] | catalog[6] == universe
    # Clients 0 and 7 lie in disjoint families of themes. Dual prices 1,1 give
    # a matching lower bound 2; hence the example has fractional cover number 2.
    assert all(int(0 in a) + int(7 in a) <= 1 for a in catalog)
    out = dict(kind='informed-independent-literal-coefficient-and-static-coverage-reconstruction',
               primary_id='62a4ee078e306dfcde6d', original_report_field_count=len(original),
               reconstructed_original_report=reconstructed, all_original_fields_equal=True,
               dense=dense, singleton6_true_full_union_target=singleton6,
               singleton0_true_full_union_target=singleton0, author_modified_target=author_target,
               six_distinct_theme_union_sizes=[dict(themes=c, coverage=v) for c, v in six_union],
               omitted_maximum_union_sizes=omit_sizes, private_blocks=private,
               example_fractional_cover_number='2',
               sum_positive_mixed_weights_times_B=str(sum(a*b for a,b in zip(LAM,B))),
               private_suffix_coefficient='1/12', positive_M_rows_private_weakening_valid=all(v <= Q(1,12) for v in B),
               source_checker_imports=0, LP_runs=0, SPE_strategy_audits=0,
               full_SPE_or_welfare_counterexample_claim=False,
               implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               original_report_sha256=hashlib.sha256((ROOT / 'original/dense_seven_scope_audit.json').read_bytes()).hexdigest())
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
