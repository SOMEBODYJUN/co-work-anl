"""Source integrity and delivery checks; this does not rerun the mathematical audit."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from tools.vendor.matek.frontmatter import parse_flat_frontmatter

BODY = ROOT / "archives/customer-attraction/state/程序/两早期主题包含倒二主题的系数审计器--程序.md"
RECEIPT = ROOT / "cleanup/workspaces/Boss7/receipts-round5/fb711c988a2ccab98a34.json"

def digest(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def main():
    inventory = {d["id"]: d for d in map(json.loads, (ROOT / "cleanup/inventory.jsonl").read_text().splitlines())}
    frozen = {
        "fb711c988a2ccab98a34": "audit_containment.py",
        "8fff587b128fa834d9ad": "two_early_containment_half.md",
        "ce7cab7fea0055068309": "uniform_K_obstruction.md",
        "4c694dba9897907a4613": "omitted_optimal_multiplicity.md",
        "2febc458086d3c08984e": "workspace_README.md",
    }
    sources = []
    for sid, name in frozen.items():
        source = inventory[sid]
        saved = digest(HERE / "original" / name)
        assert saved["bytes"] == source["size"] and saved["sha256"] == source["sha256"]
        sources.append({"source": source, "preserved": saved, "full_text_read": True,
                        "role": "primary source" if sid == "fb711c988a2ccab98a34" else "comparison only; no primary disposition here"})
    report_source = inventory["ed3ef7914a7082563bef"]
    replay = digest(HERE / "rerun/original_stdout.json")
    assert replay["bytes"] == report_source["size"] and replay["sha256"] == report_source["sha256"]
    out = json.loads((HERE / "rerun/original_stdout.json").read_text())
    expected = {"status": "passed", "scope": "existing conditional coefficient theorem; no unrestricted HALF-6 claim",
                "reduced_states": 1960, "states_with_feasible_overlap": 3360,
                "minimum_residual": "0", "nonzero_state_minimum_residual": "0",
                "F6": "2352949/6718464", "beta": "6718464/2352949",
                "multiplicity_two_bound": "9071413/4705898",
                "necessary_single_omission_fraction": "340383/2352949"}
    assert out == expected
    metadata = json.loads((HERE / "rerun/metadata.json").read_text())
    assert metadata["assertions_enabled"] and metadata["source_unchanged"] and metadata["returncode"] == 0
    assert not (HERE / "rerun/original_stderr.txt").read_bytes()
    related = [
        ("定义/共同目录完整历史模型--定义.md", "Full-history common-catalog unit-customer semantics, already read in preceding source task and reused here."),
        ("证明/六人倒二双包含证书与统一K模板边界--证明.md", "Read complete positive certificate, all 1960 local types and the distinct three-row uniform-K obstruction; current code uses H1,H2,L, not K."),
        ("引理/实际遗漏比较重数的真实前缀需求递推--引理.md", "Read complete true-prefix recurrence, nontruncated fractional extension and six-player conditions; source code checks only constants."),
        ("资源/六人冻结前沿的条件谱与共享回复接续账本--资源.md", "Read complete historical frontier and explicit prior-batch code-unread boundary; this task adds the actual code read/replay without rewriting old scope."),
        ("审查/三重早期覆盖证书的含交集重构范围--审查.md", "Read complete P3 condition, 2058/3528 domain and signed defects; cannot merge with present 1960/3360 or fixed-pair containment."),
    ]
    comparisons = [{**digest(ROOT / "archives/customer-attraction/state" / name), "read_scope": "full text", "comparison": note} for name, note in related]
    write_json("comparison.json", {"status": "local-prepared", "search_scope": "whole-repository audit_containment, two-early containment and exact multiplicity constants; frozen inventory and formal customer-attraction objects",
               "frozen_full_text_reads": list(frozen) + ["ed3ef7914a7082563bef"], "formal_full_text_reads": comparisons,
               "relation_decision": "Implementation/replay of the existing conditional coefficient proof; independent arithmetic reuse of the multiplicity lemma; comparison against uniform-K and P3, not a new unconditional theorem. Stage-three edges deferred.",
               "not_run": ["uniform-K replay or LP", "P3 audit", "general multiplicity audit", "game or SPE enumeration"]})
    write_json("manifest.json", {"status": "local-prepared", "primary_source_id": "fb711c988a2ccab98a34", "preserved_sources": sources,
               "report_frozen_source": report_source, "replayed_stdout": replay, "byte_equal_to_frozen_report": True,
               "original_entry_invocations_this_task": 2, "invocation_notes": "First normal interpreter, then final -I isolated interpreter; both yielded identical 405 bytes. The saved metadata is the final run.",
               "execution": digest(HERE / "rerun/metadata.json"), "stderr": digest(HERE / "rerun/original_stderr.txt"),
               "wrapper": digest(HERE / "replay_original.py"), "scope": "Original coefficient and constant audit only; no separate new mathematical verification in this checker."})
    meta, _ = parse_flat_frontmatter(BODY.read_text())
    assert meta["id"] == "customer-attraction/two-early-containment-coefficient-auditor"
    assert meta["kind"] == "program" and meta["type_tag"] == "程序"
    receipt = json.loads(RECEIPT.read_text())
    assert receipt["id"] == "fb711c988a2ccab98a34" and receipt["status"] == "local-prepared"
    for key in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        assert receipt[key] is True
    for key in ("read_note", "comparison_note", "decision_note", "disposition", "targets"):
        assert receipt[key]
    targets = [{"path": p, "exists": (ROOT / p).is_file()} for p in receipt["targets"]]
    assert all(x["exists"] for x in targets)
    links = []
    for path in (BODY, HERE / "README.md"):
        for raw in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in raw or raw.startswith("#"):
                continue
            exists = (path.parent / raw.split("#")[0]).resolve().exists()
            links.append({"from": str(path.relative_to(ROOT)), "target": raw, "exists": exists})
    assert all(d["exists"] for d in links)
    parsed = []
    for path in sorted(HERE.rglob("*.json")):
        json.loads(path.read_text())
        parsed.append(str(path.relative_to(ROOT)))
    write_json("self-check.json", {"status": "local-prepared", "frontmatter": meta, "source_hashes": "5/5 passed", "replay_hash_equal_to_frozen_report": True,
               "all_ten_output_fields_equal_expected": True, "json_parsed": parsed, "targets": targets, "links": links,
               "formal_body": digest(BODY), "scope": "Packaging, source identity and captured execution checks; global SPE row legality is justified in the body, not by this script."})
    print(json.dumps({"status": "local-prepared", "original_sources": len(sources), "byte_equal_report": True,
                      "json_files": len(parsed), "targets": len(targets), "links": len(links)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
