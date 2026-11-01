"""Refit one credible policy toward repeated distinct-action punishment.

The objective is the original OPT>2W construction. This finite computation is
not evidence of a positive theorem and does not enumerate all policies. Every
candidate policy is assembled from canonical *all* pure SPE outcome menus,
then independently checked at every ordered history after exact LP recovery.
"""
from pathlib import Path
from functools import lru_cache
from fractions import Fraction
import json, sys, time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(ROOT), str(ROOT / "tests/audits")]
from customer_attraction import Instance, ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, instance_from_clones,
    integer_clones, independently_verify, serializable)


def inc(k, a):
    return tuple(x + (i == a) for i, x in enumerate(k))


def attempt():
    started = time.monotonic()
    source_record = json.loads((HERE / "bank_upgrade_attempt_m5.json").read_text())
    ins = Instance.from_dict(source_record["endpoint"])
    p, m = ins.topic_count, ins.players
    path = tuple(source_record["source_path"])
    target = ins.counts(path, terminal=True)
    actual_support = {a for a, x in enumerate(target) if x}
    missing_types = tuple(c for c in ins.customers if c.topics.isdisjoint(actual_support))
    sol = ExactSPESolver(ins)
    if target not in sol.outcomes():
        raise AssertionError("source endpoint lost its exact SPE")

    @lru_cache(None)
    def score(a, q):
        # Same omitted unit customers, counted on all *different* covering actions.
        upgrade = sum(c.multiplicity * sum(q[b] for b in c.topics if b != a)
                      for c in missing_types if a in c.topics)
        distinct = sum(q[b] > 0 for b in range(p) if b != a)
        return (upgrade, distinct, ins.welfare(q), -sol._utility(q, a))

    actions = {}
    nonminimal = strict_upgrades = 0

    def expand(h, k, desired):
        nonlocal nonminimal, strict_upgrades
        if len(h) == m:
            if k != desired:
                raise AssertionError("terminal mismatch")
            return
        floor = sol.threshold(k)
        options = tuple(a for a in range(p) if desired in sol.outcomes(inc(k, a))
                        and sol._utility(desired, a) >= floor)
        chosen = path[len(h)] if h == path[:len(h)] else min(
            options, key=lambda a: (sol._utility(desired, a), a))
        if chosen not in options:
            raise AssertionError("forced actual path is not credible")
        actions[h] = chosen
        actual = sol._utility(desired, chosen)
        for a in range(p):
            child = inc(k, a)
            if a == chosen:
                nxt = desired
            else:
                all_outcomes = sol.outcomes(child)
                menu = tuple(q for q in all_outcomes if sol._utility(q, a) <= actual)
                if not menu:
                    raise AssertionError("credible child menu empty")
                nxt = max(menu, key=lambda q: (score(a, q), q))
                nonminimal += int(sol._utility(nxt, a) > min(sol._utility(q, a)
                                                            for q in all_outcomes))
                strict_upgrades += int(score(a, nxt)[0] > 0)
            expand(h + (a,), child, nxt)

    expand((), (0,) * p, target)
    cert = StrategyCertificate(actions, target)
    verify_certificate(ins, cert).assert_valid()
    cone = StrategyCone(p, m, actions)
    print(json.dumps({"stage": "repeated_upgrade_cone", "histories": len(actions),
                      "rows": len(cone.rows), "nonminimal_children": nonminimal,
                      "children_with_omitted_upgrade_crowding": strict_upgrades,
                      "seconds": time.monotonic() - started}), flush=True)
    J = tuple(source_record["target_comparison"])
    res = cone.optimize(J)
    result = {"scope": "one refitted all-history pure SPE policy; original HALF objective",
              "universal_bound_proved": False, "source_file": "bank_upgrade_attempt_m5.json",
              "source_path": path, "target_comparison": J, "m": m, "topics": p,
              "histories": len(actions), "distinct_IC_rows": len(cone.rows),
              "nonminimal_children": nonminimal,
              "children_with_omitted_upgrade_crowding": strict_upgrades,
              "strategy": cert.to_dict(), "LP_status": res["status"]}
    if res["certified"]:
        clones = integer_clones(res["values"])
        endpoint = instance_from_clones(p, m, clones)
        if not independently_verify(cone, clones):
            raise AssertionError("independent exact every-history IC failed")
        verify_certificate(endpoint, cert).assert_valid()
        W, OPT = endpoint.welfare(target), endpoint.optimal_welfare()
        result.update({"endpoint": endpoint.to_dict(), "endpoint_clones": clones,
                       "endpoint_utilities": endpoint.player_payoffs(path), "W": W, "OPT": OPT,
                       "ratio": Fraction(OPT, W), "objective": res["value"],
                       "dual_bound": res["dual_bound"], "dual_optimal": res["dual_optimal"],
                       "dual_support": res["dual_support"], "refutes_HALF": OPT > 2 * W})
    result["seconds"] = time.monotonic() - started
    return result


if __name__ == "__main__":
    out = HERE / "repeated_upgrade_attempt_m5.json"
    if out.exists():
        raise FileExistsError(out)
    result = attempt()
    out.write_text(json.dumps(serializable(result), indent=2) + "\n")
    print(json.dumps(serializable({k: v for k, v in result.items()
        if k not in ("strategy", "endpoint", "endpoint_clones", "dual_support")})), flush=True)
