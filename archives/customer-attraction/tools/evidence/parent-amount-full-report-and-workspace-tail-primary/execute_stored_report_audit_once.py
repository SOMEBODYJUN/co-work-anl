"""Execute the newly authorized stored-field audit once in a new directory; no old checker calls."""
from pathlib import Path
import json,hashlib,subprocess,sys,time
E=Path(__file__).resolve().parent;S=E.parents[4]
run=E/'stored-report-audit';run.mkdir(exist_ok=False)
man=json.loads((E/'actual-source-manifest.json').read_text());row=next(x for x in man['rows'] if x['id']=='34c68a75254ba1675fc7')
source=S/row['stage_path'];script=E/'audit_stored_report_fields.py';output=run/'stored-fields-result.json'
def fingerprint(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
before={'original_report':fingerprint(source),'audit_script':fingerprint(script)}
argv=[sys.executable,'-I','-B',str(script),str(source),str(output)]
started=time.time();t=time.perf_counter();p=subprocess.run(argv,cwd=S,stdout=subprocess.PIPE,stderr=subprocess.PIPE);elapsed=time.perf_counter()-t
(run/'stdout.txt').write_bytes(p.stdout);(run/'stderr.txt').write_bytes(p.stderr)
after={'original_report':fingerprint(source),'audit_script':fingerprint(script)}
record={'kind':'one-new-stored-report-field-arithmetic-audit, not original checker/SPE/LP replay','argv':argv,'cwd':str(S),'started_unix':started,
 'elapsed_seconds':elapsed,'exit_code':p.returncode,'python_version':sys.version,'before':before,'after':after,
 'stdout':fingerprint(run/'stdout.txt'),'stderr':fingerprint(run/'stderr.txt'),'output':fingerprint(output) if output.exists() else None,
 'original_report_unchanged':before['original_report']==after['original_report'],'audit_script_unchanged':before['audit_script']==after['audit_script']}
(run/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert p.returncode==0 and not p.stderr and record['original_report_unchanged'] and record['audit_script_unchanged']
result=json.loads(output.read_text());assert result['status']=='PASS'
print(json.dumps({'status':result['status'],'elapsed_seconds':elapsed,'reports':result['reports'],'columns':result['columns'],'stored_sender_rows':result['stored_sender_rows'],
 'max_reported_column_ratio':result['max_reported_column_ratio'],'reported_histories_not_replayed':result['sum_reported_histories_not_replayed'],
 'reported_comparisons_not_replayed':result['sum_reported_comparisons_not_replayed'],'arithmetic_checks':result['arithmetic_checks'],'output_sha256':fingerprint(output)['sha256']},ensure_ascii=False,indent=2))
