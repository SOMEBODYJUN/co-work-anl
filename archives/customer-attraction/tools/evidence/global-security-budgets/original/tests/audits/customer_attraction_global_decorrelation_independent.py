"""Independent exact audit of the uploaded 89-customer certificate.

This file never executes or imports the uploaded checker or any repository
checker.  Only the WEIGHTS and POLICY literal assignments are parsed with AST.
Payoffs are recomputed directly by customer-interest types using Fraction.
"""
from __future__ import annotations

import ast
import argparse
import hashlib
import json
import re
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "history/source/notes/customer_attraction/uploaded_pro_2026-10-10/global_security_source.md"
F = Fraction


def certificate_literals():
    if not SOURCE.exists():
        snapshot = json.loads((HERE / "certificate_data.json").read_text())
        return {int(t): w for t, w in snapshot["weights"].items()}, snapshot["policy"]
    text = SOURCE.read_text()
    blocks = re.findall(r"```python\n(.*?)```", text, flags=re.S)
    if len(blocks) != 1:
        raise ValueError("Expected the single published Python certificate block")
    syntax = ast.parse(blocks[0])
    values = {}
    for node in syntax.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("WEIGHTS", "POLICY"):
                    values[target.id] = ast.literal_eval(node.value)
    if set(values) != {"WEIGHTS", "POLICY"}:
        raise ValueError("Missing the exact literal customer or policy certificate")
    return values["WEIGHTS"], values["POLICY"]


class TypeGame:
    def __init__(self, m, n, weights, encoded):
        if not (isinstance(m, int) and m >= 1 and isinstance(n, int) and n >= 1):
            raise ValueError("Invalid game dimensions")
        if any(not isinstance(t, int) or not 0 < t < 2**m or
               not isinstance(w, int) or w <= 0 for t, w in weights.items()):
            raise ValueError("Invalid positive unit-customer type multiplicity")
        self.m, self.n = m, n
        self.types = tuple((tuple(a for a in range(m) if t & (1 << a)), w)
                           for t, w in sorted(weights.items()))
        self.weights = weights
        self.histories = tuple(h for k in range(n) for h in product(range(m), repeat=k))
        if len(encoded) != len(self.histories):
            raise ValueError("Incomplete policy")
        if any(c not in "0123456789" or int(c) >= m for c in encoded):
            raise ValueError("Invalid action encoding")
        self.policy = dict(zip(self.histories, map(int, encoded)))
        self.leaves = {}
        self.payoffs = {}
        # Explicitly unfold each ordered history; never identify by action counts.
        for h in self.histories:
            q = list(h)
            while len(q) < n:
                q.append(self.policy[tuple(q)])
            self.leaves[h] = tuple(q)
        for z in product(range(m), repeat=n):
            utility = [F(0) for _ in range(n)]
            covered = 0
            for interested, weight in self.types:
                people = [i for i, a in enumerate(z) if a in interested]
                if people:
                    covered += weight
                    share = F(weight, len(people))
                    for i in people:
                        utility[i] += share
            if sum(utility) != covered:
                raise AssertionError("Customer shares fail welfare conservation")
            self.payoffs[z] = tuple(utility), covered

    def terminal(self, h):
        return tuple(h) if len(h) == self.n else self.leaves[tuple(h)]

    def static(self, a, rivals):
        # A fresh direct calculation, independent of the full-outcome payoff table.
        out = F(0)
        for interested, weight in self.types:
            if a in interested:
                rival_load = sum(b in interested for b in rivals)
                out += F(weight, 1 + rival_load)
        return out

    def audit_spe(self):
        rows = []
        for h in self.histories:
            player = len(h)
            chosen = self.policy[h]
            original = self.terminal(h)
            current = self.payoffs[original][0][player]
            for a in range(self.m):
                deviated = self.terminal(h + (a,))
                alternative = self.payoffs[deviated][0][player]
                rows.append((h, a, original, deviated, current - alternative))
        return rows


