"""Targeted BG-HALF candidate check on eight named existing examples.

This is finite evidence, not a universal proof. Run from the repository root.
The exact solver enumerates realizable outcomes without forcing common tie
choices at distinct ordered histories.
"""

import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from customer_attraction.exact import ExactSPESolver
from customer_attraction.model import Instance


NAMES = (
    "coverage_opportunity_failure",
    "tax_bridge_failure",
    "prefix_balance_failure",
    "individual_security_failure",
    "root_tax_failure",
    "global_decorrelation_failure",
    "general_tax_failure",
    "residual_counterexample",
)


def check(name):
    source = Path("examples/customer_attraction") / (name + ".json")
    instance = Instance.from_dict(json.loads(source.read_text()))
    solver = ExactSPESolver(instance)
    solver.outcomes()
    total = 0
    minimum = None
    witness = None
    # Every legal prefix count is visited by the full root recursion.
    for background, outcomes in solver._outcomes.items():
        remaining = instance.players - sum(background)
        if not remaining:
            continue
        completion = max(
            instance.welfare(tuple(
                background[j] + int(j in support)
                for j in range(instance.topic_count)
            ))
            for size in range(min(remaining, instance.topic_count) + 1)
            for support in combinations(range(instance.topic_count), size)
        )
        # Repeated topics cannot add coverage, so supports of size <= r suffice.
        for terminal in outcomes:
            payoffs = instance.topic_payoffs(terminal)
            active_profit = sum(
                (terminal[j] - background[j]) * payoffs[j]
                for j in range(instance.topic_count)
            )
            welfare = instance.welfare(terminal)
            slack = welfare + active_profit - completion
            if minimum is None or slack < minimum:
                minimum = slack
                witness = {
                    "background": background,
                    "terminal": terminal,
                    "completion": completion,
                    "welfare": welfare,
                    "active_profit": str(active_profit),
                }
            total += 1
    return {
        "name": name,
        "checks": total,
        "minimum_slack": str(minimum),
        "minimizer": witness,
    }


if __name__ == "__main__":
    reports = [check(name) for name in NAMES]
    print(json.dumps({
        "candidate": "Cstar_h <= W_h + V_active_h",
        "scope": "eight named existing finite games; not a universal proof",
        "checks": sum(row["checks"] for row in reports),
        "reports": reports,
    }, indent=2))
