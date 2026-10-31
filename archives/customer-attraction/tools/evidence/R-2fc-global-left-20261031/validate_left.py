from pathlib import Path
import hashlib,json
base=Path(__file__).parent
checks=[]
def ck(name,ok,detail=''):
 checks.append({'name':name,'passed':bool(ok),'detail':detail})
 if not ok: raise AssertionError(f'{name}: {detail}')
manifest=json.loads((base/'source-manifest.json').read_text())
for x in manifest['sources']:
 p=base/'source'/x['local_name']; data=p.read_bytes()
 ck('source:'+x['id'],len(data)==x['source_size'] and hashlib.sha256(data).hexdigest()==x['source_sha256'],f'{len(data)} {hashlib.sha256(data).hexdigest()}')
obj=json.loads((base/'source/collision_free_obstruction_audit.json').read_text())
ck('obstruction-exact-fields',obj['W']==4 and obj['OPT']==5 and obj['Phi']=='4' and obj['actual']==[2,3],str({k:obj[k] for k in ['W','OPT','Phi','actual']}))
ck('obstruction-half-gap',2*obj['W']>=obj['OPT'],f"2W-OPT={2*obj['W']-obj['OPT']}")
ck('obstruction-replay-byte-json',json.loads((base/'replay/collision_audit.stdout.json').read_text())==obj,'equal')
probe=(base/'replay/background_probe.stdout').read_text()
ck('probe-smoke', 'completed 3 q 6 r 3 best 0.0' in probe,probe.strip())
ck('probe-no-candidate',not (base/'source/background_regret_candidate.json').exists(),'absent')
ck('stderr-empty', (base/'replay/background_probe.stderr').read_text()=='','empty')
(base/'validation.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'fixed exact five-client obstruction plus finite floating q=6,r=3 smoke; no universal SPE or half theorem'},indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)},indent=2))