def as_json(obj):
    if isinstance(obj, Fraction):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): as_json(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [as_json(v) for v in obj]
    return obj


def boundary_checks():
    cases = {}
    one = TypeGame(1, 1, {1: 1}, "0")
    cases["one_player_one_customer"] = {
        "SPE": all(row[-1] >= 0 for row in one.audit_spe()),
        "outcome": one.terminal(()), "utility": one.payoffs[(0,)][0],
    }
    empty = TypeGame(1, 3, {}, "000")
    cases["three_players_zero_customers"] = {
        "SPE": all(row[-1] >= 0 for row in empty.audit_spe()),
        "utility": empty.payoffs[empty.terminal(())][0],
        "all_static_queries_zero": all(empty.static(0, b) == 0
                                       for b in product(range(1), repeat=2)),
    }
    two = TypeGame(2, 2, {1: 1, 2: 1}, "110")
    cases["two_disjoint_topics_valid_policy"] = {
        "SPE": all(row[-1] >= 0 for row in two.audit_spe()),
        "outcome": two.terminal(()), "utility": two.payoffs[two.terminal(())][0],
        "min_comparison_slack": min(row[-1] for row in two.audit_spe()),
    }
    bad = TypeGame(2, 2, {1: 1, 2: 1}, "000")
    failures = [row for row in bad.audit_spe() if row[-1] < 0]
    cases["deliberately_non_SPE_policy"] = {
        "rejected": bool(failures),
        "violations": [{"history": r[0], "deviation": r[1], "slack": r[-1]}
                       for r in failures],
    }
    # The one-player boundary uses f_empty, and equals maximum topic coverage.
    asymmetric = TypeGame(2, 1, {1: 1, 2: 2}, "1")
    cases["one_player_nontrivial_catalogue"] = {
        "SPE": all(row[-1] >= 0 for row in asymmetric.audit_spe()),
        "W_equals_security_equals_OPT": asymmetric.payoffs[(1,)][1]
        == max(asymmetric.static(a, ()) for a in range(2)) == 2,
    }
    assert cases["one_player_one_customer"]["SPE"]
    assert cases["three_players_zero_customers"]["SPE"]
    assert cases["three_players_zero_customers"]["all_static_queries_zero"]
    assert cases["two_disjoint_topics_valid_policy"]["SPE"]
    assert cases["deliberately_non_SPE_policy"]["rejected"]
    assert cases["one_player_nontrivial_catalogue"]["W_equals_security_equals_OPT"]
    return cases


def main():
    global HERE
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    HERE = args.output_dir
    HERE.mkdir(parents=True, exist_ok=False)
    weights, encoded = certificate_literals()
    game = TypeGame(6, 4, weights, encoded)
    checks = game.audit_spe()
    violations = [r for r in checks if r[-1] < 0]
    assert not violations
    positive = [r[-1] for r in checks if r[-1] > 0]

    # Distinctness follows by signatures of positive customer-interest types.
    topic_signatures = [tuple(t for t in sorted(weights) if t & (1 << a))
                        for a in range(6)]
    assert len(set(topic_signatures)) == 6
    coverages = [sum(weights[t] for t in signature) for signature in topic_signatures]
    outcome = game.terminal(())
    utility, W = game.payoffs[outcome]
    p_hat = (F(0), F(1, 2), F(1, 2), F(0), F(0), F(0))
    menu_details, decorrelation = [], []
    for i in range(4):
        h = outcome[:i]
        menus = []
        for b in range(6):
            branch = game.terminal(h + (b,))
            rivals = branch[:i] + branch[i + 1:]
            menus.append(rivals)
            assert game.static(b, rivals) == game.payoffs[branch][0][i]
        D = sum(p_hat[a] * game.static(a, menus[a]) for a in range(6))
        C = sum(p_hat[a] * p_hat[b] * game.static(a, menus[b])
                for a in range(6) for b in range(6))
        decorrelation.append({"player": i + 1, "D": D, "C": C,
                              "kappa": D - C, "e": utility[i] - D})
        menu_details.append({"player": i + 1, "history": h,
                             "rivals_by_action": menus,
                             "full_query_matrix": [[game.static(a, menus[b])
                                                    for b in range(6)]
                                                   for a in range(6)]})

    # These explicit rational certificates are transcribed from manuscript text.
    primary = tuple(F(x, 331825) for x in (44245, 49133, 120795, 77367, 0, 40285))
    dual = {(0, 1, 2): F(1635, 13273), (0, 2, 2): F(5550, 13273),
            (0, 2, 3): F(3365, 13273), (0, 2, 5): F(1123, 13273),
            (2, 2, 3): F(1600, 13273)}
    assert sum(primary) == 1 and min(primary) >= 0
    assert sum(dual.values()) == 1 and min(dual.values()) >= 0
    static_rows = []
    for B in product(range(6), repeat=3):
        vector = tuple(game.static(a, B) for a in range(6))
        value = sum(primary[a] * vector[a] for a in range(6))
        static_rows.append((B, vector, value))
    lower = min(r[2] for r in static_rows)
    p_hat_static_values = [(r[0], sum(p_hat[a] * r[1][a] for a in range(6)))
                           for r in static_rows]
    p_hat_safety = min(v for _, v in p_hat_static_values)
    assert all(row["C"] >= p_hat_safety for row in decorrelation)
    dual_payoffs = tuple(sum(prob * game.static(a, B) for B, prob in dual.items())
                        for a in range(6))
    upper = max(dual_payoffs)
    assert lower == upper == F(508643, 26546)
    primary_active = sorted(set(tuple(sorted(r[0])) for r in static_rows if r[2] == lower))
    primary_inactive_gaps = [r[2] - lower for r in static_rows if r[2] > lower]
    same_count_replies = {}
    for h in game.histories:
        count_key = tuple(h.count(a) for a in range(6))
        same_count_replies.setdefault(count_key, set()).add(game.policy[h])
    nonanonymous_groups = sum(len(replies) > 1 for replies in same_count_replies.values())

    best_welfare = max(pair[1] for pair in game.payoffs.values())
    opt_sorted = sorted(set(tuple(sorted(z)) for z, (_, w) in game.payoffs.items()
                            if w == best_welfare))
    opt_distinct_sets = sorted(set(tuple(sorted(set(z))) for z in opt_sorted))

    manuscript_claims = {
        "customer_count": sum(weights.values()) == 89,
        "decision_histories": len(game.histories) == 259,
        "incentive_comparisons": len(checks) == 1554,
        "outcome": outcome == (2, 5, 0, 0),
        "utilities": utility == (F(71, 3), F(22), F(59, 3), F(59, 3)),
        "welfare": W == 85,
        "D_values": tuple(r["D"] for r in decorrelation)
        == (F(43, 2), F(247, 12), F(59, 3), F(59, 3)),
        "C_values": tuple(r["C"] for r in decorrelation)
        == (F(1033, 48), F(247, 12), F(59, 3), F(59, 3)),
        "kappa_values": tuple(r["kappa"] for r in decorrelation)
        == (F(-1, 48), F(0), F(0), F(0)),
        "slack_values": tuple(r["e"] for r in decorrelation)
        == (F(13, 6), F(17, 12), F(0), F(0)),
        "aggregate_D": sum(r["D"] for r in decorrelation) == F(977, 12),
        "aggregate_C": sum(r["C"] for r in decorrelation) == F(1303, 16),
        "aggregate_kappa": sum(r["kappa"] for r in decorrelation) == F(-1, 48),
        "aggregate_slack": sum(r["e"] for r in decorrelation) == F(43, 12),
        "compensated_budget": W - sum(r["C"] for r in decorrelation) == F(57, 16),
        "exact_security": lower == upper == F(508643, 26546),
        "BR_margin": W - 4 * lower == F(110919, 13273),
    }
    assert all(manuscript_claims.values())

    # A perturbation of the actual 259-digit certificate also must be caught.
    corrupted = TypeGame(6, 4, weights, "0" + encoded[1:])
    corrupted_failures = [r for r in corrupted.audit_spe() if r[-1] < 0]
    assert corrupted_failures

    summary = {
        "method": "Independent direct customer-type Fraction sums; AST literal data only",
        "unit_customers": sum(weights.values()), "positive_interest_types": len(weights),
        "distinct_topics": len(set(topic_signatures)), "topic_coverages": coverages,
        "ordered_histories": len(game.histories), "deviation_comparisons": len(checks),
        "same_count_history_groups_with_different_replies": nonanonymous_groups,
        "including_self_comparisons": len(game.histories),
        "excluding_self_comparisons": len(checks) - len(game.histories),
        "SPE_violations": len(violations),
        "tied_comparisons": sum(r[-1] == 0 for r in checks),
        "strict_comparisons": len(positive), "min_strict_SPE_slack": min(positive),
        "outcome": outcome, "utilities": utility, "W": W,
        "uncovered_types": {t: w for t, w in weights.items()
                            if not any(t & (1 << a) for a in outcome)},
        "p_hat": p_hat, "D_C_kappa_e": decorrelation,
        "p_hat_static_safety": p_hat_safety,
        "p_hat_minimizing_static_multisets": sorted(set(tuple(sorted(b))
            for b, v in p_hat_static_values if v == p_hat_safety)),
        "aggregate_D": sum(r["D"] for r in decorrelation),
        "aggregate_C": sum(r["C"] for r in decorrelation),
        "aggregate_kappa": sum(r["kappa"] for r in decorrelation),
        "aggregate_e": sum(r["e"] for r in decorrelation),
        "compensated_budget": W - sum(r["C"] for r in decorrelation),
        "static_ordered_tuples": len(static_rows),
        "static_unordered_multisets": len(set(tuple(sorted(r[0])) for r in static_rows)),
        "primary": primary, "dual": [{"B": b, "probability": p} for b, p in dual.items()],
        "primary_min": lower, "dual_max": upper, "dual_action_payoffs": dual_payoffs,
        "primary_active_multisets": primary_active,
        "min_inactive_primary_slack": min(primary_inactive_gaps),
        "dual_inactive_action_4_gap": upper - dual_payoffs[4],
        "W_minus_4v4": W - 4 * lower,
        "OPT4": best_welfare, "OPT4_action_multisets": opt_sorted,
        "OPT4_distinct_topic_sets": opt_distinct_sets,
        "W_over_OPT4": F(W, best_welfare), "OPT4_minus_W": best_welfare - W,
        "SB_upper_bound_(7/4)*4v4": 7 * lower,
        "SB_margin_7v4_minus_OPT4": 7 * lower - best_welfare,
        "conditional_7W_over_4_minus_OPT4": F(7, 4) * W - best_welfare,
        "boundary_checks": boundary_checks(),
        "real_certificate_root_mutation_rejected": bool(corrupted_failures),
        "real_certificate_root_mutation_failures": [
            {"history": r[0], "deviation": r[1], "slack": r[-1]}
            for r in corrupted_failures],
        "manuscript_numeric_claims": manuscript_claims,
    }
    summary["audit_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary["uploaded_source_sha256"] = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    (HERE / "results.json").write_text(json.dumps(as_json(summary), ensure_ascii=False, indent=2) + "\n")
    (HERE / "certificate_data.json").write_text(json.dumps(as_json({
        "weights": weights, "policy": encoded, "primary": primary,
        "dual": [{"B": b, "probability": p} for b, p in dual.items()],
    }), ensure_ascii=False, indent=2) + "\n")
    (HERE / "on_path_query_matrices.json").write_text(
        json.dumps(as_json(menu_details), ensure_ascii=False, indent=2) + "\n")
    with (HERE / "all_incentive_comparisons.tsv").open("w") as out:
        out.write("history\taction\toriginal_terminal\tdeviation_terminal\tslack\n")
        for h, a, z, zz, slack in checks:
            out.write(f"{h}\t{a}\t{z}\t{zz}\t{slack}\n")
    with (HERE / "all_static_competitors.tsv").open("w") as out:
        out.write("competitors\tf_0\tf_1\tf_2\tf_3\tf_4\tf_5\tprimary_value\n")
        for b, vector, value in static_rows:
            out.write("\t".join(map(str, (b,) + vector + (value,))) + "\n")
    print(json.dumps(as_json(summary), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
