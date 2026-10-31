from pathlib import Path
import json,hashlib,subprocess,sys,time,os
root=Path('/workspace/scratch/37f0f9248cfc')
stage=root/'boss4-next-cache/r3-priority-coupling-and-child-audit-primary'
E=stage/'archives/customer-attraction/tools/evidence/priority-coupling-and-child-audit-primary'
def sha(b):return hashlib.sha256(b).hexdigest()
cpath=root/'boss4-r3-next-np-claim.json';claim=json.loads(cpath.read_text())
ids=['8b0f49a972d0fb865274','4b15bb8e3de0852a0cec','b78978baf4341d74d94a','b17e7dee8e9bc32f136a','df3f2ed8bb8a7d41dda6']
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(ids)<=set(claim['ids'])
nm=json.loads((root/'boss4-next-cache/submarkov-next-child-QA-originals/actual-source-manifest.json').read_text())
code=next(x for x in nm['rows'] if x['id']==ids[0]);frozen=next(x for x in nm['rows'] if x['id']==ids[1])
for row in nm['rows']:
 b=Path(row['local_path']).read_bytes();assert len(b)==row['size'] and sha(b)==row['sha256']
 v=json.loads((root/'boss4-research/cleanup/progress'/(row['id']+'.json')).read_text());assert v['owner']=='Boss4' and v['source_sha256']==row['sha256']
rd=E/'replay/child-support-original-run-1'
assert not rd.exists(),'original entry not repeated: run directory must be new'
tree=rd/'original-tree';tree.mkdir(parents=True)
cp=tree/code['path'];cp.parent.mkdir(parents=True);cp.write_bytes(Path(code['local_path']).read_bytes())
input_rel=Path('research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz')
old=root/'boss4-research/archives/customer-attraction/tools/evidence/fractional-load-boundaries/original'/input_rel
pb=old.read_bytes();assert len(pb)==372216 and sha(pb)=='bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce'
ip=tree/input_rel;ip.parent.mkdir(parents=True);ip.write_bytes(pb)
assert cp.parents[3]/'R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'==ip
target=cp.with_suffix('.json');assert not target.exists()
journal={'status':'started','entry_number':1,'source_code_id':code['id'],'source_code_size':code['size'],'source_code_sha256':code['sha256'],'source_unchanged':True,'frozen_report_id':frozen['id'],'frozen_report_sha256':frozen['sha256'],'claim_capture':str(cpath),'claim_capture_sha256':sha(cpath.read_bytes()),'claim_status':claim['status'],'claim_local_sync':claim['local_sync']['status'],'claim_remote_tip':claim['remote_tip'],'command':[sys.executable,str(cp)],'cwd':str(tree),'interpreter':sys.version,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1'},'relocation':'new isolated prefix with exact original repo-relative source and sibling input hierarchy; not the original absolute repository path','input_source':str(old),'input_replay_path':str(ip),'input_size':len(pb),'input_sha256':sha(pb),'program_output_path':str(target),'original_program_calls_planned':1,'imports_of_original_program_before_entry':0,'old13_full_automaton_audit_invocations':0,'scope':'original finite static QA; old13 actual-path arithmetic only','prior_same_SHA_run_search':'only inventory/path-index/claim/normal original metadata found; no sufficient actual same-SHA replay record; frozen author report retained separately'}
jp=rd/'actual-invocation.json';jp.write_text(json.dumps(journal,ensure_ascii=False,indent=2)+'\n')
t0=time.monotonic();wall=time.time()
result=subprocess.run(journal['command'],cwd=tree,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
(rd/'stdout.txt').write_bytes(result.stdout);(rd/'stderr.txt').write_bytes(result.stderr)
journal.update({'status':'finished','started_unix_time':wall,'elapsed_seconds':time.monotonic()-t0,'returncode':result.returncode,'stdout_size':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_size':len(result.stderr),'stderr_sha256':sha(result.stderr),'original_program_calls_actual':1})
if target.exists():
 ob=target.read_bytes();fb=Path(frozen['local_path']).read_bytes();journal.update({'output_size':len(ob),'output_sha256':sha(ob),'frozen_report_byte_equal':ob==fb,'frozen_report_semantic_equal':json.loads(ob)==json.loads(fb)})
else:journal['output_missing']=True
jp.write_text(json.dumps(journal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:journal.get(k) for k in ['returncode','elapsed_seconds','stdout_size','stderr_size','output_size','output_sha256','frozen_report_byte_equal','frozen_report_semantic_equal','original_program_calls_actual','old13_full_automaton_audit_invocations']},ensure_ascii=False))
assert result.returncode==0,'failed entry preserved; do not silently retry'
assert journal.get('frozen_report_byte_equal'),'original output discrepancy preserved; do not silently retry'
