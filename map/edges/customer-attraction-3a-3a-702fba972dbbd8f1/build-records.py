from pathlib import Path
import hashlib,json
D=Path(__file__).parent
REG=json.load(open('research/registry.json'));O={x['object_id']:x for x in REG['objects']}
T=json.load(open('research/operations/map-v2/tasks/customer-attraction-3a-3a-702fba972dbbd8f1.json'))['definition']
ID={
'method':'M-fd4f565640e046f8818c8a5e68c0cbb5','exact':'M-92a2a59639cc452eb152acd08231feb1',
'copy':'customer-attraction/canonical-mean-floor-domains-and-exact-copy-cost',
'bubble':'customer-attraction/adjacent-actual-prefix-bubble-background-and-net-cost',
'reset':'customer-attraction/canonical-one-shot-reset-and-nonuniform-copy-price-residual',
'chain':'customer-attraction/actual-prefix-bubble-chain-and-canonical-deficit-witness',
'mf':'customer-attraction/history-mean-floor-domain-with-frozen-actual-tag',
'raw':'customer-attraction/unfiltered-all-tail-mean-cap-collapse',
'std':'customer-attraction/pb-standard-fractional-saddle-three-real-prefix-plateaux',
'extra':'customer-attraction/pb-extra-fractional-fixed-plateau-and-local-chain-failure',
'pair':'customer-attraction/arbitrary-background-pair-extra-slot-counterexample',
'share':'customer-attraction/repeated-root-single-last-topic-one-row-share-certificate',
 'tri':'M-66828f7b1bea4fe88a0c58b5bac96899',
 'tax':'customer-attraction/true-deviation-frozen-query-signed-tax-residual',
 'join':'M-f0b8daf961564b3bb7399f1380170a07',
 'defect':'customer-attraction/five-player-shared-harm-defect-last-floor-recursion',
 'replay':'customer-attraction/fixed-entering-role-real-replay-and-once-only-potential-budget',
 'five':'customer-attraction/five-ten-label-aggregate-last-floor-integer-evidence'}
def ref(p,section=None):
    pp=Path(p); pp=pp.resolve().relative_to(Path.cwd()) if pp.is_absolute() else pp
    x={'path':str(pp),'sha256':hashlib.sha256(pp.read_bytes()).hexdigest()}
    if section:x['section']=section
    return x

def body(k):return ref(O[ID[k]]['body']['path'],O[ID[k]]['body'].get('section'))

edges=[]
def edge(slug,src,tgt,kind,conditions,roles,explanation,scope,result,remaining=None,extra_ev=[]):
    data=dict(edge_id='cag-702-'+slug,kind=kind,status='accepted',source_ids=[ID[k] for k in src],target_ids=[ID[k] for k in tgt],premises_mode='all',relation_mode='unconditional',conditions=conditions,roles={ID[k]:v for k,v in roles.items()},explanation=explanation,scope=scope,evidence=[],reviewed_by='Boss5',review_note='本轮按完整正文实读比较，逐项核陈述、量词、全部共同条件和实际可用结论；只把下列contribution局部结果记为局部，不由语境或有限记录冒全目标。')
    seen=set()
    for k in src+tgt:
        r=body(k)
        if (r['path'],r.get('section')) not in seen:data['evidence'].append(r);seen.add((r['path'],r.get('section')))
    for p in extra_ev:data['evidence'].append(ref(p))
    if remaining:data['contribution']={'result':result,'remaining':remaining}
    else:data['whole_result']=result
    path=D/(slug+'.json');path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');edges.append((path,data))

