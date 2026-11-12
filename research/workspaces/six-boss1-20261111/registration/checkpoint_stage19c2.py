"""Main serial checkpoint: formal return and closed v6 preparation, no live tasks."""
from pathlib import Path
import json
import subprocess

R=Path(__file__).resolve().parents[4]
OUT=R.parent/'checkpoint-stage19c2'
WS='research/workspaces/six-boss1-20261111/'
LIVE=('source2_cap3_tradeoff/','source2_cap3_tradeoff.md','high_lambda_closure/','high_lambda_closure.md')
LOCAL_ONLY={WS+'registration/stage16_new_lemma/body.md'}|{WS+p+'/row_catalog.tsv' for p in [
 'visible_maximum_joint','visible_maximum_joint_v3','visible_maximum_joint_v4','visible_maximum_joint_v5','visible_maximum_joint_v6']}
LOCAL_ONLY.update({WS+name for name in ['registration/stage19-gamma36-addition.md', 'source1_lambda_complete/endpoint_table.md', 'source2_conditional_redistribution/breakpoint_table.md', 'source2_conditional_redistribution/conditional_piecewise_table.md']})
FORMAL={'research/registry.json',
 'archives/customer-attraction/state/引理/联合内部偏离的完整参数域与同菜单条件投影--引理.md',
 'archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md',
 'archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md',
 'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'}


def git(*args):
 return subprocess.run(['git',*args],cwd=R,capture_output=True,check=True).stdout


def wanted(p):
 if p in LOCAL_ONLY or '__pycache__' in Path(p).parts:return False
 if p in FORMAL or p.startswith('research/runs/six-boss1-20261111/') or p.startswith('map/edges/six-boss1-20261111/'):return True
 return p.startswith(WS) and not any(p[len(WS):].startswith(x) for x in LIVE)


assert not Path(str(OUT)+'.json').exists()
assert (R/WS/'registration/stage19c-save-receipts.json').exists()
assert git('branch','--show-current').decode().strip()=='rebuild/research-v2'
paths=[];skipped=[]
for raw in git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0'):
 if not raw:continue
 flag,p=raw[:2].decode(),raw[3:].decode()
 assert 'R' not in flag and 'C' not in flag
 if wanted(p):
  assert (R/p).is_file() and (R/p).stat().st_size<90_000_000,p
  paths.append(p)
 else:skipped.append(p)
paths=sorted(set(paths))
staged=set(git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0'))-{''}
assert staged<=set(paths),sorted(staged-set(paths))
bad=[]
for p in paths:
 try:lines=(R/p).read_text().splitlines()
 except UnicodeError:continue
 hits=[i+1 for i,s in enumerate(lines) if s.endswith((' ','\t'))]
 if hits:bad.append({'path':p,'lines':hits[:12]})
 if (R/p).read_bytes().endswith(b'\n\n'):bad.append({'path':p,'reason':'blank line at EOF'})
selection={'selected_count':len(paths),'selected_bytes':sum((R/p).stat().st_size for p in paths),
 'paths':paths,'skipped':skipped,'trailing_whitespace':bad,
 'active_writer_policy':'Selected closed sources, formal bodies/registry/affected edges and actual RUN. No stash/reset/sync. Two fresh mathematics directories excluded.'}
Path(str(OUT)+'.selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
assert not bad,bad
cmd=['python','work.py','checkpoint','-m','Boss1: return complete internal domains, ROOT270 and gamma36 proof; preserve full4177 input']+paths
Path(str(OUT)+'.argv.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:selection[k] for k in ['selected_count','selected_bytes']}),flush=True)
p=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
Path(str(OUT)+'.stdout.txt').write_text(p.stdout)
Path(str(OUT)+'.stderr.txt').write_text(p.stderr)
record={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
start=p.stdout.find('{')
if start>=0:
 try:record['receipt']=json.JSONDecoder().raw_decode(p.stdout[start:])[0]
 except json.JSONDecodeError:pass
Path(str(OUT)+'.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
x=record.get('receipt',{})
print(json.dumps({k:x.get(k) for k in ['status','commit','pushed_head','remote_tip']},ensure_ascii=False),flush=True)
if p.returncode:print(p.stderr[-4000:],flush=True)
raise SystemExit(p.returncode)
