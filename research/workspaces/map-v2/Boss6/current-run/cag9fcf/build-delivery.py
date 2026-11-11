import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
TASK = 'customer-attraction-3a-3a-9fcfdc8bf3a36190'
OUT = ROOT / 'map/edges' / TASK
OUT.mkdir(parents=True, exist_ok=True)

def ref(path, section=None):
    r = {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
    if section:
        r['section'] = section
    return r

MODEL = 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
PAY = 'archives/customer-attraction/state/资料/可信端点共同付款的接口合同与停界--资料.md'
CAP = 'archives/customer-attraction/state/引理/可信端点均值cap的三域与松弛信用--引理.md'
REPLAY = 'archives/customer-attraction/state/问题/真实重放协方差的定量付款--问题.md'
ORIGIN = 'archives/customer-attraction/state/算法/固定来源路由的最大回撤与价格分离--算法.md'
ATOM = 'archives/customer-attraction/state/定理/初始客户边独立回撤与共同价格分散返还--定理.md'
CUTS = 'archives/customer-attraction/state/审查/原子独立回撤的零返还价格与失败切面--审查.md'
MENU = 'archives/customer-attraction/state/资源/固定实际路径的可信门槛与全菜单包络--资源.md'
RENT = 'archives/customer-attraction/state/审查/可信惩罚的共同目录闭包与影子租金账--审查.md'
THRESHOLD = 'archives/customer-attraction/state/候选/动态可信门槛与归属响应税的共同付款条件--候选.md'
THRESHOLD_REVIEW = 'archives/customer-attraction/state/审查/动态门槛审查的净差量词与接续版本边界--审查.md'
QUAD = 'archives/customer-attraction/state/计算/对称二次势探针保存点的精确保底等号--计算.md'
BPC = 'archives/customer-attraction/state/定理/最大质量分区与轨道交叠的全实权价格证书--定理.md'
TWO_GROUP = 'archives/customer-attraction/state/程序/双组完整策略的分区锥探针与十例有理审计--程序.md'
STATIC53 = 'archives/customer-attraction/state/计算/五十三单位静态安全值的有理鞍点--计算.md'
SPE53 = 'archives/customer-attraction/state/构造/五十三单位四人完整策略与内生水位基准--构造.md'
FLOOR53 = 'archives/customer-attraction/state/资源/正深度静态安全地板反例的单位数据与审查出处--资源.md'
STATIC53_JSON = 'archives/customer-attraction/tools/evidence/endogenous-padding-and-security-primary/static-security-exact.json'

ids = {
    'balance': 'M-3037b0681605488faac0c733f17cffea',
    'pay': 'customer-attraction/credible-endpoint-common-payment-interface-contracts',
    'origin': 'CA-FIXED-ORIGIN-RETRACTION-v1',
    'atom': 'ATOM-RETRACTION-v1',
    'disp': 'DISPERSION-REBATE-v1',
    'fail': 'M-b36ea945fc41428c9aed003ae371dc92',
    'zero': 'customer-attraction/atom-retraction-zero-rebate-prices-and-failed-cuts',
    'menu': 'customer-attraction/fixed-actual-path-credible-thresholds-and-full-menu-envelopes',
    'bank': 'M-000c23f3a44f4ec1a907b81573ed5ef2',
    'rent_open': 'M-e3da9cd2fd704a09b76ecde385ef0695',
    'rent': 'customer-attraction/credible-punishment-common-catalog-closure-and-shadow-rent-ledger',
    'sm': 'M-3c4224decc184b5da00cbda57f823e98',
    'no_cag': 'M-67c3d64ca1824c53b72c3d2790cdbe60',
    'two_group': 'customer-attraction/closeout-72fbf99e1247805f882e844b',
    'static53': 'customer-attraction/fifty-three-unit-static-security-exact-rational-saddle',
    'bpc': 'customer-attraction/maximum-mass-partition-and-orbit-overlap-all-real-price-certificate',
    'nine': 'cag-nine-customer-one-fresh-group-two-pool-boundary-SPE',
    'eight': 'customer-attraction/six-player-true-maxroot-copy-envelope',
    'quad': 'customer-attraction/symmetric-quadratic-probe-saved-point-exact-security-equality',
    'r22': 'R22-POSITIVE-DEPTH-SECURITY-NO-v1',
    'local_replay': 'M-d30c867c139848e3b4ef57eadc270f8d',
}

edges = []
def edge(name, sources, targets, conditions, roles, explanation, scope, evidence,
         whole_result=None, contribution=None, kind='implies'):
    record = {
        'edge_id': 'cag-9fcf-' + name,
        'kind': kind,
        'status': 'accepted',
        'source_ids': [ids.get(i, i) for i in sources],
        'target_ids': [ids.get(i, i) for i in targets],
        'premises_mode': 'all',
        'relation_mode': 'unconditional',
        'conditions': conditions,
        'roles': {ids.get(i, i): s for i, s in roles.items()},
        'explanation': explanation,
        'scope': scope,
        'evidence': evidence,
        'reviewed_by': 'Boss6/cag9fcf',
        'review_note': '逐项核当前登记陈述、模型、量词和所列全文证据；所有source的当前truth_status均为proved。复用同SHA成熟解析证明及充分证书，未重跑LP、MILP、全历史IC、BI或会员型扫描。' +
                       (' 本边只交contribution；目标的其余义务不由此边支付。' if contribution else ' whole_result覆盖目标整条陈述，抽象例与真实SPE范围分别保留。'),
    }
    if whole_result:
        record['whole_result'] = whole_result
    if contribution:
        record['contribution'] = contribution
    path = OUT / (name + '.json')
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    edges.append((record, path))

edge(
    'same-source-mean-cap-payment-reduction', ['balance'], ['pay'],
    '同一有限单位客户共同标签目录、同一完整有序历史纯SPE、同一原σ查询源、同一全行可信端点均值cap共享最优点及其逐行有效对偶。actual标签仅保原actual端点；t=(1+L)^−1，p支持最大t价格γ，L为m−1质量合法分数目录负载。',
    {'balance': '提供原source的SOURCE-BAL、Qstat≥0与STATIC；μ_i保持逐行独立。',
     'pay': '只获得候选金额的精确标量化及half充分方向，候选全称金额仍开放。'},
    '令X=D+Σ_i(1+μ_i)I_i+Σ_iE_pR_i。源恒等式是W−mγ=X−Cov，故Cov−X=mγ−W。于是目标PAY式Cov≤X+(γ+Qstat)/2，在同一个接口上当且仅当W≥((2m−1)γ−Qstat)/2。该式成立时，2W≥(2m−1)γ−Qstat≥OPT_m，其中后一方向来自STATIC。整个推导不除γ或W，m=1和零客户也保留。\n\n这是精确reduction，不是Cov的已证上界。G=Σμ_iI_i+ΣER_i是同一信用的拆分；没有在X外再加G，也没有把η_i强迫为非负。局部真实重放对象M-d30c…使用释放actual-tag的GLOBAL-NET raw域、共同μ及B_i=d_i−S_i；其RESET/EDGE恒等式保祖先损失与不同主题同叶差。该对象没有给从本可信全行cap端点到raw重放终点的可信闭包及同域价格/容量映射，不能将它的净cap银行塞入X。即使局部代数相似，也不支付本候选的原source金额。',
    '只固定可信全行均值cap原σ接口的候选付款reduction。没有断言其阈值是half的必要条件，未把NET/full-slot/aligned域中的γ、价格或库存混入。',
    [ref(PAY, '一份原source共同账及其未证金额'), ref(CAP, '全行域保留原查询源的精确正信用'), ref(CAP, '倒数主账及尚未证明的付款'), ref(REPLAY, '切线EDGE与不同主题同叶残差')],
    contribution={
        'result': '候选PAY在同一可信全行cap/原source接口上精确等价W≥((2m−1)γ−Qstat)/2；因此PAY一旦成立便推出2W≥OPT_m。',
        'remaining': '仍须对每个规定实例/完整SPE及同域共享最优点证明这个阈值，等价地证明原source协方差金额。SOURCE-BAL、静态余量、局部重放恒等式及有限未分离都不提供该上界。',
    })

edge(
    'joint-coarse-and-atom-dispersion', ['origin', 'atom'], ['disp'],
    '固定同一T、INIT、d/H/J、全部真实叶与分母、optional-common路由及全额逐角色atom终端K；A和各角色一份2u cap相同。b_i=Σ_{o(a)=i}b_a，K_iℓ=Σ_{o(a)=i}K_aℓ。零b行取0。抽象严格包含见证只要求三角source/cap合同，不认证SPE实现。',
    {'origin': '给同owner同比例限制的费用仿射式和粗SOURCE-PRICE需求。',
     'atom': '给独立atom盒的可实施费用仿射式及全非负价格细需求；全额终端追踪保同一A。',
     'disp': '获得同价的精确min(D_i,E_i)返还、修复类包含及抽象严格包含。'},
    '把旧owner总回撤y_i实施为y_a=(b_a/b_i)y_i。代ATOM-RETRACT，Σ_{o(a)=i}y_a=y_i且Σ_{o(a)=i}t_aℓy_a=(K_iℓ/b_i)y_i，恰恢复旧RETRACT。因此旧同比例类嵌在独立盒内；初始库存和密度仍由同一个atom缩放证明保证。\n\n固定λ≥0，q_a=Σ_ℓt_aℓλ_ℓ，b_i q̄_i=Σ_{o(a)=i}b_aq_a。两条source-price的右端同为Σ_ℓλ_ℓ(2u_ℓ−A_ℓ)。置D_i=Σb_a(λ_i−q_a)_+和E_i=Σb_a(q_a−λ_i)_+。有b_i(q̄_i−λ_i)=E_i−D_i，粗需求减细需求=E_i−(E_i−D_i)_+=min(D_i,E_i)。零b_i整行为0。只有正质量严格跨owner价两侧才有严格返还，未产生新的IC收入。\n\n严格性用目标保存的抽象数据独立算术验证：u=(1,1,1)，A=(3/2,2,1)，owner1两atom各1/2分别终结角色2和3。原F=(3/2,5/2,3/2)，比例回撤后F′=(3/2+y,5/2−y/2,3/2−y/2)。cap1要求y≤1/2，cap2要求y≥1，故比例类无解。独立全撤去角色2的atom得到(2,2,3/2)，全部cap成立。λ=(1/2,1,0)给粗需求1/2、细需求1/4、共同RHS1/4，D_1=E_1=1/4。这个三角代数例没有由任一source定理升级为真实目录/SPE/INIT。两已证来源在真实流上的类包含与本独立抽象算术共同完整支付目标。',
    '同一固定全额atom流上比较两修复族，任意非负实价格。抽象严格包含未迁移为真实SPE严格优势；λ=1返还0，总资金条件仍等价|O|≤2W。',
    [ref(ORIGIN, '按原来源拆分与精确回撤'), ref(ORIGIN, '首次失败的显式非负价格证书'), ref(ATOM, '独立回撤与证书类扩张'), ref(ATOM, '全非负价格的精确可行性判据'), ref(ATOM, '相对owner比例回撤的精确分散返还'), ref(ATOM, '严格包含的抽象数据及真实范围')],
    whole_result='对任意同一固定合法全额atom流及每个λ≥0，粗owner需求减细atom需求逐owner恰等min(D_i,E_i)≥0；独立atom盒含同owner比例类，且正文u=(1,1,1)、A=(3/2,2,1)的三角source/cap抽象例见证严格包含。该存在例不声称来自真实SPE。')

edge(
    'atom-dispersion-zero-price-domains', ['atom', 'disp'], ['zero'],
    '同一固定合法全额atom流，正质量atom的t_a为仅支持严格未来角色的概率分布；所有A、b、u、终端量来自同一份输入。λ≥0，不改变原mandatory/common路由。',
    {'atom': '提供全价格SOURCE-PRICE、严格future与t_a概率分布，支付后缀cut的精确形式。',
     'disp': '提供每owner的精确返还min(D_i,E_i)，使零返还只需核q_a在owner价同一侧。',
     'zero': '得到全部二值/角色单调价格无返还、后缀必要式及严格细化所需条件。'},
    '若所有λ只取α≤β，则每q_a是未来λ的凸组合，属于[α,β]。owner价为α时D_i=0，为β时E_i=0，所以每owner返还0，包括全体0/1集合价格及全1价格。若λ按角色不降，严格future迫q_a≥λ_{o(a)}，所以D_i=0；不升时q_a≤λ_{o(a)}，所以E_i=0。零atom没有贡献。这些是全参数结论，不是有限价格抽样。\n\n再取后缀S_k={k,…,m}的0/1价。owner在后缀内时其所有终端也在后缀，故q_a=λ_owner=1；更早owner的λ_owner=0，所以min(λ_owner,q_a)=0。ATOM-SOURCE-PRICE左端恰Σ_{i≥k}b_i，右端Σ_{i≥k}(2u_i−A_i)，等价Σ_{i≥k}(A_i+b_i)≤2Σ_{i≥k}u_i。此处b_i是初始owner质量，不能改成未回撤F_i的incoming质量。\n\n由精确返还式，严格优势必须有某owner正质量的q_a严格跨λ_i两侧。二值或角色单调均排除此事，因此只可能在合适非单调、至少含真正中间价的价格上激活。该必要条件不保证新盒成功，也不说回撤相对原F没有作用。',
    '两个全参数零返还域和同一固定流的后缀SOURCE-PRICE必要式。不是新half总资金定理，不与另一full-SAFE/J钱包混用。',
    [ref(ATOM, '全非负价格的精确可行性判据'), ref(ATOM, '相对owner比例回撤的精确分散返还'), ref(CUTS, '两个全参数零返还域及后缀必要式')],
    whole_result='对全部固定严格future全额atom流，二值非负价格和按角色任一方向单调的价格都使每owner min(D_i,E_i)=0，粗细cut需求相同。后缀0/1价精确给Σ_{ℓ≥k}(A_ℓ+b_ℓ)≤2Σ_{ℓ≥k}u_ℓ；严格细化优势必须由适当非单调中间价及同owner跨价正质量触发。')

edge(
    'first-failed-owner-cut-exact-atom-rebate', ['origin', 'disp'], ['fail'],
    '同一固定合法全额atom流按owner汇总后执行旧比例贪心；j为其首次z_j<0。使用旧算法明确回推的λ_j=1、ℓ>j价格0、i<j全撤owner价0、未全撤owner价q̄_i。不得改成任意新盒最坏价。',
    {'origin': '提供指定首失败price、其旧CUT=z_j及此前贪心饱和/紧cap结构。',
     'disp': '在同一价把粗需求与细需求相减，精确给Σ_i min(D_i,E_i)。',
     'fail': '完整得到紧owner价离散公式及旧违反ε到新同价违反的精确变化。'},
    '旧首失败price满足λ_j=1且其后全0。i≥j的atom只能终结更晚角色，所以q_a=0；i=j时E_j=0，i>j时D_i=E_i=0，均无返还。此前全撤owner有λ_i=0且q_a≥0，故D_i=0。此前未全撤owner取λ_i=q̄_i，于是Σ b_a(q_a−λ_i)=0，即D_i=E_i。其返还min(D_i,E_i)=D_i=(1/2)Σ_{o(a)=i}b_a|q_a−q̄_i|。加总恰为目标指定的(1/2)Σ_{i<j:y_i^greedy<b_i}Σ_{o(a)=i}b_a|q_a−q̄_i|。\n\n令ε=−z_j>0。旧SOURCE-PRICE左端减共同RHS恰ε，细需求在同价减少上述返还，右端不变，所以新同价违反恰ε减此数。这里不把负的有符号违反再取正部；返还超过ε时只说明该价已不分离，仍可能存在其它失败价格。旧输入H/J及逐角色全额K保持一致是该差额成立的前提，漏掉固定余流会改变RHS。',
    '仅诊断旧比例贪心的指定第一次失败切面；不证明返还≥ε，不证明旧price仍最坏，不据消除该价推出独立atom可行。',
    [ref(ORIGIN, '固定修复族的精确三角算法'), ref(ORIGIN, '首次失败的显式非负价格证书'), ref(ATOM, '相对owner比例回撤的精确分散返还'), ref(CUTS, '旧三角贪心首败价如何改变')],
    whole_result='每个旧比例贪心首次失败j及其指定回推价λ，粗需求减细需求恰(1/2)Σ_{i<j:y_i^greedy<b_i}Σ_{o(a)=i}b_a|q_a−q̄_i|；旧违反ε=−z_j的新同价违反恰为ε减该返还。')

edge(
    'weighted-rent-common-payment-reduction', ['rent'], ['rent_open'],
    '固定同一完整有序历史纯SPE；共享背景仅为该原σ的删除槽真实菜单K=(1/m)Σ_i conv{L_i(A)}；取真正查询/背景鞍点(p*,L*)，t=(1+L*)^−1，p*仅支持t价格等于γ的合法主题。',
    {'rent': '提供真实同枝R_i/H_i及唯一RENT-t恒等账，IC_i=u_i−E_pd_i≥0。',
     'rent_open': '只得到开放UNPAID的精确W≥mγ重写，尚无共同金额上界。'},
    '对活跃A，γ=Σ_{x∈A}t_x。令z_x是同一真实完成枝中除进入者外的全部负载，则R_i−H_i=Σ_{x∈A}[t_x z_x−(1−t_x)]/(1+z_x)=Σ_{x∈A}[t_x−1/(1+z_x)]=γ−d_i(A)。对p取期望并加Σ_i IC_i，严格得到W−mγ=Σ_i IC_i+Σ_i EH_i−Σ_i ER_i。移项便知UNPAID当且仅当W≥mγ。\n\nR_i是各自互斥真实偏离叶中的t加权其它玩家份额，H_i是相同叶上的价格补差；不能将不同叶的捕获者份额合到同一个actual未来角色。只极小化任意固定p的背景未必有支持价格等于γ，因此不能漏掉真正鞍点条件。k(A)≥0及SIGNED只是原IC的减常数改写，也没有给第二份实际资金。\n\n这条强共享价格路线与全行可信mean-cap原source接口的PAY不是同一金额：后者改变背景可行域并带逐行μ_i、R_i和Qstat/2。没有同域同价格映射时，不能把两种γ或正信用拼接；本边不声称UNPAID是half的必要条件。',
    '仅原固定策略真实共享菜单鞍点上的强租金付款reduction；全目录共同闭包和特定银行必要IC均未在本边升级为普遍租金上界。',
    [ref(RENT, '同一共享鞍点上的行动折扣与收益改写'), ref(RENT, '同枝加权租金与未付款的共同金额')],
    contribution={
        'result': '开放金额Σ_iER_i≤Σ_iIC_i+Σ_iEH_i在其规定原菜单鞍点上精确等价W≥mγ；R/H/IC均沿同一原σ的各真实枝定义。',
        'remaining': '仍需证明不同互斥偏离叶的加权租金能由一次共同actual预算支付。RENT-t恒等式、鞍点KKT、行动折扣或特定Cartesian控制器的必要IC均不提供该全称上界。',
    })

edge(
    'credible-pasting-separates-sm-all-rent', ['menu'], ['sm'],
    '固定一个合法实例及确可由完整纯SPE实现的actual有序叶a；L_i(A)在精确h_i,A后的所有完整child-SPE见证上取原受迫者收益极小值。SM-all量化每个带索引合法m元组，含全部排列、重复和own标签。',
    {'menu': '提供全部first-deviation capped孩子可以同时粘合、own孩子必须固定的精确可实现集合。',
     'sm': '只获得离轨极小化、SM*/SD量词对应及不可删的own租金项；SM-all总付款未证。'},
    '每个离轨A≠a_i的最低完整孩子满足L_i(A)≤d_i^σ(A)≤u_i(a)，所以它属于E_{i,A}(a)。源的first-deviation粘合给一份保actual的完整σ⁻，同时对所有离轨列达到L_i(A)；own列仍恰为a，不能取另一个更低收益的actual孩子。对任意σ实现同一a，每个离轨真实d≥L，own真实d=u_i。\n\n定义barL_i(a_i)=u_i，离轨barL=L，及ρ_i=u_i−L_i(a_i)≥0。因此任一有序比较元组T严格有Σ_iL_i(T_i)=Σ_i barL_i(T_i)−Σ_{i:T_i=a_i}ρ_i。没有把嵌套actual孩子互相独立化。\n\n在同一实例上对全部完整σ量化：SM*要求每条可实现a和每个T有ΣbarL≥|∪T|−W，它当且仅当SD要求每份完整σ和每个T有Σd_i^σ(T_i)≥|∪T|−W。SM*⇒SD由逐列d≥barL；SD⇒SM*在给定a把全部真正离轨列同时极小化，再对σ⁻使用SD。原SM-all则还需支付上式明确列出的own租金。只找某最优排列或某最优支持不等于所有有序T；U-ENV/P-ENV中的G最大化也不是L的当前收益极小化。\n\n本边证明的是候选的可实现集合及量词reduction，未推出ΣL≥比较覆盖−W。L_i(A)≤Θ_i≤u_i使SM⇒TB⇒half的条件方向有效，但不支付SM或TB。',
    '精确区分SM-all、保own的SM*与全部真策略SD；保持原完整历史量词，不把已证离轨粘合当作共同金额。',
    [ref(MENU, '保实际叶的全部菜单同时拼合'), ref(MENU, '可信门槛L、SM和TB'), ref(MENU, '在轨租金的完整两人例'), ref(THRESHOLD, 'TB、SM与不同排列量词'), ref(THRESHOLD_REVIEW, 'TB与三个SM版本，及准确反例合同')],
    contribution={
        'result': '全部离轨最低孩子可同时保actual实现；对每个T有ΣL(T)=ΣbarL(T)−Σ_{own}ρ_i。对该实例全部完整SPE量化时SM*⇔SD，原SM-all还必须保留own租金及全有序元组量词。',
        'remaining': '仍须从原游戏全部真实IC证明覆盖净差≤ΣL，或给击中SM-all精确量词的反例。合法粘合、SM*/SD等价、有限阴性以及最优排列存在性均不支付原全称SM-all。',
    })

edge(
    'quadratic-saved-table-excludes-common-customers', ['quad'], ['no_cag'],
    '严格使用保存的三人六标签辅助游戏h=(30,22,22,34,22,26)及全部V_ab=h_a−2G_ab；允许重复行动。待排除的共同客户表示须用同一个标签覆盖映射，客户权重可signed。',
    {'quad': '提供固定整数h/G和完整V表，确定两个重复终局的全部单人收益。',
     'no_cag': '完整得到同支持不同总支付的共同客户表示障碍。'},
    '对s=2e_0+e_3，两个选0者各得(V_00+V_03)/2=(10+14)/2=12，选3者面对双0得V_30=18，总支付42。对r=e_0+2e_3，选0者得V_03=14，两个选3者各得(V_30+V_33)/2=(18+14)/2=16，总支付46。两终局支持都恰{0,3}。\n\n若存在共同客户均分表示，固定每个客户x的权重w_x（容许负数），且客户由所选标签覆盖时，在全部覆盖者间均分，则总支付Σ_i u_i=Σ_{x:c_x>0}Σ_{i覆盖x}w_x/c_x=Σ_{x:c_x>0}w_x。覆盖指示只取决于所选标签支持，不取决于这两个标签的重复人数。所以这两个相同支持终局的总支付必须相同，与42≠46矛盾。有限signed权重不改变守恒消去，故排除的不只是非负客户表示。\n\n这个障碍与该辅助游戏的精确v_3=14、最差SPE总支付42相容；没有否定其精确势性质或安全等号，也不能把42当原CAG福利。禁止重复fresh模型不含这两个重复终局，不能据此直接否它。',
    '只排除这个固定三人六标签收益表的共同客户表示，含signed客户质量；不是一般辅助势定理或原六人half反例。',
    [ref(QUAD, '全部保存点与可复核的6×6静态收益矩阵'), ref(QUAD, '同支持效率失败：连固定三人CAG表都不是')],
    whole_result='同一保存二次游戏在2e0+e3的总支付42、在e0+2e3的总支付46，支持均为{0,3}；共同客户均分表示即使允许signed客户权重也必须支持守恒，因此该固定三人数组不存在共同客户表示。')

edge(
    'maximum-mass-certifies-seven-all-interest-points', ['bpc'], ['two_group'],
    '仅双组程序七个冻结原始点n=3,…,9：m=n、2n个原标签、r_(n,n)=n，全部n客户喜欢全部标签。查询价按原标签的任意有限非负实z计算，τ为原标签权和。没有把有序策略标签商掉。',
    {'bpc': '在单格全兴趣profile上用MM/LO给全部实查询B(1)≤n−1，含重复实际主题。',
     'two_group': '只为七个已保存全兴趣原始点补齐精确全价与静态等号说明；不授其余LP或十输入审计。'},
    '七条冻结点的唯一兴趣子集均为全2n标签，客户数n。任意n个行动的每名玩家利润恒n/n=1，W=OPT_n=n；任意n−1静态竞争槽和任意query标签的收益也恒n/(1+n−1)=1，所以v_n=1。这些是原始点的全输入解析计算，不调用浮点最优状态或新IC扫描。\n\n将客户全体作为单格O，指定任一实际玩家i。p_O=1，任意主题与O的交为n，MM取等；其它n−1人各与S_i交n，LO的两侧均为(n−1)n，所以也取等。源BPC给C(z)≤(τ+n−1)u_i=τ+n−1，及B(1)≤n−1。实际C(z)=n min(1,τ)，取任一标签z=1可得C−τ=n−1，故B(1)=n−1，全价证书在τ=1达到。\n\n源正文按真实集合目录表述。这里只对它的价格/终局式作严格解码：把同覆盖标签的查询权合到共同集合N，总τ、C(z)及实际重复次数均完全保持；这没有商给定动态策略或识别有序历史。亦可直接按原2n标签验证MM/LO，源证明中的全部和式逐项相同。七点本来任何完整策略都SPE，因此其原标签范围独立保留。\n\n结论只认证保存的七个全兴趣等号点及其全实价。程序的其它兴趣向量未必满足MM/LO，末三随机审计输入确不是SPE；源BPC不推出该固定second-group策略全锥解析安全下界，也不重证十例有限执行。',
    '七个保存点的精确全实查询价格及v_n/W等号；保2n原标签和任意有序策略，不把有限点扩大为对称策略锥或一般目录结论。',
    [ref(BPC, '模型、价格和BPC-v2完整条件'), ref(BPC, '任意实τ的自足证明'), ref(TWO_GROUP, '七个冻结记录的全部数值内容与原始点真实性'), ref(TWO_GROUP, '原定义级审计的十个输入与一次实际执行')],
    contribution={
        'result': '对n=3,…,9七个原全兴趣点，u_i=1、W=OPT_n=n、v_n=1，且任意原标签实查询C(z)=n min(1,τ)、B(1)=n−1；它们精确达到BPC的τ=1价格界。',
        'remaining': '目标还含原浮点锥模型/七报告的执行范围及十输入有理审计责任；本边不推出那些执行记录，也不证明其它兴趣点或一般second-group策略锥的安全下界。相应有限/解析责任保留在目标正文及其独立定理。',
    }, kind='specializes')

edge(
    'static-saddle-pays-r22-static-component', ['static53'], ['r22'],
    '同一53单位七标签14兴趣桶，末标签显示名P/B只作索引6重命名；原总人数4包含query本人，静态竞争为不观察query实现的三个合法整数槽，允许重复与全部相关分布。',
    {'static53': '提供目标使用的全部静态原始/对偶匹配及精确数值，而非只对Q七个支持检查。',
     'r22': '只获得其逐人反例的静态分项和与数29/3的精确差；动态完整策略存在性仍由自身另证。'},
    '两对象按相同索引0,…,6使用完全相同14兴趣桶，故静态收益矩阵M_{a,c}相同。query p=(570,570,1197,570,570,1197,1174)/5848；Q在012,016,026,126,346,356,456上的分子为(370,3941,1481,1481,4089,1629,1629)/14620。源全部84三槽多重集下p期望≥t=28481/2924，七个纯query对Q的期望均为t；p/Q非负归一，故对全部query混合及全部343有序三槽词精确夹出v_4=t。84化只压缩静态负载，未压缩任何动态有序历史。紧多重集八个，Q未用的345也紧，不能省略。\n\n本静态分项与给定数29/3相差t−29/3=(85443−84796)/8772=647/8772>0。要把29/3认定为actual第二人收益，必须另给完整策略的动态证据；它不是静态鞍点推论。目标现正文已另固定σ0的400有序动作和actual(6,0,3,4)，以成熟同SHA全部399非空节点2793比较加根7比较、以及后续两份完整原入口证据完成那项责任。本轮实读这些正式证明及复用清单，不重扫2800比较，不把其2219严格/181平局统计转给另有14末位改动的literal σ1。\n\n因此本边是目标静态子证明的精确承接，不把静态保证误授顺序玩家，也不独自宣称得到整条存在反例。两对象比对已完整付清其声明follow-up问题：相同输入/相同真正v_4，不需另开一般静态搜索任务。其实际W=51给W−4t=8800/731>0、2W−OPT=49>0，所以这份逐人反例没有否定聚合或half。',
    'R22反例的静态值与差额子证明；query/竞争槽数、非适应性、整数域和两套完整策略字节身份全部保持。',
    [ref(STATIC53, '静态游戏与真正完整竞争域'), ref(STATIC53, '两个有理概率向量'), ref(STATIC53, '完整84列的精确下界载体'), ref(STATIC53, '全七行的精确对偶上界'), ref(STATIC53_JSON), ref(SPE53, '完整SPE验证的真实证据分解'), ref(FLOOR53, '原独审的完整历史责任，与现可复用证据不同'), ref('archives/customer-attraction/state/审查/正深度付款下界游戏与冻结证书复核--审查.md', '2. 原证书全部策略及非动作字段')],
    contribution={
        'result': 'R22在同一14桶输入上使用的静态分项精确为v4=28481/2924，并有全部84列/七query匹配p/Q；其与数29/3的差恰647/8772>0。',
        'remaining': '整条R22仍需要一份400节点完整纯SPE、其actual路径和第二人确得29/3的动态证明；这些不能由静态安全证书推出。目标当前成熟同SHA正文另行支付该动态责任，本边不把它隐藏成静态来源的推论。',
    })

def deliver_receipt():
    t = json.loads((ROOT / 'research/operations/map-v2/tasks' / (TASK + '.json')).read_text())['definition']
    canonical = 'map/edges/ca-tail-skew-five-six-round29-3b-365b9f01220616d9/ca-two-tail-skew-pays-six-true-copy-envelopes.json'
    shared_id = json.loads((ROOT / canonical).read_text())['edge_id']
    e = {name: record['edge_id'] for record, path in edges for name in [path.stem]}
    coverage = {}

    def cover(key, edge_names, comparison_scope, reason, state='linked'):
        i = ids[key]
        c = {'state': state, 'object_pin': t['input_pins'][i],
             'comparison_scope': comparison_scope, 'reason': reason}
        if state == 'linked':
            c['edge_ids'] = [e[n] if n in e else n for n in edge_names]
        coverage[i] = c

    cover('balance', ['same-source-mean-cap-payment-reduction'],
          '当前v2主陈述及共同付款、三域、三份内部复核/入口、真实重放问题与全部三份reset/copy/flow依赖全文。对M-d30c…in-packet核全行可信端点cap与GLOBAL-NET raw域的差别；SOURCE-BAL/STATIC固定同源同点。',
          '从已证原source账精确把候选付款化为W≥((2m−1)γ−Qstat)/2，并保half充分方向。没有证明该阈值；与NET局部边之间缺允许列、可信闭包和价格/源容量运输，因此未造跨域推导。')
    cover('pay', ['same-source-mean-cap-payment-reduction'],
          '当前v2开放全称PAY；与M-3037…同模型同source同L的账比较，并对声明对端M-d30c…的RESET/EDGE/PAIR、加权floor及最后零功边全文核实。',
          '本边仅接受候选的精确reduction与条件half方向；其源为已证M-3037…。PAY仍open，G不能重复领，行价不统一，raw重放的祖先/同叶余项未支付本域Cov。')

    coarse_scope = '比例算法、全额atom/返还定理、零返还/首失败审查、52客户原审计合同及两份CLAIMS全文；保持固定T、d/H/J、query叶、分母和原路由。'
    cover('origin', ['joint-coarse-and-atom-dispersion', 'first-failed-owner-cut-exact-atom-rebate'],
          coarse_scope,
          '旧比例费用和price与独立atom式在同一全额K上比较，保粗类嵌入和指定首失败cut=z_j。首失败λ只是旧族的分离价，细化后按离散返还改变；未沿用旧贪心作为atom算法，也未证明任意SPE修复成功。')
    cover('atom', ['joint-coarse-and-atom-dispersion', 'atom-dispersion-zero-price-domains'],
          coarse_scope + '全价格分离的量词是存在同一个y同时满足全部cap，不是每价另择y。',
          '已证全额真实atom缩放与凸分离保证共同盒判据；与粗式共同导出精确返还、类包含及两类零返还。未追踪固定余流必须逐角色入A，修后d′可超过旧u，最后仍用一份2u预算。')
    cover('disp', ['joint-coarse-and-atom-dispersion', 'atom-dispersion-zero-price-domains', 'first-failed-owner-cut-exact-atom-rebate'],
          coarse_scope + '全非负实价及目标自身抽象三角严格例；真实52点只owner不同、终端同末位，不认证真实严格优势。',
          '两共同前提给min(D,E)精确差，二值/单调价使其0，旧首败价在紧owner上变成半绝对离散。抽象严格包含与真实SPE实现分别保留；常数价总资金未增加。')
    cover('fail', ['first-failed-owner-cut-exact-atom-rebate'],
          coarse_scope + '只核旧首败j的指定回推价格，所有i≥j未来价0和此前饱和/未饱和两类逐项展开。',
          '完整推出目标半质量加权绝对离散及新同价违反ε−返还；未断言返还总够、未认旧price为新盒最坏价。')
    cover('zero', ['atom-dispersion-zero-price-domains'],
          coarse_scope + '逐owner证明全部二值及角色单调非负价，并按后缀S_k精确代SOURCE-PRICE。',
          '严格future概率行让q_a在价格区间内或owner价同侧，返还逐owner为0。后缀式保初始owner b及同次A，不能替成原F的incoming或其它核的钱包。')

    cover('menu', ['credible-pasting-separates-sm-all-rent'],
          '固定actual资源全文，保E/U-ENV/P-ENV/最低L、SM*/SD与两人租金例；原完整菜单诊断全文；共同列门槛、动态共同付款候选和净差量词审查全文。',
          '已证first-deviation粘合精确支持同时off列极小化及SM*/SD量词消元。SM-all额外扣own租金，G最大化包络不等于最低当前收益；所有菜单兼容性仍未付覆盖净差。')
    cover('bank', [],
          '当前M-000c…完整必要式及同页经济/银行同时改变、非均匀银行BR和共同目录闭包；与同组RENT-t、开放UNPAID、fixed-actual包络、SM-all和九客户两池参数比较。检索现有核心相关边，并核登记的原Cartesian银行反族精确身份。',
          '该结果仅对固定BASE/PUNISH/EXIT控制器重标均匀a,b：中间人遵从a/(m−1)+b，联合fresh偏离a+b/2，必要IC等价根u1≥a，使遗漏(m−2)a不反MIN-NET。RENT-t只是在任意固定真实鞍点上的恒等账，不能推出这一特定控制器的收益/续局；反向必要IC也不付跨枝R。九客户两池非该Cartesian控制器。当前比较范围未得有效逻辑边；一般非均匀新控制器须另证全目录真实BR，非本包待补身份问题。',
          state='isolated-after-review')
    cover('rent_open', ['weighted-rent-common-payment-reduction'],
          '当前开放UNPAID逐字量词；同页真正鞍点、行动折扣、同枝R/H及RENT-t全文，并与全行credible mean-cap原source付款比较。',
          '获得准确强付款W≥mγ的等价重写。未取得共同租金上界；这是与PAY不同的域和银行，不从BANK构造必要式或KKT领取第二笔钱。')
    cover('rent', ['weighted-rent-common-payment-reduction'],
          '同页PRICE/SIGNED/DISCIPLINE/RENT-t及first-deviation合法重选；固定actual菜单资源、共同列门槛和全行cap内部审查全文。',
          '已证同一真实枝价格差给UNPAID⇔W≥mγ的局部reduction。原模型/静态质量可用，但源域扩大、纯叶拼合与均值彩票各有不同资格，未把它们串成无条件half。')
    cover('sm', ['credible-pasting-separates-sm-all-rent'],
          '当前v1的SM-all、最低完整孩子、全部有序m元组；固定actual正文和动态门槛两篇全部量词、旧匹配净差、UV边界及SM三个版本全文。',
          '局部边保off列同时极小化、ΣL=ΣbarL−own租金与全策略SM*⇔SD。原SM-all仍open，未误用一个最优排列失败反存在版，未用19有限阴性或已证五人half逆推它。')

    quad_scope = '保存二次游戏完整h、36项V/G、静态上下界、全历史支配、同支持42/46及模型边界全文；与双组原客户/九客户原SPE静态域比较。'
    cover('no_cag', ['quadratic-saved-table-excludes-common-customers'], quad_scope,
          '同支持两个重复终局支付不同，精确否定此固定收益表的共同客户表示，signed权重亦不例外。没有否定保存点自己的辅助势/安全等号，也未把辅助总支付移作原客户覆盖。')
    cover('quad', ['quadratic-saved-table-excludes-common-customers'], quad_scope,
          '保v3=14、最差SPE总支付42、gap0的完整解析证据。它的矩阵还推出共同客户表示不可能；5000次旧探测/其它有限势点/fresh禁重复游戏均未获得此单点的量词授权。')

    cover('two_group', ['maximum-mass-certifies-seven-all-interest-points'],
          '双组程序全文：固定second-group策略的对称锥、七个n3…9全兴趣原始点、全部十输入/16824比较的原记录及PASS范围；对照BPC单格MM/LO全部实查询。',
          '只为七个原始点给BPC全实价锐值B(1)=n−1，且每标签/每背景收益恒1、W=n。十输入中7真SPE/3非SPE的原审计保持有限；没有把本局部边冒作整个锥的LP最优证明或十输入全SPE。')
    cover('bpc', ['maximum-mass-certifies-seven-all-interest-points'],
          'BPC正文全实τ证明、MM/LO、orbit/balanced层级、双块covariance和重复限制、单minority的完整SPE推论全文；与双组保存全兴趣点和九客户最小角色进行结构条件核对。',
          'MM/LO在七个全兴趣点均等号，精确得到全价B(1)=n−1并保原同覆盖标签的查询解码。一般双组profile的minority不必最小，九客户最小根主题更不满足MM；没有从SPE或对称字样免费推出结构条件。')
    cover('static53', ['static-saddle-pays-r22-static-component'],
          '53点静态正文和7×84完整有理数据；14桶完整输入、动态构造、正深度出处、literal14差审计、追加R22 v3及其两篇当前原审查和sameSHA充分验证清单全文。',
          '目标的精确静态分项与647/8772算术差由本对象支付；R22的400节点SPE证明另由自身成熟证据负责，未暗藏为静态推论。84/343等价仅静态负载，未混四竞争槽、分数背景、适应性后继或另一literal策略。声明follow-up已实读关闭。')
    cover('nine', [],
          '九客户构造完整六类型、全部43动作、末位36值和第二位36真回复表、六根偏离枝、实际345及浮点搜索合同全文；对照本包BPC条件、SM/银行构造及原动态/static量词。',
          '这是m3、old0、单fresh组的h=a−x/2=0可行点，W8/OPT9、根最小收益2；不付全族h≤0上界、old>0或六人迁移。root标签3仅2客户，而标签1/2各4客户。任一分区逐格MM求和都要求所有|T|≤|S3|，故BPC的最小角色MM不可能成立；不能据两池名称连到Cartesian银行控制器，亦不把浮点目标0当全族证明。本实际比较范围无成立逻辑边。',
          state='isolated-after-review')
    cover('eight', [shared_id],
          '八根正文全部八组B/C/非零乘子；原verify.py、三cut、三report全部512 base_minima；末两人税和残余利润定义全文。直接复用已canonical同pin边ca-two-tail-skew-pays-six-true-copy-envelopes的完整解释。',
          '既有边以同σ真实末两人三IC和两末位BR给强PAIR，再用原非负权与13/15位完整余项证明八界，兼保每枝3λδ扣减。所有源码/输入/报告SHA与本包一致，未重跑139264型扫描或旧LP，不另造同一逻辑边；八界不单独闭合六人half。')

    assert set(coverage) == set(t['object_ids'])
    assets = [ref(str(path.relative_to(ROOT))) for _, path in edges]
    assets.append(ref(canonical))
    receipt = {
        'coverage': coverage,
        'assets': assets,
        'closed_overlaps': [
            {'core_id': ids['static53'], 'peer_id': ids['r22'],
             'reason': 'R22追加当前pin0648a6…且body/evidence current。相同14桶输入的84多重集/七query静态匹配值t=28481/2924恰与R22所用相同；R22自身成熟完整σ0证据给actual第二29/3，差647/8772。以局部边明确静态/动态责任后，该精确follow-up已解决，无需发布重复3B；聚合和half均未被反驳。'},
        ],
        'follow_up_tasks': [],
        'task_id': TASK,
        'object_ids': t['object_ids'],
        'read_object_ids': t['read_object_ids'],
        'input_pins': t['input_pins'],
    }
    receipt_path = ROOT / 'map/receipts' / (TASK + '.json')
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')

    reading = []
    for a in t['context_plan']['reading_refs']:
        p = ROOT / a['path']
        reading.append({**a, 'read_start_line': 1, 'read_end_line': len(p.read_text().splitlines()),
                        'full_file_read': True, 'current_sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    review = {
        'task_id': TASK,
        'core_count': len(t['object_ids']),
        'comparison_group_count': len(t['context_plan']['comparison_groups']),
        'read_count_after_native_add': len(t['read_object_ids']),
        'new_edge_count': len(edges),
        'reused_canonical_edge': ref(canonical),
        'coverage_counts': {s: sum(c['state'] == s for c in coverage.values()) for s in ['linked', 'isolated-after-review', 'needs-decision']},
        'declared_reading_refs': reading,
        'additional_R22_full_read': [ref('archives/customer-attraction/state/审查/正深度付款下界游戏与冻结证书复核--审查.md'), ref('archives/customer-attraction/state/审查/预留菜单盲审三源实质复核--审查.md'), ref('archives/customer-attraction/tools/evidence/endogenous-padding-and-security-primary/reused-SPE-validation-manifest.json'), ref('archives/customer-attraction/tools/evidence/disjoint-reservation-literal-audit-four-primary/prior-sufficient-SPE-evidence-manifest.json')],
        'new_mathematical_program_runs': {'LP': 0, 'MILP': 0, 'IC_scan': 0, 'BI': 0, 'membership_type_scan': 0, 'random_search': 0},
        'new_logic_scope': {'whole_result': [r['edge_id'] for r, _ in edges if 'whole_result' in r], 'contribution': [r['edge_id'] for r, _ in edges if 'contribution' in r]},
        'parent_next_steps': 'Boss审读后串行edge-bind --write、edge-check，刷新receipt各asset SHA后checkpoint/push/done；worker未执行Git/queue/sync/shared registry/integration/source写入。',
    }
    (Path(__file__).parent / 'read-and-comparison-review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    return receipt_path, review

if __name__ == '__main__':
    receipt_path, review = deliver_receipt()
    print(json.dumps({'written': len(edges), 'receipt': str(receipt_path.relative_to(ROOT)),
                      'coverage': review['coverage_counts'],
                      'paths': [str(p.relative_to(ROOT)) for _, p in edges]}, ensure_ascii=False, indent=2))
