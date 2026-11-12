from pathlib import Path
import hashlib, json, shutil, subprocess, sys
B=Path('/workspace/scratch/1a53a6eb65ea');R=B/'co-work-anl-boss1';W=B/'wave13-weak-iid-menu-worker'
BASE=R/'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea';A=BASE/'wave13-weak-iid-menu-delivery-review'
TID='customer-attraction-3a-3a-2262055787552638';RP=f'map/receipts/{TID}.json';FP=f'map/edges/{TID}/worker-freeze.json'
sys.path.insert(0,str(R/'tools'))
import research_runtime as rr
import map_tasks as mt
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
t=read(R/'research/operations/map-v2/tasks'/f'{TID}.json');d=t['definition']
assert t['state']=='claimed' and t['owner']=='Boss1' and rr.pin(d)=='b8d9c106e0a2b87152078b9a334194c07647bd276970adc429049234270233b7'
reg=read(R/'research/registry.json');obs={o['object_id']:o for o in reg['objects']}
assert all(rr.pin(obs[k])==v for k,v in d['input_pins'].items())
assert sha(W/RP)=='3c8ce9d0df3c0ce2327da3af0daec81d69e7a7c32c7c075971d60a7e5abe641a'
assert sha(W/FP)=='ccba8d493cb96d4a7484ddb74712f0d5bbf5884fa53e607682c767238ae1ccaf'
receipt=read(W/RP);assert len(receipt['assets'])==4
edges=[]
for asset in receipt['assets']:
    p=asset['path'];assert sha(W/p)==asset['sha256']
    if Path(p).suffix=='.json':
        e=read(W/p)
        if isinstance(e,dict) and 'edge_id' in e:edges.append(p)
assert len(edges)==2
initial=A/'initial-binding-attempt';assert not initial.exists();initial.mkdir()
for p in list(A.iterdir()):
    if p.is_file():shutil.copyfile(p,initial/p.name)
shutil.copytree(R/f'map/edges/{TID}',initial/'edge-directory')
shutil.copyfile(R/RP,initial/'receipt.json')
for asset in receipt['assets']+[{'path':RP},{'path':FP}]:shutil.copyfile(W/asset['path'],R/asset['path'])
shutil.copyfile(W/FP,A/'worker-frozen-manifest.json')
shutil.copyfile(B/'wave13-weak-iid-root-review.md',A/'root-mathematical-review.md')
shutil.copyfile(Path(__file__),A/'finalize-revised-delivery.py')
events=[]
for p in edges:
    for action in ['edge-bind','edge-check']:
        cmd=[sys.executable,'work.py','research',action,p]
        if action=='edge-bind':cmd.append('--write')
        c=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
        events.append({'action':action,'path':p,'exit_code':c.returncode,'stdout':c.stdout,'stderr':c.stderr})
        save(A/'native-binding-events.json',events);assert c.returncode==0,c.stdout+c.stderr
f=read(R/FP);f['boss_binding']={'scope':'Worker files and hashes remain the pre-binding semantic snapshot; final bound edge hashes follow.','edges':[{'path':p,'sha256':sha(R/p)} for p in edges],'status':'Both revised edges native bound and checked; pending final receipt validation and pushed checkpoint','scientific_reruns':0};save(R/FP,f)
for asset in receipt['assets']:
    if asset['path'] in edges:asset['sha256']=sha(R/asset['path'])
receipt['root_validation']={'reviewer':'Boss1','scope':'Root full mathematical review; original worker corrected finite-premise conditional mode without source edits; both edges rebound to final review SHA','scientific_reruns':0};save(R/RP,receipt)
rows=[read(p) for p in (R/'research/operations/map-v2/tasks').glob('*.json')]
mt.validate(R,d,'map',objects=obs);mt._asset_refs(R,d,receipt,canonical=set(reg['edge_files']));mt._supersession(R,d,receipt,rows,'map')
rels,files=mt.batch_edges(R,d,receipt,obs)
for e in rels.values():rr.require_edge_result(e)
ep={read(R/p)['edge_id']:p for p in files};mt._check_edge_paths(R,d,receipt,[x for x in rows if x['definition']['task_id']!=TID],ep,reg['edge_files']);mt._map_receipt_coverage(d,receipt,obs,rels);rr.validate_map_follow_ups(d,receipt,rows,obs,final=True)
assert len(rels)==2 and len(receipt['coverage'])==2 and all(x['state']=='linked' for x in receipt['coverage'].values())
assert sorted(e['relation_mode'] for e in rels.values())==['conditional','unconditional']
for asset in receipt['assets']:assert sha(R/asset['path'])==asset['sha256']
summary={'task_id':TID,'definition_pin':rr.pin(d),'receipt_path':RP,'receipt_sha256':sha(R/RP),'receipt_pin':rr.pin(receipt),'input_pins':d['input_pins'],'core_ids':d['object_ids'],'coverage':{'linked':2,'isolated-after-review':0},'edge_count':2,'asset_count':4,'logical_edges':2,'context_edges':0,'conditional_whole_edges':1}
save(A/'validation.json',{'status':'NATIVE_FULL_RECEIPT_VALIDATION_PASSED','tasks':[summary],'root_review_sha256':sha(A/'root-mathematical-review.md'),'worker_freeze_sha256':sha(W/FP),'bound_freeze_sha256':sha(R/FP),'scientific_executions_by_Boss':0,'native_checks':['definition','edge_bind_write','edge_check','asset_refs','supersession','batch_edges','require_edge_result','edge_paths','coverage','follow_ups_final_true']})
save(A/'done-records.json',[{'task_id':TID,'receipt_file':RP}])
done=[{'task_id':TID,'receipt_file':RP}]+read(BASE/'wave13-role-refund-delivery-review/done-records.json');save(BASE/'wave13-two-mature-done-records.json',done)
print(json.dumps({'status':'NATIVE_FULL_RECEIPT_VALIDATION_PASSED','task':summary},ensure_ascii=False,indent=2))
