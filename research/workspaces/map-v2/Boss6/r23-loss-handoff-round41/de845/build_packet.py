import json, hashlib, pathlib, subprocess

REPO=pathlib.Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT=pathlib.Path(__file__).parent
TASK='customer-attraction-3a-3a-de845558940d83ed'
EDIR=pathlib.Path('map/edges')/TASK
RPATH=pathlib.Path('map/receipts')/(TASK+'.json')
(OUT/EDIR).mkdir(parents=True,exist_ok=True)
(OUT/RPATH).parent.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def jwrite(p,x): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(name, section=None):
    matches=list((REPO/'archives/customer-attraction/state').rglob(name))
    assert len(matches)==1,(name,matches)
    p=matches[0];x={'path':p.relative_to(REPO).as_posix(),'sha256':sha(p)}
    if section:x['section']=section
    return x

F='customer-attraction/forward-customer-absorption-whole-row-envelope-and-net-budget'
PAY='M-8a3d5457d56c413189e2683b8ddecde0'
FIN='customer-attraction/arbitrary-child-finance-and-coordinate-certificates-source-erratum'
ARB='customer-attraction/arbitrary-future-query-whole-row-procurement-prices-and-dual'
HALL='customer-attraction/optimal-owner-all-subset-harmonic-transport-and-anchor-isolation'
ANCHOR='M-3c46dcd1fcae445bad3d6d64684c21d2'
NS='M-966d7f6ae9b243a8a2c6a6571e2f1056'
NOPT='M-87293a52db92485094df7979eb9c6564'
THETA='CA-EXTREME-MAXIMAL-THETA-v1'
WELF='CA-EXTREME-MAXIMAL-WELFARE-v1'
LAST='customer-attraction/last-slot-value-and-catalog-counting'
EX='customer-attraction/optimal-five-query-indexed-exchange-and-outside-tax'
M1='CA-MOBIUS-BOOLEAN';M2='CA-MOBIUS-FULL-HISTORY-EMBED'
PROM='customer-attraction/terminal-promotion-potential-drop-and-sharp-new-branch-tax'

edges=[]
def edge(slug,kind,sources,targets,conditions,roles,explanation,scope,evidence,whole=None,contribution=None,mode='unconditional',note=''):
    x={'edge_id':'ca-de845-'+slug,'kind':kind,'status':'accepted','source_ids':sources,'target_ids':targets,'premises_mode':'all','relation_mode':mode,'conditions':conditions,'roles':roles,'explanation':explanation,'scope':scope,'evidence':evidence,'reviewed_by':'Boss6','review_note':note}
    if whole:x['whole_result']=whole
    if contribution:x['contribution']=contribution
    p=EDIR/(slug+'.json');jwrite(OUT/p,x);edges.append((p,x))

edge('forward-ledger-isolates-pay-slack-obligation','implies',[F],[PAY],
 '固定同一完整纯SPE、actual叶、最优并集O、正文合法前向客户流与共同整query包络λ。所有query重新从同一σ的原actual前缀读入；完整利润f保全部客户。',
 {F:'给A+P=OPT、D_env=Σλf−A及精确整行IC恒等式。',PAY:'保留尚未支付的流/包络存在性；本边只识别它所要求的精确金额与half充分性。'},
 '由A+P=OPT、D_env=Σλf−A和Γ_v=u_i−f_v，逐项相消得Σ_iΛ_i u_i+P−D_env=OPT+Σ_vλ_vΓ_v。因此Σ_i(Λ_i−2)u_i+P−D_env≤0与ΣλΓ≤2W−OPT完全等价。原SPE只另给Γ≥0；若确有这一流与包络，则OPT≤净右端≤2W。P≤|O∩C|、D_env≥0、DAG终止或在轨Γ≥0均不供给该存在性。形式harmonic树离轨有fresh偏离，不能用它否定真正SPE上存在选行证书的量词。',
 '精确代数贡献和条件闭合接口；没有构造每份SPE的PAY证书。',
 [ref('前向客户吸收的整行包络与净预算--引理.md','4. 必须面对的精确自检'),ref('前向客户吸收的整行包络与净预算--引理.md','5. 形式在轨障碍不反驳真正SPE的选行候选')],
 contribution={'result':'PAY候选的净预算恰等价于2W−OPT≥ΣλΓ；一旦同一合法流与整行包络满足该式，即推出half。','remaining':'仍须对每个原输入上的完整SPE构造μ、λ并证明这份非负IC松弛的总额不超过2W−OPT；本边未支付它。'},
 note='全文核(1)–(5)、四类客户及形式策略/真实SPE两层量词，未将开放存在性提升为已证。')

