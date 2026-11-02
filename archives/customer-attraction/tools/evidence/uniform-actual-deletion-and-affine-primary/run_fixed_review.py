#!/usr/bin/env python3
"""Run the original affine audit once and the new fixed-input audit once.

Both execute in fresh output locations. Discovery, LP, package solver and canonical
verify_certificate are never imported or invoked by this runner.
"""
from pathlib import Path
from argparse import ArgumentParser
import datetime,hashlib,json,subprocess,sys,time

HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    parser=ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    orig=HERE/'original/boss/audit_affine_obstruction.py';saved=HERE/'original/boss/audit_affine_obstruction.json'
    runtime=out/'affine-runtime';runtime.mkdir();copy=runtime/orig.name;copy.write_bytes(orig.read_bytes())
    plans=[('original-affine',[sys.executable,str(copy)],runtime),
           ('new-fixed-definitions',[sys.executable,str(HERE/'audit_fixed_inputs.py'),'--output',str(out/'definitions')],out)]
    events=[]
    for label,argv,cwd in plans:
        begin=now();tic=time.monotonic();p=subprocess.run(argv,cwd=cwd,capture_output=True)
        wall=time.monotonic()-tic;end=now()
        (out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr)
        events.append(dict(label=label,argv=argv,cwd=str(cwd),started_utc=begin,ended_utc=end,wall_seconds=wall,exit_code=p.returncode,
                           stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest()))
    generated=runtime/'audit_affine_obstruction.json'
    identical=generated.exists() and generated.read_bytes()==saved.read_bytes()
    record=dict(identity='Boss3',python=sys.version,events=events,
        original_affine_report_byte_identical=identical,
        original_affine_source_sha256=sha(orig),runtime_original_source_unchanged=sha(copy)==sha(orig),
        original_affine_entrypoint_calls=1,new_fixed_definition_entrypoint_calls=1,
        original_discovery_or_LP_entrypoint_calls=0,original_canonical_solver_calls=0,original_verify_certificate_calls=0,
        not_an_external_or_blind_review=True)
    (out/'execution-record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(events=[{k:x[k] for k in ('label','exit_code','wall_seconds','stdout_bytes','stderr_bytes')} for x in events],original_affine_report_byte_identical=identical),indent=2))
    assert all(x['exit_code']==0 for x in events) and identical,'actual failure evidence retained'

if __name__=='__main__':main()
