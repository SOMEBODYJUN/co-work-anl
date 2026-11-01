"""Static delivery check only: no source import, mathematical audit, or LP."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parent
R = P.parents[4]
manifest = json.loads((P/'source-manifest.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
hashes = 0
for rec in manifest['artifacts']:
    p = R/rec['path']
    assert p.is_file() and p.stat().st_size == rec['bytes']
    assert sha(p) == rec['sha256'], p
    hashes += 1
comparison = json.loads((P/'comparison.json').read_text())
for rec in comparison['records']:
    p = R/rec['path']
    assert p.is_file() and sha(p) == rec['sha256'], p
    assert rec['full_text_read']
    hashes += 1
jsons = 0
asts = 0
for p in P.rglob('*'):
    if p.suffix == '.json' and p.name != 'self-check.json':
        json.loads(p.read_text()); jsons += 1
    elif p.suffix == '.py':
        ast.parse(p.read_text()); asts += 1
raw = gzip.decompress((P/'original-event/capture.json.gz').read_bytes())
cap = json.loads(raw)
event = json.loads((P/'original-event/execution.json').read_text())
assert hashlib.sha256(raw).hexdigest() == event['capture_uncompressed_sha256']
assert len(cap['A']) == len(cap['b']) == len(cap['types']) == 4064
assert len(cap['names']) == 76 and all(len(row)==76 for row in cap['A'])
assert event['counts'] == {'build':1,'mixed_coeffs':1,'linprog':2}
assert event['exit_code']==0 and event['res_status']==2 and event['sep_status']==0
audit = json.loads((P/'contract-audit.json').read_text())
assert audit['status']=='PASS' and audit['captured_coefficients_compared']==308864
assert audit['simple_exact_separator']['target']=='-1/6'
assert audit['simple_exact_separator']['profile_is_SPE'] is False
assert len(audit['simple_exact_separator']['support'])==21
assert len(audit['simple_exact_separator']['literal_row_averages'])==76
assert len(audit['simple_exact_separator']['equal_share_row_averages'])==76
assert (P/'audit-stderr.txt').stat().st_size==0
assert (P/'original-event/stderr.txt').stat().st_size==0
receipt = json.loads((R/manifest['receipt']).read_text())
assert receipt['id']==manifest['source']['id']
for flag in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
    assert receipt[flag] is True
for target in receipt['targets']:
    p = R/target
    assert p.is_file() or p == P/'self-check.json', p
links = 0
for file in [R/manifest['object'],P/'README.md']:
    text = file.read_text()
    for link in re.findall(r'\]\(([^)\n]+)\)',text):
        if '://' in link or link.startswith('#'):
            continue
        assert (file.parent/link.split('#',1)[0]).resolve().exists(), (file,link)
        links += 1
result = {'status':'PASS','identity':'static package check; not a second mathematical run',
          'sha256_checks':hashes,'json_parses':jsons,'gzip_json_parses':1,'python_AST_parses':asts,
          'markdown_links_checked':links,'receipt_targets_checked':len(receipt['targets']),
          'original_main_calls':0,'original_helpers':0,'LP_calls':0,'mathematical_audit_calls':0}
(P/'self-check.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False))