edge('forward-residual-flow-embeds-in-arb','transfers',[F,FIN],[ARB],
 '固定同一原完整SPE、actual C/u/W、最优并集O和一份forward流ν及包络λ。R=O\\C，任取0≤q_x≤1；源总量Q=Σ_Rq_x。ARB吸收率必须取r_(v,x)=1/d_v(x)，其中d_v(x)为该真实query的全部玩家覆盖数；ARB完整行D_v对应forward完整收益f_v。',
 {F:'提供严格递增的自然未来coverer分流、原query访问量ν与最大访问包络λ。',FIN:'提供先聚合吸收A_v再用唯一完整行乘子w_v=A_v/f_v的合法金融合同。',ARB:'获得其任意未来query可行域中的一份具体子域流及费用上界；本边不推其全部逆推和对偶结论。'},
 '对x∈R，所有原actual前缀负载p_i(x)=0。将每个该客户的初始流及全部访问量同比缩为q_xν_x(v)，原当前吸收q_xν_x(v)/d_v(x)，其余仍按旧query中各更晚coverer的1/d_v(x)转入。总转出=(1−r)入量，所有child是合法更晚含x query，且每次重新读取同一σ的actual前缀；末位r=1，故是ARB允许的一份流。过去吸收全为0，守恒给Σ_v A_v^q=Q。令A_v^q=Σ_(x∈R∩T_v)q_xν_x(v)/d_v(x)。由于q≤1及ν≤λ，A_v^q≤λ_vΣ_(x∈T_v)1/d_v(x)=λ_v f_v；空/零利润行无正tracked吸收，取w=0。因此w_v=A_v^q/f_v≤λ_v。金融全费K=Σ_v w_v u_i=Q+Σ_vw_vΓ_v≤Q+Σ_vλ_vΓ_v，另有K≤Σ_iΛ_i u_i。ARB最小价不超过这一具体可行费。这里使用的是完整f_v，包括R外客户抵押，不是逐客户COORD投影。',
 '同一r与完整D合同下的可行嵌入、逐行w≤λ和净源金融费的显式IC松弛上界；未假定共享cap已付。',
 [ref('前向客户吸收的整行包络与净预算--引理.md','1. 状态是实际前缀查询，不是延续旧分支'),ref('任意子查询付款的两种充分证书与原等价勘误--资源.md','任意更晚query的金融证书'),ref('任意未来查询的完整行采购价与对偶--算法.md','固定状态与自由度')],
 contribution={'result':'forward在R上的任意q≤1缩放给ARB合法金融流，w≤λ，且最小费≤K=Q+ΣwΓ≤Q+ΣλΓ，同时K≤gross ΣΛ_i u_i。','remaining':'ARB的普遍净源费≤W仍需额外金额控制；Bellman达到、全LP强对偶和自由trim最优值由ARB独立证明，本边不从forward重证或完整推出它们。'},
 note='独立核p_R=0、当前率与完整行D的变量映射、自然child的严格角色增加、零行约定及费用等式；不用金融名词推COORD或钱包cap。')

