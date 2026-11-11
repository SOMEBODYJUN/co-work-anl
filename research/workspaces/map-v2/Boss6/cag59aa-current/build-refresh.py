from pathlib import Path
import json, hashlib, copy
root=Path('/workspace/scratch/62622ba39554/co-work-anl-boss6')
out=Path('/workspace/scratch/62622ba39554/staging-cag59aa')
tid='customer-attraction-3a-3a-59aab9449e77a9e4'
old=root/'research/workspaces/map-v2/Boss6/cag59aa-before-eta-round48/cag59aa'
erel=Path('map/edges')/tid
edir=out/erel
edir.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ref(p):return {'path':str(p),'sha256':sha(root/p)}
tpath=Path('research/operations/map-v2/tasks')/(tid+'.json')
task=read(root/tpath);d=task['definition'];reg=read(root/'research/registry.json');objects={x['object_id']:x for x in reg['objects']}
assert task['state']=='claimed' and task['owner']=='Boss6' and task['request_id']=='11db74662aa941a2b1ad9234da32b922'
for i in d['object_ids']+d['read_object_ids']:assert pin(objects[i])==d['input_pins'][i],i
snapshot={'task_id':tid,'owner':task['owner'],'request_id':task['request_id'],'definition_pin':pin(d)}
CR='customer-attraction/same-tail-completion-credit-obstruction'
RESET='M-fbac8151896b451abdc818851afbdee5'
REST='customer-attraction/optimal-completion-true-restart-and-retained-credit-stopping'
ETA='customer-attraction/two-provider-eta-budget-counterexample'
cr=objects[CR]['body']['path'];rest=objects[REST]['body']['path']
assert sha(root/cr)=='9707e3d1648180da23fb4bda042518799f6cd593665a81f67de3888f949ed26d'
assert sha(root/rest)=='73dcab68cb104d9e013830ab5f3a3e2d3142d25d4e8a52ee486c63d086af0261'
edgefiles=[]
for p in sorted((root/erel).glob('*.json')):
    e=read(p)
    if 'edge_id' not in e:continue
    for r in e['evidence']:
        if r['path'] in (cr,rest):r['sha256']=sha(root/r['path'])
    # The parent supplies native endpoint/evidence bindings after installing this exact mathematical result.
    for k in ('endpoint_pins','evidence_pins','review_digest'):e.pop(k,None)
    if p.stem in ('all-big-credit-family-supplies-positive-restart-witness','same-policy-restart-two-registered-formulations'):
        e['review_note']+=' 本次已核发布勘误d2c860719的精确diff及CR v4/RESET v2/REST v2注册差异：仅ETA全称候选状态与源证据绑定刷新，注册重启/折扣陈述、all-big本族局部负式及本边证明不变。26/67两人例均超ETA预算1/2，不决定恰六人half。'
    write(edir/p.name,e);edgefiles.append((p.name,e))
assert len(edgefiles)==12
assert sum('whole_result' in e for _,e in edgefiles)==8
assert sum('contribution' in e for _,e in edgefiles)==4
assert sum(e['relation_mode']=='unconditional' for _,e in edgefiles)==9
assert sum(e['relation_mode']=='conditional' for _,e in edgefiles)==3
# Accurate semantic reading ledger: the old complete reads remain attributable to the mature round.
priorledger=read(old/erel/'reading-ledger.json')
ledgerentries=[]
for x in priorledger['entries']:
    e=copy.deepcopy(x);p=e['path'];e['prior_round_actual_read']=e.pop('actual_read');e['prior_round_sha256']=e['sha256'];e['sha256']=sha(root/p)
    e['actual_read_this_refresh']='published-exact-diff-plus-prior-complete-body' if p in (cr,rest) else 'reused-mature-prior-read'
    e['read_method_this_refresh']='d2c860719完整变更逐字实读；未变部分接续此前完整正文阅读。' if p in (cr,rest) else '与旧已付数学精确pin/字节合同匹配；未重读或重跑以申报新工作。'
    ledgerentries.append(e)
