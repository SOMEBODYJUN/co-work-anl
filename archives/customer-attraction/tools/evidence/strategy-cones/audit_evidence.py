"""Check frozen-file integrity and the structure omitted by original replay CLIs.

The original exact verifiers check the mathematical primal/dual inequalities.
This complementary check validates all integer inputs, complete strategy maps,
comparison portfolios, provenance hashes, and historical-report equivalence.
It does not generate new equilibrium samples or repair missing duals.
"""
from pathlib import Path
from itertools import product, combinations
import hashlib
import json

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE / "original"


def check_actions(records, topics, players):
    histories = [tuple(x["history"]) for x in records]
    assert len(histories) == len(set(histories)), "duplicate decision history"
    expected = {h for d in range(players) for h in product(range(topics), repeat=d)}
    assert set(histories) == expected, "incomplete decision tree"
    assert all(type(x["action"]) is int and 0 <= x["action"] < topics for x in records)
    return len(histories)


def check_clones(values, topics):
    assert len(values) == (1 << topics) - 1
    assert all(type(x) is int and x >= 0 for x in values)
    assert any(values), "zero input cannot be welfare-normalized"


def main():
    manifest = json.loads((BASE / "source-manifest.json").read_text())
    for row in manifest:
        raw = (ORIGINAL / row["path"]).read_bytes()
        assert len(raw) == row["size"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    runs = ORIGINAL / "evidence/runs/2026-10-09"
    certified = json.loads((runs / "customer_attraction_strategy_lp_m4p5_certified.json").read_text())
    earlier = json.loads((runs / "customer_attraction_strategy_lp_m4p5.json").read_text())
    agreement = ["best", "cone_metadata", "cones", "distinct_inputs", "exact_primal_candidates", "exact_optimal_dual_certificates"]
    assert all(certified[k] == earlier[k] for k in agreement)
    script = ORIGINAL / "tests/audits/customer_attraction_strategy_lp.py"
    assert certified["audit_script_sha256"] == hashlib.sha256(script.read_bytes()).hexdigest()
    topics, players = certified["parameters"]["topics"], certified["parameters"]["players"]
    portfolios = set(combinations(range(topics), min(topics, players)))
    nulls, tree_keys = [], []
    for index, cone in enumerate(certified["cone_proofs"]):
        check_actions(cone["actions"], topics, players)
        tree_keys.append(tuple(sorted((tuple(x["history"]), x["action"]) for x in cone["actions"])))
        proofs = cone["portfolio_proofs"]
        assert len(proofs) == len(portfolios)
        assert {tuple(x["portfolio"]) for x in proofs} == portfolios
        for proof in proofs:
            check_clones(proof["integer_clones"], topics)
            if proof["dual_bound"] is None:
                assert not proof["dual_support"]
                nulls.append({"zero_based_cone_index": index, "portfolio": proof["portfolio"]})
    assert len(set(tree_keys)) == len(tree_keys) == certified["cones"] == 70
    assert len(nulls) == certified["unrecovered_optimal_duals"] == 2
    credible = json.loads((runs / "cone_attack_credible_selected.json").read_text())
    sampler = ORIGINAL / "tests/audits/cone_attack_credible_variants.py"
    assert credible["replay_script_sha256"] == hashlib.sha256(sampler.read_bytes()).hexdigest()
    selected = []
    for batch in credible["batches"]:
        topics, players = batch["topics"], batch["players"]
        for cone in batch["cone_proofs"]:
            nodes = check_actions(cone["strategy"]["actions"], topics, players)
            check_clones(cone["source_integer_clones"], topics)
            actions = {tuple(x["history"]): x["action"] for x in cone["strategy"]["actions"]}
            path = ()
            for _ in range(players):
                path += (actions[path],)
            for proof in cone["portfolio_proofs"]:
                check_clones(proof["integer_clones"], topics)
                assert tuple(proof["portfolio"]) == tuple(range(topics))
            selected.append({"family": cone["source_family"], "ordered_decision_nodes": nodes,
                             "actual_path": path, "statistics_on_original_input": cone["statistics"]})
    result = {"frozen_files_hash_verified": len(manifest),
              "same_historical_strategy_sample": True,
              "distinct_complete_four_provider_trees": len(tree_keys),
              "unrecovered_duals": nulls,
              "selected_credible_trees": selected,
              "scope": "structural integrity and provenance; pair with original exact replay outputs"}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
