"""Publish Stage16 reviewed bodies, RUN, and stable working mathematics once."""
from pathlib import Path
import subprocess
import json

REPO = Path(__file__).resolve().parents[4]
OUT = REPO.parent/'checkpoint-stage16'
WS = 'research/workspaces/six-boss1-20261111/'
LIVE = ('visible_maximum_joint/', 'visible_maximum_joint.md',
        'maximal_root_tail_wallet_v3_audit/', 'maximal_root_tail_wallet_v3_audit.md')
BODIES = {
    'archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md',
    'archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md',
    'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md',
    'research/registry.json'
}


def capture(args):
    return subprocess.run(args, cwd=REPO, capture_output=True, check=True).stdout


def allowed(path):
    if path in BODIES:
        return True
    if path.startswith('map/edges/six-boss1-20261111/'):
        return True
    if path.startswith('research/runs/six-boss1-20261111/'):
        return True
    if path.startswith(WS):
        return not any(path[len(WS):].startswith(prefix) for prefix in LIVE)
    return False


def main():
    assert not Path(str(OUT)+'.json').exists()
    assert (REPO/WS/'registration/stage16-save-receipts.json').exists()
    edges = json.loads((REPO/WS/'registration/stage16-edge-receipts.json').read_text())
    assert len(edges) == 16
    assert capture(['git', 'branch', '--show-current']).decode().strip() == 'rebuild/research-v2'
    assert not capture(['git', 'diff', '--cached', '--name-only']).strip()
    paths, skipped = [], []
    for raw in capture(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all']).split(b'\0'):
        if not raw:
            continue
        flag, path = raw[:2].decode(), raw[3:].decode()
        assert 'R' not in flag and 'C' not in flag
        if allowed(path):
            assert (REPO/path).is_file() and (REPO/path).stat().st_size < 90_000_000
            paths.append(path)
        else:
            skipped.append(path)
    paths = sorted(set(paths))
    assert len(paths) > 100
    cmd = ['python', 'work.py', 'checkpoint', '-m',
           'Boss1: publish real requery lemma, 867 full-type certificate and root capacity advances']+paths
    Path(str(OUT)+'.argv.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2)+'\n')
    selection = {'selected_count': len(paths), 'total_bytes': sum((REPO/path).stat().st_size for path in paths),
                 'paths': paths, 'skipped': skipped}
    Path(str(OUT)+'.selection.json').write_text(json.dumps(selection, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'selected_count': len(paths), 'selected_bytes': selection['total_bytes'],
                      'skipped_count': len(skipped)}), flush=True)
    result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    Path(str(OUT)+'.stdout.txt').write_text(result.stdout)
    Path(str(OUT)+'.stderr.txt').write_text(result.stderr)
    receipt = {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    start = result.stdout.find('{')
    if start >= 0:
        try:
            receipt['receipt'] = json.JSONDecoder().raw_decode(result.stdout[start:])[0]
        except json.JSONDecodeError:
            pass
    Path(str(OUT)+'.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    print(result.stdout[-7000:], flush=True)
    if result.stderr:
        print(result.stderr[-2500:], flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
