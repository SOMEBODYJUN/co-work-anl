#!/usr/bin/env python3
"""Reproduce the one existing eight-certificate theta-extra diagnosis.

Run from any directory:
    python research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/direct/reproduce_extra_theta_diagnosis.py

The default repository root is inferred from this script's stored location.
This reuses previously certified policies. It does NOT verify all SPE ICs,
generate instances, enumerate policies, or establish a general theorem.
"""

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


# These are the exact eight existing input/certificate pairs used in the
# original diagnostic. All paths are relative to the repository root.
PAIRS = (
    (
        "individual_security_failure",
        "examples/customer_attraction/individual_security_failure.json",
        "evidence/certificates/customer_attraction/individual_security_failure.json",
    ),
    (
        "aggregate_theta_failure",
        "examples/customer_attraction/aggregate_theta_failure.json",
        "evidence/certificates/customer_attraction/aggregate_theta_failure.json",
    ),
    (
        "five_individual_security",
        "examples/customer_attraction/five_individual_security.json",
        "evidence/certificates/customer_attraction/five_individual_security.json",
    ),
    (
        "local_security_increment",
        "examples/customer_attraction/local_security_increment.json",
        "evidence/certificates/customer_attraction/local_security_increment.json",
    ),
    (
        "eight_cce_welfare_gap",
        "examples/customer_attraction/eight_cce_welfare_gap.json",
        "evidence/certificates/customer_attraction/eight_cce_welfare_gap.json",
    ),
    (
        "dynamic_iid_local",
        "examples/customer_attraction/dynamic_iid_local.json",
        "evidence/certificates/customer_attraction/dynamic_iid_local.json",
    ),
    (
        "root_tax_failure",
        "examples/customer_attraction/root_tax_failure.json",
        "evidence/certificates/customer_attraction/root_tax_failure.json",
    ),
    (
        "worst_cce_welfare_failure",
        "examples/customer_attraction/worst_cce_welfare_failure.json",
        "evidence/certificates/customer_attraction/worst_cce_welfare_failure.json",
    ),
)


def diagnose(repository_root):
    for name, input_path, certificate_path in PAIRS:
        data = json.loads((repository_root / input_path).read_text())
        certificate = json.loads((repository_root / certificate_path).read_text())
        topic_count = len(data["topics"])
        player_count = data["players"]
        customers = [
            (set(customer["topics"]), customer.get("multiplicity", 1))
            for customer in data["customers"]
        ]
        strategy = certificate.get(
            "strategy", certificate.get("certificate", certificate)
        )
        policy = {
            tuple(entry["history"]): entry["action"]
            for entry in strategy["actions"]
        }

        # Follow the exact ordered-history policy from the empty history.
        actual_path = ()
        while len(actual_path) < player_count:
            actual_path += (policy[actual_path],)

        def utility(background, topic, extra):
            # extra=0: a player's own occurrence is already in background.
            # extra=1: insert one independent queried player into background.
            return sum(
                (
                    Fraction(
                        multiplicity,
                        extra + sum(action in interests for action in background),
                    )
                    for interests, multiplicity in customers
                    if topic in interests
                ),
                Fraction(),
            )

        actual_payoffs = [utility(actual_path, topic, 0) for topic in actual_path]
        theta_extra = None
        minimizing_background = None

        # Queries depend only on the multiset of m background topics. Thus
        # combinations_with_replacement covers all pure background values,
        # without imposing any restriction on the ordered-history SPE policy.
        for background in itertools.combinations_with_replacement(
            range(topic_count), player_count
        ):
            value = max(
                utility(background, topic, 1) for topic in range(topic_count)
            )
            if theta_extra is None or value < theta_extra:
                theta_extra = value
                minimizing_background = background

        print(
            name,
            "m=", player_count,
            "actual=", actual_path,
            "u=", ",".join(map(str, actual_payoffs)),
            "theta_extra=", theta_extra,
            "witness=", minimizing_background,
            "margin=", min(actual_payoffs) - theta_extra,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[5]
    )
    diagnose(parser.parse_args().repo_root)
