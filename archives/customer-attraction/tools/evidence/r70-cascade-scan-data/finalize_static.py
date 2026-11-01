"""Static package checks only: never run the saved data reader or original code."""
import ast
import hashlib
import json
from pathlib import Path
import re

E = Path(__file__).resolve().parent
A, R = E.parents[2], E.parents[4]
body = A/'state/计算/六人级联扫描快照与同覆盖大块的完整策略--计算.md'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
dump = lambda p,x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
ids = {'4f1faca4ff39c6b34e88': 'cascade_scan.json', '14ff67139e3cb521c73c': 'cascade_scan_best.json'}
inventory = [json.loads(line) for line in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
sources = []
for row in inventory:
    if row['id'] in ids:
        p = E/'original'/ids[row['id']]
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256']
        sources.append(row | {'saved_path': str(p.relative_to(R)), 'full_file_reviewed': True})
assert len(sources) == 2
shared = A/'tools/evidence/cascade-original-nine-boss3'
deps = json.loads((shared/'dependency-manifest.json').read_text())
dependencies = []
for item in deps:
    p = shared/item['evidence_path']
    assert p.stat().st_size == item['size'] and sha(p) == item['sha256']
    ast.parse(p.read_text())
    dependencies.append(item | {'saved_path': str(p.relative_to(R)), 'full_file_reviewed': True,
        'execution_in_this_task': False})
gen = next(r for r in inventory if r['id'] == 'f08bcbcb7a5f6f2bd41b')
gp = shared/'original/f08bcbcb7a5f6f2bd41b/cascade_attack.py'
assert sha(gp) == gen['sha256'] and gp.stat().st_size == gen['size']
ast.parse(gp.read_text())
dump(E/'source-manifest.json', {'primary': sources,
    'generator_read_but_historical_producer_version_not_uniquely_bound': gen | {'saved_path': str(gp.relative_to(R))},
    'shared_dependencies_full_read': dependencies, 'new_original_runs': 0})
comparisons = {
    '定义/共同目录完整历史模型--定义.md': '单位客户、完整历史、同覆盖标签接口与集合目录分开。',
    '程序/锚点缺口级联的完整策略锥与三个版本输出合同--程序.md': '实际生成器、完整树锥、有理恢复和版本边界。',
    '计算/级联发现的四份历史与三种完整单位客户见证--计算.md': '五人旧四历史与三不同见证不并入本六人事件。',
    '程序/七标签六人计数策略锥的覆盖缺口搜索--程序.md': '同十一客户游戏的明确标签映射，不同策略及42LP历史。',
    '定理/不交极大主题锐福利界--定理.md': '六人十一客户为既有不交大块锐性族。',
    '定理/固定完整策略的客户重数锥--定理.md': '完整IC与可行点/精确对偶/全策略量词。',
    '定理/六极大联合预算半覆盖--定理.md': '前批已全文读；本例六不同极大覆盖在其域内，不重跑。',
    '资源/六人半覆盖的独立研究合同与探索边界--资源.md': '前批全文完成的研究合同；一般六人目标与历史有限发现分开。',
}
comparison_records = []
for rel, note in comparisons.items():
    p = A/'state'/rel
    comparison_records.append({'path': str(p.relative_to(R)), 'bytes': p.stat().st_size,
        'sha256': sha(p), 'full_file_reviewed': True, 'relation': note})
cp = A/'tools/evidence/r70-count-policy-lp/exact-audit-summary.json'
comparison_records.append({'path': str(cp.relative_to(R)), 'bytes': cp.stat().st_size,
    'sha256': sha(cp), 'full_file_reviewed': True, 'relation': '已存成熟整数点与计数图审计，不重执行。'})
dump(E/'comparison-manifest.json', comparison_records)
report = json.loads((E/'data-audit.json').read_text())
assert report['status'] == 'pass' and report['all_action_records_read'] == 19608
assert len(report['nonuniform_count_groups']) == 1
assert len(report['nonuniform_count_groups'][0]['records']) == 120
assert report['full_numerical_IC_replay_calls'] == 0
original_script = Path('/workspace/scratch/c0ab78c47566/r17-audit-cascade-data.py')
original_report = Path('/workspace/scratch/c0ab78c47566/r17-cascade-data-audit.json')
assert original_script.read_bytes() == (E/'audit_saved_data.py').read_bytes()
assert original_report.read_bytes() == (E/'data-audit.json').read_bytes()
dump(E/'execution.json', {
    'event': 'one new saved-data consumption, not producer or solver replay',
    'command_as_executed': 'python /workspace/scratch/c0ab78c47566/r17-audit-cascade-data.py /workspace/scratch/c0ab78c47566/r17-cascade-scan.json /workspace/scratch/c0ab78c47566/r17-cascade-scan-best.json /workspace/scratch/c0ab78c47566/r17-cascade-data-audit.json',
    'tool_observed_exit_code': 0, 'internal_read_elapsed_seconds': report['read_elapsed_seconds'],
    'stdout': 'PASS summary displayed by tool; no separate stdout file captured',
    'stderr': 'no separate stderr file captured; no fabricated empty log',
    'checker_sha256': sha(E/'audit_saved_data.py'), 'report_sha256': sha(E/'data-audit.json'),
    'input_sha256_before_and_after': report['input_sha256_before_and_after'],
    'original_main_import_LP_BI_canonical_verifier_calls': 0,
    'full_numerical_IC_replay_calls': 0, 'repeat_of_this_event_during_formalization': False})
links = []
for p in (body, E/'README.md'):
    txt = p.read_text()
    assert txt.count('\\[') == txt.count('\\]')
    for href in re.findall(r'\]\(([^)]+)\)', txt):
        if '://' in href or href.startswith('#'): continue
        assert (p.parent/href.split('#')[0]).resolve().exists(), (p, href)
        links.append({'from': str(p.relative_to(R)), 'href': href})
receipts = []
for sid in ids:
    p = R/('cleanup/workspaces/Boss7/receipts-round17/'+sid+'.json')
    rec = json.loads(p.read_text())
    assert rec['id'] == sid and rec['disposition'] == 'integrated'
    assert all(rec[x] is True for x in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert len(rec['targets']) == 7
    for target in rec['targets']:
        if target != str((E/'self-check.json').relative_to(R)): assert (R/target).exists()
    receipts.append(p)
for p in E.glob('*.py'): ast.parse(p.read_text())
for p in E.glob('*.json'): json.loads(p.read_text())
owned = [body, *sorted(p for p in E.rglob('*') if p.is_file() and p.name != 'self-check.json'), *receipts]
result = {'status':'pass', 'static_only':True, 'primary_files':2, 'primary_bytes':sum(x['size'] for x in sources),
    'shared_generator_and_dependencies':5, 'full_read_comparisons':len(comparison_records),
    'links_checked':len(links), 'receipts':2, 'targets_each':7,
    'new_original_program_calls':0, 'saved_data_reader_reexecuted':False,
    'bindings':[{'path':str(p.relative_to(R)), 'bytes':p.stat().st_size, 'sha256':sha(p)} for p in owned],
    'local_links':links}
dump(E/'self-check.json',result)
assert all((R/t).exists() for p in receipts for t in json.loads(p.read_text())['targets'])
print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','local_links')},ensure_ascii=False))