FREE='customer-attraction/free-query-and-free-start-unit-procurement-prices'
KAPPA='M-fd6b8468eadc43b2a2e8d3058fb5089a'
edge('forward-pay-budget-implies-free-kappa-budget','implies',[PAY,F,FREE],[KAPPA],
 '条件前提是PAY候选对每个有限实例及完整SPE确有同actual重置的合法forward流与λ，满足ΣλΓ≤2W−OPT。每份σ选PAY见证使用的同一最优并集O，R=O\\C、G=C\\O、δ=OPT−W=|R|−|G|。FREE保持真query当前吸收及对真实future coverer等份出口，无旧Hall/eta或共享角色cap。',
 {PAY:'尚开放的全称存在及共同金额前提；本边完整处理它成立后的条件推导。',F:'给原全OPT流、query访问量ν、包络λ≥ν和精确IC松弛账。',FREE:'给自由query/起点等份流程的真实Bellman最小价、共同argmin兼容与自由净源精确最优值。',KAPPA:'获得每份完整σ存在一个最优O使最低δ个κ总价≤W的整条预算候选。'},
 '固定任意σ并取PAY见证的同一O、流和λ，记Γ_v=u_i−f_v≥0，其中f_v是包含全部客户的完整query收益。actual是合法m元组，故δ≥0；δ=|R|−|G|≤|R|，可选0≤q_x≤1且Σ_Rq_x=δ，δ0取零流。R客户在全部原actual前缀负载0；将其原初始分布与访问量同比缩为q_xν_x(v)。在query v=(i,a)，覆盖数d_v(x)=1+|F_i,a(x)|，当前和各future coverer均吸收/转出入量的1/d_v(x)，因此它恰是FREE允许的等份流程，只是每个到达角色继承了父query指定的合法动作。该parent-dependent选择不妨碍FREE比较：按角色逆归纳，任一该子流程单位费≥[u_i/f_v+Σ_(j∈F)V_j(x)]/(1+|F|)≥V_i(x)；任意初始角色/动作混合的费≥κ_x=min_iV_i。反之FREE在每个(i,x)固定argmin，对全部父来源和客户可同时达到；无共享cap，因此Σ_Rq_xκ_x不超过这个具体forward限制流程的金融费K。R无past且严格递增至末位全吸收，Σ_v A_v^q=δ。令A_v^q=Σ_(x∈R∩a)q_xν_x(v)/d_v(x)，同query先聚合，唯一w_v=A_v^q/f_v；零行无tracked吸收取w0。q≤1和ν≤λ给A_v^q≤λ_v f_v，故w≤λ。于是K=Σw_vu_i=δ+Σw_vΓ_v≤δ+Σλ_vΓ_v≤(OPT−W)+(2W−OPT)=W。FREE的LOWEST又给最低δ个κ之和=min_qΣqκ≤W。O始终取同一PAY见证，不换最优并集或把不同σ、分母的松弛相抵；故对每个σ得到存在一个这样的最优O，完全符合KAPPA的存在量词。',
 '完整证明的条件蕴含，方向PAY共同预算⇒FREE-KAPPA共同W预算。源PAY存在仍open；没有普遍无条件half证明，没有金融w自动COORD，也不保持旧Hall取消或初始化余额。',
 [ref('前向客户吸收的整行包络与净预算--引理.md','4. 必须面对的精确自检'),ref('自由查询与自由起点的单位采购价格--算法.md','Bellman的下界、达到与共同兼容'),ref('自由查询与自由起点的单位采购价格--算法.md','自由净源选择及开放预算'),ref('客户级自由接纳与累积税的整行付款--算法.md','同一query不必要求所有incoming同一接纳比例')],
 whole='若PAY候选对每份完整SPE给其合法流/λ及ΣλΓ≤2W−OPT，则对每个该σ存在PAY见证的同一个最优O，使FREE最低δ个κ总价≤W；事实上任一R上总量δ的q≤1均有Σqκ_FREE≤K≤W。KAPPA目标的全实例/全σ/存在O及同O净源量词全部保留。',mode='conditional',
 note='独立核父依赖query流程与每(i,x)共同Markov最小价的逆归纳比较；联合R守恒、w≤λ和同σΓ≥0逐式推出W预算，条件论证无缺步，未支付源PAY的普遍存在。')

