"""Only source identity, links, syntax and receipt; no mathematics is executed."""
import ast
import hashlib
import json
from pathlib import Path
import re

E = Path(__file__).resolve().parent
A, R = E.parents[2], E.parents[4]
body = A/'state/资源/固定背景共同客户回路的适用范围与接续--资源.md'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
dump = lambda p,x: p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
inventory = [json.loads(s) for s in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
primary = next(x for x in inventory if x['id']=='e6d7ff01cc1b00450a9e')
original = A/'tools/evidence/fixed-policy-circuit-flow/original/common_customer_README.md'
assert original.stat().st_size == primary['size'] == 1209 and sha(original) == primary['sha256']
assert original.read_bytes() == Path('/workspace/scratch/c0ab78c47566/r17-common-customer-README.md').read_bytes()
related = [
    'tools/evidence/fixed-background-circuit-basis/original/fixed_background_circuit_basis.md',
    'tools/evidence/fixed-background-circuit-basis/related/fixed_background_rank_review.md',
    'tools/evidence/fixed-background-circuit-basis/related/check_fixed_background_rank.py',
    'tools/evidence/fixed-background-circuit-basis/related/fixed_background_rank_review.json',
    'tools/evidence/fixed-background-circuit-audit-program/original/audit_fixed_background.py',
    'tools/evidence/fixed-policy-circuit-flow/original/circuit_flow_probe.py',
    'tools/evidence/fixed-policy-circuit-flow/original/circuit_flow_certificate.json',
]
sources = []
for rel in related:
    p = A/rel
    matches = [x for x in inventory if x['sha256'] == sha(p) and x['size'] == p.stat().st_size]
    assert matches, rel
    sources.append({'saved_path':str(p.relative_to(R)), 'inventory_sources':matches, 'full_file_reviewed':True})
    if p.suffix == '.py': ast.parse(p.read_text())
    if p.suffix == '.json': json.loads(p.read_text())
stable = [
    'state/定义/共同目录完整历史模型--定义.md',
    'state/定理/共同客户收益的正边际与平衡贡献--定理.md',
    'state/定理/固定完整策略的二主题耦合二倍界--定理.md',
    'state/障碍/共同有符号客户的全局三标签耦合缺口--障碍.md',
    'state/引理/第三主题占位的七收益补偿恒等式--引理.md',
    'state/引理/固定前缀正二主题电路的旧人租金误差--引理.md',
]
current = [
    'state/定理/固定背景双主题收益切片的完整有理回路--定理.md',
    'state/程序/固定背景收益切片的有理秩与核基审计程序--程序.md',
    'state/计算/固定背景收益切片的有限秩与核基审计--计算.md',
]
events = ['tools/evidence/fixed-background-circuit-audit-program/replay/execution.json',
          'tools/evidence/fixed-background-circuit-audit-program/replay/process-capture.json']
for rel in events: json.loads((A/rel).read_text())
manifest = {'primary':primary | {'saved_path':str(original.relative_to(R)), 'full_file_reviewed':True},
    'original_related_full_read':sources,
    'stable_comparisons_full_read':[{'path':str((A/p).relative_to(R)), 'bytes':(A/p).stat().st_size,
                                   'sha256':sha(A/p)} for p in stable],
    'same_batch_comparisons_read_not_content_hash_bound':[str((A/p).relative_to(R)) for p in current],
    'shared_author_event_read_not_reexecuted':[{'path':str((A/p).relative_to(R)), 'sha256':sha(A/p)} for p in events],
    'own_original_program_rank_LP_BI_or_new_numeric_scan_calls':0}
dump(E/'manifest.json',manifest)
links=[]
for p in [body,E/'README.md']:
    txt=p.read_text()
    assert txt.count('\\[')==txt.count('\\]')
    for href in re.findall(r'\]\(([^)]+)\)',txt):
        if '://' in href or href.startswith('#'):continue
        assert (p.parent/href.split('#')[0]).resolve().exists(),(p,href)
        links.append({'from':str(p.relative_to(R)),'href':href})
receipt=R/'cleanup/workspaces/Boss7/receipts-round17/e6d7ff01cc1b00450a9e.json'
rec=json.loads(receipt.read_text())
assert rec['id']==primary['id'] and rec['disposition']=='integrated' and len(rec['targets'])==5
assert all(rec[x] is True for x in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
ast.parse(Path(__file__).read_text())
for target in rec['targets']:
    if target!=str((E/'self-check.json').relative_to(R)):assert (R/target).exists()
owned=[body,E/'README.md',E/'manifest.json',Path(__file__),receipt]
result={'status':'pass','static_only':True,'primary_files':1,'primary_bytes':1209,
    'related_originals_full_read':7,'stable_comparisons_full_read':6,'same_batch_comparisons_full_read':3,
    'shared_execution_records_read':2,'links_checked':len(links),'receipt_targets':5,
    'own_mathematical_or_original_execution_calls':0,
    'bindings':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in owned],
    'local_links':links}
dump(E/'self-check.json',result)
assert all((R/t).exists() for t in rec['targets'])
print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','local_links')},ensure_ascii=False))
