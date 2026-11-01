"""Static closure only. Never import or execute any original mathematical program."""
from pathlib import Path
import ast
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BODY = ROOT / "archives/customer-attraction/state/审查/固定背景收益切片的后继独立秩审查--审查.md"
IDS = ["dc16c13a3d177b155261", "b5644b42ce76842a15e2", "29186a82220f6a599450"]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
    return {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size, "sha256": sha(p)}
def check_binding(item):
    p = ROOT/item["path"]
    assert p.is_file(), str(p)
    assert p.stat().st_size == item["bytes"], str(p)
    assert sha(p) == item["sha256"], str(p)
    return record(p)

sources = json.loads((HERE/"source-manifest.json").read_text())
comparison = json.loads((HERE/"comparison-manifest.json").read_text())
assert [x["id"] for x in sources["primary"]] == IDS
bound = []
for item in sources["primary"]:
    assert item["full_file_reviewed"] is True
    assert len(item["sources"]) == 2
    bound.append(check_binding(item))
for item in comparison["bindings"]:
    bound.append(check_binding(item))

event = json.loads((HERE/"replay/execution.json").read_text())
frozen = ROOT / sources["primary"][1]["path"]
replayed = HERE/"replay/fixed_background_rank_review.json"
assert replayed.read_bytes() == frozen.read_bytes()
expected = sources["complete_frozen_report"]
assert json.loads(frozen.read_text()) == expected
assert len(expected) == 9
assert json.loads((HERE/"replay/stdout.txt").read_text()) == expected
assert (HERE/"replay/stderr.txt").stat().st_size == 0
assert event["returncode"] == 0 and event["original_successor_main_calls"] == 1
assert event["source_sha256_before"] == event["source_sha256_after"] == sources["primary"][0]["sha256"]
assert event["frozen_report_sha256"] == sha(frozen)
assert event["new_output_byte_identical_to_frozen"] is True
assert event["assertions_enabled_by_isolated_non_O_invocation"] is True
assert "-I" in event["command"] and "-B" in event["command"] and "-O" not in event["command"]
for name in ("author_main_calls", "additional_original_helper_calls", "new_independent_matrix_scans", "LP_calls", "SPE_solver_calls"):
    assert event[name] == 0
for name in ("stdout.txt", "stderr.txt", "fixed_background_rank_review.json"):
    p = HERE/"replay"/name
    assert p.stat().st_size == event["files"][name]["bytes"] and sha(p) == event["files"][name]["sha256"]
assert event["rank_calls_from_static_loop_structure_not_dynamic_trace"] == 672

receipts = []
for sid in IDS:
    p = ROOT/"cleanup/workspaces/Boss7/receipts-round18"/(sid+".json")
    data = json.loads(p.read_text())
    assert data["id"] == sid and data["disposition"] == "integrated"
    for key in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        assert data[key] is True
    for key in ("read_note", "comparison_note", "decision_note"):
        assert data[key].strip()
    for target in data["targets"]:
        # self-check is the output currently being generated.
        assert target == str((HERE/"self-check.json").relative_to(ROOT)) or (ROOT/target).is_file(), target
    receipts.append({"path": str(p.relative_to(ROOT)), "targets": len(data["targets"]), "sha256": sha(p)})

links = []
for doc in (BODY, HERE/"README.md"):
    for target in re.findall(r"\]\(([^)]+)\)", doc.read_text()):
        if target.startswith(("https:", "http:", "#", "mailto:")):
            continue
        path = (doc.parent/target.split("#", 1)[0]).resolve()
        assert path == HERE/"self-check.json" or path.is_file(), (str(doc), target)
        links.append({"document": str(doc.relative_to(ROOT)), "target": target})

json_checked = []
ast_checked = []
paths = {ROOT/x["path"] for x in bound}
paths.update(p for p in HERE.rglob("*") if p.is_file() and p.name != "self-check.json")
paths.update(ROOT/x["path"] for x in receipts)
for p in sorted(paths):
    if p.suffix == ".json":
        json.loads(p.read_text())
        json_checked.append(str(p.relative_to(ROOT)))
    elif p.suffix == ".py":
        ast.parse(p.read_text(), filename=str(p))
        ast_checked.append(str(p.relative_to(ROOT)))
own_files = [record(p) for p in sorted(HERE.rglob("*")) if p.is_file() and p.name != "self-check.json"]
result = {
    "status": "pass",
    "scope": "Static bytes, JSON/AST, existing execution, links and receipts only; no original imports, helpers, ranks, matrices or solvers.",
    "primary_sources": len(sources["primary"]),
    "primary_bytes": sum(x["bytes"] for x in sources["primary"]),
    "bound_source_comparison_and_event_files": bound,
    "formal_body": record(BODY),
    "own_evidence_files_except_self_check": own_files,
    "json_files_checked": json_checked,
    "python_AST_files_checked": ast_checked,
    "local_links": links,
    "receipts": receipts,
    "retained_original_event": {
        "successor_main_calls": 1,
        "wall_seconds": event["wall_seconds"],
        "new_report_byte_identical": True,
        "rank_calls_static_only": 672
    },
    "this_static_check_math_or_original_invocations": 0
}
(HERE/"self-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"status":"pass", "sources":len(sources["primary"]), "bound_files":len(bound),
                 "local_links":len(links), "JSON":len(json_checked), "AST":len(ast_checked),
                 "receipts":len(receipts), "body_bytes":BODY.stat().st_size}, ensure_ascii=False))
