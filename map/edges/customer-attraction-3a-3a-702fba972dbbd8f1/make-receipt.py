from pathlib import Path
import json,hashlib,sys
D=Path(__file__).parent
ROOT=Path.cwd()
T=json.load(open('research/operations/map-v2/tasks/customer-attraction-3a-3a-702fba972dbbd8f1.json'))['definition']
O={o['object_id']:o for o in json.load(open('research/registry.json'))['objects']}
P=T['input_pins']
def ref(p):
 p=Path(p);p=p.relative_to(ROOT) if p.is_absolute() else p
 return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
edges=[]
for p in D.glob('*.json'):
 x=json.loads(p.read_text())
 if isinstance(x,dict) and 'edge_id' in x:edges.append((p,x))
reuse=Path('map/edges/customer-attraction-3a-3a-022eb352950d4307/five-player-last-floor-defect-regime.json')
rs=json.loads(reuse.read_text())
K={
 'M-fd4f565640e046f8818c8a5e68c0cbb5':('fixed-cone-two-background-certificate','通用完整有序IC/计数包络合同与指定m2/p5证书逐式比较；线性化依全部末位IC，明确固定σ而非只按路径。','得到该具体固定标签锥的完整精确特例−1/2，原29×32全矩阵及原始/对偶均按定义复核；未把随机阴性外推所有σ。'),
 'M-92a2a59639cc452eb152acd08231feb1':('fixed-cone-two-background-certificate','完整六动作、31类型、29行客户锥，与通用E*合同及两个背景凸组合比较。','整个注册目标的精确上界与mask14达到点均成立；覆盖互异子域上界有效，当前别名点不证该受限域达到。'),
 'customer-attraction/canonical-mean-floor-domains-and-exact-copy-cost':('nonuniform-reset-supplies-copy-cancellation','任意未来复制j的COPY/COPY-COST/FIRST-COPY，与非均匀RESET、冻结MF域、真实首边及气泡净成本比较。','接受来自一般reset的COPY局部代数及向真实流首边的成本贡献；j>i+1中间祖先项不能删，M(h_i,A)−u_i不预设非正，域变化不可免费统一价格。'),
 'customer-attraction/adjacent-actual-prefix-bubble-background-and-net-cost':('adjacent-transport-supplies-chain-step','完整尾策略按有序前缀同构搬运、删除同A槽、B_i及r_i行差，与正缺额链及真实流的源合同比较。','精确支持链的局部QUERY/BUBBLE/PRICE；不把新尾当原σ，不为到达下一行后重领source质量、I/S/r或η归一库存。'),
 'customer-attraction/canonical-one-shot-reset-and-nonuniform-copy-price-residual':('nonuniform-reset-supplies-copy-cancellation','全部祖先floor及源/目标tail盈余展开、同一允许raw域对偶、COPY-CANCEL残差，与冻结MF资格及统一净成本复制比较。','两个已接受局部贡献分别核COPY代数特化和冻结MF域合法reset；μ≠λ_h时(μ−λ_h)d_i(z′)必须保留。'),
 'customer-attraction/actual-prefix-bubble-chain-and-canonical-deficit-witness':('adjacent-transport-supplies-chain-step','实读相邻搬运、规范max-min/IFF、δ正/非正拼接及每步当前见证干预—搬运至末位的完整链；按指定overlap对比原真实流。','相邻同构确实供给链的局部步骤；正缺额有另构真正孩子SPE的精确IC差，却不属于原σ银行。链的多源到达容量/η边界付款未证，保开放义务而非身份不清。'),
 'customer-attraction/history-mean-floor-domain-with-frozen-actual-tag':('frozen-floor-domain-qualifies-one-shot-ledger','冻结actual-tag的原MF及FLOOR-CREDIT全部证明，与释放tag MF、ROW-NET、共同NET、单次RESET及真流允许端点比较。','在该冻结域内允许两端时给目标one-shot精确实例；A=actual改尾通常被删，需新域或重索引并重核价格和银行，不能静默把原对偶套到所有raw。'),
 'customer-attraction/pb-standard-fractional-saddle-three-real-prefix-plateaux':('standard-saddle-to-extra-mass-with-pb-bridge','标准质量r−1的全目录鞍点、j0..3恢复边际及三个真F节点，与PB完整子SPE、extra质量r及两标量/四层报告比较。','经同一PB全历史桥和明确静态质量映射得到extra完整目标；Δ>Δ+，故单看较小extra的U余额不能付标准，正文独立Taylor界和本轮有理核确认标准U>rΔ。'),
 'customer-attraction/pb-extra-fractional-fixed-plateau-and-local-chain-failure':('standard-saddle-to-extra-mass-with-pb-bridge','完整PB原证明/四审查、extra原MD/顶层py/两JSON与正式计算页全读；核r槽/质量r、KKT singleton及θ8043/2551931。','迁移边完整得到extra注册结果，另经Jensen恢复整数extra pair失败结论的局部贡献；局部负额不反aggregate、actual根弱化或half。'),
 'customer-attraction/true-deviation-frozen-query-signed-tax-residual':('real-replay-represents-signed-tax-work','精确逐客户带符号税、RES和437非SPE校准，与原真实流TELE、固定进入收益势及各行确定查询比较。','真实重放可把SPE情形的D表示成同原σ真实未来偏离路径的有符号Δd_i总功；这不控制其金额，Γ_j属于后继人而不是进入者。D≤S仍是严格未付充分预算，D≤S+ΣΓ仍只重述目标。'),
}
coverage={}
for oid,(slug,scope,reason) in K.items():
 ids=[x['edge_id'] for p,x in edges if oid in x['source_ids']+x['target_ids']]
 coverage[oid]=dict(state='linked',object_pin=P[oid],comparison_scope=scope,reason=reason,edge_ids=ids)
