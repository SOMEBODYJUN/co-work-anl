from pathlib import Path
import hashlib, json, re, shutil

ROOT=Path('/workspace/scratch/9cf2a96299f5/co-work-anl')
SRC=Path('/workspace/scratch/9cf2a96299f5/um-workspace-next')
OUT=Path('/workspace/scratch/9cf2a96299f5/um-batch-c/c166')
TARGET='archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md'
IDS=['5ae723f7d81d5b08aac0','cfb2811e522481e9692b','16b6164078316d041986','13683206df988f7b1837','2727daf3ede34845a8d7','7b06946fabfc3dbc9216']
inventory={d['id']:d for d in map(json.loads,(ROOT/'cleanup/inventory.jsonl').read_text().splitlines())}
def digest(p):
    b=p.read_bytes()
    return {'size':len(b),'lines':len(b.splitlines()),'sha256':hashlib.sha256(b).hexdigest()}
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

manifest=[]
source_refs=[]
for sid in IDS:
    d=dict(inventory[sid]); p=SRC/(sid+'--'+Path(d['path']).name)
    fp=digest(p)
    assert fp['size']==d['size'] and fp['sha256']==d['sha256'],sid
    dest=OUT/'original'/sid/Path(d['path']).name
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    d['lines']=fp['lines'];d['full_file_reviewed']=True
    d['evidence_file']='archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/'+sid+'/'+p.name.split('--',1)[1]
    manifest.append(d)
    source_refs += ['source:'+s['commit']+':'+s['path'] for s in d['sources']]
dump('manifest-additions.json',{'sources':manifest})
dump('fingerprints.json',[{'id':d['id'],'blob':d['blob'],'size':d['size'],'lines':d['lines'],'sha256':d['sha256']} for d in manifest])
dump('source-refs-additions.json',source_refs)

