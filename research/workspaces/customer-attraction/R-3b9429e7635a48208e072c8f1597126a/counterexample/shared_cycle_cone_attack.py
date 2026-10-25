"""Directed attack on Q-CAG-HALF via shared-omission reply cycles.

This does not enumerate a restricted input class to claim a positive theorem.
It asks whether one exact full-strategy cone contains a genuine OPT > 2W
instance. Canonical solver and existing cone/verification implementation only.
"""
from __future__ import annotations

import importlib.util
import gzip
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import ExactSPESolver, StrategyCertificate

spec = importlib.util.spec_from_file_location(
    "canonical_strategy_lp", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
audit = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)


def main():
    # General mechanism: the five-theme A/B/T/D/E residual cycle, with shared
    # omitted BDE and TDE blocks amplified by m-1 and m-3 fresh private themes.
    # This run attacks the direct half target at one explicit stress point.
    m, p = 5, 7
    populations = {2: 3, 4: 3, 9: 2, 17: 2, 26: 2*(m-1),
                   28: 2*(m-1), 32: 3, 64: 3}
    clones = tuple(populations.get(mask, 0) for mask in range(1, 1 << p))
    instance = audit.instance_from_clones(p, m, clones)
    solver = ExactSPESolver(instance)
    targets = sorted(solver.worst_outcomes())
    portfolios = ((0, 1, 2, 5, 6), (1, 2, 3, 5, 6))
    report = {"status": "finite_direct_counterexample_attack",
              "universal_bound_proved": False, "seed_populations": populations,
              "players": m, "topics": p, "seed_worst_welfare": solver.minimum_welfare(),
              "seed_optimum": instance.optimal_welfare(), "results": []}
    started = time.monotonic()
    for target in targets:
        cone = audit.cone_from_solver(solver, target, random.Random(0), False)
        for portfolio in portfolios:
            result = cone.optimize(portfolio)
            entry = {"root": target, "portfolio": portfolio,
                     "constraint_rows": len(cone.rows), "result": result}
            if result["certified"]:
                integer = audit.integer_clones(result["values"])
                if not audit.independently_verify(cone, integer):
                    raise AssertionError("full ordered-history direct check failed")
                candidate = audit.instance_from_clones(p, m, integer)
                welfare = candidate.welfare(cone.root)
                optimum = candidate.optimal_welfare()
                entry.update({"integer_clones": integer, "welfare": welfare,
                              "optimum": optimum, "violates_half": optimum > 2*welfare,
                              "strategy": StrategyCertificate(cone.actions, cone.root).to_dict()})
            report["results"].append(entry)
            print(json.dumps(audit.serializable({key: value for key, value in entry.items()
                                                if key not in ("strategy", "result")} | {
                "objective": result.get("value"), "dual_bound": result.get("dual_bound")})), flush=True)
    report["elapsed_seconds"] = time.monotonic() - started
    out = Path(__file__).with_name("shared_cycle_cone_attack.json.gz")
    if out.exists():
        raise FileExistsError(out)
    with gzip.open(out, "wt", encoding="utf-8") as handle:
        json.dump(audit.serializable(report), handle, separators=(",", ":"))
        handle.write("\n")


if __name__ == "__main__":
    main()
