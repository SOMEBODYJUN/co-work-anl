"""One isolated unchanged entry per original program, only after actual claim."""
from pathlib import Path
import json,hashlib,sys,subprocess,os,time
root=Path('/workspace/scratch/37f0f9248cfc');repo=root/'boss4-research';stage=root/'boss4-next-cache/r3-priority-selection-two-implementations-primary';E=stage/'archives/customer-attraction/tools/evidence/priority-selection-two-implementations-primary'
m=json.loads((root/'boss4-next-cache/submarkov-next-priority-diagnostic-originals/actual-source-manifest.json').read_text());rows=m['rows'];ids={r['id'] for r in rows};cap=Path(sys.argv[1]);c=json.loads(cap.read_text());assert c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and ids<=set(c['ids'])
def sha(b):return hashlib.sha256(b).hexdigest()
for r in rows:
 b=Path(r['local_path']).read_bytes();assert len(b)==r['size'] and sha(b)==r['sha256'];o=json.loads((repo/'cleanup/progress'/(r['id']+'.json')).read_text());assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==r['sha256']
for r in [x for x in rows if x['path'].endswith('.py')]:
 name='author' if r['id']=='b89806c3e4a0081cbe6b' else 'independent';run=E/'replay'/(name+'-original-entry-1');assert not run.exists(),'Never automatically rerun an already attempted original entry'
 tree=run/'original-tree';code=tree/r['path'];code.parent.mkdir(parents=True);b=Path(r['local_path']).read_bytes();code.write_bytes(b);frozen=next(x for x in rows if x['path']==str(Path(r['path']).with_suffix('.json')));out=code.with_suffix('.json');assert not out.exists()
 j={'status':'started','program':name,'entry_number':1,'source_id':r['id'],'source_size':len(b),'source_sha256':sha(b),'source_unchanged':True,'frozen_report_id':frozen['id'],'frozen_report_sha256':frozen['sha256'],'claim_capture':str(cap),'claim_capture_sha256':sha(cap.read_bytes()),'claim_status':c['status'],'claim_local_sync':c['local_sync']['status'],'claim_remote_tip':c['remote_tip'],'command':[sys.executable,str(code)],'cwd':str(tree),'interpreter':sys.version,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1'},'relocation':'new isolated absolute prefix preserving original repo-relative source path; no external input path requirements','input_closure':'all literal unit-client fixtures and policies embedded in unchanged source; stdlib only, no external input files','program_output_path':str(out),'imports_of_original_before_entry':0,'original_program_calls_planned':1,'scope':'four literal priority diagnostic fixtures only; no HALF/sourceflow/LP/parameter search','started_unix_time':time.time()}
 jp=run/'actual-invocation.json';jp.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');start=time.perf_counter()
 try:
  p=subprocess.run(j['command'],cwd=tree,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,timeout=60)
  j.update({'status':'finished','returncode':p.returncode,'elapsed_seconds':time.perf_counter()-start,'original_program_calls_actual':1,'stdout_size':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_size':len(p.stderr),'stderr_sha256':sha(p.stderr)})
  (run/'stdout.txt').write_bytes(p.stdout);(run/'stderr.txt').write_bytes(p.stderr)
  if out.exists():
   ob=out.read_bytes();fb=Path(frozen['local_path']).read_bytes();j.update({'output_size':len(ob),'output_sha256':sha(ob),'frozen_report_byte_equal':ob==fb,'frozen_report_semantic_equal':json.loads(ob)==json.loads(fb)})
  else:j['output_missing']=True
 except subprocess.TimeoutExpired as e:
  so=e.stdout or b'';se=e.stderr or b'';(run/'stdout.txt').write_bytes(so);(run/'stderr.txt').write_bytes(se);j.update({'status':'timeout','elapsed_seconds':time.perf_counter()-start,'original_program_calls_actual':1,'stdout_size':len(so),'stderr_size':len(se),'timeout_seconds':60})
 j['source_unchanged']=code.read_bytes()==b;jp.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:j.get(k) for k in ['program','status','returncode','elapsed_seconds','stdout_size','stderr_size','output_size','output_sha256','frozen_report_byte_equal','frozen_report_semantic_equal']},ensure_ascii=False))
