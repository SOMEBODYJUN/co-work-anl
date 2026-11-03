"""One new definition-level audit of the saved query-5 point only.

Query 2 is bound to its existing expanded-unit audit by literal input/field
comparisons; its mathematical computation is not rerun. No LP, BI, discovery
code or canonical game implementation is imported.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def load(rel):
    return json.loads((HERE / rel).read_text())


def main():
    manifest = load("source-manifest.json")
    for r in manifest:
        data = (HERE / r["artifact"]).read_bytes()
        assert len(data) == r["size"]
        assert hashlib.sha256(data).hexdigest() == r["sha256"]
        assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == r["blob"]
    diagnostic = load("original/round5_coupling/stationary_348_diagnostic.json")
    saved_q2 = load("original/round5_coupling/stationary_full_slot_counterexample_6286.json")
    old = load("dependencies/high_insertion_2cycle_348_exact.json")
    audit_q2 = load("dependencies/stationary_query2_independent_audit.json")
    q2, q5 = (next(r for r in diagnostic["results"] if r["query"] == a) for a in (2, 5))
    assert saved_q2["certificate"] == old["certificate"]
    assert saved_q2["forced_paths"] == old["forced_paths"] == q2["forced_paths"] == q5["forced_paths"]
    q2_types = [{"topics": [a for a in range(6) if r["mask"] & (1 << a)],
                 "multiplicity": r["multiplicity"]} for r in q2["unit_customers"]]
    assert saved_q2["instance"]["customers"] == q2_types
    for left, right in [("K", "K"), ("root_payoffs", "root_d"), ("root_u", "root_u"),
                        ("stationary", "p"), ("Kp", "Kp"), ("D", "D"), ("C_self", "C"),
                        ("actual_W", "actual_W"), ("OPT3", "OPT_3"), ("column_caps", "pure_column_maxima"),
                        ("stationary_gap", "stationary_query_2_overload")]:
        assert saved_q2[left] == audit_q2[right]
    assert audit_q2["status"] == "pass" and len(audit_q2["all_exact_SPE_comparisons"]) == 258
    assert min(F(r["margin"]) for r in audit_q2["all_exact_SPE_comparisons"]) == 0
    # Only literal bindings above; the pre-existing query-2 IC arithmetic is reused.

    actions = {tuple(r["history"]): r["action"] for r in old["certificate"]["actions"]}
    required = {h for d in range(3) for h in product(range(6), repeat=d)}
    assert len(actions) == 43 and set(actions) == required
    clients = tuple(r["mask"] for r in q5["unit_customers"] for _ in range(r["multiplicity"]))
    assert len(clients) == q5["total_customers"] == 6286
    assert q5["unit_customers"] != q2["unit_customers"]

    def end(h):
        h = tuple(h)
        while len(h) < 3:
            h += (actions[h],)
        return h

    @lru_cache(None)
    def evaluate(leaf):
        own = [Counter() for _ in range(3)]
        query = [Counter() for _ in range(6)]
        coverage = 0
        for mask in clients:
            load = sum(bool(mask & (1 << a)) for a in leaf)
            coverage += bool(load)
            for i, a in enumerate(leaf):
                if mask & (1 << a):
                    own[i][load] += 1
            for a in range(6):
                if mask & (1 << a):
                    query[a][load + 1] += 1
        return ([sum((F(n, d) for d, n in c.items()), F(0)) for c in own],
                [sum((F(n, d) for d, n in c.items()), F(0)) for c in query], coverage)

    comparisons = []
    for h in sorted(required, key=lambda h: (len(h), h)):
        actual = end(h)
        prescribed = evaluate(actual)[0][len(h)]
        for a in range(6):
            dev = end(h + (a,))
            margin = prescribed - evaluate(dev)[0][len(h)]
            assert margin >= 0
            comparisons.append({"history": list(h), "alternate": a, "margin": str(margin)})
    paths = [end((a,)) for a in range(6)]
    assert list(map(list, paths)) == q5["forced_paths"]
    p = list(map(F, q5["stationary"]))
    assert sum(p) == 1 and min(p) >= 0
    assert all(sum((p[b] * F(paths[b].count(a), 3) for b in range(6)), F(0)) == p[a]
               for a in range(6))
    root_payoffs = [evaluate(z)[0][0] for z in paths]
    u = evaluate(end(()))[0][0]
    price = sum((p[b] * evaluate(paths[b])[1][5] for b in range(6)), F(0))
    W = evaluate(end(()))[2]
    optimum = max(evaluate(z)[2] for z in product(range(6), repeat=3))
    assert u == max(root_payoffs) == F(q5["root_u"])
    assert price == F(q5["query_price"]) and price - u == F(123, 4)
    assert (price - u) / W == F(q5["exact_gap_normalized"]) == F(123, 17036)
    assert len(comparisons) == q5["all_comparisons"] == 258
    assert min(F(r["margin"]) for r in comparisons) == F(q5["spe_min_slack_normalized"]) == 0
    report = {"scope": "new query-5 saved point only; query-2 existing audit reused without rerun",
              "all_source_integrities_passed": True, "query2_literal_bindings_passed": True,
              "query5_input_is_distinct_from_query2": True, "query5_unit_clients": len(clients),
              "query5_complete_histories": len(required), "query5_comparisons_including_self": len(comparisons),
              "query5_nonself_comparisons": 215, "query5_all_exact_comparisons": comparisons,
              "query5_forced_paths": list(map(list, paths)), "query5_root_payoffs": list(map(str, root_payoffs)),
              "query5_root_u": str(u), "query5_stationary": list(map(str, p)),
              "query5_query_price": str(price), "query5_gap": str(price - u),
              "query5_W": W, "query5_OPT3": optimum, "query5_half_margin": 2 * W - optimum,
              "query5_normalized_gap": str((price - u) / W),
              "query2_W_from_reused_report": saved_q2["actual_W"],
              "query2_normalized_gap_from_saved_diagnostic": q2["exact_gap_normalized"],
              "query5_customer_input_sha256": hashlib.sha256(json.dumps(q5["unit_customers"],
                   sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
              "strategy_sha256": hashlib.sha256(json.dumps(old["certificate"],
                   sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
              "old_query2_math_reruns": 0, "LP_BI_or_discovery_calls": 0}
    (HERE / "query5-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "query5_all_exact_comparisons"}))


if __name__ == "__main__":
    main()