edge('hall-b-transport-isolates-owner-complete-roles','implies',[HALL],[ANCHOR],
 '固定同一最优m元组T、owner分割Q_i⊆T_i与同一合法叶B；使用Hall-B而非普通Hall-A。可以不要求B为SPE。',
 {HALL:'给HYB单点割、B图只用missing-owner客户E、非负流守恒及存在满流。',ANCHOR:'得到任一owner完备角色在任意可行满流中零source、零出入流；完整最优前缀的同叶隔离随之成立。'},
 '若Q_i⊆B_i，取HYB J={i}，损失库存M({i})为空，故B_i\\O为空，b_i^H=0。i的owner客户均不在E={x∈O:x不在B_owner(x)}，而Hall-B的角色出边和终端只由E中的owner发出，因此i没有自有出边或终端。非负守恒out_i+sink_i=b_i^H+in_i迫in_i=0；外owner指向i的正容量边在任何可行流中也必须用零。对同一σ强制完整最优前缀T_1,…,T_k后的真叶，各i≤k均owner完备，故全部已用B流与源/终端支撑于未来角色。这个量词是任何满流，而非只选一份好流；空Q_i、空主题、重复标签、k=m亦由零式覆盖。',
 'Hall-B同叶静态结构完整蕴含目标；不推出A图任意流隔离或跨叶共同钱包。',
 [ref('最优归属的全子集调和运输与锚定隔离--定理.md','B图的最优锚定角色零流'),ref('归属完备角色的Hall-B零流与同叶预留--引理.md','owner完备强迫任意可行流零入零出'),ref('归属完备角色的Hall-B零流与同叶预留--引理.md','最优全前缀与历史边界')],
 whole='对每个满足Q_i⊆B_i的锚定角色，Hall-B外部调和source为0，且任何可行满流均无该角色已用出边、终端或入边。强制同一完整最优前缀后的同叶B图因此隔离全部过去锚角色。',
 note='核所有割与B图容量，再逐角色守恒；明确普通A图与逆角色未来流不在此结论。')

edge('hall-hybrid-specializes-to-five-index-exchange','specializes',[HALL],[EX],
 'HALL取m=5；T_1,…,T_5确实达到OPT5，所有替换R_i/S_i/C/H_i为原目录合法标签。owner是静态分析分割，可按所证索引子集选择，不能把不同owner的流或容量合花。税比较另取合法非负整数背景b。',
 {HALL:'提供对任意owner、角色子集的静态HYB覆盖割；这里不使用其Hall流付款。',EX:'由单槽及多槽特化、按指定索引求和和分母界得到完整五索引静态行库及OPT外税转私有块。'},
 '先固定槽k。把所有同时在T_k和其它T槽中的客户归给一个其它含它的槽，令Q_k恰为P_k=T_k\\∪_(j≠k)T_j；其余客户任取合法owner。对J={k},B_k=R用HYB，M(J)=P_k\\R，遂有|R\\O|≤|P_k\\R|。R_i对k=i求和给配对行Σ_i t_i1_(j_T=1)(1−r_i)−1_(j_T=0)Σ_i r_i≥0；对全部(i,k)求和给1_(j_T=1)(5−Σr_i)−5·1_(j_T=0)Σr_i≥0。二者保留各自配对，不能互换。固定C对k求和给1_(j_T=1)(1−c)−5c1_(j_T=0)；分别取实际A/B再加得1_(j_T=1)(2−b)−5b1_(j_T=0)；换r为s同理。多槽I时，把所有在∪_(k∉I)T_k中的客户owner放I外，其余owner放I内；令B_i=H_i(i∈I)。HYB的外部新增并集恰为∪H_i\\O，丢失恰为O\\(∪_(k∉I)T_k∪∪_(i∈I)H_i)，所以替换后的五槽覆盖≤OPT，得覆盖指示差总和(6)。最后x∉O使t_i=0，τ_i(x)=r_i(1−s_i)/[(b+1)(b+2)]≤r_i/2。乘4/25求和并用配对交换，得(4/25)Στ_out≤(2/25)Σ|R_i\\O|≤(2/25)Σ|P_i\\R_i|。',
 '完整五索引静态交换及指定OPT私有客户容量；没有SPE前提，不把私有客户裸容量升为actual可重复收入。',
 [ref('最优归属的全子集调和运输与锚定隔离--定理.md','全角色子集的混合不等式'),ref('最优五查询的索引替换与外部回复税--引理.md','可直接输入五查询直方图的行'),ref('最优五查询的索引替换与外部回复税--引理.md','交叉末回复私有税的外部部分')],
 whole='对任意真正最优五元组，得到目标的单槽交换(1)、配对/全25/固定C/合并前缀行(2)–(5)、任意多槽覆盖差(6)及外部交叉税转指定私有块的(7)，均保合法重复索引和全客户求和量词。',
 note='独立选择单槽Q_k=private与多槽owner，核外部新增和真实库存损失恰匹配；无最优性不能调用。')

