"""Replay both frozen implementations unchanged using ordinary dependency copies.

Run from any cwd.  This wrapper checks submitted reports and exact scalar slacks;
it is a replay/reconciliation, not a third independent mathematical audit.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = Path('research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    replay = HERE / 'replay'
    replay.mkdir(exist_ok=True)
    reports = {}
    with tempfile.TemporaryDirectory(prefix='capacity-replay-') as directory:
        root = Path(directory)
        inputs = {
            'five_player_indexed_bound.json': Path('evidence/certificates/customer_attraction/five_player_indexed_bound.json'),
            'binary_tail_exact_1999.json': Path('research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'),
        }
        for name, relative in inputs.items():
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / 'inputs' / name, target)
        for folder, stem in [('five_structure', 'audit_max_theme_root_capacity'),
                             ('five_aggregate', 'audit_capacity_independent')]:
            script = root / PREFIX / folder / (stem + '.py')
            script.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE / 'source' / (stem + '.py'), script)
            result = subprocess.run([sys.executable, str(script)], cwd=root,
                                    text=True, capture_output=True, check=True)
            assert not result.stderr, result.stderr
            stdout = result.stdout.encode()
            (replay / (stem + '.stdout.txt')).write_bytes(stdout)
            generated = script.with_suffix('.json')
            content = generated.read_bytes() if generated.exists() else stdout
            (replay / (stem + '.json')).write_bytes(content)
            original = HERE / 'original' / (stem + '.json')
            assert json.loads(content) == json.loads(original.read_bytes())
            assert content == original.read_bytes()
            reports[stem] = {'all_fields_equal': True, 'bytes_equal': True,
                             'sha256': sha(original), 'stderr_empty': True}

    O, u, K = F(83705,36641), F(8897,73282), F(16741,36641)
    raw = (F(83705,219736077), F(12500,219736077), F(641,36641))
    normalized = (2400*raw[0],1200*raw[1],raw[2])
    assert normalized == (F(66964000,73245359),F(5000000,73245359),F(641,36641))
    assert sum(normalized) == 1
    rows = [(1200,9097,3497),(1200,3100,15491),
            (1200,-2897,33482),(600,-4447,28735)]
    slacks = [ks*K+us*u-left*O for left,ks,us in rows]
    assert all(s >= 0 for s in slacks)
    report = {'scope': 'unchanged original implementation replay; exact report reconciliation, not a new independent audit',
              'original_reports': reports,
              'dependencies': {p.name: {'sha256':sha(p),'bytes':p.stat().st_size}
                               for p in sorted((HERE/'inputs').glob('*.json'))},
              'scalar_row_slacks': list(map(str,slacks)),
              'scalar_domain_slacks': {'u-K/5':str(u-K/5),'K-u':str(K-u),'W-K':str(1-K)},
              'raw_dual': list(map(str,raw)),
              'normalized_dual': list(map(str,normalized)),
              'dual_normalizations_reconciled': True}
    (replay/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
