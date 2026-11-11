"""Exact feasible coupling witness for the selected cross-terminal queries.

Conditional independence is used only as an explicitly verified completion
of a fixed marginal point.  No independence assumption is imposed on SPE.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from transport_separator import Point, STATES, row_specs, budgets, primitive_cost, serial


def family_witness(point, family):
    specs = row_specs(point.labels[family])
    rhs = budgets(point, family, specs)
    costs = [F()] * len(specs)
    blocks = []
    full_domain_pairs = 0
    positive_flows = 0
    for block in point.blocks(family):
        mu = sum(block.group.rho, F())
        assert mu == point.mass[block.hist_column]
        assert sum((state.mass for state in block.family_states), F()) == mu
        full_domain_pairs += 4 * len(block.family_states)
        if not mu:
            continue
        row_totals = [F()] * 4
        column_totals = [F()] * len(block.family_states)
        flow = []
        for ri, rho in enumerate(block.group.rho):
            for si, state in enumerate(block.family_states):
                mass = rho * state.mass / mu
                assert mass >= 0
                row_totals[ri] += mass
                column_totals[si] += mass
                if not mass:
                    continue
                positive_flows += 1
                flow.append({"old_state": STATES[ri], "new_state_column": state.column, "mass": mass})
                for k, spec in enumerate(specs):
                    costs[k] += mass * primitive_cost(block, ri, state, spec)
        assert tuple(row_totals) == block.group.rho
        assert column_totals == [state.mass for state in block.family_states]
        blocks.append({"hist_column": block.hist_column, "group": block.group.key,
                       "hist_mass": mu, "old_four_state_masses": block.group.rho,
                       "positive_flow": flow,
                       "all_old_and_new_marginals_exact": True})
    queries = [{"query": spec, "budget": budget, "cost": cost, "slack": budget - cost}
               for spec, budget, cost in zip(specs, rhs, costs)]
    minimum = min(item["slack"] for item in queries)
    return {"family": family, "feasible": minimum >= 0, "minimum_query_slack": minimum,
            "query_count": len(queries), "positive_blocks": len(blocks),
            "complete_domain_pairs": full_domain_pairs, "positive_flow_entries": positive_flows,
            "queries": queries, "blocks": blocks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("point", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    point = Point(args.point)
    result = {"scope": "exact completion of the 81 specified pairwise terminal-query transportation constraints; not a complete SPE or full-catalog closure",
              "input": str(args.point.resolve()), "input_sha256": hashlib.sha256(point.raw).hexdigest(),
              "input_W": point.report.get("W"), "input_columns": len(point.columns),
              "coupling_rule": "pi_h,g,F(r,z,s) = rho_h,g(r,z) * eta_h,F(s) / mu_h; zero when mu_h=0",
              "independence_status": "chosen certificate at this point only; never assumed for true strategies",
              "families": [family_witness(point, family) for family in ("B2", "B3", "B4", "Mroot")]}
    result["all_81_queries_exactly_feasible"] = all(f["feasible"] for f in result["families"])
    result["query_count"] = sum(f["query_count"] for f in result["families"])
    assert result["query_count"] == 81
    args.output.write_text(json.dumps(serial(result), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(serial({"all_81_queries_exactly_feasible": result["all_81_queries_exactly_feasible"],
                            "families": [{k: v for k, v in f.items() if k not in ("queries", "blocks")}
                                         for f in result["families"]]}), ensure_ascii=False))


if __name__ == "__main__":
    main()
