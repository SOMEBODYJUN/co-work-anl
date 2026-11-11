"""Serial publication of closed Stage17 mathematics; leave active writers untouched."""
from pathlib import Path
import json
import subprocess

REPO=Path(__file__).resolve().parents[4]
OUT=REPO.parent/'checkpoint-stage17'
WS='research/workspaces/six-boss1-20261111/'
LIVE=('visible_maximum_joint_v4/','visible_maximum_joint_v4.md',
      'visible_maximum_joint_v4_solve/','visible_maximum_joint_v4_solve.md',
      'all_source_ordered_joint_menu/','all_source_ordered_joint_menu.md',
      'main_ordered_joint_menu/')
LOCAL_ONLY={WS+'registration/stage16_new_lemma/body.md',WS+'visible_maximum_joint/row_catalog.tsv'}

def git(*args):
    return subprocess.run(['git',*args],cwd=REPO,capture_output=True,check=True).stdout

def wanted(p):
    if p in LOCAL_ONLY:return False
    if p.startswith('research/runs/six-boss1-20261111/'):return True
    if p=='archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md':return True
    return p.startswith(WS) and not any(p[len(WS):].startswith(x) for x in LIVE)

assert not Path(str(OUT)+'.json').exists()
assert (REPO/WS/'registration/stage17-save-receipts.json').exists()
assert git('branch','--show-current').decode().strip()=='rebuild/research-v2'
paths=[];skipped=[]
for raw in git('status','--porcelain=v1','-z','--untracked-files=all').split(b'\0'):
    if not raw:continue
    flag,p=raw[:2].decode(),raw[3:].decode()
    assert 'R' not in flag and 'C' not in flag
    if wanted(p):
        assert (REPO/p).is_file() and (REPO/p).stat().st_size<90_000_000,p
        paths.append(p)
    else:skipped.append(p)
paths=sorted(set(paths))
staged=set(git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0'))-{''}
assert staged<=set(paths),sorted(staged-set(paths))
bad=[]
for p in paths:
    try:lines=(REPO/p).read_text().splitlines()
    except UnicodeError:continue
    hits=[i+1 for i,s in enumerate(lines) if s.endswith((' ','\t'))]
    if hits:bad.append({'path':p,'lines':hits[:12]})
selection={'selected_count':len(paths),'selected_bytes':sum((REPO/p).stat().st_size for p in paths),
           'paths':paths,'skipped':skipped,'trailing_whitespace':bad,
           'active_writer_policy':'Only closed frozen packages and Main RUN/status files. No stash/reset/sync.'}
Path(str(OUT)+'.selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
assert not bad,bad
cmd=['python','work.py','checkpoint','-m','Boss1: preserve full 1003 certificate, exact internal-source domains and 536 universal rows']+paths
Path(str(OUT)+'.argv.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:selection[k] for k in ['selected_count','selected_bytes']}),flush=True)
r=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
Path(str(OUT)+'.stdout.txt').write_text(r.stdout);Path(str(OUT)+'.stderr.txt').write_text(r.stderr)
record={'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
start=r.stdout.find('{')
if start>=0:
    try:record['receipt']=json.JSONDecoder().raw_decode(r.stdout[start:])[0]
    except json.JSONDecodeError:pass
Path(str(OUT)+'.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
x=record.get('receipt',{})
print({k:x.get(k) for k in ['status','commit','pushed_head','remote_tip']},flush=True)
if r.returncode:print(r.stderr[-4000:],flush=True)
raise SystemExit(r.returncode)
