#!/usr/bin/env python3
"""Rebuild the parent report from all cells of the frozen author matrices.

This does not import the parent enumerator or regenerate customer moments.
The two-player endpoint test is derived directly from complete reply sets.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original"
DATA = ORIGINAL / "research_5"


def load(path):
    return json.loads(path.read_text())


def main():
    source_paths = {
        "report": ORIGINAL / "audit_full156_reply_set.json",
        "kernel": DATA / "full156_tail2_kernel_10344.json",
        "welfare": DATA / "full156_tail2_welfare_10344.json",
        "point": DATA / "combined_branch_master_exact.json",
    }
    report, kernel, welfare, point = (load(source_paths[key])
                                     for key in ("report", "kernel", "welfare", "point"))
    hashes = {key: sha256(path.read_bytes()).hexdigest()
              for key, path in source_paths.items()}
    assert hashes["report"] == "99d94577b978d76a618781ba5274fee0297ccdeef087e90fba5d6ef52f827415"
    assert hashes["kernel"] == "876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4"
    assert hashes["welfare"] == "fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256"
    assert hashes["point"] == kernel["source_sha256"]
    assert welfare["kernel_sha256"] == hashes["kernel"]
    labels = kernel["topics"]
    assert len(labels) == len(set(labels)) == 156 and welfare["topics"] == labels
    assert kernel["players"] == 6
    assert [labels[i] for i in kernel["fixed_prefix"]] == ["A1", "A2", "A3", "A4"]
    assert kernel["aliases"] == list(range(156)) == welfare["aliases"]
    assert kernel["actual_last_pair"] == welfare["actual_pair"]
    first, last = kernel["actual_last_pair"]
    assert [labels[first], labels[last]] == ["A5", "A6"]
    scale = int(kernel["unit_customer_scale"])
    denominator = int(kernel["payoff_denominator_for_normalized_point"])
    assert scale > 0 and denominator > 0 and int(welfare["unit_customer_scale"]) == scale
    assert denominator == 60 * scale
    U = [[int(x) for x in row] for row in kernel["payoff_numerators"]]
    G = [[int(x) for x in row] for row in kernel["G_numerators"]]
    W = [[int(x) for x in row] for row in welfare["welfare_numerators"]]
    Frow = list(map(int, kernel["F_numerators"]))
    assert len(Frow) == 156
    assert all(len(matrix) == 156 and all(len(row) == 156 for row in matrix)
               for matrix in (U, G, W))
    for a in range(156):
        for b in range(156):
            assert G[a][b] == G[b][a]
            assert U[a][b] == Frow[a] - G[a][b] >= 0
            assert 0 <= W[a][b] == W[b][a] <= scale
    assert list(map(int, kernel["actual_payoff_numerators"])) == [U[first][last], U[last][first]]
    original_W = F(kernel["source_W"])
    assert F(welfare["source_W"]) == original_W == F(point["W"])
    assert original_W == F(W[first][last], scale)
    positive_hist = [column for column in point["columns"]
                     if column["kind"] == "hist" and F(column["weight"]) > 0]
    assert all(F(column["weight"]) >= 0 for column in point["columns"]
               if column["kind"] == "hist")
    assert sum((F(column["weight"]) for column in positive_hist), F(0)) == 1
    # Eight bins encode three membership bits over six indexed comparison slots.
    assert all(len(column["hist"]) == 8 and sum(column["hist"]) == 6
               and all(isinstance(count, int) and count >= 0 for count in column["hist"])
               for column in positive_hist)
    assert all(sum(multiplicity for word, multiplicity in enumerate(column["hist"])
                   if word & 4) == 1 for column in positive_hist)

    # At each first action, retain every last-player best reply, including ties.
    replies = []
    guaranteed = []
    for a in range(156):
        last_payoffs = [(U[b][a], b) for b in range(156)]
        last_best = max(value for value, _ in last_payoffs)
        reply = [b for value, b in last_payoffs if value == last_best]
        replies.append(reply)
        guaranteed.append(min(U[a][b] for b in reply))
    threshold = max(guaranteed)
    endpoints = [(a, b) for a in range(156) for b in replies[a]
                 if U[a][b] >= threshold]
    minimum_welfare = min(F(W[a][b], scale) for a, b in endpoints)
    delta = max(F(0), F(threshold - U[first][last], denominator))
    old_gap = 1 - 2 * original_W
    expected = {
        "scope": "Second definition-level r2 SPE endpoint enumeration from author kernel; fixed actual first four topics only. Not an independent customer-moment reconstruction.",
        "kernel_sha256": hashes["kernel"], "welfare_sha256": hashes["welfare"],
        "topics": 156, "ordered_pair_payoff_checks": 156**2,
        "SPE_tail_count": len(endpoints),
        "SPE_tails": [[labels[a], labels[b]] for a, b in endpoints],
        "minimum_normalized_welfare": str(minimum_welfare),
        "normalized_OPT6": "1; six T topics cover all mass",
        "minimum_strictly_above_half": minimum_welfare > F(1, 2),
        "old_actual_last_is_best_reply": last in replies[first],
        "old_actual_penultimate_deficit": str(delta),
        "three_times_deficit": str(3 * delta), "old_half_gap": str(old_gap),
        "old_target_cannot_pass_known_repair_cost": 3 * delta >= old_gap,
        "main_target": "OPEN; other first-four prefixes and other catalogues are not excluded",
    }
    assert report == expected
    assert len(endpoints) == 6
    assert all(F(W[a][b], scale) == minimum_welfare for a, b in endpoints)
    summary = {
        "status": "PASS", "all_original_fields_equal": True,
        "parent_enumerator_imported_or_executed": False,
        "customer_moment_kernel_reconstructed": False,
        "source_sha256": hashes,
        "payoff_identity_and_welfare_symmetry_pairs": 156**2,
        "last_best_reply_count_by_first_action": {labels[a]: len(reply) for a, reply in enumerate(replies)},
        "old_actual_last_best_reply_labels": [labels[b] for b in replies[first]],
        "threshold": str(F(threshold, denominator)),
        "old_actual_payoffs": [str(F(U[first][last], denominator)),
                               str(F(U[last][first], denominator))],
        "all_tail_welfares_equal": True,
        "minimum_welfare_minus_half": str(minimum_welfare - F(1, 2)),
        "repair_cost_minus_old_gap": str(3 * delta - old_gap),
        "positive_histogram_count": len(positive_hist),
        "point_record_verified_rows": point["verified_rows"],
        "kernel_filename_10344_is_not_a_new_row_verification": True,
        "rebuilt_original_report": expected,
    }
    result_path = HERE / "field-audit.json"
    result_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items()
                      if key not in {"last_best_reply_count_by_first_action",
                                     "old_actual_last_best_reply_labels",
                                     "rebuilt_original_report"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
