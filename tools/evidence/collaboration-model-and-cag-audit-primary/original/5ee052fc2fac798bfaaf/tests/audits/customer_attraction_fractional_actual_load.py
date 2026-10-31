"""Unit-client full-history audit of the fractional actual-load counterexample.

Only Python standard library; default prints, --output refuses overwrites.
The universal family is justified analytically in the linked current account.
"""
import argparse
from functools import lru_cache
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
    covered_query = sum((1 / (1 + alpha*c) for c in loads if c), F(0))
    exact_tax_gap = W + covered_query - m*M
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
            "covered_query_G_C": str(covered_query),
            "exact_tax_bridge_gap": str(exact_tax_gap),
            "weak_bridge_gap": str(gap),
            "weak_bridge_ratio": str(F(2*m-1, 2) * M / W) if W else None,
            "half_gap_2W_minus_OPT": 2*W-optimum,
            "all_history_rows": rows}


@lru_cache(None)
def bonus(r, q, e):
    """Finite BI for two unit-reward singleton resources; returns action/endloads."""
    if r == 0:
        return None, (q, e)
    _, end_q = bonus(r-1, q+1, e)
    _, end_d = bonus(r-1, q, e+1)
    if F(1, end_q[0]) >= F(1, end_d[1]):
        return 2, end_q
    return 3, end_d


def construct(m):
    game = {"topics": ["A", "B", "Q", "D"], "players": m,
            "customers": [{"topics": [0], "multiplicity": m-1},
                          {"topics": [2], "multiplicity": 1},
                          {"topics": [0, 3], "multiplicity": 1},
                          {"topics": [1, 2, 3], "multiplicity": m*(m-1)}]}
    rows = []
    for t in range(m):
        for h in product(range(4), repeat=t):
            a, b, q, d = (h.count(j) for j in range(4))
            if b == t:
                chosen = 1 if t < m-1 else 0
            else:
                chosen, _ = bonus(m-t, q, a+d)
            rows.append({"history": list(h), "action": chosen})
    return game, {"terminal_counts": [1, m-1, 0, 0], "actions": rows}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-players", type=int, default=6,
                        help="full family trees m=2,...,this value; default6")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.max_players < 2:
        parser.error("--max-players must be at least2")
    root = Path(__file__).resolve().parents[2]
    game = json.loads((root / "examples/customer_attraction/fractional_actual_load_failure.json").read_text())
    certificate = json.loads((root / "evidence/certificates/customer_attraction/fractional_actual_load_failure.json").read_text())
    concrete = audit(game, certificate)
    empty = audit(dict(game, customers=[]), certificate)
    assert empty["W"] == empty["OPT"] == 0 and empty["M"] == "0"
    try:
        audit(game, dict(certificate, actions=certificate["actions"][:-1]))
    except AssertionError:
        pass
    else:
        raise AssertionError("incomplete strategy accepted")
    families = []
    for m in range(2, args.max_players+1):
        family_game, family_certificate = construct(m)
        result = audit(family_game, family_certificate)
        result.pop("all_history_rows")
        delta = m*m-m+1
        assert F(result["M"]) == 1 + F(m*m*(m-1), delta)
        assert F(result["weak_bridge_gap"]) == F(m**3-4*m*m+3*m-1, 2*delta)
        assert result["W"] == m*m and result["OPT"] == m*m+1
        assert 2*delta*F(result["weak_bridge_gap"]) == m*m*(m-4)+3*m-1
        assert F(result["exact_tax_bridge_gap"]) == F(m*(m-1), delta) + F(m*m, 2*m-1)
        assert result["half_gap_2W_minus_OPT"] == m*m-1
        if m >= 4:
            assert F(result["weak_bridge_gap"]) > 0
        families.append(result)
    result = {"claim": "CA-FRACTIONAL-ACTUAL-LOAD-WEAK-NO-v1",
              "concrete_full_history_audit": concrete,
              "family_full_history_audits": families,
              "zero_customer_boundary_checked": True,
              "incomplete_strategy_rejected": True,
              "limitations": "Finite full-tree audits check the displayed construction; the arbitrary-m conclusion uses the analytic proof, not enumeration. No external review or novelty certification."}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    summary = dict(result)
    summary["concrete_full_history_audit"] = {k: v for k, v in concrete.items() if k != "all_history_rows"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
