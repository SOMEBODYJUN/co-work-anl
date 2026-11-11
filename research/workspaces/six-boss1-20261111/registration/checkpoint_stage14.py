"""Serial checkpoint of completed Stage14 proofs and real continuation state."""
from pathlib import Path
import json
import os
import subprocess

REPO = Path(__file__).resolve().parents[4]
OUT = REPO.parent / 'checkpoint-stage14'
WS = 'research/workspaces/six-boss1-20261111/'
ACTIVE = ('v3_optimum_joint_face/', 'v3_optimum_joint_face.md',
          'maximal_root_tail_wallet_v2/', 'maximal_root_tail_wallet_v2.md',
          'maximal_root_tail_wallet_v2_audit/', 'maximal_root_tail_wallet_v2_audit.md')
EXACT = {
    'research/registry.json',
    'archives/customer-attraction/state/引理/最大主题真实尾部的根收益加强--引理.md',
    'archives/customer-attraction/state/引理/共同最大潜力主题的两尾跨实际钱包投影--引理.md',
    'archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md',
    'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md',
}


def capture(args):
    return subprocess.run(args, cwd=REPO, capture_output=True, check=True).stdout


def allowed(path):
    if path in EXACT or path.startswith('research/runs/six-boss1-20261111/'):
        return True
    if path.startswith('map/edges/six-boss1-20261111/'):
        return True
    if path.startswith(WS):
        tail = path[len(WS):]
        return not any(tail.startswith(part) for part in ACTIVE)
    return False


def main():
    assert not Path(str(OUT) + '.json').exists(), 'Preserve prior checkpoint attempt'
    assert capture(['git', 'branch', '--show-current']).decode().strip() == 'rebuild/research-v2'
    assert not capture(['git', 'diff', '--cached', '--name-only']).strip()
    build = REPO / WS / 'registration/stage14-build.stdout.json'
    status = json.loads(build.read_text())
    assert status.get('status') == 'structure-valid-not-a-mathematical-verdict', status.get('status')
    paths, skipped = [], []
    for raw in capture(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all']).split(b'\0'):
        if not raw:
            continue
        flag, path = raw[:2].decode(), raw[3:].decode()
        assert 'R' not in flag and 'C' not in flag
        if allowed(path):
            assert (REPO / path).is_file(), path
            assert (REPO / path).stat().st_size < 90_000_000, path
            paths.append(path)
        else:
            skipped.append(path)
    paths = sorted(set(paths))
    assert EXACT <= set(paths)
    assert len(paths) > 150
    cmd = ['python', 'work.py', 'checkpoint', '-m',
           'Boss1: certify real-root tail bounds, full-type wallet optima and optimal-menu requery'] + paths
    Path(str(OUT) + '.argv.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + '\n')
    selection = {'selected_count': len(paths), 'total_bytes': sum((REPO / p).stat().st_size for p in paths),
                 'skipped': skipped, 'paths': paths}
    Path(str(OUT) + '.selection.json').write_text(json.dumps(selection, ensure_ascii=False, indent=2) + '\n')
    env = os.environ.copy()
    count = int(env.get('GIT_CONFIG_COUNT', '0'))
    env['GIT_CONFIG_COUNT'] = str(count + 1)
    env['GIT_CONFIG_KEY_' + str(count)] = 'core.whitespace'
    env['GIT_CONFIG_VALUE_' + str(count)] = 'space-before-tab,-blank-at-eol,-blank-at-eof'
    print(json.dumps({'selected_count': len(paths), 'selected_bytes': selection['total_bytes'],
                      'skipped_count': len(skipped)}), flush=True)
    result = subprocess.run(cmd, cwd=REPO, env=env, capture_output=True, text=True)
    Path(str(OUT) + '.stdout.txt').write_text(result.stdout)
    Path(str(OUT) + '.stderr.txt').write_text(result.stderr)
    receipt = {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    start = result.stdout.find('{')
    if start >= 0:
        try:
            receipt['receipt'] = json.JSONDecoder().raw_decode(result.stdout[start:])[0]
        except json.JSONDecodeError:
            pass
    Path(str(OUT) + '.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(result.stdout[-9000:], flush=True)
    if result.stderr:
        print(result.stderr[-3000:], flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
