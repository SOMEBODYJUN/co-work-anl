"""Serial standard binding/checking of exactly the reviewed Stage16 edges."""
from pathlib import Path
import subprocess
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def main():
    receipt = HERE/'stage16-edge-receipts.json'
    assert not receipt.exists()
    registration = json.loads((HERE/'stage16-register.stdout.json').read_text())
    assert registration['status'] == 'registered-local-not-pushed'
    summary = json.loads((HERE/'stage16-registration-summary.json').read_text())
    results = []
    for path in summary['edge_files_requiring_bind_check']:
        for action in ['edge-bind', 'edge-check']:
            cmd = ['python', 'work.py', 'research', action, path]
            if action == 'edge-bind':
                cmd.append('--write')
            result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
            prefix = HERE/('stage16-'+Path(path).stem+'-'+action)
            Path(str(prefix)+'.stdout.json').write_text(result.stdout)
            Path(str(prefix)+'.stderr.txt').write_text(result.stderr)
            if result.returncode:
                raise RuntimeError((path, action, result.stderr))
            results.append({'path': path, 'action': action, 'result': json.loads(result.stdout)})
            print(action+' '+Path(path).name+' PASS', flush=True)
    receipt.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
