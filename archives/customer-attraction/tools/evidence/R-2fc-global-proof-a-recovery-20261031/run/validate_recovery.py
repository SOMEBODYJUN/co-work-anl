from pathlib import Path
import json, hashlib, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source'; REPLAY=ROOT/'replay'
checks=[]
def check(name, ok, detail=''):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
    if not ok: raise AssertionError(f'{name}: {detail}')
expected={
'audit_collision_free_family.py':('484d7024f388657d79d9',3034,'9a5ec3d9a979d075235a505d0ae63362a1dfb79333a1280d7d8e535e48b0d7c1'),
'audit_collision_free_obstruction.py':('2c9581cd1e1a35237ff2',2155,'00678532fbff9f0179dee108c7ad792dcfdb59e7ac55af8610a1149a17de5a2c'),
'audit_truncated_potential.py':('da6d610ba50965200a82',2472,'c0b76546ad9cb545d22413fe460b9cbdbd8488354884fe067eac33d74406ca95'),
'collision_free_family_audit.json':('1121e1bd7ded184bd117',1344,'d4b13f887e50a909c943d769b08d550a2d4c9be62a92f707bba064f8f24b5a17'),
'collision_free_ratio_best.json':('e5a0724f34d98235f952',3448,'952a153b846b2664bbe923d9b9ea6a9dfc22187dfaa71b4f49fe95bd9be933bd'),
'collision_free_ratio_probe.py':('181f33c049afe9962dba',3116,'aec4685b0609e5826f91f678f28f893f8b537ebc00d26b006e257ca181ab8b0f'),
'truncated_potential_candidate.json':('631f2695cbf46ff1c2a2',3512,'5deb697bae4953dca400d166d2abdbef5a6e9ca983546f4c04720dc108ac7325'),
}
for name,(sid,size,sha) in expected.items():
 p=SOURCE/name; b=p.read_bytes(); got=hashlib.sha256(b).hexdigest()
 check('source:'+sid, len(b)==size and got==sha, f'{name} size={len(b)} sha={got}')
for p in SOURCE.glob('*.py'):
 r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True)
 check('py_compile:'+p.name,r.returncode==0,r.stderr)
family=json.loads((SOURCE/'collision_free_family_audit.json').read_text())
check('family-report-shape', [x['k'] for x in family]==[1,2,3])
check('family-report-values', [(x['W'],x['OPT'],x['ratio']) for x in family]==[(4,5,'5/4'),(6,8,'4/3'),(8,11,'11/8')])
check('family-replay-byte-equal', (REPLAY/'family/collision_free_family_audit.json').read_bytes()==(SOURCE/'collision_free_family_audit.json').read_bytes())
check('family-replay-clean', (REPLAY/'family/stderr.txt').read_text()=='')
obs=json.loads((REPLAY/'obstruction/stdout.json').read_text())
check('obstruction-exact', obs['W']==4 and obs['OPT']==5 and obs['Phi']=='4' and obs['two_layer_occupancy']==4 and obs['histories']==5 and obs['comparisons']==20 and obs['nonself_comparisons']==15)
check('obstruction-replay-clean', (REPLAY/'obstruction/stderr.txt').read_text()=='')
tr=json.loads((REPLAY/'truncated/truncated_potential_audit.json').read_text())
check('truncated-candidate-exact', tr['clients']==78 and tr['actual']==[1,5,5] and tr['W']==54 and tr['OPT']==75 and tr['Phi']=='141/2' and tr['truncated_Phi']=='141/2' and tr['difference']=='-9/2' and tr['comparisons']==258 and tr['minimum_slack']=='0')
check('truncated-replay-clean', (REPLAY/'truncated/stderr.txt').read_text()=='')
ratio=json.loads((SOURCE/'collision_free_ratio_best.json').read_text())
check('ratio-best-finite', ratio['q']==6 and ratio['r']==3 and isinstance(ratio['objective'],float) and ratio['objective']>1.0 and ratio['objective']<1.2)
check('ratio-probe-smoke-clean', (REPLAY/'ratio/stderr.txt').read_text()=='' and 'completed 3 q 6 r 3' in (REPLAY/'ratio/stdout.txt').read_text())
check('no-half-claim', all(2*x['W']>x['OPT'] for x in family) and 2*obs['W']>obs['OPT'] and 2*tr['W']>tr['OPT'])
result={'passed':True,'checks':checks,'source_count':len(expected),'exact_family':[(x['k'],x['W'],x['OPT'],x['ratio']) for x in family],'obstruction':{'W':obs['W'],'OPT':obs['OPT'],'Phi':obs['Phi']},'truncated_candidate':{'clients':tr['clients'],'W':tr['W'],'OPT':tr['OPT'],'Phi':tr['Phi'],'difference':tr['difference']},'ratio_best_objective':ratio['objective'],'scope':'fixed finite replays; no universal SPE or half theorem'}
(ROOT/'run/validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
