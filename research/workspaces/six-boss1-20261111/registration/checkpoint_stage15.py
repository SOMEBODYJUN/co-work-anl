"""Publish completed Stage15 work; exclude live builders and derived map dumps."""
from pathlib import Path
import subprocess
import json

REPO=Path(__file__).resolve().parents[4]
OUT=REPO.parent/'checkpoint-stage15'
WS='research/workspaces/six-boss1-20261111/'
ACTIVE=('universal_union_wallet_v5/','universal_union_wallet_v5.md',
        'v4_source2_identity/','v4_source2_identity.md',
        'background_projection_audit/','background_projection_audit.md')


def capture(args):return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout


def allowed(path):
    if path=='archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md':return True
    if path.startswith('research/runs/six-boss1-20261111/'):return True
    if path.startswith(WS):return not any(path[len(WS):].startswith(a) for a in ACTIVE)
    return False


def main():
    assert not Path(str(OUT)+'.json').exists()
    assert (REPO/WS/'registration/stage15-save-receipts.json').exists()
    assert capture(['git','branch','--show-current']).decode().strip()=='rebuild/research-v2'
    assert not capture(['git','diff','--cached','--name-only']).strip()
    paths=[]; skipped=[]
    for raw in capture(['git','status','--porcelain=v1','-z','--untracked-files=all']).split(b'\0'):
        if not raw:continue
        flag,path=raw[:2].decode(),raw[3:].decode()
        assert 'R' not in flag and 'C' not in flag
        if allowed(path):
            assert (REPO/path).is_file() and (REPO/path).stat().st_size<90_000_000
            paths.append(path)
        else:skipped.append(path)
    paths=sorted(set(paths));assert len(paths)>100
    cmd=['python','work.py','checkpoint','-m','Boss1: certify 225 full-type bound, true requery cuts and all-source portfolio family']+paths
    Path(str(OUT)+'.argv.json').write_text(json.dumps(cmd,ensure_ascii=False,indent=2)+'\n')
    selection={'selected_count':len(paths),'total_bytes':sum((REPO/p).stat().st_size for p in paths),'paths':paths,'skipped':skipped}
    Path(str(OUT)+'.selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'selected_count':len(paths),'selected_bytes':selection['total_bytes'],'skipped_count':len(skipped)}),flush=True)
    result=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
    Path(str(OUT)+'.stdout.txt').write_text(result.stdout);Path(str(OUT)+'.stderr.txt').write_text(result.stderr)
    receipt={'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
    start=result.stdout.find('{')
    if start>=0:
        try:receipt['receipt']=json.JSONDecoder().raw_decode(result.stdout[start:])[0]
        except json.JSONDecodeError:pass
    Path(str(OUT)+'.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(result.stdout[-7000:],flush=True)
    if result.stderr:print(result.stderr[-2500:],flush=True)
    raise SystemExit(result.returncode)


if __name__=='__main__':main()
