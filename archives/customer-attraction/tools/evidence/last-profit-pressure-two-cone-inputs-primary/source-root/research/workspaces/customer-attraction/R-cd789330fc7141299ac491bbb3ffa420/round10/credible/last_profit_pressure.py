"""Necessary general HALF-counterexample pressure in the same fixed policy.

Every genuine counterexample obeys (2m-1)u_m > 2W by the last player's
static query inequality. We impose its closed relaxation, with no fixed-m
coefficient tuning, and reoptimize the original comparison union objective.
"""
from pathlib import Path
from fractions import Fraction
import sys, json, time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / "tests/audits")]
from customer_attraction import StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, payoff_row, integer_clones,
    instance_from_clones, independently_verify, serializable)


def attempt(source_filename="repeated_upgrade_attempt_m5.json"):
    started = time.monotonic()
    source = json.loads((HERE / source_filename).read_text())
    p, m = source["topics"], source["m"]
    actions = {tuple(x["history"]): x["action"] for x in source["strategy"]["actions"]}
    cone = StrategyCone(p, m, actions)
    last = source["source_path"][-1]
    u = payoff_row(p, cone.root, last)
    pressure = tuple((2 * m - 1) * a - 2 * w for a, w in zip(u, cone.welfare))
    cone.rows += (pressure,)
    cone.matrix = np.array(cone.rows, dtype=float)
    res = cone.optimize(source["target_comparison"])
    result = {"scope": "same repeated-upgrade policy plus necessary general badness row",
              "universal_bound_proved": False, "LP_status": res["status"],
              "m": m, "topics": p, "source_path": source["source_path"],
              "strategy_source": source_filename,
              "necessary_row": "(2m-1) u_m >= 2W"}
    if res["certified"]:
        clones = integer_clones(res["values"])
        ins = instance_from_clones(p, m, clones)
        if not independently_verify(cone, clones):
            raise AssertionError("exact whole-tree IC failed")
        cert = StrategyCertificate(actions, cone.root)
        verify_certificate(ins, cert).assert_valid()
        W, OPT = ins.welfare(cone.root), ins.optimal_welfare()
        utilities = ins.player_payoffs(source["source_path"])
        if (2 * m - 1) * utilities[-1] < 2 * W:
            raise AssertionError("pressure row lost")
        result.update({"endpoint": ins.to_dict(), "strategy": cert.to_dict(),
                       "W": W, "OPT": OPT, "ratio": Fraction(OPT, W),
                       "utilities": utilities, "last_pressure_slack": (2*m-1)*utilities[-1]-2*W,
                       "objective": res["value"], "dual_bound": res["dual_bound"],
                       "dual_optimal": res["dual_optimal"], "dual_support": res["dual_support"],
                       "refutes_HALF": OPT > 2 * W})
    result["seconds"] = time.monotonic() - started
    return result


if __name__ == "__main__":
    path = HERE / "last_profit_pressure_m5.json"
    if path.exists():
        raise FileExistsError(path)
    result = attempt()
    path.write_text(json.dumps(serializable(result), indent=2) + "\n")
    print(json.dumps(serializable({k:v for k,v in result.items()
                                  if k not in ("endpoint", "strategy", "dual_support")})), flush=True)
