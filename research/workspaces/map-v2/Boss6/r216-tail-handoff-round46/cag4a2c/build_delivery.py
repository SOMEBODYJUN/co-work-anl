from pathlib import Path
import json, hashlib, sys, difflib
ROOT=Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT=Path('/workspace/scratch/bbb425bb840f/boss6-staging/map-cag4a2c-round45')
TASK='customer-attraction-3a-3a-4a2c4758d3d07c0a'
ED=Path('map/edges')/TASK
(OUT/ED).mkdir(parents=True,exist_ok=True)
registry=json.loads((ROOT/'research/registry.json').read_text()); objects={o['object_id']:o for o in registry['objects']}
sys.path.insert(0,str(ROOT/'tools')); import research_runtime as rr

def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):
 p=OUT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ref(path,sec=None):
 d={'path':path,'sha256':sha((ROOT/path).read_bytes())}
 if sec:d['section']=sec
 return d
model='archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
sharp='archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md'
decor='archives/customer-attraction/state/引理/单后继去相关恒等式--引理.md'
forest='archives/customer-attraction/state/候选/森林关联目录的逐人末位阈值与终局保护接口--候选.md'
occ='archives/customer-attraction/state/引理/整数后继占用储备的全菜单自税分解--引理.md'
bank='archives/customer-attraction/state/定理/前缀保险的静态安全双证与聚合稀释--定理.md'
compiler='archives/customer-attraction/state/定理/真实退出缺陷的统一与异质前缀修复--定理.md'
dp='archives/customer-attraction/state/程序/同序可信最低续局矩阵的精确路径动态规划--程序.md'
support='archives/customer-attraction/state/程序/同序可信菜单的三份探针与整数掩码故障--程序.md'
binary='archives/customer-attraction/state/定理/二值背景四尾两斜率利润界--定理.md'
maxroot='archives/customer-attraction/state/引理/五人最大主题根容量切割--引理.md'
IDS={
 'sharp':'customer-attraction/true-final-reply-push-sharp-curvature-and-two-branch-identity',
 'decor':'customer-attraction/one-follower-decorrelation',
 'utp':'M-1adc80a127be4f10b8847cb730b12380',
 'forest':'customer-attraction/forest-incidence-individual-last-slot-threshold-and-UTP',
 'occ':'customer-attraction/integer-successor-occupation-reserve-and-self-tax-decomposition',
 'gap':'M-baa3cc8d26b049de921bbae4e67206a3',
 'bank':'M-a04a790aa08742539701cd4a2f658920',
 'aggregate':'M-8abb8983f4c749679d617a56b7ce4cda',
 'compiler':'R22-PREFIX-CREDIBLE-EXIT-COMPILER-v1',
 'dp':'customer-attraction/ordered-credible-minimum-continuation-matrix-exact-path-DP',
 'support':'customer-attraction/ordered-credible-menu-three-probes-and-integer-mask-failure',
 'binary':'customer-attraction/binary-four-tail-two-slope-profit',
 'maxroot':'customer-attraction/five-player-maximum-theme-root-capacity'}
new=[]
def edge(name,sources,targets,conditions,roles,explanation,scope,evidence,whole=None,contribution=None,conditional=False):
 e={'edge_id':'cag-4a2c45-'+name,'kind':'implies','status':'accepted','source_ids':[IDS.get(s,s) for s in sources],'target_ids':[IDS.get(t,t) for t in targets],'premises_mode':'all','relation_mode':'conditional' if conditional else 'unconditional','conditions':conditions,'roles':{IDS.get(k,k):v for k,v in roles.items()},'explanation':explanation,'scope':scope,'evidence':evidence,'reviewed_by':'Boss6/map-cag4a2c-round45-worker','review_note':'完整实读所列现行陈述及承重正文后逐式比较；复用成熟精确证明/证书，不重跑旧LP、SPE全树或有限扫描。关系的完整/局部范围按本字段明确，来源原计算不记本轮执行。'}
 if whole:e['whole_result']=whole
 if contribution:e['contribution']=contribution
 e.update(rr.edge_bindings(ROOT,e,objects,verify=True))
 p=ED/(name+'.json');write(p,e);new.append((p,e))

