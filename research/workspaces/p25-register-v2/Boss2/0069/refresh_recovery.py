"""Targeted fresh-worker recovery; no Git, queue or registry writes."""
from pathlib import Path
import json,hashlib,collections,sys
R=Path('.').resolve();H=R/'research/workspaces/p25-register-v2/Boss2/0069';BP=R/'research/registration/batches/register-ab98f323ad-0069.json';RP=R/'research/registration/receipts/register-ab98f323ad-0069.json'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ref(p):
 p=Path(p);p=p if p.is_absolute() else R/p
 return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
b=read(BP);r=read(RP);previous_receipt_ref=ref(RP);task=read(R/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0069.json')['definition'];old_req=read(H/'attachment-requests.json')
# Existing mature objects/IDs and exact mature source bytes are reused, not recreated.
newton=next(o for o in b['objects'] if o['object_id']=='customer-attraction/three-remaining-truncated-price-rational-newton-certificate')
newton['model']='5个Boolean变量(a,b,c,q,r)的32个会员型、整数背景p≥0、矩形实参数d,ell及固定七个有理行的代数模板；不假设这些行已来自完整SPE。'
reg=read(R/'research/registry.json');canonical={o['object_id']:o for o in reg['objects']}
peer_path=R/'research/registration/batches/register-ab98f323ad-0001-5-evidence.json';peer={o['object_id']:o for o in read(peer_path)['objects'] if o['object_id'] in {'CA-AGGREGATE-DECORRELATION-NO','CA-ONPATH-DECOUPLED-BUDGET-NO'}}
accepted_peers={}
for oid,o in peer.items():
 if any(x['path']==b['materials'][15]['path'] and x['sha256']==b['materials'][15]['sha256'] for x in [o['body']]+o['evidence']):accepted_peers[oid]=o
for row in b['materials']:
 reason=row['reason']
 old_prefix='本次恢复按分段核读本材料数学正文、模型量词、陈述条件及证据合同；原始程序/大表按必要范围定向核读，未重跑数学程序或建边。'
 new_prefix='复用0069既有成熟草稿及此前恢复的分段正文核读记录；本fresh worker逐对象复核登记字段与精确refs，新增全文核读范围另见receipt，未将旧全批reading声明冒作本轮新读。'
 row['reason']=reason.replace(old_prefix,new_prefix)
for oid in accepted_peers:
 if oid not in b['materials'][15]['object_ids']:b['materials'][15]['object_ids'].append(oid)
b['materials'][15]['reason']='本轮全文实读该证据合同，区分89客户非最优查询的总去相关负差、36客户非最优查询的补偿预算失败、36安全最优查询正预算及61根税、策略锥定理的不同owner。两已列owner在0001-5-evidence主记录中具有同path/SHA的真实证据接入，仅按真实同组交付复用；CA-ROOT-TAX-NO及CA-SECURITY-CONE-DUAL仍待各主作者定向增量接证，故本材料保needs-decision。'
b['materials'][15]['disposition']='needs-decision'
write(BP,b)
# Exact current references, without assuming that an absent main record has accepted anything.
records=collections.defaultdict(list)
for p in [R/'research/registry.json',*sorted((R/'research/registration/batches').glob('*.json'))]:
 for o in read(p).get('objects',[]):records[o['object_id']].append((p,o))
request_rows=[];audit_rows=[]
for q in old_req['requests']:
 q=dict(q);mat=q['material'];found_can=[];found_batch=[];missing=[];owner_details=[]
 for oid in q['requested_owners']:
  es=[]
  for p,o in records.get(oid,[]):
   exact=[x for x in [o['body']]+o['evidence'] if x['path']==mat['path'] and x['sha256']==mat['sha256']]
   tp=R/'research/operations/p25-register-v2/tasks'/p.name
   state=read(tp).get('state') if tp.exists() and p.name!='registry.json' else None
   es.append({'record':ref(p),'body':o['body'],'task_state':state,'exact_material_refs':exact})
   if exact:
    (found_can if p.name=='registry.json' else found_batch).append(oid)
  if oid not in found_can and oid not in found_batch:missing.append(oid)
  owner_details.append({'object_id':oid,'records':es,'accepted_exact':oid in found_can or oid in found_batch})
 no_identity_route=not q['requested_owners']
 q.update(accepted_canonical_owners=list(dict.fromkeys(found_can)),accepted_record_owners=list(dict.fromkeys(found_batch)),pending_owners=missing)
 q['status']='pending_owner_route' if missing or no_identity_route else 'closed-canonical' if set(q['requested_owners'])<=set(found_can) else 'accepted-exact-peer-batch-delivery-dependent'
 q['audit_note']='Only exact main-record path/SHA is counted; current prepared peer batch acceptance is distinguished from canonical and requires actual joint delivery or prior canonical integration.'
 if q['material_index']==15:q['scope']='89/36两个反例已由0001-5-evidence主作者精确接证；61根税与策略锥定理的主作者尚未将本材料精确ref写入主record；不得把两查询/三实例合一。'
 request_rows.append(q);audit_rows.append({'material_index':q['material_index'],'material':mat,'owners':owner_details,'scope':q['scope'],'body_requests':q.get('owner_body_requests',[])})
pending_rows=[q for q in request_rows if q['status']=='pending_owner_route'];pending={str(q['material_index']):q['scope'] for q in pending_rows}
audit={'task_id':task['task_id'],'audit_type':'fresh current canonical and batch exact path/SHA comparison; mathematical acceptance only where actual owner record carries exact ref','registry_ref':ref('research/registry.json'),'routes':audit_rows,'unresolved_material_indices':[q['material_index'] for q in pending_rows],'peer_delivery_dependencies':[ref(peer_path)],'no_false_canonical_or_done_assertion':True}
write(H/'fresh-owner-route-audit.json',audit)
old_req.update(canonical_registry_ref=ref('research/registry.json'),requests=request_rows,unresolved_routing=pending,owner_audit=[])
old_req['audit_scope']='Fresh current-registry and exact peer-batch refs; no new acceptance inferred from a promise, body container ID or mere peer presence. See fresh-owner-route-audit.json.'
write(H/'attachment-requests.json',old_req)
# Keep former worker attestations as provenance, not this worker's fresh reading scope.
if 'prior_recovery_reading_provenance' not in r:r['prior_recovery_reading_provenance']={'receipt_ref_before_fresh_recovery':previous_receipt_ref,'reading':r.get('reading',{}),'summary':r.get('summary',{}),'recovery_review':r.get('recovery_review',{}),'status':'Prior worker/recovery testimony reused; not current fresh-worker full reading or execution attestation.'}
fresh_material_indices=[15,34,43]
fresh_scope={'task_id':task['task_id'],'status':'ready-for-parent-checkpoint-with-explicit-material-routing-needs-decision','fresh_reading':{'assigned_materials_read_in_full':[task['materials'][i] for i in fresh_material_indices],'all_23_object_registration_fields_compared':['model','statement','quantifiers','assumptions','scope','objections'],'main_records_read':['CA-AGGREGATE-DECORRELATION-NO','CA-ONPATH-DECOUPLED-BUDGET-NO'],'registry_and_peer_audit':'All requested exact IDs searched in current registry and available batch records; body/evidence path/SHA explicitly compared. Not blanket rereading all peer mathematical bodies or raw attachments.','inherited_reading_not_claimed_as_new':True},'mature_reuse':{'own_objects':len(b['objects']),'assigned_materials':len(b['materials']),'source_record':ref(H/'recovery-review.json'),'old_id_allocation':ref(H/'allocated-ids.json'),'note':'Prior complete body/definition reading attestation and mature source arguments are retained; this fresh recovery targets exact identity/routing and identified boundaries rather than re-proving all mathematics.'},'statement_corrections':[{'object_id':newton['object_id'],'field':'model','change':'5 Boolean variables have 32 membership types; former wording incorrectly said 32 variables. No identity, theorem or body bytes changed.'}],'fresh_computation':ref(H/'fresh-math-checks.json'),'pending_owner_routes':pending_rows,'peer_delivery_dependency':ref(peer_path),'no_registry_or_git_or_queue_writes':True,'edge_files':[]}
write(H/'fresh-recovery-review.json',fresh_scope)
r['reading']=fresh_scope['fresh_reading'];r['summary']={'objects':len(b['objects']),'materials':len(b['materials']),'inherited_mature_full_batch_reading':True,'fresh_full_material_indices':fresh_material_indices,'fresh_finite_math_verification':'m≤12 endpoint/capacity exact enumeration and separate budget arithmetic, not raw audit replay','edges':0,'dispositions':dict(collections.Counter(x['disposition'] for x in b['materials'])),'remaining_material_indices':[q['material_index'] for q in pending_rows],'remaining_named_owner_routes':sum(len(q['pending_owners']) for q in pending_rows),'remaining_identity_only_routes':sum(not q['requested_owners'] for q in pending_rows)}
r['batch_file']=ref(BP);r['assets']=[ref(BP)];r['attachment_requests']=ref(H/'attachment-requests.json');r['routing_pending']=pending;r['pending_owner_routes']=pending_rows;r['canonical_registry_ref']=ref('research/registry.json');r['fresh_recovery_review']=ref(H/'fresh-recovery-review.json');r['fresh_owner_route_audit']=ref(H/'fresh-owner-route-audit.json');r['peer_delivery_dependencies']=[ref(peer_path)]
sys.path.insert(0,str(R/'tools'));import registration
validation=registration.validate_batch(R,b,task['materials'],task['baseline'],accepted_peers)
refs=[x for o in b['objects'] for x in [o['body']]+o['evidence']]
for x in refs:assert ref(x['path'])['sha256']==x['sha256'],x
for x in task['materials']:assert ref(x['path'])['sha256']==x['sha256'],x
r['validation']={'status':'mathematical draft ready with explicit material routing needs-decision; parent owns actual checkpoint/CAS; not final registration closure','schema_and_ref_check':validation,'exact_object_refs_checked':len(refs),'assigned_material_ref_count_checked':len(task['materials']),'assets_byte_exact':True,'boundary_checks':ref(H/'fresh-math-checks.json'),'own_objects_not_duplicated':not any(o['object_id'] in canonical for o in b['objects']),'peer_context_note':'Two 0001-5-evidence owners used only as exact prepared same-group records. Deliver jointly or canonicalize peer first; no presumed canonical integration.'}
write(RP,r)
print(json.dumps({'batch_file':ref(BP),'receipt_file':ref(RP),'summary':r['summary'],'validation':validation,'peer_delivery_dependency':ref(peer_path)},ensure_ascii=False,indent=2))
