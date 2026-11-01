"""Static closure only: never imports the scientific sources or reruns a solver."""
import ast
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
REPO = next(p for p in BASE.parents if (p / 'cleanup/inventory.jsonl').exists())

def digest(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    manifest = json.loads((BASE / 'source-manifest.json').read_text())
    for rec in manifest['sources']:
        p = REPO / rec['stored_path']
        assert digest(p) == {'bytes': rec['size'], 'sha256': rec['sha256']}
        b = p.read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == rec['blob']
    bindings = manifest['artifacts'] + manifest['comparisons']
    for item in bindings:
        assert digest(REPO / item['path']) == {'bytes': item['bytes'], 'sha256': item['sha256']}, item['path']
    files = [REPO / x['path'] for x in manifest['artifacts']]
    parsed_json = parsed_python = 0
    for p in files + [BASE / 'source-manifest.json']:
        if p.suffix == '.json':
            json.loads(p.read_text()); parsed_json += 1
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p)); parsed_python += 1
    links = []
    for p in files:
        if p.suffix != '.md':
            continue
        for rel in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' in rel or rel.startswith('#'):
                continue
            target = (p.parent / rel.split('#')[0]).resolve()
            assert target.exists(), (p, rel)
            links.append(str(target.relative_to(REPO)))
    target_count = 0
    for sid in ('b16b0b18ac6abe5ff042', 'bc18e283c26c602f71bc'):
        receipt = json.loads((REPO / 'cleanup/workspaces/Boss7/receipts-round19' / (sid + '.json')).read_text())
        for target in receipt['targets']:
            assert (REPO / target).exists(), target
            target_count += 1
    cap = json.loads((BASE / 'replay/capture.json').read_text())
    exact = json.loads((BASE / 'exact-audit.json').read_text())
    assert exact['capture_sha256'] == digest(BASE / 'replay/capture.json')['sha256']
    assert exact['audit_script_sha256'] == digest(BASE / 'audit_exact.py')['sha256']
    event = json.loads((BASE / 'replay/execution.json').read_text())
    assert event['observer'] == digest(BASE / 'run_observed.py')
    assert event['LP_calls'] == 2 and event['default_main_calls'] == 0
    assert len(cap) == 2 and [x['beta'] for x in exact['results']] == ['1418/721', '17323/8992']
    attempts = json.loads((BASE / 'exact-audit-attempts.json').read_text())
    assert attempts['original_function_repeats'] == attempts['LP_repeats'] == 0
    result = {'status': 'PASS', 'mathematics_executed': False, 'primary_sources': len(manifest['sources']), 'artifact_bindings': len(manifest['artifacts']), 'comparison_bindings': len(manifest['comparisons']), 'JSON_parsed': parsed_json, 'Python_AST_parsed': parsed_python, 'actual_local_links': len(links), 'receipt_targets_checked': target_count, 'original_LP_calls_unchanged': 2, 'exact_audit_successful_output_bound': True}
    (BASE / 'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
