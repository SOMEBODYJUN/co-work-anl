#!/usr/bin/env python3
"""Reproducible exact arithmetic checks of the new shared-catalog algorithm."""
from fractions import Fraction as Q
from random import Random
import json
import argparse
from pathlib import Path
from facility_spe.shared_phi import menu, solve, verify, serial


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="write a new report; default leaves recorded evidence untouched")
    args = parser.parse_args(argv)
    rng = Random(2026093001)
    counts = {}
    maximum = Q(1)
    examples = [
        {"weights": [], "locations": [[], []]},
        {"weights": [1], "locations": [[0]]},
        {"weights": [1000, 1, 1008, 1002, 10, 6],
         "locations": [[0, 1, 2], [0, 1, 3, 4], [0, 2, 3, 5], [1, 2, 3]]},
    ]
    # This strong chord requires three genuine mixers to meet both quotas.
    special = menu(Q(40), Q(39), [Q(20)]*3)
    chord = [e for e in special if e["family"].startswith("strong_chord")]
    assert chord and any(all(0 < p < 1 for p in e["prob_first"]) for e in chord)
    assert any(e["loads"] == [Q(277, 4), Q(279, 4)] for e in chord)

    for case in range(750):
        n, N = rng.randrange(1, 10), rng.randrange(1, 8)
        weights = [Q(rng.randrange(1, 40), rng.randrange(1, 17)) for _ in range(n)]
        locations = [[i for i in range(n) if rng.randrange(3) != 0] for _ in range(N)]
        examples.append({"weights": weights, "locations": locations})
    for instance in examples:
        certificate = solve(instance)
        # Independently parse serialized numbers and check all unilateral profiles.
        assert verify(json.loads(json.dumps(serial(instance))),
                      json.loads(json.dumps(serial(certificate))))
        maximum = max(maximum, certificate["factor"])
        family = certificate["on_path"]["family"]
        counts[family] = counts.get(family, 0)+1
    report = serial({"games": len(examples), "random_seed": 2026093001,
                          "largest_observed_menu_factor": maximum,
                          "on_path_families": counts,
                          "three_mixer_strong_chord": {
                              "private_loads": [40, 39], "common_weights": [20]*3,
                              "loads": [Q(277, 4), Q(279, 4)]}})
    if args.report:
        args.report.write_text(json.dumps(report, indent=2)+"\n")
    print(f"Verified {len(examples)} complete exact certificates; max factor {maximum}")


if __name__ == "__main__":
    main()
