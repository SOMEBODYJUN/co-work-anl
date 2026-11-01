"""Attack parent's StrongA in one already available full-history SPE cone.

StrongA is Q-W<=Csum, where Q is the sum of frozen best-response profits and
Csum charges actual adjacent-topic losses by 1/[c(c+1)]. The maximizer tuple
is fixed at the already accepted endpoint; LP does not enumerate new policies.
Only an exact feasible positive gap would refute StrongA, never HALF itself.
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
from customer_attraction_strategy_lp import (StrategyCone, integer_clones,
    instance_from_clones, independently_verify, serializable, dot)


def frozen_row(p, path, i, topic):
    q = tuple(path.count(a) for a in range(p))
    return tuple(Fraction(1, 1 + sum(q[a] for a in range(p) if mask & (1 << a))
                               - bool(mask & (1 << path[i])))
                 if mask & (1 << topic) else Fraction(0)
                 for mask in range(1, 1 << p))


def adjacent_row(p, path):
    q = tuple(path.count(a) for a in range(p))
    out = []
    for mask in range(1, 1 << p):
        c = sum(q[a] for a in range(p) if mask & (1 << a))
        losses = sum(bool(mask & (1 << a)) and not bool(mask & (1 << b))
                     for a, b in zip(path, path[1:]))
        out.append(Fraction(losses, c * (c + 1)) if c else Fraction(0))
    return tuple(out)


def frozen_max_tuple(ins, path):
    p, m = ins.topic_count, ins.players
    clones = [0] * ((1 << p) - 1)
    for c in ins.customers:
        mask = sum(1 << a for a in c.topics)
        clones[mask - 1] = c.multiplicity
    values = tuple(tuple(dot(frozen_row(p, path, i, a), clones) for a in range(p))
                   for i in range(m))
    queries = tuple(max(range(p), key=lambda a: (values[i][a], -a)) for i in range(m))
    return queries, values, tuple(clones)


def attack():
    started = time.monotonic()
    filename = "repeated_upgrade_attempt_m5.json"
    source = json.loads((HERE / filename).read_text())
    ins = Instance.from_dict(source["endpoint"])
    p, m = ins.topic_count, ins.players
    path = tuple(source["source_path"])
    queries, source_values, clones = frozen_max_tuple(ins, path)
    actions = {tuple(x["history"]): x["action"] for x in source["strategy"]["actions"]}
    cone = StrategyCone(p, m, actions)
    if cone.root != ins.counts(path, terminal=True):
        raise AssertionError("actual ordered path does not match source policy")
    C = adjacent_row(p, path)
    Q = tuple(sum(frozen_row(p, path, i, queries[i])[j] for i in range(m))
              for j in range((1 << p) - 1))
    gap = tuple(q - w - c for q, w, c in zip(Q, cone.welfare, C))
    source_gap = dot(gap, clones)
    res = linprog(-np.array(gap, dtype=float), A_ub=-cone.matrix,
                  b_ub=np.zeros(len(cone.rows)),
                  A_eq=np.array([cone.welfare], dtype=float), b_eq=[1],
                  bounds=(0, None), method="highs")
    result = {"candidate": "StrongA: sum_i max_T frozen_f_i(T)-W <= adjacent_Csum",
              "scope": "one fixed already available full-history pure SPE cone and frozen-query tuple",
              "source_file": filename, "m": m, "topics": p, "actual_path": path,
              "fixed_queries": queries, "source_frozen_payoffs": source_values,
              "source_W": ins.welfare(cone.root), "source_Csum": dot(C, clones),
              "source_Q": dot(Q, clones), "source_signed_gap": source_gap,
              "floating_status": res.message, "refutes_HALF": False,
              "universal_bound_proved": False}
    if res.success:
        point = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
        if not cone.verify(point) or dot(cone.welfare, point) != 1:
            point = cone.recover_vertex(res.x)
        if point is not None and cone.verify(point) and dot(cone.welfare, point) == 1:
            endpoint_clones = integer_clones(point)
            target = instance_from_clones(p, m, endpoint_clones)
            cert = StrategyCertificate(actions, cone.root)
            check = verify_certificate(target, cert)
            check.assert_valid()
            if not independently_verify(cone, endpoint_clones):
                raise AssertionError("independent every-history IC failed")
            best, final_values, final_clones = frozen_max_tuple(target, path)
            true_Q = sum(max(row) for row in final_values)
            W, OPT = target.welfare(cone.root), target.optimal_welfare()
            fixed_gap, Csum = dot(gap, final_clones), dot(C, final_clones)
            strong_gap = true_Q - W - Csum
            beta = Fraction(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
            dual = tuple(Fraction(float(-x)).limit_denominator(10**7)
                         for x in res.ineqlin.marginals)
            dual_ok = all(v >= 0 for v in dual) and all(
                beta * w - sum(mu * row[j] for mu, row in zip(dual, cone.rows)) >= g
                for j, (w, g) in enumerate(zip(cone.welfare, gap)))
            result.update({"exact_primal": True, "endpoint": target.to_dict(),
                           "strategy": cert.to_dict(), "W": W, "OPT": OPT,
                           "ratio": Fraction(OPT, W), "fixed_query_signed_gap": fixed_gap,
                           "normalized_fixed_gap": dot(gap, point), "Csum": Csum,
                           "true_Q": true_Q, "true_maximizers": best,
                           "true_signed_StrongA_gap": strong_gap,
                           "refutes_StrongA": strong_gap > 0,
                           "refutes_HALF": OPT > 2 * W,
                           "all_history_check": {"histories": check.checked_histories,
                                                 "nonself_IC": check.checked_deviations},
                           "fixed_query_dual_bound": beta if dual_ok else None,
                           "dual_support": tuple((j, x) for j, x in enumerate(dual) if x)
                                           if dual_ok else ()})
        else:
            result["exact_primal"] = False
    result["seconds"] = time.monotonic() - started
    return result


if __name__ == "__main__":
    out = HERE / "strong_adjacent_gap_attack.json"
    if out.exists():
        raise FileExistsError(out)
    r = attack()
    out.write_text(json.dumps(serializable(r), indent=2) + "\n")
    print(json.dumps(serializable({k: v for k, v in r.items() if k not in
        ("endpoint", "strategy", "dual_support", "source_frozen_payoffs")})), flush=True)
