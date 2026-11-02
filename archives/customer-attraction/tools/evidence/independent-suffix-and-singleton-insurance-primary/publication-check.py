"""Read-only publication structure checks. No solver or original entry runs."""
import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
args = parser.parse_args()
REPO = args.repo.resolve()
OVERLAY = HERE.parents[4]

def read_json(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def resolve_rel(path):
    local = OVERLAY / path
    return local if local.is_file() else REPO / path

manifest = read_json(HERE / 'source-manifest.json')
assert len(manifest) == 3
for rec in manifest:
    path = resolve_rel(rec['preserved_path'])
    assert path.stat().st_size == rec['size']
    assert sha(path) == rec['sha256']
    assert rec['full_file_reviewed'] is True
    assert len(rec['sources']) == 2
assert sum(r['size'] for r in manifest) == 6589

for rec in read_json(HERE / 'comparison-bindings.json'):
    path = REPO / rec['path']
    assert path.stat().st_size == rec['size'] and sha(path) == rec['sha256'], rec['path']
dep = read_json(HERE / 'dependency-binding.json')
assert sha(REPO / dep['preserved_existing_path']) == dep['sha256']
payload = read_json(REPO / dep['preserved_existing_path'])
assert list(payload) == dep['top_level_keys']
rows = payload['policy']
histories = [tuple(r['history']) for r in rows]
assert len(rows) == len(set(histories)) == 91
assert [sum(len(h) == depth for h in histories) for depth in range(3)] == [1, 9, 81]

frozen = next(resolve_rel(r['preserved_path']) for r in manifest if r['id'] == '4460c37d26ffeb1317f0')
report = read_json(frozen)
assert list(report) == ['scope', 'decision_histories', 'all_action_comparisons', 'minimum_slack', 'actual_path', 'actual_payoffs', 'actual_W', 'component_L_B', 'component_barL_B', 'product_L_BB', 'forced_BB_path', 'forced_BB_payoffs']
assert len(report) == 12
assert [report[k] for k in ['decision_histories', 'all_action_comparisons', 'minimum_slack', 'actual_W', 'component_L_B', 'component_barL_B', 'product_L_BB']] == [91, 819, '0', 10, '3/2', '5/4', '5/2']
assert report['actual_path'] == ['CC', 'AA', 'BB'] and report['actual_payoffs'] == ['4', '3', '3']
assert report['forced_BB_path'] == ['BB', 'BC', 'CA'] and report['forced_BB_payoffs'] == ['5/2', '3', '9/2']
assert 'OPT' not in report and 'certificate_sha256' not in report
for name in ['review-product-transfer-generated.json', 'review-product-transfer-stdout.json']:
    assert (HERE / 'current-replay' / name).read_bytes() == frozen.read_bytes()
assert not (HERE / 'current-replay/review-product-transfer-stderr.txt').read_bytes()
event = read_json(HERE / 'current-replay/execution.json')
assert event['exit_code'] == 0 and event['stderr_bytes'] == 0
assert event['stdout_bytes'] == 545 and event['generated_byte_equal_frozen'] is True and event['stdout_byte_equal_generated'] is True
assert event['coupled_diagnostic_entry_executions'] == 0
assert event['frozen_report_sha256'] == event['generated_report_sha256'] == event['stdout_sha256'] == sha(frozen)

receipts = read_json(HERE / 'source-dispositions.json')
assert {r['id'] for r in receipts} == {r['id'] for r in manifest}
for rec in receipts:
    assert all(rec[k] is True for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
    assert all(rec[k] for k in ['read_note', 'comparison_note', 'decision_note'])
    for target in rec['targets']:
        assert resolve_rel(target).is_file(), target

object_path = resolve_rel('archives/customer-attraction/state/程序/双副本全续局递推与单点资源保险诊断--程序.md')
links = 0
for page in [HERE / 'README.md', object_path]:
    for raw in re.findall(r'\]\(([^)]+)\)', page.read_text()):
        if '://' in raw or raw.startswith('#'):
            continue
        target = raw.split('#', 1)[0]
        local = (page.parent / target).resolve()
        if local.is_file():
            links += 1
            continue
        relative = local.relative_to(OVERLAY)
        assert (REPO / relative).is_file(), (page, raw)
        links += 1
print(json.dumps({'status': 'PASS', 'source_count': 3, 'source_bytes': 6589, 'comparison_files': 15, 'receipt_count': 3, 'local_links_checked': links, 'new_source_entry_executions_by_this_checker': 0, 'mathematical_proof_by_this_checker': False}, ensure_ascii=False, indent=2))
