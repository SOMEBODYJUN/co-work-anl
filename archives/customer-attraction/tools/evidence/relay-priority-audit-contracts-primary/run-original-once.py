from pathlib import Path
import ast, hashlib, json, os, platform, shutil, subprocess, sys, time
EVIDENCE = Path(__file__).resolve().parent
PRIMARY = json.loads((EVIDENCE / "source-manifest.json").read_text())
BY_NAME = {Path(r["path"]).name:r for r in PRIMARY}
def original(name):
    return EVIDENCE / "original" / BY_NAME[name]["path"]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
runs=[]
for case, name, output in [("predictable", "audit_predictable_activation.py", "predictable_activation_audit.json"), ("priority", "audit_priority_coupling.py", "priority_coupling_audit.json")]:
    directory=EVIDENCE / "replay" / case
    directory.mkdir(parents=True, exist_ok=False)
    target=directory / name
    shutil.copyfile(original(name), target)
    dependencies=[]
    if case=="priority":
        prior=directory / "predictable_activation_audit.json"
        shutil.copyfile(original(prior.name), prior)
        dependencies.append({"path":prior.name,"kind":"frozen-primary-report-not-imported-program", "sha256":sha(prior),"bytes":prior.stat().st_size})
    tree=ast.parse(target.read_text())
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): imports.extend(alias.name for alias in node.names)
        elif isinstance(node,ast.ImportFrom): imports.append(node.module)
    start=time.time()
    proc=subprocess.run([sys.executable, str(target)], cwd=directory, capture_output=True)
    (directory/"stdout.txt").write_bytes(proc.stdout)
    (directory/"stderr.txt").write_bytes(proc.stderr)
    report=directory/output
    entry={"case":case,"program":name,"program_sha256":sha(target),"argv":[sys.executable,str(target)],"cwd":str(directory),"execution_count":1,"exit_code":proc.returncode,"duration_seconds":time.time()-start,"imports":imports,"local_program_imports":[],"dependencies":dependencies,"stdout_bytes":len(proc.stdout),"stdout_sha256":sha(directory/"stdout.txt"),"stderr_bytes":len(proc.stderr),"stderr_sha256":sha(directory/"stderr.txt"),"output_created":report.exists(),"exclusive_output":"x mode in unmodified source","path_difference":"copied byte-identical source executes in independent external replay directory; not original frozen path"}
    if report.exists():
        entry.update({"output_bytes":report.stat().st_size,"output_sha256":sha(report),"equals_frozen_bytes":report.read_bytes()==original(output).read_bytes()})
    (directory/"execution-state.json").write_text(json.dumps(entry,ensure_ascii=False,indent=2)+"\n")
    runs.append(entry)
    if proc.returncode:
        raise RuntimeError(f"Original {case} exit {proc.returncode}; failure preserved; no retry")
result={"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"original_program_execution_count":len(runs),"entry_side_effects":"Both programs execute at module top level and create sibling JSON exclusively. Neither imports the other. The priority input is the frozen original report, not the newly produced predictable output.","runs":runs}
(EVIDENCE/"replay"/"execution-summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False))