related=[
('archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md','full-file, segmented reads; existing identities/resource and earlier corrections'),
('archives/unrelated-machines/state/资料/个人工作区恢复规则与旧题路由边界--资料.md','full-file; recovery/provenance versus current task'),
('archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/1254c0254ceb82d8b6b7/README.md','full-file; bytewise actor-normalized template comparison'),
('archives/unrelated-machines/README.md','full-file; current problem/scope status'),
('archives/unrelated-machines/问题--问题.md','full-file; exact main-goal scope'),
('archives/unrelated-machines/state/算法/多小端原生任务的双流实际调度--算法.md','full-file; stronger arity and actual-optimal no-Q branch distinguished from density bound'),
('archives/unrelated-machines/state/审查/多小端密度流障碍与单位读出校准槽双源审查--审查.md','full-file; density flow and unrelated calibrated tree contract kept separate'),
('archives/unrelated-machines/state/审查/小任务联合槽与加权小端ST双源续审查--审查.md','full-file; mixed small-ST formula and no-Q/relative-ratio boundaries'),
('archives/unrelated-machines/state/障碍/固定轮literal-SA的单位指派趋二间隙--障碍.md','full-file; signed-literal proof and explicit threshold correction'),
('archives/unrelated-machines/state/审查/固定轮SA独立注入审查与裸阈值上界边界--审查.md','full-file; raw r1/T<1 all-class correction versus valid parameter main family'),
('archives/unrelated-machines/state/审查/重轻森林整数性与价格凸化双源审查--审查.md','full-file; pruned convexification, conditional common face and unrelated forest branch'),
('archives/unrelated-machines/state/障碍/逐价格重匹配与共同残余的量词缺口--障碍.md','full-file; old 21/20/δ classification versus all-β correction'),
('archives/unrelated-machines/state/审查/凸包边际与残余通过量占位双源审查--审查.md','full-file; fixed-R, zero edges, dynamic role and graph completion versus fixed marginals'),
('archives/unrelated-machines/state/审查/残余通过量格结构与占位图表示最终独立审查--审查.md','full-file; dynamic OPT1/2, exact deficit and finite-review scope'),
('archives/unrelated-machines/state/计算/重轻价格凸化原程序的顶点对偶与共同重面核验--计算.md','full-file; prior finite run counts, fixes and general-solver boundary; no new execution'),
('archives/unrelated-machines/state/资源/占位诱导边缺口的实际矩阵与最大流原程序--资源.md','full-file; actual matrix, finite counts, padding-free upper argument and corrected OPT1/2'),
('archives/unrelated-machines/tools/evidence/um-joint-projection/original/research/current/unrelated_machines/heavy_light_price_convexification.md','full-file 16967B primary; all-β, Γ, optimum dual face and bit-complexity'),
('archives/unrelated-machines/tools/evidence/um-joint-projection/original/research/questions/unrelated_machines/heavy_light_joint_residual_minmax_obstruction.md','full-file primary; retained candidate and correction header; anchor nonuniform slack'),
('archives/unrelated-machines/tools/evidence/um-next-actual-audit-primary/comparison/research/reviews/unrelated_machines/heavy_light_price_convexification_review.md','full-file primary review; ede1392 baseline, prior knowledge and nonfatal release fixes'),
('archives/unrelated-machines/tools/evidence/fixed-sa-assignment/original/research/current/unrelated_machines/fixed_sa_assignment_gap.md','full-file primary; symbolic injective local law and original all-class claim'),
('archives/unrelated-machines/tools/evidence/fixed-sa-assignment/original/research/reviews/unrelated_machines/fixed_sa_assignment_gap_review.md','full-file primary review; signed events and r=m endpoint, no experiment'),
('archives/unrelated-machines/tools/evidence/residual-throughput-occupation-20261031/original/residual_throughput_occupation_review.md','full-file primary review; exact dynamic value, deficit proof and finite scope'),
('archives/unrelated-machines/tools/evidence/incidence-density-specialized-reviews-20261031/86bc9ab5d127d4dcd21a.show.txt','full-file primary review; pointwise density and absolute versus relative bounds'),
]
readlog=[]
for path,scope in related:
    p=ROOT/path; readlog.append({'path':path,'scope':scope,**digest(p)})

comparison_ids=['ca9e688268a7715bd7cd','acb99150324dcb0d1a48','c8cdbf5ff2de274caf1b']
if (SRC/'0f1cbe18dcc0a3914240--weighted_small_st_barrier_review.md').exists():
    comparison_ids.append('0f1cbe18dcc0a3914240')
for sid in comparison_ids:
    d=inventory[sid];p=SRC/(sid+'--'+Path(d['path']).name)
    fp=digest(p);assert fp['size']==d['size'] and fp['sha256']==d['sha256']
    dest=OUT/'comparison-primary'/sid/Path(d['path']).name
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    readlog.append({'id':sid,'path':d['path'],'scope':'full-file primary comparison; not claimed or marked done in this six-source batch','local_copy':str(dest.relative_to(OUT)),**fp})

code_slices=[
('work.py',300,350),
('tools/evidence/frontier-collaboration-and-root-lifecycle/original/d9b5b49ab665613450d6/work.py',239,291),
('tools/evidence/frontier-collaboration-and-root-lifecycle/original/3c0404b7974eca538863/work.py',292,343),
]
for path,start,end in code_slices:
    p=ROOT/path
    readlog.append({'path':path,'scope':f'workspace_init related function slice lines {start}-{end}; no source execution; not full-file reading',**digest(p)})
raw=(SRC/'16b6164078316d041986--README.md').read_bytes()
old=(ROOT/related[2][0]).read_bytes()
assert raw.replace(b'R-5d4448b5810f4d2eacbb86c644a670a2',b'ACTOR') == old.replace(b'R-0aebcce9ae5842fdb1be78207a977265',b'ACTOR')
prefix_counts={}
for sid in IDS[::2]:
    prefix=str(Path(inventory[sid]['path']).parent)+'/'
    prefix_counts[prefix]=[d['id'] for d in inventory.values() if d['path'].startswith(prefix)]
