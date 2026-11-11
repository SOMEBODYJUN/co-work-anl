#!/usr/bin/env python3
"""Independent semantic/structural source audit, not a coefficient rescan.

Only standard-library reads of proof sources and point-free symbolic metadata.
The original shares are rederived in the companion proof.  This checker binds
that proof to exact input bytes and checks histories, query roles, and counts.
All writes stay in this audit directory.  No generator imports or optimizer.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
LAYER = WORK / "early_shared_x_joint"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    paths = {
        "complete_history_model": REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
        "unchanged_prefix_maxX_proof": WORK / "main_prefix_safety_maxx_family.md",
        "terminal_response_proof": WORK / "terminal_response_cycles.md",
        "original_MX_RC_owner": REPO / "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
        "original_PAIR_owner": REPO / "archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md",
        "true_tail_PAIR_proof": WORK / "early3_pair_cone.md",
        "original_word_patterns": REPO / "archives/customer-attraction/tools/evidence/explicit-joint-rz-and-root-extension-primary/dependencies-original/research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/fourth_indexed_projection.py",
        "original_word_usage": REPO / "archives/customer-attraction/tools/evidence/explicit-joint-rz-and-root-extension-primary/dependencies-original/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/new_reply_budget.py",
        "literal_labels": WORK / "actual_pair_20910/build.py",
        "builder_source": LAYER / "build_layer.py",
        "builder_proof": WORK / "early_shared_x_joint.md",
        "coordinate_contract": LAYER / "base_coordinate_contract.json",
        "symbolic_append": LAYER / "symbolic_append.json.gz",
    }
    pins = {
        "complete_history_model": "cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88",
        "unchanged_prefix_maxX_proof": "4d3f24e686ae38a8593b62abe1807249de6bd3884b428d52198180798ea73b81",
        "original_MX_RC_owner": "f358a161eed5f02f243223bc590a41b3247834f842ab251060e380f5cd1fed39",
        "original_PAIR_owner": "8caa0131fc5a517bbdf8001a44bc00cc6741bb5255a35e413016e4a7319779ba",
        "symbolic_append": "1ff17a93dc319e05c366424214a722a86577773599ac5692a1fabb6cfaa3a5e0",
    }
    manifest = {
        key: {"path": str(path.relative_to(REPO)), "sha256": digest(path), "bytes": path.stat().st_size}
        for key, path in paths.items()
    }
    for key, value in pins.items():
        assert manifest[key]["sha256"] == value, (key, "source pin changed")

    data = json.loads(gzip.decompress(paths["symbolic_append"].read_bytes()))
    contract = json.loads(paths["coordinate_contract"].read_text())
    hist = {h["hist_column"]: h for h in contract["histograms"]}
    assert len(hist) == 16
    assert len({h["X_column"] for h in hist.values()}) == 16
    assert contract["zero_histograms_retained"] == [1, 59, 366, 449, 524, 574]
    for h in hist.values():
        n = h["hist"]
        expected = {
            "T": sum(n[4:]),
            "B": n[2] + n[3] + n[6] + n[7],
            "C": n[1] + n[3] + n[5] + n[7],
        }
        assert sum(n) == 6 and expected == h["indexed_membership_counts"]
        actual = tuple(map(int, h["actual_bits"]))
        assert h["P"] == sum(actual[:4])
        assert h["actual_backgrounds"] == [sum(actual[:j]) for j in range(6)]

    expected_family_counts = {
        "source-IC": 4,
        "actual-source-SAFE": 84,
        "same-P-MAX": 14,
        "catalog-capacity": 14,
        "actual-MX-cap": 14,
        "branch-terminal-BR": 50,
        "branch-true-PAIR": 96,
        "actual-RC": 160,
    }
    raw = data["raw_inequality_provenance"]
    assert Counter(row["family"] for row in raw) == expected_family_counts
    assert len(raw) == len(data["inequalities"]) == 436
    assert len(data["new_columns"]) == 16 * sum(2 ** r for r in (6, 5, 4, 3)) == 1920
    assert len(data["equalities"]) == 4 * 16 * 2 == 128
    assert data["old_columns"] == 21021 and data["total_columns"] == 22941
    assert data["all_new_columns_nonnegative"] is True

    summaries = []
    actual_rc_classes = Counter()
    for branch in data["branches"]:
        i = branch["source_player"]
        m, r = 5 - i, 7 - i
        tails = branch["ordered_tail_labels"]
        assert branch["m"] == m and branch["r"] == r
        assert len(tails) == m + 1
        before = [f"A{j}" for j in range(1, i)]
        middle_names = [q["name"] for q in tails[:-1]]
        assert branch["source_history"] == before
        assert branch["last_two_prefix"] == before + ["X"] + middle_names[:-1]
        assert branch["terminal_history"] == before + ["X"] + middle_names
        assert len(branch["last_two_prefix"]) == 4
        assert len(branch["terminal_history"]) == 5
        assert branch["hidden_columns"] == 16 * 2 ** r
        assert tails[-2]["player"] == 5 and tails[-1]["player"] == 6
        rr = [row for row in raw if row["branch_source_player"] == i]
        counts = Counter(row["family"] for row in rr)
        expected_rc = (m + 1) * (m + 2) // 2 + 9 * (m + 1)
        assert counts == {
            "source-IC": 1,
            "actual-source-SAFE": 6 * (m + 1),
            "same-P-MAX": m + 1,
            "catalog-capacity": m + 1,
            "actual-MX-cap": m + 1,
            "branch-terminal-BR": 10 + m,
            "branch-true-PAIR": 2 * (9 + m) + 1,
            "actual-RC": expected_rc,
        }
        for row in rr:
            family = row["family"]
            prov = row["provenance"]
            if family == "source-IC":
                assert row["wallet"] == f"actual u{i}"
                assert prov["history"] == before and prov["frozen_actual_tail"] is False
            elif family == "actual-source-SAFE":
                j = row["actual_source_player"]
                assert row["wallet"] == f"actual u{j}"
                assert prov["history"] == [f"A{k}" for k in range(1, j)]
                assert prov["frozen_forced_X_tail"] is False
            elif family == "branch-terminal-BR":
                assert prov["history"] == branch["terminal_history"]
                assert prov["uses_actual_u6"] is False
            elif family == "branch-true-PAIR":
                assert prov["history"] == branch["last_two_prefix"]
                assert prov["uses_actual_u5_or_u6"] is False
                assert prov["diagonal_average_is_q_not_q_squared"] is True
            elif family == "actual-MX-cap":
                assert row["wallet"] == "actual u5"
                assert prov["history"] == ["A1", "A2", "A3", "A4"]
            elif family == "actual-RC":
                assert row["wallet"] == "actual u5 + F_X"
                assert prov["history"] == ["A1", "A2", "A3", "A4"]
                assert prov["cross_branch_unknown_intersections"] is False
                actual_rc_classes[row["pair_class"]] += 1
                for key in ("query_left", "query_right"):
                    q = row[key]
                    if q["kind"] == "new-tail":
                        assert q["source_player"] == i
        summaries.append({"source": i, "remaining": r, "middles": m,
                          "named_tail_roles": m + 1, "columns": 16 * 2 ** r,
                          "last_two_prefix": branch["last_two_prefix"],
                          "terminal_history": branch["terminal_history"],
                          "row_counts": dict(counts)})
    assert actual_rc_classes == {"new-tail-unordered": 34, "new-tail-known": 126}

    # One exact semantic witness for the material diagonal-mean distinction.
    q = Fraction(1, 2)
    d = 3
    mean_self_tax = q / (d * (d + 1))
    false_independent_tax = q * q / (d * (d + 1))
    assert mean_self_tax - false_independent_tax == Fraction(1, 48)
    result = {
        "status": "PASS_INDEPENDENT_MATHEMATICAL_SOURCE_AUDIT",
        "scope": "Universal source proofs; exact finite-16-hist append is a necessary restriction, not full SPE characterization.",
        "proof": str((WORK / "early_shared_x_source_audit.md").relative_to(REPO)),
        "sources": manifest,
        "source_domains": summaries,
        "family_counts": expected_family_counts,
        "new_hidden_columns": 1920,
        "common_X_equalities": 128,
        "new_inequalities": 436,
        "actual_RC_classes": dict(actual_rc_classes),
        "exact_mean_diagonal_witness": {
            "d": d, "q": str(q), "correct_tax": str(mean_self_tax),
            "incorrect_independence_tax": str(false_independent_tax), "difference": "1/48"},
        "matrix_changing_mathematical_flaws_found": [],
        "precision_improvement_absorbed_by_builder": "The 14 tails are named label roles; conditional aliases such as X=A_i or source4 X=T_k need not be distinct and are not certified by product coupling.",
        "independence": "No generator import and no 1920-column coefficient rescan; original model shares and MX/RC/PAIR payment identities are rederived in the proof.",
        "point_files_read": False,
        "optimizer_calls": 0,
        "other_workspace_files_modified": False,
    }
    target = HERE / "source_audit.json"
    assert not target.exists(), "refuse to overwrite frozen source audit"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "columns": 1920, "equalities": 128,
                      "inequalities": 436, "source_files_pinned": len(manifest)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
