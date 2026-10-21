"""Exact terminal-menu audit; no claim that a partial policy is a full SPE."""

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from customer_attraction.model import Instance


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


if __name__ == "__main__":
    print(json.dumps({"identity": "targeted terminal-menu mechanism audit",
                      "repeated_punisher": [repeated(r) for r in range(1, 7)],
                      "replicated_residual_old_group": old_group()},
                     ensure_ascii=False, indent=2))