newreads=[
 ('archives/customer-attraction/state/反例/两位提供者的分享余项预算严格反例--反例.md','complete-body',[],'本轮首次完整实读两份客户输入、全部8节点策略、两套收益矩阵、菜单、ETA1/2违例及唯一性边界。'),
 ('archives/customer-attraction/state/算法/分享余项候选的完整策略树极值--算法.md','complete-body',[],'本轮首次完整实读可信集合、离轨子树独立拼接与实际递推；只复用其正确性合同，未执行算法。'),
 ('archives/customer-attraction/tools/evidence/eta-two-provider-counterexample/verify.py','complete-code',[],'完整实读自足逐客户验证代码；未运行。'),
 ('archives/customer-attraction/tools/evidence/eta-two-provider-counterexample/replay.json','complete-report',[],'完整实读两份已存确定输出，包括全部矩阵和ETA条目；不计本轮重放。'),
 ('archives/customer-attraction/state/计算/静态安全值与聚合保底的精确核验--计算.md','complete-body',[],'补齐当前阅读合同与旧ledger的显式范围差：静态匹配证书与动态聚合失败是不同事实，所有旧run仅复用。'),
 ('archives/customer-attraction/state/审查/顺序客户吸引来源记录与上传半覆盖界限审查--审查.md','complete-body',[],'补齐当前阅读合同与旧ledger显式范围差；实读原模型来源、三人/一般弱界与逐人theta失败的精确范围，不代读原件或重跑。'),
 ('archives/customer-attraction/state/资源/一般安全付款检查点与中继分支导航--资源.md','complete-exact-section',['强聚合与准确半覆盖金额'],'只完整实读指定节：2W−OPT=2(S−D)+t+epsilon，强聚合是更强条件，末两保底不支付早期欠债。'),
]
for p,scope,sections,note in newreads:
    ledgerentries.append({**ref(p),'actual_read_this_refresh':scope,'sections':sections,'read_method_this_refresh':'完整显示指定正文/代码/报告或精确标题节；没有数学执行。','scope_note':note})
ledger={
 'actor':'Boss6','task_id':tid,'task_snapshot':snapshot,
 'formal_primary_core_count':20,'shared_read_object_count':7,
 'current_task_declared_reading_refs':{'references':len(d['context_plan']['reading_refs']),'distinct_paths':len({x['path'] for x in d['context_plan']['reading_refs']})},
 'all_current_registered_statements_quantifiers_assumptions_reviewed':True,
 'prior_ledger':{'path':str((old/erel/'reading-ledger.json').relative_to(root)),'sha256':sha(old/erel/'reading-ledger.json'),'entries':len(priorledger['entries'])},
 'entries':ledgerentries,
 'additional_re_read_this_refresh':[{'path':'archives/customer-attraction/state/引理/最优首动作菜单与真实孩子损失--引理.md','sha256':sha(root/'archives/customer-attraction/state/引理/最优首动作菜单与真实孩子损失--引理.md'),'actual_read_this_refresh':'complete-body','reason':'核ETA分布最小化与全信用恒等的逻辑范围；此前成熟读也保留。'}],
 'changed_source_reading_order':'本轮先完整实读旧714f29/2d733正文，再完整核发布d2c860719精确diff，获得当前9707e3/73dcab的完整语义覆盖；未把两页当前版本冒称第二次全页新读。',
 'mature_contract_reuse':priorledger['mature_contract_reuse'],
 'scientific_runs':{'old_CLIs':0,'LP':0,'SPE_solver':0,'BI':0,'random_scans':0,'mature_tree_replays':0,'eta_verifier':0},
 'not_claimed':'未把当前49个文件宣称本轮全部新读。旧43条ledger如实标为成熟复用；新增7路径按精确实际范围列出，MENU全文复读另列。哈希核验只说明当前字节合同，不代表阅读全文或科学运行。'
}
write(edir/'reading-ledger.json',ledger)
# Source integrity is explicitly separate from semantic reading.
priorfresh=read(old/erel/'source-freshness.json');oldpins={x['object_id']:x for x in priorfresh['object_checks']}
checks=[];direct={};delta=[]
for i in d['object_ids']+d['read_object_ids']:
    o=objects[i];p=pin(o);row={'object_id':i,'version':o['version'],'registration_pin':p,'matches_task':p==d['input_pins'][i]};checks.append(row)
    if i not in oldpins or p!=oldpins[i]['registration_pin']:delta.append({**row,'prior_version':oldpins.get(i,{}).get('version'),'change_role':'new-shared-read-ETA-evidence' if i==ETA else 'published-minimal-ETA-source-status-erratum'})
    for r in [o['body']]+o['evidence']:
        actual=sha(root/r['path']);assert actual==r['sha256'],r['path']
        direct[r['path']]={'path':r['path'],'sha256':actual,'all_direct_declared_refs_match':True,'semantic_read_scope':'reading-ledger.json；本项字节核验不等于全文新读。'}