edge('sharp-reply-pays-deleted-slot-decorrelation',['sharp'],['decor'],
'有限单位客户、有限非空共同标签目录；固定合法有序过去b且恰两位剩余，B(A)为同一完整计划在每个相关末位历史的真实最佳回复；A,A′ iid同p。菜单封顶另要求当前节点也满足同一计划的真实IC，背景计入原总人数n。',
{'sharp':'其完整陈述中的L为两条真实末位BR之间的平均松弛，L≥0且f−g展开给L=Σw(pq−j)。本边使用这一末位松弛，不把完整两槽C当删槽查询。','decor':'得到删当前槽的精确独立化恒等式、真实竞争菜单z≤u及v_n≤z。'},
'''固定b，置f(X)=Σ_{x∈X}1/(b_x+1)、g(X,Y)=Σ_{x∈X∩Y}1/((b_x+1)(b_x+2))，U_b(X,Y)=f(X)−g(X,Y)。source的真实末位松弛为L=E[U_b(B(A),A)−U_b(B(A′),A)]≥0。B(A′)只是历史A后的合法行动，并未被当作该节点最佳；非负来自同一σ逐节点BR。因A与A′同分布，两个f(B(·))期望相消，L=E[g(A,B(A′))−g(A,B(A))]，这也恰等于E U_b(A,B(A))−E U_b(A,B(A′))，即target整条恒等式。

固定过去和当前节点，列c(A)由全部过去主题及B(A)组成，删除的是当前行动A；M_{T,A}=Σ_{x∈T}1/(1+c(A)_x)。source的完整两槽查询另保A，分母多一个A会员位，不在此混用。对任意p，刚得pᵀMp≤Σ_Ap_AM_{A,A}。当前真实IC使所有M_{A,A}≤u，所以min_QpᵀMQ≤pᵀMp≤u。有限minimax给z=max_p min_QpᵀMQ≤u。每c(A)都是原总人数n−1个合法竞争槽，故真正静态值v_n的对偶允许更多列，v_n≤z。整数真实过去属于source允许的实b域，不反向把任意实b称为合法历史。''',
'完整目标只涉及恰一真实后继及删当前槽；任意离轨平局、空主题、同覆盖异标签和重复行动均保留。无多后继独立化或全位置聚合结论。',
[ref(sharp,'完整输入和独立审查身份'),ref(sharp,'精确非负分解'),ref(decor),ref(model,'策略、真实续局与全部历史量词')],
whole='对target全部合法过去、任意p及任意真实末位BR，完整得到其删当前槽恒等式与非负号；当前也满足SPE时完整得到v_n≤z≤u。')

