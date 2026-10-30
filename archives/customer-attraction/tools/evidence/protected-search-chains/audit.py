"""Exact, optimizer-free verification of the six preserved search outputs.

This checker verifies the saved rational points, the partial-chain duals on
their full stated finite atom domains, and whether each partial policy can
be completed while preserving the recorded actual first action. It does not
claim to rerun the historical enumeration of floating-point LPs.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent


def coefficient(mask, background, player_action, terminal):
    if not (mask >> player_action) & 1:
        return F(0)
    return F(1, background + sum((mask >> action) & 1 for action in terminal))


def protected(mask, background):
    return int(background == 0 and mask & 3 == 0 and mask & 12 != 0)


def constraint_coefficient(row, mask, background):
    if row[0] == "tail":
        _, first, reply, deviation = row
        return (coefficient(mask, background, reply, (first, reply))
                - coefficient(mask, background, deviation, (first, deviation)))
    assert row[0] == "root"
    _, deviation, reply = row
    return (coefficient(mask, background, 0, (0, 1))
            - coefficient(mask, background, deviation, (deviation, reply)))


def rows_from_replies(p, replies):
    rows = []
    for first, reply in replies.items():
        rows.extend(("tail", first, reply, other) for other in range(p) if other != reply)
        if first:
            rows.append(("root", first, reply))
    return rows


def check_record(name, partial):
    path = BASE / "original" / name
    raw = path.read_bytes()
    record = json.loads(raw)
    p, bmax = record["p"], record["bmax"]
    saved = record if partial else record["best"]
    support = [(int(t["mask"]), int(t["b"]), F(t["mass"])) for t in saved["support"]]
    assert len({(m, b) for m, b, _ in support}) == len(support)
    assert all(0 < m < 1 << p and 0 <= b <= bmax and w > 0 for m, b, w in support)
    if partial:
        depth = record["depth"]
        assert p == 2 + 2 * (depth + 1)
        replies = {0: 1}
        for level in range(depth):
            for chain in range(2):
                a = 2 + 2 * level + chain
                replies[a] = a + 2
    else:
        assert len(saved["reply"]) == p and saved["reply"][0] == 1
        replies = dict(enumerate(saved["reply"]))
    rows = rows_from_replies(p, replies)

    def payoff(query, terminal):
        return sum((w * coefficient(m, b, query, terminal) for m, b, w in support), F())

    first_payoff = payoff(0, (0, 1))
    last_payoff = payoff(1, (0, 1))
    W = first_payoff + last_payoff
    D = sum((w * protected(m, b) for m, b, w in support), F())
    assert W == 1
    slacks = [sum((w * constraint_coefficient(row, m, b) for m, b, w in support), F())
              for row in rows]
    assert min(slacks) >= 0
    gamma = D / W

    # Every last-player action is kept, including repetitions and all ties.
    # For an omitted first action, a completion exists iff at least one true
    # last-player best reply leaves the first player no more than actual u.
    matrix = [[payoff(last, (first, last)) for last in range(p)] for first in range(p)]
    completion = []
    obstruction = []
    for first in range(p):
        best = max(matrix[first])
        best_actions = [a for a, value in enumerate(matrix[first]) if value == best]
        first_values = [payoff(first, (first, a)) for a in best_actions]
        admissible = [a for a, value in zip(best_actions, first_values) if value <= first_payoff]
        entry = {"first": first, "last_best_payoff": str(best), "best_replies": best_actions,
                 "first_payoffs_against_best_replies": list(map(str, first_values)),
                 "root_compatible_best_replies": admissible}
        completion.append(entry)
        if first not in replies and not admissible:
            obstruction.append({"first": first, "minimum_first_payoff": str(min(first_values)),
                                "strict_root_gain": str(min(first_values) - first_payoff),
                                "best_replies": best_actions})
        if first in replies:
            assert replies[first] in admissible

    scale = lcm(*(w.denominator for _, _, w in support))
    out = {
        "name": name, "source_sha256": sha256(raw).hexdigest(), "p": p, "bmax": bmax,
        "support_types": len(support), "unit_scale": scale,
        "scaled_customers": int(scale * sum((w for _, _, w in support), F())),
        "actual_first_profit": str(first_payoff), "actual_last_profit": str(last_payoff),
        "actual_tail_profit": str(W), "protected_mass": str(D), "ratio": str(gamma),
        "reported_float": saved["value"], "recorded_reply_map": {str(k): v for k, v in replies.items()},
        "nonself_constraints": len(rows), "minimum_exact_slack": str(min(slacks)),
        "zero_slacks": slacks.count(F()), "positive_slacks": sum(x > 0 for x in slacks),
        "all_constraint_slacks": [{"row": list(r), "slack": str(s)} for r, s in zip(rows, slacks)],
        "last_payoff_matrix": [[str(x) for x in row] for row in matrix],
        "completion_by_first_action": completion,
        "partial_policy_completable_with_actual_AB": not obstruction,
        "unavoidable_root_deviations": obstruction,
        "all_catalog_labels_hit_some_fresh_positive_mass":
            all(any(b == 0 and (m >> a) & 1 for m, b, w in support) for a in range(p)),
    }
    if partial:
        assert record["atoms"] == ((1 << p) - 1) * (bmax + 1)
        assert record["rows"] == len(rows)
        weights = {tuple(t["row"]): F(t["multiplier"]) for t in saved["dual"]}
        assert len(weights) == len(saved["dual"])
        assert all(row in rows and weight > 0 for row, weight in weights.items())
        coefficients = []
        for mask in range(1, 1 << p):
            for background in range(bmax + 1):
                w = (coefficient(mask, background, 0, (0, 1))
                     + coefficient(mask, background, 1, (0, 1)))
                remainder = (gamma * w - protected(mask, background)
                             - sum((weight * constraint_coefficient(row, mask, background)
                                    for row, weight in weights.items()), F()))
                assert remainder >= 0, (name, mask, background, remainder)
                coefficients.append((mask, background, remainder))
        assert all(weights.get(row, F()) * slack == 0 for row, slack in zip(rows, slacks))
        remainder_by_atom = {(m, b): value for m, b, value in coefficients}
        assert all(remainder_by_atom[(m, b)] == 0 for m, b, w in support)
        out["exact_dual"] = {
            "gamma": str(gamma), "nonzero_row_multipliers": len(weights),
            "checked_atoms": len(coefficients), "minimum_remainder": str(min(x[2] for x in coefficients)),
            "zero_remainders": sum(x[2] == 0 for x in coefficients),
            "positive_remainders": sum(x[2] > 0 for x in coefficients),
            "primal_and_dual_complementarity": True,
            "all_atom_remainders": [{"mask": m, "b": b, "remainder": str(v)}
                                    for m, b, v in coefficients],
        }
    return out


def main():
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    for row in manifest["primary_sources"]:
        data = (BASE / row["preserved_relative_path"]).read_bytes()
        assert len(data) == row["size"] and sha256(data).hexdigest() == row["sha256"]
    names = [
        ("protected_two_p4b5.json", False), ("protected_two_p5b3.json", False),
        ("protected_two_p6b1.json", False), ("protected_chain_d1.json", True),
        ("protected_chain_d2.json", True), ("protected_chain_d3.json", True),
    ]
    results = [check_record(name, partial) for name, partial in names]
    output = BASE / "replay"
    output.mkdir(exist_ok=True)
    for row in results:
        (output / row["name"]).write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n")
    summary = []
    for row in results:
        keys = ["name", "support_types", "unit_scale", "scaled_customers", "actual_first_profit",
                "actual_last_profit", "protected_mass", "ratio", "nonself_constraints",
                "zero_slacks", "positive_slacks", "unavoidable_root_deviations",
                "all_catalog_labels_hit_some_fresh_positive_mass"]
        item = {key: row[key] for key in keys}
        if "exact_dual" in row:
            item["exact_dual"] = {k: v for k, v in row["exact_dual"].items() if k != "all_atom_remainders"}
        summary.append(item)
    report = {"status": "exact-saved-certificate-verification-passed",
              "historical_lp_search_rerun": False, "cases": summary}
    (output / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
