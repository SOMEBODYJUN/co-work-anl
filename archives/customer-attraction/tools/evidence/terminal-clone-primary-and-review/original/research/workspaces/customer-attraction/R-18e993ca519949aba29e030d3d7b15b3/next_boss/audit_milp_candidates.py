"""Exact reoptimization/audit of full-tree MILP proposals; no global MIP claim."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/audits"))
from customer_attraction_strategy_lp import (
    StrategyCone, coverage_row, payoff_row, dot, integer_clones,
    instance_from_clones, independently_verify,
)
from customer_attraction import StrategyCertificate, verify_certificate


def audit(path):
    path = path.resolve()
    raw = json.loads(path.read_text())
    m, p, player = (raw["parameters"][s] for s in ["players", "topics", "player"])
    records = []
    for proposal in raw["results"]:
        if "actions" not in proposal:
            records.append({"no_incumbent": True, "mip_status": proposal["status"]})
            continue
        actions = {tuple(row["history"]): row["action"] for row in proposal["actions"]}
        cone = StrategyCone(p, m, actions)
        h = ()
        for _ in range(m):
            h += (actions[h],)
        norm = payoff_row(p, cone.root, h[player])
        objective = (payoff_row(p, cone.root, h[-1]) if raw["parameters"]["objective"] == "terminal"
                     else coverage_row(p, proposal["portfolio"]))
        if raw["parameters"]["objective"] == "gap":
            objective = tuple(a-b for a,b in zip(objective, cone.welfare))
        result = linprog(-np.array(objective, dtype=float),
                         A_ub=-cone.matrix, b_ub=np.zeros(len(cone.rows)),
                         A_eq=[np.array(norm, dtype=float)], b_eq=[1],
                         bounds=(0, None), method="highs")
        if not result.success:
            records.append({"exact_candidate_failed": result.message})
            continue
        values = tuple(F(float(v)).limit_denominator(10**7) for v in result.x)
        if not cone.verify(values) or dot(norm, values) != 1:
            saved_welfare = cone.welfare
            cone.welfare = norm
            values = cone.recover_vertex(result.x)
            cone.welfare = saved_welfare
        if values is None or not cone.verify(values) or dot(norm, values) != 1:
            records.append({"exact_recovery_failed": True})
            continue
        clones = integer_clones(values)
        assert independently_verify(cone, clones)
        instance = instance_from_clones(p, m, clones)
        certificate = StrategyCertificate(actions, cone.root)
        report = verify_certificate(instance, certificate)
        report.assert_valid()
        beta = F(float(-result.eqlin.marginals[0])).limit_denominator(10**7)
        dual = tuple(F(float(-v)).limit_denominator(10**7) for v in result.ineqlin.marginals)
        residual = tuple(beta * norm[j] - sum(mu*row[j] for mu,row in zip(dual,cone.rows)) - objective[j]
                         for j in range(len(norm)))
        exact_dual = all(v>=0 for v in dual) and all(v>=0 for v in residual)
        utility = instance.topic_payoff(h[player], cone.root)
        welfare = instance.welfare(cone.root)
        optimum = instance.optimal_welfare()
        records.append(dict(portfolio=proposal["portfolio"],
                            exact_normalized_objective=str(dot(objective, values)),
                            fixed_cone_exact_dual=str(beta) if exact_dual else None,
                            fixed_cone_optimum_certified=exact_dual and beta==dot(objective,values),
                            actual_path=h, normalized_player=player,
                            utility=str(utility), W=welfare, OPT=optimum,
                            gap_bridge_slack=str(m*utility-(optimum-welfare)),
                            instance=instance.to_dict(), strategy=certificate.to_dict(),
                            exact_full_history_SPE=True,
                            universal_bound_proved=False))
    return {"source": str(path.relative_to(ROOT)), "records": records,
            "scope": "exact feasible SPE and fixed-cone LP certificates only; MIP upper bounds excluded"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    reports = [audit(path) for path in args.inputs]
    args.out.write_text(json.dumps(reports, indent=2) + "\n")
    for report in reports:
        print(json.dumps({"source": report["source"], "results": [
            {k:v for k,v in record.items() if k not in {"instance", "strategy"}}
            for record in report["records"]]}))
