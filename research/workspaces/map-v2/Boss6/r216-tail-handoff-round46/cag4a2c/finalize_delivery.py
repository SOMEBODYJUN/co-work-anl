exec(open('/workspace/scratch/bbb425bb840f/boss6-staging/map-cag4a2c-round45/build_delivery.py').read().split('# Complete replacement')[0])
# build_delivery.py is read as task-local data/code, never imports frozen math programs.
taskrecord=json.loads((ROOT/'research/operations/map-v2/tasks'/f'{TASK}.json').read_text()); task=taskrecord['definition']
# Check only actual supplied objects; Root will finish late canonical read-add before final delivery.
newedge_by={e['edge_id']:p for p,e in new}
canonical=[
 'map/edges/ca-tail-skew-binary-four-round29-3b-5eae5b3c8b4fc5c2/ca-two-tail-skew-pays-strengthened-binary-four-certificate.json',
 'map/edges/customer-attraction-3a-3a-3cdc3f8b2e711f10/portfolio-and-diagonal-ledger-give-positive-charge.json']
canonical_data=[]
for p in canonical:
 e=json.loads((ROOT/p).read_text());assert p in registry['edge_files'];assert rr.edge_bindings(ROOT,e,objects,verify=True)=={k:e[k] for k in ['endpoint_pins','evidence_pins','review_digest']}
 canonical_data.append({'path':p,'sha256':sha((ROOT/p).read_bytes()),'edge_id':e['edge_id'],'endpoint_pins':e['endpoint_pins'],'reuse_scope':'canonical同关系、同端点pins及证据SHA精确复用；已读边完整解释及本次所需合同，不重建边、不重跑旧LP/4096型或全树。'})

p=ED/'proof-and-comparison-review.md'
s=(OUT/'mature-draft-before-source-correction.md').read_text()
s=s.replace('# 4a2c round45 数学成熟稿（原definition 27e178…，read-add待发布）','# 4a2c round45 完整数学审读与比较')
s=s.replace('任务customer-attraction-3a-3a-4a2c4758d3d07c0a，Boss6，request f08acfe6e35f48f2aed4311d9f750b8e。clone只读；原文已读范围会在最终reading-ledger分列，不把旧计算记新运行。','本稿覆盖本任务全部22核心，原文按实际version/pin实读；具体文件/section读取和成熟证据复用边界见reading-ledger.json。6条新逻辑边均独立写出完整前提和推导；2条已canonical关系精确复用。Git、队列、规范源修订由Root串行。')
s=s.replace('可accepted whole目标one-follower','新边sharp-reply-pays-deleted-slot-decorrelation完整支持目标one-follower')
s=s.replace('静态锐界peer若read-add','与已追加只读静态锐界peer')
s=s.replace('需R22 read-add，bank单独不能付真SPE及W/OPT','R22只读端点已追加；新边保ALL两个前提，bank单独不能付真SPE及W/OPT')
s=s.replace('待读canonical全文并核SHA','已读canonical全文并核全部endpoint/evidence pins及SHA，直接复用')
s=s.replace('canonical关系待精确核','canonical关系已经全文核对并精确复用')
s=s.replace('binary peer read-add后可accepted whole或明确各步骤贡献','binary peer只读追加后，新边完整给出容量/同枝五补元/实际首步等全部步骤')
s += '''

## 最终关系范围与真实未付义务

- 六条新边中五条whole：sharp→删当前槽去相关；UTP→森林逐人（conditional开放前提）；OCC→self-tax加强；ALL[统一真退出编译器,bank静态双证]→强弱差额与稳健等价；binary四尾两斜率→五人最大根全部切割。
- support-DP→count-mask DP明确是contribution，source只支付比较维度的有序/支持/重复精确性。actual转移完备性、同(k,mask)未来充分性及跨全部q汇总仍由target另外证明；普遍SM非负也并非算法正确性的推论。
- 两条canonical复用分别完整覆盖自然ρ1 portfolio费用见证，以及普通两人税在binary四尾加强证书中的作用。本次不重签它们的数学执行历史。
- 10个isolated-after-review核心均有独立的实例/目标/量词理由，未以同模型或共用定义制造关系。没有只为连通建context边；context也未计算logical覆盖。
- 两个声明follow-up均在本包实读后闭合：one-follower×static锐界只合成末两人数字保底，不能升全人数聚合；five-root×binary已由完整新边解决。in-packet DP比较不写closed_overlaps。
- R216笔误已给零上下文补丁、完整replacement及两record影响清单。当前receipt保Root实际任务当前旧核心pins，未静默修改任何规范文件；Root需先保存整包、handoff，再改source/record并交fresh窄续。
- 本worker数学程序运行0：没有旧LP、规范BI/SPE、全树IC、R291/R286穷举、4095标量或iid/两斜率旧域重跑。只做JSON/全文SHA、已存引用/标题及edge_bindings元数据验证。
'''
(OUT/p).write_text(s)

