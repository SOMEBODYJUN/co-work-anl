"""Only17 collaboration methods per ref; imported fixtures are not rediscovered."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,time
E=Path(__file__).resolve().parent;S=E.parents[2];records={x['id']:x for f in ['source-manifest.json','dependency-manifest.json'] for x in json.loads((E/f).read_text())};out=E/'runs';out.mkdir(exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','WCG_')) and k not in ('SSH_AUTH_SOCK','SSH_ASKPASS')};env.update(GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',PYTHONDONTWRITEBYTECODE='1');summary=[]
for variant,ids in [('main',['d9b5b49ab665613450d6','0267e9382e7d95b35a5e','99da839bfd62db2365a0','db6af3d64d99cc147969']),('legacy',['3c0404b7974eca538863','de53a0261145104205aa','673a94bf8c2a50db4be5','f4ad07192854bfc106ad'])]:
 ids+=['4a9d84f0b03bbbf6c01a','086e17d599de8edb10a2','207fa0dc8920b57c0653','b054428c6de628f29738']
 with tempfile.TemporaryDirectory(prefix='collab-suite-',dir=S) as temp:
  root=Path(temp);inputs=[]
  for i in ids:
   x=records[i];raw=(S/x['saved_path']).read_bytes();assert len(raw)==x['size'] and hashlib.sha256(raw).hexdigest()==x['sha256'];p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);p.chmod(0o755 if x['mode']=='100755' else 0o644);inputs.append({'id':i,'path':x['path'],'sha256':x['sha256'],'bytes':x['size'],'mode':x['mode']})
  subprocess.run(['git','init','--quiet',str(root)],cwd=root,env=env,check=True,capture_output=True,timeout=20)
  cmd=[sys.executable,'-m','unittest','discover','-s','research/weighted_congestion_frontier/tests','-p','test_collaboration*.py','-v'];before=time.monotonic();p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=240)
  (out/(variant+'.stdout.txt')).write_text(p.stdout);(out/(variant+'.stderr.txt')).write_text(p.stderr)
  q={'variant':variant,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-before,3),'source_inputs':inputs,'python_version':sys.version,'git_version':subprocess.check_output(['git','--version'],cwd=root,env=env,text=True).strip(),'environment_guards':{k:env[k] for k in ['GIT_ALLOW_PROTOCOL','GIT_TERMINAL_PROMPT','GIT_CONFIG_NOSYSTEM','GIT_CONFIG_GLOBAL','GIT_CONFIG_SYSTEM','PYTHONDONTWRITEBYTECODE']},'temporary_fixture_removed':True,'real_remote_or_effective_credentials':False,'scope':'new17-method finite collaboration fixture per real ref pairing; imported prior suites not rerun; not production throughput or mathematics'}
  (out/(variant+'.json')).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');summary.append({k:q[k] for k in ['variant','returncode','seconds']});print(json.dumps(summary[-1]),flush=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