isolated={
 'customer-attraction/unfiltered-all-tail-mean-cap-collapse':('原SAFE完整IC、全复制raw生成元、双包含及零μ最优对偶完整证明；比较冻结MF、释放MF、ROW-NET/总NET和真实流全部允许列条件。','全raw且仅进入均值cap才精确塌缩；全复制生成元不保证未来floor/NET可行，冻结actual标签还会删掉actual全复制叶。故此等式/μ=0选项不能迁移成包内MF/NET或真实流金额结论；当前未发现支持这些整目标的逻辑边。只有具体给出另一域每个生成元仍可行才可接续，不新造一般比较任务。'),
 'customer-attraction/repeated-root-single-last-topic-one-row-share-certificate':('单行根IC的四类逐坐标恒等式、m≥3任意位界、五个保存σ根B真路径及完整等号点；全读对应程序/计算页、原审计代码和五解析证书，另定义重建9σ/5种子38060非self IC。','本包其它锥方法优化的是E*，不能仅因同用全部有序IC就导出本份额目标；双祖先cap存在量词也不推出指定五σ全锥锐性。五保存策略结论本身完整成立且可独立复用，未把general C2、四joint锥或half列作该条件引理的结果。'),
 'M-66828f7b1bea4fe88a0c58b5bac96899':('一般非负严格三角盒系统greedy最大点、首失败λ及C(λ)=z_j<0完整证明；比较包内真实流、气泡多源库存缺口及正文给出的固定来源路由应用公式。','一般算法真实成立，但包内尚未构造具有真实owner退款、严格未来非负K及同一共同cap的固定付款数据，不能把它直接接成原SPE或Cov付款。t非负/三角、初始资金和路由是必须先付的数学输入；λ≤1只在应用行和条件下成立。固定来源对象有明确后续位置，本包不另发无数据的新工作。'),
 'M-f0b8daf961564b3bb7399f1380170a07':('R28审查§3、verify_join_conflict.py全文及完整JSON；明确分开CAG两单例末位(A,B)和generic匿名表。比较气泡的换见证拼接、逐叶/均值域及五份结构性share界。','CAG末BR向量(1/2,1)/(1,1/2)准确否定分别存在⇒共同存在；这不否定气泡所用不同有序子树独立拼接，也不否定MF均值可行，更不提供general CAG full/Markov终局分离。正文错归generic的句子已由round50精确更正，本文delta逆替换核同旧SHA；registry核心身份/陈述未改，当前比较范围没有成立逻辑边。'),
}
for oid,(scope,reason) in isolated.items():coverage[oid]=dict(state='isolated-after-review',object_pin=P[oid],comparison_scope=scope,reason=reason)
oid='customer-attraction/five-player-shared-harm-defect-last-floor-recursion'
coverage[oid]=dict(state='linked',object_pin=P[oid],comparison_scope='实读全历史ε定义、倒二两尾基点、最后损害者逐层递推及目录粗界；追加完整实读5945客户十标签正文与原py/JSON，并复用已发布022边。比较本包无floor塌缩、signed税及一般三角算法，均不丢失缺陷资金。',reason='canonical局部关系精确校准该真实输入缺陷账4186>θ/2=1115/2；无条件DEFECT下界1389与实际5567相容。保递推本身正确，不能省略全历史ε或将等大小主题ε2=0扩大成全部ε=0。没有重跑111110比较的成熟原审计。',edge_ids=[rs['edge_id']])
assert set(coverage)==set(T['object_ids'])
closed=[]
for o in T['context_plan'].get('overlap_comparisons',[]):
 if o.get('status')!='follow-up':continue
 core,peer=o['core_id'],o['peer_id']
 if peer=='customer-attraction/arbitrary-background-pair-extra-slot-counterexample':
  why=('PB完整全历史策略是两平台共用的存在性桥；extra→pair边按质量r的t≤v严格恢复2u<2v，范围保持合法背景。' if 'extra-fractional' in core else '标准平台完整比较了PB全历史桥；r−1与r质量不能互换。显式标准+PB→extra迁移及extra→pair局部结论已完成具体索引比较。')+'两者的完整目录/背景/真实续局及所有singleton条件已实读，无剩余需要另发3B的比较；未把此离轨背景当actual根路径。'
 else:
  why='同一完整σ的真实流、允许域、原源银行已逐式比较。'
  if 'bubble-chain' in core:why+='链每步更换当前孩子见证，原真实流固定最初σ，故不能互认原source容量；局部搬运已给逻辑贡献，联合容量仍是明确开放数学。'
  elif 'adjacent' in core:why+='相邻搬运保删除背景/净成本行差，但不能自动保下一行原source或η质量；本包对应局部贡献准确完成比较。'
  elif 'canonical-mean' in core:why+='首copy真实边成本已有accepted局部关系；任意目标非copy同叶残差仍无定号，未把copy工具冒全流付款。'
  elif 'history-mean' in core:why+='冻结actual-tag例外可排除真流中间改尾，原MF与释放raw总NET的对偶/银行不同；one-shot受限实例已精确给出，不能静默迁移整个流。'
  elif 'unfiltered' in core:why+='无floor塌缩的生成元不保证NET/floor，μ=0只是该最粗域一个最优选项；不反真实流恒等式或其它域，不发重复语境比较。'
 closed.append(dict(core_id=core,peer_id=peer,reason=why))
