from pathlib import Path
import json,time,hashlib,shutil,subprocess,sys
ROOT=Path('/workspace/scratch/37f0f9248cfc');S=ROOT/'boss4-next-cache/r3-general-contraction-review-and-vertical-br-primary';E=S/'archives/customer-attraction/tools/evidence/general-contraction-review-and-vertical-br-primary';W=S/'cleanup/workspaces/Boss4/r3-general-contraction-review-and-vertical-br-primary';cap=ROOT/'boss4-r3-next-gv-claim.json';rows=json.loads((E/'source-manifest.json').read_text())['rows'];ids=[a['id'] for a in rows];start=time.monotonic()
while not cap.exists():
 if time.monotonic()-start>900:raise TimeoutError('No claim capture in 900 seconds; original entry calls remain zero')
 time.sleep(2)
c=json.loads(cap.read_text());assert c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and set(ids)<=set(c['ids']),c
owners=[]
for a in rows:
 p=ROOT/'boss4-research/cleanup/progress'/f"{a['id']}.json";r=json.loads(p.read_text());assert r['owner']=='Boss4' and r['disposition']=='in-progress' and r['source_sha256']==a['sha256'];owners.append({'id':a['id'],'record':r})
assert not (W/'claim-evidence.json').exists();shutil.copyfile(cap,W/'claim-evidence.json');(W/'primary-authorization-check.json').write_text(json.dumps({'status':'pass','remote_tip':c['remote_tip'],'capture_sha256':hashlib.sha256(cap.read_bytes()).hexdigest(),'actual_claim_count':len(c['ids']),'expected_ids':ids,'actual_intersection':[x for x in c['ids'] if x in ids],'source_count':5,'ownership_records':owners,'capture_preserved_full_not_projection':True},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'gate':'pass','actual_claim_count':len(c['ids']),'our_subset':5,'remote_tip':c['remote_tip']}),flush=True)
for kind in ['uniform','vertical']:
 p=subprocess.run([sys.executable,str(E/'execute-original-once.py'),kind],capture_output=True,text=True);print(p.stdout,flush=True);print(p.stderr,flush=True);assert p.returncode==0,(kind,p.returncode)
