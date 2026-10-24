"""Definition-level diagnostic for the peer prefix-request target cap.

This is a probe of one stated general candidate on previously saved complete
SPE strategies, not an SPE enumeration or a proof of that candidate.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import itertools
import json

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent


def probe(name, instance, strategy):
    m = instance["players"]
    k = len(instance["topics"])
    clients = [(frozenset(t["topics"]), t.get("multiplicity", 1))
               for t in instance["customers"]]
    if "strategy" in strategy:
        strategy = strategy["strategy"]
    policy = {tuple(t["history"]): t["action"] for t in strategy["actions"]}
    expected = sum(k**d for d in range(m))
    if len(policy) != expected:
        return {"name": name, "status": "skipped_incomplete", "nodes": len(policy)}

    @lru_cache(None)
    def leaf(h):
        h = tuple(h)
        while len(h) < m:
            h += (policy[h],)
        return h

    @lru_cache(None)
    def counts(z):
        return tuple(sum(a in B for a in z) for B, _ in clients)

    @lru_cache(None)
    def action_payoff(a, c):
        return sum((F(w, d) for (B, w), d in zip(clients, c) if a in B), F())

    def payoff(j, z, c):
        return action_payoff(z[j], c)

    # Re-check complete SPE by replaying each true child, without importing BI.
    checks = 0
    for h, a in policy.items():
        j = len(h)
        z = leaf(h)
        u = payoff(j, z, counts(z))
        for t in range(k):
            y = leaf(h + (t,))
            assert u >= payoff(j, y, counts(y)), (name, h, t)
            checks += 1

    b = leaf(())
    cb = counts(b)
    ub = [payoff(j, b, cb) for j in range(m)]
    children = []
    for i in range(1, m):
        for t in range(k):
            y = leaf(b[:i] + (t,))
            cy = counts(y)
            uy = [payoff(j, y, cy) for j in range(i)]
            children.append((i, t, y, cy, uy))

    targets = []
    for ell in range(1, m):
        total = F()
        selected = []
        for j in range(ell):
            best = (F(), None)
            for i, t, y, cy, uy in children:
                if not (j < i <= ell):
                    continue
                q = sum((F(w, old * new)
                         for (B, w), old, new in zip(clients, cb, cy)
                         if b[j] in B and b[ell] in B and y[ell] not in B), F())
                if not uy[j]:
                    assert not q
                    ratio = F()
                else:
                    ratio = q / uy[j]
                if ratio > best[0]:
                    best = (ratio, (i, t, y, q, uy[j]))
            total += ub[j] * best[0]
            if best[1] is not None:
                i, t, y, q, u = best[1]
                selected.append({"source_j": j + 1, "cut_i": i + 1,
                                 "forced_topic": t, "leaf": y,
                                 "q": str(q), "source_branch_profit": str(u),
                                 "lambda": str(ub[j] / u),
                                 "target_credit": str(ub[j] * best[0])})
        targets.append({"target_l": ell + 1, "tail_players": m - ell - 1,
                        "maximum_requested_q": str(total),
                        "actual_profit": str(ub[ell]),
                        "ratio_to_actual_profit": str(total / ub[ell]) if ub[ell] else None,
                        "cap2_slack": str(2 * ub[ell] - total),
                        "witness": selected})
    return {"name": name, "status": "complete_SPE_replayed", "spe_checks": checks,
            "actual_leaf": b, "actual_profits": list(map(str, ub)), "targets": targets}


def main():
    names = ["root_tax_failure", "fractional_actual_load_failure", "prefix_balance_failure",
             "global_decorrelation_failure", "individual_security_failure",
             "worst_pne_welfare_failure", "worst_cce_welfare_failure",
             "eight_cce_welfare_gap", "aggregate_theta_failure", "collision_free_occupancy"]
    records = []
    for name in names:
        p = ROOT / "examples/customer_attraction" / (name + ".json")
        q = ROOT / "evidence/certificates/customer_attraction" / (name + ".json")
        if p.exists() and q.exists():
            records.append(probe(name, json.loads(p.read_text()), json.loads(q.read_text())))
    old = json.loads((ROOT / "history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json").read_text())
    instance = {"players": old["n"], "topics": list(range(old["m"])),
                "customers": [{"topics": [a for a in range(old["m"]) if int(mask) >> a & 1],
                               "multiplicity": w} for mask, w in old["weights"].items()]}
    records.append(probe("uploaded_auxiliary_floor_failure", instance, {"actions": old["policy"]}))
    output = HERE / "prefix_request_cap_old_certificates.json"
    output.write_text(json.dumps({"claim": "peer prefix-request cap2, still OPEN", "records": records}, indent=2) + "\n")
    for row in records:
        print(row["name"], row["status"], [(t["target_l"], t["ratio_to_actual_profit"])
              for t in row.get("targets", [])], flush=True)


if __name__ == "__main__":
    main()