assets=[ref(p) for p,x in sorted(edges)]+[ref(reuse)]+[ref(D/p) for p in ['exact-audit.py','exact-audit.json','reading-progress.md','delta-review.json','remote-task-check.json','published-input-check.json','edge-validation.json']]
receipt=dict(coverage=coverage,assets=assets,follow_up_tasks=[],closed_overlaps=closed,reviewed_by='Boss5',reading_boundary='前次连续阅读已完成全部指定正文及所需唯一section；本次只核round50三页精确delta、当前19输入pins及最新已抓取远端44文件blob，不全文重读、不重跑已过数学oracle。两个大型数值证据JSON的重复矩阵/portfolio数组未冒逐字目视，而由前次结构核与定义重建完整矩阵、全部九σ/五种子IC及五逐类型证书校验。原程序、发现LP/MILP及规范SPE solver未运行。任务500K是official-default规划值，当前运行窗口与剩余未知。',mathematical_open_obligations=['真实流自适应Cov金额及原source/多源容量/跨行η共同付款；不是本包身份待决。','固定三角修复需实际合法初始付款和路由输入，算法不保证所有SPE成功。','五人DEFECT的小缺陷账不是一般输入前提；已有五人half由另证，不由本包各工具相加。'],draft_note='等待Boss源勘误/任务pins刷新后重建refs、edge-bind与edge-check；此字段在最终交付前更新。')
if '--final' in sys.argv:
 receipt['draft_note']='正文勘误与任务输入已按当前版本刷新；8条新逻辑边逐条绑定/检查，canonical局部边精确复用，收据assets采用最终字节SHA。数学开放付款义务保留为开放，不作身份待决。'
out=Path('map/receipts/customer-attraction-3a-3a-702fba972dbbd8f1.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'receipt':str(out),'coverage':len(coverage),'linked':sum(x['state']=='linked' for x in coverage.values()),'isolated':sum(x['state']=='isolated-after-review' for x in coverage.values()),'new_edges':len(edges),'reused_edges':1,'closed_overlaps':len(closed)},ensure_ascii=False))
