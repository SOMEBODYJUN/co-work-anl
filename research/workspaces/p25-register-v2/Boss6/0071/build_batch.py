"""Boss6: manually identified Claims; hashes and reverse owners are mechanical."""
import hashlib
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[5]
TASK = 'register-ab98f323ad-0071'
HOME = ROOT / 'research/workspaces/p25-register-v2/Boss6/0071'
task = json.loads((ROOT / f'research/operations/p25-register-v2/tasks/{TASK}.json').read_text())['definition']
ids = json.loads((HOME / 'new-ids.json').read_text())['object_ids']
model_path = 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
model = '有限单位客户，有限非空共同标签目录，单位提供者依全部有序历史各选一次；终局各客户在覆盖者间均分。允许空覆盖、同覆盖异标签、重复行动及任意离轨平局；特殊加强域逐项明列。'

def ref(path, section=None):
    d = {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
    if section: d['section'] = section
    return d

def material(i): return task['materials'][i-1]['path']

objects = []
def add(i, oid, title, kind, status, statement, quantifiers, assumptions, scope, objections, *, section=None, extra=(), model_text=model):
    text = (ROOT / material(i)).read_text()
    fm = yaml.safe_load(text.split('---', 2)[1]) if text.startswith('---\n') else {}
    sources = [str(s) for s in fm.get('source_refs', [])] or ['canonical:' + material(i)]
    evidence = [ref(model_path)] + [ref(material(j)) if isinstance(j, int) else ref(j) for j in extra]
    # Whole body is intentional when its proof spans sibling sections.
    obj = dict(object_id=oid, version=1, title=title, kind=kind, truth_status=status,
               model=model_text, statement=statement, quantifiers=quantifiers,
               assumptions=assumptions, scope=scope, objections=objections,
               body=ref(material(i), section), evidence=evidence, sources=sources)
    objects.append(obj)

read_note = '已实读成熟正文的精确陈述、条件、承重论证位置及证据职责；复用成熟证明，不重跑原程序或全树审计，不声称全文重读大原始证书。'

add(1, 'customer-attraction/common-static-q-certificate-generator',
    '固定完整策略锥任意目标的一份共同Q全查询充分证书', 'method', 'proved',
    '固定完整策略IC行G和合法静态背景B_j，对目标向量u，若存在Q>=0、ΣQ=1，以及每查询a各自λ_a>=0、逐类型r_a>=0，使u−Σ_j Q_j F_{j,a}=G^Tλ_a+r_a，则所有w>=0且Gw>=0同时满足u·w>=E_Q f_B(a;w)，从而u·w>=max_p min_B E_p f_B(a;w)。同一Q不观察查询且不依赖w；目标若确为某玩家完整收益行才可读逐人安全界。',
    '任意指定有限G/F/目标u及每个真实可行客户向量w；证书存在性作为验收前提，未声称任意σ/u都存在。',
    ['G确为该完整σ全部有序历史真实IC且符号Gw>=0', 'F和背景列表覆盖所宣称的静态对手域', 'Q归一、非负乘子及所有逐类型等式精确成立'],
    '给目标u的充分证书及有理后验验收；与聚合目标c/n的另一生成器区分目标，未取得本源common_Q输出。',
    read_note + '原attack依赖/目标构造不齐且无保存输出；Fraction近似恢复只有精确归一、非负、逐列残差全通过才成证。没有由缺输出推不存在，也无六人half结论。',
    extra=('archives/customer-attraction/tools/evidence/security-gluing-boss5/original/common_q_generator.py',))

add(6, 'customer-attraction/ordered-terminal-tax-boundary',
    '同一静态PNE且可SPE实现的计数不允许任意重排为根税路径', 'construction', 'proved',
    '每整数n>=4有共同目录叶L_i、中心H及不交B：叶各2(n−2)私客+2中心客，|H|=2(n−1)，|B|=(n−1)(2n−3)。q_H=1,q_B=n−1为PNE且存在完整SPE实际(H,B,…,B)，W=(n−1)(2n−1)、OPT=(n−1)(4n−5)，正确路径W+τ−OPT=1。重排(B,…,B,H)给OPT−W−τ=(n−1)(n−3)/n>0，但倒二改叶后真末位必须另叶使收益h>2n−3，该重排不能是SPE。',
    '每整数n>=4的显式单位客户族；存在一份完整SPE，且指定另一有序路径不可SPE。',
    ['使用正文全部历史补全规则与真实改变后末位回复', '比较量为指定有序前缀税而非仅终局计数'],
    '反驳可实现计数+任意末位指定的放松，不反驳half，亦不同于61客户真实根税反例。', read_note)

add(7, ids[0], '五客户单色后缀必要负点无法补成所指定的真实SPE', 'counterexample', 'proved',
    'A={4},B={1,2,3},T={0,4},Y1={0,3},Y2={1,2,4}三人实例，必要松弛指定actual(A,B,B)有u_A=1、τ_A=1/2、q(T)=2，负目标−1/2。然而强制根B后的全部可实现两尾是(B,T),(T,B),(T,Y2),(Y1,Y2),(Y2,T),(Y2,Y1)，根B本人最低收益3/2>1，故任何完整SPE都不能保持该actual。',
    '此一固定五单位输入，全部强制B后的完整纯子SPE；非只某个tie selector。',
    ['保共同目录全部五主题与真实两人孩子', 'necessary行不替代全历史IC'],
    '精确排除必要点的SPE补全；不是一般VA(r)或half反例。', read_note)

add(7, ids[1], '五客户静态弱占优主题不使动态完整SPE最大化调和势', 'counterexample', 'proved',
    '两人目录B={0,1,2,3},C={2,3,4},D={0,1}，根D，首B/C/D后末位分别B/B/C。所有根真收益2、末位各为BR，给完整SPE(D,C)、收益(2,3)、W5、Φ5；B对任一静态对手弱优于C/D，B²为PNE且Φ6。因此静态弱占优不强迫动态SPE最大化共同调和势。',
    '一固定五客户两人完整策略及所有静态对手主题。', ['原完整四节点回复表', '势按客户负载H_c求和'],
    '静态弱占优与动态势桥的精确反例，half仍成立。', read_note + '原报告势字段为字面常数字符串；采用正文解析计算Φ5和4H2=6，不冒作程序独立重算。')

add(8, ids[2], '固定前缀互惠末回复链的对称核与r至少二的端点债', 'lemma', 'proved',
    '固定H、整数r>=1，f_H(a)=Σ_a1/(h+1)，L_H^r(a,b)=U_a(H+a+r b)，K=f_H(b)+L=f_H(a)+f_H(b)−rΣ_ab1/[(h+1)(h+r+1)]对称。R(b)为H+b^r后的真实末位，a_(t+1)=R(a_t)使K沿链不减，有限目录环内全等。P=rU_a(H+r a+b)+rU_b(H+a+r b)=K+E；仅r>=2时E非负，其单/双命中系数为(r−1)h/[(h+r)(h+1)]、[(2r−2)h+r−2]/[(h+r+1)(h+1)]。链两端P_s<=P_t+E_s−E_t。r2有E_s<=n1/6+4n2/15<=4|∪H|/15，并可由任一三真后继的同前缀cohort最终利润一次支付。',
    '固定同一H,r及原完整策略的真实末位映射；K部分r>=1，非负债与r2支付按各自域。',
    ['所有链步在同一前缀和r上', '债只能由同一个前缀cohort收费一次'],
    '单层运输与端点账，不提供跨前缀粘合或根half。',
    read_note + '已定位原文域错：r1双命中E系数负，不能照抄“均非负”；登记将非负E限制r>=2。P端点恒等式本身不要求E非负。冻结正文未改字节。')

piroot = 'archives/customer-attraction/tools/evidence/pi-and-potential-diagnostics-primary/'
add(14, 'customer-attraction/fixed-complete-policy-potential-increment-separation-and-exact-dual',
    '固定完整策略的调和势增量epigraph分离及逐候选精确对偶', 'algorithm', 'proved',
    '固定三人六主题43有序节点σ，215行Γw<=0、63非空类型w>=0，u·w=1。加P>=0及全部56个三槽势行φ(q′)w<=P，得271×64矩阵A。对每个四槽q最小化c_q x=(u−φ(q),1)x；精确y<=0、α>=0、r=c_q−A^Ty−eα>=0给gap<=−α。原126候选只访问47：前46各全64残差有证，47号q=(0,1,1,0,1,1)有归一正见证33/182；放大91得430单位反PI，未访问79不冒全覆盖。',
    '每个固定σ和指定q的整个真实非负客户锥；有限原报告仅47/126个候选，非所有σ。',
    ['Γ符号为偏离−规定，保持全部真实有序后继', 'epigraph含所有三槽比较', '精确后验乘子和64坐标残差，数值优化仅提案'],
    '可复用势目标分离及对偶保证；有限430单位反例归0007主owner，此算法不复制反例身份。', read_note,
    extra=(13, piroot+'original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/global/pi_fixed_cone_diagnostic.json', piroot+'constraint-index.json', piroot+'check-stored-certificates.py', piroot+'stored-certificates-check.json'))

add(15, ids[3], '极大化过去租金与未来利润的Pareto剪枝丢失最坏根SPE', 'counterexample', 'proved',
    '按每个非根非终端状态的向量v_b(q)=((U_a(q))_(b_a>0),Σ(q_a−b_a)U_a(q))只留逐坐标极大，不能保完整根菜单。正文三固定单位输入A/B/D分别m,p=(4,4),(3,5),(4,5)，最坏W由完整10/11/18升为压缩11/12/21；每例仅一次末位平局删掉较低过去租金的真孩子，祖先门槛随之上升。',
    '上述明确剪枝规则及三精确输入；存在完整SPE被丢，不声称任意压缩都失败。',
    ['向量中每个已占主题利润只列一次不乘背景重数', '相等向量保全部q，根和终端不剪'],
    '否定maximize_all普遍保持最坏根福利；四例均half。', read_note,
    extra=('archives/customer-attraction/tools/evidence/continuation-floor-resumed-boss2/four-pareto-cases-and-floor-consumption.json',))

add(15, ids[4], '极小化过去租金与未来利润的Pareto剪枝也丢失最坏根SPE', 'counterexample', 'proved',
    '三人五主题17单位输入mask重数27:4,29:2,1:2,30:4,25:1,20:2,6:1,14:1，按正文v_b逐坐标极小递归剪枝。完整根E={(0,0,1,0,2),(0,1,0,0,2),(1,0,1,0,1)}，压缩仅留末项，最坏覆盖15升17=OPT；正文五处支配删除与31节点完整SPE证据支撑。',
    '固定17客户输入及minimize_all规则，全部原根可实现终局。',
    ['规则与前条相同但改取极小', '全部有序SPE集合递推及明确五处删除'],
    '与最大方向是不同精确反例，不因租金看起来更坏便可替代祖先支持。', read_note,
    extra=('archives/customer-attraction/tools/evidence/continuation-floor-resumed-boss2/four-pareto-cases-and-floor-consumption.json',))

add(18, ids[5], '任意合法前缀的旧覆盖补偿半覆盖义务', 'conjecture', 'open',
    '固定合法旧有序历史H，旧覆盖C_old，后继k名提供者任取完整纯子SPE，新增覆盖C_new在C_old外，R_k(H)为至多k个目录主题在C_old外最大覆盖。待证或精确反例：2|C_new|+|C_old|>=R_k(H)。old0退化根half；默认old2/k4/p5百样本只有限阴性。',
    '所有有限共同目录、合法H、正后继人数k及每份完整历史纯子SPE；H无须出现在某根SPE上。',
    ['R_k只算旧覆盖外客户，非完整覆盖或剩余利润', '不把默认15计数前缀冒25有序策略枚举'],
    '带固定前缀覆盖补偿的明确开放接口，未由有限29客户保存点闭合。', read_note + '100实例×15前缀查询的有限记录不证明普遍式；保存点余量27不是新节点。')

upload = 'archives/customer-attraction/tools/evidence/continuation-security/history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json'
add(21, 'CA-LAST-FLOOR-ALL-PLAYERS-NO',
    '四人十二主题完整SPE首位低于纯末位最坏BR值theta', 'counterexample', 'proved',
    'theta=min_(n−1主题背景h) max_a Σ_a1/(h_x+1)。四人十二主题26171145单位输入完整1885节点σ，actual(8,4,5,0)，theta6135346，收益(6135345,6135380,6135380,6135371)，W24541476、OPT24541532，故u1=theta−1。22620含self真续局比较及364背景/1365终局精确穷举认证；theta是min纯背景max纯查询，不是真正混合安全值v。',
    '存在一个原单位共同目录完整SPE，否定∀SPE∀玩家u_i>=theta。',
    ['原4095整数重数和全部1885有序节点不取商', 'theta与静态混合minimax安全值区分'],
    '只反逐人theta推广，不反末两位theta或half；2W−OPT24541420>0。', read_note,
    extra=(upload, 'archives/customer-attraction/tools/evidence/current-customer-attraction/original/44ef31ca794614c1c6c0.md', 'archives/customer-attraction/state/资料/上传完整策略与四路微型比较的独立审计合同--资料.md'))

tr = 'archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/'
add(24, 'customer-attraction/early-3227-local-security-certificate',
    '早期3227单位完整策略否定两条一步局部安全值付款', 'counterexample', 'proved',
    '三人六主题22类型3227单位输入完整43节点σ，actual(0,3,4)，收益(888,1041,1021)、W2950、OPT3227。真正静态根v3=8734869174/9663953、根0后v2=906有匹配鞍点。888+2v2−3v3=−111934422/9663953，888+(3/2)v2−(5/2)v3=−122270544/9663953；两一步全称式均假。聚合桥及half余额仍正，113单位后版不同输入不可替换。',
    '固定早期3227输入与完整策略的精确存在反例；两个局部式而非普遍聚合式。',
    ['输入/完整策略/两鞍点精确字节配对', '不同安全值路径下标及2W−OPT双倍口径分清'],
    '一对象合M23输入双审计与M24策略鞍点；独立实现258比较非一般安全值结论。', read_note,
    extra=(23, tr+'local_security_increment_initial_3227_input.json', tr+'local_security_increment_initial_3227_certificate.json', tr+'local_security_increment_initial_3227_independent_audit.json', tr+'local_security_increment_initial_3227_audit.json', tr+'verify_3227_audits.py', tr+'verify_3227_audits.json'))

add(29, 'customer-attraction/insertion-replacement-prefix-profit-and-harmonic-difference',
    '静态后缀替换的前缀利润差及同一位置调和势差', 'lemma', 'proved',
    '任意静态合法叶y，前k位固定、r=m−k可删。总/前/尾客户负载c,b,a，后缀j改T给ΔP_j=Σ_(B_j差T)b/[c(c−1)]−Σ_(T差B_j)b/[c(c+1)]；Σ_jΔP_j=Σ_(x∉T)ab/[c(c−1)]−Σ_(x∈T)(r−a)b/[c(c+1)]，仅非零贡献取分母。Φ(y^(j,T))−Φ(y)=u_T(y删j)−u_j(y)>=ins_T(y)−u_j(y)。同一j同时u_j<ins_T和ΔP_j<=0才给势升且cap不增，PSUM本身无必然负号。',
    '所有m>=1静态profile、0<=k<=m、合法T及j>k；不要求SPE。',
    ['b0贡献忽略，b>0时分母正', 'k0/r0空域按正文处理', '两符号必须同一后缀位置'],
    '静态恒等式；没有修复后真实SPE的符号或预算保证。', read_note)

add(30, 'EMPTY-DILUTION-ENDPOINT-HOMOGENEITY-v1',
    '固定非空完整端点菜单的空查询稀释一阶齐次', 'lemma', 'proved',
    '有限非空固定菜单Z和非负查询核K，合法空主题E满足K(E,Z)=0。F(p)=min_Z E_pK(s,Z)则任意q及0<=ε<=1有F((1−ε)δ_E+εq)=εF(q)。故正预算严格分离可去空查询行；此等式不授权删除由强制空行动产生的端点列。固定原σ全部位置/行动完整m槽端点的自由Q合同不同于自身推送p×p。',
    '任意有限非空菜单、q、ε；齐次部分不需SPE。',
    ['对同一个固定菜单取min', '空查询整行零，非空列域保持'],
    '准确去空行与自由端点合同；一般FM付款仍未证，不借2m−1替完整槽2m。', read_note,
    model_text='有限非空端点菜单上的非负有限核；CAG应用端点由同一完整σ全部(i,t)真实完成、含当前共m槽。')

add(31, ids[6], '含空标签34客户完整SPE的共同实际列救援与强推送分离', 'construction', 'proved',
    '正文13类型34单位三人七标签（含Empty）57节点σ为完整SPE，actual(0,3,4)，u=(29/3,67/6,67/6)，W32、OPT34。actual完整列对七query的K=(27/4,8,33/4,29/4,29/4,17/2,0)，所以同一列cap17/2<根29/3<W/3，FM及Mfull在此例成立。该列逐客户负载支配空根列(6,0,1)。然而X2/Empty混合ε=1/24的三位置自身推送D−G=12ε²−ε=−1/48；自由F=13/48，故强桥失败与自由列救援并存。',
    '这一固定含空标签34客户完整策略及所有query分布；不是六主题43节点旧证书。',
    ['保原57节点动作及全部21带索引端点', '三位置aggregate ε1/24与JSON根局部ε1/10分开'],
    '同一精确fixture分别验证自由Q与强推送差异，不推广一般FM或删全部空强制列。', read_note, extra=(30,))

add(32, 'customer-attraction/finite-credible-endpoint-cap-exact-hinge-penalty',
    '有限可信端点逐叶cap的精确单边铰链罚表示', 'lemma', 'proved',
    '有限E，d,H实值，Ecap={Y:d(Y)<=u}非空，Hcap=max_Ecap H。μ0=max_(d>u)(H−Hcap)_+/(d−u)，无违反列取0，则每μ>=μ0都有max_E[H−μ(d−u)_+]=Hcap。原source每个d<=u时罚逐点零，不能冒成均值cap线性对偶的正μI银行；不在E的reset叶不受此界。',
    '任意上述有限E,d,H,u及μ>=μ0。', ['有限端点且cap可行集非空', '逐叶cap不同于均值cap'],
    '有限精确罚表示，未给输入无关μ上界、可信闭包或六人付款。', read_note,
    model_text='有限带实数收益/影子值的端点集合；应用时端点必须为所指定孩子的完整可信SPE。')

add(35, ids[7], '实际ABB路径的七真实松弛与80角点half充分证书', 'method', 'proved',
    'm=k+l,k>=1,l>=2，实际全叶仅A/B且真实末三位ABB。固定前缀含k−1个A,l−2个B；A改B的真QR孩子与原倒二改T_j的真Y_j保持不同。正文七行g1…g7全客户和非负，其中g5=S+V/m由m次倒二IC与全部m²交叉末BR得。若λ>=0且16个a/b/q/r会员态×五(d,ell)角点满足Σλg<=2·1_(a∨b)−1_(d>0)，则对全部客户求和给2W>=|∪T_j|，任意比较m元组故half。',
    '任意满足真实ABB路径条件的完整SPE及任意m合法比较槽含重复；每(k,l)需本身精确非负乘子证书。',
    ['不是只终局计数，必须实际有序末ABB', 'Q/R和Y_j均原策略真实续局', '80角点是扩大投影域，失败不自动坏游戏'],
    '充分证书机制，不把有限乘子观察外推所有k,l。', read_note)

add(35, 'customer-attraction/tail-ABB-seven-real-slacks-and-finite-rational-certificates',
    '75组指定计数实际ABB路径的精确half乘子证书', 'theorem', 'proved',
    '前条七行机制在l2…8且k1…(2l+1)的保存77个浮点成功提案中，有75组精确非负七乘子通过80角点。唯一未认证两提案k14/l7与k15/l8在(1,1,0,0,d1,ell0)余量分别−90369007/179509219967096535584250、−1/3676928511756562；不否同参数其它系数。故half对这75个(k,l)且实际末ABB的全原模型成立；六人包括(4,2),(3,3),(2,4),(1,5)。',
    '指定75组计数内所有真实ABB完整SPE；不是75个仅单客户游戏或全l无穷族。',
    ['实际ABB机制及正文完整75组有理λ', '所有λ非负和全部80逐类型余量精确成立'],
    '有限参数族的普遍条件定理；浮点false343项没有不可行证书，不赋数学反例状态。', read_note,
    extra=('archives/customer-attraction/tools/evidence/root-ABB-finite-certificates-and-symbolic-failure/README.md',
           'archives/customer-attraction/tools/evidence/root-ABB-finite-certificates-and-symbolic-failure/original/6a747d6aa67a18b5507d-abb_dual_report.json',
           'archives/customer-attraction/tools/evidence/root-ABB-finite-certificates-and-symbolic-failure/original/025e6a711d02643ffc6c-abb_dual.py',
           'archives/customer-attraction/tools/evidence/root-ABB-finite-certificates-and-symbolic-failure/known-helper-audit-001/audit_abb_frozen_records.py'))

add(36, 'customer-attraction/tail-ABB-five-multiplier-rational-candidate-failed-class',
    'ABB特定五乘子有理通式对每个l至少三均有负余量', 'obstruction', 'proved',
    'k=2l+1,m=3l+1的正文五乘子均在l>=2非负，但会员(a,b,q,r,d)=(1,1,1,0,1)余量R(l)=(-18l^4+27l^3+41l²−5l−1)/(162l^5+243l^4+162l³+6l²−12l−1)。分母移l2+u全正，分子移l3+u=−376−974u−688u²−189u³−18u^4，故每实l>=3严格负，l3为−47/7930；l2该类为81/10367>0。其它31类通过不修坏类。',
    '这一特定接触三等式产生的五乘子通式；每实l>=3（尤其所有整数），不声称所有七乘子模板不可行。',
    ['沿真实ABB七行合同使用五个指定行', '完整32会员类不能省唯一坏类'],
    '精确系数模板障碍；单列未必满足SPE，故不反half。', read_note)

add(43, ids[8], '五客户抽象三槽尾菜单否定根尾弱排序推出均匀额外查询平均不超一', 'counterexample', 'proved',
    '四标签，兴趣mask3三单位、mask12两单位；根i0/1/2/3对应尾(1,1),(0,0),(0,3),(0,2)。每列根恰1且每尾>=1，独立均匀根列与均匀query的额外槽均值J=(11/8+13/12)/2=59/48>1。但首列history(0,1)后指定末1得1，改2独享2，因此连末BR都不满足，非SPE。',
    '一个精确整数形式菜单，否定只保根收益cap和尾收益floor的抽象弱平均界。',
    ['均匀根列和均匀query独立', '无真实策略/末BR前提，不升级原模型反例'],
    '精确松弛反例，与额外槽LP静态安全下界及八标签真末BR障碍分立。', read_note,
    model_text='四共同标签五单位客户的形式三槽菜单；仅根cap/尾floor约束，不假设完整SPE。')

# No automatic title-to-Claim conversion: unresolved existing owners below are explicit routes.
rows = []
routes = json.loads((HOME / 'owner-routes.json').read_text())['routes']
route_map = {r['material_index']: r for r in routes}
by_path = {}
for o in objects:
    for rr in [o['body'], *o['evidence']]: by_path.setdefault(rr['path'], []).append(o['object_id'])
for i, m in enumerate(task['materials'], 1):
    owners = list(dict.fromkeys(by_path.get(m['path'], [])))
    if owners:
        disp = 'objects' if any(o['body']['path']==m['path'] for o in objects) else 'attachment'
        reason = f'实读M{i}精确陈述/量词/条件与承重定位，按记录所列对象归属；原成熟证明和必要证据复用，0原程序重跑。'
        if i in route_map: reason += ' 本页另有跨批同义主owner接证路线未闭合，见receipt，不以当前部分owner吞并未接独有证据。'
    elif i == 3:
        disp, reason = 'excluded', '已读全文。短文仅文献导入模型/静态NE与全部SPE量词的边界说明，无自足新数学对象；具体非匿名反桥与一手论文范围由M2及已有LB-PRIORITY-VALID-UTILITY-SPE承载。未冒称新检索或文献不存在性。'
    else:
        disp = 'needs-decision'
        reason = '已读成熟正文的数学与源审计责任；确定是现有/他批主body的独立证明、输入或必要审计，尚待主owner实际接入精确ref。不是数学open阻塞。精确目标/差异/下一步见本批receipt owner_routes。'
    rows.append(dict(m, disposition=disp, object_ids=owners, reason=reason))

batch = dict(schema=2, baseline=task['baseline'], objects=objects, materials=rows, edge_files=[])
batch_path = f'research/registration/batches/{TASK}.json'
(ROOT / batch_path).parent.mkdir(parents=True, exist_ok=True)
(ROOT / batch_path).write_text(json.dumps(batch, ensure_ascii=False, indent=2)+'\n')
receipt = {'batch_file': ref(batch_path), 'assets': [ref(batch_path)],
           'read_scope': {'materials': list(range(1,47)), 'method': read_note,
                          'not_claimed': '大原始数值证书/程序未全文重清洗、未逐句重证；M10完整动作串按原件保留不再算3315节点。'},
           'owner_routes': routes,
           'mathematical_corrections': [{'material_index':8, 'detail':'r1的E双命中系数为负。K/链仍r>=1，非负E改r>=2，r2端点/前缀cohort支付分开。冻结正文不改字节。'}],
           'next_action': 'lead按路线协调原主body作者实接evidence；已DONE主owner用定向增量，不原地覆盖。清楚open对象正常登记。'}
receipt_path = f'research/registration/receipts/{TASK}.json'
(ROOT / receipt_path).parent.mkdir(parents=True, exist_ok=True)
(ROOT / receipt_path).write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'objects':len(objects),'materials':len(rows),'needs_decision':sum(r['disposition']=='needs-decision' for r in rows)},ensure_ascii=False))
