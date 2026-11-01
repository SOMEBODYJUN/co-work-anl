"""Static checks for the three entry resources only; no mathematical execution."""
from pathlib import Path
import ast, hashlib, json, re

E = Path(__file__).resolve().parent
A, R = E.parents[2], E.parents[4]
body = A/'state/资源/六人半覆盖的独立研究合同与探索边界--资源.md'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prefix = 'research/workspaces/customer-attraction/R-70d2119f50a642dc94b386eb142f1f2d/'
commits = ['68fad804ec5946cb296f77dc5b336308a66abf12', 'aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']
primary = [
    ('4c65cb733e750ff3cd42', 'README.md', 654, '5b47cfccd02a56359a9755ad27b12f7e1f9955b7b18ac56f1e349783134b5801', '456fca6c67790891246d50cac048afd7152dd602'),
    ('0feb999c7e960f46b89b', 'SIX_BRIEF.md', 5250, '475c568882025f7c2833fe227da05ea8152e8de26e9d2ff1cd11101bc523d9cd', '05906febb0e8be85955679a89a9a766e46e2ea1c'),
    ('9bf870223d2b33512e0b', 'workspace.json', 150, '0d73a6be1e65d985917efcfe53fb77be7c1cccec3e185a34a406be9a0e9a5290', 'ef404253295f452d2a4a07eef089f9ef046e6ada'),
]
sources = []
for sid, name, size, expected, blob in primary:
    p = E/'original'/name
    assert p.stat().st_size == size and sha(p) == expected
    exported = Path('/workspace/scratch/c0ab78c47566')/('r70-entry-'+sid+'.txt')
    assert exported.read_bytes() == p.read_bytes()
    sources.append({'id': sid, 'path': prefix+name, 'size': size, 'sha256': expected,
        'blob': blob, 'commits': commits, 'saved_path': 'original/'+name, 'full_file_read': True})
workspace = json.loads((E/'original/workspace.json').read_text())
assert workspace == {'schema': 1, 'save': 'customer-attraction',
    'actor': 'R-70d2119f50a642dc94b386eb142f1f2d', 'instance': '6f2d2555cbae4e2189252c4fbee20da9'}
comp = [
    'state/定义/共同目录完整历史模型--定义.md',
    'state/算法/完整历史纯SPE终局全集--算法.md',
    'state/定理/五人半覆盖--定理.md',
    'state/定理/六极大联合预算半覆盖--定理.md',
    'state/定理/七极大主题半覆盖与五六提供者边界--定理.md',
    'state/引理/共同末位报价与隐藏回复投影--引理.md',
    'state/引理/末两人重叠比较与任意索引聚合--引理.md',
    'state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md',
    'state/定理/静态混合安全值的锐目录计数界--定理.md',
    'state/审查/失败路线中的真实顺序收费与模板边界--审查.md',
    'state/反例/逐人末位二倍保底的七客户反例--反例.md',
    'state/反例/三人顺序SPE低于全部静态CCE福利--反例.md',
    'state/反例/顺序SPE终局不必为同时PNE--反例.md',
    'state/反例/五客户无拥挤SPE负载桥障碍--反例.md',
    'state/反例/实际前缀的剩余利润与新增覆盖--反例.md',
    'state/反例/实际均匀缩放负载的弱付款桥--反例.md',
    'state/障碍/R23-promotion势能桥与零遗憾重置精确反例--障碍.md',
    'state/候选/相邻真实双主题的势排除预算--候选.md',
    'state/反例/调和复制税逐分支归纳的六客户边界--反例.md',
    'state/障碍/全混合终局势预算的静态行族不足--障碍.md',
    'state/程序/有序自复制税势预算的全SPE终局探针--程序.md',
    'state/计算/ZZ阈值必要系统的有理候选点--计算.md',
    'state/构造/回复会员阈值的共同凸抬升与对角预算拆分--构造.md',
    'state/资源/显式回复主图的阶段点与未闭报价账本--资源.md',
    'state/资源/六人研究入口与真实尾利润投影的四条冻结行--资源.md',
    'state/资源/末位标量与索引必要行的接续版本账本--资源.md',
]
manifest = {'primary_sources': sources, 'primary_total_bytes': 6054,
    'workspace_complete_fields': workspace,
    'fully_read_comparisons': [{'path_relative_to_archive': p, 'size': (A/p).stat().st_size,
                               'sha256': sha(A/p)} for p in comp],
    'same_batch_program_read_and_linked_without_mutable_body_hash':
        'state/程序/六人浮点终局搜索的随机输入入口--程序.md',
    'ownership_boundary': 'original/SIX_SEARCH.py and related/six_1/spe_dp.py belong to the separate root program task; not part of these three receipts',
    'original_program_runs_for_this_resource': 0, 'LP_runs': 0,
    'new_mathematical_checks': 0, 'mature_audit_reruns': 0}
(E/'metadata-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
links = []
for p in (body, E/'README.md'):
    text = p.read_text()
    assert text.count('\\[') == text.count('\\]')
    for href in re.findall(r'\]\(([^)]+)\)', text):
        if '://' in href or href.startswith('#'): continue
        assert (p.parent/href.split('#')[0]).resolve().exists(), (p, href)
        links.append({'from': str(p.relative_to(R)), 'href': href})
receipts = []
for sid, name, *_ in primary:
    p = R/('cleanup/workspaces/Boss7/receipts-round16/'+sid+'.json')
    rec = json.loads(p.read_text())
    assert rec['id'] == sid and rec['disposition'] == 'integrated'
    assert all(rec[x] is True for x in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for'])
    assert str(body.relative_to(R)) in rec['targets']
    assert str((E/'original'/name).relative_to(R)) in rec['targets']
    for target in rec['targets']:
        if target != str((E/'self-check.json').relative_to(R)): assert (R/target).exists()
    receipts.append(p)
ast.parse(Path(__file__).read_text())
json.loads((E/'metadata-manifest.json').read_text())
owned = [body, E/'README.md', E/'metadata-manifest.json', Path(__file__),
         *[E/'original'/name for _, name, *_ in primary], *receipts]
result = {'status': 'pass', 'static_only': True, 'primary_sources': 3,
    'primary_bytes': sum(x[2] for x in primary), 'workspace_fields': len(workspace),
    'fully_read_comparison_bindings': len(comp), 'same_batch_additional_program_full_read': True,
    'local_links_checked': len(links), 'receipt_files': len(receipts),
    'receipt_targets_each': 6, 'original_program_calls': 0, 'math_calls': 0,
    'bindings': [{'path': str(p.relative_to(R)), 'bytes': p.stat().st_size,
                  'sha256': sha(p)} for p in owned], 'local_links': links}
(E/'self-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
assert all((R/t).exists() for p in receipts for t in json.loads(p.read_text())['targets'])
print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','local_links')}, ensure_ascii=False))
