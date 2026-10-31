from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'audit_collision_free_spe.py':('9c88e282902193a10afc',4128,'981e8f32d4eff3432f075733fc634ab712e4624c1b71b906fcce735b938113f1'),'collision_free_spe_exact_audit.json':('765c3b41163d0e50febe',2263,'33ccb3eb762c6b6bd96d601d23ae3e7ec8f2e66a1553d8db63e508828e9ea187'),'root_collision_free_family_audit.json':('20c89386263335ea5d0b',1183,'8e63bb1f845683eae08a4445d1a5977cfc537187c879552c6b6197e5689723f4'),'root_collision_free_family_audit.py':('bac0e0159f6d432c8c0a',4253,'d8656e0214f73d5db4875d9007a03e69e6f32c5f04c49246783be9405bfe7908')}
for n,(sid,size,sha) in exp.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha)
for p in SRC.glob('*.py'):
 r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True); ck('compile:'+p.name,r.returncode==0,r.stderr)
spe=json.load(open(SRC/'collision_free_spe_exact_audit.json')); ck('spe-exact',spe['status']=='all_exact_assertions_passed' and spe['decision_histories']==5 and spe['comparisons_including_self']==20 and spe['actual_profile']==[2,3] and spe['welfare']==4 and spe['optimum']==5 and spe['half_coverage_holds'] is True)
ck('spe-byte-replay',(SRC/'collision_free_spe_exact_audit.json').read_bytes()==(REP/'collision_free_spe_exact_audit.json').read_bytes() and (REP/'spe.stderr').read_text()=='')
fam=json.load(open(SRC/'root_collision_free_family_audit.json')); cases=fam['cases']; ck('family-shape',[(x['k'],x['W'],x['OPT'],x['ratio'],x['decision_histories'],x['comparisons_including_self']) for x in cases]==[(1,4,5,'5/4',5,20),(2,6,8,'4/3',57,399),(3,8,11,'11/8',1111,11110)])
ck('family-byte-replay',(SRC/'root_collision_free_family_audit.json').read_bytes()==(REP/'root_collision_free_family_audit.json').read_bytes() and (REP/'family.stderr').read_text()=='')
ck('half-boundary',2*spe['welfare']>spe['optimum'] and all(2*x['W']>x['OPT'] for x in cases))
out={'passed':True,'checks':checks,'scope':'independent exact finite replays; no universal half theorem','spe':{'W':spe['welfare'],'OPT':spe['optimum'],'histories':spe['decision_histories'],'comparisons':spe['comparisons_including_self']},'family':[(x['k'],x['W'],x['OPT'],x['ratio']) for x in cases]}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
