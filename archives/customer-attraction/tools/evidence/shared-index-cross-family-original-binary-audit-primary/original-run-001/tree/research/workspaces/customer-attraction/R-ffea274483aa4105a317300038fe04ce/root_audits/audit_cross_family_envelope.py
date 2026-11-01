"""Independent exact audit of one cross-family necessary last-player row.

No importing the discoverer's code or LP solver. Enumerate all binary
assignments compatible with each atom's shared optimal-theme incidence.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
original_path = ROOT / "evidence/certificates/customer_attraction/five_player_indexed_bound.json"
after_path = ROOT / "research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.json"
original = json.loads(original_path.read_text())
after = json.loads(after_path.read_text())
triples = tuple(product((0, 1), repeat=3))
quads = tuple(product((0, 1), repeat=4))
coefficients = []
assignments = 0
for atom in original["primal"]["atoms"]:
    # At the AB-branch terminal node (A,B,T_i,R_i), the chosen last action
    # is S_i. For a customer, its denominator is a+b+t_i+r_i+1.
    a, b = map(int, atom["bits"][:2])
    entries = []
    chosen = F(0)
    for multiplicity, (t, r, s) in zip(atom["AB_hist"], triples):
        denominator = a + b + t + r + 1
        entries.extend([(t, F(1, denominator))] * multiplicity)
        chosen += F(multiplicity * s, denominator)
    assert len(entries) == 5
    I_counts = tuple(sum(n * bits[2] for n, bits in zip(atom["second_hist"], quads)
                         if bits[0] == t) for t in (0, 1))
    assert sum(t == 0 for t, _ in entries) >= I_counts[0]
    assert sum(t == 1 for t, _ in entries) >= I_counts[1]
    products = []
    for flags in product((0, 1), repeat=5):
        if tuple(sum(flag for flag, (label, _) in zip(flags, entries) if label == t)
                 for t in (0, 1)) != I_counts:
            continue
        diagonal = sum((flag * inverse for flag, (_, inverse) in zip(flags, entries)), F(0))
        products.append(diagonal)
        assignments += 1
    maximum = max(products)
    rearranged = sum((sum(sorted((v for label, v in entries if label == t), reverse=True)
                           [:I_counts[t]], F(0)) for t in (0, 1)), F(0))
    assert maximum == rearranged
    total_inverse = sum((inverse for _, inverse in entries), F(0))
    count = sum(I_counts)
    for diagonal in products:
        off_diagonal = count * total_inverse - diagonal
        # The minimum possible cross-index deviation sum is achieved at
        # the largest admissible diagonal matching term.
        assert off_diagonal >= count * total_inverse - maximum
    coefficients.append(4 * chosen - count * total_inverse + maximum)

weight_sets = {
    "original_437": [F(atom["mass_numerator"], original["primal"]["denominator"])
                      for atom in original["primal"]["atoms"]],
    "reweighted_447": list(map(F, after["exact_reweighting"]))}
slacks = {name: sum((w * c for w, c in zip(weights, coefficients)), F(0))
          for name, weights in weight_sets.items()}
assert all(value < 0 for value in slacks.values())
out = {"scope": "One necessary cross-family AB:last-S versus second:I off-diagonal envelope, on frozen atom support",
       "source_original": str(original_path.relative_to(ROOT)),
       "source_reweighted": str(after_path.relative_to(ROOT)),
       "atoms": len(coefficients), "compatible_binary_assignments": assignments,
       "exact_slacks": {key: str(value) for key, value in slacks.items()},
       "conclusions": ["Both frozen points fail this necessary condition",
                       "The minimum-of-offdiagonal bound is exact given the t/I marginal",
                       "No universal bound for the enlarged LP or SPE follows from these checks"]}
(HERE / "cross_family_envelope_independent_audit.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
