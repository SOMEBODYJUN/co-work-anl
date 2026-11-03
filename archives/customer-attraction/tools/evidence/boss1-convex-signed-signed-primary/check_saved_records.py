"""Read-only exact arithmetic/structure check of six frozen signed records.

Does not import or execute any source entry, SPE solver, LP, or verifier.
Does not recompute M, enumerate SPE outcomes, or certify the 769-row cone.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed"
DEPENDENCY = HERE / "dependency"


def load(path):
    return json.loads(path.read_text())


def costs(g):
    p = [max(x, 0) for x in g]
    n = [max(-x, 0) for x in g]
    return 2 * sum(p) - sum(n) + max(p, default=0) + max(n, default=0)


def leaf(customers, path):
    payoff = [F(0) for _ in path]
    coverage = F(0)
    for row in customers:
        mass = F(row.get("weight", row.get("multiplicity")))
        owners = [i for i, a in enumerate(path) if a in row["topics"]]
        if owners:
            coverage += mass
            for i in owners:
                payoff[i] += mass / len(owners)
    return payoff, coverage


def main():
    manifest = load(HERE / "source-manifest.json")
    checked = []
    for record in manifest["primary"] + manifest["dependencies"]:
        # Paths are repository-relative, independent of the caller's cwd.
        marker = "boss1-convex-signed-signed-primary/"
        path = HERE / record["local_path"].split(marker, 1)[1]
        data = path.read_bytes()
        assert len(data) == record["size"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
        checked.append(record["id"])

    designated = load(SOURCE / "designated_seed_attack.json")
    root_data = load(DEPENDENCY / "examples/customer_attraction/root_tax_failure.json")
    assert designated["root_tax_m4"]["instance"] == root_data
    assert designated["root_tax_m5"]["instance"] == dict(root_data, players=5)
    leaf_checks = []
    prices = {"lambda1": F(1), "lambda3/2": F(3, 2), "lambda2": F(2)}
    for name, case in designated.items():
        for key, row in case["minima"].items():
            u, welfare = leaf(case["instance"]["customers"], row["path"])
            assert list(map(str, u)) == row["u"] and welfare == row["W"]
            g = [F(x) - y for x, y in zip(row["M_early"], u)]
            assert list(map(str, g)) == row["g"]
            b = 2 * welfare - row["OPT"]
            assert b == row["B"] and costs(g) == F(row["C"])
            budget = b + (costs(g) if key == "signed" else prices[key] * sum(g))
            assert budget == F(row["value"])
            leaf_checks.append([name, key, str(budget)])

    cone = load(SOURCE / "one_cone_seed_attack.json")
    masses = cone["nonzero_weights"]
    assert len({tuple(r["topics"]) for r in masses}) == len(masses) == 7
    assert all(F(r["weight"]) > 0 for r in masses)
    assert sum(F(r["weight"]) for r in masses) == F(cone["rational_sum_weights"]) == 1
    u, welfare = leaf(masses, cone["target"])
    assert list(map(str, u)) == cone["u"]
    g = [F(x) - y for x, y in zip(cone["U"], u)]
    assert list(map(str, g)) == cone["rational_g"]
    comparator = [a for a in range(6) if a != cone["best_comparator_omits"]]
    _, covered = leaf(masses, comparator)
    b = 2 * welfare - covered
    assert b == F(cone["B_comparator"])
    assert b + costs(g) == F(cone["rational_seed_budget"]) == F(2, 5)
    # Finite price-grid size is metadata, not a rerun of the LP.
    price_count = sum(sum(max(1-x, 0) for x in v) <= 1
                      and sum(max(x-2, 0) for x in v) <= 1
                      for v in product(range(4), repeat=4))

    review = load(SOURCE / "independent_floor_deletion_review.json")
    raw = load(DEPENDENCY / "research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/credible/true_reset_floor_counterexample.json")
    a = review["original"]["supplied_policy_audit"]
    b_audit = review["original"]["reconstructed_policy_audit"]
    assert a == b_audit
    policy = {tuple(r["history"]): r["action"] for r in review["original"]["independently_reconstructed_policy"]}
    supplied = {tuple(r["history"]): r["action"] for r in raw["certificate"]["actions"]}
    assert policy == supplied
    histories = {h for d in range(4) for h in product(range(4), repeat=d)}
    assert set(policy) == histories and len(policy) == 85
    for audit in (a, b_audit):
        assert len(audit["comparisons"]) == audit["all_forced_comparisons"] == 340
        assert {(tuple(r["history"]), r["forced"]) for r in audit["comparisons"]} == {
            (h, t) for h in histories for t in range(4)}
        assert min(F(r["IC_gap"]) for r in audit["comparisons"]) == F(audit["minimum_IC_gap"]) == 0
        assert all(set(r) == {"history", "forced", "obey_terminal", "forced_terminal", "IC_gap"}
                   for r in audit["comparisons"])
    deleted = review["deleted_game"]
    assert len(deleted["full_floor_table"]) == 21
    assert {tuple(r["history"]) for r in deleted["full_floor_table"]} == {
        h for d in range(3) for h in product(range(4), repeat=d)}
    for row in deleted["full_floor_table"]:
        assert set(row["ell"]) == {"0", "1", "2", "3"}
        assert max(map(F, row["ell"].values())) == F(row["mu"])
    for row in deleted["target_prefix_floor_table"]:
        assert len(row["all_forced_actions"]) == 4
        assert max(F(r["ell"]) for r in row["all_forced_actions"]) == F(row["mu"])
    deficits = [F(x)-F(y) for x, y in zip(deleted["mu"], deleted["target_profits"])]
    assert list(map(str, deficits)) == deleted["signed_deficits"]
    assert sum(deficits) == sum(max(x, 0) for x in deficits) == 11
    assert sum(deficits) - F(deleted["deleted_original_profit"]) == F(5, 3)
    print(json.dumps({
        "status": "PASS: saved-record arithmetic and structure only",
        "source_and_dependency_hashes_checked": checked,
        "designated_saved_leaf_records": leaf_checks,
        "fixed_cone_saved_point": {"W": str(welfare), "chosen_comparator_coverage": str(covered),
                                  "B_plus_C": cone["rational_seed_budget"], "price_grid_count": price_count},
        "floor_saved_structure": {"audit_dicts_equal": a == b_audit,
                                  "reconstructed_actions_equal_supplied": policy == supplied,
                                  "actions": len(policy), "saved_comparison_rows_each": 340,
                                  "full_floor_rows": 21, "failure_gap": "5/3"},
        "limits": ["M and stated minima not recomputed", "no SPE BI or policy replay",
                   "769 IC rows not regenerated", "no LP or exact dual",
                   "no source entry or canonical code imported/executed"]
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