for r in d['context_plan']['reading_refs']:assert sha(root/r['path'])==r['sha256'],r['path']
fresh={'task_id':tid,'owner':'Boss6','request_id':task['request_id'],'definition_pin':pin(d),'core_count':20,'read_count':7,
 'object_checks':checks,'changed_or_added_objects':delta,'direct_source_checks':list(direct.values()),
 'task_snapshot_sha256':sha(root/tpath),'registry_snapshot_sha256':sha(root/'research/registry.json'),'all_input_pins_match':True,
 'all_current_context_reading_ref_bytes_match':True,'semantic_reading_ledger':str(erel/'reading-ledger.json'),
 'published_source_correction':{'commit':'d2c860719ec561a8587e4df5d883338dd1f29249','state':'resolved-and-published','source_pins':[ref(cr),ref(rest)],'registered_versions':{CR:4,RESET:2,REST:2},'mathematical_effect':'一般保xi仅删eta候选已由ETA2两个完整两人SPE否定；all-big局部不否定和12条边的成熟结论均保持正确。'},
 'pending_source_correction':None,
 'native_actions_deferred_to_parent':['edge-bind','edge-check','queue/checkpoint/done'],
 'relation_mode_final_review':priorfresh['relation_mode_final_review']}
write(edir/'source-freshness.json',fresh)
receipt=read(old/('map/receipts/'+tid+'.json'))
for i,c in receipt['coverage'].items():c['object_pin']=d['input_pins'][i]
receipt['coverage'][CR]['comparison_scope']='复用完整all-big解析证明与成熟并行原MD/code/JSON合同；本轮实读旧正文并核发布勘误diff，及ETA26/67正文/算法/自足代码/输出，准确区分全称ETA已否定与all-big本族未否定；m3/5旧运行不计本轮。'
receipt['coverage'][REST]['comparison_scope']='完整同h同σ两真实枝与all-big严格reset1推导按成熟稿复用；本轮核REST v2正文勘误仅改ETA候选现状，保xi省eta一般全称已由两人例否定，不扩成重启statement的新结论。'
receipt['coverage'][RESET]['comparison_scope']='RESET/REST完整注册statement及成熟逐定义互推复用；本轮核RESET v2只刷新CR证据SHA，不把同页ML静态联合lambda界或ETA反例冒作真实reset的一般付款。'
receipt['task_snapshot']=snapshot;receipt['source_status']='Current published ETA erratum resolved; all20 core pins and7 shared-read input pins match current claimed definition.12 mature logical edges preserved; native binding/check and checkpoint by parent.'
receipt['reading_accounting']={'ledger':str(erel/'reading-ledger.json'),'prior_mature_entries_reused':43,'new_explicit_paths_read':7,'published_source_diffs_reviewed':2,'scientific_runs':0,'statement':'未将49文件全部标为本轮新读；MENU全文本轮复读另列，原12边与6closed-overlap成熟推导复用。'}
receipt['current_additional_comparisons']=[
 {'core_id':CR,'peer_id':ETA,'disposition':'closed-without-refutation-edge','reason':'ETA否全保xi仅删eta的附加全称候选；CR注册statement只断言删xi/eta与固定alpha折扣障碍，all-big本族未否ETA的局部话仍真，不反CR。'},
 {'core_id':REST,'peer_id':ETA,'disposition':'closed-without-refutation-edge','reason':'ETA状态勘误不改变REST注册重启恒等和正restart见证；当前counterexample不支付或否定C_A−C_B的一般真实枝关系。'}]