edge('forest-utp-pays-individual-threshold',['utp'],['forest'],
'固定一个全目录压缩关联图为森林的有限单位客户实例、全游戏人数m≥1及其θ_m；假设source所述UTP对每个合法计数前缀成立。策略仍量化全部有序历史，不要求同计数节点同selector。',
{'utp':'提供每个前缀存在T且对所有相容终局统一保护的开放前提；前提只要求严格后继≥同一全游戏θ_m。','forest':'按真实偏离后的同σ子博弈逆归纳得到每位≥θ_m，再与静态(S)合成条件福利界。'},
'''固定同一实例的θ_m，按剩余人数r对每个有序历史归纳。r=1时该历史负载总槽m−1，末位最佳值M(b)≥θ_m。r≥2时，对当前历史的计数b选UTP给出的T作为当前真实偏离；该偏离之后仍沿所给完整σ，每个后继节点继承同一完整SPE，归纳已保证全部后继角色的最终利润≥θ_m。实际得到的终局q满足q≥b+e_T且总人口m，因此UTP的全终局蕴含给强制T的当前人也≥θ_m。当前节点真实IC把此界转给规定行动。若后继重复T，UTP前提已含当前同主题份额的界，仍无漏洞。过去角色不属于UTP前提。

最后逐位求和W≥mθ_m。独立静态证明：固定任意m−1槽背景k和一个最优m元组的重数d_x，对d_x>0用1≤(d_x+k_x)/(1+k_x)，第一部分Σ_x d_x/(1+k_x)≤mM(k)，第二部分按m−1个背景槽至多(m−1)M(k)，故OPT_m≤(2m−1)M(k)，取最小得OPT_m≤(2m−1)θ_m。于是W≥m OPT_m/(2m−1)。这里左端是覆盖客户数Σ_{d_x>0}1，不能写Σd_x。附带R216旧证据页恰有这一笔误，已另附最小修订；主candidate正文(S)正确。本边一般推导使用该正确主正文。

source UTP自身仍open。每个T不同坏终局q^T如何沿森林同时拼成同一个m−1背景尚未证明，本边不填这个缺口，也不拿一般图或有限阴性反例代替森林结构。''',
'这是“所有前缀UTP⇒所有完整SPE逐人θ_m及其条件福利”的完整蕴含。开放前提保持开放，relation_mode为conditional；不把θ_m改θ_r，不要求count统一策略。',
[ref(forest,'更明确的UTP终局保护接口'),ref(forest,'已证的通用静态界与条件福利推论'),ref(forest,'尚缺的叶消息及比例陷阱'),ref(model)],
whole='若source逐前缀UTP在该关联森林输入上成立，则target全部有序历史、每份完整纯SPE、每位收益≥固定θ_m；并有通用静态OPT_m≤(2m−1)θ_m及条件福利W≥mOPT_m/(2m−1)。',conditional=True)

edge('occupation-conservation-pays-current-gap',['occ'],['gap'],
'固定合法整数过去b、余n+1人且n≥1，以及同一完整形式计划的全部强制当前分支；a∈{0,1}，k∈{0,…,n}整数，d=1+b+a+k；所有期望来自同一当前分布p。q=Pp只平均真实n个后继主题，不预设后继SPE。',
{'occ':'给同一I、V+与qᵀKp之间的完整守恒nqᵀKp=V++I，保额外槽分母及整数负载。','gap':'用一次self-tax抵消同负载交叉项的精确正分解支付G−D，再合守恒；D换u另需当前IC。'},
'''对一客户，source的I=(1/2)E[Δk(Δk+Δa)/(dd′)]。定义Qself=E[a/((b+1+k)(b+2+k))]，真实当前分母在a=1时为d−1。直接展开G_x−D_x=(1/2)E[Δa(Δa+Δk)/(dd′)]−Qself，所以I_x−(G_x−D_x)=Qself+(1/2)E[(Δk²−Δa²)/(dd′)]。

唯一可能负项是Δk=0、Δa=±1。对每j，两种有序交叉对的概率共2p_(1,j)p_(0,j)，与1/2抵消后为−p_(1,j)p_(0,j)/((b+1+j)(b+2+j))。和同一个Qself合并为Σ_j p_(1,j)(1−p_(0,j))/((b+1+j)(b+2+j))。剩下Δk≠0时整数平方≥1≥Δa²。因此精确得到target正分解，两个显示部分均非负，故I≥G−D。

与source同一份守恒相加：G+V+≤D+I+V+=D+nqᵀKp。若当前节点对同一完整计划的每个真实强制分支满足IC，D≤u，才可再≤u+nqᵀKp。后继理性不曾使用。Qself只合一次，不再在结尾额外扣税。V+分母比原真实叶多一个额外查询槽，不能替换原尾利润；本论证不控制另一侧pᵀKq或对称方向导数。分数k的负边界不属于本整数域。''',
'完整target的逐客户正分解、CURRENT-GAP与带另付当前IC的推论；无跨枝钱包、WD普遍正导数或half结论。',
[ref(occ,'1. 同一固定计划、全部当前行动及整数负载'),ref(occ,'2. 占用恒等式与逐对非负'),ref(occ,'3. 同一self-tax只付一次：I≥G−D'),ref(occ,'4. 整数边界不是所有分数质量的结论')],
whole='对target全部整数完整计划和p，完整得到其精确非负分解、I≥G−D及G+V+≤D+nqᵀKp；只有另满足当前同计划IC时，完整得到G+V+≤u+nqᵀKp。')

