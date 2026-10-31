from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
expected={
'exact_tax_probe.py':('115b42a116e15b821e19',4930,'c8c4a0faabde42a02f51037d02a8bb73cc33c478004888bd1dd96b7dedc2d500'),
'exact_tax_scan_m4p6.json':('c0c1973365884e5cbf7e',3015,'81ea1729db5f4a8e2ca34e2496a50bb2bb5285fc1f9a89ede5b8b43dfada797d'),
'exact_tax_scan_m5p6.json':('a3fa866a17aaafa76def',3729,'199b558e70a3c06637dca60209325a0c8a6fd1263ec81f16a1403d377602b109')}
for n,(sid,size,sha) in expected.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} size={len(b)} sha={hashlib.sha256(b).hexdigest()}')
r=subprocess.run([sys.executable,'-m','py_compile',str(SRC/'exact_tax_probe.py')],capture_output=True,text=True); ck('py_compile',r.returncode==0,r.stderr)
for n,m,seed,best,rows,trials in [('exact_tax_scan_m4p6.json',4,2026102171,-0.25,1295,40),('exact_tax_scan_m5p6.json',5,2026102172,-0.2,7775,50)]:
 x=json.load(open(SRC/n)); ck(n+'-finite-status',x['status']=='finite_probe_only' and x['m']==m and x['p']==6 and x['seed']==seed and len(x['trials'])==trials and x['best']==best and all(t['rows']==rows for t in x['trials']) and all(t['outcomes']>=1 for t in x['trials']))
ck('short-m4-replay',(REP/'m4.stderr.txt').read_text()=='' and '"best": -0.25' in (REP/'m4.stdout.txt').read_text() and (REP/'exact_tax_scan_m4p6.json').exists())
ck('short-m5-replay',(REP/'m5.stderr.txt').read_text()=='' and '"best": -0.2' in (REP/'m5.stdout.txt').read_text() and (REP/'exact_tax_scan_m5p6.json').exists())
ck('no-exact-failure-output',not any(REP.glob('exact_tax_failure_*.json')))
ck('bridge-scope',True,'The source only searches finite random complete-SPE cones and would exact-audit a positive LP candidate; negative best values are no-hit evidence, not a universal proof.')
out={'passed':True,'checks':checks,'source_count':3,'scan_summary':{'m4':{'trials':40,'rows_per_trial':1295,'best':-0.25},'m5':{'trials':50,'rows_per_trial':7775,'best':-0.2}},'scope':'finite random probe and exact reconstruction gate; no universal half conclusion'}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
