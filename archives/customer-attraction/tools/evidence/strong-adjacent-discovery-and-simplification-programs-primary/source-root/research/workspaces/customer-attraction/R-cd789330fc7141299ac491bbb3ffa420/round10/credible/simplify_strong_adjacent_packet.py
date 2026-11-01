"""One integer witness simplification inside the SAME successful policy cone.

It minimizes unit-customer count subject to all existing full-history IC and
the already separated fixed-query StrongA gap being positive. MILP only
proposes integers; exact full-history checks decide acceptance. No policy scan.
"""
from pathlib import Path
from fractions import Fraction
from math import lcm
import json, sys, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csc_matrix, vstack

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / "tests/audits"), str(HERE)]
from customer_attraction import StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, instance_from_clones,
    independently_verify, dot, serializable)
from strong_adjacent_gap_attack import frozen_row, adjacent_row, frozen_max_tuple


def simplify():
    started = time.monotonic()
    source = json.loads((HERE / "strong_adjacent_gap_attack.json").read_text())
    p, m = source["topics"], source["m"]
    path, queries = tuple(source["actual_path"]), tuple(source["fixed_queries"])
    actions = {tuple(x["history"]): x["action"] for x in source["strategy"]["actions"]}
    cone = StrategyCone(p, m, actions)
    C = adjacent_row(p, path)
    fs = [frozen_row(p, path, i, t) for i, t in enumerate(queries)]
    gap = tuple(sum(f[j] for f in fs) - w - c
                for j, (w, c) in enumerate(zip(cone.welfare, C)))
    scale = lcm(*(x.denominator for row in cone.rows for x in row),
                *(x.denominator for x in gap))
    G = np.array([[int(x * scale) for x in row] for row in cone.rows], dtype=float)
    gr = np.array([[int(x * scale) for x in gap]], dtype=float)
    A = vstack([csc_matrix(G), csc_matrix(gr)], format="csc")
    lo = np.r_[np.zeros(len(cone.rows)), 1.]
    res = milp(np.ones((1 << p) - 1), integrality=np.ones((1 << p) - 1),
               bounds=Bounds(0, np.inf), constraints=LinearConstraint(A, lo, np.inf),
               options={"time_limit": 30., "mip_rel_gap": 0.})
    r = {"scope": "one integer simplification in the same StrongA witness full-history cone",
         "source_file": "strong_adjacent_gap_attack.json", "m": m, "topics": p,
         "actual_path": path, "fixed_queries": queries,
         "floating_status": res.message, "solver_status": int(res.status),
         "universal_bound_proved": False, "scale": scale}
    if res.x is not None:
        clones = tuple(int(round(x)) for x in res.x)
        if any(abs(float(x) - a) > 1e-5 for x, a in zip(res.x, clones)):
            raise AssertionError("noninteger proposed multiplicity")
        if not cone.verify(clones) or dot(gap, clones) <= 0:
            raise AssertionError("proposed simplified witness fails exact constraints")
        ins = instance_from_clones(p, m, clones)
        cert = StrategyCertificate(actions, cone.root)
        check = verify_certificate(ins, cert)
        check.assert_valid()
        if not independently_verify(cone, clones):
            raise AssertionError("independent every-history IC failed")
        best, values, _ = frozen_max_tuple(ins, path)
        Q = sum(max(row) for row in values)
        W, OPT, Csum = ins.welfare(cone.root), ins.optimal_welfare(), dot(C, clones)
        r.update({"endpoint": ins.to_dict(), "strategy": cert.to_dict(),
                  "W": W, "OPT": OPT, "ratio": Fraction(OPT, W), "true_Q": Q,
                  "Csum": Csum, "true_maximizers": best,
                  "true_signed_StrongA_gap": Q-W-Csum, "refutes_StrongA": Q > W+Csum,
                  "refutes_HALF": OPT > 2*W, "customer_count": ins.customer_count,
                  "positive_types": len(ins.customers),
                  "histories": check.checked_histories, "nonself_IC": check.checked_deviations})
    r["seconds"] = time.monotonic()-started
    return r


if __name__ == "__main__":
    out = HERE / "strong_adjacent_simplified_packet.json"
    if out.exists():
        raise FileExistsError(out)
    r = simplify()
    out.write_text(json.dumps(serializable(r), indent=2)+"\n")
    print(json.dumps(serializable({k:v for k,v in r.items() if k not in ("endpoint", "strategy")})), flush=True)
