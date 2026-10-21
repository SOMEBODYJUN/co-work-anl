"""Exact terminal-menu audit; no claim that a partial policy is a full SPE."""

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def repeated(r: int) -> dict:
    # k=1 suffices to expose the last-node contradiction. The analytic note
    # permits arbitrary k and arbitrary overlapping reward sets.
    x = {f"x{i}" for i in range(12)}
    a = {"a"}
    b = {f"b{i}" for i in range(12)}
    d = {f"d{i}" for i in range(6 * r)}
    inst = Instance.from_topic_sets((x, x | a, x | b, b | d), r + 1,
                                   ("C", "A", "B", "D"))
    actual = (0,) + (3,) * r
    actual_dev = (0,) + (3,) * (r - 1) + (2,)
    penalty = (1,) + (2,) * r
    penalty_dev = (1,) + (2,) * (r - 1) + (3,)
    actual_u = inst.player_payoffs(actual)[-1]
    actual_dev_u = inst.player_payoffs(actual_dev)[-1]
    penalty_u = inst.player_payoffs(penalty)[-1]
    penalty_dev_u = inst.player_payoffs(penalty_dev)[-1]
    assert actual_u == actual_dev_u
    assert penalty_dev_u - penalty_u == Fraction(6 * r) - Fraction(12, r + 1)
    assert (penalty_dev_u > penalty_u) == (r >= 2)
    return {"r": r, "actual_last": str(actual_u),
            "actual_deviation_B": str(actual_dev_u),
            "penalty_last": str(penalty_u),
            "penalty_deviation_D": str(penalty_dev_u),
            "penalty_strictly_invalid": penalty_dev_u > penalty_u}


def old_group() -> dict:
    blocks = [{f"{s}{i}" for i in range(n)}
              for s, n in (("X0", 2), ("Y0", 2), ("V0", 2), ("P0", 3),
                           ("X1", 2), ("Y1", 2), ("V1", 2), ("P1", 3),
                           ("Z", 2), ("Q", 3))]
    x0, y0, v0, p0, x1, y1, v1, p1, z, q = blocks
    inst = Instance.from_topic_sets((x0 | y0, p0 | v0, x1 | z | v1,
                                    y1 | z | v1, q | z), 3,
                                   ("A0", "T0", "D1", "E1", "B"))
    intended = inst.player_payoffs((0, 2, 3))[-1]
    dev = inst.player_payoffs((0, 2, 1))[-1]
    assert intended == 4 and dev == 5
    return {"old_group_intended_E1": str(intended),
            "old_group_deviation_T0": str(dev),
            "strictly_invalid": dev > intended}


def mixed_tail_full_spe() -> dict:
    # The obstruction concerns repeated B_i only. A mixed B_i/D response
    # really can work, so independently verify a complete countercheck.
    xs = [{f"x{i}_{j}" for j in range(2)} for i in range(3)]
    aa = [{f"a{i}"} for i in range(3)]
    b, d = {"b0", "b1"}, {"d0", "d1"}
    covers, labels = [], []
    for i in range(3):
        covers.extend((xs[i], xs[i] | aa[i], xs[i] | b))
        labels.extend((f"C{i}", f"A{i}", f"B{i}"))
    covers.append(b | d)
    labels.append("D")
    inst = Instance.from_topic_sets(covers, 5, labels)
    solver = ExactSPESolver(inst)
    path = (0, 3, 6, 9, 9)
    certificate = solver.certificate(on_path=path)
    check = verify_certificate(inst, certificate)
    assert check.valid
    assert inst.welfare(check.terminal_counts) == 10
    assert inst.optimal_welfare() == 13
    return {"identity": "complete SPE showing the obstruction is specific",
            "path": [inst.topics[a] for a in path],
            "welfare": inst.welfare(check.terminal_counts),
            "optimum": inst.optimal_welfare(),
            "checked_histories": check.checked_histories,
            "checked_deviations": check.checked_deviations,
            "valid": check.valid}


def directed_scan() -> dict:
    found, checked = [], 0
    pref = (1, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    target = (1, 0, 0, 1, 0, 0, 1, 0, 0, 2)
    for x in (2, 4):
        for a in range(1, 2 * x + 1):
            for b in range(4 * x + 1):
                for d in range(x, 4 * x + 1):
                    if b + d < x + 2 * a:
                        continue
                    types = []
                    for i in range(3):
                        types.append(CustomerType(frozenset((3 * i, 3 * i + 1,
                                                             3 * i + 2)), x))
                        types.append(CustomerType(frozenset((3 * i + 1,)), a))
                    if b:
                        types.append(CustomerType(frozenset((2, 5, 8, 9)), b))
                    types.append(CustomerType(frozenset((9,)), d))
                    instance = Instance(tuple(str(i) for i in range(10)),
                                        tuple(types), 5)
                    checked += 1
                    if target in ExactSPESolver(instance).outcomes(pref):
                        found.append([x, a, b, d])
    return {"identity": "finite partial-subgame scan; not a general theorem",
            "checked": checked, "feasible_parameters": found,
            "coordinate_order": ["x", "a", "b", "d"]}


if __name__ == "__main__":
    result = {"identity": "targeted terminal-menu mechanism audit",
              "repeated_punisher": [repeated(r) for r in range(1, 7)],
              "replicated_residual_old_group": old_group(),
              "mixed_tail_full_spe": mixed_tail_full_spe()}
    if "--scan" in sys.argv:
        result["directed_scan"] = directed_scan()
    print(json.dumps(result, ensure_ascii=False, indent=2))
