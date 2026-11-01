"""Replay each frozen entry mode once, outside the clone; retain exact patches.

New cleanup orchestration, not part of the frozen mathematical generator.
The exclusive rerun directory prevents accidental evidence replacement.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'work.py').is_file())
SHARED = HERE.parent / 'full156-tail-parent-report/original/research_5'
PAIR = HERE.parent / 'full156-pair-master-point/original/pair_master_exact.json'
INPUTS = {
    'full156_tail2_kernel.py': (HERE / 'original/full156_tail2_kernel.py', 'f84aa1a54ffba718b2f77ad65fb0f79c9ba2690fde75a5d84c53d5eb913cdc0c'),
    'combined_branch_master_exact.json': (SHARED / 'combined_branch_master_exact.json', 'd1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8'),
    'pair_master_exact.json': (PAIR, '090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2'),
}
OUTPUTS = {
    'full156_tail2_kernel_10344.json': '876f063e9e88679c8803011775b04a4b707b8b586dfd3a840fd056f9ddcef3d4',
    'full156_tail2_welfare_10344.json': 'fe8fb09f7527f8f4cd26ad67f6e43be5bc84cb5d9c47fea39fd0661bab0e5256',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    assert sys.flags.optimize == 0, 'Assertions must remain enabled'
    source_rows = []
    for name, (path, expected) in INPUTS.items():
        data = path.read_bytes()
        assert sha(data) == expected
        source_rows.append({'name': name, 'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': expected})
    for name, expected in OUTPUTS.items():
        assert sha((SHARED / name).read_bytes()) == expected
    out = HERE / 'rerun'
    out.mkdir(exist_ok=False)
    temp = Path(tempfile.mkdtemp(prefix='full156-kernel-original-', dir=ROOT.parent))
    execution = {'scope': 'one unmodified default run and one unmodified --with-welfare run; no LP solve',
                 'started_utc': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
                 'executable': sys.executable, 'assertions_enabled': True, 'temporary_cwd': str(temp),
                 'inputs': source_rows, 'runs': [], 'temporary_directory_removed': False}
    try:
        for name, (path, _) in INPUTS.items():
            shutil.copyfile(path, temp / name)
        for mode, args in [('default', []), ('with-welfare', ['--with-welfare'])]:
            argv = [sys.executable, '-B', str(temp / 'full156_tail2_kernel.py'), *args]
            start = time.monotonic()
            result = subprocess.run(argv, cwd=temp, capture_output=True, check=False)
            elapsed = time.monotonic() - start
            (out / (mode + '.stdout.txt')).write_bytes(result.stdout)
            (out / (mode + '.stderr.txt')).write_bytes(result.stderr)
            row = {'mode': mode, 'argv': argv, 'cwd': str(temp), 'exit_code': result.returncode,
                   'wall_seconds': elapsed, 'stdout_bytes': len(result.stdout), 'stdout_sha256': sha(result.stdout),
                   'stderr_bytes': len(result.stderr), 'stderr_sha256': sha(result.stderr)}
            execution['runs'].append(row)
            write_json(out / 'execution.json', execution)
            assert result.returncode == 0, row
        comparisons = []
        generated_kernel_sha = sha((temp / 'full156_tail2_kernel_10344.json').read_bytes())
        for name, old_sha in OUTPUTS.items():
            old_bytes, new_bytes = (SHARED / name).read_bytes(), (temp / name).read_bytes()
            old, new = json.loads(old_bytes), json.loads(new_bytes)
            assert list(old) == list(new)
            changed = {key: {'frozen': old[key], 'rerun': new[key]} for key in old if old[key] != new[key]}
            allowed = {'seconds'} if 'kernel' in name else {'kernel_sha256'}
            assert set(changed) <= allowed, (name, list(changed))
            if 'welfare' in name:
                assert new['kernel_sha256'] == generated_kernel_sha
            # Verify that these small top-level patches recover the exact output bytes.
            restored = dict(old)
            restored.update({key: v['rerun'] for key, v in changed.items()})
            assert (json.dumps(restored, indent=2) + '\n').encode() == new_bytes
            comparisons.append({'filename': name, 'frozen_path': str((SHARED / name).relative_to(ROOT)),
                'frozen_bytes': len(old_bytes), 'frozen_sha256': old_sha,
                'rerun_bytes': len(new_bytes), 'rerun_sha256': sha(new_bytes),
                'fields': len(old), 'equal_fields': [key for key in old if old[key] == new[key]],
                'changed_fields': changed, 'mathematical_fields_equal': True,
                'exact_bytes_reconstructible_from_frozen_plus_patch': True})
        for name, (path, expected) in INPUTS.items():
            assert sha(path.read_bytes()) == sha((temp / name).read_bytes()) == expected
        for name, expected in OUTPUTS.items():
            assert sha((SHARED / name).read_bytes()) == expected
        write_json(out / 'comparison.json', {'scope': 'all top-level fields and every nested matrix element compared exactly',
            'payoff_scalar_entries_equal': 156 + 2 * 156**2, 'welfare_scalar_entries_equal': 156**2,
            'outputs': comparisons, 'input_bytes_unchanged': True,
            'large_outputs_retention': 'Exact frozen files plus byte-reconstruction patches; duplicate large matrices removed.'})
        execution['finished_utc'] = datetime.now(timezone.utc).isoformat()
        execution['all_checks_passed'] = True
    finally:
        shutil.rmtree(temp)
        execution['temporary_directory_removed'] = True
        write_json(out / 'execution.json', execution)
    print(json.dumps({'status': 'PASS', 'runs': len(execution['runs']), 'comparison': str(out / 'comparison.json')}))


if __name__ == '__main__':
    main()