edge('fixed-cone-two-background-certificate',['method'],['exact'],'specializes',
 '固定m=2,p=5的六动作σ：根2、末层(2,2,1,2,2)。客户质量非负、所有24条非self有序IC、W=主题1与2并集质量>0；允许同覆盖及空覆盖标签。',
 {'method':'给全IC锥、包络线性化及W=1截面；末位IC使所用两个背景回复确为BR。','exact':'将通用合同具体化为明示σ的精确上界与达到点。'},
 '由通用合同，E(1)采用σ(1)=2、E(2)采用σ(2)=1且皆为真实BR包络。逐31个类型展开，(2/3)E(1)+(1/3)E(2)=(3/2)W−(1/2)Σ_{1∈s,2∉s}x_s≤3W/2，故E*=min_h E(h)≤3W/2。x_14=1给W=1且六节点24条IC均成立，五背景E=(2,3/2,3/2,3/2,2)，从而达到E*=3/2。原始/对偶目标相等；本轮从均分定义重建全部29×32矩阵，逐行、原始/对偶及reduced cost精确核同。',
 '仅这份完整σ的标签客户锥。上界仍限制覆盖互异子域，但别名达到点不证明该子域能达到；不外推其它策略、m=5或half。',
 '该明示m2/p5完整σ的正W全IC锥中，max(E*−2W)/W=−1/2；两背景凸组合给精确上界、mask14一客户给精确达到点。',extra_ev=[D/'exact-audit.json',D/'exact-audit.py'])

edge('adjacent-transport-supplies-chain-step',['bubble'],['chain'],'implies',
 '同一有限客户实例、合法actual前缀h_i、任意A及精确前缀(h_i,A,b_i)后的完整尾SPE见证；若使用价格式，两行必须在同一允许raw域、同一shadow和同一总NET-cap共同μ下。',
 {'bubble':'提供全尾有序前缀同构、删除背景相等和精确净成本/价格行差。','chain':'其单步QUERY/BUBBLE/PRICE部分获得可复用的完整尾搬运依据。'},
 '将尾策略每个有序历史(h_i,A,b_i,s)重标到(h_i,b_i,A,s)。两已占槽的总负载一致，故每个未来真实比较保持，得到下一actual前缀强制A后的完整孩子SPE。删除的都是选A的单位槽，因此ell_i(z)=ell_{i+1}(w)、d_i(z)=d_{i+1}(w)。严格更深收益和规范M相消，B_i(z)−B_{i+1}(w)=M(h_i,A)−u_{i+1}(z)；同shadow同μ给r_i−r_{i+1}=η_i−η_{i+1}+μ(M−u)。',
 '目标气泡链的局部搬运步骤，含完整离轨尾策略而非一条叶。',
 '链目标的QUERY、BUBBLE和共同价格PRICE三式逐点成立，搬运尾仍为真实完整孩子SPE。',
 '目标的任意正缺额δ真IC见证须另用规范max-min独立拼接；真正迭代还需每步重新干预当前见证，不能用固定旧Y机械重复。多源归一质量、η边界及原source银行始终未付。')

edge('nonuniform-reset-supplies-copy-cancellation',['reset'],['copy'],'implies',
 '同一完整孩子SPE见证，在其未来j>i处强制T=A后沿同一见证完成。抽取源证明中独立于价格的同主题等收益，不选择新对偶，不声称任意MF最优价格可以归一。',
 {'reset':'提供保祖先损失及(μ−λ_h)d_i(z′)残差的精确同主题代数。','copy':'其COPY收益差恒等式可从该一般残差准确特化。'},
 'reset证明首先给独立于任何价格的d_i(z′)=u_j(z′)，以及同一见证真实IC差Γ=u_j(z)−u_j(z′)≥0。将两式相加立即得到Δd_i+Γ=u_j(z)−d_i(z)。一般COPY-CANCEL准确显示：若另有λ_h=μ，该价格加权部分等于μ倍此式；本边不选择任何新最优对偶，也不把原MF对偶强行改价。',
 '目标的COPY部分，任意未来j；复制源可按任意完整孩子SPE量化。',
 '对真实复制叶，d_i(z′)−d_i(z)+Γ_j=u_j(z)−d_i(z)，且新叶进入者与复制者收益相等。',
 '目标COPY-COST和FIRST-COPY净成本界还需将全部严格后继规范盈余、中间祖先项及B_i定义一起展开；ROW-NET对偶推论另需同允许raw域和真实净cap价格。一般λ≠μ时原残差不能删除。')

