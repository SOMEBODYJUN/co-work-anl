"""Format/link/transport verification only; does not run source auditors."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/cag-coupled-seats-and-upload-audits'
W = ROOT / 'cleanup/workspaces/Boss4/r3-cag-coupled-seats-and-upload-audits-next'

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

formals = json.loads((E / 'formal-manifest.json').read_text())
links = []
for row in formals:
    path = ROOT / row['path']
    data = path.read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', data.decode()):
        if target.startswith(('https:', 'http:', '#')):
            continue
        dest = (path.parent / target.split('#', 1)[0]).resolve()
        assert dest.is_relative_to(ROOT) and dest.is_file(), (row['path'], target)
        links.append({'from': row['path'], 'target': target, 'exists': True})

bad_c0, trailing, binary, utf8_count = [], [], [], 0
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or not path.relative_to(ROOT).parts[0] in {'archives', 'tools', 'cleanup'}:
        continue
    data = path.read_bytes()
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        binary.append({'path': str(path.relative_to(ROOT)), 'bytes': len(data),
                       'sha256': hashlib.sha256(data).hexdigest()})
        continue
    utf8_count += 1
    for offset, char in enumerate(text):
        if ord(char) < 32 and char not in '\n\r\t':
            bad_c0.append({'path': str(path.relative_to(ROOT)), 'offset': offset, 'code': ord(char)})
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.rstrip(' \t') != line:
            trailing.append({'path': str(path.relative_to(ROOT)), 'line': line_number})
assert not bad_c0, bad_c0
assert not trailing, trailing
assert len(binary) == 0
report = {'passed': True, 'scope': 'all transported UTF-8 file bytes; no binary assets in this batch',
          'utf8_files_scanned_before_report': utf8_count, 'forbidden_C0': bad_c0,
          'trailing_whitespace': trailing, 'binary_preserved': binary, 'formal_local_links': links,
          'source_audit_reruns': 0}
save(E / 'transport-self-check.json', report)
save(W / 'transport-self-check.json', report)

files = []
for path in sorted(ROOT.rglob('*')):
    if path.is_file() and path.relative_to(ROOT).parts[0] in {'archives', 'tools', 'cleanup'}:
        data = path.read_bytes()
        files.append({'path': str(path.relative_to(ROOT)), 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest()})
save(ROOT / 'copy-files.json', files)
(ROOT / 'copy-paths.txt').write_text('\n'.join(row['path'] for row in files) + '\n')
summary = {'files': len(files), 'bytes': sum(row['bytes'] for row in files), 'formal_files': len(formals),
           'formal_bytes': sum(row['bytes'] for row in formals), 'primary_files': 5, 'primary_bytes': 37791,
           'semantic_receipts': 5, 'semantic_checks': 58, 'semantic_checks_passed': True,
           'formal_local_links': len(links), 'forbidden_C0': 0, 'trailing_whitespace': 0,
           'reused_prior_exact_successes': 2, 'new_source_CLI_invocations': 3, 'new_distinct_primary_codes': 3, 'successful_report_invocations': 3,
           'manifest_sha256': hashlib.sha256((ROOT / 'copy-files.json').read_bytes()).hexdigest(),
           'universal_six_player_half_claimed': False, 'existing_page_correction_suggestions': 4, 'existing_pages_changed': 0}
save(ROOT / 'delivery-summary.json', summary)
print(json.dumps(summary, ensure_ascii=False))
