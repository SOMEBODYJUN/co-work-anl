"""Attack TB-ANY on the null path in products of a known tight null budget.

This tests one explicit general candidate, never asserts a new special theorem.
The base is k=2 of the existing collision-free 3/2 family, with a null action.
Cross-coordinate SPE threats need not factor; all credible outcomes are retained.
"""
import json
from pathlib import Path
from attack_threshold_products import product_instance
from customer_attraction.exact import ExactSPESolver


def diagnostic(factors):
    instance = product_instance(factors, 3)
    solver = ExactSPESolver(instance)
    values = []
    for used in range(3):
        k = (0,) * (instance.topic_count - 1) + (used,)
        values.append(solver.threshold(k))
    optimum = instance.optimal_welfare()
    budget = sum(values)
    return {"factors": len(factors), "topics": instance.topic_count,
            "players": 3, "null_thresholds": list(map(str, values)),
            "optimum": optimum, "null_budget": str(budget),
            "gap": str(budget-optimum), "counterexample": budget < optimum,
            "states": solver.stats.count_states,
            **({"instance": instance.to_dict()} if budget < optimum else {})}


if __name__ == "__main__":
    base = (7, {7: 2, 56: 2, 1: 1, 8: 1, 82: 1, 64: 1})
    reports = []
    for copies in (1, 2):
        report = diagnostic([base] * copies)
        print(json.dumps(report), flush=True)
        reports.append(report)
        if report["counterexample"]:
            break
    Path(__file__).with_name("null_product_tight_diagnostic.json").write_text(
        json.dumps({"candidate": "TB-ANY", "reports": reports,
                    "status": "finite exact diagnostic only"}, indent=2) + "\n")
