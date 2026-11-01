"""Static package closure, with zero mathematical program invocations."""
from pathlib import Path
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/"archives/customer-attraction/state/审查/静态安全亏量与舍入的后继独立审查--审查.md"
IDS=["d5853fd6622bc2202955","c685b48a31d21ba6d162","231301a6bdb11ea09340"]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
    return {"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":sha(p)}
def verify(row):
    p=ROOT/row["path"]
    assert p.is_file() and p.stat().st_size==row["bytes"] and sha(p)==row["sha256"],str(p)
    return record(p)
sources=json.loads((HERE/"source-manifest.json").read_text())
comparison=json.loads((HERE/"comparison-manifest.json").read_text())
assert [x["id"] for x in sources["primary"]]==IDS
bound=[]
for row in sources["primary"]+sources["related"]:
    assert row["full_file_reviewed"] is True
    bound.append(verify(row))
for row in comparison["stable_full_read_bindings"]:
    bound.append(verify(row))
for path in comparison["same_batch_formal_links"]:
    assert (ROOT/path).is_file(),path
event=json.loads((HERE/"replay/execution.json").read_text())
report=HERE/"original/security_slack_review.json"
new=HERE/"replay/security_slack_review.json"
expected=sources["complete_frozen_report"]
assert len(expected)==8 and json.loads(report.read_text())==expected
assert new.read_bytes()==report.read_bytes()
assert json.loads((HERE/"replay/stdout.txt").read_text())==expected
assert (HERE/"replay/stderr.txt").stat().st_size==0
assert event["returncode"]==0 and event["original_successor_main_calls"]==1
assert event["assertions_enabled_by_isolated_non_O_invocation"] is True
assert "-I" in event["command"] and "-B" in event["command"] and "-O" not in event["command"]
assert event["source_sha256_before"]==event["source_sha256_after"]==sources["primary"][0]["sha256"]
assert event["new_output_byte_identical_to_frozen"] is True
assert event["frozen_report_sha256"]==sha(report)
for key in ("author_main_calls","additional_original_helper_calls","new_independent_numeric_scans","LP_calls","SPE_solver_calls"):
    assert event[key]==0
for name in ("stdout.txt","stderr.txt","security_slack_review.json"):
    p=HERE/"replay"/name
    assert event["files"][name]["sha256"]==sha(p) and event["files"][name]["bytes"]==p.stat().st_size
assert event["check_calls_static_not_dynamic_trace"]==88
assert event["finite_scope_from_source"]=={"generic_cap_cases":80,"sharp_families":7,"sharp_backgrounds":1275,"mixed_case":1}
receipts=[]
for sid in IDS:
    p=ROOT/"cleanup/workspaces/Boss7/receipts-round19"/(sid+".json")
    data=json.loads(p.read_text())
    assert data["id"]==sid and data["disposition"]=="integrated"
    assert all(data[k] is True for k in ("full_file_reviewed","related_material_checked","unique_content_accounted_for"))
    assert all(data[k].strip() for k in ("read_note","comparison_note","decision_note"))
    for target in data["targets"]:
        assert target==str((HERE/"self-check.json").relative_to(ROOT)) or (ROOT/target).is_file(),target
    receipts.append({"path":str(p.relative_to(ROOT)),"sha256":sha(p),"targets":len(data["targets"])})
links=[]
for doc in (BODY,HERE/"README.md"):
    for target in re.findall(r"\]\(([^)]+)\)",doc.read_text()):
        if target.startswith(("https:","http:","#","mailto:")):
            continue
        p=(doc.parent/target.split("#",1)[0]).resolve()
        assert p==HERE/"self-check.json" or p.is_file(),(str(doc),target)
        links.append({"document":str(doc.relative_to(ROOT)),"target":target})
paths={ROOT/x["path"] for x in bound}
paths.update(p for p in HERE.rglob("*") if p.is_file() and p.name!="self-check.json")
paths.update(ROOT/x["path"] for x in receipts)
jsons=[];asts=[]
for p in sorted(paths):
    if p.suffix==".json":
        json.loads(p.read_text());jsons.append(str(p.relative_to(ROOT)))
    elif p.suffix==".py":
        ast.parse(p.read_text(),filename=str(p));asts.append(str(p.relative_to(ROOT)))
result={
"status":"pass","scope":"Only hashes, parsing, saved-event consistency, links and receipts; no original imports or new mathematical execution.",
"primary_sources":3,"primary_bytes":sum(x["bytes"] for x in sources["primary"]),
"related_sources_full_read_not_primary_in_this_object":len(sources["related"]),
"bound_files":bound,"formal_body":record(BODY),
"evidence_files_except_self":[record(p) for p in sorted(HERE.rglob("*")) if p.is_file() and p.name!="self-check.json"],
"JSON_files_checked":jsons,"Python_AST_files_checked":asts,"local_links":links,"receipts":receipts,
"retained_original_event":{"successor_main_calls":1,"wall_seconds":event["wall_seconds"],"report_byte_identical":True,"static_check_calls_not_trace":88},
"this_static_check_original_or_math_invocations":0}
(HERE/"self-check.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":"pass","bound_files":len(bound),"links":len(links),"JSON":len(jsons),"AST":len(asts),"receipts":len(receipts),"body_bytes":BODY.stat().st_size}))