review=read(old/erel/'mathematical-review.json');review.pop('pending_source_status_issue',None)
review['task_snapshot']=snapshot;review['published_source_status_correction']=fresh['published_source_correction']
review['edge_count']=12;review['new_canonical_delivery_edges']=12;review['new_mathematical_relations_this_refresh']=0;review['mature_relations_recovered']=12
review['read_scope_accounting']=receipt['reading_accounting'];review['additional_current_comparisons']=receipt['current_additional_comparisons']
review['current_versions_and_unchanged_results']={'CR':'v3→v4：body/objections/版本；注册statement与量词不变。','RESET':'v1→v2：CR evidence SHA/版本；body、statement、量词不变。','REST':'v1→v2：body SHA/版本；statement与量词不变。','other_23_mature_input_objects':'与旧source-freshness所列registration_pin完全相同。','ETA':'新增只读v2，证明仅指向全称ETA候选，不把其当六人half或CR/REST注册命题的反例。'}
review['canonical_review']={'registry_sha256':sha(root/'research/registry.json'),'reused_prior_scope':read(old/erel/'mathematical-review.json')['canonical_review'],'current_focused_review':'本轮对更正涉及三对象的canonical端点/证据扫描未发现已有登记边；恢复12edge_id均沿原稳定稿，未为ETA状态纠正造重复边。'}
review['mature_run_policy']='旧成熟解析证明/完整树/LP/审计输出按精确合同复用。当前仅记录文本、差异、SHA与input pin；无科学运行，无原生绑定/检查/队列/Git写入。'
review['closed_overlaps']=receipt['closed_overlaps'];review['follow_up_tasks']=[]
review['source_issue_remaining']=None
review['parent_finalization']='父Boss原生edge-bind/check后刷新receipt.assets哈希并checkpoint/done；本稿不冒称已发布本包。'
write(edir/'mathematical-review.json',review)
receipt['assets']=[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted(edir.glob('*.json'))]
write(out/('map/receipts/'+tid+'.json'),receipt)
manifest={'task_id':tid,'task_snapshot':snapshot,'delivery_state':'current-input-mature-result-await-parent-native-bind-check-checkpoint','edges':12,'whole_result':8,'contribution':4,'unconditional':9,'conditional':3,'coverage':{'linked':14,'isolated-after-review':6,'needs-decision':0},'declared_closed_overlaps':6,'follow_up_tasks':[],'scientific_runs':0,
 'files':[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted((out/'map').rglob('*.json'))],
 'no_hash_cycle':'receipt lists edges and review assets, not itself or this manifest; manifest hashes all map files.',
 'parent_action':'Install to original write_paths after native synchronization is idle. Bind/check12 edges, then reseal receipt assets and manifest if binding changes edge bytes.'}
write(out/'delivery-manifest.json',manifest)
print(json.dumps({'out':str(out),'definition_pin':pin(d),'receipt_sha256':sha(out/('map/receipts/'+tid+'.json')),'manifest_sha256':sha(out/'delivery-manifest.json'),'files':len(manifest['files']),'counts':manifest['coverage'],'changed_inputs':len(delta),'source_hashes':[ref(cr),ref(rest)]},ensure_ascii=False,indent=2))
