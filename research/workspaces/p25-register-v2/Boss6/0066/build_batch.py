import json, hashlib, re, os
from pathlib import Path
import sys
sys.path.insert(0,str(Path.cwd()/'tools'))
from registration import validate_batch
ROOT=Path.cwd(); W=Path('research/workspaces/p25-register-v2/Boss6/0066'); T='register-ab98f323ad-0066'
D=json.loads(Path('research/operations/p25-register-v2/tasks/'+T+'.json').read_text())['definition']; MS=D['materials']; texts=[Path(m['path']).read_text() for m in MS]
ids=json.loads((W/'new-ids.json').read_text())['object_ids']; extra=['M-77ae6cb0994145feafae34f1345c05d6','M-942e12ff254c45b68d3d732c1d45e68e']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p):return {'path':str(p),'sha256':sha(p)}
def sr(i):return {k:MS[i][k] for k in ['path','sha256']}
def front(i,key):
 m=re.search(r'(?m)^'+key+r':\s*[\"\']?([^\n\"\']+)',texts[i]);return m.group(1).strip() if m else None
def linked_evidence(i):
 out=[]
 for dest in re.findall(r'\]\(([^\n]+?)\)',texts[i]):
  dest=dest.strip('<>').split('#')[0]
  if '://' in dest:continue
  p=Path(os.path.normpath(str(Path(MS[i]['path']).parent/dest)))
  if p.is_file() and '/tools/evidence/' in str(p):out.append(ref(p))
 return out
MODEL='有限不同单位客户、有限非空共同带标签目录及覆盖映射、单位权提供者；按固定顺序观察全部有序历史各选一次，终局客户价值在全部覆盖者间均分。保空覆盖、同覆盖异标签、重复行动、零客户与任意离轨弱平局；真实偏离后沿同一完整纯策略在改变后的历史续完。根W为全部实际覆盖，非零背景剩余利润另计。'
O=[]; own={i:[] for i in range(len(MS))}
def add(i,title,statement,quantifiers,assumptions=(),truth='proved',kind='theorem',oid=None,scope=None,objections=None,ev=()):
 oid=oid or front(i,'id'); assert oid
 refs=[D['context_plan']['shared_read_refs'][0]]+linked_evidence(i)
 for e in ev:
  refs.append(sr(e) if isinstance(e,int) else ref(e))
 seen=set();refs=[r for r in refs if r['path']!=MS[i]['path'] and not (r['path'] in seen or seen.add(r['path']))]
 source=[MS[i]['path']]+re.findall(r'(?m)^\s*-\s*[\"\']?((?:source:|clean:)[^\n\"\']+)',texts[i])
 o={'object_id':oid,'version':1,'title':title,'kind':kind,'truth_status':truth,'model':MODEL,'statement':statement,'quantifiers':quantifiers,'assumptions':list(assumptions),'scope':scope or title,'objections':objections or '本次fresh重新实读成熟正文的陈述、条件、量词及完整论证/证据定位，复用成熟证明；未重清洗、重跑原程序或建超边。数学开放义务与身份/来源待接证分别记录。','body':sr(i),'evidence':refs,'sources':list(dict.fromkeys(source))}
 O.append(o);own[i].append(oid);return o
