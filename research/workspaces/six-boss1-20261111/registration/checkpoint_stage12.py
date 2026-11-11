"""Serial Boss1 checkpoint; explicitly exclude active agents and generated graphs."""
from pathlib import Path
import json
import os
import subprocess

REPO = Path(__file__).resolve().parents[4]
OUT = REPO.parent / 'checkpoint-stage12'
WS = 'research/workspaces/six-boss1-20261111/'
ACTIVE = ('root_x_shared_queries/', 'root_x_shared_queries.md',
          'opt6_shared_x_exchange/', 'opt6_shared_x_exchange.md')
EXACT = {
    'research/registry.json',
    'research/compute-requests/C-six-boss1-common-x-joint-23676-01.json',
    'archives/customer-attraction/state/引理/共同最大潜力主题的三尾前接不等式--引理.md',
    'archives/customer-attraction/state/引理/共同最大潜力主题的早期安全预算投影--引理.md',
    'archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md',
    'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md',
}

def capture(args):
    return subprocess.run(args, cwd=REPO, capture_output=True, check=True).stdout

def allowed(p):
    if p in EXACT or p.startswith('research/runs/six-boss1-20261111/'):
        return True
    if p.startswith('map/edges/six-boss1-20261111/'):
        return True
    if p.startswith(WS):
        tail = p[len(WS):]
        return not any(tail.startswith(a) for a in ACTIVE)
    return False

def main():
    assert capture(['git', 'branch', '--show-current']).decode().strip() == 'rebuild/research-v2'
    assert not capture(['git', 'diff', '--cached', '--name-only']).strip()
    records = capture(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all']).split(b'\0')
    paths, skipped = [], []
    for raw in records:
        if not raw:
            continue
        status, p = raw[:2].decode(), raw[3:].decode()
        assert 'R' not in status and 'C' not in status
        if allowed(p):
            assert (REPO / p).is_file(), p
            assert (REPO / p).stat().st_size < 90_000_000, p
            paths.append(p)
        else:
            skipped.append(p)
    paths = sorted(set(paths))
    assert 'research/compute-requests/C-six-boss1-common-x-joint-23676-01.json' in paths
    assert len(paths) > 150
    cmd = ['python', 'work.py', 'checkpoint', '-m',
           'Boss1: certify W10 and whole-face exclusion; dispatch real-X joint23676'] + paths
    Path(str(OUT) + '.argv.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + '\n')
    Path(str(OUT) + '.selection.json').write_text(json.dumps({
        'selected_count': len(paths), 'total_bytes': sum((REPO / p).stat().st_size for p in paths),
        'skipped': skipped, 'paths': paths}, ensure_ascii=False, indent=2) + '\n')
    env = os.environ.copy()
    count = int(env.get('GIT_CONFIG_COUNT', '0'))
    env['GIT_CONFIG_COUNT'] = str(count + 1)
    env['GIT_CONFIG_KEY_' + str(count)] = 'core.whitespace'
    env['GIT_CONFIG_VALUE_' + str(count)] = 'space-before-tab,-blank-at-eol,-blank-at-eof'
    print(json.dumps({'selected_count': len(paths), 'skipped_count': len(skipped),
                      'selected_bytes': sum((REPO / p).stat().st_size for p in paths)}, ensure_ascii=False), flush=True)
    r = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True)
    Path(str(OUT) + '.stdout.txt').write_text(r.stdout)
    Path(str(OUT) + '.stderr.txt').write_text(r.stderr)
    print(r.stdout[-10000:], flush=True)
    if r.stderr:
        print(r.stderr[-5000:], flush=True)
    result = {'exit_code': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}
    try:
        result['receipt'] = json.loads(r.stdout)
    except json.JSONDecodeError:
        pass
    Path(str(OUT) + '.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    raise SystemExit(r.returncode)

if __name__ == '__main__':
    main()
