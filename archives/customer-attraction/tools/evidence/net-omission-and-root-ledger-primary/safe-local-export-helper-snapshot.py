from pathlib import Path
import json,subprocess,os,hashlib,sys,re
root=Path('/workspace/scratch/37f0f9248cfc');repo=root/'boss4-research';out=Path(sys.argv[1]).resolve();assert out.is_relative_to(root/'boss4-next-cache');out.mkdir(parents=True,exist_ok=True)
inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())};env=os.environ.copy();env.update(GIT_NO_LAZY_FETCH='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null');rows=[];missing=[]
for i in sys.argv[2:]:
 assert re.fullmatch('[a-f0-9]{20}',i);x=inv[i]
 p=subprocess.run(['git','-c','protocol.allow=never','-c','remote.origin.promisor=false','-c','remote.origin.url=/nonexistent-codex-local-object-only','cat-file','blob',x['blob']],cwd=repo,env=env,capture_output=True)
 if p.returncode:missing.append({'id':i,'path':x['path'],'reason':'local blob absent; no network attempted'});continue
 b=p.stdout;assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256'];assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==x['blob'];dest=out/i/x['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);rows.append(dict(x,local_path=str(dest)))
(out/'local-export-manifest.json').write_text(json.dumps({'method':'no network/lazy fetch; source SHA256/size/Git object SHA1 verified','rows':rows,'missing':missing},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'exported':[(x['id'],x['size']) for x in rows],'missing':[x['id'] for x in missing]},ensure_ascii=False))
