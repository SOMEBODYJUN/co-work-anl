from pathlib import Path
import subprocess,json,hashlib,time
B=Path('/workspace/scratch/37f0f9248cfc');R=B/'boss4-research';C=B/'boss4-next-cache';D=C/'R79-regret-required-seeds';D.mkdir(exist_ok=True);inv=json.loads((B/'boss4-available-all.json').read_text());rs=[r for r in inv if '/R-79a883d99127437ebe4f0423a181f01b/construct/seed_source_' in r.get('path','')];rows=[]
for r in rs:
 p=D/r['id'];capture=D/(r['id']+'-normal-show.json')
 if r['id']=='11b20b3cd0f9f814da06':
  assert p.is_file();receipt={'source':r,'output':str(p)};capture.write_text(json.dumps({'capture_mode':'already-observed tool stdout semantically transcribed; no second show','argv':['python','work.py','clean','show',r['id'],'--out',str(p)],'cwd':str(R),'exit_code':0,'observed_normal_show':receipt},ensure_ascii=False,indent=2)+'\n')
 else:
  argv=['python','work.py','clean','show',r['id'],'--out',str(p)];t=time.monotonic();z=subprocess.run(argv,cwd=R,text=True,capture_output=True);capture.write_text(json.dumps({'argv':argv,'cwd':str(R),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr,'elapsed_seconds':time.monotonic()-t},ensure_ascii=False,indent=2)+'\n');assert z.returncode==0,(r['id'],z.stderr);receipt=json.loads(z.stdout);assert receipt['source']['sha256']==r['sha256']
 b=p.read_bytes();assert len(b)==r['size'] and hashlib.sha256(b).hexdigest()==r['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'];rows.append({**r,'local_path':str(p),'actual_normal_show_capture':str(capture),'role':'required related frozen input; not new primary/done'});print(r['id'],len(b),'normal/hash OK',flush=True)
(D/'actual-related-source-manifest.json').write_text(json.dumps({'rows':rows,'source_count':len(rows),'source_bytes':sum(r['size'] for r in rows),'new_primary_count':0,'new_done_count':0},ensure_ascii=False,indent=2)+'\n');print('ALL',len(rows),sum(r['size'] for r in rows),flush=True)
