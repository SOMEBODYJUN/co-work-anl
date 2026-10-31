"""Only new disposable roots and local file Git remotes, with synthetic test identities."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile,time
E=Path(__file__).resolve().parent;S=E.parents[2]
records={x['id']:x for f in ['source-manifest.json','code-dependency-manifest.json','data-dependency-manifest.json'] for x in json.loads((E/f).read_text())}
out=E/'runs';out.mkdir(exist_ok=True)
env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','WCG_')) and k not in ('SSH_AUTH_SOCK','SSH_ASKPASS')}
env.update(GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',PYTHONDONTWRITEBYTECODE='1')
summary=[]
for variant,ids in [('main',['0267e9382e7d95b35a5e','d9b5b49ab665613450d6','db6af3d64d99cc147969','99da839bfd62db2365a0']),('legacy',['de53a0261145104205aa','3c0404b7974eca538863','f4ad07192854bfc106ad','673a94bf8c2a50db4be5'])]:
 ref='main' if variant=='main' else 'legacy-cleanup'
 ids+=['b054428c6de628f29738','6a406a34c340855b3f7f']
 docs=[x['id'] for x in json.loads((E/'data-dependency-manifest.json').read_text()) if any(z['name']==ref for z in x['sources']) and not any(k in x['path'] for k in ['PRO_BRIEF','PRO_ATTACK','review_status'])]
 with tempfile.TemporaryDirectory(prefix='work-suite-',dir=S) as temp:
  root=Path(temp);inputs=[]
  for ident in ids+docs:
   x=records[ident];raw=(S/x['saved_path']).read_bytes();assert len(raw)==x['size'] and hashlib.sha256(raw).hexdigest()==x['sha256'];p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);p.chmod(0o755 if x['mode']=='100755' else 0o644);inputs.append({'id':ident,'path':x['path'],'sha256':x['sha256'],'bytes':x['size'],'mode':x['mode'],'runtime_use':'code' if ident in ids else 'path-existence assertion only; mathematical text not read by tests'})
  subprocess.run(['git','init','--quiet',str(root)],cwd=root,env=env,check=True,capture_output=True,timeout=20)
  cmd=[sys.executable,'-m','unittest','discover','-s','research/weighted_congestion_frontier/tests','-p','test_work.py','-v'];before=time.monotonic();p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=240)
  (out/(variant+'-work.stdout.txt')).write_text(p.stdout);(out/(variant+'-work.stderr.txt')).write_text(p.stderr)
  helper=subprocess.run(['bash',str(root/'research/weighted_congestion_frontier/tools/work.sh'),'--help'],cwd=root.parent,env=env,capture_output=True,text=True,timeout=20)
  (out/(variant+'-worksh-help.stdout.txt')).write_text(helper.stdout);(out/(variant+'-worksh-help.stderr.txt')).write_text(helper.stderr)
  result={'variant':variant,'returncode':p.returncode,'seconds':round(time.monotonic()-before,3),'command':cmd,'source_inputs':inputs,'work_sh_help_exit':helper.returncode,'work_sh_help_has_checkpoint':'checkpoint' in helper.stdout,'python_version':sys.version,'git_version':subprocess.check_output(['git','--version'],cwd=root,env=env,text=True).strip(),'environment_guards':{k:env[k] for k in ['GIT_ALLOW_PROTOCOL','GIT_TERMINAL_PROMPT','GIT_CONFIG_NOSYSTEM','GIT_CONFIG_GLOBAL','GIT_CONFIG_SYSTEM','PYTHONDONTWRITEBYTECODE']},'real_remote_or_effective_credentials':False,'scope':'new finite local fixtures, synthetic actors/ASKPASS only, not current production or mathematics'}
  (out/(variant+'-work.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');summary.append({k:result[k] for k in ['variant','returncode','seconds','work_sh_help_exit']});print(json.dumps(summary[-1]),flush=True)
(out/'work-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
