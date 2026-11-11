"""Independent literal checks for two-node facets and a three-node obstruction."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

states = list(product((0, 1), repeat=2))
for e, f in product(states, repeat=2):
    r, z = e
    R, Z = f
    s = -(r - R) * (z - Z)
    a, b, c, d = [int(e == st) for st in states]
    A, B, C, D = [int(f == st) for st in states]
    facets = [b+c, B+C, b+B, c+C, b+c+d-D, B+C+D-d]
    assert all(s <= bound for bound in facets)

odd_sets = [mask for mask in range(64) if mask.bit_count() % 2]
for bits in product((0, 1), repeat=6):
    rs, zs = bits[:3], bits[3:]
    own = [rs[i] != zs[i] for i in range(3)]
    cross = [rs[i] != zs[(i+1) % 3] for i in range(3)]
    edges = own + cross
    s = sum(rs[i] * (zs[(i+1) % 3] - zs[i]) for i in range(3))
    assert 2*s == sum(own) - sum(cross)
    assert s <= 1
    for mask in odd_sets:
        lhs = sum((1 if mask >> i & 1 else -1) * edges[i] for i in range(6))
        assert lhs <= mask.bit_count() - 1

def slack(atom, i, j):
    return F(atom[i][1] - atom[j][1], 1 + atom[i][0])

deterministic = [tuple((1, 1) if i == k else (0, 0) for i in range(3))
                 for k in range(3)]
pair_certificates = []
for i in range(3):
    for j in range(i+1, 3):
        first = [(0, 1)] * 3
        second = [(1, 0)] * 3
        first[j], second[j] = (1, 0), (0, 1)
        # i retains 01 then 10. The uninvolved node also has its prescribed marginal.
        q_atoms = [tuple(first), tuple(second)]
        for k in range(3):
            assert sorted(atom[k] for atom in q_atoms) == [(0, 1), (1, 0)]
        atoms = deterministic + q_atoms
        values = [sum((slack(atom, u, v) for atom in atoms), F())
                  for u, v in ((i, j), (j, i))]
        assert values == [0, 0]
        pair_certificates.append({"pair": [i+1, j+1],
                                  "Q_atoms": q_atoms,
                                  "two_true_IC_slacks": list(map(str, values))})

deterministic_cycle = sum((sum((slack(atom, i, (i+1) % 3)
                               for i in range(3)), F())
                           for atom in deterministic), F())
assert deterministic_cycle == -F(3, 2)
q_max_per_customer = max(sum((slack(tuple((1-z, z) for z in zz), i, (i+1) % 3)
                             for i in range(3)), F())
                         for zz in product((0, 1), repeat=3))
assert q_max_per_customer == F(1, 2)
assert deterministic_cycle + 2*q_max_per_customer == -F(1, 2)
out = {
    "scope": "literal finite verification supplement; transport formulas have separate analytic proofs; not an SPE counterexample",
    "six_dual_facets_all_16_literal_state_pairs": True,
    "all_32_odd_sets_on_all_64_binary_assignments": True,
    "pair_completions": pair_certificates,
    "three_deterministic_blocks_cycle_slack": str(deterministic_cycle),
    "Q_maximum_cycle_slack_per_customer": str(q_max_per_customer),
    "Q_mass": "2",
    "full_three_cycle_strict_upper": "-1/2",
}
path = Path(__file__).with_name("main_verify_rz_cycles.json")
path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out, ensure_ascii=False))
