"""Frozen checkpoint tests with file-only temporary Git fixtures; no active checkout."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,time
E=Path(__file__).resolve().parent;S=E.parents[2]
records={x['id']:x for name in ['source-manifest.json','dependency-manifest.json'] for x in json.loads((E/name).read_text())}
out=E/'runs';out.mkdir(exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','WCG_')) and k not in ('SSH_AUTH_SOCK','SSH_ASKPASS')}
env.update(GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',PYTHONDONTWRITEBYTECODE='1')
summary=[]
for variant,primary,rootid in [('main','db6af3d64d99cc147969','d9b5b49ab665613450d6'),('legacy','f4ad07192854bfc106ad','3c0404b7974eca538863')]:
    with tempfile.TemporaryDirectory(prefix='checkpoint-audit-',dir=S) as tmp:
        root=Path(tmp);inputs=[]
        for i in [primary,rootid,'794a190330ebe5b3679b','b054428c6de628f29738','2f4fa59cd9903d4c32e9']:
            x=records[i];raw=(S/x['saved_path']).read_bytes();assert len(raw)==x['size'] and hashlib.sha256(raw).hexdigest()==x['sha256']
            p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);p.chmod(0o755 if x['mode']=='100755' else 0o644);inputs.append({'id':i,'path':x['path'],'sha256':x['sha256'],'bytes':x['size'],'mode':x['mode']})
        subprocess.run(['git','init','--quiet',str(root)],cwd=root,env=env,check=True,capture_output=True,timeout=20)
        for label,command in [('original45',[sys.executable,'-m','unittest','discover','-s','research/weighted_congestion_frontier/tests','-p','test_checkpoint.py','-v']),('new6',[sys.executable,str(E/'probe_fixture.py')])]:
            before=time.monotonic();p=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,timeout=180)
            key=variant+'-'+label;(out/(key+'.stdout.txt')).write_text(p.stdout);(out/(key+'.stderr.txt')).write_text(p.stderr)
            report={'variant':variant,'suite':label,'returncode':p.returncode,'seconds':round(time.monotonic()-before,3),'command':command,'source_inputs':inputs,'git_version':subprocess.check_output(['git','--version'],cwd=root,env=env,text=True).strip(),'python_version':sys.version,'environment_guards':{k:env[k] for k in ['GIT_ALLOW_PROTOCOL','GIT_TERMINAL_PROMPT','GIT_CONFIG_NOSYSTEM','GIT_CONFIG_GLOBAL','GIT_CONFIG_SYSTEM','PYTHONDONTWRITEBYTECODE']},'scope':'new finite isolated software fixtures only; no production, real authentication or mathematical certification','real_remote_or_effective_credentials':False,'temporary_fixture_removed':True}
            (out/(key+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');summary.append({k:report[k] for k in ['variant','suite','returncode','seconds']});print(json.dumps(summary[-1]),flush=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
