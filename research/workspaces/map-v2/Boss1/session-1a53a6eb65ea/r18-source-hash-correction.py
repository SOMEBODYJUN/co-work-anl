"""Correct one truncated source hash after preserving the in-flight core draft.

The source mathematics, frozen code/output and registered mathematical contract
remain unchanged. The source-body reference and its baseline advance together.
"""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

ROOT = Path.cwd()
OUT = ROOT / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
sys.path.insert(0, str(ROOT / 'tools'))
import research_runtime as rr


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


tid = 'customer-attraction-3a-3a-d9b971ecd9ba54c7'
task = read(ROOT / 'research/operations/map-v2/tasks' / (tid + '.json'))
assert task['state'] == 'handoff' and task.get('owner') is None, tid
oid = 'customer-attraction/R18-rent-correction-search'
path = 'archives/customer-attraction/state/审查/R18租金修正搜索正确来源--审查.md'
old_sha = 'f9dd8f2ef7d35ceaf35fd865356ae1223c636fb7fc21a7aac1c051e087371ab7'
old_literal = '02d38231c6ff2731c5253fd0eabf212c2d0cf53a85c7865e'
new_literal = '02d382a9b52110f3b4b70231c6ff2731c5253fd0eabf212c2d0cf53a85c7865e'
source_path = ROOT / path
assert sha(source_path) == old_sha
source_text = source_path.read_text()
assert source_text.count(old_literal) == 1
code = ROOT / 'archives/customer-attraction/tools/evidence/R18-dynamic-one-rent-correction/rent_correction_search.py'
manifest = code.parent / 'manifest.json'
assert code.stat().st_size == 1376 and sha(code) == new_literal
assert read(manifest)['source_sha256'] == new_literal

regpath = ROOT / 'research/registry.json'
reg = read(regpath)
before_registry_sha = sha(regpath)
old_baseline = copy.deepcopy(reg['baseline'])
basepath = ROOT / old_baseline['path']
assert sha(basepath) == old_baseline['sha256']
baseline = read(basepath)
objects = {o['object_id']: o for o in reg['objects']}
before = copy.deepcopy(objects[oid])
assert before['version'] == 2 and before['body'] == {'path': path, 'sha256': old_sha}
affected = [o['object_id'] for o in reg['objects']
            if any(ref['path'] == path for ref in [o['body'], *o['evidence']])]
assert affected == [oid], affected
for rows in [reg['materials'], baseline['materials']]:
    hits = [x for x in rows if x['path'] == path]
    assert len(hits) == 1 and hits[0]['sha256'] == old_sha

source_path.write_text(source_text.replace(old_literal, new_literal))
new_sha = sha(source_path)
assert source_path.read_text().replace(new_literal, old_literal) == source_text
objects[oid]['body']['sha256'] = new_sha
objects[oid]['version'] = 3
objects[oid]['objections'] += (
    ' 本轮仅将正文抄录的主程序SHA补全为实际1376字节代码及manifest共同给出的64位值；'
    '原数学陈述、量词、12类型固定输入、精确收益与冻结浮点输出均不变。'
    '前述双精度/未夹逼描述保留原冻结证据的历史范围，本轮新增的短有理夹逼另见构图数学复核。'
)
for key in ['title', 'kind', 'truth_status', 'model', 'statement', 'quantifiers', 'assumptions', 'scope', 'evidence', 'sources']:
    assert objects[oid][key] == before[key], key
for rows in [reg['materials'], baseline['materials']]:
    next(x for x in rows if x['path'] == path)['sha256'] = new_sha

newbase = ROOT / 'research/registration/baseline-boss1-r18-source-hash-20261112.json'
assert not newbase.exists()
baseline['coverage_note'] = baseline.get('coverage_note', '') + '；Boss1仅补全R18正文抄录漏串的主程序SHA，保数学合同和全部冻结科学字节。'
baseline['commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
save(newbase, baseline)
reg['baseline'] = {'path': newbase.relative_to(ROOT).as_posix(), 'sha256': sha(newbase)}
proposal = OUT / 'r18-source-hash-proposed.json'
save(proposal, reg)
result = subprocess.run([sys.executable, 'work.py', 'research', 'register', '--record-file', proposal.relative_to(ROOT).as_posix()], capture_output=True, text=True)
print(result.stdout, end='')
print(result.stderr, end='')
if result.returncode:
    raise SystemExit(result.returncode)
proposal.unlink()
audit = {
    'status': 'registered-local-not-pushed', 'reviewer': 'Boss1',
    'preserved_task': tid, 'before_registry_sha256': before_registry_sha,
    'after_registry_sha256': sha(regpath), 'old_baseline': old_baseline,
    'new_baseline': reg['baseline'], 'path': path, 'old_sha256': old_sha,
    'new_sha256': new_sha, 'old_literal': old_literal, 'new_literal': new_literal,
    'verified_source': {'path': code.relative_to(ROOT).as_posix(), 'sha256': sha(code), 'bytes': code.stat().st_size},
    'verified_manifest': {'path': manifest.relative_to(ROOT).as_posix(), 'sha256': sha(manifest)},
    'before_object': before, 'after_object': objects[oid],
    'old_object_pin': rr.pin(before), 'new_object_pin': rr.pin(objects[oid]),
    'mathematical_contract_changed': False, 'scientific_runs': 0,
    'remaining': 'Native same-ID refresh and fresh-worker continuation from the preserved nine-core mathematical delivery; all other in-flight batches continue.'
}
save(OUT / 'r18-source-hash-correction.json', audit)
print(json.dumps({'status': audit['status'], 'object_id': oid, 'object_pin': audit['new_object_pin'], 'source_sha256': new_sha, 'baseline': reg['baseline']}, ensure_ascii=False))
