"""Retry the concrete corrected publication; preserve the failed attempt receipt."""
from pathlib import Path
import json
import subprocess

REPO=Path(__file__).resolve().parents[4]
OUT=REPO.parent/'checkpoint-stage16c'
WS='research/workspaces/six-boss1-20261111/'
LIVE=('visible_maximum_joint_v2/','visible_maximum_joint_v2.md',
      'main_source2_maximum_nested_safe_audit/','main_source2_maximum_nested_safe_audit.md')
FROZEN_LOCAL_DRAFT=WS+'registration/stage16_new_lemma/body.md'
BODIES={
    'archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md',
    'archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md',
    'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md',
    'research/registry.json'}


def capture(args):
    return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout


def allowed(path):
    if path in {FROZEN_LOCAL_DRAFT,WS+'visible_maximum_joint/row_catalog.tsv'}:
        return False
    if path in BODIES or path.startswith('map/edges/six-boss1-20261111/') or path.startswith('research/runs/six-boss1-20261111/'):
        return True
    return path.startswith(WS) and not any(path[len(WS):].startswith(p) for p in LIVE)


def main():
    assert not Path(str(OUT)+'.json').exists()
    assert (REPO/WS/'registration/stage16b-save-receipts.json').exists()
    assert capture(['git','branch','--show-current']).decode().strip()=='rebuild/research-v2'
    paths,skipped=[],[]
    for raw in capture(['git','status','--porcelain=v1','-z','--untracked-files=all']).split(b'\0'):
        if not raw: continue
        flag,path=raw[:2].decode(),raw[3:].decode()
        assert 'R' not in flag and 'C' not in flag
        if allowed(path):
            assert (REPO/path).is_file() and (REPO/path).stat().st_size<90_000_000,path
            paths.append(path)
        else: skipped.append(path)
    paths=sorted(set(paths))
    staged=set(capture(['git','diff','--cached','--name-only','-z']).decode().strip('\0').split('\0'))-{''}
    assert staged <= set(paths),sorted(staged-set(paths))
    assert FROZEN_LOCAL_DRAFT not in paths
    for path in paths:
        try:
            lines=(REPO/path).read_text().splitlines()
        except UnicodeError:
            continue
        bad=[i+1 for i,line in enumerate(lines) if line.endswith((' ','\t'))]
        assert not bad,(path,bad[:8])
    selection=dict(selected_count=len(paths),selected_bytes=sum((REPO/p).stat().st_size for p in paths),paths=paths,skipped=skipped)
    cmd=['python','work.py','checkpoint','-m','Boss1: publish real requery lemma, full visible-C certificate and nested true-source advance']+paths
    Path(str(OUT)+'.selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
    Path(str(OUT)+'.argv.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in selection.items() if k not in ['paths','skipped']}),flush=True)
    r=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
    Path(str(OUT)+'.stdout.txt').write_text(r.stdout);Path(str(OUT)+'.stderr.txt').write_text(r.stderr)
    receipt=dict(exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
    start=r.stdout.find('{')
    if start>=0:
        try: receipt['receipt']=json.JSONDecoder().raw_decode(r.stdout[start:])[0]
        except json.JSONDecodeError: pass
    Path(str(OUT)+'.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    actual=receipt.get('receipt',{})
    print(json.dumps({k:actual.get(k) for k in ['status','commit','branch','created_commit','checked_head']}),flush=True)
    if r.returncode: print(r.stderr[-5000:],flush=True)
    raise SystemExit(r.returncode)


if __name__=='__main__':
    main()