edge('frozen-floor-domain-qualifies-one-shot-ledger',['mf'],['reset'],'implies',
 '固定冻结actual标签的MF域，z为一份完整孩子SPE规定叶，z′为未来单次真实偏离后同见证叶，且z,z′均为该域允许列。A≠B_i时允许任意raw尾；A=B_i时仅原实际叶，非平凡同tag改尾通常不满足此条件。',
 {'mf':'提供逐历史Δ、允许列的非负约化成本、规范源盈余以及实际标签资格例外。','reset':'在这一明确域实例中可合法使用ALL-PRICE并重构全部祖先floor账。'},
 '从MF的Δ_g(y)=1延伸g(M(g)−u_j(y))及R=η+μd+ΣλΔ−score，单次偏离前的j<k历史不变，故Δ_g(z′)−Δ_g(z)=u_j(z)−u_j(z′)；当前k给Γ；严格后继给各自尾盈余之差。逐历史求和再减两个R定义，得到目标DIFF及ONE-SHOT的精确加权式。非负R(z′)只在该允许列资格已核时可用；源I/floor/r三项仍只是同一G。',
 '仅冻结actual-tag域中的允许两端单次reset实例；全历史祖先项及各历史λ都保留。',
 '在该冻结MF域内允许的z,z′上，ΔF=Σ祖先λ收益损失+λ_hΓ+F_tail(z)−F_tail(z′)，score差=μΔd+ΔF+R(z)−R(z′)。',
 '目标的一般raw域版本须按该域重新核列资格及对偶；actual-tag改尾被删时不能套此式的R≥0，也不能免费跨行重索引并沿用原μ/λ/η或概率库存。COPY残差和多源付款须各自另核。')

edge('first-copy-gives-specific-replay-edge-cost',['copy'],['replay'],'implies',
 '真实重放的第一未来边j=i+1，目标动作恰为原进入标签A；同一完整原σ及同一固定进入角色i。若套ROW-NET对偶，还须z′为该给定允许raw域的列。',
 {'copy':'给首后继真实复制的B_i(z′)=M(h_i,A)−S_{>i+1}(z′)≤M(h_i,A)。','replay':'给定流中满足该动作条件的一类未来边可用此精确局部成本界。'},
 'REPLAY首边前叶正是finish_σ(h_i,A)，强制第一后继选A并沿同一σ完成，完全匹配复制对象FIRST-COPY。单位均分使d_i(z′)=u_{i+1}(z′)，B_i中两收益相消，严格后继S≥0，得B_i(z′)≤M(h_i,A)，并有Δd_i+Γ=u_{i+1}(z)−d_i(z)。',
 '只对第一未来动作复制A的边；不更改Q_i，也不为一般y_j推同主题结论。',
 '真实流该特定首边的净成本和复制收益工作有上述精确界，可直接代入该边的有符号净成本账。',
 '全目标仍含任意目标Q_i的流/端点/TELE。一般目标y_j≠A留下同叶d_i(z′)−u_j(z′)无定号，较晚复制仍保祖先损失；本局部界不给Cov总金额、原源容量或NET共同付款。')

edge('standard-saddle-to-extra-mass-with-pb-bridge',['std','pair'],['extra'],'transfers',
 '保同一PB客户、目录、合法b、r=2475及完整子SPE，不更改真实人数/策略；只把静态竞争质量r−1改为r，下标δ_r改为δ_(r+1)。桥为完整PB子SPE及新质量下的全目录KKT、子边际恢复和精确有理余额，均在正文及本轮audit明算。',
 {'std':'提供同一PB输入的标准自由分数鞍点与平台证明结构；其全目录singleton/梯度检查不可省。','pair':'提供同一输入的完整有序历史子SPE、前三F利润u及严格旧静态s>u。','extra':'迁移后实际得到质量r的额外分数首步平台与局部负额、固定总利润正额。'},
 '置L+=3r/Q=7425/2063∈(3,4)，p仍每段均匀1R+2D，q仍均匀3R。f(1+L+)<g(1)，H_R>12/[Q(M+6)^2]>12/(4QM²)>12/(HM²)>H_D；两singleton方向低于3dH_R且singleton查询低于Δ+，故同一凸一阶论证在全目录得δ_(r+1)(b)=Δ+=d[f(1+L+)+2g(1)]。子竞争质量r−1取θ=3(L+−1)/(r−1)=8043/2551931，hot/outside逐客户总负载都恢复L+，嵌入给反向界，故δ_r(b+F)=Δ+。PB桥给原完整策略u=3df(3)且s=d[f(1+L+)+2g(r+1)]>u；因此Δ+>s>u，局部负额u−Δ+。同一已证实际计数给U=d[9f3+1648f1+824f2+4944g2472]，本轮有理重算正差U−rΔ+，与原两完整报告吻合。',
 '这一个合法非零背景PB子SPE的静态质量迁移；r不从2475改成2476真实玩家，不能由此转实际根前缀或聚合/half反例。',
 '同一PB完整子SPE满足δ_(r+1)(b)=δ_r(b+F)=Δ+>u，extra局部链u+(r−1)δ_r(child)−rδ_(r+1)(parent)=u−Δ+<0，同时U>rΔ+。',extra_ev=[D/'exact-audit.json',D/'exact-audit.py'])

