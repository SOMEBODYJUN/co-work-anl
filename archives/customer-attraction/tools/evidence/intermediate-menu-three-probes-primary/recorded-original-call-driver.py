from pathlib import Path
import json,hashlib,shutil,importlib.util,sys,time,platform
agent=Path('/workspace/scratch/a79bc5ba354d/boss3-current/agent-a2');base=agent.parent
ev=agent/'deliverables/archives/customer-attraction/tools/evidence/intermediate-menu-three-probes-primary'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
items=json.loads((base/'sources/a2-manifest.json').read_text())
for x in items:
 p=Path(x['local_file']);assert h(p)==x['sha256'];assert p.stat().st_size==x['size']
 dst=ev/'original'/x['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
 x['preserved_path']=str(dst.relative_to(ev));x.pop('local_file');x.pop('progress',None)
(ev/'source-manifest.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
raw=ev/next(x['preserved_path'] for x in items if x['id']=='61c2553d74d86a489392');data=json.loads(raw.read_text())
script=ev/next(x['preserved_path'] for x in items if x['id']=='33dd6ec2b18113da781f')
assert data['n']==3 and data['m']==5 and data['weights']==[[1,6],[2,3],[3,6]]
spec=importlib.util.spec_from_file_location('frozen_probe_last_menu',script);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
start=time.perf_counter();answer=module.solve(data['n'],data['m'],data['weights']);elapsed=time.perf_counter()-start
assert answer is not None
result={'index':data['index'],'n':data['n'],'m':data['m'],'weights':data['weights'],'u':str(answer['u']),'menu':[[str(d),str(w),list(z),last] for d,w,z,last in answer['menu']]}
assert result==data
assert json.dumps(result,indent=2).encode()==raw.read_bytes()
replay=ev/'original-fixture-call';replay.mkdir(exist_ok=True)
(replay/'returned-fixed-instance.json').write_text(json.dumps(result,indent=2))
event={'operation':'one-original-solve-call-on-frozen-instance','entry':'probe_last_menu.solve','python':platform.python_version(),'assertions_enabled':__debug__,'elapsed_seconds':elapsed,'original_module_imports':1,'original_solve_calls':1,'original_main_calls':0,'random_trials_executed':0,'args':{'n':3,'m':5,'weights':data['weights']},'input_report_sha256':h(raw),'source_sha256':h(script),'returned_serialization_matches_frozen_bytes':True,'outcomes_cache':answer['outcomes'].cache_info()._asdict(),'pay_cache':answer['pay'].cache_info()._asdict(),'recorded_driver_sha256':h(Path(__file__))}
(replay/'event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(event,ensure_ascii=False,indent=2))
