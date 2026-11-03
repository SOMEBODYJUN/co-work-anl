"""Read-only identity, schema, transcription and policy-difference checks.

This does not evaluate utilities, check IC, optimize coverage, invoke an LP or
execute any frozen program.  Its report deliberately keeps those boundaries.
"""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

IDS = ["caf0a6e05a87748367c4", "397a11a3aebb0a75bf68",
       "9019138f2770c8cf5e5b", "71bb086422d9f9255f6d"]
EVIDENCE = Path("archives/customer-attraction/tools/evidence/root-regret-discovery-and-frozen-audit-four-primary")
ORIGINAL = EVIDENCE / "original"
KEYS = {"kind", "instance", "actions", "actual", "root_deviation_payoffs",
        "actual_root_payoff", "root_regret", "positive_depth_decision_histories",
        "all_ordered_positive_depth_IC_verified_exactly", "W", "OPT_m"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def walk(actions, prefix=()):
    while len(prefix) < 4:
        prefix += (actions[prefix],)
    return list(prefix)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--primary-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inventory = {r["id"]: r for r in
                 map(json.loads, (args.repo / "cleanup/inventory.jsonl").read_text().splitlines())
                 if r["id"] in IDS}
    records, objects, policies = [], [], []
    args.output.mkdir(parents=True, exist_ok=True)
    receipt_dir = args.output / "clean-show-receipts"
    receipt_dir.mkdir(exist_ok=True)
    tables = ["# 四份原种子的完整有序动作表", "",
              "本表只作无损转写；每份根、6个第二位、36个第三位、216个末位全部保留。",
              "第三位矩阵的行/列为首/次行动；末位矩阵每块固定首行动，行/列为次/第三行动。", ""]
    for source_id in IDS:
        row = inventory[source_id]
        source_path = ORIGINAL / row["path"]
        data = (args.repo / source_path).read_bytes()
        assert len(data) == row["size"] and digest(data) == row["sha256"]
        primary_path = args.primary_dir / f"{source_id}.json"
        receipt_path = args.primary_dir / f"{source_id}.receipt.json"
        receipt_data = receipt_path.read_bytes()
        receipt = json.loads(receipt_data)
        assert receipt["source"] == row
        assert Path(receipt["output"]) == primary_path
        assert primary_path.read_bytes() == data
        (receipt_dir / receipt_path.name).write_bytes(receipt_data)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert blob == row["blob"]
        obj = json.loads(data)
        assert set(obj) == KEYS
        assert obj["kind"] == "full root-only source plan; root may be suboptimal"
        inst = obj["instance"]
        assert set(inst) == {"topics", "customers", "players"}
        assert inst["players"] == 4 and inst["topics"] == list(map(str, range(6)))
        customers = inst["customers"]
        for customer in customers:
            assert set(customer) == {"topics", "multiplicity"}
            assert type(customer["multiplicity"]) is int and customer["multiplicity"] > 0
            assert customer["topics"] and len(customer["topics"]) == len(set(customer["topics"]))
            assert all(type(a) is int and 0 <= a < 6 for a in customer["topics"])
        signatures = [tuple(i for i, c in enumerate(customers) if a in c["topics"])
                      for a in range(6)]
        assert len(set(signatures)) == 6
        actions = {}
        for record in obj["actions"]:
            assert type(record) is list and len(record) == 2
            history, action = record
            assert type(history) is list and all(type(a) is int and 0 <= a < 6 for a in history)
            assert type(action) is int and 0 <= action < 6
            history = tuple(history)
            assert history not in actions
            actions[history] = action
        expected = {h for d in range(4) for h in product(range(6), repeat=d)}
        assert set(actions) == expected and len(actions) == 259
        assert walk(actions) == obj["actual"]
        assert obj["positive_depth_decision_histories"] == 258
        assert obj["all_ordered_positive_depth_IC_verified_exactly"] is True
        assert len(obj["root_deviation_payoffs"]) == 6
        for value in obj["root_deviation_payoffs"] + [obj["actual_root_payoff"], obj["root_regret"]]:
            assert isinstance(value, str)
        rec = dict(row)
        rec.update({"existing_frozen_copy": source_path.as_posix(),
                    "normal_clean_show_export": str(primary_path),
                    "normal_clean_show_receipt": "clean-show-receipts/" + receipt_path.name,
                    "normal_clean_show_receipt_sha256": digest(receipt_data),
                    "normal_clean_show_matches_frozen_copy": True,
                    "full_file_reviewed": True, "byte_identity_passed": True,
                    "top_level_keys": sorted(obj),
                    "customer_rows": len(customers),
                    "unit_customers": sum(c["multiplicity"] for c in customers),
                    "topic_sizes": [sum(c["multiplicity"] for c in customers if a in c["topics"])
                                    for a in range(6)],
                    "distinct_coverage_signatures": 6,
                    "decision_histories_by_depth": {str(d): sum(len(h) == d for h in actions) for d in range(4)},
                    "root_action": actions[()], "actual": obj["actual"],
                    "forced_root_paths": [walk(actions, (a,)) for a in range(6)],
                    "declared_root_deviation_payoffs": obj["root_deviation_payoffs"],
                    "declared_actual_root_payoff": obj["actual_root_payoff"],
                    "declared_root_regret": obj["root_regret"],
                    "declared_W": obj["W"], "declared_OPT_m": obj["OPT_m"]})
        records.append(rec)
        objects.append(obj)
        policies.append(actions)
        tables += [f"## {Path(row['path']).name} ({source_id})", "",
                   f"根行动：{actions[()]}", "",
                   "第二位（首行动0…5）：`" + ",".join(str(actions[(a,)]) for a in range(6)) + "`", "",
                   "第三位：", "", "| 首/次 | 0 | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|---|"]
        for a in range(6):
            tables.append("| " + str(a) + " | " + " | ".join(str(actions[(a, b)]) for b in range(6)) + " |")
        for a in range(6):
            tables += ["", f"末位，首行动={a}：", "", "| 次/第三 | 0 | 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|---|---|"]
            for b in range(6):
                tables.append("| " + str(b) + " | " + " | ".join(str(actions[(a, b, c)]) for c in range(6)) + " |")
        tables.append("")
    differences = []
    for left, right in [(0, 1), (2, 3)]:
        diff = [{"history": list(h), "left_action": policies[left][h], "right_action": policies[right][h]}
                for h in sorted(policies[left], key=lambda h: (len(h), h))
                if policies[left][h] != policies[right][h]]
        differences.append({"left": IDS[left], "right": IDS[right],
                            "identical_instance": objects[left]["instance"] == objects[right]["instance"],
                            "policy_differences": diff})
    assert differences[0]["policy_differences"] == [{"history": [5, 0, 0], "left_action": 0, "right_action": 4}]
    assert differences[1]["policy_differences"] == [{"history": [], "left_action": 5, "right_action": 3}]
    assert objects[2]["instance"]["customers"][:5] == objects[0]["instance"]["customers"]
    related = []
    for name in ["audit_frozen_sources.py", "frozen_sources_exact_audit.json", "root_regret_discovery_report.json"]:
        path = ORIGINAL / Path(records[0]["path"]).parent / name
        data = (args.repo / path).read_bytes()
        related.append({"existing_path": path.as_posix(), "size": len(data), "sha256": digest(data),
                        "full_file_reviewed": True, "executed_this_batch": False})
    report = {"scope": "identity/schema/full-history domain/metadata transcription/policy differences only",
              "original_program_executions": 0, "new_IC_comparisons": 0,
              "new_utility_evaluations": 0, "new_OPT_enumerations": 0, "new_LP_calls": 0,
              "sources": records, "within_variant_differences": differences,
              "v1_extends_v0_by_customer_rows": 11,
              "related_frozen_evidence": related}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "structure-and-differences.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (args.output / "ordered-action-tables.md").write_text("\n".join(tables) + "\n")
    print(json.dumps({"sources": len(records), "identical_bytes": True,
                      "decisions_per_source": 259, "policy_differences": differences,
                      "new_IC_comparisons": 0, "new_OPT_enumerations": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
