"""Record only Main's actually reviewed comparison, preserving all other pending work."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
R = P.parents[4]
target = R/'map/integration.json'
d = json.loads(target.read_text())
old = json.loads((P/'preassemble_pending.json').read_text())
receipt = json.loads((R/'map/receipts/six-boss1-source-requery-map3b.json').read_text())
pins = json.loads((P/'input_pins.json').read_text())
assert len(pins) == 15 and len(receipt['coverage']) == 8 and len(receipt['assets']) == 14
registry = json.loads((R/'research/registry.json').read_text())
assert len(registry['edge_files']) == 2127
ours = {}
for a in receipt['assets']:
    raw = (R/a['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == a['sha256']
    e = json.loads(raw)
    assert a['path'] in registry['edge_files']
    ours[e['edge_id']] = e
assert len(ours) == 14
note = ('Boss1 six-boss1-source-requery-map3b：八核心及七共享来源的十四条准确关系已逐项实读并经正规回执接入；'
        '一条新source3关系支付目标完整C36/C30及ROOT36/30/CAP2结论，其余仅支付各自明列贡献。'
        '具体证明范围、条件及原字节在本批comparison_review.md和input_pins.json。'
        '全型覆盖界与固定16hist排除严格区分，accepted不提升half；没有新增跨外档迁移。'
        '仅清本批确已审的对象/边delta，旧pending和同期Boss2等未审关系继续保留。')
assert note not in d['review_note'], 'Already recorded; no duplicate review.'
d['reviewed_by'] = d['reviewed_by'] + '; Boss1'
d['review_note'] += '\n' + note
for scope in ['archives/customer-attraction','archives/customer-attraction/subarchives/six-providers']:
    row = d['archive_reviews'][scope]
    row['comparison_scope'] += '\nBoss1本轮范围：同一actual前四最大X的H3/SAFE/UP、末容量与真实跨钱包投影；真最大C根、同源portfolio、PAIR与任意两历史C36/C30，及计算v13中各自实际付款。'
    row['outcome'] += '\n' + note
    opening = 'Boss1本RUN的原六人half和完整SPE反例仍未闭合；后续root270/可见C/内部SAFE的新工作包不属于本批已正式登记的计算v13结论。'
    if opening not in row.setdefault('open_math',[]): row['open_math'].append(opening)
cross = d['cross_archive_review']
cross['comparison_scope'] += '\nBoss1只接customer-attraction父档与six-providers子档的上述明确比较。'
cross['outcome'] += '\n同一客户模型内各ALL前提及不同OR路线保留；没有从目录邻近或并行集成生成与调度等其它存档的新模型映射。'

previous = old.get('pending_changes',{})
new = d.get('pending_changes',{})
pending_edges = (set(previous.get('edge_ids',[])) | set(new.get('edge_ids',[]))) - set(ours)
pending_objects = (set(previous.get('object_ids',[])) | set(new.get('object_ids',[]))) - set(pins)
# A reviewed object is still an endpoint of an unreviewed changed relation.
for eid in pending_edges:
    pending_objects.update(d.get('edge_endpoints',{}).get(eid,[]))
pending_scopes = set(previous.get('archive_scopes',[])) | set(new.get('archive_scopes',[]))
for oid in pending_objects:
    pending_scopes.update(d.get('object_scopes',{}).get(oid,[]))
d['pending_changes'] = {'object_ids':sorted(pending_objects), 'edge_ids':sorted(pending_edges),
                        'archive_scopes':sorted(pending_scopes)}
# Keep prior unresolved prose even where assemble's delta computation omitted it.
for scope, unresolved in old['archive_unresolved'].items():
    if scope in d['archive_reviews']:
        row = d['archive_reviews'][scope]
        row['unresolved'] = list(dict.fromkeys(row.get('unresolved',[])+unresolved))
cross['unresolved'] = list(dict.fromkeys(cross.get('unresolved',[])+old['cross_archive_unresolved']))
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
summary = {'status':'OUR14_RELATIONS_IN_CANONICAL_OTHER_PENDING_PRESERVED',
           'edge_files':len(registry['edge_files']), 'reviewed_core_count':8,'reviewed_input_count':15,
           'reviewed_edge_ids':sorted(ours), 'task_receipt_pin':d['task_receipt_pins']['six-boss1-source-requery-map3b'],
           'remaining_pending_counts':{k:len(v) for k,v in d['pending_changes'].items()},
           'scope':'Local integrated draft. No whole-repository final or original half claim.'}
(P/'integration_review_result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
