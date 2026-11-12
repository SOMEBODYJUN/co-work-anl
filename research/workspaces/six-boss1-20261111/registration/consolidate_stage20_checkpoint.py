"""Main serial checkpoint from the integrated clone, copying only closed work."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

B=Path('/workspace/scratch/b0fef5ec503f')
SRC=B/'co-work-anl-boss1'
DST=B/'co-work-anl-boss1-map'
WS='research/workspaces/six-boss1-20261111/'
MW='research/workspaces/map-v2/Boss1/six-boss1-stage19/'
OUT=B/'checkpoint-stage20a'
EXCLUDED={WS+'registration/stage16_new_lemma/body.md'}|{WS+p+'/row_catalog.tsv' for p in [
 'visible_maximum_joint','visible_maximum_joint_v3','visible_maximum_joint_v4','visible_maximum_joint_v5','visible_maximum_joint_v6']}
EXCLUDED|={WS+p for p in ['registration/stage19-gamma36-addition.md','source1_lambda_complete/endpoint_table.md',
 'source2_conditional_redistribution/breakpoint_table.md','source2_conditional_redistribution/conditional_piecewise_table.md',
 'visible_maximum_joint_v6_solve_v2/core_interface_patch.diff']}
README='archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'

def git(root,*args,check=True):
 return subprocess.run(['git',*args],cwd=root,capture_output=True,check=check)

assert not Path(str(OUT)+'.json').exists()
assert json.loads((DST/'map/integration.json').read_text())['task_receipt_pins']['six-boss1-stage19-wallets-map3b']=='19e9f6b2d4b94cced9b34ff3e5b884e025a7067f217c06f2b23299e6e4988481'
assert len(json.loads((DST/'research/registry.json').read_text())['edge_files'])==2130
assert not (SRC/WS/'visible_maximum_joint_v6_solve_v2/single_lp_consumed.json').exists()
copies=[]
for row in git(SRC,'status','--porcelain=v1','-z','--untracked-files=all').stdout.split(b'\0'):
 if not row:continue
 flag,p=row[:2].decode(),row[3:].decode()
 assert 'R' not in flag and 'C' not in flag
 if p in EXCLUDED or '__pycache__' in Path(p).parts:continue
 if not (p.startswith(WS) or p.startswith('research/runs/six-boss1-20261111/') or p==README):continue
 origin=SRC/p;dest=DST/p
 assert origin.is_file(),p
 if dest.exists() and dest.read_bytes()!=origin.read_bytes():
  base=git(SRC,'show','HEAD:'+p,check=False)
  assert base.returncode==0 and dest.read_bytes()==base.stdout,('preserve unexpected destination edit',p)
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(origin,dest)
 copies.append({'path':p,'sha256':hashlib.sha256(origin.read_bytes()).hexdigest(),'bytes':origin.stat().st_size})
record={'status':'MAIN_CLOSED_WORK_COPIED_BYTE_EXACT_FOR_SERIAL_CHECKPOINT',
 'source_head':git(SRC,'rev-parse','HEAD').stdout.decode().strip(),
 'integrating_head':git(DST,'rev-parse','HEAD').stdout.decode().strip(),
 'copied_files':copies,'live_isolated_directories_not_copied':['root270_replycaps_iter2_stage','cap3_full_delta_rows_stage'],
 'no_active_writer_in_source_or_destination_clone':True}
copy_record=WS+'registration/stage20a-copy-record.json'
(DST/copy_record).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
selected={x['path'] for x in copies}|{copy_record}
for row in git(DST,'status','--porcelain=v1','-z','--untracked-files=all').stdout.split(b'\0'):
 if not row:continue
 p=row[3:].decode()
 if p.startswith(MW) or p in ['research/registry.json','map/coverage.json','map/integration.json']:
  selected.add(p)
selected=sorted(selected)
bad=[]
for p in selected:
 f=DST/p;assert f.is_file() and f.stat().st_size<90_000_000,p
 try:t=f.read_text()
 except UnicodeError:continue
 if t.endswith('\n\n') or any(line.rstrip()!=line for line in t.splitlines()):bad.append(p)
assert not bad,bad
staged=set(git(DST,'diff','--cached','--name-only','-z').stdout.decode().strip('\0').split('\0'))-{''}
assert staged<=set(selected),staged-set(selected)
selection={'selected_count':len(selected),'selected_bytes':sum((DST/p).stat().st_size for p in selected),'paths':selected}
Path(str(OUT)+'.selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:selection[k] for k in ['selected_count','selected_bytes']}),flush=True)
cmd=['python','work.py','checkpoint','-m','Boss1: integrate reviewed Stage19 relations; prove true reply-cap welfare gain and preserve full next-stage recovery']+selected
p=subprocess.run(cmd,cwd=DST,capture_output=True,text=True)
Path(str(OUT)+'.stdout.txt').write_text(p.stdout);Path(str(OUT)+'.stderr.txt').write_text(p.stderr)
result={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
try:result['receipt']=json.JSONDecoder().raw_decode(p.stdout[p.stdout.index('{'):])[0]
except (ValueError,json.JSONDecodeError):pass
Path(str(OUT)+'.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
receipt=result.get('receipt',{})
print(json.dumps({k:receipt.get(k) for k in ['status','commit','pushed_head','remote_tip']}),flush=True)
if p.returncode:print(p.stderr[-4000:],flush=True)
raise SystemExit(p.returncode)
