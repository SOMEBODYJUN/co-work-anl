"""Exactly one untouched successor-security CLI in a new scratch directory."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,time
BASE=Path("/workspace/scratch/c0ab78c47566")
SOURCE=BASE/"r19-check-security-slack.py"
FROZEN=BASE/"r19-security-slack-review.json"
RUN=BASE/"r19-security-slack-review-run"
RUN.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)=="1b79cdf4eda44466e7df4228e468ae1bdcb923f5a01f88c22f6f33a89e18690d"
assert sha(FROZEN)=="96a0cc858bcceb8527fc7a2c2cd486c0c9875e5f1a78cd4b250c75946ca90960"
target=RUN/"check_security_slack.py"
shutil.copyfile(SOURCE,target)
before=sha(target)
command=[sys.executable,"-I","-B",str(target)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.perf_counter()
process=subprocess.run(command,cwd=RUN,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
elapsed=time.perf_counter()-t
(RUN/"stdout.txt").write_bytes(process.stdout)
(RUN/"stderr.txt").write_bytes(process.stderr)
out=RUN/"security_slack_review.json"
files=["check_security_slack.py","stdout.txt","stderr.txt"]+(["security_slack_review.json"] if out.exists() else [])
event={
"started_utc":started,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"command":command,"cwd":str(RUN),"returncode":process.returncode,"wall_seconds":elapsed,
"python":sys.version,"assertions_enabled_by_isolated_non_O_invocation":True,
"source_sha256_before":before,"source_sha256_after":sha(target),
"frozen_report_sha256":sha(FROZEN),"new_output_exists":out.exists(),
"new_output_byte_identical_to_frozen":out.exists() and out.read_bytes()==FROZEN.read_bytes(),
"files":{name:{"bytes":(RUN/name).stat().st_size,"sha256":sha(RUN/name)} for name in files},
"original_successor_main_calls":1,"author_main_calls":0,"additional_original_helper_calls":0,
"new_independent_numeric_scans":0,"LP_calls":0,"SPE_solver_calls":0,
"observation":"direct untouched original CLI; no runpy/profile/helper interception; no regenerated random-case ledger",
"check_calls_static_not_dynamic_trace":88,
"finite_scope_from_source":{"generic_cap_cases":80,"sharp_families":7,"sharp_backgrounds":1275,"mixed_case":1},
}
(RUN/"execution.json").write_text(json.dumps(event,ensure_ascii=False,indent=2)+"\n")
assert process.returncode==0 and event["new_output_byte_identical_to_frozen"]
assert before==sha(target) and len(process.stderr)==0
print(json.dumps({"status":"pass","wall_seconds":elapsed,"returncode":process.returncode,
"output_bytes":out.stat().st_size,"output_sha256":sha(out),
"stdout_bytes":len(process.stdout),"stderr_bytes":len(process.stderr)}))
