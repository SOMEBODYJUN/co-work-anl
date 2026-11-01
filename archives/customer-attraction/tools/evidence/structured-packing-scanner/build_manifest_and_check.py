"""Record the reviewed source identities and perform bounded delivery checks."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from tools.vendor.matek.frontmatter import parse_flat_frontmatter

BODY = ROOT / "archives/customer-attraction/state/程序/结构化相对私有块策略锥扫描器--程序.md"
RECEIPT = ROOT / "cleanup/workspaces/Boss7/receipts-round4/df0869a6fbef9062a300.json"

def digest(path):
    data = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def main():
    inventory = {v["id"]: v for v in map(json.loads, (ROOT / "cleanup/inventory.jsonl").read_text().splitlines())}
    originals = {"df0869a6fbef9062a300": "structured_packing_scan.py",
                 "ebc029a8cdb5b255c1a2": "private_block_scan.py",
                 "8774aded792c416dc2cf": "coverage_loss_cone_scan.py"}
    sources = []
    for sid, filename in originals.items():
        entry = inventory[sid]
        saved = digest(HERE / "original" / filename)
        assert saved["sha256"] == entry["sha256"] and saved["bytes"] == entry["size"]
        sources.append({"source": entry, "preserved": saved,
                        "role": "primary cleaned source" if sid == "df0869a6fbef9062a300" else "fully read comparison only; not dispositioned here"})
    replay = []
    for n, sid in [(4, "c44723ed32d119642928"), (5, "9d2fb6b26cc4ae9f2ce7"), (6, "e1ebb4aec12d1c0727fe")]:
        path = HERE / "rerun/research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/induction" / ("structured_packing_" + str(n) + ".json")
        saved, entry = digest(path), inventory[sid]
        assert saved["sha256"] == entry["sha256"] and saved["bytes"] == entry["size"]
        observed_path = HERE / "rerun" / ("observed_" + str(n) + ".json")
        observed = json.loads(observed_path.read_text())
        assert observed["last_move_difference_from_exact_priority"] == []
        assert observed["exact_seed_minimum_ic_slack_for_observed_policy"] == "0"
        assert observed["success"]
        replay.append({"n": n, "frozen_report_source": entry, "new_original_format_output": saved,
                       "byte_equal_to_frozen_report": True, "observed": digest(observed_path),
                       "ratio": observed["ratio"], "seed_exact_ic_minimum": "0",
                       "last_action_policy_equal_to_fraction_priority": True,
                       "final_lp_point_is_not_exactly_certified_by_this_replay": True})
    related = [
        ("定义/共同目录完整历史模型--定义.md", "full-history quantifiers, exact unit-customer interpretation, and limitations of count compression"),
        ("反例/任意人数首步补全余额--反例.md", "complete analytic seed and strategy family; all sections read including general-n full-history proof and the distinction from half"),
        ("定理/实际遗漏私有席位谱与锐界--定理.md", "global maximal-cover private blocks, actual omissions and single-block-touch property; cannot substitute the LP's relative blocks"),
        ("定理/小外部主题闭合的相对核心容量归纳与自动半覆盖--定理.md", "relative-core use requires strictly small outside actions and compliant-prefix closure, absent from this LP"),
        ("引理/最优首动作菜单与真实孩子损失--引理.md", "all credit terms and true continuation branch definitions; packing is not the loss objective"),
        ("引理/最优补全私有块交换与分支账本--引理.md", "static exchange includes outside credit e and completion slack; E_j alone is not first-step loss")]
    comparisons = [{**digest(ROOT / "archives/customer-attraction/state" / p), "read_scope": "full text", "comparison": note} for p, note in related]
    write_json("comparison.json", {"status": "local-prepared", "search_scope": "whole repository structured_packing; customer-attraction state relative/global private blocks and arbitrary-n first-prefix balance; frozen inventory adjacent induction scripts",
             "formal_full_text_reads": comparisons, "frozen_full_text_reads": list(originals) + ["c44723ed32d119642928", "9d2fb6b26cc4ae9f2ce7", "e1ebb4aec12d1c0727fe"],
             "not_run": ["private_block_scan.py", "coverage_loss_cone_scan.py"],
             "relation_decision": "Preserve source/implementation link to the all-n seed family, finite-check links to three reports, and distinction from private-spectrum and exchange lemmas. No stage-three hyperedges created."})
    write_json("manifest.json", {"status": "local-prepared", "primary_source_id": "df0869a6fbef9062a300",
             "preserved_frozen_sources": sources, "actual_original_entry_replays": replay,
             "execution": digest(HERE / "rerun/run-metadata.json"), "stdout": digest(HERE / "rerun/stdout.txt"),
             "wrapper": digest(HERE / "replay_original.py"),
             "scope": "Exactly the original n=4,5,6 entry; unchanged source in isolated cwd. Fraction audit here covers the integer seed and observed policy, not the optimized LP primal/dual."})
    meta, _ = parse_flat_frontmatter(BODY.read_text())
    assert meta["id"] == "customer-attraction/structured-relative-private-packing-cone-scanner"
    assert meta["kind"] == "program" and meta["type_tag"] == "程序"
    parsed = []
    for path in sorted(HERE.rglob("*.json")):
        json.loads(path.read_text())
        parsed.append(str(path.relative_to(ROOT)))
    receipt = json.loads(RECEIPT.read_text())
    assert receipt["id"] == "df0869a6fbef9062a300"
    assert receipt["status"] == "local-prepared"
    for key in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]:
        assert receipt[key] is True
    for key in ["read_note", "comparison_note", "decision_note", "disposition", "targets"]:
        assert receipt[key]
    target_checks = [{"path": p, "exists": (ROOT / p).is_file()} for p in receipt["targets"]]
    assert all(x["exists"] for x in target_checks)
    link_checks = []
    for path in [BODY, HERE / "README.md"]:
        for raw in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in raw or raw.startswith("#"):
                continue
            dest = (path.parent / raw.split("#")[0]).resolve()
            link_checks.append({"from": str(path.relative_to(ROOT)), "target": raw, "exists": dest.exists()})
    assert all(x["exists"] for x in link_checks)
    report = {"status": "local-prepared", "frontmatter": meta, "json_files_parsed": parsed,
              "targets": target_checks, "links": link_checks, "source_hash_checks": "all passed",
              "replay_report_hashes_equal_frozen": True, "final_body": digest(BODY),
              "limit": "These are packaging/identity checks plus the separately recorded seed audit; mathematical correctness and exact LP optimality are not established by receipt fields."}
    write_json("self-check.json", report)
    print(json.dumps({"status": "local-prepared", "source_hashes": len(sources), "byte_equal_report_replays": len(replay),
                      "json_files": len(parsed), "targets": len(target_checks), "links": len(link_checks)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