edge('near-saturation-certificate-attains-template-corner','implies',[NS],[NOPT],
 '只限末位IC乘子固定1、末主题统一容量权t、中间主题统一权p及逐客户非负余项的模板，k≥2，目标F≤s+BΔ+V(U−s)。不声称所有SPE证明方法或实际实例的最优系数。',
 {NS:'给t=k、每中间p=k/2、B=k−1及三类ρ≥0的显式可行证书。',NOPT:'获得其受限模板最小角点的可达侧；必要坐标下界仍来自目标自己的独立三坐标证明。'},
 'NS的精确恒等式用末位IC权1、L容量权k及k−2个中间容量权k/2。故V=k+(k−2)k/2=k²/2，B=k−1，所有客户余项按c=0、c=1/l=0、c=l=1三类非负，对全部整数背景及合法目录成立。k=2时没有中间项，仍t=2、B=1、V=2。与目标另证的必要坐标t≥k、p≥k/2(k≥3)、B≥t−1合看，这份证书同时达到其B/V下界；本边只交这一可达性，不从一个上界假称已经推出所有系数的必要性。',
 '完整成立的局部贡献：模板角点可达。U是全目录共同容量；U=u或K/k两读出不扩大为全局half。',
 [ref('任意人数near-saturation末位容量--引理.md','逐客户非负证书'),ref('任意人数near-saturation末位容量--引理.md','两个可读出行与系数边界')],
 contribution={'result':'在目标受限模板内存在显式证书达到B=k−1、V=k²/2，末/中间容量权为k/k/2；k=2单列。','remaining':'仅凭该可行证书不能推出必要下界；t≥k、p≥k/2和B≥t−1由目标绑定原稿的三个精确坐标承担，也未得到实际SPE类全局最优性。'},
 note='完整读正文与3518字raw解析证明，核t/p/B三个必要坐标与显式可达侧，未重跑有限Fraction枚举或44/60行全局证书。')

edge('theta-and-catalog-counting-give-sharp-core-welfare','implies',[THETA,LAST],[WELF],
 '客户对不同极大覆盖的归属大小仅1、k−1或k；任意合法背景b、r≥1名剩余玩家及同一完整纯SPE。共同核心强化和逐人数锐性在空根m人陈述；静态扩张到极大主题不改变原动态实际策略。',
 {THETA:'给每名剩余玩家≥θ_r(b)的真实中继结论。',LAST:'给通用静态F_r(b)≤(2r−1)θ_r(b)及根覆盖计数界。',WELF:'获得剩余利润、空根核心强化和每人数的完整锐性。'},
 '逐人θ保底求和给P_r≥rθ_r；LAST的同背景利润计数给rθ_r≥rF_r/(2r−1)，非零背景只算剩余者利润。空根令共同核心C=∩极大覆盖、c=|C|。仅在θ静态min/max中把查询及竞争主题扩为原合法极大主题：查询扩张不减收益，竞争扩张不增各查询值，因此值保持。全部m个极大槽都含核心，θ_m=c/m+θ_res；删除共同核心保极大覆盖的非包含关系与归属类，LAST对残余目录给θ_res≥OPT_res/(2m−1)，OPT_m=c+OPT_res。故W≥mθ_m≥c+m(OPT_m−c)/(2m−1)，即OPT_m≤c+(2−1/m)(W−c)。实际末位为BR，必包含整个核心（若漏客户，合法严格超集使收益增加），故W≥c；没有要求早期真实主题含核心。锐性：m≥2时取一个大小m大私瓣、m−1个互不交单客户私瓣，并给全部主题加同一c核心；所有有序历史后都选大主题。核心每人c/m固定，大主题从私瓣至少1，任一单例至多1，所以完整SPE。W=m+c、OPT=2m−1+c，使核心式取等。m=1另为W=OPT，零客户按零值处理。',
 '结构条件下目标全部剩余利润与空根锐福利结论；不推出一般中间归属的θ桥或六人half。',
 [ref('单例缺一极大归属的真实中继保底--定理.md','4. 全分支闭合与全部玩家结论'),ref('单例缺一极大归属的真实中继保底--定理.md','5. 共同核心改进与逐人数锐性'),ref('末位最坏背景值与目录计数界--引理.md','4. 非零背景比较的是剩余利润')],
 whole='每个结构合法背景和完整SPE均有P_r≥rθ_r≥rF_r/(2r−1)；空根OPT_m≤c+(2−1/m)(W−c)，并对每个m及允许的共同核心大小由完整全大主题策略达到等号。',
 note='核固定前缀嵌入与纯θ/混合v的量词差；核心只作静态归约，锐族在全部历史的IC逐式给出，不借13例有限回放证明全称。')

