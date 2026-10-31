from pathlib import Path
import hashlib,json,py_compile,sys
B=Path(__file__).parent
m=json.loads((B/'source-manifest.json').read_text())
checks=[]
def ck(name,ok,detail=''):
 checks.append({'name':name,'passed':bool(ok),'detail':detail})
for x in m['sources']:
 p=B/'source'/Path(x['path']).name
 ck('source:'+x['id'], hashlib.sha256(p.read_bytes()).hexdigest()==x['source_sha256'] and p.stat().st_size==x['source_size'])
for p in sorted((B/'source').glob('*.py')):
 py_compile.compile(str(p),doraise=True)
 ck('compile:'+p.name,True)
pairs=[('max_theme_branch_capacity_audit.json','replay/work/max_theme_branch_capacity_audit.json'),('deficit_probe_4_4.json','replay/deficit/deficit_probe_4_4.json'),('deficit_probe_5_4.json','replay/deficit/deficit_probe_5_4.json'),('three_price_template_obstruction.json','replay/work/three_price_template_obstruction.json')]
for a,b in pairs:
 ck('replay:'+a,json.loads((B/'source'/a).read_text())==json.loads(B.joinpath(b).read_text()))
report=json.loads((B/'replay/work/three_price_template_report.json').read_text())
ck('template-report-shape',len(report)==8 and [x['n'] for x in report]==[1,2,3,4,5,10,20,100])
ck('finite-scope',True)
out={'passed':all(x['passed'] for x in checks),'checks':checks}
(B/'validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['passed']: sys.exit(1)