assert all(len(v)==2 for v in prefix_counts.values())
dump('read-comparison-log.json',{
    'schema':1,'internal_actor':'Boss5','six_sources_full_read':True,
    'related_reads':readlog,
    'contracts_read':['AGENTS.md','cleanup/OBJECTS.md','cleanup/receipt-example.json'],
    'programmatic_inventory_exact_prefix_matches':prefix_counts,
    'searches':['all three exact actors and instances across repository/current archives; no preexisting formal exact-identity match','all five mathematical basenames and claim IDs across repository; primary copies and later corrections followed'],
    'template_comparison':{'source':'16b6164078316d041986','comparison':'1254c0254ceb82d8b6b7','actor_normalized_bytes_equal':True},
    'new_mathematical_program_runs':0,'git_network_clean_calls_by_internal_solver':0,
    'reading_boundary':'No external PDFs newly fetched or read; original mathematical audit code was not reexecuted or fully reread; prior run scopes are read from their primary reviews/current resource objects. Comparison sources receive no done credit here.',
})

shared_comp='已全文比较统一历史身份页、恢复资料、R-0aeb原模板；实际读取现行和两冻结root的workspace_init相关函数，核四键/resume/不覆盖README合同。全仓精确actor/instance与五数学入口检索、三个精确目录inventory定位已做。实读三数学新导出原件、固定SA主稿及review、价格主稿/旧候选修正/冻结review、残余最终review和密度流review，并全文读对应正式算法/障碍/审查/计算资源。完整清单与精确指纹见read-comparison-log.json；未读外部PDF，新增数学程序运行0。'
finish='该源由父Boss5将正式target与原证据合入、检查并checkpoint后使用此receipt；内部Solver只在仓库外备稿，未调用Git/网络/clean。'
notes={
'5ae723f7d81d5b08aac0':(
'完整实读README：R-5b4a/unrelated-machines，UM-TARGET-v1 OPEN；写“两条”却实际列密度流、加权ST、固定SA三个入口，全部保留。正面共同容量/实际输出/可靠FAIL，反面真实近二compiler，以及γ→0/非局部unit-medium/增长层级下一义务完整读。',
'源不是空模板。密度流逐机计数/取整与加权ST逐机工作/+β分别比较；Q空绝对界与Q非空相对界分开。固定SA原主构造有效，后续补裸r1/T<1不能无条件sup2。三个数学原件/正式对象不互代，未凭局部层失败推出一般算法困难性。',
'retained历史接续：三结构障碍的假设、实际解码、量词/范围纠错和未交义务写入资源分节；规范数学已有承载，无新同义定理或compiler完成认定。'),
'cfb2811e522481e9692b':(
'完整实读profile四键：schema整数1、save unrelated-machines、actor R-5b4a0ff933b9452a8b008430b96a9890、instance d0515257b5844badb2b6424886976f20；与README/冻结目录一致。',
'四字段同形于已有历史容器，精确actor/instance独有；README中的三障碍、OPEN及下一步没有写入JSON，字段不提供角色/时间/分支/数学或推送认证。',
'retained：保原四值、双冻结定位和README的身份来源配对，不接管当前身份、不立数学对象。'),
'16b6164078316d041986':(
'完整实读653B/15行README：R-5d4448b5810f4d2eacbb86c644a670a2/unrelated-machines；问题/版本/表示/卡点仍占位；notes/experiments/candidates只是建议，无实际材料链接；成熟资产规范入库、私聊/已推送可见/checkpoint pushed合同完整读。',
'替完整actor后与1254c0254ceb82d8b6b7原模板字节一致；精确inventory目录仅README/profile且当前正式数学无精确身份引用，不据此断言作者在其它位置无研究。未给OPEN/CLOSED，不补造数学状态。',
'retained：合并模板共性并保独有actor/profile/指纹/来源和占位状态；没有新命题、实验、idea或实际推送证据。'),
'13683206df988f7b1837':(
'完整实读profile四键：schema整数1、save unrelated-machines、actor R-5d4448b5810f4d2eacbb86c644a670a2、instance a97e36d47c9f447db6056a783a60f001；配套README发布身份一致。',
'schema/save是通用格式路由，actor/instance不同于其余五源且不可互换；与模板和root恢复合同比较，profile不包含数学状态、当前任务授权或推送凭证。',
'retained：保精确容器原值和配对来源边界，通用恢复解释沿现资料；不执行resume、不创造数学结论。'),
'2727daf3ede34845a8d7':(
'完整实读README：历史boss3但本clone是新发布号、旧成果作者身份保留；UM-TARGET-v1 OPEN。价格凸化重构ede1392原候选剪枝/量词/参数，精确dual共同big面仅成功证书。固定R格次模、D=e(I)、动态角色2×2不继承，以及全机共同容量/可靠FAIL/总位进展下一义务全部读。',
'全文核旧minmax修正、价格主稿和冻结review：δ>3/20数值例OPT21/20>T、全β参数族、固定原T剪枝分类、剪枝sup2/未剪枝固定m锐界m、最优面所有流同big与失败无可靠拒绝。全文核残余主稿/最终review/现资源：固定R格次模、D超模；动态值2,1,1,2真OPT1/2；固定αδ图缺口e(I)、任意独立集投影但原OPT1易解，不作hardness。',
'retained历史接续：保作者归属、价格共同面条件、固定R与身份容量同步缺口、有限实现与证明边界和未交一般恢复义务；现对象承载数学，不重复立新定理或把内部审查升级外审。'),
'7b06946fabfc3dbc9216':(
'完整实读profile四键：schema整数1、save unrelated-machines、actor R-5fcc01de5a654d98b079c5c35d235152、instance 5bd5057e92284488ac30a5ea50dc13d6；与历史boss3 README新发布号一致。',
'与旧同类profile/恢复合同及2727 README比较：该profile没有旧作者映射、价格版本、证明、角色或分支字段；不得把boss3称谓或保存身份当当前Boss5/他人旧成果接管。',
'retained：完整保原actor/instance/格式及双定位，与README建立身份来源配对，不给定理数学推导边、不改当前任务。')}
receipts=[]
for sid in IDS:
    n,c,de=notes[sid];d=inventory[sid]; fp=next(x for x in manifest if x['id']==sid)
    receipt={'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
    'read_note':n+f" 原件{d['size']}B/{fp['lines']}行，SHA256={d['sha256']}，blob={d['blob']}；两个冻结commit内容相同。",
    'comparison_note':c+' '+shared_comp,'decision_note':de+' '+finish,'disposition':'retained','targets':[TARGET]}
    receipts.append(receipt);dump('receipt-'+sid+'.json',receipt)
dump('receipts.json',receipts)

body=(OUT/'resource-sections.md').read_text()
links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',body)
link_results=[]
for link in links:
    target=(ROOT/TARGET).parent/link
    link_results.append({'link':link,'exists':target.exists()})
assert all(x['exists'] for x in link_results)
dump('validation.json',{'six_original_hashes_match_inventory':True,'profile_keys_exact':all(set(json.loads((SRC/(sid+'--workspace.json')).read_text()))=={'schema','save','actor','instance'} for sid in IDS[1::2]),'template_actor_normalization_equal':True,'exact_inventory_prefix_count_each':2,'links':link_results,'missing_links':0,'new_mathematical_program_runs':0,'all_receipt_targets_same_existing_resource':True})
print(json.dumps({'six_sources':len(manifest),'related_read_entries':len(readlog),'receipts':len(receipts),'formal_links':len(links),'resource_bytes':len(body.encode()),'packet':str(OUT)},ensure_ascii=False))
