"""Exact, narrow replay of one frozen B-menu price separation.

The original CLI is invoked once.  A separate calculation aggregates the
menu's first moment by its old hist column before computing any price.
No mother-matrix builder, optimizer, or SPE solver is imported or invoked.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

EXPECTED = {
    "ddf2520de2255a1c4472": (719, "eaea78f17b3da08eda9121e8254f27dfb58a2065ca5039d96d79f924034a2318"),
    "59a90ea11a2df684017e": (1592, "7b90478c27cc242ca7d06e5d8be3934f6a55d260cf52e0551d322d813120e032"),
    "point": (844597, "6269be5cbcd61d397c33e19ce2ac31ace3f73aeec22c978426d8f3b30b0fada7"),
}


def identity(path, repo):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(repo)), "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    base = repo / "archives/customer-attraction/tools/evidence"
    frozen = base / "menu-price-and-prescribed-prefix-audits-primary/frozen-inputs"
    paths = {
        "ddf2520de2255a1c4472": frozen / "ddf2520de2255a1c4472-B_menu_actual_price_separation.json",
        "59a90ea11a2df684017e": frozen / "59a90ea11a2df684017e-audit_B_menu_actual_prices.py",
        "point": base / "swap-B-visible-and-histogram-projection-two-primary/source-root/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/coupled_B_master_exact.json",
    }
    identities = {key: identity(path, repo) for key, path in paths.items()}
    for key, info in identities.items():
        assert (info["size"], info["sha256"]) == EXPECTED[key]
    inventory = {d["id"]: d for line in (repo / "cleanup/inventory.jsonl").read_text().splitlines()
                 if (d := json.loads(line))["id"] in EXPECTED}
    for key in ("ddf2520de2255a1c4472", "59a90ea11a2df684017e"):
        assert (inventory[key]["size"], inventory[key]["sha256"]) == EXPECTED[key]

    # Run the unmodified frozen command-line entry point, including its SHA guard.
    process = subprocess.run([sys.executable, str(paths["59a90ea11a2df684017e"]),
                              "--point", str(paths["point"])],
                             text=True, capture_output=True, check=True)
    assert process.stderr == ""
    original = json.loads(process.stdout)
    point = json.loads(paths["point"].read_bytes())
    separation = json.loads(paths["ddf2520de2255a1c4472"].read_bytes())
    columns = point["columns"]
    kinds = Counter(c["kind"] for c in columns)
    assert kinds == {"K": 1, "hist": 16, "joint-reply": 582,
                     "overlap": 1306, "actual-B-branch-state": 128}
    weights = [F(c["weight"]) for c in columns]
    assert all(w >= 0 for w in weights)
    hist = {j: c for j, c in enumerate(columns) if c["kind"] == "hist"}
    moments = {j: F(0) for j in hist}
    masses = {j: F(0) for j in hist}
    states = {j: set() for j in hist}
    for j, c in hist.items():
        assert len(c["actual_bits"]) == 6 and set(c["actual_bits"]) <= {"0", "1"}
        assert len(c["hist"]) == 8 and all(type(h) is int and h >= 0 for h in c["hist"])
        assert sum(c["hist"]) == 6 and c["d"] == sum(c["hist"][4:]) == 1
    for j, c in enumerate(columns):
        if c["kind"] != "actual-B-branch-state":
            continue
        h = c["hist_column"]
        assert h in hist and c["Q"] in (0, 1) and c["R"] in (0, 1) and c["ell"] in (0, 6)
        state = (c["Q"], c["R"], c["ell"])
        assert state not in states[h]
        states[h].add(state)
        masses[h] += weights[j]
        moments[h] += weights[j] * F(c["ell"], 6)
    assert all(len(states[h]) == 8 and masses[h] == weights[h] for h in hist)
    assert all(0 <= moments[h] <= weights[h] for h in hist)

    # First moments z_h, rather than raw B-state rows, are enough for all seven prices.
    utilities = [F(0) for _ in range(6)]
    prices = [F(0) for _ in range(6)]
    rows = []
    for h, c in hist.items():
        bits = tuple(int(b) for b in c["actual_bits"])
        load = sum(bits)
        local_u = [weights[h] / load if b else F(0) for b in bits]
        local_p = [moments[h] / (sum(bits[:i]) + 6 - i) for i in range(6)]
        utilities = [a + b for a, b in zip(utilities, local_u)]
        prices = [a + b for a, b in zip(prices, local_p)]
        rows.append({"hist_column": h, "actual_bits": c["actual_bits"],
                     "hist_mass": str(weights[h]), "mean_menu_inclusion_mass": str(moments[h]),
                     "u6_contribution": str(local_u[5]), "price6_contribution": str(local_p[5]),
                     "slack6_contribution": str(local_u[5] - local_p[5])})
    slacks = [u - p for u, p in zip(utilities, prices)]
    K = sum((weights[j] for j, c in enumerate(columns) if c["kind"] == "K"), F(0))
    menu_size = sum(moments.values(), F(0))
    expected = {"scope": "exact price rows of one necessary point, not SPE",
                "source_sha256": EXPECTED["point"][1],
                "actual_utilities": [str(u) for u in utilities],
                "reply_family_prices": [str(p) for p in prices],
                "price_slacks": [str(s) for s in slacks],
                "capacity_slack": str(K - menu_size)}
    assert original == expected
    assert separation["point_sha256"] == EXPECTED["point"][1]
    assert separation["row"] == "u6 - sum_state weight*ell/(6*(actual_prefix5_load+1)) >= 0"
    assert F(separation["u6"]) == utilities[5]
    assert F(separation["reply_family_average_price"]) == prices[5]
    assert F(separation["minimum_row_value"]) == slacks[5] == -F(separation["violation"]) < 0
    assert all(s > 0 for s in slacks[:5]) and K - menu_size > 0
    assert min(slacks + [K - menu_size]) == slacks[5]
    assert sum(utilities, F(0)) == F(point["W"])
    assert sum((weights[h] for h in hist), F(0)) == F(point["O"]) == 1
    assert F(point["strict_half_gap"]) == 1 - 2 * sum(utilities, F(0)) > 0
    summary_path = base / "coupled-b-fixed-points-boss3/replay/single/summary.json"
    summary = json.loads(summary_path.read_text())
    old_menu = summary["ordinary_Y_menu_prices_not_in_saved_matrix"][0]
    assert summary["source_point_sha256"] == EXPECTED["point"][1]
    assert old_menu["actual_payoffs"] == expected["actual_utilities"]
    assert old_menu["Y_query_values"] == expected["reply_family_prices"]
    assert old_menu["six_actual_price_slacks"] == expected["price_slacks"]
    assert old_menu["capacity_slack"] == expected["capacity_slack"]
    result = {"status": "passed", "scope": "One frozen necessary point; seven ordinary menu prices only.",
              "source_identity": identities, "original_cli_invocations": 1,
              "mother_matrix_builder_invocations": 0, "optimizer_invocations": 0,
              "SPE_solver_invocations": 0, "columns": len(columns), "column_kinds": dict(kinds),
              "all_column_weights_nonnegative": True, "hist_marginal_equalities_checked": len(hist),
              "states_per_hist": 8, "all_ell_first_moments_within_hist_mass": True,
              "original_cli_and_grouped_first_moment_results_identical": True,
              "all_separation_record_scalars_match": True,
              "prior_summary_comparison": identity(summary_path, repo),
              "all_prior_summary_price_scalars_match": True,
              "prices": expected, "K": str(K), "mean_menu_size": str(menu_size),
              "W": str(sum(utilities, F(0))), "O": "1",
              "strict_half_gap_one_minus_two_W": point["strict_half_gap"],
              "hist_price_decomposition": rows,
              "not_checked": ["5259 mother-matrix rows", "a complete common-catalog realization",
                              "full ordered-history strategy", "all SPE incentive constraints",
                              "other saved points or reoptimized points"]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "passed", "original_cli_invocations": 1,
                      "price_slack_signs": ["positive" if s > 0 else "negative" for s in slacks],
                      "capacity_slack_sign": "positive"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
