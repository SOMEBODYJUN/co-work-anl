"""Structural delivery checks only; never imports or runs the mathematical sources."""
from pathlib import Path
import argparse, ast, hashlib, json, re

parser = argparse.ArgumentParser()
parser.add_argument('--comparison-root', type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent
root = base.parents[4]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = json.loads((base/'source-manifest.json').read_text())['primary']
deps = json.loads((base/'dependency-manifest.json').read_text())['dependencies']
for rec in sources + deps:
    path = root/rec['saved_as']
    assert path.stat().st_size == rec['size'], str(path)
    assert digest(path) == rec['sha256'], str(path)
    if path.suffix == '.py':
        ast.parse(path.read_text(), filename=str(path))
for rec in sources:
    normal = json.loads((base/rec['normal_show_receipt']).read_text())['source']
    for field in ('id', 'path', 'size', 'sha256', 'blob', 'sources'):
        assert normal[field] == rec[field], (rec['id'], field)

event = json.loads((base/'native-regression/execution.json').read_text())
stdout = base/'native-regression/stdout.json'
stderr = base/'native-regression/stderr.txt'
assert event['returncode'] == 0 and stderr.read_bytes() == b''
assert digest(stdout) == event['stdout_sha256']
assert digest(stderr) == event['stderr_sha256']
assert event['script_sha256'] == sources[2]['sha256']
assert event['input_sha256'] == next(x['sha256'] for x in deps if x['path'].endswith('individual_security_failure.json'))
report = json.loads(stdout.read_text())
assert report['source_sha256'] == event['input_sha256']
assert report['nodes'] == 43 and report['IC_comparisons_including_self'] == 258

markdowns = list(base.glob('*.md')) + list((root/'archives/customer-attraction/state/程序').glob('*.md'))
links = 0
for md in markdowns:
    for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', md.read_text()):
        dest = dest.split('#')[0]
        if not dest or '://' in dest:
            continue
        target = (md.parent/dest).resolve()
        if not target.exists():
            assert args.comparison_root, ('missing link without comparison root', str(target))
            target = args.comparison_root/target.relative_to(root)
        assert target.exists(), (str(md), dest)
        links += 1
result = {
    'status': 'PASS',
    'primary_files': len(sources), 'primary_bytes': sum(x['size'] for x in sources),
    'dependencies': len(deps), 'local_links_checked': links,
    'native_regression_events': 1,
    'matching_native_runs': 0, 'canonical_solver_runs': 0, 'LP_runs': 0,
    'scope': 'byte identity, AST parse, source receipts, links and execution bindings only; no mathematical replay by this checker'
}
(base/'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False))
