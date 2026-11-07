import json,pathlib,hashlib,re
R=pathlib.Path.cwd(); task=json.load(open('research/operations/p25-register-v2/tasks/register-ab98f323ad-0069.json'))['definition']; mats=task['materials']; OUT=pathlib.Path('research/registration/batches/register-ab98f323ad-0069.json'); REC=pathlib.Path('research/registration/receipts/register-ab98f323ad-0069.json'); home=pathlib.Path('research/workspaces/p25-register-v2/Boss2/0069')
new=dict(zip(['menu_efficiency','CM','PEEL_reset','beta_finite','missing_payment','disjoint_extension','coalition_end','coalition_cap','all_big_credit'],['M-d78294c3593a431a8d3d9824dac6ed8b','M-e7dce51dc7b049f998e9c6b1c516e850','M-f876c99a355747c1b1f47fcdad04752c','M-08f7fee93729484da264a7c696d884a0','M-58ef82731528424394935220507e6fc1','M-bb7fa19357034cdb89eb096c2a6c5a53','M-4acc7b279439494a9d9893eec095c24c','M-ea769a946ef944b1aae282bd49d1a8ec','M-46bca22511db490aa208dcd4a74a673e']))
(home/'allocated-ids.json').write_text(json.dumps(new,indent=2)+'\n')
def ref(p,section=None):
 p=str(p); z={'path':p,'sha256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()};
 if section:z['section']=section
 return z
def mr(i,section=None):return ref(mats[i]['path'],section)
model='有限单位客户、有限非空共同标签目录及任意覆盖映射、单位提供者按全部有序历史顺序各行动一次；终局客户价值在覆盖者间均分。保空主题、重复行动、同覆盖异标签、零客户和全部离轨平局。'
def source(i):
 t=pathlib.Path(mats[i]['path']).read_text(); a=re.findall(r'source:[^\s\]"\',]+',t); return list(dict.fromkeys(a)) or ['mature-state:'+mats[i]['path']]
def obj(oid,i,title,kind,truth,statement,quantifiers,assumptions,scope,objections,evidence=(),section=None,mod=model):
 e=[]
 for x in evidence:
  x=mr(x) if isinstance(x,int) else ref(x) if isinstance(x,str) else x
  if x not in e and x!=mr(i,section):e.append(x)
 if mod==model:
  d=task['context_plan']['shared_read_refs'][0]
  if d not in e:e.append(d)
 o=dict(object_id=oid,version=1,title=title,kind=kind,truth_status=truth,model=mod,statement=statement,quantifiers=quantifiers,assumptions=assumptions,scope=scope,objections=objections,body=mr(i,section),evidence=e,sources=source(i)); objects.append(o); return o
objects=[]
# Fixed-policy methods are explicit mathematical contracts, not universal negative claims.
net='customer-attraction/true-net-matching-seven-input-cone-catalog-and-quantifier-boundaries'
obj(net,1,'指定最优元组的真实净差匹配固定策略客户锥','method','definition','固定完整形式策略σ及指定最优m槽元组T，定义δ=OPT−W−maxπΣiV_i,Tπ(i)。对非负兴趣类型权w、完整真实IC Γw≥0、T覆盖不低于全部比较支持、W=1，枚举槽排列约束t≤(o_T−a−Σi v_i,Tπ(i))w，最大化t。精确非负整数点及完整IC才反“每个最优元组可付”，不能仅凭一指定T反“存在一个最优元组可付”。','任意给定有限合法全历史策略及指定最优比较元组；每个π∈S_m共同约束；现源码仅七输入66支持的有限历史探索。',['必须核完整合法动作域及最终有理重数非负','前缀六标签输入在源码被选中动作最大值缩为四标签权域'],'真实后继净差匹配的固定策略LP；不等同静态冻结匹配或half缺口','七输入649动作、66支持无正分离只是历史README；两个端点未过有理flag。源码有理flag漏重查非负，不提供精确阴性对偶；不同最优支持可使用不同w，不能拼成同实例排除全部最优元组。')
menu='customer-attraction/root-menu-tail-aggregate-security-and-terminal-BR-compression-obstruction'
obj(menu,3,'根菜单尾总安全加保留末位BR仍不足聚合安全','counterexample','proved','十单位客户、四主题S0=A∪B,S1=A,S2=D,S3=B∪C，块大小2,3,2,3。四枝(003),(103),(220),(330)根收益(2,1,3/2,2)，尾利润(5,6,13/2,5)，各≥2v2(1_a)，各末位真实全目录BR；选根0有W7<3v3=36/5。根0孩子倒二改2后末位3唯一BR，改者3>2，故此菜单不可能补为完整SPE。','存在上述一个共同客户表的压缩菜单；局部v2=(5/2,45/16,3,5/2)，v3=12/5由匹配查询/对偶证明。',['仅对四条保留枝要求末位BR，未要求各根后的完整子SPE'],'精确否定尾总安全+末位BR的压缩充分接口','不是完整SPE聚合安全反例；此游戏half余量4。不同排序尾可影响末位身份；H_I输出023是终局多重集，不能当真实路径023。',[2])
obj(new['menu_efficiency'],3,'十客户压缩障碍游戏的全部完整SPE反而全覆盖','lemma','proved','对同一十客户四主题游戏，区间剪枝H_I(∅)只保终局多重集{0,2,3}，而H_I包含全部完整SPE终局，故每份完整SPE福利均10=OPT3；根0的真实可实现顺序为032。','该一个固定输入的每份完整有序历史纯SPE；存在性由有限树BI。',['采用区间剪枝保SPE终局的已证定义；排序仅压缩终局计数'],'固定游戏的全SPE福利分类','这是合法客户游戏与不可信压缩菜单的区分，不推广为一般H_I付款或half定理。',[2,'archives/customer-attraction/state/定理/区间终局剪枝的上界比较与全效率目录类--定理.md'],section='H_I输出是多重集，不是有序路径023')
clone='customer-attraction/real-clone-gain-fixed-definition-audit-and-canonical-search-blind-spot'
obj(clone,5,'每可实现路径一份最低偏离收益证书遗漏真实克隆增益','obstruction','proved','ExactSPESolver的ordered_outcomes枚举可实现有序路径，certificate却在每个离轨孩子只选当前偏离者收益最低的可信子终局。五客户四人ABAA实例所需AA后AABB给旧A收益3/2；该选择器改选AA后3A1B给旧A收益1，因此遍历全部actual路径、各配一份该规范完整证书仍不枚举全部SPE并漏本点克隆增益。','指定冻结选择器的完整实现及该固定两不交主题3/2客户块实例；不声称它漏所有实例。',['单位同主题玩家在同一终局收益相等','完整历史并不强制选择最小偏离者续局'],'规范证书枚举的真实数学覆盖盲区','固定核15历史30含自身比较；2000次阴性为三人四标签有限随机域，四人追加无冻结输出。反例本体归五客户真实后继克隆主owner，不重建其身份。')
hard='customer-attraction/fixed-genuine-SPE-hard-deletion-not-continuous-zero-deficit-funded'
obj(hard,7,'同一真实SPE硬删除正信用无法由连续零亏空函数付款','obstruction','proved','固定13人六主题36单位客户完整DAG策略实际P^10,A,A,B，u=(5/2)^12,3。任意0<ε≤1/24取自由t=5/2+ε，各根收益<t且各根tail总≥12t。实际低尾恰位置1..11，硬删后根P收益25，释放Γ45/2而亏空向量δ=(ε^11,0)→0。任何固定有限K≥0的KΣδ、以及任何在0连续且φ(0)=0的纯δ函数均不能对全小ε上界Γ。','同一固定输入、人数、目录和完整σ；对每固定K或固定连续φ，存在任意小正ε使付款失败。',['t是自由阈值，不等同真正安全值或OPT内生门槛','φ仅以该亏空向量变化，其固定参数可依实例/人数'],'自由门槛下的硬删除亏空付款模板','真正守恒的是原被删者在P上的绝对份额45/2，总删利润55/2；删后P,B不再是两人SPE（B可改D得5>3）。原v13≤5/2，故不反内生安全值门槛；不反half/GAP-r。',[8,9])
gapcone='customer-attraction/fixed-complete-strategy-tail-gap-cone-attack-scope'
obj(gapcone,10,'固定完整策略与真实背景终局的GAP-r客户锥攻击','method','definition','固定全有序策略σ、合法旧背景b、真实终局c及剩r人，对指定实际使用主题a和任意r槽比较计数q最大化ΣS[f_S(q)−p_S−r u_S(a)]x_S；约束x≥0、Σx=1与整张σ的全部真实IC。正的合法整数点将否定F_r(b)−P≤r min余u；子状态按(b,c)去重而不只按b。','任意给定满足实现scope p≤7,m≤5的完整形式策略；余r≥3，所有允许比较计数和实际占用主题。',['动作键完整仍须另核动作标签合法、重数非负','偏离后沿同一σ真实后继'],'最小收益差额候选的固定策略锥发现接口','原prefix与fractional两个输入830/196是LP尝试非成功数，均witness null，仅有限浮点阴性。有理化核正gap与全部IC但未另断言最终weights非负；没有普遍阴性对偶或half结论。')
# The compact old page needs its original self-contained statements as evidence.
man=json.load(open('archives/customer-attraction/tools/evidence/R-059140e622784d85a4e3a4dd6554f506/source-manifest.json')); raw={x['id']:x['preserved_path'] for x in man}
obj(new['CM'],14,'空动作下最低可信首利的修正单调式仍失败','counterexample','proved','令Θr(b)为全部完整SPE当前收益最小值、L_r,b(A)为强制A后全部可信孩子当前收益最小值、F_b(A)=Σx∈A1/(b_x+1)。39单位客户五主题含空E的输入具有空背景Θ1..4=(24,33/2,19/2,65/6)。四人强制E有F=L=0而Θ4−Θ3=4/3>0，否定Θr(b)≤Θr−1(b+1_A)+F_b(A)−L_r,b(A)。','存在一个39客户固定目录、r4、b0、A空的严格反例；客户共同复制任意正整数倍保持严格失败。',['Θ与L均量化完整可信续局，非任意终局最小值'],'动态可信首利人数删除的辅助单调桥','不反POP、TB、SM或half；不是固定人数福利研究。39客户完整树由原精确集合值BI和真实IC证书定位，不拿780比较代替普遍证明。',[raw['d4afcb7e902a615d25bc'],raw['3687a4f6085bbcb21290'],raw['6ac7f74af07e3699c9a9']],section='1. 辅助动态可信首利候选被精确否定')
obj(new['PEEL_reset'],14,'三剩余重跑真实后继的PEEL重置恒等式及负重置项','lemma','proved','余三人强制枝(A,M_A,B_A)，交叉真实末回复C_A,T=σ_last(h,A,M_T)。原PEEL的非负末位信用L在重跑σ时精确相消：Δ=E[S+Q−L]+R，R=E[F_(b+A)(B_A)−F_(b+A)(C_A,T)]，故D−F=E[S+Q]+R，D−C=E[S+Q]+R+J。34客户完整SPE、安全最优p=(10,10,21,10,10,21)/82给R=−113/164，D−F=−11/82，否定R≥0的免费递归。','任意合法余三人节点及同一完整SPE、iid同目录p的恒等式；存在给定34客户精确负R见证。',['S与Q是改变中间动作后同一σ的真实中间IC和交叉末位BR','不得冻结原B_T充作交叉真实回复'],'末位剥离递归的精确重置付款缺口','节点PEEL本身合法；不许同时保旧EL又免费递归Δ。J正碰撞足够大，本例W32/OPT34不反Mfull、Mpath或half。',[raw['fad09689d31ab06094d4']],section='2. PEEL 恒等式可以成立，但递归必须支付重置项')
obj(new['beta_finite'],14,'六旧完整SPE的beta-packing固定探针有限记录','computation','finite','固定六个旧策略及有限owner/beta-packing比较，精确报告role/action/cap2最大值依次为(2/11,2/11,13/11)、(1,1,2)、(1,49/67,1696/1015)、(3/2,1,2)、(1,1,2)、(51221/76055,748568/1323357,14807/8323)。保原输入命名及完整报告，不作普遍packing上界。','仅冻结表的六个命名输入、程序指定的有限合法owner与最优元组。',['使用原完整策略真实后继；输入与程序按manifest绑定'],'有限精确诊断','computed不是theorem；有限极值不能证明全历史、全owner或所有可能付款机制，更不反half。',[raw['4964ee2c8fcb43af62a6'],raw['a702cb0a914b5f038b9b']],section='3. 旧完整 SPE 上的有限 beta-packing 探针')
b3a='B3-TAIL-MIN-NORMALIZATION-NO-v1'; b3b='B3-TAIL-MIN-RELOCATION-GAP-36-v1'; review='archives/customer-attraction/state/审查/末两最小收益归一化的拒绝候选与精确代价--审查.md'
obj(b3a,16,'福利低于nθn时所有最小收益者均不能正规化到末两位','obstruction','proved','θn=min合法(n−1)元组B maxAΣx∈A1/(1+c_B)。末两位逐人收益≥θn，故尾部含任何全局最小收益位置就有W≥nθn。若某完整SPE福利W0<nθn，则任意W≤W0的完整SPE，其全局最小收益的全部出现位置均严格早于末两位；任何整份策略更换把最小收益移尾，福利需增加至少nθn−W0>0。','每有限共同目录输入、n≥2、每份完整SPE；含最小收益平局，允许整份离轨策略改变。',['真实末两人保底定理','θn是纯min-max末位背景值，非混合安全值vn'],'福利不增末位/倒二最小收益正规化障碍','n2严格前提不可能，零覆盖不满足严格前提。重排同一终局保收益多重集却不保SPE；不否定允许付正福利的变换或half。',[17,review,'archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md'])
obj(b3b,16,'36客户最小收益尾部正规化的精确福利代价为二','counterexample','proved','三人六主题X={0,1,2},Y={3,4,5}，9跨组pair各一客户、9个两X两Y类型各三客户，共36。θ3=12、OPT36。全部完整SPE福利为34或36；低福利有跨组minority第一位收益(10,12,12)，同组全异收益(12,12,12)。minσW34，而尾部含全局最小者的minσW36，最小代价2、倍率18/17。','该固定36单位客户目录的全部完整有序历史纯SPE；48可实现有序终局中12含尾部最小。',['完整末位/倒二激励分类；两套完整策略实际034与012'],'固定输入的精确正规化成本','48是可实现有序终局数非48完整策略。34仍满足half，真正v3=10不同于θ3=12；不主张所有实例代价恒2。',[17,review,'archives/customer-attraction/state/计算/静态安全值与聚合保底的精确核验--计算.md'])
station='customer-attraction/arbitrary-shared-incidence-single-stationary-flow-obstruction'
obj(station,20,'任意中间共享类型的单一驻留流可有负净信用','obstruction','proved','0基路由矩阵n=[[0,0,0,1],[0,0,1,0],[0,0,0,1],[2,2,1,0]]每列和2、对角零，π=(2,1,2,4)/9满足nπ=2π。取共享类型J={1,2}，后继负载K=(0,0,1,1)，根减后继均值δ=(0,1,1/4,−1/2)，π·δ=−1/18。合法路由列和与驻留方程不足保证任意共享客户型逐型付款。','存在上述一个四路由、r3、背景0的代数投影；不量化所有可选流都失败。',['标签明确从0开始','未附完整客户目录、全树策略与全部IC'],'单驻留逐类型支付模板','不是完整SPE/half反例；不同于均匀流−1/8的另一矩阵；不否目标并集真实包络。',mod='共同目录单位客户路由机制的代数投影；非负整数路由列和r−1、驻留分布，未给完整SPE。')
relax='customer-attraction/comparator-multiplicity-single-root-108-row-obstruction'
obj(relax,22,'五人比较重数单根108必要行不蕴含half','obstruction','proved','九出现主题实际01234与根改4后的45678、客户九会员位b和比较五槽重数d0..5共3072原子，W=1,x≥0；正文明确9节点各11查询/覆盖行、四背景利润行、四末对行和一根IC共108行。16支持精确点满足全部行且O/W=1523853699890/669004065243>2，故该必要行系统不能推出O≤2W。','一个明确有理LP及一个精确非负可行点；对该108行的任何非负组合均不能给所述结论。',['O只是比较覆盖抽象账，未给逐标签比较目录实现','背景三/四人利润行只用于合法真实前缀的必要来源'],'固定五人压缩松弛的精确分离','没有证明此点来自完整SPE、O=真实OPT，亦无精确LP最优性；与460行双根松弛变量不同。不反当前五人half或六人目标。',['archives/customer-attraction/tools/evidence/root-branch-comparator-primary/exact-relaxation-witness.json'])
rep='customer-attraction/single-bonus-repeated-tail-incompatible-last-responses'
obj(rep,24,'单公共奖金尾复制模板在r≥2末位比较互斥','obstruction','proved','块Xi,Pi,Z,E两两不交，大小c>0,a,b,d≥0，共同目录Ci=Xi,Ai=Xi∪Pi,Bi=Xi∪Z,D=Z∪E。要求同一完整SPE实际C1..Ck D^r且强制Ai后其余主玩家保持Cj、末r人全Bi。两条真实末位BR分别强制d≥rc/2和d≤c/(r+1)，合得r(r+1)≤2，整数r≥2不可能；r1仅允许d=c/2。','任k≥1,r≥1及上述非负整数单位客户块；给定同一完整策略两条路径要求。',['偏离枝仍保留完整目录D与Ai，末位可真改行动'],'指定公共奖金重复尾路径模板','两末位必要条件已足以排r≥2；r1必要条件不自动充分构成SPE。不排其它森林、多惩罚者或后继覆盖新客户机制。',[25])
obj(new['missing_payment'],24,'实际遗漏客户可由各一次无后继竞争偏离支付的充分half条件','lemma','conditional','若最优比较遗漏客户可分割为组Pi，每个玩家至多一组；玩家i有一个合法真实偏离Ti覆盖Pi，且按同一σ偏离后其它后继仍不覆盖Pi，则偏离者独得|Pi|，真实IC给|Pi|≤ui。相加遗漏≤W，故OPT≤2W。','任完整SPE；存在满足上述同一最优遗漏客户分割及逐玩家一次偏离的条件下成立。',['Pi实际完全遗漏，过去也不覆盖','每位玩家只领一组，不复用整主题IC','未来不覆盖Pi是额外待核假设，未证一般成立'],'遗漏客户保持私有的明确充分支付','不能用于后继改为覆盖遗漏新客户的情形。模板Ai私有Pi未被Bi覆盖只给a≤c，不构造一般六人付款。')
obj(new['disjoint_extension'],24,'保留原实际路径的不交新主题扩展须同时受末两人收益限制','lemma','proved','向任一完整SPE目录加与全部旧主题不交的F、|F|=v，并假设扩展后仍有保留同一实际路径的完整SPE。末位可改F给v≤u_m；倒二首次改F后末位改旧S_m至少得u_m而复制F仅v/2，v>0时末位不复制，故倒二独得v≤u_(m−1)。v0直接成立。','任m≥2及任意非负整数v，在明确路径保留SPE扩展存在条件下的必要结论。',['加入F后完整策略须重新合法且保留实际路径','F与所有旧客户覆盖不交'],'新不交主题的末两位必要支付','不宣称任意不交扩展自动保SPE；更早偏离可同时改变多个后继，不能从此推出全部玩家收益≥v。')
eps='customer-attraction/five-provider-positive-residual-improvement'
obj(eps,28,'五人完整有理证书的严格因子改进','corollary','proved','令ε=1788637526774492965820/(120·10^22)=89431876338724648291/60000000000000000000000>0。五人主证书全部非零实际会员位的余项至少ε，未覆盖位非负，故Σρ≥εW；由2W−O=非负真实IC组合+Σρ+2264870·10^−22 K得OPT5≤(2−ε)W。','恰五人每有限单位客户/有限非空共同目录/每份完整有序历史纯SPE；零背景根福利。',['同五人原53整数权、同完整类型域有理证书，不作再优化','其31项覆盖位最小余项中最小者在实际位00001'],'五人福利定理的精确定量严格改进','覆盖率≈0.5003729107356346仅OPT>0时定义；零OPT用乘法式。不认证锐性或六人/全人数。',['archives/customer-attraction/state/定理/五人半覆盖--定理.md'])
sel='customer-attraction/potential-maximizing-tail-real-reply-selected-credit-single-tax'
obj(sel,32,'最大势首题真实末回复的选择信用共用单次尾税','lemma','proved','固定合法前缀后真实末两人(D,E)利润d,e，Pq(T,S)=fq(T)+fq(S)−gq(T,S)，M=maxP，Γ=M−Pq(D,E)。每个可作最大势首题T的原真实回复QT仍满足Pq(T,QT)=M，δT=Uq(T,QT)静态最佳，εT=d−δT≥0，且Γ+εT=fq(QT)−fq(E)≤τ≤d/2。取δ*=minTδT、ε*=d−δ*、Ksel=Γ+ε*，得Γ≤Ksel≤τ，d/2+Γ≤δ*≤d；五人三槽合法前缀另有δ*≥v5。','任合法整数前缀恰余两人及任完整纯SPE；对全部最大势首题共同成立，原末位平局保持不另选。',['τ=Σx∈D且x不在E1/((qx+1)(qx+2))','P为势增量，非两人利润和'],'同一真实末二节点的精确信用与界','Ksel按最小真实首题利润选，不能任取T；不可给多个早角色复制同一税。严格例Γ0而Ksel=τ1/4。早期全局付款仍open。',['archives/customer-attraction/state/引理/固定两尾势缺口的三项真实比较--引理.md','archives/customer-attraction/state/反例/势最优首题选择的严格尾部信用--反例.md'])
delprobe='customer-attraction/actual-terminal-deletion-support-random-policy-cone-probe'
obj(delprobe,33,'实际终局删位支持的固定策略固定查询客户锥','method','definition','固定四人六标签全有序σ与一个查询p，Bi为actual删第i位置的静态三槽背景，dσ,p(w)=mini Epf_w(a,Bi+a)。63非空兴趣类型质量和t非负、总质量1、1554完整真实IC及4条t≤g_i；最小化W−(7/2)t。22固定p为六纯、十五均匀二点、六题均匀。删除支持对手受限，maxp dσ,p≥真正v4，故精确正违反只否该支持加强。','每一给定完整策略、22固定查询及非负质量锥；原随机100轮每轮仅一份规范σ，实际受控复放仅首轮。',['改变当前行动后沿同一σ后继','最终有理候选必须重核完整IC、非负重数与精确目标'],'删除受限静态值的固定策略发现接口','一次首轮22LP无正点、原seed60客户完整IC及全矩阵有理核已保存；浮点近−1/12无精确阴性对偶。源码有理化只打印minGamma不assert，未重算严格目标；不是真正安全值反例。')
obj(new['coalition_end'],34,'同分支新保留组旧损失加退款的精确端点包络','lemma','proved','整数0≤p≤c≤m、c≥1、a≥1、p+a≤d0≤d≤m，B(d0)=p(1/c−1/d0)_++a(1/d0−1/d)。固定p,c,a,d，在全部允许整数d0上的最大值恰max{B(p+a),B(d)}。d0≤c段非增；d0≥c段为p/c+(a−p)/d0−a/d，最多先减后增，故两端达最大。','全部上述整数负载，含p0和单点区间；a是新组实际覆盖本客户人数。',['旧损失与退款来自同一客户同一分支','实际c≥1，a≥1保证删除后分母正'],'不需SPE的同分支负载代数','不能跨分支拼旧损失和退款，删后元组不需也不保证SPE；原单人三候选公式不能不改用于联盟。',mod='一个客户的实际负载c、保留旧前缀负载p、新保留覆盖组a及删前/删后负载；仅整数包含关系，无SPE理性假设。')
obj(new['coalition_cap'],34,'新保留组同分支信用的全整数锐容量','lemma','proved','对固定m≥2、1≤a<m，在0≤p≤c≤m、c≥1、p+a≤d0≤d≤m全域，B=p(1/c−1/d0)_++a(1/d0−1/d)的最大值为C_m,a=2a/(a+1)−a/m；p=c=1,d0=a+1,d=m达到。a=m时约束迫p0、d0=d=m，B恒0。C>1 iff m>a(a+1)/(a−1)，首次m7，a3达15/14；m=(a+1)^2时C→2。','任全部合法整数负载参数；锐性仅为负载合同，非SPE可实现性。',['B为同一分支同客旧正损失加新组绝对退款','实际c≥1；a=m边界单独处理'],'同分支联盟信用的精确全域容量','一客户目录{空,{x}}的标量取等模式不构成SPE（实际空行动者可获正份额）。不否half/全部联盟机制；真实全树访问总权与整主题共同IC仍须另付。',mod='同一客户整数负载合同，与END相同；不假设存在实现取等的完整SPE。')
obj(new['all_big_credit'],36,'恒大主题完整SPE族的最优菜单L与Q同时为零','lemma','proved','任m≥1，目录为不交大题B大小m及m−1个单客户小题。全部有序历史恒选B是完整SPE：当前大题最终利润≥1，真改小题至多1。actual B^m有W=m,u_i1，OPT=2m−1，最优元组每主题一次；每实际位置最优主题真实与冻结查询均1，故静态信用L_i=有符号适应差Q_i=0、R_i=m，SHARP?=ΣL−ΣQ恰0。','任整数m≥1的明确单位客户族、上述一份完整全历史策略；未枚举该族全部策略。',['信用L与Q使用同一覆盖最优索引元组和actual前缀定义'],'真实最优菜单sharp接口的解析紧性校准','只显示若一般SHARP?成立则该接口的2−1/m系数不能再改善；未证明所有目录SHARP?。原程序只核m5，任m由正文解析证明；不同于同族UV失败。',[37,'archives/customer-attraction/state/引理/最优主题菜单的非负静态信用与带符号自适应恒等式--引理.md'])
newton='customer-attraction/three-remaining-truncated-price-rational-newton-certificate'
obj(newton,43,'三剩余截断价格固定七行的全整数背景有理Newton证书','proof','proved','对正文定义的七R_j与ρ=tα+1[p+s>0]−min(1,d)−κα−λ·R，取(t,κ,λ)=(3/2,43/46,(0,0,20/23,0,6/23,21/23,0))或(2,262/411,(8/411,32/411,91/137,61/822,122/411,532/411,16/411))。32个Boolean会员型、五(d,ell)角点的ρ(0)和清分母N(p)=ρ(p)(p+1)(p+2)(p+3)从p1起四个Newton系数均非负，故所有整数p≥0有ρ≥0；双仿射及缺角单调覆盖[0,t]^2。','两组明确有理参数；全部32 Boolean型、整数p≥0及d,ell∈[0,t]；任非负客户重数可线性相加。',['仅正文固定R_j及ρ的模板定义；t≥1','p0独立处理，零分子取0'],'固定截断价格代数行合同的精确证明','未证七行来自同一真实SPE分支、d/ell合法同源、或共同客户钱包，故不推出half。113/822元数据未被原脚本推为任一组价格常数。普通τ2七λ另给κ0弱结论；16160行p≤100和浮点模板/有限锥阴性仅附件合同，不扩大本全p证明。',['archives/customer-attraction/state/审查/三价模板与均匀质量证书的范围审查--审查.md','archives/customer-attraction/state/审查/三价模板搜索与均匀质量证书增量--审查.md','archives/customer-attraction/state/程序/R486终局价格锥与均匀三二对偶--程序.md'],mod='32个Boolean变量(a,b,c,q,r)、整数背景p≥0、矩形实参数d,ell及固定七个有理行的代数模板；不假设这些行已来自完整SPE。')
# Persist mathematical draft immediately. External supports are completed below after owner coordination.
assign={}
for o in objects:
 for i,m in enumerate(mats):
  if m['path'] in {x['path'] for x in [o['body']]+o['evidence']}:assign.setdefault(i,[]).append(o['object_id'])
external={
0:['customer-attraction/finite-layer-anonymous-potential-cardinality-concavification'],
4:['SECURITY-OPT-REAL-TAIL-GAP-v1','M-2ffd990fe18940feb8056569ce61043e'],
6:['customer-attraction/optimal-slot-parameter-kernels-and-anchored-harmonic-budget'],
12:['customer-attraction/whole-profit-copy2-failure-and-prefix-request-cap2-quantifiers','M-ddd87cdc712c4ac68ec926984d718726'],
13:['customer-attraction/eight-client-uniform-optimal-topic-permutation-budget-failure','customer-attraction/single-role-dynamic-loss-same-client-credit-and-unpaid-shares','customer-attraction/deepest-low-threshold-node-per-successor-query-external-profit','M-57cc29d007474699abddc1bc2a9ab543'],
15:['CA-ROOT-TAX-NO','CA-AGGREGATE-DECORRELATION-NO','CA-ONPATH-DECOUPLED-BUDGET-NO','CA-SECURITY-CONE-DUAL'],
17:['customer-attraction/maximum-mass-partition-and-orbit-overlap-all-real-price-certificate'],
18:['customer-attraction/legal-background-first-step-coverage-counterexample','M-21108b01d92540379cb7c7227ec6ade3'],
19:['CA-COLLISION-FREE-LOAD-PAYMENT-NO'],
21:['CA-FOUR-UPPER-1499-750'],
26:['B9-OPT-RANDOM-SLOT-EXCHANGE-v1'],
29:['FIVE-THIRD-FLOOR-ROOT-v1','FIVE-MAX-FOUR-TAIL-v1','FIVE-MAX-DIRECT-v1'],
30:['FIVE-THIRD-FLOOR-ROOT-v1','FIVE-MAX-FOUR-TAIL-v1','FIVE-MAX-DIRECT-v1','FIVE-SHARED-K-EXACT-v1'],
31:['customer-attraction/five-player-common-maximum-theme-variable-copy-rigidity-and-capacity-rows','M-2a5c4d23c3a84486971f84ceb3f801ec'],
35:['customer-attraction/whole-row-scalar-finance-and-coordinate-cover-unbounded-separation','customer-attraction/free-complete-menu-source-mismatch-and-conditional-reciprocal-debt'],
36:['customer-attraction/optimal-menu-static-credit-signed-adaptivity','M-a0d36df1c03e426d8e824eaca526ab1c'],
37:['customer-attraction/actual-prefix-full-cover-credit-sharp-coefficient-and-old-player-return','M-11bb8909e92245d0a861fb03a5814e30','N5-PREFIX-PAID-INTERFACES-v1'],
38:['customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'],39:['customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'],40:['customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'],41:['customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'],
42:['M-a0ff64e390d547858476ea79c9403d12','M-06f6b8ff456c4de59eb0add2cb939067','M-f55fd1a56f574bcbac6960e92f693c59']}
# Pending route names are explicit, never silently guessed as accepted owner records.
pending={0:'银行逐人门槛及四层DR支持Shapley合同尚需各主owner接收；不把无输出LP当结果。',5:'五客户克隆真反例主owner接证；此页独有规范选择器盲区本批独立。',9:'伪孩子摘要及任意预定末深的主owner接证；低尾实际证据已归本批hard对象。',11:'全future ALL/ROW、OWN初始化、最大系数退款、EG反族等主owner接证；共同不同action整行系数未付。',12:'末层锐二倍族与静态CCE两个主owner接证；COPY2/PCAP精确合同主owner已定位。',15:'共享预算定义主owner接证；89/36/61和全策略锥分对象，程序不替普遍定理。',18:'0009已确认精确ID customer-attraction/legal-background-first-step-coverage-counterexample并承诺实读接证；主记录尚未发布，不能视为已接。本页三搜索只作其必要证据。',19:'78客户与十一客户调和势失败的统一主owner接证，分别54/75/141/2和8/11/21/2，不混输入。',25:'森林逐人θ/UTP候选主owner接80/240/9072有限报告；不升级有限阴性。',27:'381客户无slack强聚合的同一精确被否辅助命题主owner接独立证据。',35:'自由完整菜单主owner接FQ实现/八客户正逐客债，勿把正逐客债当整体失败。',37:'全尾ROW主owner接九fixture有限原审计；N5身份待确认与该原审计确实共同。',42:'自洽三门槛及弱总行同一余额交已发布主owner；无新共同付款。'}
# Override accepted external owner IDs only through explicit parent-supplied decisions.
fix=home/'owner-decisions.json'
if fix.exists():
 f=json.loads(fix.read_text())
 for k,v in f.get('external',{}).items():external[int(k)]=v
 for k in f.get('resolved_material_indices',[]):pending.pop(int(k),None)
# A route closes only when exact bytes are in a currently canonical owner.
canonical=json.loads(pathlib.Path('research/registry.json').read_text())
canonical_objects={o['object_id']:o for o in canonical['objects']}
accepted={}; owner_audit=[]
for i,ids in external.items():
 for oid in ids:
  o=canonical_objects.get(oid)
  linked=bool(o and any(x['path']==mats[i]['path'] and x['sha256']==mats[i]['sha256'] for x in [o['body']]+o['evidence']))
  owner_audit.append({'material_index':i,'object_id':oid,'canonical_present':bool(o),'exact_material_ref_present':linked})
  if linked:accepted.setdefault(i,[]).append(oid)
  else:pending.setdefault(i,'主owner已定位但本材料精确path/SHA未出现在当前canonical主record中；保留接证请求。')
owner_tasks={0:['register-ab98f323ad-0002','register-ab98f323ad-0021'],5:['register-ab98f323ad-0006'],9:['register-ab98f323ad-0007'],11:['register-ab98f323ad-0003'],12:['register-ab98f323ad-0003','register-ab98f323ad-0020'],15:['register-ab98f323ad-0001-5-evidence','register-ab98f323ad-0010','register-ab98f323ad-0012'],18:['register-ab98f323ad-0009'],19:['register-ab98f323ad-0007','register-ab98f323ad-0010'],25:['register-ab98f323ad-0004'],27:['register-ab98f323ad-0005'],35:['register-ab98f323ad-0005','register-ab98f323ad-0017'],37:['register-ab98f323ad-0017','register-ab98f323ad-0026']}
owner_body_requests={15:[{'object_id':'CA-AGGREGATE-DECORRELATION-NO','body':ref('archives/customer-attraction/state/反例/四人总去相关的单根负差--反例.md'),'owner_task':'register-ab98f323ad-0001-5-evidence'}, {'object_id':'CA-ONPATH-DECOUPLED-BUDGET-NO','body':ref('archives/customer-attraction/state/反例/三人全分布补偿预算--反例.md'),'owner_task':'register-ab98f323ad-0001-5-evidence'}],18:[{'object_id':'customer-attraction/legal-background-first-step-coverage-counterexample','owner_task':'register-ab98f323ad-0009','acceptance':'worker确认精确ID并承诺实读合入，未发布'}],35:[{'object_id':'customer-attraction/free-complete-menu-source-mismatch-and-conditional-reciprocal-debt','owner_task':'register-ab98f323ad-0005'}]}
rows=[]
for i,m in enumerate(mats):
 ids=list(dict.fromkeys(assign.get(i,[])+accepted.get(i,[])))
 bodyids={o['object_id'] for o in objects if o['body']['path']==m['path']}
 canonical_body=any(canonical_objects[oid]['body']['path']==m['path'] for oid in accepted.get(i,[]))
 disp='objects' if bodyids or canonical_body else 'attachment' if ids else 'needs-decision'
 why='本批连续全文实读，核模型/量词/状态与完整正文及必要证据入口；复用成熟证明，未重清洗/重跑数学程序或建边。'
 if i==23:disp='excluded';ids=[];why='完整实读。此页明确自称阶段一问题身份/目录脚手架，实际精确模型与当前六人原题由完整模型及six-providers问题承担；无独有数学陈述或证明，不凭旧脚手架造重复问题节点。'
 if i in pending:why+=' 待主owner精确接证（本行只列实际闭合owner）：'+pending[i]
 rows.append(dict(m,disposition=disp,object_ids=ids,reason=why))
batch=dict(schema=2,objects=objects,materials=rows,edge_files=[]);OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
req=[]
for i in sorted(set(external)|set(pending)):
 req.append({'material_index':i,'material':mats[i],'requested_owners':external.get(i,[]),'accepted_canonical_owners':accepted.get(i,[]),'owner_tasks':owner_tasks.get(i,[]),'owner_body_requests':owner_body_requests.get(i,[]),'required_action':'由主body批次作者核数学后将本材料ref合入主record.evidence；0069只反向路由，不另写略异同ID。','status':'closed' if i not in pending else 'pending','scope':pending.get(i,'当前canonical主body已精确接入本材料。')})
requests_file=home/'attachment-requests.json'
requests_file.write_text(json.dumps({'task_id':task['task_id'],'canonical_registry_ref':ref('research/registry.json'),'requests':req,'unresolved_routing':pending,'owner_audit':owner_audit},ensure_ascii=False,indent=2)+'\n')
receipt={'batch_file':ref(OUT),'assets':[ref(OUT)],'allocated_object_ids':new,'summary':{'objects':len(objects),'materials':len(rows),'all_44_materials_read':True,'shared_definitions_read':2,'mathematical_program_runs':0,'edges':0,'dispositions':{k:sum(x['disposition']==k for x in rows) for k in ['objects','attachment','excluded','needs-decision']},'remaining_material_indices':sorted(pending)},'reading':{'read_materials':mats,'read_shared_refs':task['context_plan']['shared_read_refs'],'additional_body_reads':[ref(review),ref('archives/customer-attraction/state/审查/三价模板与均匀质量证书的范围审查--审查.md'),ref('archives/customer-attraction/state/审查/三价模板搜索与均匀质量证书增量--审查.md'),ref('archives/customer-attraction/state/程序/R486终局价格锥与均匀三二对偶--程序.md')]+[ref(raw[k]) for k in ['d4afcb7e902a615d25bc','fad09689d31ab06094d4','2683aba9b2c115693606']],'raw_evidence_read_status':'正文成熟证明与必要原件定向实读；额外程序/大表只核path/SHA及成熟合同，不声称本次重跑或逐字重读全附件。','context_plan_not_runtime_measurement':task['context_plan']},'routing_pending':pending,'attachment_requests':ref(requests_file),'canonical_registry_ref':ref('research/registry.json'),'validation':{'status':'recoverable draft; exact owner evidence closure pending; not done'}}
import sys
sys.path.insert(0,str(R/'tools'))
import registration
validation=registration.validate_batch(R,batch,task['materials'],task['baseline'])
receipt['validation']['schema_and_ref_check']=validation
REC.parent.mkdir(exist_ok=True);REC.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'objects':len(objects),'materials':len(rows),'dispositions':receipt['summary']['dispositions'],'pending_materials':sorted(pending),'validation':validation},ensure_ascii=False))
