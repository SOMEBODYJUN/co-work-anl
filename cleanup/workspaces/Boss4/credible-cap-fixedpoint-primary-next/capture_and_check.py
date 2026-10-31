"""Capture frozen text and validate artifact structure; no mathematical program run."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE = Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/credible-cap-fixedpoint-primary-next')
EVIDENCE = Path('archives/customer-attraction/tools/evidence/credible-cap-fixedpoint-primary')
WORKSPACE = Path('cleanup/workspaces/Boss4/credible-cap-fixedpoint-primary-next')
PRIMARY = ['16da5e2c119023a56d73', '3c1727fd6999135f2732', '24072a6e5b7a57d21326', 'bd11d0a038fe1e453429', '82b52a07559128d36d23']
COMPARISON = ['b98ed5f000945f0e87b0', 'cdc4e5c3adb365ba0ad6', '69fd1ae65a4287092175', '305ad98b11c8a485cf60', '9c30c2796b1bd2d10286', '89f691dd5f3db0d80ba6', '52bf7b08dfaf1c4994d9', 'c73f84162625abb1b9a1', 'c65d6c6caec06eac291a', '5fb577eec293372a3ad5', '908be8a7065a9b58786f']
CURRENT_FULL = [
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md',
 'archives/customer-attraction/state/算法/固定进入槽的真实后继重放与一次势预算--算法.md',
 'archives/customer-attraction/state/问题/真实重放协方差的定量付款--问题.md',
 'archives/customer-attraction/state/引理/同前缀行动平衡交换的半份约化成本界--引理.md',
 'archives/customer-attraction/state/引理/规范门槛均值域与复制偏离的精确成本--引理.md',
 'archives/customer-attraction/state/引理/完整槽均值cap的原源范数账与付款接口--引理.md',
]
CURRENT_SCOPE_ONLY = [
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md',
 'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
]

def dump(path, obj):
    (STAGE / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    inventory = {r['id']: r for r in map(json.loads, (REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    frozen = []
    for source_id in PRIMARY + COMPARISON:
        row = inventory[source_id]
        first_data = None
        locations = []
        for source in row['sources']:
            data = subprocess.check_output(['git', 'show', source['commit'] + ':' + source['path']], cwd=REPO, timeout=30)
            if first_data is None:
                first_data = data
            assert data == first_data
            assert len(data) == row['size'] and digest(data) == row['sha256']
            locations.append(dict(source, bytes_verified=True))
        target = EVIDENCE / 'original' / row['path']
        (STAGE / target).parent.mkdir(parents=True, exist_ok=True)
        (STAGE / target).write_bytes(first_data)
        frozen.append(dict(id=source_id, role='primary' if source_id in PRIMARY else 'comparison-only', read_scope='full-text', blob=row['blob'], size=row['size'], sha256=row['sha256'], sources=locations, saved_path=str(target)))
    current = []
    for path in CURRENT_FULL + CURRENT_SCOPE_ONLY:
        data = (REPO/path).read_bytes()
        current.append(dict(path=path, sha256=digest(data), size=len(data), read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    manifest = dict(primary_count=len(PRIMARY), primary_bytes=sum(r['size'] for r in frozen if r['role']=='primary'), comparison_count=len(COMPARISON), comparison_bytes=sum(r['size'] for r in frozen if r['role']=='comparison-only'), frozen_sources=frozen, current_objects=current, claim_push='aeabaf99880a2756189919c8fa1135bdb6d970ac', no_source_programs=True)
    dump(EVIDENCE/'source-manifest.json', manifest)
    links = []
    formal = sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'))
    for path in formal + [STAGE/EVIDENCE/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#')[0]
            resolved = (path.parent/target).resolve()
            rel = resolved.relative_to(STAGE)
            exists = resolved.exists() or (REPO/rel).exists()
            links.append(dict(file=str(path.relative_to(STAGE)), target=target, resolves=exists))
            assert exists, (path, target)
        assert path.read_text().count('\\[') == path.read_text().count('\\]')
    receipts = json.loads((STAGE/WORKSPACE/'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts} == set(PRIMARY)
    for receipt in receipts:
        assert all(receipt[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in receipt['targets']:
            assert (STAGE/target).exists() or (REPO/target).exists()
    report = dict(kind='artifact-structure-and-frozen-byte-validation', mathematical_programs_run=[], primary_originals_exact=True, both_frozen_locations_verified=True, formal_object_count=len(formal), receipt_count=len(receipts), local_link_count=len(links), links=links, all_checks_passed=True, mathematical_scope='Human semantic reconstruction is recorded in self-review.md; these checks do not prove covariance payment or HALF.')
    dump(EVIDENCE/'verification.json', report)
    print(json.dumps({k: report[k] for k in ['kind','primary_originals_exact','both_frozen_locations_verified','formal_object_count','receipt_count','local_link_count','all_checks_passed']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