add(1,'最优终局冻结匹配的ALL诊断与37条有限保存记录','定义f_i(T;z)=Σ_T[1+c_x(z)−1_(x∈S_i)]^−1，Q_all=max_最优可重复m元组T min_π Σ_i f_i(T_π(i);z)，Q_exists则把外max换min。原两入口均算Q_all，17份固定完整策略与20个命名输入331终局/27665比较对均无正Q_all−W；当前仅独立枚17保存矩阵的372排列并核算术。计数压缩对冻结成本合法，不能把策略改成计数策略。','对全部合法静态终局及最优元组定义量词成立；有限阴性仅指定37条输入记录。',truth='finite',kind='method',scope='固定策略验证/全部可实现终局两入口的不同合同及保存银行；不证明普遍匹配。',objections='强式Q_exists≤W已有52/1953客户反例且五人有W25/Q51/2反例。本页finite银行不恢复其OPEN；源码max不能冒作存在式min。未重新验证17份SPE或枚20输入终局。')
add(1,'存在最优元组的弱冻结匹配half充分预算','开放预算为每个完整纯SPE终局存在最优可重复m元组T，使min_πΣ_i f_i(T_π(i);z)≤(1+1/m)W。逐客户给任意T/π成本≥OPT−(1−1/m)W，因此该存在式若成立即推出OPT≤2W。','∀有限单位输入、m≥1、每份完整纯SPE，∃最优T及排列；不是每个T都成立。',truth='open',kind='candidate',oid=ids[0],objections='现有一单位强冻结反例不足否定本较弱阈值；五人half已证也不能反推本预算。完整充分代数在正文；一般存在义务未解。')
add(2,'五人一税ONEGAP的同背景充分预算','在同一完整五人SPE的实际前三步背景q上，U123=u1+u2+u3，Γ2为同背景两主题补全最大调和势减实际尾势；开放ONEGAP为U123+Γ2≥3v5。结合0≤Γ2≤u4/2、u4/u5≥v5可得W≥9v5/2，再由OPT5≤9v5得half。','∀五人合法输入及完整σ的实际前三步，量均绑定同一背景/策略；v5为四整数竞争者的真正隐藏查询安全值。',truth='open',kind='candidate',oid=ids[1],ev=['archives/customer-attraction/state/引理/固定两尾势缺口的三项真实比较--引理.md','archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md'],objections='本预算未由五人half反推，也未由有限命名审计证明。跨背景Γ2和不同策略付款不可相加。')
add(2,'五人十题一税命名审计的440兼容前缀有限记录','原five_individual_security输入v5=2262/139；124个根SPE终局计数与120前三步计数形成440兼容对，各查55个两主题尾。最小保存ONEGAP余量1779/1390>0，路径(3,7,8,5,6)，W84/U123501/10/Γ2=0。原11111历史99999非自身IC仅是旧重建元数据；未保存此正点完整策略。','仅指定命名输入全部原兼容对的历史记录；当前保有理字段算术与证书域检查。',truth='finite',kind='finite-observation',scope='有限一税回归；不宣称当前重跑BI、715安全比较或完整IC。')
add(2,'五经济四银行保险族的全历史控制器与一税正余量','五经济块各a客户、四银行块各b客户，20个笛卡尔主题；正整数b≥3a/2时BASE/PUNISH/EXIT控制器在全部有序历史给完整SPE。actual经济00001、银行01230；W=2a+4b，U123=3a/4+5b/2，真正v5=3a/5+b/2，Γ2=3a/4。因此ONEGAP余量b−3a/10≥6a/5>0，且U123−5v5/2≥9a/8。','∀正整数a,b满足b≥3a/2，存在正文指定完整策略；不量化该目录全部SPE或其它控制器。',assumptions=['目录恰全部经济×银行主题，块两两不交','每次偏离按同一状态控制器的真实孩子完成'],oid=ids[2],kind='construction',ev=['archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md'])
add(4,'私有四客户填充族的全历史4收益下界','14客核心AD2/AE2/B3/T3/BDE2/TDE2，加k个互不交四私客主题，m=k+2。任一合法非终端有序历史的任一完整纯子SPE，当前最终利润≥4；故根W≥4m。OPT_m=4m+2，全部客户并集4m+6。','∀整数k≥0，∀合法历史，∀其每份完整纯SPE当前玩家。',kind='lemma',objections='人数归纳在真实偏离孩子施用；该floor不证明指定P0…Pk−1,A,B路径对每个k可实现，k4的有限完整证书另归六人CQ owner。')
add(6,'任意非负实背景的两人共同静态查询最小利润预算','恰两人、客户背景b_x≥0，q_b(U,V)=Σ_U[1+b_x+1_(x∈V)]^−1。任一完整纯SPE实际A,B、a=q(A,B)、d=q(B,A)、R=a+d，对每个合法T有q(T,A)+q(T,B)≤R+min(a,d)。P1逐客户与P2逐客户代数结合第一位真实T孩子及实际末位BR即给2a+d、a+2d两界。','∀有限客户/共同目录，∀实背景b≥0，∀完整二人子SPE，∀合法查询T；允许A=B、空题及零收益。',kind='lemma',objections='非零背景R不等于完整覆盖；一般人数CQ桥已由六人例否定。587B旧审计160项/后来80+40回归是有限证据，普遍实背景由正文证明；本次未新运行。',ev=[5])
add(7,'共享索引残余族的静态CQ缺口与合法安全值上界','对m≥2，r=m−1，目录Ai/Di/Ei及B,T共3m−1标签，4m+6单位客户如正文。静态终局A1…Ar,B有W=4m+1、早期收益4/末5、F(T)=5m；m≥6时F(T)>W+4。合法查询前背景D1…Dr给各查询Ai3、Di1+4/m、Ei2+4/m、B/T3+2/m，故v_m≤3+2/m且W−mv_m≥m−1。实际αc背景另有G=(4m+1)m/(2m−1)、max g=5。','∀整数m≥2的上述明确静态输入/终局；没有任何指定路径的SPE存在量词。',kind='static-construction',ev=[5],objections='m6此为17标签30客，不是9标签CQ完整SPE；九标签DAG及私块floor均不认证此族路径。纯静态上界不声称精确v。旧fractional全人数OPEN已由十三人反例纠正。')
add(8,'最优客户一次归属收费的弱存在付款义务','对最优索引元组及实际槽匹配，把每个最优客户仅向一个覆盖它的比较索引归属，冻结分母c_x+1−1_(x∈a_j)，得总一次收费R。逐客户OPT≤R+(1−1/m)W；开放义务是在每份完整SPE中存在合法选择R≤(1+1/m)W，从而half。更强R≤W只在无环真实替换等附加条件下有证明。','∀合法m人完整σ，∃最优元组、槽匹配和一次客户归属；不是所有匹配都便宜。',truth='open',kind='candidate',ev=['archives/customer-attraction/state/引理/最早归属客户的无环真实替换付款--引理.md'],objections='无环见证普遍存在性失败不自动否所有更宽一次收费；共同F(T)、whole-theme Q与R不同。文件中其它已证/已否历史内容待各主owner接证，不在本条重授。')
add(9,'五人1100必要行的超过二投影原声明及缺失质量证书','原十标签incidence稿声明W1、O=1029888020062/463330867145>2、K=O/5，并通过50 floors+400 AP+250真正加权最大BNS-C+400 v2交换。若其非负质量点确可行则该必要行锥不能推出2W≥O；但本地缺group_mass的2471B JSON和4690B审计，成熟页仅保存原分数/行数/最小slack，未独立重构。','指定五人十标签必要系统的单个原有理点声明；逻辑障碍以点可行性为前提，不宣称任一完整SPE。',truth='unassessed',kind='projection-obstruction',objections='欠完整质量表与精确审计，不能把原声明升级proved可行点、精确最优或真实half反例；旧root/v2的成熟交换证明是另对象。')
add(10,'固定43节点策略的IC/稀释/回路非负证书编译方法','三人六标签固定σ：根0、次位按首题X/Y选3/0、末位取第二题组内未见最小标签。126独立非负收益坐标，258形式真IC+2520锋利同题稀释非负行、45PAIR+60SIX零等式；先LP恢复有理primal/dual再逐坐标认证，后固定β选L1较小分解，成立证书βr−o=Iᵀμ+Cᵀθ+s，μ/s≥0而θ可有符号。','仅同一固定σ及比较124；每次有限恢复必须精确通过所有行，程序不保证任意浮点点可恢复。',kind='method',ev=[11],objections='“非负流”不限制零等式乘子符号；第二LP非最少支持且无精确成本最优性。两页共享原main一次；本登记不重复运行。')
add(11,'固定策略比较124收益松弛的精确8/5与原点不可正实现','上述126坐标、2778非负行和105零身份、R=1的抽象LP精确max O=8/5。有理原始点和12IC+10稀释非负乘子、18PAIR+10SIX有符号乘子给126坐标无余项身份8R/5−O=μI+θC。故任何真实客户且同σ为SPE时|T1∪T2∪T4|≤8W/5；原达到点C12=C14=8/9、C1=32/45、C124=8/5，次模余项−8/15，严格排除非负共同客户实现。','指定三人六标签固定完整σ和比较124的全部抽象可行收益表；真实推论另要求同σ为SPE。',kind='exact-certificate',ev=[10],objections='抽象sharpness不是真实客户最优常数，O非自动OPT；与另一同值8/5系统不假定可行集或primal相同。R0由齐次证书涵盖。')
add(12,'四份安全值搜索报告的124保存记录与版本边界','四原报告含124条含best/重复记录、60不同输入，分别n4k5/n4k6/n5k6/cyclic_n5k6。n4k6保存全主题客户正数、n4k5保存PNE点，与现生成器置全主题0/仅nonPNE入bank不相容，故不绑定当前main版本。除n4k5与循环静态重构外，minSPE/最差计数及LP值保原有限记录，未授完整策略或精确鞍点。','只指定四冻结报告的保存输入与字段；不量化未存试次或任意SPE。',truth='finite',kind='finite-observation',objections='报seed/试数不能补原argv、版本或完整IC；浮点微负非反例。具体静态零和C6精确值另有本页独立对象。')
add(12,'n4k5十四输入的纯安全鞍点与微负精确归零','原best及13种bank输入取C=T3。任意三竞争背景纯C查询≥|C|/4，纯3C背景下全部五query≤|C|/4，因此v4=|C|/4；所存4C叶W−4v4=0且静态PNE。best值109/4，全部bank129/4，微负原gap为浮点。','仅正文完整列出的14个不同整数输入；对每个输入全部三竞争背景/五query给匹配证书。',oid=ids[3],kind='exact-finite-certificate',objections='静态鞍点/PNE不认证缺失完整SPE、最坏SPE资格或DP完备性。')
add(12,'C6循环三十输入的均匀安全值与稠密f族公式','对C6不变六标签输入，均匀query与最小背景群平均给v5=(1/360)min_|h|4 Σ_BwB|B|60/(1+h(B))。正文30整数点的126背景、全部最小背景及正缺口精确核同。各只缺一题的六类型每类f时v5=7f/6，所列五互异叶W6f、W−5v5=f/6；f17得119/6、17/6。','30明确循环输入的有限静态证书；公式中的f族∀正整数f，全部126背景。',oid=ids[4],kind='exact-static-certificate',objections='不认证worst列表的SPE资格/完备性；六位循环class不能当双三块二元class种子。')
add(13,'双四块四十整数输入的11背景轨道精确静态值','n5/k8、群(S4×S4)⋊C2，非零六轨道(a,b,c,d,e,f)=(04,14,23,24,33,34)每具体类型共同重数，N=2a+8b+48c+12d+16e+8f。全部330四竞争计数分11轨道，v5=(1/480)min_ℓ Cℓ·(a,b,c,d,e,f)，正文列完整系数。30bank+10initial共40输入的原V和全部最小背景被精确匹配；best N172/v4043/120/差85/24。','仅这40保存整数输入；11轨道解析公式适用于上述非负轨道输入域。',kind='exact-finite-certificate',objections='原全SPE最低福利、G/策略、LP最优未获该静态核认证；10initial均不等当前30bank。十锥稠密点另列独立身份。')
add(13,'八标签各缺一题稠密归一点的真正v5=63/320','八客户类型j各只不喜欢题j、质量1/8，五互异主题叶W1。均匀查询对四竞争计数h给7/64 Σ_j(5−h_j)^−1，严格凸离散平衡在四1四0取min，故v5=63/320、W−5v5=1/64；乘8为单位客户W8/v63/40/差1/8。','固定八类型归一形状及全部四竞争背景；正同倍缩放按齐次性。',oid=ids[5],kind='static-value',objections='原十锥0.125为精确有限小数但同值不证明原G/完整SPE或LP最优；相对差为1/63，不是绝对差1/64。')
add(14,'双三块三十放大点与十锥记录的有限范围','n4/k6、群(S3×S3)⋊C2。30bank都是六个各缺一题类型的同一形状整数放大；10initial有9个加03/13类且不在bank。保存原SPE/rows/states/HiGHS消息，仅静态值由五轨道解析核对。输出0.16666666666666666不是原字节恰1/6；当前单一正形状W归一另得精确点。','固定两报告30bank与10initial/锥；不授30000未保存试次或原完整策略。',truth='finite',kind='finite-observation',objections='原1/6十进制不能原样当精确可行证书；解析归一和原LP认证必须分开。')
add(14,'双三块三轨道客户的安全值公式与精确W归一','六题分3+3，非零03/13/23轨道每具体类型重数a,b,f≥0且f>0，N=2a+6b+6f。三整数竞争背景共56个、五群轨道，真正v4=(30a+100b+105f)/72；a=b0时最小背景全部20个三互异。每类各缺一题质量1/6的W1归一点，v4=35/144、W−4v4=1/36；乘6回单位客户W6/v35/24/差1/6。','∀上述非负参数且f>0，全部三竞争背景；归一仅单一正23形状。',oid=ids[6],kind='static-value',objections='群对称化不限制动态策略；所列终局覆盖N不认证SPE可实现或结果集完备。')
add(15,'四个自由分数漂移保存输入的纯主题匹配值与零债','n3k5的best/bank和n4k6的best/bank共四不同整数输入，所记终局全部选a（分别1/4）。令Cj=|Aj|、Ij=|Aj∩Aa|、Gj=Cj−Ij+Ij/n。四表max Gj=Ca/n，纯q=e_a给根t_n(0)和child t_(n−1)(1a)同上界，任意q查询a给同下界。故两值精确等于52/3、26、191/4、213/4，u=Ca/n，局部D=u+(n−1)t_child−nt_root=0。','仅四个原整数输入/指定叶；匹配上下界对整个自由q单纯形成立。',kind='exact-finite-certificate',ev=['archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md'],objections='42保存记录只有四输入，bank每份20重复；浮点微负均有精确零解释。不认证缺失完整SPE或一般局部债/聚合。')
add(16,'实际路径逐节点真实回复的联合静态菜单与固定策略锥合同','由集合值R(q)携目标j的DAG选择完整σ，沿actual每位置i强制b取同σ真实叶ν(d_b)，删当前一槽得h_i(b)=ν(d_b)−e_b并联合去重为M。z_M=max_p min_h∈M E_pF_h≥真正v_n；path-only另为所有实际标签支持的背景，二者不同。固定DAG全节点IC锥Gw≥0、actual覆盖cw1后交替优化w/p只作有限双线性发现。独立有理审计29记录、八G共6950行/437850系数核同；八归一末点v5=zM1/5、W1，n4best v4=zM215/4、W215。','程序合同一般合法n/k且无整数溢出；有限认证仅14不同保存整数输入及八固定末点。',kind='method',objections='负restricted差仅否额外菜单限制，不能因zM≥v倒推真桥或half失败；原数值state不等精确鞍点，本登记复用成熟独立审计。')
add(17,'实际末两主题D/R正负缺口分解及可检查half充分条件','m≥2、t=m−2，actual尾A,B，p早期负载/c最终负载，s=min(uA,uB)，α,β≥0/α+β=t。D=Σ(α1A+β1B−p)+/c，R为反正部，精确P=αuA+βuB+R−D、W≥ms−D。完整SPE给s≥θ(h)≥θ_m≥v_m≥OPT/(2m−1)，故若存在D≤s/2则W≥OPT/2。带R/尾超额判据精确等价W≥(m−1/2)θ(h)，参数相消不提供一般付款。','恒等式∀合法m槽叶；充分条件∀完整纯SPE且∃满足固定总权的参数。',kind='conditional-theorem',truth='conditional',ev=[18,19,20,'archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md','archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md'],objections='原H审查没有审新D预算；small-D不是普遍必要性质，反族另给。θ纯minmax与v混合maxmin不互换，m2/空题/零客户正文处理完整。')
add(17,'末两正缺口存在参数的m−1整数候选精确有限化','令β=t−α、α∈[0,t]。D为连续凸分段仿射：交集常项Σ_(A∩B)(t−p)/(p+2)，差集分别(α−p)+/(p+1)、(t−α−p)+/(p+1)。全部折点整数，故min_实α D=min_k=0…t D(k,t−k)，一般只需m−1参数，六人五个。','∀任意合法m槽终局，m≥2；包括t0、A=B、空差集及同覆盖不同标签。',oid=ids[7],kind='algorithm',ev=[19,20],objections='只检测一个给定终局的small-D条件；不枚全部SPE、不证明一般支付或half。')
add(18,'真实末两主题逐客户负载继承的条件福利界','m≥2、t=m−2，同一actual早期负载p、尾A,B。若∃α,β≥0，总权t且∀x p_x≥α1_A+β1_B，则P≥αuA+βuB、W≥mθ(h)≥mv_m，mOPT_m≤(2m−1)W。H等价A∩B上p=t且差集最小负载LA+LB≥t（空差集取t）。四客户四人85节点路径C,D,A,B给αβ1、WOPT4，早期不包含任何尾主题，证严格扩类。','∀共同目录m≥2及每份完整σ满足H的真实终局；不声称H普遍。',truth='conditional',kind='conditional-theorem',oid='CA-TERMINAL-PAIR-LOAD-SECURITY-v1',ev=[17,19,'archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md','archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md'],objections='未截断max(α+β)可超过t甚至空题无界，不能当一般进度界；本命题总权固定t。余项优化在零参数最宽，不补一般早期利润。')
add(20,'共同核加私客的完整SPE族及small-D普遍强化反证','每m≥3/K≥0，m题Tj=K共同客户+各自一私客；每个有序历史选未见最小标签给完整SPE。actual全不同，每人s=θ(h)=K/m+1，WOPT=K+m；所有α+β=m−2均D=R=m−2且H不成立。K≥m(2m−5)恰满足small-D，六人K42给48客/H外等号；K0对所有参数D=m−2>s/2，否定“每份SPE可选small-D参数”，D/s随m无界。','∀整数m≥3/K≥0存在指定完整σ；D/R结论对全部合法参数。',kind='counterexample-family',ev=[17,19],objections='族始终满覆盖，不是half反例。新共同核族是成熟正文解析补充，非旧85节点程序/审查的实验结论。')
add(21,'同型不交卫星52保存输入的完整轨道有限认证与可行价格值','当前精确轨道函数对8人3核心8卫星12输入、9人2核心9卫星40输入重算全部根轨道/最坏W/OPT并匹配。最大OPT/W分别401/341、157/97，均<2；八人12保存z的Fraction目标核同，最大2431/3220仅可行下界。另288+36有名集合比较及零客户并类控制核同；旧36独审缺w/g，不能重放。','仅两报告52明确输入及324明确小/混前缀测试；不量化所有八九人目录。',truth='finite',kind='finite-certificate',ev=['archives/customer-attraction/state/算法/对称不交卫星块的完整SPE结果轨道递推--算法.md'],objections='报告参数字段与现main不绑定，当前仅函数级复算；无价格精确上界/对偶，不能把12值<1当B(v)/W最优<1。')
add(22,'均匀通用时间的固定计数/完整历史策略锥交替探针','完整m行动叶Z_i(A)后额外查询价G_p(z)=Σp_TΣ_T1/(1+c_x(z))，ψ_i=min_A G_p(Z_i(A))。两程序固定λ寻找Σλ_iψ_i−W/m>0，在一个计数selector或三个给定有序历史σ的全IC客户锥上交替LP优化p/w。原两报告records[]，仅有限浮点阴性；均匀λ对应Σψ_i≤W，跨全部实例存在另一共同λ是更弱不同量词。','每次固定σ/λ的程序合同；有限报告不证任意σ、w、p或通用λ。',truth='finite',kind='method',objections='额外查询使用完整叶1+c，不是删当前m−1替换价。未执行新LP/BI；均匀开放预算主owner须另接本程序证据。')
add(23,'26978十四类型点与R373d族的二人矩等价及三人分离','原14兴趣型26978客六题点全部大小/两两交集矩阵，与R373d(d,g)=(1995,13)在正文重标后相同；二人全部36有序叶72利润、21覆盖及任意同标签完整σ的IC相同。原reply B/D/D/E/D/E给完整7节点SPE，W13000/唯一TS最优14004/遗漏13978/R−W978。三人固定B,D,E叶选B收益本点15008/3、旧12型16990/3，差1982/3，阻止高人数外推。','仅该26978整数输入与指定R373d族成员的全部两人统计/策略；三人只比较一个定义叶，不授SPE。',kind='equivalence',objections='此为二人矩接口等价，不是逐客户同构或新R373反例身份；71客2175B载体另待已有主owner接受完整回复版本。无MILP最小性/全局最优结论。')
add(25,'三人16客户严格唯一SPE否定末位最低福利平均选择器','三人四题16单位客户，完整21节点全部63非自身IC严格、最小1/6，故唯一完整纯SPE路径(1,2,1)、收益(11/2,5,11/2)、WOPT16。末位11/2>W/3=16/3，严格否定“存在最低福利SPE使末利≤平均”选择器。另49客户大证书指定SPE W45/OPT49/收益91/6,44/3,91/6，但all_spe_terminal_counts唯一仅旧声明。','∃此16客户输入，唯一完整纯SPE对全部21历史成立；大证书不独立认证所有策略终局。',oid=ids[9],kind='counterexample',objections='唯一性由严格逐历史比较承担；固定策略MILP最优非遍历全部σ最优。两例half余量均正，不当六人反例。')
add(25,'最小实际收益支付的全人数开放桥与有限策略锥搜索','待证桥为OPT_m≤W+(m−1)min_i u_i（每份完整纯SPE）。原固定策略浮点LP搜索m3/k4与k5各1000试，425/813不同σ均未获候选，best gaps约8.33e−17/1.33e−15；当前20-trial smoke19策略只检链路。','开放合同∀m与全部完整SPE；记录仅两有限固定σ银行，不是全称阴性或精确零。',truth='open',kind='candidate',oid=extra[1],objections='没有一般证书或真实反例；last-average选择器失败不否定该min收益桥。')
add(27,'q≥3的只依会员计数无余项单BR核模板不可能','固定h≥0/r>0/q≥3，只看源会员次数d的核F要求全部形式会员模式及a→R替换满足ΔF≥(η−α)/(h+1+rβ)。第三源命中/pivot不命中两向逼F2−F1=1/(h+1)；pivot命中/第三源不命中又逼1/(h+r+1)，矛盾。原K_L替换余项为B−Σ_(β0,e1)r(η−α)/((h+1)(h+r+1))，B是真末BR非负。','对全部形式会员模式、同一真实BR行系数恰1、余项逐类型非负这一严格模板；不是某个真实SPE总和付款。',kind='obstruction',objections='q2第一模式不存在、r0分母相同，不被排除；允许身份核/跨客信用/其它行系数已换合同。最优槽联合交换只控制C外新覆盖，不支付C内重复租金。')
add(27,'身份敏感固定pivot核的真实单步上升与精确切换债','定义S_L^b=f_H(b)+Σ_(a槽≠b)U_a(H+b^r+a)。固定b将非pivot槽替真实末回复R(b)时ΔS=B≥0；完成q−1次后L*={b,R,…,R}，切pivot到R的损失恰(q−2)Σ_(x∈R\b)r/((h_x+1)(h_x+r+1))≥0。q2债0；固定pivot单步上升不能免费跨pivot望远镜。','任意合法背景H、r>0、q≥2源多重列表及同σ真实末回复；clone显示叶代数不冒原σ真叶。',oid=extra[0],kind='identity',objections='源/实际收益/跨客信用能否付切换债另开放；不宣称一般half障碍。')
add(29,'四客户无平局完整SPE否定省略旧玩家利润的非根中继','二人主题A={1,2,3}、C={4}，根A、两末节点均A；三个非自身比较严格差1/2,1/2,5/2，完整纯SPE。历史(A)末位强制C令AA→AC，ΔW1、Δtail0，故旧R1 ΔW≤Δtail失败；ΔB3/2、当前损失g1/2准确支付。actualW3/OPT4仍half。','指定4单位客户/2题/全部3有序节点完整σ；不存在借平局选择。',oid=ids[10],kind='counterexample',objections='旧三客户含平局例另属既有中继owner，不替换其客户/审计身份；原1519B代码没有冻结运行报告，本次未运行。')
add(29,'固定过去背景的fresh覆盖与active股份精确中继分解','任意合法h/i，U为旧覆盖并集、b旧负载、k(T)从当前起active终负载。F(T)=|{x∉U:kx>0}|、G(T)=Σ_(x∈U)kx/(bx+kx)，则W=|U|+F、旧玩家总B=|U|−G、active总P=F+G=d+V。固定同σ，规定与真强制T两枝当前损失g≥0，故ΔF=ΔV−ΔG−g。','∀完整σ/合法h/合法T；代数分解∀叶，SPE只用于g≥0。',oid=ids[11],kind='identity',objections='ΔG不可无条件删符号或跨互斥子树相加；不产生共同全局望远镜预算。C1/R2一般主owner另待接证。')
add(30,'联合后继容器负载保底的调和预算不具人数无关常数','极大主题路由前缀p、剩r，J1取无同题后继容器计数最坏分母，J2递归给每份完整SPE当前收益≥F(p,r)。N=(m+1)k、目录全部k子集、k≥max(2,m−1)时OPT_m=mk而任意前缀F=(k+1)/r(r≥2)、F(p,1)=k；路径保底预算B=(k+1)H_m−1，m5/k6给899/60<15。k=m−1时OPT/B~m/logm无界。该目录真实所有根SPE却W=mk。','∀m≥2/k≥max(2,m−1)，所列目录全部合法前缀/完整σ；失败是J1/J2充分预算，不是SPE福利。',oid='CA-R0F997-JOINT-COPY-FLOOR-OBSTRUCTION-20261030',kind='obstruction',objections='J1达到的近复制尾不可信：末位有fresh k题严格改进；保联合q仍遗漏真实最佳性。解析无界不由有限样本支持。')
add(32,'三客户完整SPE路径无法裸删一人继承为较短SPE','A={a},B={a,b},C={b,c}，正文13节点完整三人σ路径(C,A,C)、每人1/WOPT3。两人同目录末位唯一BR分别A→C、B→C、C→B，故全部根SPE叶仅(B,C),(C,B)。删原路径任一位仅(A,C),(C,C),(C,A)，均非两人SPE。否定任意完整SPE总可删一位不改其它终局而继承SPE。','∃该3单位客户输入/指定完整三人σ；对三种删位全否，对所有两人完整SPE叶列尽。',oid=ids[8],kind='counterexample',objections='不是人数福利单调性反例，二/三人福利都3；不排重新求较短SPE、信用状态或真实后继修复。其它对称储备/调和两既有工具只作跨owner来源。')
add(34,'一次最多耗d份fresh储备时的容量余量保护','在对所有合法后继封闭的节点域，有两两不交指定储备，d≥1/H>0；每行动至多触d份fresh，任碰已触储备行动的全即时收益严格<H；每fresh r有合法专用D_r只碰r，若后继不碰r则本次最终≥H。若剩n、fresh数q≥d(n−1)+1，则每份完整纯SPE全部未来利润≥H且无人触自己行动前已触储备。人数归纳在真偏离D_r孩子及真规定孩子分别闭合。','∀上述状态域/每节点条件和每份完整σ，不任选有利续局。',truth='conditional',kind='conditional-theorem',objections='只给至少H；另需全行动即时≤H才给恰H。储备重叠、容量不足、没有专用题、旧储备不严格低H时不适用。与d1纯块旧引理不同，专用行动可含块外核心收益。')
add(35,'共核心均匀外围目录的已有hub后全部fresh外围定理','真实r≥2、偶k≥r，M=3 C(k,k/2)核心每半标签类型3客，外围P_a含其M/2核心+专有M/3私客。hub含全部核心和额外R_h（与所有外围客户不交，hub额外可互相交）。设a_r=(1−2^(−r−1))/(r+1)、e_r(k)=E[1/(1+Bin(r,1/k))]；若每hub δ_h≤M e_r(k)/3−M a_r，则任意含≥1次hub且过去外围互异的前缀后，每份完整子SPE所有后继均选未见外围。','∀上述r/k/有限hub目录与全部所列合法有序前缀、每份完整历史纯SPE。静态比较另用r+1人，不与真实r互换。',truth='conditional',kind='conditional-theorem',ev=[34],objections='先以储备H=M/3+M/(2r)排旧外围而允许未来hub，再用两条真孩子和超几何差分d_j<a_r排hub。不证明首hub前外围互异或根λ付款；不解一般非均匀储备/half。')
add(36,'非均匀独立储备末个C子局的239输入精确有限诊断','k3/t2/m5，Random751103生成400次参数并末位必要过滤，239合格输入的末个C前缀集合值LCM60逆归纳均目标C-then-D终局计数不可达。冻结best x3/a2、(b0,d0)=(6,0)、(b1,d1)=(9,2)，680计数状态、R_size5、强制A2最低利润7/2>x3，gap1/2；独立32单位客户有序树2955节点核同一best。','仅原400生成/239合格试次（非去重全域）及一个best独立有序树；负计数足排指定顺序，阳性需另补路径及早期IC。',truth='finite',kind='finite-certificate',ev=[33,34],objections='m是5不是6；报告不存全部239输入/策略，all-k/t非均匀候选未证。q计数缓存集合值允许同计数有序子树不同续局，不强制Markov。')
# Exact primary files whose mature pages use a package directory or inline names.
# Byte fingerprinting locates the frozen evidence; it does not claim a new run.
primary={
 22:[
  'archives/customer-attraction/tools/evidence/separated-omission-uniform-time-and-bank-programs-primary/source-manifest.json',
  'archives/customer-attraction/tools/evidence/separated-omission-uniform-time-and-bank-programs-primary/original/8b7335fa56176ee5d393/cone_time_attack.py',
  'archives/customer-attraction/tools/evidence/separated-omission-uniform-time-and-bank-programs-primary/original/0d315a91d3edfbbd15d6/cone_time_attack.json',
  'archives/customer-attraction/tools/evidence/separated-omission-uniform-time-and-bank-programs-primary/original/0f8e97d2d465930431b3/targeted_history_cone.py',
  'archives/customer-attraction/tools/evidence/separated-omission-uniform-time-and-bank-programs-primary/original/3973e0c3633e87d10cf1/targeted_history_cone.json'],
 23:[
  'archives/customer-attraction/tools/evidence/unique-residual-discovery-four-primary/actual-source-manifest.json',
  'archives/customer-attraction/tools/evidence/unique-residual-discovery-four-primary/primary-original/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/residual_unique_bridge_lp.json',
  'archives/customer-attraction/tools/evidence/unique-residual-discovery-four-primary/primary-original/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/residual_unique_certificate.json']}
