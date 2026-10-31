"""Capture frozen text and validate artifact structure; no mathematical program run."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE = Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-cross-role-capacity')
EVIDENCE = Path('archives/customer-attraction/tools/evidence/cross-role-capacity-primary')
WORKSPACE = Path('cleanup/workspaces/Boss4/r3-cross-role-capacity')
PRIMARY = ['5324af15497c072261ab','7a47283b90da9d8af1bc','3ea81eb3459228c16b83','94f62b8bf6ed8c17630c','c458d6c7595f02da5781']
DEPENDENCIES = ['3beb17d5735520b90e84','a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']
COMPARISON = DEPENDENCIES + ['346725beb0701e526ca2','910786dd2c954cc709ed','78733bd2f46e1594dcfa','16da5e2c119023a56d73','2afc42441f977269bd33','9da7c5510bd045b3d059']
CURRENT_FULL = ['archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md', 'archives/customer-attraction/state/引理/同前缀行动平衡交换的半份约化成本界--引理.md', 'archives/customer-attraction/state/算法/固定进入槽的真实后继重放与一次势预算--算法.md', 'archives/customer-attraction/state/问题/真实重放协方差的定量付款--问题.md', 'archives/customer-attraction/state/引理/完整槽均值cap的原源范数账与付款接口--引理.md', 'archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md', 'archives/customer-attraction/state/障碍/真实分支替代与静态排列的量词缺口--障碍.md', 'archives/customer-attraction/state/计算/动态交换完整策略与assignment证书--计算.md', 'archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md', 'archives/customer-attraction/state/引理/最优组合影价松弛与正损失替换停界--引理.md']
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
        frozen.append(dict(id=source_id, role='primary' if source_id in PRIMARY else ('runtime-dependency-only' if source_id in DEPENDENCIES else 'comparison-only'), read_scope='full-text', blob=row['blob'], size=row['size'], sha256=row['sha256'], sources=locations, saved_path=str(target)))
    current = []
    for path in CURRENT_FULL + CURRENT_SCOPE_ONLY:
        data = (REPO/path).read_bytes()
        current.append(dict(path=path, sha256=digest(data), size=len(data), read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    manifest = dict(primary_count=len(PRIMARY), primary_bytes=sum(r['size'] for r in frozen if r['role']=='primary'), runtime_dependency_count=len(DEPENDENCIES), runtime_dependency_bytes=sum(r['size'] for r in frozen if r['role']=='runtime-dependency-only'), comparison_count=len(COMPARISON)-len(DEPENDENCIES), comparison_bytes=sum(r['size'] for r in frozen if r['role']=='comparison-only'), frozen_sources=frozen, current_objects=current, claim_push='a690454d202b50377916f5295bbc5ab1ce9f830f', no_source_programs=False)
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
    report = dict(kind='artifact-structure-and-frozen-byte-validation', mathematical_programs_run=['audit_cross_role_exchange.py: one isolated execution, recorded in replay/execution.json'], primary_originals_exact=True, both_frozen_locations_verified=True, formal_object_count=len(formal), receipt_count=len(receipts), local_link_count=len(links), links=links, all_checks_passed=True, mathematical_scope='Source reconstruction is recorded in self-review.md; original program execution is separately recorded and validates only two fixed-input COPY/GATE formulas, not complete SPE ICs, covariance payment, or HALF.')
    dump(EVIDENCE/'verification.json', report)
    print(json.dumps({k: report[k] for k in ['kind','primary_originals_exact','both_frozen_locations_verified','formal_object_count','receipt_count','local_link_count','all_checks_passed']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
