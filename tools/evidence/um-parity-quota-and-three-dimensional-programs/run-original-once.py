#!/usr/bin/env python3
"""One exact frozen entry per requested source, in a fresh directory."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
import time

root=Path(__file__).resolve().parent
ident,out=sys.argv[1],Path(sys.argv[2])
assert ident in {'8af37296657f6ee6656d','11edfbeb430cb529a9a7','a68bbc33808220d4814e','4f13d4de5870674ce284'}
program=root/'original'/(ident+'.py')
out.mkdir(parents=True,exist_ok=False);(out/'cwd').mkdir()
started=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
try:
    result=subprocess.run([sys.executable,str(program)],cwd=out/'cwd',capture_output=True,text=True,timeout=180,check=False)
    code,stdout,stderr=result.returncode,result.stdout,result.stderr
except subprocess.TimeoutExpired as err:
    code='timeout';stdout=err.stdout or b'';stderr=err.stderr or b''
    if isinstance(stdout,bytes):stdout=stdout.decode()
    if isinstance(stderr,bytes):stderr=stderr.decode()
(out/'stdout.txt').write_text(stdout);(out/'stderr.txt').write_text(stderr)
record={'source_id':ident,'source_sha256':hashlib.sha256(program.read_bytes()).hexdigest(),
        'source_bytes':program.stat().st_size,'entry_runs_this_batch':1,'returncode':code,
        'argv':[sys.executable,str(program)],'cwd':str((out/'cwd').resolve()),'cwd_initially_empty':True,
        'started_utc':started,'elapsed_seconds':time.monotonic()-clock,'python':sys.version,
        'input_files':[],'project_module_imports':[],'dependencies':'only fractions, itertools, random standard library as read in frozen source',
        'stdout_sha256':hashlib.sha256(stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(stderr.encode()).hexdigest(),
        'scope':'frozen original entry output only; PASS or exit0 does not establish a faithful mathematical oracle'}
(out/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_id':ident,'returncode':code,'stdout':stdout,'stderr_tail':stderr[-1200:],'output':str(out.resolve())},ensure_ascii=False))
