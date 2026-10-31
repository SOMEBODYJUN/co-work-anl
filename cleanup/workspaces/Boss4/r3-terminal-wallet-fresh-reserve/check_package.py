"""Validate frozen bytes, current artifact links and the separately recorded run.

This script does not execute any mathematical source program.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO = Path('/workspace/scratch/37f0f9248cfc/boss4-research')
STAGE = Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-terminal-wallet-fresh-reserve')
EVIDENCE = Path('archives/customer-attraction/tools/evidence/terminal-wallet-fresh-reserve-primary')
WORKSPACE = Path('cleanup/workspaces/Boss4/r3-terminal-wallet-fresh-reserve')
PRIMARY = ['30449824f9a39ec251e2','3beb17d5735520b90e84','53c66ec7d069d0a166ab','86f3b77f8de039cb76be','9da7c5510bd045b3d059']
DEPENDENCIES = ['a7579960b289fff40c97','ff1a437e39e730d230eb','be317a14860bf5650dfe']
COMPARISON = ['f811c6617841fee2c723','47b0b012b74895569094','5363963e01e403375246','c1f623cb38dd6c5c98ee','8c3c0850f65a2812d079','6b81f6445e9914b0b550','e34ee6479d87bca78052','c320561014ad69bbebf0','7cfd730044a42f607965','8b9cf44d16a024398ef3']
CURRENT_FULL = [
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/引理/实际末两人的查询税余量--引理.md',
 'archives/customer-attraction/state/引理/循环污染查询的加权调和付款--引理.md',
 'archives/customer-attraction/state/定理/末两人回复循环静态运输恒等式--定理.md',
 'archives/customer-attraction/state/定理/两主题笛卡尔根修复及成本下界--定理.md',
 'archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md',
 'archives/customer-attraction/state/反例/静态最优主题排列的冻结后缀失败--反例.md',
 'archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md',
 'archives/customer-attraction/state/计算/动态交换完整策略与assignment证书--计算.md',
 'archives/customer-attraction/state/引理/最优组合影价松弛与正损失替换停界--引理.md',
 'archives/customer-attraction/state/引理/最优元组跨角色零净损失替换门--引理.md',
 'archives/customer-attraction/state/计算/跨角色替换门原程序的依赖与精确复跑--计算.md',
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
    dump(EVIDENCE/'verification.json',dict(all_checks_passed=False,status='validation-in-progress'))
    inventory = {r['id']:r for r in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
    frozen = []
    for sid in PRIMARY + DEPENDENCIES + COMPARISON:
        row = inventory[sid]
        first = None
        locations = []
        for source in row['sources']:
            data = subprocess.check_output(['git','show',source['commit']+':'+source['path']],cwd=REPO,timeout=30)
            assert len(data)==row['size'] and digest(data)==row['sha256']
            if first is not None:
                assert data==first
            first = data
            locations.append(dict(source,bytes_verified=True))
        target=EVIDENCE/'original'/row['path']
        (STAGE/target).parent.mkdir(parents=True,exist_ok=True)
        (STAGE/target).write_bytes(first)
        role='primary' if sid in PRIMARY else ('runtime-dependency-only' if sid in DEPENDENCIES else 'comparison-only')
        frozen.append(dict(id=sid,role=role,read_scope='full-text',blob=row['blob'],size=row['size'],sha256=row['sha256'],sources=locations,saved_path=str(target)))
    current=[]
    for path in CURRENT_FULL+CURRENT_SCOPE_ONLY:
        data=(REPO/path).read_bytes()
        current.append(dict(path=path,sha256=digest(data),size=len(data),read_scope='full-text' if path in CURRENT_FULL else 'model-scope-and-status-passages-only'))
    dump(EVIDENCE/'source-manifest.json',dict(primary_count=len(PRIMARY),primary_bytes=sum(r['size'] for r in frozen if r['role']=='primary'),runtime_dependency_count=len(DEPENDENCIES),runtime_dependency_bytes=sum(r['size'] for r in frozen if r['role']=='runtime-dependency-only'),comparison_count=len(COMPARISON),comparison_bytes=sum(r['size'] for r in frozen if r['role']=='comparison-only'),frozen_sources=frozen,current_objects=current,claim_push='b6c14c398ab92125a2a9e07e41c6f6f374f3541e',source_program_execution='one original terminal-wallet main; no fresh/LP/padded-insurer run'))

    execution=json.loads((STAGE/EVIDENCE/'replay/execution.json').read_text())
    assert execution['executions_of_original_entrypoint']==1
    assert execution['exit_code']==0 and execution['generated_report_byte_identical_to_frozen']
    assert execution['input_and_code_bytes_unchanged']
    original_report=STAGE/EVIDENCE/'original'/inventory['53c66ec7d069d0a166ab']['path']
    generated=(STAGE/EVIDENCE/'replay/terminal_wallet_exact_audit.json').read_bytes()
    assert generated==original_report.read_bytes()
    assert digest(generated)==execution['generated_report_sha256']
    results=json.loads(generated)
    assert sum(v['complete_ordered_histories'] for v in results['cases'].values())==302
    assert sum(v['all_true_ic_including_self'] for v in results['cases'].values())==1812
    assert sum(len(v['rows']) for v in results['cases'].values())==12

    links=[]
    formal=sorted((STAGE/'archives/customer-attraction/state').rglob('*.md'))
    required=['id','kind','type_tag','title','status','summary','source_refs']
    for path in formal+[STAGE/EVIDENCE/'README.md']:
        content=path.read_text()
        if path in formal:
            assert content.startswith('---\n')
            front=content.split('---',2)[1]
            for key in required:
                assert re.search(r'^'+key+r':',front,re.M),(path,key)
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' in target or target.startswith('#'):
                continue
            target=target.split('#')[0]
            resolved=(path.parent/target).resolve()
            relative=resolved.relative_to(STAGE)
            exists=resolved.exists() or (REPO/relative).exists()
            links.append(dict(file=str(path.relative_to(STAGE)),target=target,resolves=exists))
            assert exists,(path,target)
        assert content.count('\\[')==content.count('\\]'),path
    receipts=json.loads((STAGE/WORKSPACE/'semantic-receipts.json').read_text())
    assert {r['id'] for r in receipts}==set(PRIMARY)
    for receipt in receipts:
        assert all(receipt[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        for target in receipt['targets']:
            assert (STAGE/target).exists() or (REPO/target).exists(),target
    report=dict(kind='artifact-structure-and-frozen-byte-validation',mathematical_programs_run=['audit_terminal_wallet.py: one isolated original main execution, recorded in replay/execution.json'],primary_originals_exact=True,both_frozen_locations_verified=True,formal_object_count=len(formal),receipt_count=len(receipts),local_link_count=len(links),links=links,recorded_execution_checked=True,all_checks_passed=True,mathematical_scope='Analytic reconstruction and limitations in self-review.md; original main checks 302 histories,1812 incl-self ICs and 12 terminal queries on two fixed certificates. No fresh, LP, insurer or HALF proof program run.')
    dump(EVIDENCE/'verification.json',report)
    print(json.dumps({k:report[k] for k in ['kind','primary_originals_exact','both_frozen_locations_verified','formal_object_count','receipt_count','local_link_count','all_checks_passed']},ensure_ascii=False))

if __name__=='__main__':
    main()