# Exact reading ledger. Full mathematical Markdown sources were read in their entirety except the two specified sections.
refs=[]
seen=set()
partial={
 'archives/customer-attraction/state/审查/R216可信攻击与森林前缀候选的证据边界增量--审查.md':('section-read','森林末位候选与有限证据；并精确定位唯一错误显示式，未声称全文读取其它数学节。'),
 'archives/customer-attraction/state/资料/个体安全和全树流独立审计的完整合同--资料.md':('section-read','匹配静态安全证书、唯一性与真实预算；核34客户另一实例及根负κ由后继补偿的比较边界，未声称全篇原数组重读。'),
 'archives/customer-attraction/tools/evidence/terminal-price-boss4/original/audit_mass_two.json':('selected-fields-and-byte-pin','完整lambda/scope/bad四行与行数160；全文件SHA核对；其它156条rows未逐项重读，成熟完整域证书按正文/原程序精确合同复用。')}
for x in task['context_plan']['reading_refs']:
 q=x['path']
 if q in seen:continue
 seen.add(q); mode,detail=partial.get(q,('full-read','本文件正文/代码/JSON全部实际阅读；旧运行记作来源证据，未执行。'))
 refs.append({'path':q,'sha256':sha((ROOT/q).read_bytes()),'reading_mode':mode,'actual_scope':detail})
for q in ['archives/customer-attraction/state/定理/自然重分配的入密度共同对角账--定理.md','archives/customer-attraction/state/障碍/最优组合真实偏离匹配不足--障碍.md']:
 if q not in seen: refs.append({'path':q,'sha256':sha((ROOT/q).read_bytes()),'reading_mode':'full-read','actual_scope':'为精确canonical复用追加的source完整陈述与全部自足证明正文。'});seen.add(q)
# Do not claim that reading the canonical edge caused every larger raw attached certificate to be reread.
ledger={'task_id':TASK,'owner':'Boss6','source_policy':'clone只读，全部生成文件在仓库外staging镜像write_paths；Python -B；无credentials/Library。','definition_pin':rr.pin(task),'request_id':taskrecord['request_id'],'core_records':[{ 'object_id':i,'version':objects[i]['version'],'object_pin':rr.pin(objects[i]),'reading':'registry完整陈述/量词/假设/objections和对应下列承重正文均已核'} for i in task['object_ids']], 'read_records':[{ 'object_id':i,'version':objects[i]['version'],'object_pin':rr.pin(objects[i]),'reading':'实读registry合同并对照实际需要的自足承重正文；附属历史大数组/代码不因列于registry而虚称已重读'} for i in task['read_object_ids']], 'files':refs,'canonical_reuse':canonical_data,'nonreading_boundary':'未逐一全文重读registry全部巨大原附件；成熟原证书按精确声明/自足承重正文和canonical合同复用。没有以字节SHA核对冒充数学全文阅读。','executions':{'new_mathematical_runs':0,'old_LP':0,'SPE_solver':0,'full_tree_IC':0,'enumerated_instance_scans':0,'metadata_only':'读取JSON、完整文件SHA256、引用唯一标题检查、rr.edge_bindings(current objects/evidence)；本地生成草稿/receipt/manifest。'}}
write(ED/'reading-ledger.json',ledger)

# Coverage is mathematical, not a uniform no-edge template.
coverage={}
def cov(i,reason,scope,edges=None):
 coverage[i]={'state':'linked' if edges else 'isolated-after-review','object_pin':rr.pin(objects[i]),'comparison_scope':scope,'reason':reason}
 if edges:coverage[i]['edge_ids']=edges
