"""Original HALF construction attempt, not a universal positive certificate.

The generic candidate has a repeated auxiliary bank and an A,A,B residual
trap, plus m comparison actions. A full-history SPE cone permits *all* nonempty
incidence types; the fixed seed only proposes a truthful policy. LP endpoints
are accepted over Fraction and checked at every ordered history. No git calls.
"""
from pathlib import Path
import sys, json, time
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[6]
sys.path[:0] = [str(ROOT), str(ROOT / "tests/audits")]
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (
    StrategyCone, instance_from_clones, integer_clones, serializable,
    independently_verify,
)

HERE = Path(__file__).resolve().parent


def original_seed(m):
    if m < 4:
        raise ValueError("this is a generic candidate architecture with padding")
    p = m + 3
    weights = {1: 4, 2: 4, 4: 2, 4 | 8: 2, 4 | 16: 2,
               1 | 8 | 16: 6, 2 | 8 | 16: 2, 32: 5 * (m - 3)}
    return instance_from_clones(p, m, tuple(weights.get(mask, 0)
                                          for mask in range(1, 1 << p)))


def attempt(m=5):
    start = time.monotonic()
    ins = original_seed(m)
    p = ins.topic_count
    solver = ExactSPESolver(ins)
    path = (5,) * (m - 3) + (0, 0, 1)
    q = ins.counts(path, terminal=True)
    # This is checked separately for each input. No arbitrary-m padding theorem.
    if q not in solver.outcomes():
        return {"m": m, "stage": "seed_target_not_credible", "q": q}
    cert = solver.certificate(q, on_path=path)
    verify_certificate(ins, cert).assert_valid()
    cone = StrategyCone(p, m, dict(cert.actions))
    J = (2, 3, 4) + tuple(range(6, p))
    if len(J) != m:
        raise AssertionError("comparison uses exactly m legal topics")
    print(json.dumps({"stage": "cone", "m": m, "topics": p,
                      "histories": len(cert.actions), "distinct_IC_rows": len(cone.rows),
                      "source_path": path, "seconds": time.monotonic() - start}), flush=True)
    endpoint = cone.optimize(J)
    meta = {"m": m, "topics": p, "source": ins.to_dict(), "source_path": path,
            "source_utilities": ins.player_payoffs(path), "source_W": ins.welfare(q),
            "source_OPT": ins.optimal_welfare(), "target_comparison": J,
            "all_incidence_types_allowed": (1 << p) - 1,
            "histories": len(cert.actions), "distinct_IC_rows": len(cone.rows),
            "LP_status": endpoint["status"], "universal_bound_proved": False,
            "scope": "one complete full-history strategy cone, original HALF objective"}
    if endpoint["certified"]:
        clones = integer_clones(endpoint["values"])
        target = instance_from_clones(p, m, clones)
        if not independently_verify(cone, clones):
            raise AssertionError("independent every-history exact IC failed")
        report = verify_certificate(target, cert)
        report.assert_valid()
        W = target.welfare(q)
        OPT = target.optimal_welfare()
        meta.update({"endpoint": target.to_dict(), "endpoint_clones": clones,
                     "strategy": cert.to_dict(), "endpoint_utilities": target.player_payoffs(path),
                     "endpoint_W": W, "endpoint_OPT": OPT, "ratio": Fraction(OPT, W),
                     "objective": endpoint["value"], "dual_bound": endpoint["dual_bound"],
                     "dual_optimal": endpoint["dual_optimal"],
                     "dual_support": endpoint["dual_support"],
                     "refutes_HALF": OPT > 2 * W})
    meta["seconds"] = time.monotonic() - start
    return meta


if __name__ == "__main__":
    output = HERE / "bank_upgrade_attempt_m5.json"
    if output.exists():
        raise FileExistsError(output)
    record = attempt(5)
    output.write_text(json.dumps(serializable(record), indent=2) + "\n")
    print(json.dumps(serializable({k: v for k, v in record.items()
                                 if k not in ("source", "endpoint", "endpoint_clones", "strategy",
                                              "dual_support")})), flush=True)