edge('compiler-and-bank-pay-aggregate-deficits',['compiler','bank'],['aggregate'],
'固定m≥2、1≤j<m的同人数真实前缀编译输入：目标z的第j位后有给定完整真尾；ell_i遍历所有强制行动含正常动作后的完整后继SPE，Δ=max_i(M_i−u_i)_+。正有理s≥Δ；旧客户和保险客户不交，目录完整Cartesian。统一清分母复制全部旧新客户。',
{'compiler':'承担全坐标首次联合异常后永久真孩子拼接、新策略全历史SPE、保旧z，以及精确W′与OPT′。','bank':'承担j个2s银行、ks蓄水、k−1个s叶的静态原始/对偶匹配v_m(bank)=s。','aggregate':'结合Cartesian静态安全值精确可加得到三种差额成本、固定(m,j)强弱桥的稳健等价及零端点。'},
'''令k=m−j。bank共有m个不交块，块大小n_D s，Σ_D n_D=2m−1。p_D=n_D/(2m−1)对任意m−1槽背景由Cauchy保证至少s；q_D=n_D−1是合法总槽m−1确定背景，所有块查询恰s。因此v_bank=s。

完整Cartesian的任一确定产品竞争元组投影为两个组件的m−1元组，查询利润相加。组件最优原始查询的独立乘积保证v_old+v_bank；反向把组件最优对偶背景独立抽取并逐槽配对，对每个确定联合查询都≤两值和，故v′=v+s。这里不推产品SPE坐标可分；新策略的真实IC由compiler的首次任意联合异常（包括只改保险或只改旧主题）永久进入真孩子证明承担。

compiler给W′=W+(m+j)s、OPT′=OPT+(2m−1)s，代入v′=v+s得到：mv′−W′=(mv−W)−js；(m−1/2)v′−W′=((m−1/2)v−W)−(j+1/2)s；OPT′−2W′=(OPT−2W)−(2j+1)s。三种旧差额不同，严格种子须各自超过自己的成本，不能互换；本边没有提供任何严格种子。

固定(m,j)，若强安全桥对所有完整SPE成立，对任何Δ>0编译输入取s=Δ即得mv−W≤jΔ；弱桥同理给(m−1/2)v−W≤(j+1/2)Δ。Δ=0时compiler从给定真尾向前逐级拼贴其它行动最低真孩子，保旧路径直接成完整SPE，无需零银行或极限。反向若全部编译输入满足相应预算，对任意实际完整SPE用其真尾和Δ=0即恢复相应桥。固定数值j只涵m≥j+1，m=1另有W=v1=OPT1。''',
'完整target关于正尺度差额、强/弱固定人数稳健等价及零端点；ALL两个输入缺一不可。编译器提供的是具体合法新SPE，并非证明普遍安全桥或half。',
[ref(bank,'真正静态安全值与产品方向'),ref(bank,'任意前j保险bank的显式双证'),ref(bank,'三种坏差额只共用编译器，不是同一目标'),ref(bank,'稳健等价的固定人数和零端点'),ref(compiler,'统一修复的全坐标首次退出与精确最优'),ref(compiler,'零端点、等价量词与当前五人推论')],
whole='对完整target输入v′=v+s，强/弱/half差额分别精确减少js、(j+1/2)s、(2j+1)s；固定合法(m,j)的强、弱全SPE安全桥分别等价于全部编译输入相应旧差额≤jΔ、≤(j+1/2)Δ，Δ=0由真实拼合处理。')

