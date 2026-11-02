from pathlib import Path
import shutil,json,hashlib,subprocess,sys,time,platform
base=Path('/workspace/scratch/a79bc5ba354d/boss3-current')
repo=Path('/workspace/scratch/a79bc5ba354d/co-work-anl-boss3')
agent=base/'agent-a'; ev=agent/'deliverables/archives/customer-attraction/tools/evidence/indexed-five-probe-primary'
ids=['e1c83d76b09fcdcfbd1f','d7eef7982a66754c06e7','c22aa1a2f00fdff9844e','559c69af59f4e0284761','0fbaf567de4f29fac658','b1132ae520c99d578e34']
manifest=[x for x in json.loads((base/'sources/manifest.json').read_text()) if x['id'] in ids]
assert len(manifest)==6
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
related=repo/'archives/customer-attraction/tools/evidence/global-indexed-reviews-boss3/related'
for x in manifest:
 p=Path(x['local_file']);assert h(p)==x['sha256'];assert len(p.read_bytes())==x['size']
 dst=ev/'original'/x['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
 x['preserved_path']=str(dst.relative_to(ev))
 x.pop('local_file');x.pop('progress',None)
 if (related/p.name.split('--',1)[1]).exists():
  twin=related/p.name.split('--',1)[1]; assert h(twin)==x['sha256'];x['already_archived_same_sha256']=str(twin.relative_to(repo))
(ev/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
cert=repo/'archives/customer-attraction/tools/evidence/terminal-menu-exclusion-and-envelope-primary/comparison/five_player_indexed_bound.json'
assert h(cert)=='18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
data=json.loads(cert.read_text());p=data['primal'];assert len(p['atoms'])==64
rt=agent/'runtime';src=next(x for x in manifest if x['id']=='0fbaf567de4f29fac658')
script=rt/src['path'];script.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ev/src['preserved_path'],script)
cert_rt=rt/'evidence/certificates/customer_attraction/five_player_indexed_bound.json';cert_rt.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(cert,cert_rt)
before={str(x.relative_to(rt)):h(x) for x in [script,cert_rt]}
start=time.perf_counter(); proc=subprocess.run([sys.executable,str(script)],cwd=rt,capture_output=True,text=True);elapsed=time.perf_counter()-start
replay=ev/'replay';replay.mkdir(exist_ok=True)
(replay/'stdout.json').write_text(proc.stdout);(replay/'stderr.txt').write_text(proc.stderr)
assert proc.returncode==0,proc.stderr
out=script.with_suffix('.json');frozen=ev/next(x['preserved_path'] for x in manifest if x['id']=='559c69af59f4e0284761')
shutil.copy2(out,replay/'offdiagonal_probe.json')
assert out.read_bytes()==frozen.read_bytes()
r=json.loads(out.read_text());from fractions import Fraction as F
assert len(r['all'])==r['row_count']==27
assert r['negative']=={k:v for k,v in r['all'].items() if F(v)<0}
assert len(r['negative'])==8
assert sum(F(v)==0 for v in r['all'].values())==3
assert sum(F(v)>0 for v in r['all'].values())==16
assert before=={str(x.relative_to(rt)):h(x) for x in [script,cert_rt]}
event={'operation':'one-original-offdiagonal-main-replay','argv':[sys.executable,str(script)],'cwd':str(rt),'python':platform.python_version(),'assertions_enabled':__debug__,'elapsed_seconds':elapsed,'returncode':proc.returncode,'stderr_bytes':len(proc.stderr.encode()),'input_sha256':before,'frozen_output_sha256':h(frozen),'replayed_output_sha256':h(out),'output_byte_identical':True,'row_count':27,'negative_count':8,'zero_count':3,'positive_count':16,'original_main_calls':1,'LP_calls':0,'SPE_solver_calls':0,'independent_new_formula_audit_calls':0}
(replay/'event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
(ev/'reused-input.json').write_text(json.dumps({'path':str(cert.relative_to(repo)),'source_ref':'source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/five_player_indexed_bound.json','sha256':h(cert),'size':cert.stat().st_size,'primal_atoms':64,'denominator':p['denominator'],'read_scope':'Complete JSON parsed for exact frozen primal and all 64 atom descriptors/weights; no replay of original 437-row audit or dual certification'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(event,ensure_ascii=False,indent=2))
