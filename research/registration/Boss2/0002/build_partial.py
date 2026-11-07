from pathlib import Path
import hashlib,json,re,os
ROOT=Path(__file__).resolve().parents[4]
os.chdir(ROOT)
DIR=Path('research/registration/Boss2/0002')
TASK='register-ab98f323ad-0002'
DEFINITION=json.loads(Path(f'research/operations/p25-register-v2/tasks/{TASK}.json').read_text())['definition']
R=DEFINITION['materials']
BASE='archives/customer-attraction/state/'
EV='archives/customer-attraction/tools/evidence/'
MODEL='有限单位客户、有限非空共同带标签目录、单位提供者逐个选一次，终局覆盖客户由覆盖者均分；完整有序历史纯SPE保重复、空覆盖、覆盖别名与离轨弱平局。'
DEFM='定义/共同目录完整历史模型--定义.md'
FDEF='定义/自由分数背景安全门槛--定义.md'
A=['M-7678ce7b20a04e4b806dbaee70d44dd9','M-fa37479c5ed0448cb7fa1f4c7382453c','M-39733c91afe1408f86effa7888f32759','M-8a4b526ab7b74b65904a6858c9fd9f29','M-b303a38dafc844778e3fadc6887f8234','M-05993f95c99e49298a6212e9e4e69469','M-d07633272d954434bc6edbda3b9bd0f4']
O=[]; M={}; decisions={}
def src(path):
    s=Path(path).read_text().split('---',2)[1]
    return list(dict.fromkeys(re.findall(r'source:[0-9a-f]{40}:[^"\n,\]]+',s)))
def ref(x, section=None):
    if isinstance(x,tuple): return ref(*x)
    if isinstance(x,int): r=dict(R[x])
    else:
        p=Path(x if x.startswith(('archives/','research/','tools/')) else BASE+x)
        r=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    if section:r['section']=section
    return r
def add(i,id,title,status,kind,statement,quantifiers,scope,objections,section=None,evidence=(),model=MODEL,assumptions=(),sources=()):
    b=ref(i,section)
    o=dict(object_id=id,version=1,title=title,kind=kind,truth_status=status,model=model,statement=statement,quantifiers=quantifiers,assumptions=list(assumptions),scope=scope,objections=objections,body=b,evidence=[ref(x) for x in evidence],sources=list(dict.fromkeys(src(b['path'])+list(sources))))
    O.append(o)
    row=M.setdefault(i,{**R[i],'disposition':'objects','object_ids':[],'reason':'本轮顺序实读成熟正文，核陈述、量词、状态和证据位置；复用成熟论证。'})
    row['object_ids'].append(id)
    return o
def ex(i,reason):
    M[i]={**R[i],'disposition':'excluded','object_ids':[],'reason':reason}
def use(i,ids,reason,disp='attachment'):
    row=M.setdefault(i,{**R[i],'disposition':disp,'object_ids':[],'reason':reason})
    row['object_ids']=list(dict.fromkeys(row['object_ids']+list(ids))); row['reason']+=' '+reason if row['reason']!=reason else ''
def cross(i,reason,ids):
    decisions.setdefault(i,[]).append(dict(reason=reason,owner_ids=ids))
def save():
    (DIR/'partial-batch.json').write_text(json.dumps(dict(schema=2,baseline=DEFINITION['baseline'],objects=O,materials=[M[i] for i in sorted(M)],edge_files=[]),ensure_ascii=False,indent=2)+'\n')
    (DIR/'partial-progress.json').write_text(json.dumps(dict(task_id=TASK,read_and_written_indices=sorted(M),cross_owner_notes=decisions,status='local-partial-not-ready'),ensure_ascii=False,indent=2)+'\n')

