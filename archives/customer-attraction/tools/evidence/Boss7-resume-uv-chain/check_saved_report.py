"""Check every saved UV audit field from its disjoint unit-client definition.

No original code/model import or BI search.  The saved child outcome sets are
checked against the proved all-prefix closed form for one large topic and
disjoint singletons, including the terminal-prefix boundary.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / "original" / name).read_text())


def main():
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for r in manifest:
        data = (HERE / r["artifact"]).read_bytes()
        assert len(data) == r["size"]
        assert hashlib.sha256(data).hexdigest() == r["sha256"]
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == r["blob"]
    saved = read("uv_all_big_audit.json")
    m, p = 4, 4
    weights = (4, 1, 1, 1)
    client_topic = (0, 0, 0, 0, 1, 2, 3)

    def end(prefix):
        return tuple(prefix) + (0,) * (m - len(prefix))

    def cov(path):
        return sum(weights[a] for a in set(path))

    def gain(path, i):
        return F(weights[path[i]], path.count(path[i]))

    def shares(path, i):
        a = path[i]
        return [F(1, path.count(a)) if t == a else F(0) for t in client_topic]

    expected_histories = []
    slacks = []
    for d in range(m):
        for h in product(range(p), repeat=d):
            actual = end(h)
            u = gain(actual, d)
            deviations = []
            for a in range(p):
                branch = end(h + (a,))
                v = gain(branch, d)
                assert u >= v
                slacks.append(u - v)
                deviations.append({"action": a, "terminal": list(branch),
                                   "payoff": str(v), "IC_margin": str(u - v)})
            expected_histories.append({"history": list(h), "prescribed_action": 0,
                                       "prescribed_terminal": list(actual), "prescribed_payoff": str(u),
                                       "deviations": deviations})
    all_leaves = list(product(range(p), repeat=m))
    optimum = max(map(cov, all_leaves))
    optimal = [t for t in all_leaves if cov(t) == optimum]
    actual = end(())
    W = cov(actual)
    chain_records = []
    for t in optimal:
        d = [F(0)] * len(client_topic)
        chain = []
        for i, a in enumerate(t):
            before = end(t[:i])
            after = end(t[:i + 1])
            delta = [b - c for b, c in zip(shares(before, i), shares(after, i))]
            d = [x + y for x, y in zip(d, delta)]
            ic = gain(before, i) - gain(after, i)
            assert ic >= 0
            chain.append({"k": i + 1, "prefix": list(t[:i]), "prescribed_action": 0,
                          "forced_action": a, "Z_minus": list(before), "Z_plus": list(after),
                          "client_share_changes": list(map(str, delta)), "IC_gain": str(ic)})
        V = [F(int(a in t) - 2 * int(a in actual)) + d[x]
             for x, a in enumerate(client_topic)]
        assert d == [F(13, 12)] * 4 + [F(-1)] * 3
        assert V == [F(1, 12)] * 4 + [F(0)] * 3
        assert sum(d) == F(4, 3) and sum(V) == F(1, 3)
        chain_records.append({"optimal_tuple": list(t), "chain": chain,
                              "d_per_unit_client": list(map(str, d)),
                              "V_per_unit_client": list(map(str, V)),
                              "IC_sum": str(sum(d)), "UV_holds": all(v <= 0 for v in V)})

    def outcomes_from_closed_form(prefix):
        c = tuple(prefix.count(a) for a in range(p))
        remaining = m - len(prefix)
        if not remaining:
            return [c]
        if sum(c[1:]):
            return [(c[0] + remaining,) + c[1:]]
        return sorted([(m, 0, 0, 0)] + [tuple((m - 1) if a == 0 else int(a == s)
                                             for a in range(p)) for s in range(1, p)])

    child_records = []
    L = []
    child_outcomes = 0
    for i in range(m):
        prefix = actual[:i]
        children = []
        row = []
        for a in range(p):
            forced = prefix + (a,)
            c = tuple(forced.count(t) for t in range(p))
            terminal_counts = outcomes_from_closed_form(forced)
            values = [F(weights[a], q[a]) for q in terminal_counts]
            row.append(min(values))
            child_outcomes += len(terminal_counts)
            children.append({"forced_action": a, "child_prefix_counts": list(c),
                             "all_SPE_terminal_counts": list(map(list, terminal_counts)),
                             "current_payoffs": list(map(str, values)), "L": str(min(values))})
        L.append(row)
        child_records.append({"actual_prefix": list(prefix), "children": children})
    theta = [max(row) for row in L]
    sm = [sum((L[i][a] for i, a in enumerate(t)), F(0)) for t in optimal]
    expected = {
        "status": "exact_counterexample_to_universal_UV_optimum_chain_existence_only",
        "source_family": "co-work-anl/research/questions/customer_attraction_half_coverage.md:23",
        "reviewed_UV": "R-f399f831353446a49502f49d8abd2cb7/probabilistic_route/variation_bridge.md:111",
        "labels": ["B", "s1", "s2", "s3"],
        "unit_clients": ["b1", "b2", "b3", "b4", "s1", "s2", "s3"],
        "unit_client_interests": [[a] for a in client_topic],
        "instance": {"topics": ["B", "s1", "s2", "s3"],
                     "customers": [{"topics": [a], "multiplicity": weights[a]} for a in range(p)],
                     "players": m},
        "actual_path": list(actual), "W": W, "OPT": optimum,
        "half_slack_2W_minus_OPT": 2 * W - optimum,
        "decision_histories_checked": len(expected_histories),
        "comparisons_including_self": len(slacks), "nonself_comparisons": len(slacks) - len(expected_histories),
        "minimum_IC_margin": str(min(slacks)),
        "complete_strategy_and_all_deviations": expected_histories,
        "all_terminal_tuples_checked_for_OPT": len(all_leaves),
        "all_optimal_ordered_tuples": list(map(list, optimal)),
        "all_optimal_chain_variation_audits": chain_records,
        "any_optimal_chain_satisfies_UV": any(r["UV_holds"] for r in chain_records),
        "set_valued_BI_child_audits": child_records,
        "L_matrix": [list(map(str, row)) for row in L],
        "Theta": list(map(str, theta)), "sum_Theta": str(sum(theta)),
        "all_optimal_tuple_SM_sums": list(map(str, sm)),
        "SM_right_side_OPT_minus_W": optimum - W,
        "TB_slack_W_plus_sumTheta_minus_OPT": str(W + sum(theta) - optimum),
        "scope": "UV conditional implication remains true; SM, THRESHOLD and Q-CAG-HALF are not refuted.",
    }
    assert saved == expected, "saved report does not match exact definition/closed-form expectations"
    summary = read("uv_summary.json")
    assert summary == {k: expected[k] for k in (
        "status", "decision_histories_checked", "comparisons_including_self",
        "all_terminal_tuples_checked_for_OPT", "any_optimal_chain_satisfies_UV", "W", "OPT",
        "L_matrix", "Theta", "TB_slack_W_plus_sumTheta_minus_OPT")}
    receipt = read("uv_receipt.json")
    assert set(receipt) == {"actor", "body", "id", "kind", "schema", "seq", "time"}
    assert set(receipt["body"]) == {"asset", "mentions", "save", "text", "thread"}
    assert receipt["schema"] == 3 and receipt["kind"] == "message" and receipt["seq"] == 216
    result = {
        "all_source_integrity_checks_passed": True, "manifest_files": len(manifest),
        "all_report_fields_match_exact_expectations": True, "report_top_fields": len(saved),
        "summary_is_exact_projection": True, "decision_histories": len(expected_histories),
        "comparisons_including_self": len(slacks), "nonself_comparisons": len(slacks) - len(expected_histories),
        "terminal_tuples_for_OPT": len(all_leaves), "optimal_tuples_and_chains": len(optimal),
        "chain_rows": sum(len(r["chain"]) for r in chain_records),
        "unit_client_chain_changes": sum(len(r["chain"]) * len(client_topic) for r in chain_records),
        "BI_child_sets_checked_against_proved_closed_form": m * p,
        "BI_child_terminal_records_checked": child_outcomes,
        "no_new_BI_solver_or_original_program_run": True,
        "message_metadata": {k: receipt[k] for k in ("actor", "id", "kind", "schema", "seq", "time")},
        "historical_message_asset": receipt["body"]["asset"],
        "historical_asset_commit_not_checked_out": True,
        "universal_result_basis": "analytic all-m proof in formal object; finite checker is regression only",
    }
    (HERE / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("message_metadata", "historical_message_asset")}))


if __name__ == "__main__":
    main()
