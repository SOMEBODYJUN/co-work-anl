from pathlib import Path
import hashlib, json, subprocess, sys
HERE=Path(__file__).resolve().parent
checks=[]
def ck(name, ok, detail=''):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
    if not ok: raise AssertionError(f'{name}: {detail}')
manifest=json.loads((HERE/'source-manifest.json').read_text())
for s in manifest['sources']:
    p=HERE/'source'/s['local_name']
    ck('source:'+s['id'], p.exists(), str(p))
    ck('sha:'+s['id'], hashlib.sha256(p.read_bytes()).hexdigest()==s['source_sha256'], hashlib.sha256(p.read_bytes()).hexdigest())
    ck('size:'+s['id'], p.stat().st_size==s['source_size'], str(p.stat().st_size))
for p in ['source/actual_ap_projection.py','source/exact_projection_witness.py']:
    r=subprocess.run([sys.executable,'-m','py_compile',str(HERE/p)],capture_output=True,text=True)
    ck('compile:'+p,r.returncode==0,r.stderr)
for name,exp in [('ap_m5_symmetric_replay.json',(2.3158682560504418,450,True)),('ap_m5_replay.json',(2.3158682560504453,450,False)),('bns_m5_symmetric_replay.json',(2.225443383452107,930,True))]:
    d=json.loads((HERE/'replay'/name).read_text()); ck('replay:'+name,d['status']==0,str(d.get('message'))); ck('rows:'+name,d['rows']==exp[1],str(d['rows'])); ck('sym:'+name,d['symmetric_opt_singletons']==exp[2],str(d['symmetric_opt_singletons'])); ck('objective:'+name,abs(d['optimum_float']-exp[0])<1e-10,str(d['optimum_float']))
r=json.loads((HERE/'replay/work/exact_projection_witness.json').read_text())
ck('exact-witness-W',r['W']=='1',r['W']); ck('exact-witness-opt',r['comparison_union']=='3311537042/1488034729',r['comparison_union']); ck('exact-witness-gap',r['excess_over_2W']=='335467584/1488034729',r['excess_over_2W']); ck('exact-witness-rows',r['checked_rows']=={'floor':50,'AP':400,'BNS_all_maxima':250},str(r['checked_rows'])); ck('exact-witness-slack',r['minimum_AP_slack']=='6484381029/74401736450',r['minimum_AP_slack'])
result={'passed':all(x['passed'] for x in checks),'checks':checks,'scope':'necessary AP/BNS projection and exact rational witness; no continuation tree or SPE certificate'}
(HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
