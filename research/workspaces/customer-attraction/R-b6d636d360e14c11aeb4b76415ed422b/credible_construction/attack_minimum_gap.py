"""Target only OPT-W <= m min_i u_i, inside saved full SPE cones.

Floating LP proposes a witness; Fraction checks every SPE row and a separately
expanded unit-customer verifier checks every ordered-history deviation.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, StrategyCertificate, verify_certificate
from tests.audits.customer_attraction_strategy_lp import (
    StrategyCone, coverage_row, payoff_row, dot, integer_clones,
    instance_from_clones,
)

HERE = Path(__file__).resolve().parent


def serial(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def unit_check(instance, certificate):
    """Do not use the solver or payoff-row arithmetic; expand actual clients."""
    covers = [set() for _ in instance.topics]
    index = 0
    for typ in instance.customers:
        for _ in range(typ.multiplicity):
            for a in typ.topics:
                covers[a].add(index)
            index += 1
    hist = dec = 0
    min_slack = None

    def utility(path, who):
        return sum((Fraction(1, sum(x in covers[a] for a in path))
                    for x in covers[path[who]]), Fraction(0))

    def walk(h):
        nonlocal hist, dec, min_slack
        if len(h) == instance.players:
            return h
        branches = [walk(h + (a,)) for a in range(instance.topic_count)]
        actual = branches[certificate.actions[h]]
        actual_u = utility(actual, len(h))
        hist += 1
        for a, branch in enumerate(branches):
            if a == certificate.actions[h]:
                continue
            dec += 1
            slack = actual_u - utility(branch, len(h))
            if slack < 0:
                raise AssertionError((h, a, actual_u, utility(branch, len(h))))
            min_slack = slack if min_slack is None else min(min_slack, slack)
        return actual

    path = walk(())
    return {"histories": hist, "deviations": dec,
            "path": path, "minimum_slack": min_slack,
            "payoffs": [utility(path, i) for i in range(instance.players)]}


def scan(cone, origin):
    best = Fraction(-10**9)
    checks = 0
    duals = []
    failed_duals = 0
    for support in combinations(range(cone.topics), min(cone.players, cone.topics)):
        covered = coverage_row(cone.topics, support)
        for a, count in enumerate(cone.root):
            if not count:
                continue
            objective = tuple(v-w-cone.players*u for v, w, u in zip(
                covered, cone.welfare, payoff_row(cone.topics, cone.root, a)))
            res = linprog(-np.array(objective, dtype=float),
                          A_ub=-cone.matrix, b_ub=np.zeros(len(cone.rows)),
                          A_eq=np.array([cone.welfare], dtype=float), b_eq=[1],
                          bounds=(0, None), method="highs")
            checks += 1
            if not res.success:
                failed_duals += 1
                continue
            beta = Fraction(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
            mu = tuple(Fraction(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals)
            residual = tuple(beta*w-sum(z*row[j] for z,row in zip(mu,cone.rows))-v
                             for j,(w,v) in enumerate(zip(cone.welfare,objective)))
            dual_ok = all(x >= 0 for x in mu) and all(x >= 0 for x in residual)
            if dual_ok:
                duals.append({"support":support,"topic":a,"upper_bound":beta,
                              "nonzero_multipliers":[(i,x) for i,x in enumerate(mu) if x]})
            else:
                failed_duals += 1
            r = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
            if not cone.verify(r) or dot(cone.welfare, r) != 1:
                r = cone.recover_vertex(res.x)
            if r is None or not cone.verify(r) or dot(cone.welfare, r) != 1:
                continue
            value = dot(objective, r)
            best = max(best, value)
            if value > 0:
                clones = integer_clones(r)
                instance = instance_from_clones(cone.topics, cone.players, clones)
                certificate = StrategyCertificate(cone.actions, cone.root)
                verification = verify_certificate(instance, certificate)
                verification.assert_valid()
                independent = unit_check(instance, certificate)
                return {
                    "status": "exact_counterexample", "origin": origin,
                    "instance": instance.to_dict(), "strategy": certificate.to_dict(),
                    "support": support, "tested_topic": a,
                    "welfare": instance.welfare(cone.root),
                    "optimum": instance.optimal_welfare(),
                    "unit_audit": independent, "normalized_violation": value,
                    "lp_calls": checks,
                }
    return {"status": "no_counterexample_found", "origin": origin,
            "best_normalized_violation": best, "lp_calls": checks,
            "all_objectives_have_exact_duals": failed_duals == 0,
            "exact_dual_upper_bound": max((x["upper_bound"] for x in duals),default=None),
            "failed_duals": failed_duals, "duals":duals}


def main():
    pairs = [
        ("root_tax_failure", 6, 4),
        ("individual_security_failure", 6, 3),
        ("eight_cce_welfare_gap", 4, 3),
        ("worst_cce_welfare", 5, 3),
    ]
    reports = []
    for name, p, m in pairs:
        path = ROOT / "evidence/certificates/customer_attraction" / (name + ".json")
        if not path.exists():
            continue
        obj = json.loads(path.read_text())
        strategy = obj.get("strategy", obj)
        actions = {tuple(item["history"]): item["action"] for item in strategy["actions"]}
        cone = StrategyCone(p, m, actions)
        report = scan(cone, str(path.relative_to(ROOT)))
        reports.append(report)
        print(serial({k:v for k,v in report.items() if k not in ("instance", "strategy")}), flush=True)
        if report["status"] == "exact_counterexample":
            (HERE / "minimum_gap_counterexample.json").write_text(json.dumps(serial(report), ensure_ascii=False, indent=2) + "\n")
            break
    if all(r["status"] != "exact_counterexample" for r in reports):
        path = ROOT / "evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json"
        obj = json.loads(path.read_text())
        for i, proof in enumerate(obj["cone_proofs"]):
            actions = {tuple(item["history"]): item["action"] for item in proof["actions"]}
            report = scan(StrategyCone(5, 4, actions), str(path.relative_to(ROOT)) + f":cone={i}")
            reports.append(report)
            print(serial({k:v for k,v in report.items() if k not in ("instance", "strategy")}), flush=True)
            if report["status"] == "exact_counterexample":
                (HERE / "minimum_gap_counterexample.json").write_text(json.dumps(serial(report), ensure_ascii=False, indent=2) + "\n")
                break
    (HERE / "minimum_gap_scan.json").write_text(json.dumps(serial(reports), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
