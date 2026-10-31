from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys,time,ast,re
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-kfac-greedy-and-flow-primary')
E=S/'tools/evidence/kfac-greedy-and-flow-primary'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
primary=json.loads((E/'source-manifest.json').read_text())
deps=json.loads((E/'dependency-manifest.json').read_text())
byid={d['id']:d for d in primary+deps}
tree=E/'replay-tree'
for d in primary+deps:
 b=(S/d['saved_path']).read_bytes()
 assert len(b)==d['size'] and sha(b)==d['sha256']
 p=tree/d['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 if p.suffix=='.py':ast.parse(b.decode())
flow=json.loads((S/byid['41b0ab6732ba2f681e68']['saved_path']).read_text())
eptas=json.loads((S/byid['d027eeb6603c80ef3c5a']['saved_path']).read_text())
for report in [flow,eptas]:
 for path,h in report['source_sha256'].items():
  d=next(x for x in byid.values() if x['path']==path)
  assert h==d['sha256'],path
note=(tree/'history/source/notes/multi_facility/equal_light_flow_pro_report_2026-10-07.md').read_text()
blocks=re.findall(r'^'+chr(96)*3+r'python\n(.*?)^'+chr(96)*3,note,re.M|re.S)
assert len(blocks)==1
code=blocks[0];assert sha(code.encode())==flow['archived_code_sha256']
anchor='    a = []\n';assert code.count(anchor)==1
instrumented=code.replace(anchor,'        audit_residual(graph, source, sink, total_cost)\n\n'+anchor)
assert sha(instrumented.encode())==flow['instrumented_archived_code_sha256']
(E/'read-embedded-equal-flow.py.txt').write_text(code)
(E/'instrumentation-readback.py.txt').write_text(instrumented)
jobs=[
('greedy-cap','d165f0b0cbc484ee0ad3','812637c4d5d7e327de64'),
('greedy-potential','8e4166732a1d048fddfb','36882baacad2b171cf66'),
('greedy-repair-order','2a77d0eb61bccece8dae','a47ce4a499fcf500b8eb')]
out=E/'runs';out.mkdir(exist_ok=True)
results=[]
for name,sid,inp in jobs:
 with (out/(name+'-started.json')).open('x') as f:
  json.dump(dict(source_id=sid,started_utc=datetime.now(timezone.utc).isoformat(),original_CLI_invocation_this_batch=1),f)
 command=[sys.executable,'-I','-B',str(tree/byid[sid]['path'])]
 start=time.monotonic()
 proc=subprocess.run(command,cwd=tree,capture_output=True,timeout=180)
 elapsed=round(time.monotonic()-start,6)
 for stream,data in [('stdout',proc.stdout),('stderr',proc.stderr)]:
  with (out/f'{name}.{stream}.txt').open('xb') as f:f.write(data)
 d=dict(name=name,source_id=sid,source_sha256=byid[sid]['sha256'],input_binding={k:byid[inp][k] for k in ['id','path','size','sha256']},command=command,cwd=str(tree),exit_code=proc.returncode,elapsed_seconds=elapsed,stdout_bytes=len(proc.stdout),stderr_bytes=len(proc.stderr),original_CLI_invocations_this_batch=1,reason='No sufficiently bound prior successful complete original CLI found; earlier related imports/fixture checks do not execute this source audit.',runtime=dict(version=sys.version,optimize=0,isolated=1),scope='one original explicit fixture; stdout is original concise PASS, no fabricated JSON witness or universal test suite')
 dump(out/f'{name}-run.json',d);results.append(d)
 assert proc.returncode==0 and not proc.stderr and proc.stdout
dump(out/'new-run-summary.json',results)
dump(E/'same-SHA-success-reuse.json',dict(old_successes_reused=[
dict(source_id='cd26f8a883a5ebf2e64d',report_id='41b0ab6732ba2f681e68',old_status=flow['status'],all_report_source_hashes_match_actual_files=True,embedded_and_instrumented_hashes_match=True,new_original_CLI_calls=0,scope='6691 exact oracle inputs,4500 random,2187 grid,4special;1000 path identities; archived-only residual checks'),
dict(source_id='8bb33ff5bfd5b36ce7d0',report_id='d027eeb6603c80ef3c5a',old_status=eptas['status'],all_report_source_hashes_match_actual_files=True,new_original_CLI_calls=0,scope='186 two-facility/four-site inputs, including180 random at most6 clients plus larger gap cases; no production EPTAS')],new_original_CLIs=3,new_mathematical_input_fixtures=3,new_repository_suites=0,no_Git_fixture_or_operation=True,source_reports_unchanged=True))
print(json.dumps(dict(status='three original greedy CLIs passed once; two exact old successes reused',runs=results),ensure_ascii=False))