add(0,A[0],'全尾真实查询行的逐动作势移植与信用恒等式','proved','identity','令A=W−|O|+Ω，Ω=Σ_{x∈O}(1+b_x)⁻¹。固定原实际前缀，T_j强制后的同σ真实尾为Y_j；独立均匀j,l，逐槽移植Y_l并每步回到真实σ续局。各步真实IC损失均值G≥0、同叶删当前返还均值D有符号、末步返还为0。精确有R_i−(|O|−W)=A−EΛ+E C^rep+q(G−D)，其中Λ为冻结尾稀释损失，C^rep按原比较索引计重复。','每个有限实例和完整σ，每个实际位置，每个q≥1合法比较元组；r=1时逐步和为空。','真实逐动作移植与静态交叉尾只用于恒等式；D可有任意符号。','已有一般PATH与同叶删槽身份无需重立；这里的新复合合同是全尾真实查询行的预算等式。',evidence=[DEFM])
add(0,'customer-attraction/full-tail-real-query-row-cover-credit-and-multilevel-return-payment','全位置真实查询行及最低收益位置的返还付款','open','candidate','全ROW要求R_i(T)≥|∪T|−W，按ROW-ID等价qD+EΛ≤A+E C^rep+qG。较弱MIN-ROW要求存在一个最优m槽T及实际最小收益位置i使R_i(T)≥OPT_m−W；由真实IC有R_i≤m u_i≤W，故它足以half。','全ROW量化每份完整σ、每个实际位置与比较元组；MIN-ROW在每份完整σ内分别存在一个最优m槽和实际最小收益位置。','末两行已有证明；五人half另证，不反推任意早期行。','34客户负去相关及88客户四个最优槽全部负只否免费去相关，未击穿信用、ROW或half；剩共同支付有符号返还和尾稀释。',evidence=[0,1,2])
add(1,'customer-attraction/actual-three-tail-all-optimal-six-query-decorrelation-obstruction','88客户实际三人余局的全部最优六槽去相关严格为负','proved','counterexample','九主题88客户六人完整纯SPE实际(6,7,8,0,3,4)，W=86、OPT₆=88。实际前缀(6,7,8)恰余三人；全部四种最优六槽（置换无关）对均匀查询的D−Q分别为−11/72、−11/72、−1/9、−1/9，其中D是同σ各查询真尾收益平均，Q是独立交叉尾平均。','存在该固定原实例、完整σ和实际余三人前缀，使每个最优六槽元组均失败。','反驳存在一个均匀最优六槽可免费去相关；未否非均匀查询、真实ROW或half。','全部66,430决策节点按同一策略核实；原审查程序缺本地blob，完整证书为成熟正文记录的知情独立定义级重构。',evidence=[EV+'six-optimal-query-decorrelation-primary/new-independent-audit/outputs/actual-banks.policy.json',EV+'six-optimal-query-decorrelation-primary/new-independent-audit/outputs/independent-audit.payload.json',EV+'six-optimal-query-decorrelation-primary/new-independent-audit/independent_six_decorrelation.py',EV+'six-optimal-query-decorrelation-primary/missing-original-audits-boundary.json'])
add(2,'customer-attraction/penultimate-true-query-row-and-three-tail-signed-return-boundary','任意长元组的实际倒二真实查询行及两种余量','proved','theorem','令R=Σ_j U_b(T_j,D_j)，D_j为实际倒二强制T_j后同σ真实末回复，实际末两题A,B、尾利润V、新覆盖F_new，L_b=max_T t_b(T)。有R≥|O|−W+t_b(A)及R≥|O|−W+F_new/2+(V/2−L_b)。两个余量共享信用，只可取大不可相加。','每个m≥2原实例、每份完整σ、任意q≥1合法比较元组，均在实际倒二前缀。','q=m且T最优时若倒二为实际最小收益位置则half；不搬移该位置。','仅有一个真实后继的去相关，不能把该步骤推广为任意早期行。',section='任意长比较元组的倒二真实查询行',evidence=[(2,'单真实末回复的去相关'),(2,'全局旧覆盖与不重复支付的余量')])
add(2,A[1],'真实三人余局的双IC与有符号删中间返还恒等式','proved','identity','固定合法三人余局，同σ两查询A,A′分别真尾(B,C),(B′,C′)，交叉真末Ĉ=C(A,B′)。真均值减独立交叉均值Δ=Eℓ₁+Eℓ₂+E[U_b(C;A)−U_b(Ĉ;A)]。ℓ₁,ℓ₂是原(h,A),(h,A,B′)IC非负，最后项可为负。','任意合法三人余局和完整续局，任意目录分布p，独立同分布A,A′。','旧34客户完整策略取p=(10,10,21,10,10,21)/82给Δ=−11/82；88客户最优六槽是另一个更强反例。','不能把删中间后的静态核叫删人SPE；也不同于另有第三条IC的税上界。',section='三人余局为何多出有符号返还',evidence=[(2,'旧34客户完整见证及后续量词加强'),1])
add(3,'customer-attraction/five-actual-tail-potential-gap-common-payment-interface','五人实际尾势缺口与前三收益的无条件上界','proved','theorem','恰五人实际前三收益P=u₁+u₂+u₃，尾势缺口Γ=max_{T,R}Φ_q(T,R)−Φ_q(D,E)，q实际前三负载。由5d≥h+t_q(D)、Γ≤t_q(D)及Γ≤d/2、e≥h/4（h=OPT₅−W）得P+Γ≤(49W−13OPT₅)/36。','每份五人零背景原完整纯SPE。','若O>0、W=O/2并全链取等，则d=O/9,e=O/8,Γ=O/18,P=19O/72且D与其他四题不交。','这只给上界及必要取等条件。零福利仅在全目录零覆盖时发生，证明不除h。',evidence=[2,'引理/末两人重叠比较与任意索引聚合--引理.md','引理/分数覆盖的真实前缀利润预算--引理.md'])
add(3,A[2],'五人共同付款23/72最优覆盖的充分候选','open','candidate','候选P+Γ≥23OPT₅/72；若成立，与已证上界P+Γ≤(49W−13OPT₅)/36共同推出OPT₅≤2W。P=u₁+u₂+u₃，Γ只取实际前三负载的末两题势缺口。','对每个五人零背景实例及每份完整纯SPE。','ONE-GAP的3v₅版本更强；half已另证，不能反推PAY。','没有全局早期真实子树共同下界；两单点对3u₅的反例的P位置和阈值均不应代换。',evidence=[3])
add(4,'customer-attraction/two-singleton-terminal-potential-payment-counterexample','五人两单点完整SPE否定末三利润加尾势缺口支付三倍末位','proved','counterexample','五人两单点输入有完整31历史纯SPE，路径(0,1,1,1,0)，收益(1/2,1/3,1/3,1/3,1/2)，W=OPT₅=2。正文P定义为u₃+u₄+u₅，实际尾势已最大Γ₂=0；P+Γ₂−3u₅=−1/3。','存在指定两个单位客户、两单点主题、五人合法原输入及完整纯SPE。','只否该末三P和实际末位u₅的版本；该路径前三收益亦为7/6，但不同P定义不得互换为一般关系。','原规范策略与独立表在10个离轨动作不同，分别保完整核验；四主题另点不混作同策略。',evidence=[EV+'maxroot-gamma-shared-menu-primary/README.md'])
add(5,'customer-attraction/potential-maximizing-first-action-strict-selected-tail-credit-example','六客户五人完整SPE严格分离选择信用与势缺口','proved','counterexample','两不交主题大小5和1，规定第一次B出现后全A，尚无B则前四A第五B。完整纯SPE实际AAAAB，尾势已最大Γ=0，两个势最优首题按原真实末回复利润5/4和1，故K_sel=1/4=尾差集税>Γ。','存在该五人零背景固定输入与完整纯SPE。','只分离局部量K_sel、Γ；并未给ONE-GAP或MAXPAIR-CREDIT反例，也不是五人主证明的同名全局K。','选首题后末位必须真实回复，不将某个静态势最大对直接强制。',evidence=[EV+'tail-pair-and-import-integrity-resumed-boss3/new-verify_selected_credit_example.json'])
cross(5,'既有0069局部选择信用上界将该页用作Γ<K_sel的达界比较；该局部定理和固定全树分离见证为不同对象。',['customer-attraction/potential-maximizing-tail-real-reply-selected-credit-single-tax'])
add(6,'customer-attraction/five-provider-selected-maxpair-credit-early-payment-candidate','五人最大势末对选择信用的共同早期付款','open','candidate','设Γ为实际前三负载下的末对势缺口，δ*为所有可作静态最大势对首题T经原真实末回复后第四位收益最小值，K_sel=Γ+u₄−δ*。待证P+K_sel≥3v₅，P=u₁+u₂+u₃。由K_sel≤u₄/2且u₄,u₅≥v₅，若成立则W≥9v₅/2≥OPT₅/2。','每个恰五人零背景实例及每份完整纯SPE；以同一σ计算所有真实回复。','是比ONE-GAP弱的付款要求；六客户例只分离信用量，两个候选均成立。','早期三步改变真实子树与末两菜单，局部选择信用只收费一次，尚无共同跨树下界。',evidence=['引理/最大势末对真实回复的选择信用与单次尾税--引理.md',5])
add(7,'cag-two-player-anonymous-potential-static-security-and-cycle-boundary','两人匿名精确势博弈每份完整纯SPE逐人支付静态安全值','proved','theorem','有限匿名两人收益(A[a,b],A[b,a])有精确势当且仅当A[a,b]=h_a+K[a,b]且K对称。在任何完整纯SPE中，均匀抽真实末回复映射任一循环作不观察查询的静态背景，得v₂≤u₁；实际首动加末位BR给v₂≤u₂。','每个有限非空匿名两人精确势博弈、每份完整纯SPE。','允许负效用，不要求自拥挤或DR；固定背景CAG是特例。','静态安全对手不观察查询抽样；无势类反例独立。',section='精确势给出的两人正边界',model='有限两人匿名顺序博弈，公共动作集L，收益为任意实矩阵的A[a,b]与A[b,a]。')
add(7,A[3],'匿名自拥挤但无精确势时聚合静态安全值失败','proved','counterexample','对每个k≥5，循环动作矩阵在b=a或a+1收益0、其他1，真实末回复a+1得1，根全动作得0，故完整SPE的W=1而v₂=(k−2)/k。k=5另有全正、严格自拥挤、唯一末回复例W=12<2v₂=62/5，根仍平局。','每个整数k≥5存在第一构造；另有固定k=5正收益版本。','反驳无势更宽类中的静态安全支付，不是非负客户均分模型。','沿动作循环的反对称差和非零，排除精确势。',section='匿名、自拥挤仍不足：任意k≥5的无势循环',evidence=[(7,'全正效用与唯一末回复仍不能修复无势合同')],model='有限两人匿名顺序博弈，公共动作集和自拥挤A[a,a]≤A[a,b]，不要求精确势。')
add(8,'cag-two-step-security-chain-conditional-grouping-and-finite-search-boundary','合法背景两步静态安全链PAIR付款','open','candidate','令V=v_r(b)，V′=v_{r−2}(b+A+B)为真正整数静态安全值，真实首两动作A,B利润u₁,u₂。PAIR候选u₁+u₂+(r−2)V′−rV≥0恰为两个相邻链增量之和；若全域成立，结合末一/两人基例逐对归并给P_r(b)≥r v_r(b)。全兴趣客户的PAIR系数为0，去掉不改任一IC。','每个合法有序背景、r≥3剩余玩家、每份原完整续局。','非零背景P_r是剩余总利润；r=3为全剩余利润桥，非同一空根或θ。','逐步失败不否相邻和；有限浮点锥阴性及MILP超时非全称证明。根最小均衡收益失败另由四人精确例认证。',evidence=[7,'定理/真实路径安全值链的嵌入与债务恒等式--定理.md'])
add(9,'customer-attraction/four-player-minimum-root-SPE-payoff-payment-failure','四人完整SPE否定四倍全均衡最小根收益的总付款','proved','counterexample','14客户四主题四人原实例全部可实现有序SPE终局恰(1,3,0,0),(3,1,0,0)，收益同为(13/4,13/4,11/4,11/4)，故同实例全SPE最小根收益r_min=13/4，W=12<4r_min=13且OPT₄=14。','存在该原实例及完整纯SPE；根最小值量化同一实例所有完整纯SPE。','只否根最小收益复制；计数为两终局，非两策略。','成熟证据保存源JSON、集合值逆归纳和一份85历史全策略；不把旧扫描的源述数字单独当证书。',evidence=[EV+'root-minimum-payoff-primary/README.md'])
ex(10,'完整实读R642恢复入口、目录作用、旧64/38点、2396核验及各数学路由。恢复身份、旧命令与已有对象导航不另立数学身份；38坐标点排除的源述范围和对应已整理版本留正文，非新完整SPE或全型付款证书。')
add(11,A[4],'税敏感静态包络的覆盖比较与静态CCE付款','proved','theorem','h为m−1合法背景，f_h(T)=Σ_{x∈T}(1+b_x)⁻¹，τ=Σ b_x/(1+b_x)。E_mix=min_Q[m max_T E_Q f_h(T)+E_Q τ]，E_*=min_h[m BR(h)+τ(h)]，有OPT_m≤E_mix≤E_*≤(2m−1)θ_m。任意m人同时行动CCE μ，独立均匀删除玩家所得Q还给E_mix≤(2−1/m)EμW。','每个有限实例、m≥1；同一静态Q服务全部查询。CCE结论量化任意同实例静态CCE。','有限minimax形式成立；独立删除是静态构造，不代换指定顺序策略福利。','三人静态CCE福利不能普遍小于给定SPE；这不直接否包络付款。',section='同一分布服务全部查询的税包络',evidence=[(11,'静态CCE能支付什么')])
add(11,A[5],'任意真实末对节点和末回复循环的税包络上界','proved','theorem','固定任意有序长度m−2节点P，取同σ真实末回复β(a)的任一循环C。均匀C背景P+a给逐查询E f_{P+a}(T)≤u(P)，税增量均值D_C=E Σ_{x∈a}1/[(p_x+1)(p_x+2)]≤u(P)。因而E_mix≤m u(P)+τ(P)+D_C≤(m+1)u(P)+τ(P)。','每个m≥2原实例、每份完整纯SPE、每个合法有序P及其每个真实回复循环C。','实际与离轨P均可；上界作用于混合包络E_mix。','不把循环分布降为某个纯背景，不保证有预算≤2W。',section='任一真实末对节点给出的循环预算',evidence=[(11,'同一分布服务全部查询的税包络')])
add(11,'cag-tax-sensitive-static-envelope-and-terminal-reply-cycle-budgets','真实完整SPE的全局税包络付款','open','candidate','候选每份原完整纯SPE实际福利W能支付E_mix≤2W；较强纯背景包络E_*≤2W同样足以half。另一个充分方向是在真实末对节点P及其回复循环C中找到m u(P)+τ(P)+D_C≤2W。','每个有限共同目录实例、每份完整纯SPE；若走循环路线则在该策略中存在P,C。','有限纯包络浮点策略锥仅为源述探索，非普遍有理证书。','任意真实节点的解析上界和静态CCE支付都成立，但从互斥真实节点或其他均衡搬预算未证。',evidence=[11])
agg=json.loads((DIR/'aggregate-last-floor-owner.json').read_text()); O.append(agg); M[12]={**R[12],'disposition':'objects','object_ids':[agg['object_id']],'reason':'本轮全文实读本一般整数反族及跨批36客户反例，取共同旧Claim CA-AGGREGATE-LAST-FLOOR-NO；前者主正文，后者同一桥的另一个证书，具体赤字不同。'}
add(20,'B10-IID-SUPPORT-AVERAGE-NO-v1','两人真实支持平均不足三人静态iid收益且支持外枢轴修复','proved','counterexample','对任意偶k≥8，令M=3·binom(k,k/2)，每个k/2外围标签集有3名同时喜欢hub的客户，外围另各M/3私有客户。静态三人均匀外围q是对称iid Nash，λ=M(7/24+g/3)，g=1−1/k+1/(3k²)。真实两人强制根按q平均D=7M/12<λ，而根选支持外H得3M/4>λ；严格差M(3k²−24k+8)/(72k²)。','每个偶整数k≥8存在单位输入和给定完整两人纯SPE；λ对同目录指定静态三人q。另有单独262客户小例。','只否用指定q平均真实根偏离支付λ；不否实际根EI或half。','首动作后所有末位动作类别已覆盖；静态α_H、θ₂、真实根和全部均衡根最小值不互换。父审四例与子审八参数属成熟有限复用。',evidence=['程序/两人支持外枢轴的单位展开与静态三人核验--程序.md','程序/子集枢轴两人族的组合计数与逐客户有理审计--程序.md',('资源/额外iid两人子批的同源审计复用与静态反桥闭合--资源.md','成熟资产的同字节及成功事件复用'),(EV+'general-half-r75-entry-four-primary/original/CLAIMS.md','B10-IID-SUPPORT-AVERAGE-NO-v1')])
save()
