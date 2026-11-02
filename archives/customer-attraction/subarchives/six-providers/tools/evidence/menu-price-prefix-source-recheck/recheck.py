"""Recheck three frozen audit sources without modifying any archived input.

The full prefix computation replays the original solver.  Only the last-two
player calculation below is an independent SPE calculation.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = repo / "archives/customer-attraction/tools/evidence"
    six = repo / "archives/customer-attraction/subarchives/six-providers/tools/evidence"
    frozen = base / "menu-price-and-prescribed-prefix-audits-primary/frozen-inputs"
    original = six / "boss6-full18-prefix/original"
    paths = {
        "ddf2520de2255a1c4472": frozen / "ddf2520de2255a1c4472-B_menu_actual_price_separation.json",
        "59a90ea11a2df684017e": frozen / "59a90ea11a2df684017e-audit_B_menu_actual_prices.py",
        "9536369246be24174433": original / "research_1/audit_seed_actual_prefix.py",
        "69c73607edd62b9b0e42": base / "swap-B-visible-and-histogram-projection-two-primary/source-root/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/coupled_B_master_exact.json",
        "e3b91330bfecffa97610": original / "research_1/bigint_controller_attack.py",
        "faa31af555920b59561d": original / "research_1/full18_cone_attack.py",
        "40f4176105c101f8cea8": original / "research_5/seed18_Rdiag.json",
        "e6866c6c6c9f1ec30857": original / "research_1/seed18_Rdiag_actual_prefix_audit.json",
    }
    inventory = {rec["id"]: rec for line in (repo / "cleanup/inventory.jsonl").read_text().splitlines()
                 if (rec := json.loads(line))["id"] in paths}
    identities = []
    for source_id, path in paths.items():
        raw = path.read_bytes()
        rec = inventory[source_id]
        assert len(raw) == rec["size"]
        assert hashlib.sha256(raw).hexdigest() == rec["sha256"]
        identities.append({**rec, "used_path": str(path.relative_to(repo)),
                           "role": "primary" if source_id in list(paths)[:3] else "related-input-or-dependency"})
    dump(out / "source-manifest.json", identities)

    price = subprocess.run([sys.executable, str(paths["59a90ea11a2df684017e"]), "--point",
                            str(paths["69c73607edd62b9b0e42"])], text=True, capture_output=True, check=True)
    assert price.stderr == ""
    (out / "price.stdout.json").write_text(price.stdout)
    actual_price = json.loads(price.stdout)
    point = json.loads(paths["69c73607edd62b9b0e42"].read_bytes())
    columns = point["columns"]
    hist = {j: c for j, c in enumerate(columns) if c["kind"] == "hist"}
    assert Counter(c["kind"] for c in columns) == {"K": 1, "hist": 16, "joint-reply": 582,
                                                   "overlap": 1306, "actual-B-branch-state": 128}
    assert all(F(c["weight"]) >= 0 for c in columns)
    first_moments = {j: F(0) for j in hist}
    masses = {j: F(0) for j in hist}
    states = {j: set() for j in hist}
    for c in columns:
        if c["kind"] != "actual-B-branch-state":
            continue
        j = c["hist_column"]
        assert j in hist
        state = c["Q"], c["R"], c["ell"]
        assert c["Q"] in (0, 1) and c["R"] in (0, 1) and c["ell"] in (0, 6)
        assert state not in states[j]
        states[j].add(state)
        masses[j] += F(c["weight"])
        first_moments[j] += F(c["weight"]) * F(c["ell"], 6)
    assert all(len(states[j]) == 8 and masses[j] == F(hist[j]["weight"]) for j in hist)
    utilities, prices = [F(0)] * 6, [F(0)] * 6
    for j, c in hist.items():
        bits = [int(b) for b in c["actual_bits"]]
        assert len(bits) == 6 and set(bits) <= {0, 1}
        for a in range(6):
            if bits[a]:
                utilities[a] += F(c["weight"]) / sum(bits)
            prices[a] += first_moments[j] / (sum(bits[:a]) + 6 - a)
    capacity = sum((F(c["weight"]) for c in columns if c["kind"] == "K"), F(0)) - sum(first_moments.values(), F(0))
    slacks = [u - p for u, p in zip(utilities, prices)]
    assert actual_price["actual_utilities"] == list(map(str, utilities))
    assert actual_price["reply_family_prices"] == list(map(str, prices))
    assert actual_price["price_slacks"] == list(map(str, slacks))
    assert actual_price["capacity_slack"] == str(capacity)
    separation = json.loads(paths["ddf2520de2255a1c4472"].read_bytes())
    assert separation["point_sha256"] == actual_price["source_sha256"] == inventory["69c73607edd62b9b0e42"]["sha256"]
    assert F(separation["u6"]) == utilities[-1]
    assert F(separation["reply_family_average_price"]) == prices[-1]
    assert F(separation["minimum_row_value"]) == slacks[-1] == -F(separation["violation"]) < 0
    assert all(s > 0 for s in slacks[:-1]) and capacity > 0

    # Preserve argv and relative input identity while isolating the output write.
    with tempfile.TemporaryDirectory(prefix="prefix-runtime-", dir=out) as directory:
        run = Path(directory)
        (run / "research_1").mkdir()
        (run / "research_5").mkdir()
        for source_id in ("9536369246be24174433", "e3b91330bfecffa97610", "faa31af555920b59561d"):
            shutil.copyfile(paths[source_id], run / "research_1" / paths[source_id].name)
        shutil.copyfile(paths["40f4176105c101f8cea8"], run / "research_5/seed18_Rdiag.json")
        prefix = subprocess.run([sys.executable, "audit_seed_actual_prefix.py", "../research_5/seed18_Rdiag.json", "fresh"],
                                cwd=run / "research_1", text=True, capture_output=True, check=True)
        assert prefix.stderr == ""
        regenerated = json.loads((run / "research_1/fresh_actual_prefix_audit.json").read_text())
    (out / "prefix.stdout.txt").write_text(prefix.stdout)
    dump(out / "prefix-regenerated.json", regenerated)
    historical = json.loads(paths["e6866c6c6c9f1ec30857"].read_bytes())
    assert {k: v for k, v in regenerated.items() if k != "seconds"} == {k: v for k, v in historical.items() if k != "seconds"}

    seed = json.loads(paths["40f4176105c101f8cea8"].read_bytes())
    labels, customers = seed["topics"], seed["customers"]
    assert seed["players"] == 6 and len(labels) == 18 and len(customers) == 252
    assert len(set(labels)) == 18 and labels[:6] == ["A" + str(i) for i in range(1, 7)]
    total = sum(c["multiplicity"] for c in customers)
    seen = set()
    for c in customers:
        assert type(c["multiplicity"]) is int and c["multiplicity"] > 0
        support = frozenset(c["topics"])
        assert len(support) == len(c["topics"]) and all(type(a) is int and 0 <= a < 18 for a in support)
        assert support not in seen
        seen.add(support)

    # Direct customer-by-customer integer arithmetic, without Attack or solve.
    def payoff(counts, action):
        value = 0
        for c in customers:
            if action in c["topics"]:
                load = sum(counts[a] for a in c["topics"])
                assert load > 0 and 60 % load == 0
                value += c["multiplicity"] * (60 // load)
        return value

    target = [1] * 6 + [0] * 12
    for d, rec in enumerate(regenerated["checks"]):
        assert F(rec["actual_player_u_over_total"]) == F(payoff(target, d), 60 * total)
        witness = rec["floor_minimizing_terminal_counts"]
        action = labels.index(rec["best_security_action_label"])
        assert len(witness) == 18 and sum(witness) == 6
        assert all(witness[j] >= 1 for j in range(d)) and witness[action] >= 1 + int(action < d)
        assert F(rec["SPE_security_floor_over_total"]) == F(payoff(witness, action), 60 * total)
        assert F(rec["strict_floor_gap_over_total"]) == F(rec["SPE_security_floor_over_total"]) - F(rec["actual_player_u_over_total"])

    fifth_rows = []
    for a in range(18):
        replies = []
        for b in range(18):
            terminal = [int(j < 4) + int(j == a) + int(j == b) for j in range(18)]
            replies.append((payoff(terminal, b), payoff(terminal, a), b))
        last_best = max(v[0] for v in replies)
        best_replies = [v for v in replies if v[0] == last_best]
        minimum = min(v[1] for v in best_replies)
        fifth_rows.append({"action": labels[a], "last_best_reply_labels": [labels[v[2]] for v in best_replies],
                           "minimum_fifth_payoff_over_total": str(F(minimum, 60 * total))})
    floor = max(F(r["minimum_fifth_payoff_over_total"]) for r in fifth_rows)
    fifth = regenerated["checks"][4]
    assert floor == F(fifth["SPE_security_floor_over_total"])
    assert next(r for r in fifth_rows if r["action"] == fifth["best_security_action_label"])["minimum_fifth_payoff_over_total"] == str(floor)
    assert "A6" in fifth_rows[4]["last_best_reply_labels"]
    assert floor > F(fifth["actual_player_u_over_total"])
    last_payoffs = []
    for a in range(18):
        counts = [int(j < 5) + int(j == a) for j in range(18)]
        last_payoffs.append(payoff(counts, a))
    assert last_payoffs[5] == max(last_payoffs)
    assert F(last_payoffs[5], 60 * total) == F(regenerated["checks"][5]["SPE_security_floor_over_total"])
    dump(out / "independent-tail.json", {"method": "direct integer enumeration of all 18x18 last-two-player terminals; all exact last-player best replies retained",
         "customers_consumed": len(customers), "total_unit_customers": str(total), "fifth_action_rows": fifth_rows,
         "fifth_full_SPE_floor_over_total": str(floor), "fifth_strict_gap_over_total": fifth["strict_floor_gap_over_total"],
         "last_actual_action_is_best_reply": True,
         "scope": "Independent SPE check only at depth4 and depth5; depth0..3 min/max membership comes from original solver replay."})
    import numpy
    import scipy
    dump(out / "verification.json", {"status": "passed", "python": platform.python_version(), "numpy": numpy.__version__,
         "scipy": scipy.__version__, "frozen_identities_checked": len(paths), "original_price_cli_invocations": 1,
         "original_full_prefix_cli_invocations": 1, "prefix_all_fields_except_top_level_seconds_equal": True,
         "price_grouped_first_moment_result_equal": True, "price_slack_signs": ["positive" if v > 0 else "negative" for v in slacks],
         "capacity_slack_sign": "positive", "independent_last_two_player_terminals": 324,
         "all_six_reported_actual_and_witness_payoffs_directly_recomputed": True,
         "not_checked": ["5259 mother-matrix feasibility", "other saved price points", "global independent full-SPE solver", "full ordered-history strategy certificate", "general six-player half theorem"]})
    print("passed: 8 frozen identities, two original CLI replays, grouped prices, independent 324-terminal tail")


if __name__ == "__main__":
    main()
