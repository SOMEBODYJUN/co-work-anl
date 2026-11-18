"""Verify the 49/10 certificate with exact arithmetic and no optimizer."""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path

TAU = Fraction(49, 10)
BRANCHES = {(0, 6), (1, 6), (2, 6), (2, 4), (3, 5)}


def shares(actions):
    total = sum(actions)
    return [Fraction(chosen, total) if total else Fraction(0) for chosen in actions]


def contribution(names, actions, catalog, target, maximum,
                 actual_shares=None, source=None):
    payoff = shares(actions)
    subtotal = Fraction(0)
    for name, multiplier in names.items():
        if name == "R1/2":
            prefix = sum(actions[:4])
            value = (TAU*payoff[4] + payoff[5]/2
                     - Fraction(target, prefix+1)
                     + Fraction(target*actions[4]*(prefix == 0), 4))
        elif name.startswith("F"):
            i = int(name[1:])
            value = TAU*payoff[i] - Fraction(target, sum(actions[:i])+6-i)
        elif name.startswith("H"):
            i, j = map(int, name[1:].split("-"))
            value = payoff[i] - Fraction(catalog[j], sum(actions[:i])+6-i)
        elif name.startswith("CAP"):
            j = int(name[3:])
            value = maximum - (catalog[j] if source is None else catalog[7+j])
        elif name == "IC-own":
            value = actual_shares[source] - payoff[source]
        else:
            raise ValueError(f"Unknown proof row: {name}")
        subtotal += multiplier*value
    return subtotal


def verify():
    data = json.loads(Path(__file__).with_name("anchor-menu-49-10-certificate.json").read_text())
    weights = {group: {key: Fraction(value) for key, value in rows.items()}
               for group, rows in data["weights"].items()}
    if any(v <= 0 for rows in weights.values() for v in rows.values()):
        raise ValueError("All stored multipliers must be positive")
    coefficient = Fraction(data["coverage_coefficient"])
    if (Fraction(data["tau"]) != TAU or coefficient <= Fraction(1, 2)
            or coefficient*Fraction(data["opt_over_welfare_bound"]) != 1):
        raise ValueError("Coverage coefficient does not establish the stated guarantee")
    actual_rows = weights.pop("actual")
    branches = [(tuple(map(int, key.split(":"))), group) for key, group in weights.items()]
    if {key for key, _ in branches} != BRANCHES:
        raise ValueError("Unexpected branch identity")
    residues = []
    local_types = 0
    for anchor, member in product(product((0, 1), repeat=7), (0, 1)):
        actual = anchor[:6]
        maximum = anchor[6]
        actual_shares = shares(actual)
        total = contribution(actual_rows, actual, anchor, member, maximum)
        for (source, label), branch_weights in branches:
            scores = []
            for tail in product((0, 1), repeat=5-source):
                actions = actual[:source] + (anchor[label],) + tail
                scores.append(contribution(branch_weights, actions, anchor+tail, member,
                                           maximum, actual_shares, source))
                local_types += 1
            total += max(scores)
        residual = int(any(actual)) - coefficient*member - total
        if residual < 0:
            raise ValueError(f"Negative residual at {anchor}, {member}: {residual}")
        residues.append(residual)
    zero_count = sum(q == 0 for q in residues)
    if zero_count != data["zero_anchors"]:
        raise ValueError("Zero residual count changed")
    return {"tau": data["tau"], "welfare_per_covered_target": str(coefficient),
            "upper_factor": data["opt_over_welfare_bound"], "anchor_types": len(residues),
            "local_branch_types": local_types, "minimum_residual": str(min(residues)),
            "zero_anchors": zero_count,
            "positive_multipliers": sum(map(len, data["weights"].values()))}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
