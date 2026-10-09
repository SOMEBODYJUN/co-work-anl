"""Exact independent certificate audit: no optimal-portfolio matching can work.

The fixed fixture has a unique two-theme coverage optimum. Complete prescribed
histories and every actual deviation are evaluated directly from unit customer
types, without invoking the SPE outcome recurrence. Canonical solver checks are
additional corroboration. Floating LP/MILP proposal output is not proof input.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def audit() -> dict:
    instance_path = ROOT / "examples/customer_attraction/portfolio_matching_failure.json"
    certificate_path = ROOT / "evidence/certificates/customer_attraction/portfolio_matching_failure.json"
    raw = json.loads(instance_path.read_text())
    cert = json.loads(certificate_path.read_text())
    k, m = len(raw["topics"]), raw["players"]
    assert (k, m) == (5, 2)
    customers = tuple((frozenset(item["topics"]), item["multiplicity"])
                      for item in raw["customers"])
    assert all(type(w) is int and w > 0 for _, w in customers)
    actions = {tuple(item["history"]): item["action"] for item in cert["actions"]}
    expected_histories = {h for length in range(m)
                          for h in product(range(k), repeat=length)}
    assert set(actions) == expected_histories

    def continuation(history):
        history = tuple(history)
        while len(history) < m:
            history += (actions[history],)
        return history

    def payoff(action, history):
        return sum((Fraction(w, sum(a in topics for a in history))
                    for topics, w in customers if action in topics), Fraction(0))

    def coverage(support):
        return sum(w for topics, w in customers if topics.intersection(support))

    checks = 0
    incentives = []
    follower_table = []
    for history in sorted(actions, key=lambda h: (len(h), h)):
        chosen = actions[history]
        chosen_path = continuation(history + (chosen,))
        own = payoff(chosen, chosen_path)
        branch_values = []
        for alternative in range(k):
            branch = continuation(history + (alternative,))
            value = payoff(alternative, branch)
            branch_values.append(str(value))
            if alternative != chosen:
                assert own >= value, (history, chosen, alternative, own, value)
                checks += 1
        incentives.append({"history": list(history), "chosen_action": chosen,
                           "prescribed_payoff": str(own),
                           "all_branch_payoffs": branch_values})
        if history:
            follower_table.append({"first_action": history[0],
                                   "all_follower_payoffs": branch_values,
                                   "prescribed_response": chosen,
                                   "first_player_final_payoff":
                                       str(payoff(history[0], chosen_path))})
    actual = continuation(())
    assert actual == (4, 0)
    counts = tuple(actual.count(a) for a in range(k))
    assert tuple(cert["terminal_counts"]) == counts
    welfare = coverage(set(actual))
    assert welfare == 44
    payoffs = tuple(payoff(a, actual) for a in actual)
    assert payoffs == (22, 22)
    all_portfolios = []
    for portfolio in combinations(range(k), m):
        all_portfolios.append({"portfolio": list(portfolio),
                               "coverage": coverage(portfolio)})
    optimum = max(item["coverage"] for item in all_portfolios)
    optimal = [tuple(item["portfolio"]) for item in all_portfolios
               if item["coverage"] == optimum]
    assert optimum == 45 and optimal == [(1, 3)]
    portfolio = optimal[0]
    residual = sum(w for topics, w in customers
                   if topics.intersection(portfolio) and not topics.intersection(actual))
    assert residual == 42
    matrix = tuple(tuple(payoff(topic, continuation(actual[:i] + (topic,)))
                         for topic in portfolio) for i in range(m))
    assert matrix == ((19, 19), (22, 22))
    matching_values = [sum(matrix[i][permutation[i]] for i in range(m))
                       for permutation in permutations(range(m))]
    maximum_matching = max(matching_values)
    assert maximum_matching == 41 < residual
    assert optimum <= 2 * welfare

    from customer_attraction import Instance, StrategyCertificate, ExactSPESolver, verify_certificate
    canonical_instance = Instance.from_dict(raw)
    canonical_certificate = StrategyCertificate.from_dict(cert)
    checked = verify_certificate(canonical_instance, canonical_certificate)
    checked.assert_valid()
    assert checked.checked_histories == len(expected_histories) == 6
    assert checked.checked_deviations == checks == 24
    solver = ExactSPESolver(canonical_instance)
    assert counts in solver.outcomes()
    assert canonical_instance.optimal_welfare() == optimum
    assert solver.minimum_welfare() == 41
    result = {
        "claim_id": "CA-PORTFOLIO-MATCHING-NO", "status": "exact counterexample verified",
        "meaning": "every optimal portfolio fails; unique optimum makes both fixed-optimum and existential-optimum versions false",
        "not_a_half_coverage_counterexample": True,
        "arithmetic": "direct Fraction customer shares and integer coverage; no floating point",
        "customer_count": sum(w for _, w in customers),
        "catalog_size": k, "players": m,
        "topic_labels": raw["topics"], "actual_history": list(actual),
        "actual_terminal_counts": list(counts), "actual_payoffs": list(map(str, payoffs)),
        "actual_welfare": welfare, "opt_m": optimum,
        "all_two_theme_coverages": all_portfolios,
        "unique_optimal_portfolio": list(portfolio),
        "optimal_uncovered_customers": residual,
        "deviation_payoff_matrix": [list(map(str, row)) for row in matrix],
        "assignment_sums": list(map(str, matching_values)),
        "maximum_assignment_sum": str(maximum_matching),
        "matching_shortfall": str(residual - maximum_matching),
        "all_history_incentives": incentives,
        "follower_response_table": follower_table,
        "independent_checked_histories": len(expected_histories),
        "independent_checked_deviations": checks,
        "canonical_complete_certificate_verified": checked.valid,
        "canonical_all_spe_terminal_counts": [list(q) for q in sorted(solver.outcomes())],
        "canonical_minimum_spe_welfare": solver.minimum_welfare(),
        "base_git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "instance_sha256": hashlib.sha256(instance_path.read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError("frozen evidence must not be overwritten")
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("all_history_incentives", "follower_response_table",
                                     "all_two_theme_coverages", "canonical_all_spe_terminal_counts")}))


if __name__ == "__main__":
    main()
