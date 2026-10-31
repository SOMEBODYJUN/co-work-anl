#!/usr/bin/env python3
"""Execute one frozen primary entry with exact sibling dependencies in fresh dirs."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

root=Path(__file__).resolve().parent
ident,out=sys.argv[1],Path(sys.argv[2])
names={'e8b6428338f9c956317c':'home_unit_cycle_and_directed_token.py',
 '594190c19816e3b1e99a':'home_unit_cycle_independent.py',
 'e8706876e0c1b5dcebd9':'rooted_dag_transit_branch_search.py',
 '3c16720b6c276a5997e1':'rooted_dag_transit_independent.py',
 '10ce30330f34e96a1a00':'slot_envelope_identity.py'}
assert ident in names
out.mkdir(parents=True,exist_ok=False);(out/'inputs').mkdir();(out/'cwd').mkdir()
source=root/'original'/(ident+'.py');program=(out/'inputs'/names[ident]).resolve()
shutil.copyfile(source,program)
aliases=[{'source_id':ident,'path':str(program),'sha256':hashlib.sha256(program.read_bytes()).hexdigest(),'role':'primary original entry'}]
argv=[sys.executable,str(program)]
if ident=='e8b6428338f9c956317c':argv+=['--audit','all','--output',str((out/'report.json').resolve())]
if ident=='10ce30330f34e96a1a00':argv+=['--output',str((out/'report.json').resolve())]
if ident=='e8706876e0c1b5dcebd9':
    dep=(out/'inputs/rooted_dag_congestion_flow.py').resolve();shutil.copyfile(root/'support/rooted_dag_congestion_flow.py',dep)
    aliases.append({'source_id':'cd5e59034198845a9ec2','path':str(dep),'sha256':hashlib.sha256(dep.read_bytes()).hexdigest(),'role':'actual sibling loaded by fixtures(); only old min_certificate/validate invoked, not old main'})
if ident=='3c16720b6c276a5997e1':
    dep=(out/'inputs/rooted_dag_transit_branch_search.py').resolve();shutil.copyfile(root/'original/e8706876e0c1b5dcebd9.py',dep)
    argv+=['--implementation',str(dep)]
    aliases.append({'source_id':'e8706876e0c1b5dcebd9','path':str(dep),'sha256':hashlib.sha256(dep.read_bytes()).hexdigest(),'role':'reviewed implementation imported explicitly for comparisons; its main/fixtures not invoked'})
record={'status':'running','source_id':ident,'entry_runs':1,'argv':argv,'cwd':str((out/'cwd').resolve()),'cwd_initially_empty':True,
 'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'input_aliases':aliases,
 'network_calls':0,'bytecode_writes_disabled':True,'source_files_modified':False}
(out/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
clock=time.monotonic();env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
try:
    result=subprocess.run(argv,cwd=out/'cwd',capture_output=True,text=True,timeout=900,check=False,env=env)
    code,stdout,stderr=result.returncode,result.stdout,result.stderr
except subprocess.TimeoutExpired as err:
    code='timeout';stdout=err.stdout or b'';stderr=err.stderr or b''
    if isinstance(stdout,bytes):stdout=stdout.decode()
    if isinstance(stderr,bytes):stderr=stderr.decode()
(out/'stdout.txt').write_text(stdout);(out/'stderr.txt').write_text(stderr)
if code==0 and not (out/'report.json').exists():
    parsed=json.loads(stdout);(out/'report.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n')
record.update(status='completed',returncode=code,elapsed_seconds=time.monotonic()-clock,
 stdout_sha256=hashlib.sha256(stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(stderr.encode()).hexdigest())
record['inputs_unchanged_after_run']=all(hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256'] for a in aliases)
(out/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_id':ident,'returncode':code,'elapsed_seconds':record['elapsed_seconds'],
 'stdout_bytes':len(stdout.encode()),'stderr_tail':stderr[-1800:],'inputs_unchanged':record['inputs_unchanged_after_run'],
 'output':str(out.resolve())},ensure_ascii=False))
