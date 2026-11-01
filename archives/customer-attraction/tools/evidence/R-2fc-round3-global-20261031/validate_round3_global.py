from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'fractional_floor_m3q6.json':('4e8756dd24907a467cc9',2813,'0ff1b01d0a61e7bb87d23054c1e2d8860a686732a626faf1443651c2f98a5ba4'),'fractional_floor_m4q7.json':('8f2e672ef09b7dceeb41',6134,'b804790be1250f3f229f8592d4f7380150ded42017f4a34ec278a9fa377606c0'),'fractional_floor_probe.py':('e41ccfecef49b3cc9f9d',3648,'8f39d6809d5823aaf8626e63c1905e720bd8544eb394b91a68936a10283ae315'),'safe_action_m3q6.json':('85229befa581b5094585',223,'fafe7d3dc99cb4b1c4544674e864cc21e502720f8771d11d0e5046450574ae1a'),'threshold_safe_action_probe.py':('147286427b013102d22a',2529,'568717ed56c1673685493f1cd55ab2cdc5b10136618603a3c77ad2b9e1175d4e')}
for n,(sid,size,sha) in exp.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} {len(b)}')
for p in SRC.glob('*.py'):
 r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True); ck('compile:'+p.name,r.returncode==0,r.stderr)
for n in ['fractional_floor_m3q6.json','fractional_floor_m4q7.json']:
 x=json.load(open(SRC/n)); ck(n+'-finite',x['universal_claim_proved'] is False and x['completed']==1000 and x['best'] is not None and x['best']['root_over_fractional']>=1-1e-9)
safe=json.load(open(SRC/'safe_action_m3q6.json')); ck('safe-finite',safe['universal_claim_proved'] is False and safe['completed']==1000 and safe['candidate'] is None and safe['best_bad_action_count']==5)
ck('floor-smoke',(REP/'floor_smoke.stderr').read_text()=='' and json.load(open(REP/'floor_smoke.json'))['completed']==3 and json.load(open(REP/'floor_smoke.json'))['universal_claim_proved'] is False)
ck('safe-smoke',(REP/'safe_smoke.stderr').read_text()=='' and json.load(open(REP/'safe_smoke.json'))['completed']==3 and json.load(open(REP/'safe_smoke.json'))['candidate'] is None)
out={'passed':True,'checks':checks,'scope':'finite random exact-SPE oracle plus numerical fractional/safe-action probes; no universal result','fractional':{'m3q6_root_over_fractional':json.load(open(SRC/'fractional_floor_m3q6.json'))['best']['root_over_fractional'],'m4q7_root_over_fractional':json.load(open(SRC/'fractional_floor_m4q7.json'))['best']['root_over_fractional']},'safe_action':{'completed':safe['completed'],'best_bad_action_count':safe['best_bad_action_count'],'candidate':safe['candidate']}}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
