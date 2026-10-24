"""Independent exact checks of SM-opt-exists, SM-opt-all and TB.

Only the five fixed fixtures in main() are examined. This is not a scan and
does not prove any universal statement. No project solver/model is imported.
The oracle keeps complete ordered histories, expands unit customers, and
uses Fraction for every payoff and comparison.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]


class OrderedOracle:
    def __init__(self, data):
        self.p = len(data["topics"])
        self.m = data["players"]
        self.units = tuple(
            frozenset(row["topics"])
            for row in data["customers"]
            for _ in range(row.get("multiplicity", 1))
        )

    @lru_cache(None)
    def utility(self, terminal, role):
        assert len(terminal) == self.m
        action = terminal[role]
        return sum(
            (Fraction(1, sum(a in interests for a in terminal))
             for interests in self.units if action in interests),
            Fraction(0),
        )

    @lru_cache(None)
    def welfare(self, terminal):
        return sum(any(a in interests for a in terminal)
                   for interests in self.units)

    @lru_cache(None)
    def realizable(self, history):
        """All ordered terminal paths attainable by some pure SPE here."""
        if len(history) == self.m:
            return frozenset({history})
        role = len(history)
        children = tuple(self.realizable(history + (a,)) for a in range(self.p))
        ell = tuple(min(self.utility(z, role) for z in child)
                    for child in children)
        threshold = max(ell)
        return frozenset(z for child in children for z in child
                         if self.utility(z, role) >= threshold)

    @lru_cache(None)
    def row(self, history):
        role = len(history)
        assert role < self.m
        return tuple(min(self.utility(z, role)
                         for z in self.realizable(history + (a,)))
                     for a in range(self.p))

    def verify_complete_strategy(self, actions):
        expected = {h for t in range(self.m)
                    for h in product(range(self.p), repeat=t)}
        assert set(actions) == expected

        @lru_cache(None)
        def rollout(h):
            if len(h) == self.m:
                return h
            return rollout(h + (actions[h],))

        comparisons = 0
        for h in expected:
            actual = self.utility(rollout(h), len(h))
            for a in range(self.p):
                comparisons += 1
                assert actual >= self.utility(rollout(h + (a,)), len(h))
        return rollout(()), len(expected), comparisons

    def audit(self, path):
        path = tuple(path)
        assert path in self.realizable(())
        rows = tuple(self.row(path[:i]) for i in range(self.m))
        all_tuples = tuple(product(range(self.p), repeat=self.m))
        optimum = max(map(self.welfare, all_tuples))
        opt_tuples = tuple(t for t in all_tuples if self.welfare(t) == optimum)
        sums = {t: sum((rows[i][t[i]] for i in range(self.m)), Fraction(0))
                for t in opt_tuples}
        denominator_rows = tuple(tuple(sum(
            (Fraction(1, sum(a in interests for a in path[:i]) + self.m - i)
             for interests in self.units if action in interests), Fraction(0))
            for action in range(self.p)) for i in range(self.m))
        assert all(denominator_rows[i][a] <= rows[i][a]
                   for i in range(self.m) for a in range(self.p))
        denominator_sums = {
            t: sum((denominator_rows[i][t[i]] for i in range(self.m)), Fraction(0))
            for t in opt_tuples}
        argmin = min(sums, key=lambda t: (sums[t], t))
        argmax = max(sums, key=lambda t: (sums[t], t))
        w = self.welfare(path)
        theta = tuple(max(row) for row in rows)
        gap = optimum - w
        best_sum, worst_sum = sums[argmax], sums[argmin]
        assert sum((self.utility(path, i) for i in range(self.m)), Fraction(0)) == w
        assert all(self.utility(path, i) >= theta[i] for i in range(self.m))
        return {
            "path": path,
            "welfare": w,
            "optimum": optimum,
            "optimum_minus_welfare": gap,
            "optimal_ordered_tuple_count": len(opt_tuples),
            "rows_L": rows,
            "theta": theta,
            "sum_theta": sum(theta, Fraction(0)),
            "min_opt_sum_L": worst_sum,
            "min_opt_tuple": argmin,
            "max_opt_sum_L": best_sum,
            "max_opt_tuple": argmax,
            "SM_opt_all_slack": worst_sum - gap,
            "SM_opt_exists_slack": best_sum - gap,
            "TB_slack": sum(theta, Fraction(0)) - gap,
            "max_opt_worst_denominator_sum": max(denominator_sums.values()),
            "worst_denominator_exists_slack": max(denominator_sums.values()) - gap,
            "ordered_SPE_path_count": len(self.realizable(())),
            "ordered_history_oracle_states": sum(self.p ** t
                                                 for t in range(self.m + 1)),
        }


def rational_json(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {k: rational_json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [rational_json(v) for v in value]
    return value


def main():
    results = {}
    # The selected histories are supplied by the frozen complete strategies;
    # all of those strategies are independently checked below.
    for name in ("root_tax_failure", "aggregate_theta_failure",
                 "individual_security_failure", "portfolio_matching_failure"):
        data = json.loads((ROOT / "examples/customer_attraction" / f"{name}.json").read_text())
        cert = json.loads((ROOT / "evidence/certificates/customer_attraction" / f"{name}.json").read_text())
        strategy = cert.get("strategy", cert)
        actions = {tuple(row["history"]): row["action"]
                   for row in strategy["actions"]}
        oracle = OrderedOracle(data)
        path, histories, comparisons = oracle.verify_complete_strategy(actions)
        results[name] = oracle.audit(path)
        results[name]["frozen_complete_strategy_histories_verified"] = histories
        results[name]["frozen_complete_strategy_comparisons_verified"] = comparisons

    # This is exactly the previously known m=4 all-big UV obstruction. It is
    # included to keep that obstruction separate from both SM and TB.
    all_big = {"topics": ["B", "S1", "S2", "S3"], "players": 4,
               "customers": [{"topics": [0], "multiplicity": 4}] +
                            [{"topics": [a]} for a in (1, 2, 3)]}
    results["known_all_big_m4"] = OrderedOracle(all_big).audit((0, 0, 0, 0))
    assert results["known_all_big_m4"]["rows_L"] == ((Fraction(1),) * 4,) * 4
    assert results["known_all_big_m4"]["max_opt_worst_denominator_sum"] == Fraction(17, 6)
    assert results["known_all_big_m4"]["worst_denominator_exists_slack"] == Fraction(-1, 6)
    # These checks are diagnostics, not assumed conclusions inside the oracle.
    assert all(row["SM_opt_exists_slack"] >= 0 for row in results.values())
    assert all(row["SM_opt_all_slack"] >= 0 for row in results.values())
    assert all(row["TB_slack"] >= 0 for row in results.values())
    output = {
        "status": "PASS: five deterministic existing-fixture diagnostics only",
        "universal_status": "SM-opt-exists, SM-opt-all, TB and Q-CAG-HALF remain OPEN",
        "independence": "No customer_attraction imports; expanded unit customers; complete ordered histories; Fraction arithmetic",
        "fixtures": results,
    }
    target = Path(__file__).with_name("ordered_threshold_audit.json")
    target.write_text(json.dumps(rational_json(output), indent=2) + "\n")
    print(json.dumps(rational_json(output), indent=2))


if __name__ == "__main__":
    main()