for i, paths in primary.items():
 for o in O:
  if o['object_id'] in own[i]:
   for p in paths:
    if ref(p) not in o['evidence']:o['evidence'].append(ref(p))
p25='archives/customer-attraction/tools/evidence/R-3b6b-potential-exchange-20261031/'
for o in O:
 if o['object_id'] not in [ids[9],extra[1]]:continue
 common=['source-manifest.json','run-manifest.json','validation.json']
 exact=['source/last_average_selection_small_certificate.json','source/last_average_selection_certificate.json','source/audit_last_average_selection.py','source/last_average_selection_independent_audit.json','replay/audit_last_average_selection.json','replay/verify_potential.py','replay/verify_potential.stdout']
 search=['source/min_payoff_lp_search.py','source/min_payoff_lp_discovery.json','source/min_payoff_k5_m3_discovery.json','replay/min_payoff_smoke.json']
 for p in common+(exact if o['object_id']==ids[9] else search):o['evidence'].append(ref(p25+p))
# Evidence-only task materials belonging to local primary objects.
for i, owners in {3:[4,7,9],5:[4,6,7],19:[17,18,20],32:[34]}.items():
 for j in owners:
  for o in O:
   if o['object_id'] in own[j] and sr(i) not in o['evidence']:o['evidence'].append(sr(i))
