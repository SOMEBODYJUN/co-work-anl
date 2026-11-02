"""Independent exact coefficient audit; never imports the discovery program.

Input is the saved rational multiplier list.  All path payoffs, source IC,
safe queries, last-player queries and two-player-tax rows are rebuilt here.
The validity of the rows for arbitrary SPE follows from their definitions;
this audit exhausts the finite Boolean domain of their coefficient identity.
"""
import argparse
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

F = Fraction
BASE = Path(__file__).resolve().parent
LABELS = tuple("ZTABCDQRSXY")
BRANCHES = {"actual": tuple("TABCD"), "root": tuple("TDQRS"),
            "second": tuple("TADXY")}
FIRST_OPTIMIZER = {"actual": 1, "root": 2, "second": 3}


def share(numerator, denominator):
    if numerator == 0:
        return F(0)
    assert denominator > 0
    return F(numerator, denominator)


def payoff(member, branch, position):
    path = BRANCHES[branch]
    return share(member[path[position]], member["Z"] + sum(member[t] for t in path))


def slack(member, optimum_bit, name):
    parts = name.split(":")
    if parts[0] == "CAP":
        assert parts[1] != "T" and parts[1] in LABELS
        return F(member["T"] - member[parts[1]])
    if parts[0] == "copy":
        branch = parts[1]
        position = {"root": 1, "second": 2}[branch]
        return payoff(member, "actual", position) - payoff(member, branch, position)
    branch, kind = parts[:2]
    path = BRANCHES[branch]
    if kind.isdigit():
        # Author's indices start at the A/D position, after forced T.
        position = int(kind) + 1
        assert FIRST_OPTIMIZER[branch] <= position <= 4
        assert parts[2] == "floor" and parts[3] in LABELS
        old_load = member["Z"] + sum(member[t] for t in path[:position])
        return payoff(member, branch, position) - share(member[parts[3]], old_load + 5 - position)
    if kind == "lastO":
        old_load = member["Z"] + sum(member[t] for t in path[:4])
        return 6 * payoff(member, branch, 4) + share(old_load, old_load + 1) - optimum_bit
    assert kind == "pairO"
    old_load = member["Z"] + sum(member[t] for t in path[:3])
    tax = share(member[path[3]], (old_load + 1) * (old_load + 2))
    pair_budget = payoff(member, branch, 3) + payoff(member, branch, 4) + tax
    return 3 * pair_budget + share(old_load, old_load + 1) - optimum_bit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=BASE / "research_1/background_maxroot_certificate.json")
    args = parser.parse_args()
    saved = json.loads(args.certificate.read_text())
    B, C = F(saved["B"]), F(saved["C"])
    weights = {name: F(value) for name, value in saved["multipliers"].items()}
    assert B > 0 and C == -7 and all(weight > 0 for weight in weights.values())
    assert saved["M"] == 6
    assert sum(weight for name, weight in weights.items() if name.endswith("O")) == 1
    minimum = None
    checked = 0
    zeros = 0
    background_minima = {0: None, 1: None}
    for bits in product((0, 1), repeat=len(LABELS)):
        member = dict(zip(LABELS, bits))
        maximum_deviator = payoff(member, "actual", 0)
        residuals = []
        for optimum_bit in (0, 1):
            residue = B * maximum_deviator + C * member["T"] - optimum_bit
            residue -= sum(weight * slack(member, optimum_bit, name)
                           for name, weight in weights.items())
            assert residue >= 0, (member, optimum_bit, residue)
            residuals.append(residue)
            minimum = residue if minimum is None else min(minimum, residue)
            z = member["Z"]
            background_minima[z] = residue if background_minima[z] is None else min(background_minima[z], residue)
            zeros += residue == 0
            checked += 1
        assert residuals[0] == residuals[1]
    assert checked == 4096 and len(weights) == 25
    print(json.dumps({"status": "passed", "states": checked,
                      "positive_multipliers": len(weights), "B": str(B), "C": str(C),
                      "minimum_residual": str(minimum), "zero_residual_states": zeros,
                      "minimum_by_background_bit": {str(k): str(v) for k, v in background_minima.items()},
                      "comparison_bit_eliminated": True,
                      "imports_discovery_code": False}, indent=2))


if __name__ == "__main__":
    main()
