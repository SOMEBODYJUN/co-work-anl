"""Check preserved identities and current matrix internals; never execute old audits."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from tools.vendor.matek.frontmatter import parse_flat_frontmatter

BODY = ROOT / "archives/customer-attraction/state/程序/完整156主题的作者两人尾审计器--程序.md"
RECEIPT = ROOT / "cleanup/workspaces/Boss7/receipts-round6/c1d38c8c285d284f3667.json"

def digest(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def main():
    inventory = {d["id"]: d for d in map(json.loads, (ROOT / "cleanup/inventory.jsonl").read_text().splitlines())}
    files = [
        ("c1d38c8c285d284f3667", HERE / "original/audit_full156_tail2.py", "primary source; fully read and run once"),
        ("4fb7add9aa294a3da316", HERE.parent / "full156-tail-parent-report/original/research_5/full156_tail2_kernel_10344.json", "only original runtime input; full JSON parsed and every matrix entry inspected"),
        ("39be3c9d1b2acc20bae2", HERE.parent / "full156-tail-parent-report/original/audit_full156_reply_set.py", "comparison source fully read; not executed by this task"),
        ("30ffd5d8405d7bc16953", HERE.parent / "full156-tail-parent-auditor/related/full156_tail2_kernel.py", "generator fully read; not executed or independently reimplemented"),
        ("f90132f8d6b5ff445853", HERE.parent / "full156-tail-parent-report/original/review_full156_tail.md", "mathematical review fully read"),
    ]
    sources = []
    for sid, path, role in files:
        saved, original = digest(path), inventory[sid]
        assert saved["bytes"] == original["size"] and saved["sha256"] == original["sha256"]
        sources.append({"source": original, "preserved": saved, "role": role})
    kernel_path = files[1][1]
    k = json.loads(kernel_path.read_text())
    names = k["topics"]
    n = len(names)
    ff = list(map(int, k["F_numerators"]))
    gg = [[int(v) for v in row] for row in k["G_numerators"]]
    uu = [[int(v) for v in row] for row in k["payoff_numerators"]]
    assert n == 156 and len(set(names)) == n and len(ff) == n
    assert len(gg) == len(uu) == n and all(len(row) == n for row in gg + uu)
    positions = 0
    for i in range(n):
        for j in range(n):
            assert gg[i][j] == gg[j][i]
            assert uu[i][j] == ff[i] - gg[i][j] >= 0
            positions += 1
    den, scale = int(k["payoff_denominator_for_normalized_point"]), int(k["unit_customer_scale"])
    assert den == 60 * scale > 0
    assert k["players"] == 6 and k["fixed_prefix"] == [0, 1, 2, 3] and k["actual_last_pair"] == [4, 5]
    assert k["aliases"] == list(range(156)) and k["original_labels"] == names
    write_json("matrix-inspection.json", {"status": "local-prepared", "kernel": digest(kernel_path),
               "all_topics": names, "shape": [n, n], "matrix_positions_checked": positions,
               "F_length": len(ff), "G_symmetric": True, "U_equals_F_minus_G": True, "U_nonnegative": True,
               "D": str(den), "S": str(scale), "D_equals_60S": True,
               "fixed_prefix": k["fixed_prefix"], "actual_pair": k["actual_last_pair"], "identity_aliases": True,
               "scope": "Matrix-internal and metadata checks additional to the author script; no customer or R/Z threshold reconstruction, no welfare/point/LP verification."})
    original_report = inventory["c758f099da46df6918a5"]
    report_path = HERE / "rerun/full156_tail2_exact_audit.json"
    report = digest(report_path)
    stdout = digest(HERE / "rerun/stdout.txt")
    assert report["bytes"] == stdout["bytes"] == original_report["size"]
    assert report["sha256"] == stdout["sha256"] == original_report["sha256"]
    output = json.loads(report_path.read_text())
    assert len(output) == 19 and output["source_sha256"] == inventory["4fb7add9aa294a3da316"]["sha256"]
    execution = json.loads((HERE / "rerun/execution.json").read_text())
    assert execution["original_entry_invocations"] == 1 and execution["returncode"] == 0
    assert execution["inputs_unchanged"] and execution["temporary_layout_removed"]
    assert not (HERE / "rerun/stderr.txt").read_bytes()
    formal = [
        ("程序/完整156主题的两人尾集合审计器--程序.md", "Parent additionally enumerates every achievable tail and checks welfare; no claim of a second customer matrix implementation."),
        ("计算/完整156主题固定前缀的两人尾报告--计算.md", "Parent 16 fields, same input kernel and extra point/welfare dependencies, exact finite six-tail welfare result."),
        ("资源/完整阈值目录固定四前缀的可信尾停界--资源.md", "Full analytic endpoint criterion and historical report scope; current code read/run does not rewrite that earlier unread-matrix status."),
        ("定理/真实退出缺陷的统一与异质前缀修复--定理.md", "Complete real-exit semantics, j=5 requires actual last BR, compiler cost 2R+Delta >=3delta5; not a lower bound for all repair algorithms."),
    ]
    comparisons = [{**digest(ROOT / "archives/customer-attraction/state" / name), "read_scope": "full text", "comparison": note} for name, note in formal]
    write_json("comparison.json", {"status": "local-prepared", "search_scope": "whole customer-attraction state and frozen inventory full156, threshold materialization, exact tails and repair contracts",
               "frozen_full_text_reads": [x[0] for x in files if x[0] != "4fb7add9aa294a3da316"] + ["c758f099da46df6918a5"],
               "formal_full_text_reads": comparisons,
               "new_readonly_matrix_work": "Before the authorized write window, parsed complete kernel, checked all 24336 F-G/U positions and independently calculated BR/M/target deficit; no old entry was executed then. Saved checker reproduces only matrix integrity part.",
               "not_run": ["full156_tail2_kernel.py", "audit_full156_reply_set.py", "welfare generator", "original necessary-graph LP", "six-player full tree"],
               "relation_decision": "Author target-tail/credible-deficit implementation, shared matrix dependency and parent broader tail-set comparison, plus conditional existing repair-cost consequence. Stage-three graph deferred."})
    write_json("manifest.json", {"status": "local-prepared", "primary_source_id": "c1d38c8c285d284f3667", "sources": sources,
               "original_runtime_input_count": 1, "large_shared_dependency_not_duplicated": True,
               "original_report_source": original_report, "new_report": report, "stdout": stdout,
               "byte_equal_to_frozen_report": True, "execution": digest(HERE / "rerun/execution.json"),
               "wrapper": digest(HERE / "run_original_once.py"), "actual_entry_run_count": 1})
    meta, _ = parse_flat_frontmatter(BODY.read_text())
    assert meta["id"] == "customer-attraction/full156-author-two-player-tail-auditor" and meta["kind"] == "program"
    receipt = json.loads(RECEIPT.read_text())
    assert receipt["id"] == "c1d38c8c285d284f3667" and receipt["status"] == "local-prepared"
    for key in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        assert receipt[key] is True
    for key in ("read_note", "comparison_note", "decision_note", "disposition", "targets"):
        assert receipt[key]
    targets = [{"path": p, "exists": (ROOT / p).is_file()} for p in receipt["targets"]]
    assert all(d["exists"] for d in targets)
    links = []
    for path in (BODY, HERE / "README.md"):
        for raw in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in raw or raw.startswith("#"):
                continue
            links.append({"from": str(path.relative_to(ROOT)), "target": raw,
                          "exists": (path.parent / raw.split("#")[0]).resolve().exists()})
    assert all(d["exists"] for d in links)
    parsed = []
    for path in sorted(HERE.rglob("*.json")):
        json.loads(path.read_text()); parsed.append(str(path.relative_to(ROOT)))
    write_json("self-check.json", {"status": "local-prepared", "frontmatter": meta, "source_hash_checks": len(sources),
               "matrix_positions_checked": positions, "original_report_hash_equal": True, "json_parsed": parsed,
               "targets": targets, "links": links, "body": digest(BODY),
               "scope": "Identity, packaging and explicitly stated matrix checks; not a customer-model or full-six-player certification."})
    print(json.dumps({"status": "local-prepared", "source_hashes": len(sources), "matrix_positions": positions,
                      "json_files": len(parsed), "targets": len(targets), "links": len(links)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