# Only source-to-owner routes. Never duplicate external main records.
registry=json.loads(Path('research/registry.json').read_text()); canonical={o['object_id']:o for o in registry['objects']}
route_doc=json.loads((W/'owner-routes.json').read_text()); routes=route_doc['routes']
for x in routes:
 x['status']='needs-decision-owner-evidence-not-attached'
 x['observed_on_current_registry']=x['object_id'] in canonical
 if x['object_id'] in canonical:
  x['owner_body']=canonical[x['object_id']]['body']
  if any(r['path']==x['material']['path'] and r['sha256']==x['material']['sha256'] for r in [canonical[x['object_id']]['body']]+canonical[x['object_id']]['evidence']):x['status']='accepted-in-current-registry'
def route(i,oid,body,reason,section=None,task=None):
 if any(x['material']['path']==MS[i]['path'] and x['object_id']==oid for x in routes):return
 req=sr(i);req.update({'section':section} if section else {})
 routes.append({'material':sr(i),'object_id':oid,'owner_body':ref(body),'requested_evidence':req,'section':section,'status':'needs-decision-owner-evidence-not-attached','reason':reason,**({'owner_task':task} if task else {})})
CQ='customer-attraction/six-player-thirty-client-common-query-minimum-payoff-counterexample'; CQBODY='archives/customer-attraction/state/反例/六人共同静态查询最小收益桥的三十客户反例--反例.md'
for i in [5,7]:route(i,CQ,CQBODY,'同九标签30客/W25/OPT26/F30完整SPE的旧审计/新重构来源；须接旧新DAG身份差和strict/tie不倒填；不重复主反例。',task='register-ab98f323ad-0001-5-evidence')
route(23,'customer-attraction/global-proof-residual-two-integer-witnesses-and-full-reply-versions','archives/customer-attraction/state/资源/残余桥两份整数见证的目标与完整回复版本--资源.md','2175B是71单位客户/7历史/reply B,D,D,E,D,E的完整载体；0030本身needs-decision指0003/0006，待lead给真正已发布主Claim并接证；不得当该container已发布数学ID。',section='2175B包是已证71输入的完整载体',task='register-ab98f323ad-0003 / register-ab98f323ad-0006')
route(8,'M-f16deb0259e8412fa8ff45ec81b43e49',canonical['M-f16deb0259e8412fa8ff45ec81b43e49']['body']['path'],'历史无环条件正确/见证普遍存在性失败及较弱一次收费量词边界的来源；主owner须保对应历史状态。')
# External 32/33/37/31/24/26 are intentionally needs-decision until their owner has attached exact bytes.
materials=[]
attachment_local={3:[4,7,9],5:[4,6,7],19:[17,18,20]}
for i,m in enumerate(MS):
 local=list(own[i])
 for j in attachment_local.get(i,[]):local+=own[j]
 local=list(dict.fromkeys(local))
 pending=[x for x in routes if x['material']['path']==m['path'] and x['status']!='accepted-in-current-registry']
 if own[i]:disp='objects'
 elif local and not pending:disp='attachment'
 else:disp='needs-decision'
 reason='fresh本次连续实读成熟正式正文全文（含模型、精确量词/条件、解析论证、表格、来源和纠错），复用成熟证明；原大JSON/代码/程序输出仅按正式正文定位，不冒作本次原字节全文审查或重跑。'
 if local:reason+=' 本批实际数学owner：'+','.join(local)+'。'
 if pending:reason+=' 未闭跨owner证据：'+'；'.join(x['object_id']+'：'+x['reason'] for x in pending)+'。精确路由见receipt.owner_routes；尚未接证不称已完成来源归一。'
 materials.append(dict(m,disposition=disp,object_ids=local,reason=reason))