edge('extra-fractional-floor-recovers-pair-failure',['extra'],['pair'],'implies',
 '同一PB输入/合法b及r=2475完整子SPE，前两人各u；v_(r+1)为r个整数竞争槽的先承诺安全值，δ_(r+1)为质量r的自由分数值。查询者自身的一份保留。',
 {'extra':'提供精确全目录自由分数下界δ_(r+1)=Δ+>u及同一完整策略的前两人利润。','pair':'恢复该任意合法背景pair桥的严格失败结论，但不冒用其单独s公式证书。'},
 '对任意整数竞争元组的混合Q，平均负载属于质量r的自由目录凸包；逐查询倒数Jensen给max_T E_Q payoff≥max_T payoff(平均负载)≥δ_(r+1)。有限minimax因此v_(r+1)≥δ_(r+1)=Δ+>u。两位实际利润同为u，得到u1+u2=2u<2v_(r+1)。也可用extra的固定p convex KKT下界逐个整数元组推出同一先承诺保证。',
 '精确否定每个合法背景/每份完整子SPE的前两人extra安全值付款桥；不把背景合法性当根实际可达性。',
 '用更强分数鞍点保证恢复PB的pair失败结论2u<2v_(r+1)(b)，量词及r槽一致。',
 '目标登记还明示其较弱s=d[f(1+rk/Q)+2g(r+1)]的逐层Jensen证书和完整G/P/F模式构造；这些细节由PB正文独立维护，不能仅从Δ+>u倒推s>u或假称本边重新展开巨大树。',extra_ev=['archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md'])
edge('real-replay-represents-signed-tax-work',['replay'],['tax'],'implies',
 '限目标签名税恒等式的完整纯SPE情形。对每行i分别应用重放定理：p_i为确定标签T_i，Q_i为y_i=(actual_{<i},T_i,actual_{>i})的单点；该冻结尾叶仅是分析终点，raw域必须允许它。每行固定势Φ_i(z)=d_i(z)。',
 {'replay':'给每行从同一原σ真实查询源到任意指定raw叶的逐未来真实IC路径及任意固定势TELE。','tax':'其D=Σ(f_i−q_i)获得逐真实未来边的精确有符号工作表示。'},
 '第i行原源z_i=finish_σ(actual_{<i},T_i)的进入收益是q_i；选定raw终点y_i的进入收益是冻结查询f_i。真实重放逐未来角色将源尾改成actual尾，进入标签始终T_i，所以最终enter标签边是恒等且Δd_i=0。TELE取同一固定Φ_i=d_i，得f_i−q_i=Σ_{j>i}[d_i(z_i^j)−d_i(z_i^{j−1})]。各行相加即D为这些真实路径上的有符号进入收益工作；每个j边另有原σ的整人Γ_j≥0，但Γ_j属于未来角色j，不能据此给进入者Δd_i固定符号。',
 '任意合法m标签比较元组的SPE版签名税；各行分别以确定查询应用，不要求所有T_i相同或将冻结叶冒作可信孩子SPE。',
 'D=Σ_iΣ_{j>i}Δd_i可用同一原σ的真实未来偏离路径精确表示，终点正是目标定义中的冻结查询；所有中间边保真实有序IC。',
 '目标对任意非SPE策略也成立的RES代数、静态S≥0及D≤S充分付款仍由其独立证明维护。本边不给D的上界，不可把未来角色Γ_j≥0误作进入者Δd_i≥0，也不合并互斥分支银行。')

print(json.dumps({'edges_written':[str(p) for p,_ in edges],'count':len(edges)},ensure_ascii=False))
