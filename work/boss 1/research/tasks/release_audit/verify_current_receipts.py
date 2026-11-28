"""Cross-check current check results, inputs and raw clone outputs before the acceptance is frozen."""
import argparse
import gzip
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent
W=HERE.parents[2]
ROOT=HERE.parents[4]
FORMAL=["formal/report.md","formal/judgments.json","formal/scenarios.json","formal/calculator.html"]


def sh(data):
    return hashlib.sha256(data).hexdigest()


def sha(p):
    return sh(p.read_bytes())


def j(p):
    return json.loads(p.read_text())


def canon(x):
    return sh(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode())


def normalized(payload):
    res=json.loads(json.dumps(payload))
    if res.get("name")=="early-warning":
        del res["result"]["executed_at"]
        for model in ["logit","hist_gradient_boosting"]:
            del res["result"]["models"][model]["elapsed_seconds"]
    return canon(res)


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)


def matching_files(root,names):
    return {str(p.relative_to(W)):sha(p) for p in sorted(root/name for name in names)}


def inspect_monthly_archive(path):
    with np.load(path,allow_pickle=False) as data:
        meta=json.loads(data["metadata"].tobytes())
        offsets=meta["unique_trajectories_start_and_length"]
        pairs=meta["pairs"]
        assert len(pairs)==len({(a,b) for a,b,_,_ in pairs})==1500
        assert len(offsets)==1115 and len(meta["fields"])==43
        assert all(old==new and old in offsets for _,_,old,new in pairs)
        assert sum(offsets[new][1] for _,_,_,new in pairs)==168216
        lengths=sorted(tuple(v) for v in offsets.values())
        assert lengths[0][0]==0 and all(a+l==b for (a,l),(b,_) in zip(lengths,lengths[1:]))
        unique_months=sum(l for _,l in lengths)
        assert unique_months==125106
        baseline=next(new for strategy,scenario,_,new in pairs if (strategy,scenario)==("S000","severe"))
        begin,length=offsets[baseline]
        assert length==101
        final={}
        for i,name in enumerate(meta["fields"]):
            keys=data["k"+str(i)]; indices=data["v"+str(i)]
            assert len(indices)==unique_months and indices.max()<len(keys)
            decoded=keys[indices].view(np.float64)
            if name=="month":
                assert all(np.array_equal(decoded[s:s+l],np.arange(1,l+1)) for s,l in lengths)
            if name in {"debt","arrears","missedDebtService","unpaid","unfundedDiscretionary"}:
                final[name]=float(decoded[begin+length-1])
        assert final["arrears"]==final["missedDebtService"]==0
        assert abs(final["debt"]-515306.917)<0.001 and abs(final["unfundedDiscretionary"]-1871.727825)<0.000001
        assert final["unfundedDiscretionary"]==final["unpaid"]
        return {"strategy_scenario_pairs":len(pairs),"field_count":len(meta["fields"]),"months_per_edition":168216,
            "same_old_and_new_trajectory_keys":True,"deduplicated_single_scenario_trajectories":len(offsets),
            "unique_months_stored":unique_months,"S000_severe_month_101_decoded":final,"file_sha256":sha(path)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--formal-commit",required=True)
    ap.add_argument("--fresh-receipt",type=Path,required=True)
    ap.add_argument("--fresh-archive",type=Path,required=True)
    ap.add_argument("--monthly-archive",type=Path,required=True)
    ap.add_argument("--fresh-proof-files",nargs="+",type=Path,required=True)
    ap.add_argument("--household-receipt",type=Path,required=True)
    args=ap.parse_args()
    files=[p.resolve() for p in [args.fresh_receipt,args.fresh_archive,args.monthly_archive,*args.fresh_proof_files,args.household_receipt]]
    assert all(p.is_file() and p.is_relative_to(W) for p in files)
    cur=git("rev-parse",args.formal_commit).decode().strip()
    formal={name:sha(W/name) for name in FORMAL}
    for name,h in formal.items():
        assert sh(git("show",cur+":work/boss 1/"+name))==h
    all_evidence={str(p.relative_to(W)):sha(p) for p in files}

    econ=W/"research/tasks/research_independent_review"
    old=j(econ/"economic_checks.json"); delta=j(econ/"economic_delta.json")
    assert old["author"]==delta["author"]=="boss 1"
    assert old["reviewer"]==delta["reviewer"]=="/root/research_independent_review"
    assert delta["economic_verdicts"]=={key:"pass" for key in ["sources","frameworks","models","hyperedges","judgments"]}
    for name,h in delta["current_file_sha256"].items():
        assert sh(git("show","d139823:work/boss 1/"+name))==h
        if name!="research/RESUME.md":
            assert sha(W/name)==h, name
    resume=W/"research/RESUME.md"
    assert "7394ed770c1b47d134bc51e64aa3bb721dc157e0" in resume.read_text()
    assert "s18、s19、s20 未登记完成" in resume.read_text()
    all_evidence["research/RESUME.md"]=sha(resume)
    all_evidence.update(matching_files(econ,["economic_checks.json","economics_review.md","economic_delta.json","economic_delta.md",
        "verify_economic_delta.py","proposal_receipt.json","independent_models.json","independent_history.json","independent_accounts.json"]))
    economic=j(HERE/"crosscheck_economy.json")
    assert economic["script_sha256"]==sha(HERE/"crosscheck_economy.py")
    assert sum(i["cells_compared"] for i in economic["banks"]["workbooks"].values())==770

    hh=W/"research/tasks/household_independent_audit_v2"
    num=j(hh/"numeric_report.json")
    ext=j(hh/"extended_report.json")
    ui=j(hh/"offline_attempt.json")
    package=j(hh/"packaging_report.json")
    assert num["requests"]==87 and num["checksRun"]==num["passed"]==179 and num["failed"]==0
    assert (ext["requests"],ext["checks"],ext["passed"],ext["failed"])==(25,36,36,0)
    for n,row,payload in [(num,"independent_input.json","observed_engine_output.json.gz"),(ext,"extended_inputs.json","extended_outputs.json.gz")]:
        assert sha(hh/row)==n["inputSHA256"]
        assert sh(gzip.decompress((hh/payload).read_bytes()))==n["uncompressedOutputSHA256"]
    assert num["scriptSHA256"]==sha(hh/"independent_numeric.py") and num["adapterSHA256"]==sha(hh/"node_bridge.cjs")
    for fname,expected in num["reviewedArtifacts"].items():
        assert sha(W/"research/tasks/household_engine"/fname)==expected
    html_hash=formal["formal/calculator.html"]
    assert package["sha256"]==ext["formalHTML"]==ui["htmlSha256"]==html_hash
    assert all(v is True or v==[] for v in package["checked"].values())
    assert ui["verdict"]=="blocked" and ui["stage"]=="browser-launch" and "exitCode=127" in ui["reason"]
    assert all(ui[k]==[] for k in ["actions","downloads","screenshots","geometry"])
    hh_signed=j(args.household_receipt)
    assert hh_signed["reviewer"]=="/root/household_independent_audit" and hh_signed["verdict"]=="pass"
    assert html_hash in json.dumps(hh_signed)
    for fname,expected in hh_signed.get("artifacts",{}).items():
        assert sha(hh/fname)==expected
    all_evidence.update(matching_files(hh,["numeric_report.json","independent_numeric.py","independent_input.json",
        "observed_engine_output.json.gz","extended_contract_audit.py","extended_inputs.json","extended_outputs.json.gz",
        "extended_report.json","offline_attempt.json","offline_replay.py","demo_crosscheck.json","packaging_report.json",
        "migration.py","migration_diff.json","legacy_equivalence.json"]))

    own=j(HERE/"corrected_engine_results.json")
    demo=j(HERE/"final_demo_crosscheck.json")
    assert own["formalHTMLSha256"]==demo["htmlSha256"]==html_hash
    assert own["assertions"]==own["passed"]==77 and not own["failed"] and all(o["pass"] for o in own["cases"])
    assert own["scriptSha256"]==sha(HERE/"repaired_contract_tests.cjs") and own["postRepairInputSha256"]==sha(HERE/"post_repair_contract_inputs.json")
    assert demo["scriptSha256"]==sha(HERE/"inspect_frozen_demo.cjs")
    assert (demo["observed"]["commonFeasible"],demo["observed"]["commonFeasibleDistinct"],demo["observed"]["allDistinct"],demo["observed"]["paretoRules"])==(134,105,416,6)
    for key in ["before","after"]:
        closing=demo["oldAndCurrentDemoClosing"][key]
        assert closing["releaseFees"]==180 and closing["month"]==27 and abs(closing["closingPrincipal"]-557.756630583241)<1e-9
    all_evidence.update(matching_files(HERE,["pre_repair_cases.json","pre_repair_replay.cjs","pre_repair_results.json",
        "post_repair_contract_inputs.json","repaired_contract_tests.cjs","corrected_engine_results.json","inspect_frozen_demo.cjs",
        "final_demo_crosscheck.json","crosscheck_economy.py","crosscheck_economy.json","verify_current_receipts.py"]))

    fresh=j(args.fresh_receipt)
    assert fresh["verdict"]=="pass" and fresh["source_commit"]==cur
    assert fresh["actor"]=="boss 1" and fresh["run_id"]=="35440ff34fc845dbaa2b3d94cf6d2c00" and fresh["cycle"]==1
    assert fresh["independent_executor"]=="/root/fresh_restore"
    assert {n:fresh["formal_file_sha256"][n] for n in FORMAL}==formal
    assert fresh["formal_file_sha256"]["research/tasks/household_engine/engine.js"]==own["engineSha256"]
    for fname,expected in fresh.get("artifact_sha256",{}).items():
        assert sha(W/fname)==expected
    control=j(args.fresh_receipt.parent/"verification.json")
    assert control["commit"]==cur and control["binding"]["actor"]=="boss 1" and len(control["completed_stages"])==17
    assert bool(control["active_plan"]["all_input_paths_clone_local"]) and len(control["carried_from_prior_real_replay"])==10
    assert control["state_sha256"]==sh(git("show",cur+":work/boss 1/research_state.json"))
    assert fresh["clone"]["final_session_check_exit"]==3 and not fresh["clone"]["complete"]
    assert len(control["registered_stage_files"])==144 and all(r["registered"]==r["git_object"]==r["observed"] for r in control["registered_stage_files"])
    old_restore=W/"research/tasks/fresh_restore"
    history=j(old_restore/"receipt.json")
    assert history["verdict"]=="fail" and history["source_commit"].startswith("1580e86")
    all_evidence.update(matching_files(old_restore,["receipt.json","comparisons.json","raw_evidence.zip","resolved-environment.txt"]))
    old_job={r["original_id"]:r for r in j(old_restore/"comparisons.json")["runner"]["jobs"]}
    plan=j(W/"research/models/compute-current.json")
    ledger=j(W/"compute/ledger.json")
    by_id={r["id"]:r for r in ledger["runs"]}
    assert len(ledger["runs"])==12 and len(plan["jobs"])==11
    comparisons={}
    srcs=sorted((ROOT/"cncrisis").glob("*.py"))+[ROOT/"work.py",ROOT/"crisis.py"]+sorted(ROOT.glob("requirements*.txt"))
    code_sha=sh(b"".join(str(p.relative_to(ROOT)).encode()+b"\0"+p.read_bytes() for p in srcs))
    with zipfile.ZipFile(args.fresh_archive) as archive,zipfile.ZipFile(old_restore/"raw_evidence.zip") as prev:
        checks=json.loads(archive.read("sha256.json"))
        assert len(checks)==123 and set(checks)==set(archive.namelist())-{"sha256.json"}
        for name,h in checks.items():
            assert sh(archive.read(name))==h
        actual_ledger=json.loads(archive.read("audit/ledger-13.json"))["runs"]
        assert actual_ledger[:-1]==ledger["runs"]
        for spec in plan["jobs"]:
            ident=spec["id"]
            current=by_id[ident]
            inp=ROOT/spec["input"]
            assert inp.resolve().is_relative_to(ROOT) and sha(inp)==current["input_sha256"]
            env_sha=sh(json.dumps(current["versions"],sort_keys=True).encode())
            assert env_sha==current["environment_sha256"] and code_sha==current["code_sha256"]
            fingerprint_parts=[code_sha,env_sha,spec["method"],sha(inp)]
            nested=j(inp).get("csv")
            if nested:
                assert not Path(nested).is_absolute() and (ROOT/nested).resolve().is_relative_to(ROOT)
                fingerprint_parts.append(sha(ROOT/nested))
            fingerprint=sh("|".join(fingerprint_parts).encode())
            assert fingerprint==current["fingerprint"]
            out=W/"compute"/current["output"]
            assert sha(out)==current["output_sha256"]
            norm=normalized(j(out))
            if ident=="historical-warning-portable-v3":
                matches=[n for n in archive.namelist() if Path(n).name=="fresh-v2-"+out.name]
                assert len(matches)==1,matches
                member=matches[0]
                data=archive.read(member)
                append=actual_ledger[-1]
                assert append["id"]=="fresh-v2-"+ident and append["wall_seconds"]>0 and append["status"]=="complete"
                assert append["output_sha256"]==sh(data)==fresh["model_replay"]["raw_output_sha256"]
                assert append["fingerprint"]==fingerprint and append["code_sha256"]==code_sha and append["environment_sha256"]==env_sha
                source_archive=str(args.fresh_archive.resolve().relative_to(W))
                committed_version=cur
            else:
                row=old_job[ident]
                assert row["source_spec_external_csv"] is None
                assert row["fingerprint"]==fingerprint and row["code_sha256"]==code_sha and row["environment_sha256"]==env_sha
                assert set(row["clone_input_hashes"])=={n for n in [spec["input"],nested] if n}
                for n,h in row["clone_input_hashes"].items():
                    assert sha(ROOT/n)==sh(git("show",history["source_commit"]+":"+n))==sh(git("show",cur+":"+n))==h
                member=row["archived_as"]
                data=prev.read(member)
                assert sh(data)==row["replay_file_sha256"]
                source_archive=str((old_restore/"raw_evidence.zip").relative_to(W))
                committed_version=history["source_commit"]
            assert normalized(json.loads(data))==norm
            comparisons[ident]={"main_output":str(out.relative_to(W)),"specification":spec["input"],"spec_sha256":sha(inp),
                "nested_panel_if_any":nested,"source_clone_commit_for_actual_execution":committed_version,"raw_results_archive":source_archive,
                "fresh_archive_member":member,"fresh_output_sha256":sh(data),"current_fingerprint":fingerprint,
                "main_output_sha256":sha(out),"both_normalized_sha256":norm}
    assert len({v["fresh_archive_member"] for v in comparisons.values()})==11
    monthly_archive=inspect_monthly_archive(args.monthly_archive)
    state=j(W/"research_state.json")
    verdicts={**delta["economic_verdicts"],"household_engine":"pass","offline_ui":"blocked","independent_review":"pass","fresh_restore":"pass"}
    assert len(state["stages"])==17 and state["release"] is None
    evidence={"schema":"independent-review-process-evidence.v1","reviewer":"/root/release_audit","author":"boss 1","run_id":fresh["run_id"],
        "cycle":1,"completed_utc":datetime.now(timezone.utc).isoformat(),"frozen_formal_commit":cur,"formal_sha256":formal,
        "verdict":"pass","verdict_scope":"The independent review of the substantive items was performed, including challenged false positives, fixes and retests. The release result is reject while offline_ui is blocked.",
        "actual_check_dispositions":verdicts,"economic_checks_direct":economic["graph"],"economic_evidence_issues_resolved":[
        "Historical timing corrected to last information years 1981, 1999, 2016 and last three-year label maturity 1984, 2002, 2019.",
        "PF029 and QA001 corroborate one banking takeover; publication fallback groups cannot be counted as separate events.",
        "The archived old JST absolute CSV path failed strict clone isolation. The current specification resolves inside an independent clone. No new independent macro sample or predictive permission."],
        "household":{"base_checks":179,"base_requests":87,"extended_checks":36,"extended_requests":25,"separate_release_controls":77,
        "different_audit_cases_may_overlap":True,"domestic_CNY":True,"demo":demo["observed"],
        "old_scope":"Incorrect target could change a first-month deficit of 200 into a ten-year balance of 36000; the old engine ranked a prohibited 9211.51 payoff. Both historical failures preserved.",
        "new_scope":"Missing/mistyped target rejects; ordinary, capped/periodic, early full settlement, sale-specific and scheduled-maturity contracts checked on the actual formal inline engine."},
        "offline_ui":{"formal_sha256":html_hash,"stage":ui["stage"],"actual_wrapper":ui["launchExecutable"],"process_exit":127,
        "real_pages":0,"actions":len(ui["actions"]),"screenshots":len(ui["screenshots"]),"downloads":len(ui["downloads"]),
        "browser_console_and_network_assertions":"Unobservable before browser launch."},
        "fresh_restore":{"receipt":str(args.fresh_receipt.resolve().relative_to(W)),"archived_raw_output_comparisons":comparisons,
        "ignored_only_for_JST":["/result/executed_at","/result/models/logit/elapsed_seconds","/result/models/hist_gradient_boosting/elapsed_seconds"],
        "actual_execution_counts":{"unchanged_specifications_linked_to_previous_isolated_clone":10,"changed_specification_rebuilt_and_executed_in_current_clone":1},
        "independent_decoding_of_raw_two_edition_household_output":monthly_archive,
        "state":"The earlier commit failed strict isolation for its corrected historical job only. Its 10 other actual clone-local computations are individually matched by input, nested CSV where applicable, code, environment, fingerprint and archived raw output. The replacement specification actually ran in the new clone."},
        "direct_evidence_sha256":all_evidence}
    (HERE/"review_process_evidence.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"independent_review":"pass","fresh_restore":"pass","offline_ui":"blocked","release":"reject",
        "evidence_sha256":sha(HERE/"review_process_evidence.json")}))


if __name__=="__main__":
    main()