E=lambda name:'cag-4a2c45-'+name
cov(IDS['decor'],'与sharp共享真实末位松弛L，f−g展开完整得到删当前槽恒等式；当前同σ IC和minimax给v≤z≤u。另与静态锐界合得末两人≥OPT_n/(2n−1)，不能付较早玩家。','完整读去相关/sharp与static锐界；区分删当前槽C_del和保完整两槽C_full；n为全人数。',[E('sharp-reply-pays-deleted-slot-decorrelation')])
cov(IDS['sharp'],'source的L≥0可完整推出删当前槽目标；原PUSH另含曲率和PAIR/锐族。本边没有把C_full≤D当成C_del≤D，也未向多尾扩张。','完整PUSH/等号/单客户实b,t锐族/PAIR及三人D<C但u>C的不同失败层级。',[E('sharp-reply-pays-deleted-slot-decorrelation')])
cov(IDS['utp'],'开放UTP若每前缀成立，按全部有序历史、固定全游戏θ逆归纳完整给F-THETA；跨不同坏q同时拼接仍未付。','完整森林candidate，比较F-THETA、静态(S)及R216指定节，发现R216覆盖式笔误另附补丁。',[E('forest-utp-pays-individual-threshold')])
cov(IDS['forest'],'条件关系完整；静态OPT≤(2m−1)θ与W求和给条件福利2−1/m。森林结构充分拼接未证，有限探针不升定理；保旧pin并要求Root修证据SHA后fresh窄续。','全目录标签-压缩类型二部森林、UTP全终局量词、非laminar比较及全部有序历史；R216仅指定节。',[E('forest-utp-pays-individual-threshold')])
cov(IDS['gap'],'OCC同一I守恒联一次self-tax正分解完整支付G−D，D≤u仅在当前同计划IC另有时使用；后继IC无需。','OCC整文、标量4095程序合同/分数边界和来源现态资源均全文；保V+额外槽分母。',[E('occupation-conservation-pays-current-gap')])
cov(IDS['occ'],'给CURRENT-GAP结尾必需的nqᵀKp=V++I守恒，整数Δk/二元Δa保非负；另一侧pᵀKq与WD不从此得到。','完整整数计划全部p、两分数k反例域及bank紧最大元否WD的实际边界；无旧回归执行。',[E('occupation-conservation-pays-current-gap')])
cov('M-62d8b0e030534a8bb3858529bd96f65f','必要松弛负点(A,B,B)在根B的全部六可信尾都使根得≥3/2>1，故不能补成保持该actual的SPE。与同页弱占优/势反例是另一个两人三题输入，不互推，也不反VA一般命题。','单色后缀程序正文全部：31变量21行、五客户表、六尾排除、160标量恒等式与另一五客户例。')
cov('M-93710711333e4d2f8c560e1c32adabf2','完整两人(D,C)势5而静态弱占优B的B²势6，反弱占优⇒动态势最大；不能否定五人七主题的严格统一优势逆归纳唯一性，其严格条件更强。','完整B/C/D三末位表和全部根真实收益2，解析H1/H2势；与五人34点严格优势及必要点实例分开比较。')
cov('M-13cccc1cb9d1426db71b4eb0fa6a2298','六个R291有限域检查最大调和势≤W+有序复制税；与R286检查W/OPT及两输入域无直接数值推导。四题32767为全15型二值，不能混成十单/双型59048或一般定理。','完整审查/六JSON/三人归纳攻击JSON及域勘误README；未重跑2186×5或32767全集。')
cov('M-b81c224ec6ff497c985c23c85b8ee03e','R286两个来源报告域为16383全三题重数0..3、59048四题十单/双型0..2，保存9/11与8/11；旧helper缺失的复现层级不由R291成功补足。不同目标与范围不能互作证书。','全部搜索程序/报告及R286-R291审查与勘误；保来源报告身份，无新扫描。')
cov(IDS['aggregate'],'ALL编译器和bank双证完整给v′/W′/OPT′及三种不同成本；Δ0真孩子拼合完成固定(m,j)强弱桥等价。未提供严格种子或普遍付款。','完整prefix insurance与uniform/heterogeneous repair两页；区分强安全、弱充分桥、half三目标。',[E('compiler-and-bank-pay-aggregate-deficits')])
cov(IDS['bank'],'不交m块的p原始与q确定背景精确夹vbank=s；与真实编译器共同应用，bank单独不证明产品全历史SPE、W/OPT公式。','完整bank双证k1/m2边界、Cartesian静态两向原始/对偶及compiler全部首次联合退出/零端点。',[E('compiler-and-bank-pay-aggregate-deficits')])
cov('customer-attraction/six-theme-three-player-conditional-iid-payment','固定43节点σ与uniform q的63列有理恒等式完整证明条件锥W≥Z3；它不向任意σ/q外推，也不由末两人逐人静态保底补成全树iid。36点逐人失败和−5/9模板余项与总支付相容。','定理、恢复计算全文与证书24SPE/2NE/36余项全部字段；复用精确认证，不新运行发现器或258IC。')
cov(IDS['dp'],'support-DP提供已接受局部比较维度贡献；目标另外已证actual合法性和合并充分性，整个联合DP不由source单独承担。actual列L也取可变后继最小，不与保actual fixed-f/SM*混同。','全部路径DP、support peer、边界资源全文；best与bestopt、19保存项与异常/过滤范围、整数mask实现错误分别核。',[E('support-dp-supplies-path-dp-comparison-state')])
cov('CA-TWO-REMAINING-TAX','精确复用当前canonical tax→binary加强证书关系；本包新binary→五根边继续使用其原局部界。T2对非零背景只比较剩余利润，R51的最坏总覆盖下降不否定它。','T2及residual定义全文、binary两支末对六索引行和已有canonical完整解释/current pins；无旧4096型重跑。',['ca-two-tail-skew-pays-strengthened-binary-four-certificate'])
cov('customer-attraction/uniform-mass-two-slot-multiplier-newton-obstruction','固定七λ下四个负Newton行以及p1的−1/18等精确负值只否指定模板，不能推出别的乘子不存在或真实SPE失败。与T2/其它局部成功证书无矛盾，无可用新逻辑关系。','障碍全文和原1566B程序全文；JSON完整lambda/scope/bad四行、rows数量和全文SHA，未逐读其余156行。')
cov('customer-attraction/cartesian-fixed-plan-terminal-boundary-and-continuation-reset-gap','保每个旧τ动作且末位有正regret时，完整Cartesian只改旧坐标保aux必改进，故不可能。prefix compiler允许首次退出后重选旧真尾，未保坏τ，所以不被该障碍反驳；重选必须含Gdev−Gprescribed。','Cartesian障碍全文/证据README、prefix修复全文；区分保全旧计划与只保实际路径，m1末位边界含入。')
cov('customer-attraction/natural-incoming-density-covariance-and-common-diagonal-ledger-exact-regression','已canonical相同ALL关系及当前pins精确复用：86客户portfolio+共同密度账给固定ρ1未取消流C=5/4、K−W=29/38。另同实例Hall取消后NET可付，故不反NET存在或half；不能把OCC的一侧I移作此Cov信用。','自然回归、NET三例、追加portfolio与密度定理全文，canonical边全文与所有绑定核对；未复跑1842IC或旧自然流。',['cag-3cdc3f8b-portfolio-and-diagonal-ledger-give-positive-charge'])
cov('M-d13c4d43f186493fb91513a7690368b3','环静态v_n有原始/旋转对偶匹配；奇数菜单弱根尾排序比值无界，但末位改新题严格获利，所以不反真实SPE extra-one、森林UTP或全尾≥v的最小坏点R。静态锐界只有普遍下界，不能替代本精确值。','完整环障碍全文：任意固定额外槽、奇数h族、n/r/k量词、末位获利、原有限探针真实范围。')
cov(IDS['maxroot'],'binary两斜率在同一最大根真四尾上五补元平均联整数容量，完整支付四全局行、任意Q两切割与actual首步行。比较不花五份尾利润，actual首题不需最大；标量松弛仍不足half。','五根容量与binary两斜率完整正文、原13乘子/1280型完备系数证明合同；没有重跑旧域。',[E('binary-four-tail-pays-five-root-capacity')])
cov('customer-attraction/five-player-seven-topic-static-security-equality-point','固定34客户七主题输入的严格差≥3/5使全部有序历史唯一全选5；纯查询/纯背景夹v5=29/5，W=5v5、OPT34。与两人弱占优势分离不冲突，不能把该点的全背景严格性或取等扩大到其它权/人数/策略锥。','精确点、有限搜索程序全文与个体安全审计指定节（另一34客户三人输入）；无BI/LP或1470背景重跑。')
cov('customer-attraction/r51-background-worst-total-welfare-nonmonotonicity','固定两未来、e0到2e0的两份新子SPE使最坏完整总覆盖13降12；与两人税的R_b比较、其它未来利润方向或空根人数改变是不同合同，不能以同13客户互用。此背景不要求完整根实际可达。','R51全文全部末位收益表、旧唯一和新恰两份子SPE及13/12总覆盖；无4^5策略或原发现函数重跑。')
assert set(coverage)==set(task['object_ids'])

