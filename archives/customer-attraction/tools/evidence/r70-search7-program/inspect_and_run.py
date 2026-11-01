"""Preserve ELF inspection; compile once; run a bounded current binary event."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'binary-event'
OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def call(name,argv):
    started=datetime.now(timezone.utc).isoformat()
    clock=time.monotonic()
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=60)
    (OUT/(name+'.stdout.txt')).write_bytes(r.stdout)
    (OUT/(name+'.stderr.txt')).write_bytes(r.stderr)
    return dict(name=name,argv=argv,start_utc=started,wall_seconds=time.monotonic()-clock,
                exit_code=r.returncode,stdout_bytes=len(r.stdout),stderr_bytes=len(r.stderr))
events=[]
for name,args in [
    ('file',['file','search7']),
    ('readelf',['readelf','-h','-l','-S','-d','-n','--version-info','-p','.comment','search7']),
    ('symbols',['nm','-C','search7']),
    ('disassembly',['objdump','-d','-C','--no-show-raw-insn','search7']),
    ('rodata',['objdump','-s','-j','.rodata','search7']),
    ('compiler-version',['g++','--version']),
]:events.append(call(name,args))
before={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in [ROOT/'search7.cpp',ROOT/'search7']}
events.append(call('compile',['g++','-std=c++17','-O2','search7.cpp','-o',str(OUT/'rebuilt-search7')]))
assert events[-1]['exit_code']==0
identical=(ROOT/'search7').read_bytes()==(OUT/'rebuilt-search7').read_bytes()
os.chmod(ROOT/'search7',0o755)
events.append(call('original-short',[str(ROOT/'search7'),'1','192711']))
assert events[-1]['exit_code']==0
if not identical:
    events.append(call('rebuilt-short',[str(OUT/'rebuilt-search7'),'1','192711']))
    assert events[-1]['exit_code']==0
    output_equal=all((OUT/('original-short.'+s+'.txt')).read_bytes()==(OUT/('rebuilt-short.'+s+'.txt')).read_bytes() for s in ['stdout','stderr'])
else:output_equal=True
after={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in [ROOT/'search7.cpp',ROOT/'search7']}
assert before==after
report=dict(status='PASS_BOUNDED_CURRENT_BINARY_EVENT',source_inputs_before=before,source_inputs_after=after,
            rebuilt=dict(bytes=(OUT/'rebuilt-search7').stat().st_size,sha256=sha(OUT/'rebuilt-search7')),
            byte_identical_rebuild=identical,short_stdout_stderr_equal=output_equal,events=events,
            original_binary_entries=1,rebuilt_entries=0 if identical else 1,requested_budget=1,explicit_seed=192711,
            historical_scan_replayed=False,LP_calls=0,
            scope='ELF static structure plus one compile and bounded current entry; byte identity or finite output agreement is stated separately, not inferred historical compiler flags or scan provenance.')
(OUT/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['events','source_inputs_before','source_inputs_after']},indent=2))
