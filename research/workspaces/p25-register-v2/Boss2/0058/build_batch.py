"""Boss2/0058 semantic registration; assignments below are explicit mathematical judgments."""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TASK = 'register-ab98f323ad-0058'
definition = json.loads((ROOT / f'research/operations/p25-register-v2/tasks/{TASK}.json').read_text())['definition']
refs = definition['materials']
ids = json.loads((Path(__file__).parent / 'new-ids.json').read_text())['object_ids']
objects, materials, routes = [], {}, []
MODEL = '有限单位客户、有限非空共同标签目录、单位提供者依全部有序历史各选一次；终局客户在覆盖者间均分；保空覆盖、重复、覆盖别名和弱平局。'

def ref(path, section=None):
    p = ROOT / path
    out = {'path': path, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    if section: out['section'] = section
    return out

def page(i):
    s = (ROOT / refs[i]['path']).read_text()
    m = re.search(r'^id:\s*["\']?([^"\'\n]+)', s, re.M)
    return m.group(1).strip() if m else None

def sources(i):
    s = (ROOT / refs[i]['path']).read_text()
    return list(dict.fromkeys(re.findall(r'source:[^"\n]+', s.split('---', 2)[1] if s.startswith('---') else s))) or [refs[i]['path']]

def own(i, oid, title, kind, status, statement, quantifiers, assumptions=(), scope='', objections='', ev=()):
    obj = dict(object_id=oid, version=1, title=title, kind=kind, truth_status=status,
        model=MODEL, statement=statement, quantifiers=quantifiers,
        assumptions=list(assumptions), scope=scope or '仅陈述中限定的输入、比较量与完整策略范围。',
        objections=objections or '复用已整理的自足论证；本次核精确陈述、条件与证明位置，未重新执行原数学程序。',
        body=dict(refs[i]), evidence=[dict(refs[j]) if isinstance(j,int) else j for j in ev], sources=sources(i))
    objects.append(obj)
    row=materials.setdefault(i,dict(refs[i], disposition='objects',object_ids=[],reason=''))
    row['disposition']='objects';row['object_ids'].append(oid)
    row['reason']='实读本页成熟陈述及所列承重论证，按独立数学身份分列；正文完整保留，不把其有限日志另造节点。'
    return obj

def attach(i, owners, reason):
    materials[i]=dict(refs[i],disposition='attachment',object_ids=list(owners),reason=reason)
    for o in objects:
        if o['object_id'] in owners and refs[i] not in o['evidence']: o['evidence'].append(dict(refs[i]))

def pending(i, reason, owners=()):
    materials[i]=dict(refs[i],disposition='needs-decision',object_ids=[],reason=reason)
    routes.append(dict(material_index=i,material=refs[i],requested_owners=list(owners),reason=reason))

own(0,page(0),'真实偏离、冻结查询与覆盖松弛的带符号税恒等式','identity','proved',
    '任意完整策略及任意m索引合法比较元组，q_i为真偏离收益、f_i为冻结替换收益，D=Σ(f_i−q_i)、Γ_i=u_i−q_i、S=W+Σf_i−|∪T_i|≥0，则2W−|∪T_i|=ΣΓ_i+S−D。完整SPE才给Γ_i≥0；D≤S是half充分加强，D≤S+ΣΓ仅重述目标。逐节点真实税为Σ_T d_x/[(b_x+1)(b_x+1+d_x)]。',
    '每个m≥1、每份完整有序策略、每个合法比较m元组；非负IC部分另要求该策略为完整纯SPE。',
    scope='签名税不能逐项截正；437客户正规式NE的同点只是公式校准，不是SPE反例。')
own(1,page(1),'五人全历史共享损害缺陷的逐人末位保底递推','lemma','proved',
    'θ=min_{h∈L⁴}max_TΣ_T1/(b_h+1)。ε_j遍历所有j步历史和受第j人严格损害的旧人，取加入后I_j−I_i的正部最大值，E=max(ε4,ε5)。任意完整SPE有u4,u5≥θ,u3≥θ−E,u2≥θ−ε3−E,u1≥θ−ε2−ε3−E，因此W≥5θ−ε2−2ε3−3E≥5θ−6max ε_j。并有ε_j≤max_{A∩B≠∅}(|B∖A|−|A∖B|/(j−1))_+，j2为等式。',
    '每个五人输入、全部完整纯SPE及全部离轨前缀；缺陷最大值须取全历史而非实际路径。',
    scope='缺陷账≤θ/2再结合θ≥OPT5/9才给条件half；等大小主题只保证ε2=0，不删除后续缺陷。')
own(2,page(2),'5945客户十标签完整策略严格违反五倍聚合末位地板','counterexample','proved',
    '正文给365正兴趣型、5945单位客户的整数输入与读取第二行动组的全历史策略：根X0，第二人取反组最小fresh，以后跟第二行动组最小fresh。成熟精确全树审计给actual X0Y0Y1Y2Y3，收益(1107,1115,1115,1115,1115)，W5567、θ1115、OPT5=5575，故W−5θ=−8而2W−OPT=5559>0。',
    '存在该精确五人十标签实例及所述完整有序历史纯SPE；不量化任意浮点重数。',
    scope='保该特定整数输入/策略证书的独有身份；一般n≥3反族另有主owner。本对象不是half反例。',
    objections='复用成熟11111历史/111110含自身比较的精确审计；未将发现器浮点轨道向量当整数实例或新跑全树。')
own(3,page(3),'两组对称轨道总质量上的完整fresh策略锥压缩','algorithm-guarantee','proved',
    'n≥2,K≥n，两组各K标签、交换组与组内置换对称的非负客户轨道总质量。根任取、第二人反组fresh、以后跟第二行动组fresh。该完整有序策略为SPE当且仅当正文枚举的全部负载分拆压缩真实IC行成立：深度d≥2保指定组、两组完整正负载分拆与每种重复/fresh行动类，另保第二人两类非平凡偏离。收益系数由包含当前标签的子集负载DP精确Fraction平均；轨道变量是总质量，非每mask重数。',
    '每个n≥2、K≥n、群对称非负有理轨道质量、每份满足规则的确定fresh选择器；须检查全部精确行。',
    scope='有限235条float报告只作发现记录；该算法表示定理不授打印点精确可行或一般策略净化。')
own(4,page(4),'实际相邻角色的单题冻结替换查询付款候选','conjecture','open',
    '固定任意合法背景、余r≥2人的完整纯SPE实际叶，q_i(T)=Σ_{x∈T}1/[L_x+1−1_{S_i}(x)]为移去i且冻结其余actual动作的查询。候选为每个i<r及每个合法T都有q_i(T)≤u_i+u_{i+1}。末对与r2已由末位锚闭合，早期相邻对一般仍未付中间静态premium。',
    '所有合法背景、所有剩余人数r≥2、每份完整纯SPE、每个相邻i和每个合法单题T。',
    scope='不等于存在最优元组匹配总费、FTA额外槽或已被PB否定的强首对安全桥。')
own(4,ids[0],'冻结角色转移的精确客户差与真实末位锚','lemma','proved',
    '任意合法叶及任意i,j,T，q_i−q_j=D⁺_ij−D⁻_ij，其中D⁺=Σ_{T∩(S_i∖S_j)}1/[L(L+1)]，D⁻反向，且D⁺≤u_i/2。完整子SPE末位有q_r(T)≤u_r，故q_i(T)≤u_r+u_i/2。任意相邻对的付款差=(u_i−D⁺)+(u_{i+1}−q_{i+1})+D⁻，中间项可负。',
    '任意合法背景/叶/查询的转移恒等式；最后一步锚要求真实末位BR。',
    scope='同一u_r不能在所有早期对中重复计作公共库存；旧两人/PB审计仅该引理的特例。')
own(5,page(5),'静态插入与真实后继债务的两松弛精确总账','identity','proved',
    '固定完整SPE actual负载c及最优m元组。f_c(T)=Σ_T1/(c+1)，δ_i=Σ_{T∩A_i}1/[c(c+1)]，冻结替换q_i=f_c+δ_i，真实收益d_i，R_i=q_i−d_i可带符号。令V=Σ_{c>0}1/(c+1)，Ecov=W−V+Σf_c(T_i)−OPT≥0，SIC=Σ(u_i−d_i)≥0，则2W−OPT=V+Σδ_i−ΣR_i+Ecov+SIC。',
    '每个m≥1输入、完整纯SPE与固定最优索引元组；相同代数对任意元组用其并集成立。',
    scope='ΣR≤V+Σδ只是充分加强，不与half等价；精确等价必须保Ecov和SIC。与签名税对象保独有信用分解。')
attach(6,[page(5)],'R24入口的实际数学归本批债务总账；纯导航/旧身份不造对象。其余PB与有限扫描分别在本批对象准确定位。')
own(7,ids[1],'首位extra-one桥的最小人数坏点正规形及二主题闭合','lemma','conditional',
    '若u1≥v_{r+1}(b)有按剩余人数最小的失败，令t=v_{r+1}(b)>u，则每个根强制A的真实枝根收益d_A≤u，每个后继收益≥t，任一后继主题的根外收益≥t−d_A>0。固定项静态嵌入使该归纳成立；至多两个目录主题时互补主题迫d_A≥t矛盾，余两人任意目录亦成立，故最小失败至少r3且至少三主题。',
    '对一个按剩余人数最小的合法背景坏点，全部根行动及同σ真实后继；二主题闭合对全部合法背景。',
    assumptions=['v_{r+1}是允许r槽不观察查询的真正静态安全值；不能换成受限真实尾菜单值。'],
    scope='后续银行m4零根族已否一般extra-one；本条件正规形与小目录结论保留，不将互斥枝outside信用求和。')
own(7,ids[2],'最差首位SPE收益不按固定合法背景单调嵌入','counterexample','proved',
    '两不交主题A3客户、B2客户，余两人零根唯一SPE根选A、末位B，最差首益M2(0)=3；合法前缀A后余一人最佳收益M1(1_A)=2。因此M2>M1，不存在所拟固定项背景单调嵌入。',
    '存在该两主题两人输入；M是最差完整SPE首益而非静态minimax值。',
    scope='不反静态v的固定项嵌入，不反half。')
own(8,page(8),'全部真实PB标量行的精确线性最小值','obstruction','proved',
    '只保u_i≥0、P_i=Σ_{j≤i}u_j及O≤P_{i−1}+m(m−i+1)u_i，m≥2,O>0，则min W/O=1−∏_{r=1}^m(1−1/(mr))=:F_m(m)。逐行等号向量达到下界；F2=5/8,F3=41/81，所有m≥4严格低于1/2，且F_m(m)~H_m/m→0。',
    '所有满足该抽象标量系统的非负向量；不是所有向量均可由真实CAG完整SPE实现。',
    scope='排除只用这些行的非负组合/标量势证明half；不能登记成CAG坏均衡。')
own(9,page(9),'任意主题包截断最大覆盖质量的真实前缀包络','lemma','proved',
    '任意可覆盖客户集C、非负合法主题包z，τ=Σz>0，a_x=Σ_{T∋x}z_T，M_C(z)=Σ_C min(1,a_x)。在任意actual位置、余r人、过去最终利润P，同一完整SPE有M_C(z)≤P+rτu_i。有限LP质量曲线M_C(q)=max_{Σz≤q}M_C(z)给所有q>0的P+rqu_i≥M_C(q)，以及u_i≥sup_q(M_C(q)−P)/q/r。',
    '每份完整纯SPE、每个actual位置、任意C与任意非零实权合法主题包；不要求包完整覆盖C。',
    scope='主题权是比较工具，不是隐藏行动/分数客户游戏；每个位置包可不同但利润始终同一actual叶。')
own(9,ids[3],'高分数覆盖数不控制真实单位质量或合法子集路由','counterexample-family','proved',
    '每题一私有客户加L共同客户，或无全局共同核心、每题一私有且每个H_j有L客户归除j外全部题，均有τ_C=s而最优私有对偶总重仅s，真实质量可任意大。另N=km的全部k元子集目录有τ_C=m、无全局私有且有m不交比较块；当m≥k合法题可跨k块，k无统一常数界。',
    '上述每个整数s,L或k,m参数域的静态单位客户目录。',
    scope='两个独立受否推理均是从高τ推出质量/路由结构；不声称坏SPE。')
own(10,page(10),'查询重数细化的同叶前缀预算与单会员遗漏门槛','lemma','proved',
    '任意q索引合法查询并集O，actual并集U，C=|U∩O|，J=Σ_{x∈O∖U}d_x，则每个actual位置C+J≤P_{i−1}+qru_i，从而W≥[1−∏_{r=1}^m(1−1/(qr))](C+J)。m=q5最优元组给OPT5≤10837W/6049+[D1−E−Σ_{d≥3}(d−2)D_d]/2。K5保险十查询J=4L给4L+F≤4000000W/841117。',
    '每个m≥1、q≥1、完整纯SPE及任意允许重复的比较元组；五人及K5系数仅相应特定域。',
    scope='单会员只相对所选比较元组，非全目录私有；原五行对偶分母二倍标度勘误已正文保留。')
own(12,page(12),'五个全新整块在严格银行价下的真实两尾不交配对','lemma','proved',
    '任意合法前缀后恰余两人，五个不交经济整块各ℓ>0且全新，目录恰有全部K5双块配对、其他题至多单整块。以旧银行价Σ1/(q_x+1)计，单块题<ℓ、纯银行<2ℓ、配对<ℓ/2。则每份完整两尾SPE两位均选经济索引不交配对，各经济收益2ℓ、总收益≥2ℓ；所有真实末位BR都满足，不固定有利平局。',
    '全部满足严格价界的参数输入、合法前缀与该子博弈全部完整纯SPE。',
    scope='不可改弱价界或切割经济块；前缀不必是零根SPE的actual。')
own(12,'customer-attraction/fresh-pair-bank-insurance-share-bounds','配对保护下旧银行同叶的一次/两次保险份额','lemma','proved',
    '保严格价配对保护全部前提。旧纯银行玩家B的每客户负载q_x≥1，F_B为属于至少一个配对的B客户。若每银行客户至多挂一配对，旧收益≥Σ_{B∖F_B}1/q_x+Σ_{F_B}1/(q_x+1)；任意配对关联仍≥Σ_{B∖F_B}1/q_x+Σ_{F_B}1/(q_x+2)。',
    '全部配对保护输入与旧银行玩家；单挂只用于一次覆盖式。',
    assumptions=['本页前节全部严格价界及完整两尾SPE；保所有银行客户的原负载。'],
    scope='是同一实际两尾叶份额，不假设所有保险客户都被触及。')
own(12,'customer-attraction/287-client-k5-pair-point-late-deviation-exclusion','287客户K5必要点的真实后期偏离排除','obstruction','proved',
    '正文14正类型的20标签287客户点，目标ABCDE收益(12,15,20,30,60)、W137、OPT5=287。第三位前缀A0A1强制A4后，严格价配对引理迫两尾选不交纯经济配对，使其收益恰60>20；第四位同样强制A4得60>30，故该目标不属于任何完整SPE。25标签295客户specialist变体亦满足这些严格界，第三位仍60。',
    '这两个明确整数输入的指定目标；不量化一般保险修复或所有新增奖励。',
    scope='根/第二门槛45与最差福利233属历史BI另证；本对象只保解析后期排除。',ev=[11])
own(13,page(13),'单挂唯一旧整银行的严格三分之一保护','lemma','proved',
    '五全新经济整块各ℓ>0、全部K5配对，旧纯银行B大小整数0<b<3ℓ且每客户旧负载恰1。每B客户至多挂一配对，各配对银行仅来自B；覆盖整个B的非配对标签仅B自身，其余题至多一个完整经济块。则所有完整两尾SPE使旧B玩家u_B>b/3并有u_B≥b/3+1/6。',
    '全部满足窄目录、单挂、唯一整银行及无额外配对奖金前提的合法前缀/完整两尾SPE。',
    scope='不需小价格且不保证尾配对不交；与严格银行价引理前提不同，不吞成一个命题。')
own(13,'customer-attraction/single-bank-three-block-size-tie-threshold-example','b=3ℓ时三分之一银行收益可取等的完整局部SPE','counterexample','proved',
    'ℓ1、五经济单客户、B3客户，目录为B与十K5配对，只有R01附全部B。合法前缀B后余两人，当前R01、每个当前行动后的末位恒R01；正文逐全部11种当前行动及末位BR比较证完整SPE，未来(R01,R01)各得2，旧银行恰1=b/3。',
    '存在该八客户11标签局部子博弈及所给全部11个末位处方。',
    scope='反严格保护扩展到b≤3ℓ；未将前缀B认证成五人零根actual，不是half反例。')
own(17,'B2-COLLISION-FREE-RESPONSE-DEFECT-v1','实际不交叶的真实响应缺陷交换恒等与条件福利界','lemma','proved',
    'm=k+1完整SPE actual(C1,…,Ck,D)两两不交。任意i,T的真实末位R，F_{t,r,d}(h)=(r−t)/(h+t+r)−d/(h+t+1)，第一项t=r时取0；Δ=Σ[F(h′)−F(p)]。L_{i,T}=|T∖U|+|T∩Ci|+|T∩(U∖Ci)|/2，则3|Ci|/2−L=g_i+g_R+g_D+|Ci∖R|/2−Δ。对最优m元组全查询和Δtot，有OPT≤β_kW+(2k+1)Δtot/[2(k+1)²]，β=(8k²+11k+4)/[4(k+1)²]。',
    '全部实际不交完整SPE、每个实际早期位置和合法查询；Δtot针对一个固定最优索引元组。',
    scope='Δtot≤(5k+4)W/[2(2k+1)]为half充分条件，不是一般已证预算；不等于只比较查询者的R债务。',ev=[18])
own(17,'B2-UNIFORM-RESPONSE-DEFECT-BUDGET-NO-v1','完整无碰撞策略的全查询响应缺陷对福利比无界','counterexample-family','proved',
    '每k≥2有正文Q/B可信子树粘合的m=k+1人完整SPE，目录Aj=Xj+aj,Bj=Xj+b,Cj=Xj,D={b,d}，|Xj|2，actual C1…CkD。W=2k+2，唯一最优计数A1…AkD覆盖3k+2。对任意最优排列Δtot=k(k−1)/2，故Δtot/W无界；阈值首次k7失效(21>104/5)。',
    '每个整数k≥2存在该全历史策略；每个最优索引排列给同总和。',
    scope='反所有固定C的Δtot≤CW；仍OPT/W<3/2，不反half或选定一对一查询预算。',ev=[18])
attach(18,['B2-COLLISION-FREE-RESPONSE-DEFECT-v1','B2-UNIFORM-RESPONSE-DEFECT-BUDGET-NO-v1'],'精确审计分别为响应恒等/无界全查询族提供有限证据；冻结条件定理的外主owner另待接证，不以3078查询或PASS造节点。')
own(24,page(24),'等重全非空客户型的任意完整fresh处方均为SPE','construction','proved',
    '1≤m≤k，k标签的每个非空兴趣型各一名单位客户。任意完整有序策略只要每节点选此前未出现标签，就是完整SPE：所有fresh真续局当前值相同且严格优于repeat。零根W=OPT_m=2^k−2^{k−m}，各u_i=W/m；k>m时未选T的同题冻结删位D_T=W。',
    '所有整数1≤m≤k、所有逐历史fresh确定处方，允许重复过去；只对该全型等重输入。',
    scope='给固定σ客户锥的精确可行下界1，非LP最优上界；重加权后仍须查全部IC。',ev=[23])
own(28,'CA-R0F997-CREDIBLE-THRESHOLD-PRICE-HALF-20261030','可信阈值路径价格PRICE-HALF的精确开放候选','conjecture','open',
    '合法背景b、余r人，v_r(b)=max_A min_{q∈R_{r−1}(b+1_A)}U_A(b+1_A+q)，L0=0,Lr=v_r(b)+min_A L_{r−1}(b+1_A)。已知任意完整子SPE剩余总利润≥Lr。未证主候选F_r(b)≤2Lr(b)，F为背景后最优r主题总利润；根成立即half。r2有F2≤3L2/2；all-big Ln=n且OPT=2n−1。',
    '每个合法背景、每个r≥1；R为全部完整可信后继集合，不局限一份σ或匿名选择器。',
    scope='逐层价格路径不等于同一份最小总利润SPE；61客户L36/最小福利38仅分离这两个量。')
own(29,page(29),'保持最优补全的eta/r全路径预算候选及有限筛查','conjecture','open',
    '沿生成真实路径，第i步余r_i，保持当前剩余覆盖F(r,P)最优的菜单内定义η=r d−M−(r−1)t，候选Σ_i min_menu η_i/r_i≤2W−OPT。冻结seed723、1000小参数有限筛查未给严格正excess，保存best为零客户W=OPT=ηsum=0；本候选未证亦无有效反例。',
    '候选拟量化每个原模型完整SPE的真实路径和对应保持最优补全菜单；当前程序只覆盖m2–5、p3–6的1000次有限生成。',
    scope='不把零权最佳记录作为正质量边界证据；具体η菜单不是TB/POP的同一合同。')

# The precise eta candidate already has a canonical owner. Do not duplicate it.
objects[:] = [o for o in objects if o['object_id'] != page(29)]
materials.pop(29)
pending(29,'已实读；与canonical M-5a32d36d5d2d4eb8a54df3a0a7566a9b的η菜单及Σminη/r合同完全相同。需主作者实际接本有限原审计ref；不以零客户best另造节点。',['M-5a32d36d5d2d4eb8a54df3a0a7566a9b'])

# Separate the two different static conclusions previously sketched together.
mass = next(o for o in objects if o['object_id']==ids[3])
mass['title']='高分数覆盖数不控制真实单位质量的两个目录族'
mass['statement']='每题一私有客户加L共同客户，或无全局共同核心、每题一私有且每个H_j有L客户归除j外全部题，均有τ_C=s而最优私有对偶总重仅s，真实质量分别s+L、s+sL，可任意大。故最优覆盖对偶总重不占真实单位质量的统一正常数比例。'
mass['scope']='仅否定高τ到真实单位质量的推理；不声称坏SPE。'
own(9,ids[4],'高分数覆盖数与不交最优块不提供常数合法路由','counterexample-family','proved',
    'N=km全部k元子集目录，整数k,m≥2，有τ_C=m、无全局私有且存在m不交k元比较块。m≥k时合法题可跨k个不同比较块；k任意大，故比较块不交及高τ不推出所有合法题包含于一个或统一常数个比较块。',
    '上述所有整数参数的静态单位客户目录；不作SPE实现声明。')
attach(11,['customer-attraction/287-client-k5-pair-point-late-deviation-exclusion'],'287客户必要点、真实全树诊断与specialist差异为该目标解析排除的输入/范围证据；保137/287必要点与233真实最差福利、295变体不同。其余扫描日志不造节点。')
own(14,page(14),'存在最优比较元组的最低可信孩子付款义务SM-opt-exists','conjecture','open',
    '固定一份完整SPE实际有序路径h_i，ℓ_{h_i}(A)=min_{z∈R(h_i,A)}u_i(z)，R遍历该孩子全部完整可信续局。每i有u_i≥max_Aℓ_i(A)。开放付款为：是否每份actual路径存在一个真正最优m索引元组或其排列，使Σ_iℓ_{h_i}(T_i)≥OPT_m−W；若成立即half。',
    '所有原输入及每份完整SPE的固定actual路径，存在一个最优索引元组/排列；ℓ允许逐孩子另选可信SPE。',
    scope='与canonical SM-all的所有合法元组量词分立；原未定义费用L_i的排序想法不造数学节点。own列最低孩子可能改变actual叶，续局租金仍承重。')
attach(15,[page(9)],'六源合同中的截断质量包络、静态障碍与有限回归为本批主包络证据；完整分数覆盖前缀定理/7比2子类的外主owner接证另列收据。')
own(16,page(16),'21份固定完整策略锥的共同静态安全对偶证书','certificate-theorem','proved',
    '固定正文列出的21份完整有序策略σ（19份5人7题、1份5人8题、1份6人8题），Kσ={w≥0:Γw≥0}保全部原IC。所存每份共用合法静态n−1槽分布Q，并为每query a给λ_a≥0使c/n−E_Q f_B(a)−Γᵀλ_a≥0。故每份锥上所有非负客户质量w都有Wσ(w)≥n v_n(w)。有理质量清分母还原单位客户。',
    '仅给定21份σ、各自全部非负完整IC客户锥、所有静态查询；不量化全部策略。',
    scope='精确有限证书证明整个指定质量锥的条件数学保证；非仅21个客户点或普通PASS。其他两审计的弱负载桥和覆盖回归仍沿外owner。',
    ev=[ref('tools/evidence/collaboration-model-and-cag-audit-primary/related-cones/760834c0f64c80b5ccc1'),ref('tools/evidence/collaboration-model-and-cag-audit-primary/original/3e153d43f71d6ebd66e6/tests/audits/customer_attraction_new_security_cones.py'),ref('tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-report.json')])
own(19,ids[10],'同一原完整策略的四真实叶双重重置恒等','identity','proved',
    '固定actual节点Z_{<i}、任意同深合法g，a=σ_i(g)。四个真实叶B=finish(g,a),A=finish(Z_{<i},a),E=finish(g,S_i),Z=finish(Z_{<i},S_i)，当前角色收益分别v,D,w,u。两整行IC给e=u−D≥0、ℓ=v−w≥0，故(v−D)−(w−u)=e+ℓ≥0。',
    '同一完整纯SPE、任意同深合法有序历史g；所有finish均沿同一原策略。',
    scope='SQ只比较四枝整行，不给v上界或多context共用u的合计容量；不得逐客户重权IC。')
own(22,page(22),'同题冻结删位、最优元组平均与对称静态CCE的精确表示','identity','proved',
    '任意m人确定叶s、负载c和覆盖C，有D_T=Σ_i u_i(T,s_{−i})=(m+1)Σ_{x∈T}1/(c_x+1)−|T∖C|。任意m索引元组的均匀排列冻结费用Q=(1/m)Σ_jD_Tj≥|O∖C|+|O∩C|/m≥|O|−(1−1/m)W。把actual叶角色均匀置换后的对称分布为静态CCE当且仅当每T有D_T≤W。',
    '每个合法确定叶及合法查询/带重复索引元组；恒等和对称化表示无需SPE。',
    scope='若存在最优元组Q≤(1+1/m)W则half；全T的SA已被十三人例否，坏平均不否存在好匹配。',ev=[23])
own(25,page(25),'core恰等人数时fresh完整策略的actual竞争菜单固定','lemma','proved',
    'n人、core≥n、另有至少一个query标签，完整策略每有序节点只选此前未用core标签。若core=n，则全部actual位置强制任一行动后删当前者的真实竞争计数菜单，恰为{C_core∖{a}:a∈C_core}，大小n。理由是每分支留下n−1个不同core，actual各位置自身行动已给全部n种。core>n时仅有n≤|M|≤binom(core,n−1)。',
    '任意core-fresh完整处方；只是形式策略菜单组合恒等，不先断言任意客户质量下为SPE。',
    scope='1400条浮点gap缺策略/方向payload，不授精确可行或共同混合桥；全零基IC方向编译沿外现有主owner。',ev=[24])
own(33,page(33),'最优首动作的静态低损失不控制真实重启损失','obstruction','proved',
    '同σ同历史h强制最优A后真尾Y_A，ρ_A=G−C_A。对任一真尾行动B，λ_B=G−F_{r−1}(P∪B)，其自身真尾覆盖C_B和真实孩子损失R_B满足R_B=ρ_A−λ_B+(C_A−C_B)。all-big完整SPE根强制singleton A给ρ_A=m−2、η_A=0，取真尾B为大主题得λ_B=0、R_B=m−1、restart=1。因此不能删除restart并以静态低λ替换真实枝损失。',
    '所有所述同σ历史的精确恒等；每m≥3的all-big族给严格正restart见证。',
    scope='排静态菜单再启动捷径，不是half反例；保ξ省η候选另归现有η主owner。')
own(34,'JOINT-SPECTRUM-FRACTIONAL-NOSUFF-v1','actual私有遗漏G谱与全部分数前缀行的完整图反模型','obstruction','proved',
    '每m≥13，L=lcm(1,…,m),K=(m−1)L，遗漏题B_j每对共享L客户，另不交银行A_r大小K/r。银行逆序路径u_i=λ_i=K/r,W=KH_m，全局私有遗漏a_j=0，全部E及全部合法分数覆盖都满足|E|≤P+rτu_i，而OPT_m≥mK/2>2W。末两人倒二改B后末位唯一A1，收益从K/2升K，所以该路径确定非SPE。',
    '每个m≥13构造一条满足原actual遗漏G谱+全部分数行的非SPE路径。',
    scope='只否这些必要接口的充分性；后来全部全局私有含已覆盖者的P扩展能排该点，不得扩大否定范围。',ev=[35,36,37])
own(34,ids[5],'匹配共享遗漏已使原G谱与全部分数行不足','obstruction','proved',
    '每m≥5，L=lcm(1,…,m)，每组两个B_j^ε共享L−1遗漏客户且各带一个A1信用客户，银行A_r大小L/r，A1另有L−2m私有客户。全部3m题不同且极大，遗漏关联恰匹配。银行逆序路径u_i=λ_i=L/r,W=LH_m,OPT_m=mL>2W，同时满足全部E/τ前缀行。倒二改B后所有末位BR恰另一组B，与其不交，偏离得L>L/2，确定非SPE。',
    '每个整数m≥5的匹配遗漏目录与指定银行路径；不是实际SPE坏福利。',
    scope='与v1不同模型/人数范围分立；不能用来反扩展全私有P谱或六人half。',ev=[35,36,37])
attach(35,['JOINT-SPECTRUM-FRACTIONAL-NOSUFF-v1',ids[5]],'程序/双报告分别实现v1 m13/20与v2 m5/13，并保真实末位排除；有限回归计数不另造节点，原G谱主owner额外接证另列。')
own(38,page(38),'经典近二大主题完整SPE族的末两人PAY精确支付','lemma','proved',
    'm≥3大主题m客户加m−1不交单例，全历史恒大主题。在末两人前缀，真最优d1，最优参数t0=4m/(m+1)，最小收费差G=−(m²−4m+7)/(m²−1)<0。m2根另算G=−1。通用d1末对斜率条件Σ_{b≥1}n_b/(b+1)≤(m−1)n0/2保证t0最优（平段取左端）。',
    '上述全部整数m≥2的既有完整SPE族；斜率判据只适用d1且恰余两人。',
    scope='近二性不反PAY；未推广所有SPE的末对付款。')
own(38,ids[6],'负首步余额近二族的末两人PAY精确支付','lemma','proved',
    '对已证n≥4负首步余额族actual A B^(n−1)，真最优每叶一次且d1，O=2n²−2n−2、W=n²−2。末对前缀A B^(n−3)的负载多重表见正文（n4必须合并两条b1）；最优t0=4n/(n+1)，Qmax=4n−6+8/(n+1)，E=n²−2n−2+2/n+2/(n−1)，故G=−2n+8−4/n−4/(n−1)−8/(n+1)<0。',
    '每个整数n≥4的该既有完整策略与单位客户输入。',
    scope='首步负余额与OPT/W→2均不反PAY；SPE可信性复用原族完整证明。')
own(39,page(39),'PAY全部可信有序路径的精确max-min切断算法','algorithm-guarantee','proved',
    '固定有限m≥2输入，Out(q)保存全部完整SPE可实现最终计数，L(q)=max_a min_{z′∈Out(q+e_a)}U_a(z′)。固定z的合法边要求z∈Out(q+e_a)且U_a(z)≥L(q)。对每q枚全部真最优m计数组合并精确最小化t收费得g_z(q)，深m−1置+∞，V_z(q)=min(g_z(q),max_a V_z(q+e_a))。则max_z V_z(0)恰等于所有完整SPE实际路径上min_{k≥2,真最优J,t}收费差的最大值。',
    '每个固定合法有限输入、全部完整历史SPE、有利前缀存在量词与所有真OPT计数。',
    scope='计数缓存是集合，不固定同计数平局；正值必须补满有序离轨树及定义级核验，计数路径不够。',ev=[40,41,42])
own(39,ids[7],'PAY内层凹分段价格的精确加权分位解','algorithm-guarantee','proved',
    '固定m≥k≥2、前缀负载b和真最优m元组客户次数d>0。q(t)=min(td/[m(b+1)],(td/m+4−t)/(b+k))=a t−Δ(t−τ)_+，a=d/[m(b+1)]，Δ=[d(k−1)+m(b+1)]/[m(b+1)(b+k)]，τ=4m(b+1)/[d(k−1)+m(b+1)]。Q=Σwq凹，首次累计wΔ≥Σwa的断点是最左最大化t；可O(n log n)次有理比较及线性算术求得，空正d集取0。',
    '固定允许PAY前缀、非负单位客户重数和0≤d≤m；不将d域换成只到k。',
    scope='算术次数非位长复杂度；内层最优未付跨前缀共同预算。',ev=[40,41])
own(39,ids[8],'每份完整SPE存在可支付实际前缀的PAY义务','conjecture','open',
    'PAY收费J_{k,m,t}(b,d)=1−2(k−2)d/[m(b+k)]−min(td/[m(b+1)],(td/m+4−t)/(b+k))。对任意完整SPE，是否存在某个actual余k≥2前缀、某个真正最优m计数组合J及t∈[0,4]，使Σ_{d>0}J_{k,m,t}(b_x,d_x)≤2E（E为早期玩家在原最终叶的利润）？已有O≤2P+min_tΣJ，若存在即half。',
    '每个m≥2原输入、每份完整有序历史纯SPE，存在actual前缀/真OPT计数/参数；不要求每个前缀。',
    scope='三固定输入全路径阴性与两近二族不证一般存在性；参数左跳只反单调右扫规则。',ev=[38,40,41,42])
attach(40,[page(39),ids[7],ids[8]],'PAY原三个入口/真实输入及精确有限全路径结果归本批算法与开放义务；128完整策略、81/6/2路径与三固定输入不同，不把一次运行或单次数值造节点。')
attach(41,[page(39),ids[7],ids[8]],'原程序/报告/完整m5树的来源闭合；其左跳主owner额外接证另列，p3负收费阻止误称PAY反例。')

# Full mathematical bodies are now read. External owners must actually accept bytes.
attach(20,['customer-attraction/full-spe-static-positive-regret-four-client-replication'],'已全文实读并与0057主作者比较；其主record已实际接此path/SHA。五态、全k副本和独审版本保同身份；不是half反例。')
pending(21,'纯状态账本不造节点。高背景利润、调和逐人付款及玩家专属ghost-ticket编译的独立代数复核应归各精确原owner；尚需定位后两主ID并实际接证。')
pending(23,'已实读完整43处方/程序合同。对称fresh证明已归本批对象；十三人SA/alpha/平均宽限主owner、C7及正性障碍的来源/范围复核尚待各主record接收精确ref。', ['customer-attraction/same-topic-frozen-deletion-static-allowance-thirteen-player-obstruction','M-5058c58fffab4700a759c7a22f763410','M-3505416cc1714c84baef9767bd1ca902'])
pending(26,'恢复入口的独有内容为十三人三付款桥准确量词及存在平均/匹配仍未被该例反驳；应接0027既有三owner，不另造历史入口对象。',['customer-attraction/same-topic-frozen-deletion-static-allowance-thirteen-player-obstruction','M-5058c58fffab4700a759c7a22f763410','M-3505416cc1714c84baef9767bd1ca902'])
pending(27,'已实读：439全整数候选与779精确载体同有限输入；应归24客户跨SCC可逆行主owner及原锥双向空间owner。浮点成员挑行后的精确rank不认证lineality，不另造成功日志节点。',['customer-attraction/twenty-four-customer-complete-spe-cross-SCC-reversible-row','customer-attraction/payoff-type-map-kernel-and-full-real-row-cone-lineality'])
pending(30,'R79三Claim均有既有精确主owner：四七客户协方差、POT/RESET、同质筛选。本文包含同质筛选完整证明及根source后悔修正，需实际接入；DIRECT后续银行否定不得继续OPEN。',['B20-COVARIANCE-CLIENTWISE-NO-v1','B20-POT-RESET-REP-v1','B20-HOMOGENEOUS-SCREEN-v1'])
pending(31,'已实读全部all-big/LOCAL及9660B原审计合同；同尾信用折扣主body在另Boss3的0053，精确同Claim须接证；菜单主owner与归属成本主owner也要接此独立原审查，不复刻主record。',['customer-attraction/same-tail-completion-credit-obstruction','CA-OPTIMAL-FIRST-ACTION-BRANCH-GAP-v1','M-5a32d36d5d2d4eb8a54df3a0a7566a9b'])
pending(32,'菜单原稿、私有孩子两层信用、任意非菜单动作λ公式和后续all-big状态属已登记菜单/eta及0053信用折扣主owner；正文数学未改字节，需主record实际接收本来源ref。',['CA-OPTIMAL-FIRST-ACTION-BRANCH-GAP-v1','M-5a32d36d5d2d4eb8a54df3a0a7566a9b','customer-attraction/same-tail-completion-credit-obstruction'])
pending(36,'已实读六原Claim的具体量词及后补marked-relay来源：本批v1/v2与PAY有主记录；外主owner为既有G谱、COMMON-CORE、静态最坏占用、PAY左跳、中继总账/首次根容量、极端极大归属保底，需精确接证。',['CA-ANCHOR-PRIVATE-SEAT-SPECTRUM-v1','CA-COMMON-CORE-ARBITRARY-TAIL-v2','customer-attraction/last-deviation-marked-relay-and-first-deviation-root-capacity','customer-attraction/static-worst-background-occupied-payoff-and-real-last-repair','CA-PAY-PARAMETER-LEFT-JUMP-v1'])
pending(37,'已实读signed三层存在桥、枢轴/梯度及原程序补取时态；本批G谱反模型仅否原actual遗漏接口，非后续全私有P扩展。外净预算、枢轴与梯度主owner需接该准确范围/原审计，不以浮点1.95造新定理。',['customer-attraction/terminal-net-budget-tuple-support-quantifiers-and-conditional-payment','customer-attraction/arbitrary-background-two-topic-pivot-rent-and-positive-measure','CA-PAY-PARAMETER-LEFT-JUMP-v1'])
pending(42,'原RT-r独有整标签次数证明与CC/v2逐客户饱和不同应同主身份保独立证明；PAY/m槽与高背景/k槽域也分清。需COMMON-CORE及高背景/端点主owner实际接该五源合同ref；本批PAY已接。',['CA-COMMON-CORE-ARBITRARY-TAIL-v2','customer-attraction/joint-minimum-denominator-and-last-floor-high-background-half-profit','customer-attraction/joint-background-profit-signed-endpoint-defect'])

# Preserve the complete finite proof/certificate for the 5945-customer instance.
manifest=json.loads((ROOT/'archives/customer-attraction/tools/evidence/five-round2-cross-replies-regret-and-literature-primary/source-manifest.json').read_text())
finite=next(o for o in objects if o['object_id']==page(2))
finite['evidence'].extend(ref(x['preserved_path']) for x in manifest if 'audit_five_availability.' in x['path'])

def write():
    batch=dict(schema=2,baseline=definition['baseline'],objects=objects,
               materials=[materials[i] for i in sorted(materials)],edge_files=[])
    path=f'research/registration/batches/{TASK}.json'
    (ROOT/path).write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
    progress=dict(task_id=TASK,recorded_material_indices=sorted(materials),
        remaining_material_indices=[i for i in range(len(refs)) if i not in materials],
        semantic_routes=routes,objects=len(objects),note='本地实质草稿；全批未闭合前不提交done；继承/本次读取分别记录。')
    (Path(__file__).parent/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'objects':len(objects),'materials':len(materials),'remaining':progress['remaining_material_indices']},ensure_ascii=False))

if __name__=='__main__':write()
