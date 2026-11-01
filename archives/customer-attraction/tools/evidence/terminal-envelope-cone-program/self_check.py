"""Static package audit, never execute the original program or exact audit."""
from pathlib import Path
import hashlib
import json
import ast
import re

PACKAGE=Path(__file__).resolve().parent
REPO=PACKAGE.parents[4]


def main():
    manifest=json.loads((PACKAGE/"artifact-manifest.json").read_text())
    sources=json.loads((PACKAGE/"source-manifest.json").read_text())
    bindings=0
    for row in manifest["files"]+sources["frozen_sources"]+sources["related_full_reads"]:
        p=REPO/row.get("path",row.get("local_path"))
        raw=p.read_bytes()
        assert len(raw)==row["bytes"] and hashlib.sha256(raw).hexdigest()==row["sha256"],str(p)
        bindings+=1
    nj=np=0
    for p in sorted(PACKAGE.rglob("*")):
        if p.suffix==".json" and p.name!="self-check.json":
            json.loads(p.read_text());nj+=1
        if p.suffix==".py":
            ast.parse(p.read_text(),filename=str(p));np+=1
    random=json.loads((PACKAGE/"original/envelope_cone_probe.json").read_text())
    known=json.loads((PACKAGE/"original/envelope_known_cones.json").read_text())
    assert len(random)==3 and len(random["parameters"])==5 and len(random["records"])==12
    assert len(known)==2 and len(known["records"])==7
    assert all(len(r)==7 and r["success"] for r in random["records"])
    assert all(len(r)==9 and r["success"] for r in known["records"])
    event=json.loads((PACKAGE/"replay/execution.json").read_text())
    exact=json.loads((PACKAGE/"exact/exact-small-cone.json").read_text())
    assert event["status"]==exact["status"]=="PASS"
    assert event["call_counts"]=={"canonical_worst_certificate":1,"original_optimize":1,"original_main":0,"linprog":1}
    assert all(event["shared_historical_fields_match"].values())
    assert not event["random_main_replayed"] and not event["remaining_known_cases_replayed"]
    assert exact["LP_calls"]==exact["canonical_solver_calls"]==exact["original_module_imports"]==0
    assert exact["independent_exact_runs"]==1
    assert exact["exact_max_epsilon"]=="-1/2" and exact["exact_min_objective"]=="1/2"
    assert exact["captured_float_coefficients_matched_exactly"]==1022
    assert len(exact["matrix"])==29 and all(len(r)==32 for r in exact["matrix"])
    assert len(exact["policy"]["actions"])==6
    assert len(exact["raw_client_policy_audits"])==2
    assert all(len(r["IC_comparisons"])==24 for r in exact["raw_client_policy_audits"])
    assert len(exact["optimized_point_backgrounds"])==5
    assert exact["all_remaining_historical_cones_exactly_certified"] is False
    links=formulas=0
    for rel in manifest["markdown_objects"]:
        p=REPO/rel;s=p.read_text()
        assert all(line.rstrip()==line for line in s.splitlines()),rel
        assert s.count(r"\[")==s.count(r"\]"),rel
        formulas+=s.count(r"\[")
        for match in re.finditer(r"\]\(([^)]+)\)",s):
            target=match.group(1).split("#",1)[0]
            if target and "://" not in target:
                assert (p.parent/target).resolve().exists(),(rel,target)
                links+=1
    targets=0
    for rid in ["817e89899b14e920d464","2c16247ed5813c135fae","9a8c0e55c867131b5297"]:
        p=REPO/"cleanup/workspaces/Boss7/receipts-round21"/(rid+".json")
        r=json.loads(p.read_text())
        assert r["id"]==rid and r["disposition"]=="integrated"
        assert all(r[k] for k in ["full_file_reviewed","related_material_checked","unique_content_accounted_for",
                                  "read_note","comparison_note","decision_note"])
        for target in r["targets"]:
            assert (REPO/target).is_file() or REPO/target==PACKAGE/"self-check.json",target
            targets+=1
    out={"status":"PASS","scope":"static files, stored records and references only",
         "sha256_bindings":bindings,"JSON_parsed":nj,"Python_AST_parsed":np,
         "local_links":links,"display_formula_pairs":formulas,"receipts":3,"receipt_targets":targets,
         "new_original_calls":0,"new_LP_calls":0,"new_math_enumerations":0,
         "historical_records_reviewed":19,"exact_new_fixed_policy_cones":1}
    (PACKAGE/"self-check.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(out,ensure_ascii=False))


if __name__=="__main__":
    main()