closed=[{'core_id':IDS['maxroot'],'peer_id':IDS['binary'],'reason':'实读同一1_T二值背景四尾定理，已由新边cag-4a2c45-binary-four-tail-pays-five-root-capacity完整给五补元平均、四容量行和actual首步行；无需再发布同关系3B。'}, {'core_id':IDS['decor'],'peer_id':'CA-OBLIVIOUS-MIXED-SECURITY-2N1','reason':'两全文实读后完整合成末两人逐人u≥v_n≥OPT_n/(2n−1)，n为原全人数；static只给数值基准，不证明早期玩家或W≥(n−1/2)v。此声明对已解决，普通开放聚合桥不为本对虚造followup。'}]

# Manifest excludes itself and receipt; receipt may safely list manifest as asset.
files=sorted(x for x in (OUT/ED).iterdir() if x.is_file() and x.name!='manifest.json')
entries=[{'path':str(x.relative_to(OUT)),'sha256':sha(x.read_bytes())} for x in files]
manifest={'task_id':TASK,'definition_pin':rr.pin(task),'request_id':taskrecord['request_id'],'new_files':entries,'canonical_reuse':canonical_data,'receipt_is_intentionally_not_hashed_here':True,'source_freshness':'当前原任务核心pins全部等于registry；R216证据笔误已报Root。此包保存完整成熟稿，规范源改版后需fresh窄续forest，不以本包旧pin冒充刷新后审读。'}
write(ED/'manifest.json',manifest)
assets=entries+[{'path':str(ED/'manifest.json'),'sha256':sha((OUT/ED/'manifest.json').read_bytes())}]+[{k:x[k] for k in ['path','sha256']} for x in canonical_data]
receipt={'task_id':TASK,'owner':'Boss6','request_id':taskrecord['request_id'],'definition_pin':rr.pin(task),'coverage':coverage,'assets':assets,'closed_overlaps':closed,'follow_up_tasks':[],'reading_ledger':str(ED/'reading-ledger.json'),'source_freshness':{'all_core_pins_match_current_registry':all(task['input_pins'][i]==rr.pin(objects[i]) for i in task['object_ids']),'known_source_correction_pending':str(ED/'source-correction-impact.json'),'disposition':'完整成熟旧pin稿已保全；Root先durable/handoff，随后最小修规范源及两个命中records，fresh worker窄续受影响forest core。其余21核心和无交集边可复用。'},'execution_boundary':'数学程序0；只读来源与元数据/引用绑定验证；未改clone、未Git/队列写。'}
write(Path('map/receipts')/(TASK+'.json'),receipt)
print(json.dumps({'request':taskrecord['request_id'],'definition_pin':rr.pin(task),'core':len(coverage),'read':len(task['read_object_ids']),'linked':sum(x['state']=='linked' for x in coverage.values()),'isolated':sum(x['state']=='isolated-after-review' for x in coverage.values()),'new_edges':len(new),'canonical':len(canonical_data),'new_asset_files':len(entries)+1,'receipt_sha256':sha((OUT/'map/receipts'/f'{TASK}.json').read_bytes())},ensure_ascii=False))
