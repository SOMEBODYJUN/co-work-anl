"""Record only Main's actually reviewed comparison, preserving all other pending work."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
R = P.parents[4]
target = R/'map/integration.json'
d = json.loads(target.read_text())
old = json.loads((P/'preassemble_pending.json').read_text())
receipt = json.loads((R/'map/receipts/six-boss1-stage19-wallets-map3b.json').read_text())
pins = json.loads((P/'input_pins.json').read_text())
assert len(pins) == 17 and len(receipt['coverage']) == 9 and len(receipt['assets']) == 17
registry = json.loads((R/'research/registry.json').read_text())
assert len(registry['edge_files']) == 2130
ours = {}
for a in receipt['assets']:
    raw = (R/a['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == a['sha256']
    e = json.loads(raw)
    assert a['path'] in registry['edge_files']
    ours[e['edge_id']] = e
assert len(ours) == 17
note = ('Boss1 six-boss1-stage19-wallets-map3b：九核心及八共享来源的十七条关系已逐项重判并经正规回执接入。'
        '旧十四条中六条原字节保留、八条按扩展正文更新；旧source3整结果声明准确收窄为v2贡献。'
        '三条新ALL关系支付完整内部参数域、ROOT270全结果、3056整面排除及γ36普遍界。'
        '计算v15仅修复正式证据的发布路径，数学仍同v14；全型普遍界与固定16hist有限值分开。'
        'half和完整SPE反例均未闭合；只清本批确已审对象/关系，其他存档及Boss未审pending继续保留。')
assert note not in d['review_note'], 'Already recorded; no duplicate review.'
d['reviewed_by'] = d['reviewed_by'] + '; Boss1'
d['review_note'] += '\n' + note
for scope in ['archives/customer-attraction','archives/customer-attraction/subarchives/six-providers']:
    row = d['archive_reviews'][scope]
    row['comparison_scope'] += '\nBoss1本轮范围：同一actual前四最大X与真正裸最大C分开；真实内部域/同菜单投影、PAIR及P25联合ROOT270、完整3056正付款/整面排除和γ36。旧H3/SAFE/UP/容量等关系只承认原明列贡献，17关系按当前准确pins。'
    row['outcome'] += '\n' + note
    row['open_math'] = [x for x in row.get('open_math',[]) if not (x.startswith('Boss1本RUN') and '不属于本批' in x and 'v13' in x)]
    opening = 'Boss1本RUN的原六人half和完整SPE反例仍未闭合；ROOT270/可见C/内部SAFE/γ36已纳入本批准确版本；新4177准备尚未求解，后续cap3及高lambda闭合仍属另轮工作区成果。'
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
summary = {'status':'OUR17_RELATIONS_IN_CANONICAL_OTHER_PENDING_PRESERVED',
           'edge_files':len(registry['edge_files']), 'reviewed_core_count':9,'reviewed_input_count':17,
           'reviewed_edge_ids':sorted(ours), 'task_receipt_pin':d['task_receipt_pins']['six-boss1-stage19-wallets-map3b'],
           'remaining_pending_counts':{k:len(v) for k,v in d['pending_changes'].items()},
           'scope':'Local integrated draft. No whole-repository final or original half claim.'}
(P/'integration_review_result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
