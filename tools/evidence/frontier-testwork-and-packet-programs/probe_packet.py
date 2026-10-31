"""New finite helper cases and real-byte current-input refusal; no historical ZIP claim."""
from pathlib import Path
import hashlib,importlib.util,json,os,subprocess,sys,tempfile,zipfile
E=Path(__file__).resolve().parent;S=E.parents[2];out=E/'runs';out.mkdir(exist_ok=True)
rows={x['id']:x for f in ['source-manifest.json','data-dependency-manifest.json'] for x in json.loads((E/f).read_text())}
source=S/rows['8981310291bda5d63e07']['saved_path'];spec=importlib.util.spec_from_file_location('frozen_exporter',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
def record(case,observed):results.append({'case':case,'observed':observed})
for p in ['','/absolute','a//b','a/../b','a\\b','a\x00b']:
 try:m.safe_path(p)
 except ValueError:pass
 else:raise AssertionError(p)
record('six unsafe archive paths refused',6)
assert m.extract_task(b'header\n~~~text\nwhole task\n\n~~~\nfooter\n')==b'whole task\n'
for raw in [b'no task block\n',b'~~~text\na\n~~~\n~~~text\nb\n~~~\n']:
 try:m.extract_task(raw)
 except ValueError:pass
 else:raise AssertionError('task ambiguity')
record('single task extraction and zero/multiple rejection',{'single_complete_body':'whole task\n','invalid_cases':2})
raw=b'[x](../paper.md)\n`[code](../keep.md)`\n~~~python\n[z](../keep2.md)\n~~~\n[id]: <../ref.md>\n'
converted,changed=m.rewrite_links(raw,'research/topic/a.md','https://github.com/fixture/repo','a'*40)
assert len(changed)==2 and b'`[code](../keep.md)`' in converted and b'[z](../keep2.md)' in converted and b'/blob/'+b'a'*40+b'/research/paper.md' in converted
record('relative prose/reference destinations rewritten while inline/fenced code preserved',{'source_hex':raw.hex(),'converted_hex':converted.hex(),'changed':changed})
try:m.rewrite_links(b'[x](%2e%2e/%2e%2e/%2e%2e/outside.md)','research/topic/a.md','https://github.com/fixture/repo','a'*40)
except ValueError:record('encoded link escape refused',True)
else:raise AssertionError('encoded escape')
env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','WCG_')) and k not in ('SSH_AUTH_SOCK','SSH_ASKPASS')};env.update(GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null',PYTHONDONTWRITEBYTECODE='1')
with tempfile.TemporaryDirectory(prefix='packet-fixture-',dir=S) as tmp:
 root=Path(tmp);repo=root/'repo';repo.mkdir()
 existing=root/'existing';existing.write_text('keep');dangling=root/'dangling';dangling.symlink_to(root/'absent')
 for p in [existing,dangling,repo/'new-output']:
  try:m.external_new_path(p,repo)
  except ValueError:pass
  else:raise AssertionError(p)
 record('existing, dangling-symlink and repository-contained outputs refused',3)
 content={'TASK.md':b'synthetic helper fixture\n','optional/example.md':b'finite file I/O example, no mathematical theorem\n'}
 content['MANIFEST.json']=(json.dumps({'files':[{'path':k,'sha256':m.sha(v)} for k,v in content.items()]})+'\n').encode()
 packet=root/'small-output';archive=root/'small.zip';m.write_and_verify(content,packet,archive)
 with zipfile.ZipFile(archive) as z:assert set(z.namelist())==set(content) and all(z.read(k)==v for k,v in content.items())
 record('small actual ZIP/extraction/output reread',{'members':sorted(content),'payload_sha256':{k:m.sha(v) for k,v in content.items()},'zip_sha256':m.sha(archive.read_bytes()),'scope':'synthetic three-file helper packet, not canonical22'})
 bad={'TASK.md':b'synthetic','MANIFEST.json':b'{"files":[{"path":"TASK.md","sha256":"wrong"}]}\n'};badout=root/'bad-output';badzip=root/'bad.zip'
 try:m.write_and_verify(bad,badout,badzip)
 except ValueError:assert not badout.exists() and not badzip.exists()
 else:raise AssertionError('bad manifest')
 record('bad manifest hash rolls back newly created outputs',True)
 inputs=[]
 for ident in ['8981310291bda5d63e07','1cf29de35f3e8a430186','4564afcb575533e1c830','ff9fc2edcae1cd6fac79','9481228f7835e0de76b0']:
  x=rows[ident];raw=(S/x['saved_path']).read_bytes();assert len(raw)==x['size'] and m.sha(raw)==x['sha256'];p=repo/x['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);inputs.append({'id':ident,'path':x['path'],'bytes':x['size'],'sha256':x['sha256']})
 def git(*args):return subprocess.run(['git',*args],cwd=repo,env=env,capture_output=True,check=True,timeout=20).stdout
 git('init','--quiet');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid');git('add','.');git('commit','--quiet','-m','real frozen-input bytes in new disposable fixture');commit=git('rev-parse','HEAD').decode().strip()
 # A dirty working-tree brief must not replace the committed byte input.
 (repo/'research/weighted_congestion_frontier/PRO_BRIEF.md').write_text('dirty unrelated text\n')
 finalout=root/'canonical-attempt';finalzip=root/'canonical-attempt.zip'
 cmd=[sys.executable,str(source),'--repo',str(repo),'--commit',commit,'--output-dir',str(finalout),'--zip',str(finalzip)];p=subprocess.run(cmd,cwd=repo,env=env,capture_output=True,text=True,timeout=30)
 assert p.returncode==1 and 'PRO_ATTACK differs from its reviewed source mapping hash' in p.stderr and not finalout.exists() and not finalzip.exists()
 (out/'packet-real-input-refusal.stdout.txt').write_text(p.stdout);(out/'packet-real-input-refusal.stderr.txt').write_text(p.stderr)
 record('real current frozen-input bytes refuse stale reviewed TASK before any package',{'returncode':p.returncode,'stderr':p.stderr,'fixture_commit':commit,'original_source_commits_not_recreated':True,'source_inputs':inputs,'output_exists':False,'zip_exists':False,'dirty_worktree_not_used':True,'old_task_sha_unavailable':'76b12f434c6990930bbabe8b909ec96c4de7915afab4e38ae8211318846f0e89','current_task_sha':rows['9481228f7835e0de76b0']['sha256']})
result={'passed':True,'cases':results,'counted_cases':len(results),'source_id':'8981310291bda5d63e07','source_sha256':m.sha(source.read_bytes()),'python_version':sys.version,'scope':'new finite helpers plus true-byte input refusal at newly created fixture commit, not old complete22 ZIP or mathematical verification','real_remote_or_effective_credentials':False,'environment_guards':{k:env[k] for k in ['GIT_ALLOW_PROTOCOL','GIT_CONFIG_GLOBAL','GIT_CONFIG_SYSTEM','GIT_CONFIG_NOSYSTEM','GIT_TERMINAL_PROMPT']}}
(out/'packet-probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'cases':len(results),'passed':True,'canonical_package':'refused-task-hash-mismatch-no-output'}))
