"""Pressure the exact all-m bridge OPT-W <= m min_i u_i.

This only reuses round10's already verified full-history policy. No policy or
fixed-size instance scan is performed. All accepted endpoints are recovered
over Fraction, integerized, and checked on every ordered history. A positive
bridge gap would only refute this named bridge; HALF is checked separately.
"""
from pathlib import Path
from fractions import Fraction
import json, sys, time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / "tests/audits")]
from customer_attraction import Instance, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (
    StrategyCone, coverage_row, payoff_row, dot, integer_clones,
    instance_from_clones, independently_verify, serializable,
)


def pressure():
    start = time.monotonic()
    source_file = HERE.parent.parent / "round10/credible/repeated_upgrade_attempt_m5.json"
    source = json.loads(source_file.read_text())
    ins = Instance.from_dict(source["endpoint"])
    p, m = ins.topic_count, ins.players
    actions = {tuple(x["history"]): x["action"] for x in source["strategy"]["actions"]}
    cone = StrategyCone(p, m, actions)
    path = tuple(source["source_path"])
    comparison = tuple(source["target_comparison"])
    i = 0
    utility = payoff_row(p, cone.root, path[i])
    optimal_lower = coverage_row(p, comparison)
    objective = tuple(o - w - m * u for o, w, u in
                      zip(optimal_lower, cone.welfare, utility))
    # Explicitly retain role i as an actual minimum-payoff player.
    minimum_rows = tuple(tuple(x-y for x, y in zip(payoff_row(p, cone.root, a), utility))
                         for a in path if a != path[i])
    rows = cone.rows + minimum_rows
    matrix = np.array(rows, dtype=float)
    result = linprog(-np.array(objective, dtype=float), A_ub=-matrix,
                     b_ub=np.zeros(len(rows)),
                     A_eq=np.array([cone.welfare], dtype=float), b_eq=[1],
                     bounds=(0, None), method="highs")
    record = {"candidate": "OPT_m-W <= m min_i actual_u_i", "m": m,
              "topics": p, "actual": path, "fixed_comparison": comparison,
              "fixed_minimum_role": i, "all_incidence_types_allowed": (1 << p)-1,
              "source": str(source_file.relative_to(ROOT)),
              "scope": "one already available complete SPE cone; no universal conclusion",
              "floating_status": result.message,
              "universal_bound_proved": False, "refutes_HALF": False}
    if result.success:
        point = tuple(Fraction(float(x)).limit_denominator(10**7) for x in result.x)
        feasible = lambda v: (cone.verify(v) and dot(cone.welfare, v) == 1
                              and all(dot(r,v) >= 0 for r in minimum_rows))
        if not feasible(point):
            point = cone.recover_vertex(result.x)
        if point is not None and feasible(point):
            clones = integer_clones(point)
            endpoint = instance_from_clones(p, m, clones)
            certificate = StrategyCertificate(actions, cone.root)
            report = verify_certificate(endpoint, certificate)
            report.assert_valid()
            if not independently_verify(cone, clones):
                raise AssertionError("ordered-history independent IC check failed")
            utilities = endpoint.player_payoffs(path)
            W, OPT = endpoint.welfare(cone.root), endpoint.optimal_welfare()
            record.update({"exact_primal": True, "endpoint": endpoint.to_dict(),
                "strategy": certificate.to_dict(), "utilities": utilities,
                "W": W, "OPT": OPT, "ratio": Fraction(OPT,W),
                "fixed_objective": dot(objective, clones),
                "normalized_fixed_objective": dot(objective, point),
                "true_bridge_gap": OPT-W-m*min(utilities),
                "refutes_bridge": OPT > W+m*min(utilities),
                "refutes_HALF": OPT > 2*W,
                "all_history_check": {"histories": report.checked_histories,
                                       "nonself_IC": report.checked_deviations}})
        else:
            record["exact_primal"] = False
    record["seconds"] = time.monotonic()-start
    return record


if __name__ == "__main__":
    output = HERE / "minimum_netgap_pressure.json"
    if output.exists():
        raise FileExistsError(output)
    result = pressure()
    output.write_text(json.dumps(serializable(result), indent=2)+"\n")
    print(json.dumps(serializable({k:v for k,v in result.items()
                                  if k not in ("endpoint", "strategy")})))
