import json
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]
HERE = pathlib.Path(__file__).resolve().parent
TASK = 'register-ab98f323ad-0057'
task = json.loads((ROOT / f'research/operations/p25-register-v2/tasks/{TASK}.json').read_text())
materials = task['definition']['materials']
allocated = json.loads((HERE / 'new-ids.json').read_text())['object_ids']
objects = []

def ref(path):
    p = ROOT / path
    return {'path': path, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def mat(i):
    return dict(materials[i - 1])

DEFINITION = ref('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md')
MODEL = '有限不同单位客户、有限非空共同标签目录；单位提供者依次观察全部有序历史并各选一次；终局客户价值在覆盖者间均分，纯SPE在全部离轨有序节点保持真实后继。'

def add(oid, title, kind, status, body, statement, quantifiers, assumptions, scope, objections, evidence=(), extra=(), model=MODEL):
    ev = [DEFINITION] + [mat(i) for i in evidence] + [ref(p) for p in extra]
    own = mat(body)
    ev = list({x['path']: x for x in ev if x['path'] != own['path']}.values())
    text = (ROOT / own['path']).read_text()
    src = re.findall(r'(?:source:[^\s"\],]+)', text.split('---', 2)[1])
    objects.append({'object_id': oid, 'version': 1, 'title': title, 'kind': kind,
                    'truth_status': status, 'model': model, 'statement': statement,
                    'quantifiers': quantifiers, 'assumptions': assumptions, 'scope': scope,
                    'objections': objections, 'body': own, 'evidence': ev,
                    'sources': list(dict.fromkeys(src + ['state:' + own['path']]))})

add(allocated[0], '八客户删去未用主题可提高全部SPE福利且损失OPT', 'counterexample', 'proved', 1,
    '三人目录A={0,1}, B={2,3,4,5}, C={0,1,6}, D={0,1,7}有完整SPE ABB、W=6。只删C后A/B/D的全部SPE有序路径唯一DBB、W=7；同时OPT由8降到7，故只反驳这种删除保持某个不更高福利SPE，不承担保OPT版本。',
    '存在这一指定三人八单位客户完整SPE；缩减后量化全部完整SPE。', ['保持原标签收益与全部历史；缩减恰删C、另保D。'],
    '有限精确删目录反例；区别于保actual与唯一OPT支持的全人数删B族。', '正文保存21节点完整策略、全部原14条路径和缩减唯一DBB；证明/穷尽结果来自已整理规范与独立有序BI，不重跑。',
    extra=['archives/customer-attraction/tools/evidence/boss1-resume-independent-frontier-completion/source-manifest.json'])
add(allocated[1], '两人删未用标签保持计数福利而不能保持原有序SPE路径', 'counterexample', 'proved', 1,
    '两人A/B/C客户类型A4、B6、AB1、C5、AC4、ABC1有完整策略根B、A后C、B后C、C后A，实现BC。删A后唯一SPE路径CB，仍各选一B一C且W=17；所以只否定原有序路径保留，不否定原终局计数或福利保留。',
    '存在给定21单位客户两人完整SPE；删A后的全部SPE路径唯一CB。', ['缩减保B/C并删除不再被覆盖的A独有客户；所有真实回复保留。'],
    '准确有序缩减边界。', '正文逐行解析末位及根最佳回复，保真实平局；sample=20/tested=23是旧扫描索引/路径事件，不作命题量词。')
add('RI-SLACK-IDENTITY', '同一真实终局的剩余利润精确盈余递推', 'identity', 'proved', 2,
    '固定合法前缀h、背景b、余r≥1及任意完整形式策略，实际当前A后b′=b+1_A。P_h=u_h+P_hA；定义F_r(b)=max合法r槽Σc/(b+c)、E_h=2P_h−F_r、Δ_h=F_r−F_(r−1)(b′)，则E_h=E_hA+2u_h−Δ_h。此恒等式不需要均衡。',
    '每个有限合法实例、每个有序前缀及每个给定完整形式策略的同一真实终局。', ['父/子利润都使用该同一终局分母；F_0=P_terminal=0。'],
    '非零背景只记剩余玩家份额，根才等覆盖。', '孩子盈余可返还其精确数值；不同互斥孩子不得相加向同一实际W收费。', evidence=[4])
add('RI-FLOOR-RESERVE', '合法背景固定起点的全真实未来玩家静态保底', 'lemma', 'proved', 2,
    '固定起点(h,b,r≥1)，h_r(b)=max_TΣ_(x∈T)1/(b_x+r)。在任一完整纯SPE的任意真实后代节点，当前行动者最终收益≥h_r(b)，因此P_h≥r h_r(b)、E_h≥2r h_r(b)−F_r(b)。',
    '全部合法起点、每份完整纯SPE及该起点后的每个真实决策节点。', ['真实子博弈IC；起点后总共只有r位新覆盖者；达到最大值的T合法。'],
    '允许空主题、同覆盖别名、零客户和所有有序离轨平局。', '分母上界固定原起点b+r，不冻结偏离后继，也不借待证half循环证明floor。', evidence=[4])
add(allocated[2], '指定floor储备台阶若普遍成立则推出全背景半利润', 'conditional-reduction', 'proved', 2,
    '若所有合法背景余r≥2及全部完整SPE的实际步满足F_r≤max{2rh_r,2u+max(F_child,2(r−1)h_child)}，则由r=1最佳回复、孩子归纳及静态floor推出F_r≤2P_h，根得OPT≤2W。',
    '对假定普遍台阶作余人数归纳；结论涵盖全部合法前缀和完整SPE。', ['所列RESERVE-STEP全称假设；RI-FLOOR-RESERVE；真实孩子是子SPE。'],
    '已证明的逻辑蕴含；不把假前提认证为真。', 'RESERVE-STEP已由69客户完整四人SPE反驳，故此正确条件推导本身不能证明一般half。')
add(allocated[3], '全合法背景额外比较槽半利润义务', 'open-obligation', 'open', 4,
    '判定是否每个合法背景b、余r≥1和每份完整纯SPE均有F_(r+1)(b)≤2P_r(b,σ)，其中F用r+1个可重复比较主题，仅计这些比较玩家在原背景下的Σc/(b+c)。',
    '所有有限合法实例、合法有序背景、余人数r≥1及每份完整历史纯SPE。', ['比较槽比实际剩余人数多一；背景保留原合法过去玩家。'],
    '比同槽F_r≤2P_r更强的独立候选，不是EI的逐人静态Nash桥。', '所读probe仅1750输入的历史文字阴性且无独立stdout；未给普遍证明/反例。RS失败不逻辑反驳本候选。')
add('cag-carried-floor-recursive-step-fixed-cone-primal-dual-certificate', '固定69客户策略及ABCD最优面的floor台阶最大归一缺口为1/12', 'exact-optimization-certificate', 'proved', 6,
    '固定四人六标签闭式策略σ（前三恒A；末位按A计数/F条件取A/E/F）及O=ABCD，x≥0、实际W=1、自由缺口d。全部310条真IC、126条O最优约束、6+56+6个台阶分支共504行的有理LP最大d恰1/12。九类69客户点除以48且d=4/48达到；行30/31/32权1、77/106/123权1/6、498权1给β=1/12的非负对偶，客户余项≥0且自由d余项恰0。',
    '该固定完整σ、固定O与归一切片的全部非负有理/实客户质量可行点。', ['504行按原精确生成定义；d为自由实变量；W=1；O被所有四槽多重元组比较约束为最优。'],
    '单一策略锥与比较最优面；不优化任意σ/背景/人数。', '精确原始—对偶等值证明，不以HiGHS Optimal或有限PASS为一般结论。69客户只是达到点，原half仍成立。',
    extra=['archives/customer-attraction/tools/evidence/Boss7-resume-recursive-step/verify_saved_dual.py','archives/customer-attraction/tools/evidence/Boss7-resume-recursive-step/verification.json','archives/customer-attraction/tools/evidence/Boss7-resume-recursive-step/manifest.json'])
add(allocated[4], '指定八客户策略三个actual前缀均不违反正确额外iid槽桥', 'theorem', 'proved', 7,
    '四题A₂、B₄、A₂+c、A₂+d的给定三人SPE actual(0,1,1)、各收益2。正确r+1人辅助静态iid Nash在根λ4<15/8<2，在前缀0后λ3<52/27<2，在01后λ2=76/45<2。Nash分布为(0,t,(1−t)/2,(1−t)/2)，各层的唯一内点根由正文三精确多项式确定。',
    '仅该指定完整SPE的全部三个实际前缀；静态值对辅助游戏的任意对称Nash相同。', ['背景保留；r为iid竞争者数；辅助总人数r+1；T0严格被T2支配。'],
    '指定压力家族未命中，不是EI普遍证明。', '完整SPE资格复用原八客户对象；静态Nash解析与动态SPE分别承担。旧同人数λ3(0)>u不反本根λ4。', evidence=[5,11])
add(allocated[5], '36客户块复制压力族所有k的正确额外iid根值小于10', 'theorem', 'proved', 7,
    'k≥1个互不交36客户块、m=3k、6k题的既有nice-history完整SPE根u=10。均匀q为辅助3k+1人iid对称Nash，λ=3E[1/(1+Bin(3k,1/(3k)))]+18E[1/(1+Bin(3k,2/(3k)))]<12−3/e−9/e²<10；k=1值305/36。',
    '每个整数k≥1的根；不量化这些复制族全部非空前缀。', ['原36客户块及nice-history完整SPE资格复用；均匀目录置换对称；正确3k个iid对手。'],
    '一整解析压力族的根排除。', '二项积分严格指数上界承担全k；1296静态值只属k1的有限检查，不能外推。', evidence=[5,11])
add(allocated[6], '固定完整策略总覆盖机会的IC加epigraph攻击合同', 'method', 'proved', 10,
    '固定全部有序历史策略σ、非负客户型质量x，全部真实单偏离IC恰刻画其SPE质量锥。在根收益u=1切片，对每个m−1不同标签支持D加入coverage({0}∪D)≤q，最小化q−coverage(O)时q恰为固定根标签后最佳m−1槽总覆盖；负目标是OPT首步补全损失的下界，O最优时等于该损失。',
    '固定m,k,σ,O且k≥m−1；全部非负质量可行点。', ['所有有序历史真实IC；q只以正系数进目标；补足不同标签不减覆盖；根行动0及根收益1归一化。'],
    '覆盖epigraph发现方法；不同于非零背景剩余利润F。', '原九次仅浮点有限O/固定锥、未附有理对偶，不能据阴性证明δ≤2u或half；此为完整精确合同的正确性。')
add(allocated[7], '固定完整策略及有理iid分布的精确反例接受判据', 'method', 'proved', 10,
    '固定四人六标签完整σ及有理查询q，g_M=Σ_(j=0)^4(1−t_M)^j/5，α_a=1_(a∈M)g_M、λ=Σq_aα_a。若有理x≥0、Σx=1满足全部真IC、支持λ−α_a精确0、零支持λ−α_a≥0且(u_root−λ)·x<0，则q为辅助五人静态对称Nash，清分母整克隆给原单位客户合法EI反例。',
    '每个固定有理q及每个通过全部精确行的有理x；并非仅原七q。', ['指定σ在全部259有序节点定义；真实后继IC；g的几何和端点t=0取1。'],
    '有限有理恢复接受保证。', '原七q/四恢复点只有历史文字、未取得向量/对偶；恢复失败不证明无有理点，非负点也不证明同锥最优。')
add(allocated[8], '含空题的全actual路径额外槽推送二次稀释恒等式', 'identity', 'proved', 11,
    '任意完整形式策略，令Z_i(t)在actual位置i强制t后沿同σ真实完成全部m槽。D=ΣE_t u_i(Z_i(t))，G=ΣE_(t,s)insert_s(Z_i(t))。对空题E、p_e=(1−e)δE+e q，H_E(q)=ΣE_s insert_s(Z_i(E))，则D(p_e)=eD(q)、G(p_e)=e(1−e)H_E(q)+e²G(q)，故D−G=e(D−H)+e²(H−G)。',
    '任意有限目录含空题、完整形式策略、查询分布q及e∈[0,1]。', ['insert的分母为1+完整m槽客户负载；空题源/查询给0；同一actual位置和真实改变后继。'],
    '全actual位置二抽样代数；不需要SPE。', '若∀p强ΣG≤ΣD则必D(q)≥H_E(q)；此为必要条件，不付款弱ΣG≤W。', evidence=[12])
add(allocated[9], '34客户全actual路径强推送桥的空题稀释反例', 'counterexample', 'proved', 11,
    '既有三人七题34客户完整SPE actual034，u=(29/3,67/6,67/6)、W32、OPT34。对q=δX2，三个actual位置真分支得ΣD=63/2、ΣH_E=65/2、ΣG=41/2；故p_e沿空题方向的Σ(D−G)=12e²−e<0当0<e<1/12，e1/24差−1/48。',
    '存在所给完整SPE，且全部e∈(0,1/12)均反强全路径桥。', ['完整57节点策略与34单位客户原证书；三位置均沿同σ强制后真实完成。'],
    '强ΣG≤ΣD失败；本扰动线始终G≤41/2<W32，不反弱福利聚合。', '不同于根单点−e+25e²/6。W−D(p_1/24)=491/16仍为大IC松弛，不能把强失败升成half反例。', evidence=[5,12],
    extra=['archives/customer-attraction/tools/evidence/extra-iid-aggregation-and-reserve-primary/related-audit-source-manifest.json','archives/customer-attraction/tools/evidence/extra-iid-aggregation-and-reserve-primary/original-audit-execution-summary.json'])
add('customer-attraction/global-terminal-depth-harmonic-weakening-obstruction', '全树末k层真实最优加早期实际鲁棒保底仍有无界调和损失', 'obstruction', 'proved', 14,
    '每m≥2、1≤k<m，K=lcm(1,…,m)，m个不交大主题各K及m−k个私有E_j大小K/(m−j+1)。完整形式策略前m−k位置恒选各E_j，之后fresh大题；任意深度≥m−k节点都真BR，全部早期实际鲁棒保底亦成立，却W=K(k+H_m−H_k)、OPT=mK。固定k比例无界，若2(k+H_m−H_k)<m则弱化破half。',
    '全部整数m,k；每个深层有序历史与全部早期实际逐主题保底。', ['只保所列弱化，不要求早期真实IC；主题互不交，K整除全部大小。'],
    '比仅固定实际前缀尾SPE更强的删信息障碍。', '早期改fresh大题得K>K/r_j，明确非SPE。不能分离完整Γ或否所有全树方法。', evidence=[13])
add(allocated[10], '固定末两人菜单加非均匀早期H/L保底的三原子分离', 'obstruction', 'proved', 14,
    '固定G=S+Z/(2m)+V/m，早期H_j=u_j−Σ_(x∈A)1/(b+r_j)、L_j=u_B−U_p(E_j,A)，m≥3。不存在λ_j,γ_j≥0使全部合法客户类型的2w−o−G−ΣλH−ΣγL逐列非负：只属A列迫Λ≥3(m−2)，只属B列迫Γ≤3/2，全部E列又迫Λ≤(m−2)(2m+3)/(2(m−1))，矛盾。',
    '每个m≥3及任意依m选择的非负非均匀乘子；全部合法客户兴趣列。', ['明确固定G/H/L合同；三个客户型只属于比较T1而不属于任何R_i。'],
    '指定行锥逐坐标证书不可能性。', '合法兴趣列不等同时满足全部SPE行的客户向量；不构成原模型SPE反例，重选G/增早期真分支不在排除范围。')
add('customer-attraction/bounded-suffix-security-insufficient-for-half', '固定实际前缀尾SPE与早期最坏保底不足half', 'obstruction', 'proved', 15,
    '每k≥1、m≥2k+1，n=m−k、L=k+1。E含n客户，m个不交Q各L，形式路径E^n Q1…Qk；固定该前缀后的完整k人尾是SPE，早期全部逐题最坏分母保底成立，但W=m+k²、OPT=(k+2)m−2k−1、OPT−2W=k(m−2k−2)−1，m≥2k+4时正。',
    '全部整数k≥1,m≥2k+1；完整尾部所有有序历史，早期全部实际位置和主题。', ['只保早期鲁棒下界；不要求早期真实偏离最优。'],
    '固定k时OPT/W→k+2的精确弱化边界。', '最后一个早期E玩家真改fresh Q得k+1>1，故形式策略非SPE。与全树深层调和族规模/量词不同。')
add('ACTUAL-OPTIMUM-PRUNING', '仅保actual与唯一OPT支持可排除全部原低福利SPE', 'obstruction', 'proved', 16,
    '每m=k+1≥2，X_i两客户、私客a_i及b,d，A_i=X_i+a_i、B_i=X_i+b、C_i=X_i、D={b,d}。存在原完整SPE C1…CkD、W2m；唯一最优支持全A加D覆盖3m−1。只保actual与OPT支持即删全部B后，每份完整SPE恰全A任意排列再D，W=OPT=3m−1，故没有不更高福利的SPE。',
    '每m≥2；原SPE存在量词，原全部最优排列共享唯一支持；缩减后量化每份SPE。', ['全部真实有序子树；Q状态允许多旧A；剪枝F/E增强域保旧C末端升级。'],
    '免费actual/OPT目录缩减桥的全人数否定。', '原最低福利未声称恰2m；剪枝按删B，非删C的极大化操作；始终half成立，不给复杂度或一般小闭包下界。', evidence=[1,13])
add('customer-attraction/fixed-label-hamming-neighborhood-and-complete-tail-row-truncation', '固定标签Hamming保护带加全部真实尾IC的删行障碍', 'obstruction', 'proved', 17,
    '每m≥1、0≤k≤m−1、0≤r≤m−k−1，n=m−k,d=n−r，L为1…d公倍数；不交A_i大小L/max(d−i+1,1)及m个B各L。完整形式策略保护全部actual节点、早期固定A标签前缀距离≤r节点和全部最后k层真IC，却W=L(H_d+r+k)、OPT=mL；m>2(H_d+r+k)时仅此删行锥无half证书。d≥2在h=(B1,…,B_(r+1))有规定L/d、偏离fresh B得L的明确省略负行。d1则整树受保护且全效率。',
    '全部列明整数参数及全部被保护有序历史和合法偏离。', ['Hamming距离相对固定标签前缀，不是相对σ行为偏离数；同一完整形式策略真完成。'],
    'Γ_ret的非负锥分离；固定k/r无常数比，k+r线性小于m/2亦可破half。', '非SPE向量不能分离完整Γ；d1与有限程序中的完整SPE认证单列。20组/560组/8组有不同枚举域，PASS含预期负行。', evidence=[18,19,20,21,22,23,28],
    extra=['archives/customer-attraction/tools/evidence/R51-hamming-tail-auditor/manifest.json','archives/customer-attraction/tools/evidence/R51-path-tail-obstruction-auditor/manifest.json'])
add('customer-attraction/common-core-equal-private-symmetric-occupancy-DP', '公共核等私客的HM最大占用置换压缩精确递推', 'algorithm', 'proved', 26,
    '恰m≥1标签、K≥0个共同单位客户、每题一私客，终局已占用a收益K/m+1/z_a。P_j(b)=max_(z∈HM(b))z_j足以给L_M=K/m+max_a1/P_a(b+e_a)，按myopic上界筛E，再P逐坐标max、G=L+min_child G。排序计数并恢复等计数组完整置换轨道后，原算法每态返回准确P/G/L，仅需Σ_(n=0)^m p(n)个分拆态。',
    '全部整数m≥1,K≥0及每个合法计数前缀；保持原全部有序历史策略域。', ['只查询已加e_a的a坐标；eligible用K/(|b|+1)+1/(b_a+1)；等计数组对称。'],
    '精确HM放松算法，不是真SPE全集、HI或一般half算法。', '零占用辅助坐标不能用倒数冒充min收益；不要求坐标max共同实现，不给位复杂度多项式或原main运行认证。', evidence=[25])
add(allocated[11], '保存的六客户五标签静态鞍点边界重构值为一', 'exact-static-instance', 'proved', 29,
    '五标签中3为一名私客，0/1/4同覆盖另五客户，2为空。查询p3=1/3,p4=2/3，四槽背景按单客槽s、五客槽r有F=1/[3(s+1)]+10/[3(r+1)]≥1，r+s≤4；纯四五客块给全部查询≤1，故v5=1。全部最坏标签计数25个（15个s0/r4、10个s1/r3）；选中s1/r3占用3收益1、净债0。',
    '该固定六单位客户五标签实例的全部70个四槽计数背景与全部查询。', ['明确从保存近似点重构整数1、5及概率1/3、2/3；保同覆盖异标签和空题。'],
    '独立可复用精确边界实例，非坏占用反例。', '原active_backgrounds=2是重权前种子，不能当重构后最优面；不认证原浮点权重的精确最优面。',
    extra=['archives/customer-attraction/tools/evidence/occupied-security-program-closure/verify_saved_boundary.py','archives/customer-attraction/tools/evidence/occupied-security-program-closure/saved-boundary-exact.json'])
add('customer-attraction/padded-on-path-same-topic-kernel-budget-boundary', '同主题actual节点查询的补位核最小预算为(1+1/m)W', 'obstruction', 'proved', 33,
    '每m≥2在86客户五题基础上加m−2个22客户私有Z，存在完整SPE Z1…Z_(m−2),E,A，各人22、W22m，唯一OPT支持全Z+B+D覆盖22m+1。限制查询取自actual上规定行动等于分配槽主题的节点时，所有匹配及满足逐客户(C)/核覆盖的非负污染与权重最小预算恰22(m+1)。解除同主题节点限制，全部复用末A节点、P0/λ1，预算22m，真实查询和44+11(m−2)≤W。',
    '每整数m≥2；原完整SPE存在，所述受限付款族内对全部匹配/非负P/权重取最小。', ['配套加权调和引理的(C)和Kλ(Jx)≥1；唯一最优比较客户为单元素索引；真实指定续局完整粘合。'],
    '受限接口锐预算下界与同族跨主题逃逸。', '非普遍运输/half障碍；m2…5机器全树数据只作有限证据，全m由解析扩展与唯一OPT证明承担。', evidence=[32],
    extra=['archives/customer-attraction/tools/evidence/cyclic-padding-boundary/source-manifest.json','archives/customer-attraction/tools/evidence/cyclic-padding-boundary/audit_full_data.py'])
add(allocated[12], '恒大主题族固定同一最优链的非负IC重赋权仍不能逐列证明half', 'obstruction', 'proved', 34,
    'm≥4，m客户大题B和m−1不交单例的完整恒B SPE。任意固定最优排列链的强制B行全零，强制单例、B负载k的行在该单例为−1、每个B客户1/k。若仅该链m条IC加客户非负性逐列证明2W−OPT，乘子须λ_k≥1且Σ_(k=2)^m λ_k/k≤1，然而H_m−1>1，矛盾。',
    '每m≥4和每个固定的最优主题排列链；所有非负同链乘子。', ['只允许这条固定链的真实IC与客户非负性；λ可依m和链选择。'],
    '比单位UV链失败更强的同链调权边界。', '不排跨链任挑单行、链外IC、signed债或一般全树证书；原完整SPE仍W=m、OPT2m−1。')
add('customer-attraction/frozen-optimal-matching-outside-credit-and-quantifier-boundary', '四客户给定最优比较的全部冻结匹配超过W加外信用', 'counterexample', 'proved', 35,
    '两人四客A={x,y},B={b,c},T={x,y,c},D={x,y,b}，完整策略根A，末回复A→B,B→D,T→D,D→T。actual AB、W=OPT4。给定最优(T,D)的两冻结匹配均9/2>W+|U\\C|=4；但最优AB/BT/BD最小匹配2/3/3，因此此例仅反每个给定最优版，不反存在某最优弱版。',
    '存在给定完整SPE与指定最优T,D；对其全部两种冻结匹配。', ['冻结报价固定其他actual行动；与真实改变后继收益分开；所有五节点及平局保留。'],
    '冻结匹配量词及后继可信性边界。', '原B后末位D收益应5/2而非2，纠正不损SPE。存在最优弱版已被另52客户唯一OPT反驳，此处不重复立该身份。')
add('customer-attraction/full-spe-static-positive-regret-four-client-replication', '四客户副本全树SPE使静态正遗憾归一化无界', 'counterexample-family', 'proved', 36,
    '每k≥1，k个不交四客块X={a,b},Y={c,d},Z={b,c,d}、m2k。五态规范历史E/Y/XY/Z/ZZ加永久BI接管给完整SPE，actual全Y再全X，各人2、W=OPT4k；每Y静态正遗憾1/2、每X为0，R=k/2。因此任何固定有限C≥0的R≤CW/m被k>4C否定。',
    '每整数k≥1存在给定完整纯SPE；任何固定有限C可选择人数2k反驳该桥。', ['规范模式离开五态后永久在确切有序子树BI接管；共同全3k标签；静态遗憾冻结其他终局动作。'],
    '归一化静态遗憾桥失败；可变人数，不直接否固定五人RT5。', '唯一危险E→Z偏离由规范ZZ给3/2，其余即时上界安全；不能简单并独立策略。全覆盖最优，不反half。已全文实读0084的R-18 round3成熟障碍页并核精确字节：同全部k五态永久BI副本族，54891状态/行动、k1/2完整树和k5值仅作其所列有限证据，不重复造主身份或据此反固定五人RT5。',
    extra=['archives/customer-attraction/state/资源/可信副本拼接的审查版本与低福利缺口--资源.md',
           'archives/customer-attraction/state/障碍/R-18-round3静态总正遗憾可信副本放大族--障碍.md'])
add('customer-attraction/five-player-frozen-regret-coverage-tax-sufficient-budget', '五人实际SPE终局的RT5静态遗憾税义务', 'open-obligation', 'open', 37,
    '每份五人完整纯SPE实际终局s，冻结其他四行动的总正遗憾R=Σ_i(max_Q u_i(Q,s_−i)−u_i(s))与Z=Σ_(c_x>0)1/(c_x+1)是否总满足R≤6Z/5？',
    '所有有限合法共同目录单位客户实例及每份五人完整历史纯SPE。', ['R含原动作故非负；Z是同一实际终局税，不能跨枝相加。'],
    '独立加强候选；half已证不反向证明RT5。', '44客户压力例仅R/Z20/23，旧三人浮点阴性不关闭五人量词；可变人数副本放大亦不直接否定。')
add(allocated[13], '五人任意终局满足RT5即推出半覆盖', 'conditional-reduction', 'proved', 37,
    '任意五人终局，令R为冻结总正遗憾、Z=Σ1/(c+1)。若R≤6Z/5，则OPT5≤2W。对最优比较均匀随机排列，冻结收益均值F≤W+R，逐客户得L+6Z_O/5≤W+R；故OPT≤2W+R−6Z_O/5−E，且6Z_E/5≤E。',
    '任意有限合法目录的任意五人终局；不需SPE，只额外假定所列RT5。', ['比较索引允许重复；真实SPE与冻结报价不混；W0边界单列。'],
    '已证充分逻辑；RT5普遍真值仍open。', '不是从SPE直接断冻结偏离≤u；Z_O与Z_E必须来自同一实际终局。')
add(allocated[14], '任意非负背景末两人冻结遗憾由实际差集税支付', 'lemma', 'proved', 37,
    '背景b≥0、真实两人SPE(A,B)，f(X)=Σ_X1/(b+1),g(X,Y)=Σ_(X∩Y)1/[(b+1)(b+2)]。任一首人冻结替换T的遗憾U(T;B)−U(A;B)≤g(A,A\\B)；末位静态遗憾0。因此两人总正遗憾≤g(A,A\\B)，零背景时≤|A\\B|/2≤Z。',
    '每个非负整数背景、每份完整两人子SPE和每个合法T。', ['T后真实末回复Q；依次用首位IC、离轨/实际末位BR及非负集合差。'],
    '局部两尾运输，不把多个后继合为一名整组行动者。', '只给同一实际A\\B的局部税；尚未证明五位总遗憾共同预算。')
add(allocated[15], '44客户五人保险SPE的冻结遗憾税压力值20/23', 'construction', 'proved', 37,
    '五个经济块各4、四个银行块各6、20个Cartesian标签共44单位客户，完整BASE/PUNISH/EXIT控制器给actual经济负载(4,1,0,0,0)、银行(2,1,1,1)、收益(4,7,7,7,7)、W32、OPT44；冻结遗憾R12、Z69/5，R/Z20/23。一般块大小a,b该同一控制器成立当且仅当b≥3a/2。',
    '存在这份完整五人SPE；所列控制器对一般正块大小的准确可信性门槛。', ['BASE根重锚；fresh银行偏离触发末位复制；EXIT的过去银行已重复；PUNISH保持目标。'],
    'RT5与更强R≤Z均未被该指定压力例反驳。', '全有序历史和再次偏离由三模式解析证明；三人浮点探针不能代替此构造，控制器新颖性不另认领。')
add('customer-attraction/five-player-strategic-normal-form-equilibrium-credibility-gap', '437客户策略正规式NE低于half且离轨IC缺口48', 'counterexample', 'proved', 39,
    '五人十个不交主题A1…A5大小12,15,20,30,60及五O各60，共437客户。完整策略在精确A路径选下一A，离轨后永久复制首错标签；actual W137、OPT300。任一玩家单边改完整策略只能改变其唯一actual节点，收益≤60/(6−i)=|A_i|，故为策略正规式NE。离轨(O1)处第二人复制得12、改O2独享60，IC−48，故非SPE。',
    '存在该完整策略剖面的正规式NE；所有纯/混合单方策略偏离不获利；存在明确离轨盈利偏离。', ['所有11111有序决策节点有定义；每人只行动一次；首次错误标记永久保持。'],
    '任何覆盖全部普通策略NE的smoothness保证常数须≥300/137>2。', 'SPE专用离轨可信性证明不受此边界否定；不反已证五人half或六人目标。', evidence=[38])

# Existing mathematical owners are reused only after their actual record binds
# these exact bytes. An unanswered request never becomes acceptance.
all_owners = {}
owner_locations = {}
registry_path = ROOT / 'research/registry.json'
published_records = [registry_path]
for tp in sorted((ROOT / 'research/operations/p25-register-v2/tasks').glob('*.json')):
    state = json.loads(tp.read_text())
    receipt = state.get('receipt', {})
    br = receipt.get('batch_file')
    if state.get('state') != 'done' or not br:
        continue
    p = ROOT / br['path']
    if p.is_file() and ref(br['path']) == br:
        published_records.append(p)
for p in published_records:
    for o in json.loads(p.read_text()).get('objects', []):
        oid = o['object_id']
        owner_locations.setdefault(oid, []).append(ref(p.relative_to(ROOT).as_posix()))
        # Current canonical takes precedence. A claimed draft is not an
        # acceptance, and equal-version records are never silently overwritten.
        if oid not in all_owners:
            all_owners[oid] = o
requests = json.loads((HERE / 'attachment-requests.json').read_text())['requests']
pending = {}
extra_owners = {}
route_checks = []
for r in requests:
    owner = all_owners.get(r['object_id'])
    refs = {x['path']: x['sha256'] for x in ([owner['body']] + owner['evidence'])} if owner else {}
    for ev in r['requested_evidence']:
        assert ref(ev['path']) == ev
        accepted = refs.get(ev['path']) == ev['sha256']
        route_checks.append({'object_id': r['object_id'], 'material': ev,
                             'accepted': accepted,
                             'owner_status': 'published-main-record-missing-exact-evidence' if owner and not accepted else
                                             'accepted' if accepted else 'main-record-not-published',
                             'main_body': owner['body'] if owner else r.get('expected_main_body'),
                             'owner_task': r.get('owner_task'),
                             'next_action': r.get('next_action'),
                             'published_owner_records': owner_locations.get(r['object_id'], []),
                             'mathematical_reason': r['mathematical_reason']})
        if accepted:
            extra_owners.setdefault(ev['path'], []).append(r['object_id'])
        else:
            pending.setdefault(ev['path'], []).append(r['object_id'])

# Two previously published acceptances, confirmed by reading registry/batch refs.
preaccepted = {
    5: ['M-39efbd59b255457e82303be3881f54d5', 'M-3ef821ac4c2f4acc961f098e4973c094', 'M-e39117bc24ae48adaba9e454a64f666b'],
    34: ['customer-attraction/optimal-prefix-customer-variation-harmonic-obstruction'],
}
for i, ids in preaccepted.items():
    p = materials[i - 1]['path']
    for oid in ids:
        o = all_owners[oid]
        assert any(a['path'] == p and a['sha256'] == materials[i - 1]['sha256'] for a in o['evidence'])
        extra_owners.setdefault(p, []).append(oid)

rows = []
for i, m in enumerate(materials, 1):
    p = m['path']
    owned = [o['object_id'] for o in objects if o['body']['path'] == p]
    supported = [o['object_id'] for o in objects if any(a['path'] == p for a in o['evidence'])]
    ids = list(dict.fromkeys(owned + supported + extra_owners.get(p, [])))
    if pending.get(p):
        disposition = 'objects' if owned else 'needs-decision'
        missing = [r for r in route_checks if r['material']['path'] == p and not r['accepted']]
        details = []
        for r in missing:
            status = '主record尚未published/canonical，须由其真实owner发布后接证' if not r['published_owner_records'] else '已发布主record尚缺本页精确path/SHA，须由lead定向补证'
            details.append(r['object_id'] + '：' + status + '；' + r['mathematical_reason'])
        reason = '沿用已完整实读成熟稿，本轮定向复核陈述/量词/条件与实际接证。' + ('本批独立成熟对象已保全；' if owned else '') + '未决仅为以下外owner路由，非数学open：' + '；'.join(details) + '。精确已发布record路径/SHA、材料字节与下一步见Boss2/0057/read-and-routing-audit.json；不能以claimed草稿、发送请求或本地peer代替接收。'
    elif owned:
        disposition = 'objects'
        reason = '全文实读；独立陈述、量词、条件及完整论证见所列对象，程序/数值和历史审查按数学owner归证，不以PASS另立节点。'
    elif ids:
        disposition = 'attachment'
        reason = '全文实读；同一数学的必要原实现、有限报告、独立证明重构或来源闭包，精确字节已经由所列数学owner实际引用。不同程序覆盖域及历史阅读/执行时序分别保留。'
    else:
        disposition = 'excluded'
        reason = '全文实读；仅历史导航/来源时序或外部文献假设比较，无新增可独立引用的本模型数学结论；不以文献半界、程序名称或缺失运行补造对象。原文保留用于追溯。'
    rows.append({**m, 'disposition': disposition, 'object_ids': ids, 'reason': reason})

record = {'schema': 2, 'objects': objects, 'materials': rows, 'edge_files': []}
out = ROOT / f'research/registration/batches/{TASK}.json'
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
audit = {'task_id': TASK, 'read_complete_materials': list(range(1, 40)),
         'shared_definition_read': DEFINITION, 'new_object_count': len(objects),
         'unaccepted_external_owners': pending, 'batch_file': ref(out.relative_to(ROOT).as_posix()),
         'current_registry': ref('research/registry.json'),
         'external_route_checks': route_checks,
         'accepted_uv_route': {'object_id': preaccepted[34][0], 'material': mat(34),
                               'published_owner_records': owner_locations[preaccepted[34][0]],
                               'status': 'accepted-exact-bytes; duplicate evidence request withdrawn',
                               'identity_boundary': 'UV不存在及完整链随机化失败沿既有主record；固定同一链非负lambda不可能性由本批M-4792b826411b402fb3a164d1d76e5526保独立范围；不把UV失败升级为SM/TB或half失败'},
         'accepted_incoming_evidence': [{'source_task': 'register-ab98f323ad-0084',
                                        'object_id': 'customer-attraction/full-spe-static-positive-regret-four-client-replication',
                                        'version': 1,
                                        'material': ref('archives/customer-attraction/state/障碍/R-18-round3静态总正遗憾可信副本放大族--障碍.md'),
                                        'reading_scope': 'Whole mature page; exact same all-k game, five canonical states, permanent BI takeover, static R=k/2 and arbitrary fixed-C bridge failure. Finite 54891 checks and k1/2 tree counts remain finite; no mathematical run repeated.',
                                        'status': 'accepted in this actual main record; source-task author can reverse-route exact bytes after publication'}],
         'scope': 'Prior complete reading of 39 mature state files retained; this resumption targeted exact statements, quantifiers, conditions and carrying evidence, plus current canonical/done receipt bytes. Existing complete proofs reused; no mathematical programs rerun; no graph edges; no canonical writes'}
(HERE / 'read-and-routing-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
receipt = {'task_id': TASK, 'batch_file': audit['batch_file'], 'assets': [audit['batch_file']],
           'mathematical_open_objects': [o['object_id'] for o in objects if o['truth_status'] == 'open'],
           'routing_pending_materials': [m['path'] for m in rows if m['disposition'] == 'needs-decision'],
           'routing_pending_owners': sorted({oid for ids in pending.values() for oid in ids}),
           'routing_audit': ref((HERE / 'read-and-routing-audit.json').relative_to(ROOT).as_posix()),
           'accepted_incoming_evidence': audit['accepted_incoming_evidence'],
           'completion_scope': 'Mature mathematics is deliverable with explicit unresolved external evidence routes; no main record duplicated, no canonical acceptance or final registration closure claimed.'}
(ROOT / f'research/registration/receipts/{TASK}.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'objects': len(objects), 'materials': len(rows), 'pending_materials': len(pending), 'batch': str(out)}, ensure_ascii=False))