record={'schema':2,'objects':O,'materials':materials,'edge_files':[]}
p=Path('research/registration/batches/'+T+'.json');p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
route_doc.update(registry_checked_sha256=sha('research/registry.json'),routes=routes,note='fresh本次重新读38正式正文/2共享定义。所有未接证路由保needs-decision；仅读当前canonical与本地已发布batch，不操作Git/远端claim/done。混合页有本批body需disposition objects，待接部分在reason/objections/本路由单列。')
(W/'owner-routes.json').write_text(json.dumps(route_doc,ensure_ascii=False,indent=2)+'\n')
alloc={'prior_history':'unknown; fresh worker did not inherit previous reading','reused_allocated_ids':ids,'new_allocation_command':'python work.py research new-id --count 2','newly_allocated_ids':extra,'assignments':[{'object_id':o['object_id'],'title':o['title'],'body':o['body']} for o in O if o['object_id'] in ids+extra]}
(W/'allocated-identities.json').write_text(json.dumps(alloc,ensure_ascii=False,indent=2)+'\n')
result=validate_batch(ROOT,record,expected_materials=MS,baseline_ref=D['baseline'])
receipt={'task_id':T,'batch_file':ref(p),'assets':[ref(p)],'reading':{'worker_mode':'fresh; prior worker history/reading not inherited','formal_materials':38,'shared_definition_files':2,'scope':'本次实际重新连续读完38份成熟正文全文及2共享定义；长输出截断处用精确行段续读（尤其12/13数值表、34/35定义/证明）。核成熟陈述、量词、前提、状态、完整论证及必要证据位置；未重新清洗、重证或重跑原程序，未声称继承旧worker阅读。','raw_evidence_scope':'原大JSON/源码/证书依成熟正文精确路径与SHA定位；未对全部原件全字节重审。另实际全文读R-3b6b两份小型certificate JSON、source/last_average_selection_independent_audit.json、replay/audit_last_average_selection.json、两份min_payoff discovery、smoke、run-manifest及validation；核完整21动作/客户类型与审计字段，仍未运行。正式正文已完整承重的解析论证直接复用。','mathematical_executions':0},'status':'local-mathematics-complete-pending-cross-owner-evidence','counts':{'objects':len(O),'materials':len(materials),'owner_routes':len(routes),'needs_decision_materials':sum(x['disposition']=='needs-decision' for x in materials)},'owner_routes':routes,'allocated_id_provenance':alloc,'validation':{'validate_batch':result,'material_sha256_all_match_task':all(sha(m['path'])==m['sha256'] for m in MS),'registry_mutated':False,'edge_files_empty':True,'semantic_note':'结构SHA与body/owner检查通过不等价于跨owner证据闭合。纯外owner材料needs-decision；有本批body的混合页objects而其未接来源在reason和owner_routes明确待判。'}}
Path('research/registration/receipts/'+T+'.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'batch':str(p),'objects':len(O),'materials':len(materials),'owner_routes':len(routes),'pending_materials':receipt['counts']['needs_decision_materials'],'validation':result},ensure_ascii=False))
