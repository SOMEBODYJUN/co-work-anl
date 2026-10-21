"""Definition-level unit-customer audit; imports no CAG implementation/solver."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def audit(game, certificate):
    m, p = game["players"], len(game["topics"])
    assert m >= 1 and p >= 1
    units = [frozenset(row["topics"]) for row in game["customers"]
             for _ in range(row["multiplicity"])]
    assert all(all(type(a) is int and 0 <= a < p for a in x) for x in units)
    entries = certificate["actions"]
    actions = {tuple(row["history"]): row["action"] for row in entries}
    required = {h for t in range(m) for h in product(range(p), repeat=t)}
    assert len(entries) == len(actions) and set(actions) == required
    assert all(type(a) is int and 0 <= a < p for a in actions.values())

    def finish(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def payoffs(z):
        out = [F(0)] * m
        for x in units:
            users = [i for i, a in enumerate(z) if a in x]
            for i in users:
                out[i] += F(1, len(users))
        return tuple(out)

    def welfare(z):
        return sum(any(a in x for a in z) for x in units)

    rows, slacks = [], []
    for h in sorted(required, key=lambda x: (len(x), x)):
        i, chosen = len(h), actions[h]
        values = [payoffs(finish(h + (a,)))[i] for a in range(p)]
        own = values[chosen]
        assert all(own >= value for value in values)
        slacks.extend(own - value for a, value in enumerate(values) if a != chosen)
        rows.append({"history": list(h), "chosen": chosen,
                     "branch_payoffs": list(map(str, values))})
    z = finish(())
    counts = tuple(z.count(a) for a in range(p))
    assert counts == tuple(certificate["terminal_counts"])
    u, W = payoffs(z), welfare(z)
    assert sum(u) == W
    alpha = F(m-1, m)
    loads = [sum(a in x for a in z) for x in units]
    queries = [sum((1 / (1 + alpha * c) for x, c in zip(units, loads)
                    if a in x), F(0)) for a in range(p)]
    M = max(queries)
    gap = F(2*m-1, 2) * M - W
    optimum = max(welfare(other) for other in product(range(p), repeat=m))
    # Check the sufficient bridge's algebra separately, on every comparison tuple.
    for other in product(range(p), repeat=m):
        rhs = sum((queries[a] for a in other), F(0))
        rhs += sum((alpha*c / (1 + alpha*c) for c in loads), F(0))
        assert welfare(other) <= rhs <= (2*m-1) * M
    return {"customers": len(units), "players": m, "topics": p,
            "ordered_decision_nodes": len(required),
            "proper_action_comparisons": len(slacks),
            "minimum_spe_slack": str(min(slacks, default=F(0))),
            "on_path": list(z), "terminal_counts": list(counts),
            "player_payoffs": list(map(str, u)), "W": W, "OPT": optimum,
            "query_values": list(map(str, queries)), "M": str(M),
            "weak_bridge_gap": str(gap),
            "weak_bridge_ratio": str(F(2*m-1, 2) * M / W) if W else None,
            "half_gap_2W_minus_OPT": 2*W-optimum,
            "all_history_rows": rows}


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1] / "true_spe_search"
    game = json.loads((base / "fractional_weak_m4_instance.json").read_text())
    certificate = json.loads((base / "fractional_weak_m4_certificate.json").read_text())
    result = audit(game, certificate)
    # Edge check: removing all customers preserves a full-history strategy as SPE.
    empty = dict(game, customers=[])
    edge = audit(empty, certificate)
    assert edge["W"] == edge["OPT"] == 0 and edge["M"] == "0"
    result["zero_customer_boundary_checked"] = True
    # Negative check: incomplete maps are not full SPE certificates.
    bad = dict(certificate, actions=certificate["actions"][:-1])
    try:
        audit(game, bad)
    except AssertionError:
        result["incomplete_strategy_rejected"] = True
    else:
        raise AssertionError("incomplete strategy accepted")
    destination = Path(__file__).with_name("fractional_weak_m4_audit.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "all_history_rows"}, indent=2))
