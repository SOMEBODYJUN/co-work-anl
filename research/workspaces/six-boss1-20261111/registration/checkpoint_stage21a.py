"""Main serial checkpoint: completed research-clone work, isolated agents excluded."""
from pathlib import Path
from hashlib import sha256
import subprocess
import json

B=Path('/workspace/scratch/b0fef5ec503f')
R=B/'co-work-anl-boss1'
W='research/workspaces/six-boss1-20261111/'
RUN='research/runs/six-boss1-20261111/'
README='archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'
OUT=B/'checkpoint-stage21a'
EXCLUDED={W+'registration/stage16_new_lemma/body.md'}|{W+p+'/row_catalog.tsv' for p in [
 'visible_maximum_joint','visible_maximum_joint_v3','visible_maximum_joint_v4','visible_maximum_joint_v5','visible_maximum_joint_v6']}
EXCLUDED|={W+p for p in [
 'registration/stage19-gamma36-addition.md','source1_lambda_complete/endpoint_table.md',
 'source2_conditional_redistribution/breakpoint_table.md','source2_conditional_redistribution/conditional_piecewise_table.md',
 'visible_maximum_joint_v6_solve_v2/core_interface_patch.diff']}
def git(*args):
    return subprocess.run(['git',*args],cwd=R,capture_output=True,check=True).stdout
assert not Path(str(OUT)+'.json').exists()
for d,pin in {
    'visible_maximum_joint_v6_solve_v2':'993c51f83859005df9fe237979360ed54e4b52f310e13eb7c078c4d1c8646d2a',
    'main_root_reweighting':'fb21377e83b3edfe8c1334dfd1aa63e48b2003e1f52aa73cda4e5d80796fedf3',
    'main_v6_exact_audit':'b77a4dc203eaea44ba1367f049237e927d57ce30d271eab45d0a33ab1a3b679f',
    'main_terminal_reply_requery':'e72172fe5bb25c7feae3ec8e7668a52404f507b180cdc874d4a2a62036c38e8a',
}.items():
    assert sha256((R/W/d/'freeze_manifest.json').read_bytes()).hexdigest()==pin
assert not git('ls-files','-u')
selected=[]
for entry in git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0'):
    if not entry: continue
    status,path=entry[:2].decode(),entry[3:].decode()
    assert 'R' not in status and 'C' not in status
    if path in EXCLUDED or '__pycache__' in Path(path).parts: continue
    if path.startswith(W) or path.startswith(RUN) or path==README: selected.append(path)
selected=sorted(set(selected))
assert selected
bad=[]
for path in selected:
    p=R/path;assert p.is_file() and p.stat().st_size<90_000_000,path
    try:s=p.read_text()
    except UnicodeError:continue
    if s.endswith('\n\n') or any(line.rstrip()!=line for line in s.splitlines()):bad.append(path)
assert not bad,bad
staged=set(git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0'))-{''}
assert staged<=set(selected),staged-set(selected)
record={'status':'MAIN_CLOSED_STAGE21_ASSETS_SELECTED',
    'source_head':git('rev-parse','HEAD').decode().strip(),'selected_count':len(selected),
    'selected_bytes':sum((R/p).stat().st_size for p in selected),'paths':selected,
    'excluded_frozen_text_originals_restored_by_gzip':sorted(EXCLUDED),
    'active_agent_directories_outside_clone':['visible_v7_prepare_stage','source3_A5_joint_stage','source2_C_joint_SAFE4_stage'],
    'v6_solver_stopped_and_frozen':True,'optimizer_calls_v6_total':1,
    'full_necessary_matrix_and_exact_SPE_model_preserved':True}
Path(str(OUT)+'.selection.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['selected_count','selected_bytes']}),flush=True)
args=['python','work.py','checkpoint','-m',
    'Boss1: certify full4177 solve; prove stronger universal bound and true terminal-reply requery family']+selected
p=subprocess.run(args,cwd=R,capture_output=True,text=True)
Path(str(OUT)+'.stdout.txt').write_text(p.stdout)
Path(str(OUT)+'.stderr.txt').write_text(p.stderr)
result={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
try:result['receipt']=json.JSONDecoder().raw_decode(p.stdout[p.stdout.index('{'):])[0]
except (ValueError,json.JSONDecodeError):pass
Path(str(OUT)+'.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
receipt=result.get('receipt',{})
print(json.dumps({k:receipt.get(k) for k in ['status','commit','pushed_head','remote_tip']}),flush=True)
if p.returncode:print(p.stderr[-4000:],flush=True)
raise SystemExit(p.returncode)
