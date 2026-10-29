"""Independently replay the five-player universal rational upper certificate.

This checker imports only Python's standard library.  It reads the frozen
certificate but independently rebuilds every raw coefficient from three path
strings; it does not import the discovery LP, its row generator, or a game/SPE
solver.  The universal proof also requires the manuscript's row-legality
arguments; finite arithmetic replay alone is not a proof of those arguments.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "evidence/certificates/customer_attraction/five_player_bound.json"
LABELS = tuple("ABCDEUVWXY")
PATHS = {"actual": tuple("ABCDE"),
         "second": tuple("AEUVW"),
         "third": tuple("ABEXY")}


def raw_coefficient(pattern, name):
    """Return one customer's coefficient and the separate OPT coefficient."""
    bit = dict(zip(LABELS, pattern))

    def share(path, position):
        numerator = bit[path[position]]
        return (Q(numerator, sum(bit[theme] for theme in path))
                if numerator else Q(0))

    if name.startswith("F:"):
        if len(name.split(":")) != 2:
            raise AssertionError("invalid genuine deviation row")
        branch = name.split(":")[1]
        if branch not in ("second", "third"):
            raise AssertionError("unknown genuine deviation branch")
        position = 1 if branch == "second" else 2
        return (share(PATHS["actual"], position)
                - share(PATHS[branch], position), Q(0))

    parts = name.split(":")
    path = PATHS[parts[0]]
    if parts[1] == "r2":
        if parts[2:] != ["O"]:
            raise AssertionError("unexpected two-player row")
        prefix_load = sum(bit[theme] for theme in path[:3])
        first_remaining_bit = bit[path[3]]
        two_player_budget = (share(path, 3) + share(path, 4)
                             + Q(first_remaining_bit,
                                 (prefix_load + 1) * (prefix_load + 2)))
        return (Q(5, 2) * two_player_budget
                + Q(prefix_load, prefix_load + 1), Q(-1))

    position = int(parts[1]) - 1
    if position not in range(5):
        raise AssertionError("invalid player position")
    if position < {"actual": 0, "second": 2, "third": 3}[parts[0]]:
        raise AssertionError("a forced-deviation mover is not a local optimizer")
    prefix_load = sum(bit[theme] for theme in path[:position])
    remaining = 5 - position
    actual_payoff = share(path, position)
    if parts[2] == "K":
        if len(parts) != 4:
            raise AssertionError("invalid topic-comparison row")
        return (actual_payoff - Q(bit[parts[3]], prefix_load + remaining), Q(0))
    if parts[2:] != ["O"]:
        raise AssertionError("unknown optimal-coverage row")
    return (5 * remaining * actual_payoff
            + Q(prefix_load, prefix_load + remaining), Q(-1))


def audit():
    certificate_bytes = CERTIFICATE.read_bytes()
    data = json.loads(certificate_bytes)
    if data["labels"] != list(LABELS):
        raise AssertionError("certificate membership order changed")
    expected_paths = {name: [LABELS.index(theme) for theme in path]
                      for name, path in PATHS.items()}
    if data["paths"] != expected_paths:
        raise AssertionError("certificate genuine branch paths changed")
    multipliers = {name: Q(value) for name, value in data["multipliers"].items()}
    bound = Q(data["bound"])
    if any(value < 0 for value in multipliers.values()):
        raise AssertionError("negative multiplier")

    optimal_coefficient = sum((weight * raw_coefficient((0,) * 10, name)[1]
                               for name, weight in multipliers.items()), Q(0))
    if optimal_coefficient != -1:
        raise AssertionError("aggregate OPT coefficient is not exactly -1")

    residuals = []
    for index, pattern in enumerate(product((0, 1), repeat=10)):
        coverage = int(any(pattern[:5]))
        residual = bound * coverage - sum(
            (weight * raw_coefficient(pattern, name)[0]
             for name, weight in multipliers.items()), Q(0))
        if residual < 0:
            raise AssertionError(("negative raw residual", pattern, residual))
        if residual != Q(data["residuals"][index]):
            raise AssertionError(("saved raw residual disagrees", pattern, residual))
        residuals.append(residual)
    if len(data["residuals"]) != len(residuals):
        raise AssertionError("saved residual count disagrees")
    rounded_bound = Q(221, 100)
    if not bound < rounded_bound:
        raise AssertionError("exact bound does not improve 221/100")

    return {
        "audit": "customer_attraction_five_player_independent",
        "scope": "Independent exact arithmetic replay of the universal five-player certificate; manuscript supplies row legality",
        "arithmetic": "fractions.Fraction; no LP, game solver, or shared row-generator imports",
        "nonnegative_multipliers": len(multipliers),
        "OPT_coefficient": str(optimal_coefficient),
        "membership_patterns": len(residuals),
        "minimum_residual": str(min(residuals)),
        "maximum_residual": str(max(residuals)),
        "zero_residual_patterns": sum(value == 0 for value in residuals),
        "exact_bound": str(bound),
        "rounded_bound": str(rounded_bound),
        "rounding_up_gap": str(rounded_bound - bound),
        "all_saved_residuals_independently_match": True,
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "independent_audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional fresh audit report")
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError("refusing to overwrite an existing report")
    report = audit()
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