edge('mobius-inversion-with-positive-bias-compiles-full-history','transfers',[M1],[M2],
 'p≥n≥1，任意有理F:2^P→Q且F(空)=0；辅助游戏每节点只准此前未用标签，效用为F的终局删除边际。D为共同正整数分母，对DF反演得到整数x，M=Σ非空B|x_B|，K=4M+1，r_B=x_B+K。',
 {M1:'给唯一signed反演、所有重复计数的唯一调和扩张及精确删除边际；清分母后整数重数。',M2:'获得合法单位客户实例的全部有序历史fresh支配、辅助SPE的恰好满射投影和根收益平移。'},
 'M1给整数x与全计数Φ_x，而非允许任意补重复终局。r_B≥1可展开不同单位客户；正singleton保证主题非空及覆盖互异。任一已选行动的signed收益绝对值≤M。对任一长度d<n、过去不同标签数k≤d的有序历史，p−k≥n−d保证未来足够fresh。按剩余人数逆归纳：若任一孩子子SPE今后均fresh，比较当前fresh a与过去出现v≥1次的old b；仅在均匀偏置部分置换未用标签以对齐各自真实后继，并使a不在对齐后继中。把类型按含a/b配对，二者皆含项相消，仅含者之差为Σ_(C⊆P\\{a,b})[1/(1+s_C)−1/(1+v+s_C)]≥v/(v+1)≥1/2。signed两真实叶收益差≥−2M，故总差≥K/2−2M=1/2>0。基础末位相同，故所有有序历史（含过去重复）中任何子SPE都排old。固定前缀下fresh动作及任意fresh后继的偏置部分相同，fresh比较完全保signed差；在无重复历史，M1删除边际恰为DF边际，所以任一原SPE限制是辅助SPE。反向给定整份辅助SPE，在每个首次重复的孩子子树，对唯一signed计数扩张选完整fresh受限BI子SPE；各不同有序子树独立补齐。偏置不改其中fresh比较，old动作由前述严格差排除；在无重复子树保原辅助策略，fresh偏离仍在该子树、old偏离进已补子树且严格劣。因此每份辅助策略均有原完整SPE扩展，投影恰为全部辅助SPE，但不同重复子树扩展可同投影，非一一对应。根n-distinct终局每名偏置份额为K·2^(p−n)Σ_(j=1)^n C(n−1,j−1)/j=K(2^p−2^(p−n))/n，signed为D u_i，给精确根平移及全部根有序路径、无重复历史激励平局对应。',
 '目标完整历史编译的整条陈述，包含所有重复离轨历史及正客户合法化。p<n不适用，n=1无old、M=0时K=1。没有福利比例保持或half反例迁移。',
 [ref('子集调和势的Möbius反演--定理.md','从子集势到真正的边际收益对象'),ref('无重复辅助博弈的完整历史编译--定理.md','所有重复历史上的严格支配证明'),ref('无重复辅助博弈的完整历史编译--定理.md','无重复子树的等价及重复子树的扩展')],
 whole='对每个所述F和p≥n，构造r=x+4M+1后每份原完整SPE在全部有序历史均选fresh；限制投影恰为辅助SPE全集，每份辅助策略有完整原扩展，根终局和有序路径相应保持，根收益变为D u_i+K(2^p−2^(p−n))/n，且无重复子树的全部激励平局保留。',
 note='逐段重构未用标签对齐、strict gap≥1/2、signed真实后继界和全部重复子树扩展；正重数本身不替代支配证明，不声称投影双射。')

jwrite(OUT/'new-edge-index.json',[{'path':p.as_posix(),'edge_id':x['edge_id']} for p,x in edges])
print('wrote',len(edges),'edges')
