"""Static closure only, with no original/definition-audit execution."""
from pathlib import Path
import ast,hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/"archives/customer-attraction/state/程序/真实前缀均匀接口的随机策略锥探针与取等记录--程序.md"
IDS=["3477ada253f971c404ba","9d2350424091677818cf","9a4dc621afb0d044fd37"]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):
    return {"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":sha(p)}
def verify(row):
    p=ROOT/row["path"]
    assert p.is_file() and p.stat().st_size==row["bytes"] and sha(p)==row["sha256"],row["path"]
    return rec(p)
manifest=json.loads((HERE/"source-manifest.json").read_text())
assert [x["id"] for x in manifest["primary"]]==IDS
bound=[verify(row) for group in ("primary","shared_code_dependencies","related_originals_and_formal_comparisons") for row in manifest[group]]
event=json.loads((HERE/"exact-audit/execution.json").read_text())
report=json.loads((HERE/"exact-audit/report.json").read_text())
ledger=json.loads((HERE/"exact-audit/case-ledger.json").read_text())
assert event["status"]==report["status"]=="pass"
for key in ("original_main_calls","original_helper_calls","LP_calls","SPE_solver_calls","new_random_searches"):
    assert event[key]==report[key]==0
assert event["independent_stored_point_audit_events"]==report["independent_stored_point_audit_events"]==1
assert event["inputs_sha256_before"]==event["inputs_sha256_after"]
assert event["audit_script_sha256"]==sha(HERE/"audit_stored_points.py")
for name,item in event["outputs"].items():
    p=HERE/"exact-audit"/name
    assert sha(p)==item["sha256"] and p.stat().st_size==item["bytes"]
assert report["total_history_nodes"]==290 and report["total_all_action_comparisons"]==1709
assert [x["exact_interface_objective"] for x in report["cases"]]==["2","3"]
assert [x["source_sha256"] for x in report["cases"]]==[x["sha256"] for x in manifest["primary"][1:]]
assert [len(x["nodes"]) for x in ledger]==[31,259]
receipts=[]
for sid in IDS:
    p=ROOT/"cleanup/workspaces/Boss7/receipts-round20"/(sid+".json")
    row=json.loads(p.read_text())
    assert row["id"]==sid and row["disposition"]=="integrated"
    assert all(row[k] is True for k in ("full_file_reviewed","related_material_checked","unique_content_accounted_for"))
    assert all(row[k].strip() for k in ("read_note","comparison_note","decision_note"))
    for target in row["targets"]:
        assert target==str((HERE/"self-check.json").relative_to(ROOT)) or (ROOT/target).is_file(),target
    receipts.append({"path":str(p.relative_to(ROOT)),"targets":len(row["targets"]),"sha256":sha(p)})
links=[]
for doc in (BODY,HERE/"README.md"):
    for target in re.findall(r"\]\(([^)]+)\)",doc.read_text()):
        if target.startswith(("http:","https:","#","mailto:")):continue
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
    if p.suffix==".py":
        ast.parse(p.read_text(),filename=str(p));asts.append(str(p.relative_to(ROOT)))
result={"status":"pass","scope":"Hashes, JSON/AST, saved-event summaries, links, receipts only; no arithmetic audit rerun.",
"primary_sources":3,"primary_bytes":sum(x["bytes"] for x in manifest["primary"]),
"bound_files":bound,"formal_body":rec(BODY),
"evidence_files_except_self":[rec(p) for p in sorted(HERE.rglob("*")) if p.is_file() and p.name!="self-check.json"],
"JSON_checked":jsons,"Python_AST_checked":asts,"local_links":links,"receipts":receipts,
"retained_event":{"definition_audit_events":1,"wall_seconds":event["wall_seconds"],"history_nodes":290,"all_action_comparisons":1709,"original_main_LP_solver":0},
"this_static_check_math_calls":0}
(HERE/"self-check.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":"pass","bound":len(bound),"links":len(links),"JSON":len(jsons),"AST":len(asts),"receipts":len(receipts),"body_bytes":BODY.stat().st_size}))