edge('support-dp-supplies-path-dp-comparison-state',['support'],['dp'],
'给定target的正确R(k)、threshold M(k)、Fraction矩阵L(k,t)，固定根可实现q；对每个固定可实现actual有序路径，取其逐层前缀k_i对应的L_i(t)。source支持DP适用于任何这样的精确矩阵。',
{'support':'提供长度m、有序、允许重复且终态支持恰S的比较维度最小和归纳；每重复一次仍付一次L。','dp':'把该比较维度提升到(k,mask)，另需自身的全部actual路径合法性及合并充分性证明。'},
'''固定一条可实现actual路径h，source的d_i(M)精确最小化前i个比较行动的ΣL(k_i,t)，其中已用标签集合恰M。末行动t唯一给前i−1段和一步L，故转移保全部有序tuple；不同顺序和重复各自计费，只在最终cover(mask)去重。对cover(S)=OPT的支持取最小恰给该路径全部最优比较元组的cost，若不限定cover则也给全部比较元组。

target将actual前缀k作为额外状态，并为固定q同时选择下一actual a。每次先付当前L(k,t)，再迁移(k+e_a,mask∪{t})；因此source的比较维度及重复/支持语义可直接使用。它不独自证明actual转移恰好枚举全部有序SPE路径，也不独自证明不同actual histories到同k时未来可合并。本edge只登记这一比较维度的已证贡献。

完整target另以k_a<q_a、q∈R(k+e_a)、u_a(q)≥M(k)证明actual合法性，并用L和合法动作集只依k,q、最终覆盖只依mask证明保最小成本无损。这些另行证明在target正文已成立；它们仍是由本贡献走到整个target所需的步骤，不冒作source单独给出的结论。actual列L也最小化可改变actual尾的其它子SPE，不等SM*、固定σ菜单或fixed-f税递推。''',
'accepted的局部算法贡献，不以source单前提宣称整个actual×comparison联合DP、19历史成功项或普遍SM。原theta_dp字面整数in错误仍保留，未运行修复。',
[ref(support,'4. 意图中的支持动态规划为何可用，以及尚未执行什么'),ref(dp,'为什么(k,mask)合并无损'),ref(dp,'固定q时全部actual路径的合法域'),ref(dp,'best、bestopt和停止规则')],
contribution={'result':'对每条固定可实现actual路径，精确最小化全部长度m有序比较tuple的Σ_i L(k_i,T_i)，终态支持去重、重复主题逐次付款；该比较维度可原样纳入(k,mask)联合状态。','remaining':'整个target还须证明actual合法转移枚举全部可实现路径、同(k,mask)未来充分性、跨全部根q/终态的最小化；这些由target独立证明承担，本边未以source算法替代。普遍SM非负更没有由精确最小化算法自动推出。'})

edge('binary-four-tail-pays-five-root-capacity',['binary'],['maxroot'],
'恰五人、有限单位客户共同标签目录、任意完整有序历史纯SPE σ；u为actual第一人收益，K为全目录最大主题大小。强制任意最大主题T后沿同σ得到真实四尾，比较始终使用同一最优五索引元组，允许重复/空主题。',
{'binary':'在T造成的二值背景1_T和actual首题造成的二值背景1_A0，对每个四比较索引补元给同一四尾两斜率预算1999V0/1000+5V1/3。','maxroot':'通过整数根容量、同一最优元组五补元平均及根IC z≤u得到全部四条容量行、任意主题后两切割和actual首步行。'},
'''K=0时各量0。K>0时每实际节点改最大主题至少K/5，故每人≥K/5，K/5≤u≤K≤W且O≤5K。强制根最大主题T后的真实四尾从T内取得V1=K−z，外取得V0=尾外覆盖，原根IC给K/5≤z≤u。内部客户总负载c∈{1,…,5}，四尾主题总成员≤4K，所以V0≤5K−Σ_T c。对k=1,…,4，c+k(k+1)/c−(2k+1)=(c−k)(c−k−1)/c≥0，故V0≤(4−2k)K+k(k+1)z。Cauchy另给V0≤5K−K²/z；只在K>0时除z。

固定一个最优五索引元组并集U、O=|U|。对每个索引i删去它得四元组T_−i。source在同一个背景1_T、同一个真实四尾上同时给R_(1_T)(T_−i)≤aV0+bV1，a=1999/1000,b=5/3。客户在最优五元组中出现j次：若不在T，平均贡献为4/5(j1)或1(j≥2)；若在T，平均贡献1−6/[5(j+1)]≥2/5。因此五补元平均≥4O/5−2|T∩U|/5≥4O/5−2K/5，得4O/5≤aV0+bV1+2K/5。五条比较只平均同一预算，没有付五份互斥枝利润。

代入V1=K−z和四容量上界，z系数ak(k+1)−b均正，可用z≤u。k1…4精确化整得到1200O≤9097K+3497u；1200O≤3100K+15491u；1200O+2897K≤33482u；600O+4447K≤28735u。每合法Q有|Q|≤K，后两行左侧正K系数可弱化为|Q|，方向保持。

在actual分支首题A0大小L，真实四尾有V0=W−L,V1=L−u。同一source及五补元平均先保|A0∩U|≤L，得2400O≤5997W−5000u+203L≤5997W−5000u+203K。actual首题从未被要求最大。全部source应用为合法二值背景后的恰四真尾，强制根不当新最优者。''',
'完整target全部必要不等式与域。它不单独half，也不把允许O/W>2的标量松弛点称SPE；四尾总利润始终按同背景R计算。',
[ref(binary,'1. 完整模型与精确目标'),ref(binary,'2. 同一完整策略的两条真实路径'),ref(binary,'4. 完整客户域的精确恒等式'),ref(maxroot)],
whole='对target全部五人完整SPE，得到最大根四个整数容量切割、独立Cauchy容量、四条全局整系数行、任意合法Q的后两切割及actual首步2400O≤5997W−5000u+203K，完整保同σ与同最优五元组。')

# Complete replacement and zero-context patch remain outside canonical source.
err='archives/customer-attraction/state/审查/R216可信攻击与森林前缀候选的证据边界增量--审查.md'
old=(ROOT/err).read_text()
bad=r'$$\sum_x d_x\le mM(k)+(m-1)M(k)=(2m-1)M(k),$$'
good=r'$$\operatorname{OPT}_m=\sum_{x:d_x>0}1\le mM(k)+(m-1)M(k)=(2m-1)M(k),$$'
assert old.count(bad)==1
replacement=old.replace(bad,good)
replacement_path=ED/'R216-corrected-full-replacement.md';(OUT/replacement_path).write_text(replacement)
patch=''.join(difflib.unified_diff(old.splitlines(True),replacement.splitlines(True),fromfile='a/'+err,tofile='b/'+err,n=0))
(OUT/ED/'R216-coverage-count-fix.patch').write_text(patch)
impact=[]
for o in objects.values():
 hits=[r for r in [o['body']]+o.get('evidence',[]) if r.get('path')==err]
 if hits:impact.append({'object_id':o['object_id'],'version':o['version'],'object_pin':rr.pin(o),'references':hits,'semantic_effect':'forest静态证据公式笔误修正；另一节数学不变但全文字节SHA变化，均须更新引用并增record版本。'})
write(ED/'source-correction-impact.json',{'source':ref(err),'replacement_sha256':sha(replacement.encode()),'minimal_exact_replacement':{'old':bad,'new':good},'proof_of_error':'m=2，单客户单非空主题，最优比较两次同题d_x=2，唯一背景k_x=1，M=1/2；误式给2≤3/2。正确式左侧覆盖客户数1。','mathematical_scope':'主forest candidate正文静态(S)已正确，UTP与F-THETA开放状态不变。此补丁只修证据笔误，不新增定理或反例对象。','affected_registry_records':impact,'root_actions_required':'先保存本完整成熟稿/handoff；Root修规范源、更新所有命中SHA与record版本、baseline/registry及受影响任务。核心forest改版后用fresh worker窄续本组，不由当前worker冒充新core已审。','proposed_patch':str(ED/'R216-coverage-count-fix.patch'),'full_replacement':str(replacement_path)})
print(json.dumps({'new_edges':len(new),'files':[str(p) for p,_ in new],'correction_affected_ids':[x['object_id'] for x in impact]},ensure_ascii=False))
