import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[5]
TASK = 'register-ab98f323ad-0068'
HOME = ROOT / 'research/workspaces/p25-register-v2/Boss6/0068'
task = json.loads((ROOT / f'research/operations/p25-register-v2/tasks/{TASK}.json').read_text())['definition']
materials = task['materials']
texts = {i + 1: (ROOT / x['path']).read_text() for i, x in enumerate(materials)}
new_ids = ['M-12c3a90cc0d445e6a14d0a245b56bdf6', 'M-6c00c3f200054a5199b3a60078211e76', 'M-b349be0d16a24aeeb74f3d6be397397a', 'M-fc8efc0f68474ae0a200cf784deb6bc0', 'M-56650e9396ea45c2874ee5abb789537e', 'M-0bbcdaf7c8e2480a826a75480849bc49', 'M-d9045f1b200b4735ba8f46adcd61013c', 'M-c5dcfeb52be64bdbbe96f0d903ab69ee']
(HOME / 'allocated-identities.json').write_text(json.dumps({'command': 'python work.py research new-id --count 8', 'object_ids': new_ids, 'git_or_shared_file_write': False}, ensure_ascii=False, indent=2) + '\n')

MODEL = '有限不同单位客户、有限非空共同标签目录及任意覆盖映射、单位权顺序提供者；完整纯策略保全部合法有序历史，含空覆盖、同覆盖异标签、重复行动、零客户及任意离轨弱平局。每个强制行动后沿同一原策略的真实后继完成，终局客户价值在全部覆盖者间均分；合法非零背景仅算剩余利润时另明示。'
DEF = task['context_plan']['shared_read_refs'][0]
objects = []
by_n = {i: [] for i in texts}

def ref(path, section=None):
    p = ROOT / path
    x = {'path': str(path), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    if section: x['section'] = section
    return x

def primary_id(n):
    return re.search(r'^id:\s*[\"\']?([^\"\'\n]+)', texts[n], re.M).group(1).strip()

def source_refs(n):
    front = texts[n].split('---', 2)[1]
    return list(dict.fromkeys([materials[n-1]['path'], *re.findall(r'source:[^\s\"\',\]]+', front)]))

def linked_evidence(n):
    out = []
    p = ROOT / materials[n-1]['path']
    for s in re.findall(r'\]\(([^)]+)\)', texts[n]):
        s = s.strip('<>').split('#')[0]
        if 'tools/evidence/' not in s: continue
        q = (p.parent / s).resolve()
        if q.is_file() and q.is_relative_to(ROOT): out.append(ref(q.relative_to(ROOT).as_posix()))
    return out

def add(n, title, statement, quantifiers, assumptions=(), scope='', objections='', kind='lemma', truth='proved', oid=None, model=MODEL, support=()):
    oid = oid or primary_id(n)
    evidence = [DEF]
    evidence.extend(linked_evidence(n))
    for j in support:
        evidence.append(materials[j-1]); by_n[j].append(oid)
    seen = set()
    evidence = [r for r in evidence if not (r['path'] in seen or seen.add(r['path'])) and r['path'] != materials[n-1]['path']]
    objects.append({'object_id': oid, 'version': 1, 'title': title, 'kind': kind, 'truth_status': truth,
                    'model': model, 'statement': statement, 'quantifiers': quantifiers,
                    'assumptions': list(assumptions), 'scope': scope or quantifiers,
                    'objections': objections or '本轮实读本页完整数学正文、量词、条件、准确状态及完整论证位置，复用成熟证明；没有重跑原程序、重新清洗大原件或把有限报告推广为全称结论。',
                    'body': materials[n-1], 'evidence': evidence, 'sources': source_refs(n)})
    by_n[n].append(oid)
    return oid

add(1, '末位纯最佳回复平台上的祖先收益严格分离',
    '任意整数M≥1，两不交主题A、B大小2M、M，真实前缀A后末位的全部纯BR收益对(current,ancestor)恰为{(M,M),(M,2M)}。两点分别可扩成完整两人纯SPE，故即使C依此固定状态取任意有限实值，|Δancestor|≤C|Δcurrent|也失败。纯集合仅两点，整纵段属于其凸包。',
    '对每个正整数M存在所述目录和两份完整策略；所否定的是任意有限斜率的普遍局部控制。',
    scope='两人、一个真实可达祖先前缀的纯BR坐标接口；两份策略不是一份σ在同历史随机选择。',
    objections='完整证明在本页“精确原单位模型与纯续局集合”及“排除的有限斜率及仍可用的绝对收入”；原M1/2/7程序只作局部BR检查。W为2M或3M，OPT=3M，不是half或安全值平台的反例。', kind='counterexample')

add(2, '固定正旧背景信用不能普遍加入两倍剩余利润预算',
    '取s≥3整数、m=s²，主题A含m客户并有m−3不交单例，全部历史恒A是完整SPE。实际第一A作旧背景后r=m−1，P=r，旧信用B=m/2，比较剩余利润F_r=2m−2s，且(2P−F_r)/B=4(s−1)/s²→0。因此任何固定c>0的普遍2P≥F_r+cB均失败。',
    '对每c>0存在整数s>max(3,4/c)的合法实际前缀见证。',
    assumptions=['F_r是旧背景下r个比较主题的最大剩余总利润，非含旧人租金的完整覆盖。', '取等需要m−s个不同单例，故精确公式域为s≥3。'],
    scope='固定正系数旧背景信用的加强；不反基本2P≥F_r或half。', kind='counterexample')
add(2, '连续调和延拓替换不能保留log水位原高尾与原缺口信用',
    'φ(L)=Σ_(k≥1)[1/k−1/(k+L)]有φ(0)=0、φ(L+1)−φ(L)=1/(L+1)、φ′(L)<1/L。单客户、根和唯一尾均覆盖、t=1/2、原缺口D=0时，max_(0≤w≤1)[φ(1+w)−tw]的唯一最优w*严格在(0,1)，因而原高尾没有保权1且根返还1/(1+w*)−1/2>0=D。',
    '存在该单客户辅助优化输入，否定用此φ原样替换log而同时保两项合同。',
    scope='辅助目标函数的具体替换障碍；非原SPE策略反例，也不否其他另带预算的连续调和方案。',
    kind='counterexample', oid=new_ids[0])

add(3, '合法背景聚合探针的给定查询精确下界接口',
    '规范集合值solver可按V(q;prefix)=Σ_a(q_a−prefix_a)U_a(q)选最小剩余总利润终局；给定非负归一查询p̂后，对全部r−1静态主题多重集逐行Fraction求min_q M_q·p̂，得到真正v_r(b)的有效下界，毋须浮点LP最优性。若V<r v_low则给聚合候选的分离提案，完整原模型反例尚须展开目标策略并核全有序IC。',
    '任合法整数前缀、r≥1和完整静态矩阵；认证下界要求给定p̂确切非负且和1。',
    assumptions=['LP仅提案p；有理化和归一后的概率合法性须独立核验。', '原源码没有另assert p̂≥0及scale>0，本记录不替它补造检查或成功运行。'],
    scope='可复用的精确下界/反例提案方法；seed7723645、1500结构迭代只是原有限发现域。',
    objections='正文给完整矩阵、最差剩余利润选择及下界证明。当前无该原1500轮完整stdout/阴性JSON，未运行solver/LP/代码，不把历史未反驳当一般聚合定理。', kind='method')

add(5, '联盟保留负载的共同信用精确全参数上界',
    'B=p(1/c−1/d0)_++a(1/d0−1/d)，0≤p≤c、p+a≤d0≤d≤m。固定整数1≤a≤m−1时全部合法负载的最大B恰为2a/(a+1)−a/m，由p=c=1,d0=a+1,d=m取等；a=m时合同迫p=0,d0=d=m，最大值为0。固定四参数最大值在d0=p+a或d0=d端点达到。',
    '任m≥2及所给整数a；最大值量化合法标量负载合同，不量化全部模式的SPE实现。',
    scope='联盟负载代数，不能把单当前者1−1/m cap直接移用。',
    objections='本页“联盟扩展”有完整端点和两情形上界证明。标量sharp未证明同一SPE能同时实现全部负载；m7/a2与a3为22/21、15/14，不是half反例。', oid=new_ids[1])
add(5, '唯一主题完整SPE使精确同枝信用跨深度无归一累计超支',
    '唯一标签A={x}、所有m位恒A是完整SPE，W=OPT=1。每个位置i删全部未来者时p=i−1,c=d=m,a=1,d0=i，精确B_i=K_i=1/i−1/m，故Σ_iB_i=H_m−1；m4为13/12、m6为29/20且随m无界。',
    '任m≥1的同一真实完整SPE，逐深度各使用一次规定删除。',
    scope='排除每深度独立领一份的无条件累计；不排有N/CK容量、内生低尾或停止选择的机制。',
    objections='该例无遗漏，严格低收益阈值W/m或OPT/(2m)下无尾可删；完整代入在“从一条分支到整棵树”。与已有单枝B/K及N/CK主身份区分。', kind='counterexample', oid=new_ids[2])

add(7, '四客户纯孩子凸化与真实父门槛截取严格不交换',
    '两人三标签A={x1,x2},B={x1,x2,y},C={y,z}。真孩子A为AB/AC，根利润分别1和2；孩子B为BB/BC，根利润3/2、5/2；孩子C为CB，根利润3/2，故真实父门槛t=3/2。先纯过滤得到根有序叶AC,BB,BC,CB；先凸A孩子再截期望门槛保半半AB/AC，L=c_y+c_z为3/2，而整个纯根凸包L≥2。增加全部线性可读终局坐标也不修复单一期望IC操作。',
    '存在该四单位客户空根两人游戏；FILTER⊊CLIP，且新增点越出全部纯根结果凸包。',
    scope='原纯SPE类别的非交换障碍；本两人例另有行为混合SPE实现。',
    objections='原正文完整给末位表、真门槛、必要充分拼接及分离证明；原审计6作为证据保81策略/5SPE/3计数。最差纯W3、OPT2=4、混合W7/2，不反half；任意多层凸递推与行为混合菜单等价未证。',
    kind='counterexample', support=(6,))
add(8, '单半空间全部点对表示的递归凸外松弛与纯BI包含',
    '有限非空C及线性半空间v_a≥c，以所有可行原点和跨门槛两点交点组成D，则conv(D)=conv(C)∩{v_a≥c}。用此法从递归relaxed孩子重算Mhat=max_a min v_a并逐行动截取、合凸，准确表示递归有理多面体H；真纯终局向量集E(k)⊆V(k)⊆H(k)，Mhat(k)≤真M(k)，故线性成本最小值是纯BI的合法外松弛下界。',
    '任有限有理生成集；对应固定有限共同目录游戏的每个合法计数背景。',
    assumptions=['保全部跨阈值点对，不以部分抽样或浮点凸包替代。', '门槛由relaxed孩子重算，不声称是真纯M。'],
    scope='精确凸多面体表示方法与包含方向。',
    objections='完整权重极点证明与逆向归纳在§1。一般无损、一般行为混合等价、多项式大小均未证；m4冻结main不能原样产m5JSON，30客户候选本身另归B8主owner。', kind='method')
add(9, '四人真实父筛选的条件纯成本严格高于最优仿射包络',
    '四人四标签10客户(mask1:3,2:1,4:2,7:1,8:2,10:1)，真实根门槛5/2；固定根行动0的真孩子仅(2011,p11/6,W9)和(1111,p10/3,W10)，故纯过滤值P0=10。最优非负乘子包络sup_λ min{9+2λ/3,10−5λ/6}=85/9，于λ=2/3取等，差5/9；匹配凸点权5/9、4/9。',
    '存在这份固定根行动条件菜单；sup遍历全部非负实乘子。',
    scope='条件纯叶过滤与一个仿射下包络的严格弱对偶间隙。',
    objections='完整70计数状态及原340有序历史证据在本页；全根仍有2011、1111，最低W9，不得把条件P0=10说成全根最低福利，亦不是half反例。', kind='counterexample', support=(10,))
add(11, '真实删位支持、偏离菜单及固定查询客户锥的三个静态接口',
    '同一完整σ的实际删位背景D、全部实际前缀真偏离后删当前所得M、全静态背景B满足D⊆M⊆B，故v_m≤c_M≤c_D。固定实例优化Q是有限矩阵min_Q max_query；固定σ、固定p并以W1归一时，Γw≥0、w≥0及每背景t≤ΣpA(w)构成另一个线性锥优化；后二者不能当作同时优化p和w的全局线性程序。',
    '任固定有限完整形式策略、相应非负客户权以及给定查询概率；静态minimax对有限域成立。',
    scope='可复用菜单构造、包含方向及两种不同LP变量合同。',
    objections='正文§1–4有完整矩阵及量词。三原代码浮点输出未精确认证；全大起点cap1/ratio9/10是解析校准，不证明全部300输入或锥上界。', kind='method')

add(18, '旧人总收入可信下包络的末步两倍门槛付款',
    '合法b余r人，V=max补全覆盖，E=min_(y∈R(b))Σ_a b_aU_a(y)，Ψ=V−E。r1时以nmax为最大新增覆盖、nmin为全部末位BR中的最小新增覆盖、M为最佳利润，有V=W(b)+nmax,E=W(b)+nmin−M，故Ψ=nmax−nmin+M≤2M；每个满历史孩子Ψ0，全部末步边付款成立。',
    '任合法有限前缀、任意末位平局及全部合法强制行动。',
    scope='r=1普遍结论；E是旧人总收入最小，不是各旧人最小相加。')
add(18, '旧人银行下包络在两条实际SPE边上严格欠付',
    '既有61客户四人完整SPE实际AAAF，u=(9,9,9,11),W38,OPT61。在空/A/AA/AAA，(V,E,Ψ,M)分别(61,0,61,9),(61,9,52,9),(51,18,33,9),(41,27,14,11)。实际A→AA及AA→AAA两边均有Ψ下降19>2M=18，否定全部状态/全部行动的BANK逐边合同。',
    '存在所述真实可达完整SPE边；精确下包络极值由本页解析证明和成熟完整策略共同支持。',
    scope='逐边银行势加强；累计ΣM38仍足付OPT61，不反MP/half。', kind='counterexample', oid=new_ids[3])
add(18, '银行下包络加入平均新增覆盖仍不能逐边付款',
    'Ψ+=Ψ+N/r、N=min_(y∈R(b))[W(y)−W(b)]。三人15客户星形例全历史恒中心B，根Ψ+=18、M3，首B后Ψ+=10，于是实际首边下降8>2M6。',
    '存在该成熟完整SPE和合法首步；只否定明示的N/r修正。',
    scope='特定新增覆盖修正的严格反例，不否任意非局部信用或half。', kind='counterexample', oid=new_ids[4])

add(20, '额外整数背景、完整根菜单、实际插入的域比较及条件覆盖接口',
    '合法b余r人，面对r整数主题竞争的v_(r+1)(b)、同一策略强制根后的完整r槽菜单Mfull和实际唯一完整叶插入I(z)满足v_(r+1)≤Mfull≤I(z)。若一份m人完整策略在每个实际前缀满足u_i≥v_(r_i+1)(b_i)，前缀嵌入给W≥m v_(m+1)(0)，结合OPT_m≤2m v_(m+1)(0)推出half。',
    '域包含对任固定策略/合法背景；覆盖结论以所述全实际节点逐人前提为条件。',
    assumptions=['静态背景在查询实现前选择；竞争者联合分布可相关。'],
    scope='三种不同静态对手合同的精确比较与条件推导。',
    objections='普遍逐人前提已由银行族否定，不能记open或无条件证明。四保存点中两点有字面负IC/概率不归一，只作为发现资料；两个完整有限单位SPE校准不推广全称。', kind='conditional-interface', truth='conditional')
add(21, '局部uniform-subset价格不能单独推出旧终点HIT命中界',
    '抽象两层非负网络，两层current均标同一角色j，另有未来目标ℓ。首层各1/2送同角色续层和ℓ；次层各1/2在j实际终止和送ℓ。每层满足包含current的二元uniform-subset PRICE，但最终ℓ质量3/4>旧|K|/(1+|K|)=1/2。因PROJ current可续到另一natural context，旧HIT把current∉K终点值取0的归纳不能仅凭PRICE继承。',
    '存在该抽象有限流网络；结论只否定PRICE⇒旧HIT的逻辑推断。',
    scope='非CAG抽象接口诊断；实际coverer约束能否排除此合成仍待另证。',
    objections='本页“PRICE保留与旧HIT归纳停界”给完整网络。不是构造出的客户游戏/SPE反例，局部SD/PROJ/STATIC和有限ancestry组件继续由原owner保留。', kind='counterexample',
    model='带角色标签的有限非负守恒流网络；局部转移属于包含current的uniform-subset凸包。此对象没有断言其能由CAG真实context实现。')
add(22, '同孩子系数cap1不能自动提供逐sender源金额预算',
    '任n≥1、m≥2，目录{A,空}、|A|=n且全历史恒A为完整SPE。actual B=A^m，末位强制空后的V使每旧sender p_j(V)=n/(m−1)，正价q_jm=n/[m(m−1)]、retained e_j=n/m。λ_j=1的旧回推各actual角色恰占n/m且总额W=n、同孩子cap1有效，却每sender λ_jp_j(V)>p_j(B)=n/m。缩λ至(m−1)/m虽满足AMOUNT，末位少收n/m²。',
    '对全部n≥1、m≥2给同一个完整SPE方案；否定旧规则自动蕴含AMOUNT-single。',
    scope='系数归一与金额归一的输入合同严格分离。',
    objections='m1无sender、n0无严格分离；不否所有别的金额方案、AMOUNT→cap2或half。全m解析证明在两节正文，原n7/m1,2,5,17有限脚本未运行。', kind='counterexample')
add(25, '裸最大主题K的根整行加强仅m≤2普遍成立',
    'K=max|T|，最优m索引主题并集O；R1为逐最优索引强制根后沿原σ的根收益和。R1≥OPT−(m−1)K/m在m1、m2成立；每m≥3的成熟笛卡尔银行完整SPE有K3、R1=m²/(m−1)、OPT=3m−2、W2m，所求右侧超R1为[2m(m−2)²−3]/[m(m−1)]>0。标准all-big族取等不能推广此合同。',
    'm≤2量化所有原模型完整SPE及最优索引元组；m≥3逐人数存在真实完整SPE反例。',
    scope='裸K强化的精确人数边界。',
    objections='银行完整控制器为必要依赖，当前无新运行。真ROW/MG余量3+1/(m−1)>0，half余量m+2>0；不能把助手失败判成ROW/MG或half失败。', kind='counterexample')
add(26, '对齐单删的同查询社会边际signed共同池与坏过去修正',
    '固定合法b、原r≥2身份和同一σ，q_i=U_b(z)−U_b(z删i)≥0且Σq_i≤U_b。退款恒等式Σ_(d≠i)u_i(z删d)=r u_i−q_i。同原历史/角色/查询A且全删位对齐时Σ_(d≠i)g_i^d=−rΓ_i+q_i(z_S)−q_i(z_A)。actual路径完整行λ_(i,A)≥0、Σ_Aλ≤1时，signed删位和、查询边际及rΓ共用一次Σq_i(z)付款。离轨不符过去B须扣其退款差，Γ系数为r−|B|；不同删位乘子公共部分是逐行min_d。',
    '任合法外背景、原r身份、每原历史与同一查询；POOL只使用同actual规定叶及每角色完整行质量≤1。',
    assumptions=['物理单删回放必须真正重建同一原历史，任意离轨历史不自动全对齐。', 'g为signed偏离差，不替成逐删位独立max查询。'],
    scope='共同社会边际和完整行乘子的精确付款恒等式；空背景Σq为独占客户数。',
    objections='本页完整给单叶/任意离轨/公共min证明。辅助收益及凹算子另列；未给真实物理r−1人SPE修复或一般覆盖债务非负分解。')
add(26, '保留原身份的单删辅助势与有限人数凹价值删除闭包',
    '辅助树仍有原r个决策身份，收益bar u_i=(r u_i−q_i)/(r−1)，全树偏离差≤q_i(z_S)/(r−1)，任何原规定路径正regret和≤U_b(z)/(r−1)。势(rΦ_b−U_b)/(r−1)产生该收益且为单调凹资源势。一般单调凹f(0)=0在0≤t≤r上，D_rf(t)=[(r−t)f(t)+t f(t−1)]/(r−1)仍单调凹；覆盖核变成D_rf(1)=1、D_rf(t)=r/(r−1)于t≥2，已非单位覆盖核。',
    '任r≥2、固定合法背景与原完整SPE；一般凹算子仅在有限可行域0≤t≤r断言。',
    scope='同r辅助近似激励及资源核闭包，不是物理删掉一名决策者后的原CAG-SPE。',
    objections='完整增量与二阶差证明在辅助全树/一般凹价值两节；r不能在深层重置。一般随机保留扩展已有R6身份，本对象保单删辅助势及明确覆盖类不闭边界。', oid=new_ids[5])
add(27, '任意额外列分布的末位精确税比较与全部非负余量',
    'actual末位背景b、最佳末利u；任额外主题分布Q，M_Q=max_T E_Q K_b(T,A)、τ=Σ b/(b+1)、t_b(A)=Σ_(x∈A)1/[(b+1)(b+2)]，则OPT_m≤mM_Q+τ+E_Qt_b。精确信用为τ+E_Qt_b=W−u/2−D_old−e_Q/2−B_Q/2，三余量均非负；取最优Q值L得OPT_m≤mL+W−u/2。',
    '任m≥1原完整SPE的actual末节点及每个合法Q；末位最佳回复足够该静态推导。',
    scope='静态比较与精确信用；Q不观察查询实现，也不是根m−1槽自由背景。',
    objections='完整逐客户推导及m1/u0边界在第二节。三个把该比较付到2W的助手已被成熟P池族从k6/12/22否定；本记录不把这些假前提复活，其他根账本指针不另授定理。')
add(28, '笛卡尔保旧计划的末位必要条件及真实续局重置差',
    '同人数、客户不交、完整Cartesian辅助目录中，若旧末位τ在某旧历史有正regret，任何在全部联合历史保留τ旧动作的新SPE不可能：末位只改旧坐标且保aux即严格改善。允许旧续局变化时，定义G_i(H,a,b)=u_old(Z^μ(H,a,b))−u_old(Z^τ(h,a))，总偏离增益精确为旧τ强制叶差+G_dev−G_prescribed+aux偏离差。',
    '任旧完整计划τ（无需SPE）、任同人数不交完整Cartesian辅助及全部联合历史；重置等式不预设μ是SPE。',
    scope='保全部旧计划的必要边界与允许变化后的准确账。',
    objections='不排非Cartesian限制、增加响应者或改变旧末位。若规定旧动作也重选，旧regret基点另变；不能由删后退款差省略G差，也没有普遍修复预算。')
add(29, '全部actual位置竞争菜单的固定完整策略锥交替方法',
    '固定完整σ，以各actual位置强制任意合法动作后真完成并删当前位置构成M。给定p时最小化W=c·w，条件Γw≥0,w≥0且每B∈M的E_p f_B(w)≥1；固定w后另解查询安全LP再交替。这是菜单保底归一≥1、非W1或总客户1；精确可行W<m时才分离cap(M)≤W/m。全兴趣型质量m给任意形式σ/p的精确可行点W=m，仅证最小值≤m。',
    '任固定有限完整形式σ和合法混合p；方法分离结论要求恢复精确非负客户、p、全真实IC及所有背景行。',
    scope='实际前缀菜单结构上的两块双线性交替攻击方法。',
    objections='185随机best=m是未更新哨兵，不能说最优=m。原main不产named schema，k4 named多非法历史，全部未重跑；一般共同菜单候选另有主owner。', kind='method', support=(30,))
add(30, '四类型10客户的完整core策略与actual菜单cap取等校准',
    '四不同覆盖类C,A,B,D，客户类型{A}:1、{A,B,D}:1、{C,B}:4、{C,D}:4，m4。全历史取core C的完整策略为SPE：C利润至少2，改A≤2，改B/D以≥1的另一core桶对付≤1的共享桶，别名core等值。actual W8，任删一槽背景3C下全部查询恰2，所以cap2、W/cap4；OPT4=10。',
    '存在该明确整数单位客户输入及完整core策略；也可同覆盖core别名提升。',
    scope='原root_tax浮点named记录邻近的另取精确解析点；不认证原十进制记录或整个固定锥最优。',
    objections='完整全历史证明与全部查询表值在root_tax节。原prefix_balance k4却259六分支处方的格式缺口没有被本校准修复；half余量6。', kind='construction', oid=new_ids[6])
add(31, '十五份地板锥记录共享的单客户完整SPE、矩阵身份和零债',
    '15记录仅initial/trace两型，其余12字段同点。最终mask47唯一一客户、E空，84全部计数前缀各一target，动作始终覆盖该客户，展开259有序节点1554含自身比较构成完整SPE，actual BCCC各1/4、W=OPT₄=1。真实504计数比较去零去重306条63维行，其12Γ整数矩阵与15份289170原float系数逐格转换一致。真正t4=1/4，δ=0；另取q*五非空各1/5，原二进制q不归一，原p/z给Fenchel下界1/4−2^-106。',
    '该固定保存点与全部15记录的全字段/矩阵身份；t4量化完整自由q单纯形。',
    scope='一个精确有限完整SPE与自由分数值/矩阵证书，不是15独立反例或全锥下界。',
    objections='完整闭式动作、target索引、全部矩阵构造与t4双边解析证明在§3–5；原q和z误差不改字节，原浮点−2^-53不是严格负债。新读取只复用既有固定核事件，未重跑原5494570B搜索。', kind='exact-finite-certificate')
add(33, '36客户自由删槽三菜单和游戏的全查询精确最优164/5',
    '三人六标签36客户指定完整SPE actual034、u=(10,12,12),W34,OPT36。全部18真实删槽列有五种静态背景。p*=(0,2/5,2/5,0,0,1/5)给Σ_i min_B F_p=164/5；q1=(2/5,0,0,3/5,0,0),q2=(1/5,4/5,0,0,0,0),q3=e0逐纯查询封顶同值，故整个查询单纯形最大值恰164/5，余量6/5。坏p=(e2+e5)/2正确列和65/2，自身同law推送则69/2>34。',
    '同一个明确单位客户输入、完整43节点策略，优化量化全部p及逐位置独立列混合。',
    scope='受限三菜单和游戏的精确值；p*不是声称真正静态v3的安全最优分布。',
    objections='完整18列、108查询值、SPE五类型证明及匹配有理上下界均在全文；v3=10及一般AFC不同。原作者两入口只复用成熟成功事件，当前未重跑。', kind='exact-finite-certificate', support=(36,))
add(34, '任意自由删槽列混合的激励松弛与跨势精确余额',
    '任完整确定σ（不需SPE）、实际z、任query p及每位置归一q_i，Φ为调和势，Θ=Σ_i E_(B~q_i,T~p)[Φ(V_i(B)+T)−Φ(V_i(B))]。逐列势抵消精确给W−Θ=Σ_i E_B[u_i(z)−u_i(Z_i(B))]+Σ_i E_(B,T)[Φ(Z_i(B))−Φ(V_i(B)+T)]。SPE只令首和E≥0。36客户菜单最优解有Θ164/5,E64/15,R−46/15，总余6/5。',
    '任m≥1、任p和各自q_i；T与当前位置B独立，跨位置B无需相互独立。',
    scope='全列代数余额和负跨项真实例；AFC需E+R合计付款，不要求R单独非负。',
    objections='完整逐列证明在第一节，边界m1/空题/零客户给出；仅有势/SPE未证一般CAG预算。一般open与非CAG22环不混同。', support=(33,))
add(35, '真实后继逐位回放的删槽势望远镜与异分布当前端点',
    '固定actual位置i，独立A,B同law p，B枝后继逐位回放到A枝，每步沿原σ的合法真实IC Γ≥0。D_i(p)−C_i(p)=EΣ_(k>i)Γ+EΣ_(k>i)[Φ(X_k删k)−Φ(X_(k+1)删k)]。最后槽删除差0，i=m两和空，i=m−1恢复单后继非负。若B改law q_i，必须再减[E_p Φ(V_i(A))−E_q Φ(V_i(B))]；自由取最小列不能免费抵消该端点。',
    '任完整纯SPE、每actual位置及任独立查询分布p,q_i，保全部有序回放历史。',
    scope='全参数精确回放恒等式；早位删除差无已证统一符号。',
    objections='本页给完整单步展开、相容端点及同law/独立性各自用途。普通中间势恒等式不另造节点；当前未追加参数扫描。', support=(36,))
add(37, '按被删实际玩家份额降权精保持静态收益与静态NE',
    '固定实际q，删玩家i并对x∈S_i令w_x^-i=w_x(c_x−1)/c_x，其他不变，所有剩余玩家原收益逐项保持、删后W−u_i。若原q为同时行动静态NE，则新叶仍NE：新固定偏离贡献不大于原偏离贡献，规定收益不变。',
    '任有限非负有理客户价值和固定叶；静态NE保持另要求原叶静态NE。',
    scope='同叶份额代数与静态最佳回复。分母只用于被i覆盖客户；可清分母复制为单位客户。',
    objections='偏离后的顺序真实后继和可信子局会变，故不推顺序SPE闭包。条件归纳若有DEL会得n/(n+k−1)锐式，但DEL实际已被同页反例否定。')
add(37, '份额删除不保顺序实际叶且平均最坏续局闭包失败',
    '成熟34客户三人输入中，原SPE q=(0,1,0,0,1,1)首位/最小收益61/6，删首位后原余叶不属于新两人SPE集合（唯一计数为101000）。另原SPE q=(1,1,0,0,1,0),W32，三个份额降权删后最坏两人SPE福利125/6、125/6、70/3，和65>64=(3−1)W。因此保首删/保最小收益者删及平均DEL均失败。',
    '存在同一成熟输入上的两份精确SPE终局；各删后最小值取全部完整两人SPE。',
    scope='顺序可信性及平均闭包的精确反例；有理价值尺度已回到未清分母单位。',
    objections='同页完整定位父审输入与三份删后证书。另两删除可保持，不扩大成每种都失败；三人half未被反。', kind='counterexample', oid=new_ids[7])

# Ownership routes contain exact byte and identity requests. They do not mutate
# the primary objects, which belong to other task authors.
registry = json.loads((ROOT / 'research/registry.json').read_text())
catalog = {o['object_id']: o for o in registry['objects']}
owner_batches = {}
for p in (ROOT / 'research/registration/batches').glob('*.json'):
    if p.name == TASK + '.json': continue
    for o in json.loads(p.read_text()).get('objects', []):
        catalog.setdefault(o['object_id'], o)
        owner_batches.setdefault(o['object_id'], []).append(p.relative_to(ROOT).as_posix())
routes = []
def route(n, ids, reason, section=None, future_body=None, future_id=None):
    for oid in ids or [future_id]:
        owner = catalog.get(oid)
        body = owner['body'] if owner else ref(future_body)
        tasks = []
        for p in (ROOT / 'research/operations/p25-register-v2/tasks').glob('*.json'):
            data = json.loads(p.read_text())
            if any(m['path'] == body['path'] for m in data.get('definition', {}).get('materials', [])):
                tasks.append({'task_id': p.stem, 'owner': data.get('owner'), 'state': data.get('state')})
        routes.append({'material': materials[n-1], 'object_id': oid, 'source_section': section,
                       'primary_body': body, 'owner_batches': owner_batches.get(oid, []), 'owner_tasks': tasks,
                       'status': 'pending-owner-evidence-attachment', 'reason': reason})

route(5, ['customer-attraction/same-branch-deletion-refund-and-old-prefix-positive-loss-sharp-common-credit','M-8f450a7d41594d05a1ece6d4856d54c6'], '根CLAIMS/FAILED_ROUTES完整保B/K与N/CK，补主owner实接；联盟与重入本批分立。')
for n in [3,4]: route(n, ['customer-attraction/old-prefix-residual-new-coverage-and-same-branch-refund-contracts'], '本源攻击的是更强合法背景V≥r v_r；Hres主稿§更强背景聚合的条件关系精确说明该充分桥，补两不同有限探针的证据范围，不把根零背景强聚合等价对象混成同量词。')
route(8, ['B8-PURE-MENU-CONVEX-CUT-NO-v1'], '30客户候选和最终证书完全同输入坐标；补m4生产者不能原样产m5的版本断点。', '5. 候选本身的精确分离及其最终证明身份')
route(10, ['CA-UNIFORM-ACTUAL-DELETION-CAP-NO'], '补原353锚定图和规范1555图560动作差，分别完整IC及126/125；同actual不等于同策略。', '5. 对原保存图的固定有理核验及不同身份')
for n in [12,13]: route(n, ['cag-exact-same-topic-threshold-promise-slices-and-retroactive-rent','M-c485c6216694439490afcca241cb9038','M-fdc2946fae794567a71e1f984863c0aa'], '分别补886查询/300历史报告和630输入/35598单坐标断言；不并计数或互借事件；终端预算数学仍open。')
route(14, ['customer-attraction/truncated-intersection-moments-full-payoff-and-boolean-positivity','M-37b7d7de813c4ff69c63fcb679950f36'], '13639B实现与13字段原报告的两键版本差；精确矩表示与Boolean正性有限伴随证据。')
route(15, ['M-92acf65e22574d9fa859015f9ec38dac'], '九给定完整策略381项H有理诊断；原程序未assert普遍PW，保open。')
route(16, ['customer-attraction/cross-population-static-cce-mean-welfare-bridge'], 'security README的PC旧探索/后银行新任务分段；有限报告未精确认证CCE。')
route(17, ['customer-attraction/cross-population-static-cce-mean-welfare-bridge'], '补真正占用LP、九全部浮点标量和51原支持；无有理化/残差/原SPE复验。')
route(19, ['customer-attraction/query-entry-above-own-forced-payoff-potential-order-counterexample'], '270精确packet/43节点215非自身IC/36K完整绑定。其余五浮点点不借此认证。')
route(21, ['customer-attraction/joint-column-capacity-and-positive-tax-preserving-reverse-split','M-b29430314bce490aa4c60a00b48a7430','customer-attraction/common-coverer-request-density-projection-and-static-column-deficit','M-57cc29d007474699abddc1bc2a9ab543','customer-attraction/prefix-request-pushback-monotone-prices-and-ancestry-normalization'], '五稿完整域、SD符号、保P_B反向分裂、COMMON/STATIC/PROJ及ancestry的审查先验；本批抽象HIT逻辑反例分立。')
route(23, ['customer-attraction/source-preserving-client-flow-initialization-and-context-density'], 'R65 fresh INV/INIT/EDGE的PREFIX-DENSITY是一般SOURCE定理严格特化；保逐receiver非同角色cap的边界。')
route(24, ['R6-ERASURE-JOINT-v1','R6-ERASURE-NESTING-v1','R6-ERASURE-LOSS-POTENTIAL-v1'], '补两原实现有限参数、不同计数/核族、root仅端点和两次exact-byte成熟事件；不重授全阶定理。')
route(32, ['AFC-ANON-POTENTIAL-v0','customer-attraction/anonymous-marginal-potential-free-column-deficit-and-concavification'], '仅原始未凹化C22完整507历史/11154比较，stdout语义同冻结而非字节同；不倒填DR凹化。')
route(36, ['customer-attraction/six-label-group-policy-single-query-signed-potential-free-column-certificate'], '9IC+3MENU的80坐标精确非负势恒等式；仅固定p，完整程序与零余项证书。')
route(38, ['customer-attraction/finite-layer-anonymous-potential-cardinality-concavification','customer-attraction/anonymous-marginal-potential-free-column-deficit-and-concavification'], '固定C22/M21/L43的独立定义级有理核，完整凹化报告2564B逐字节同；一般L/M存在性依解析主定理。')
for n in [34,35,36]: route(n, ['customer-attraction/actual-position-aggregate-free-column-budget'], 'AFC精确未付义务/自由列原发现与完整证据；不从程序另立略异主候选。')
for n in [29,30]: route(n, [], '共同菜单主稿归0002/Boss2；补actual菜单策略锥/185哨兵行及named版本界，数学open非身份争议。', future_body='archives/customer-attraction/state/候选/全部实际节点真实竞争菜单的共同混合--候选.md', future_id='cag-all-actual-node-real-competition-menu-mixture')
route(16, [], '后银行势最大新增计数SPE可实现及连续前缀低菜单工具归0007/Boss1；不是前安全探索一般桥。', future_body='archives/customer-attraction/state/定理/不交资源的势最大计数与银行可信低退出--定理.md', future_id='customer-attraction/singleton-resource-potential-maximizer-spe-implementation-and-bank-exit')

# Whole-file refs retain all supporting steps, including mature complete SPE
# proofs or finite input/certificate files outside the primary body.
extra = {
    3: ['archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md'],
    18: ['archives/customer-attraction/state/反例/四人实际根总税--反例.md', 'archives/customer-attraction/state/反例/首步机会成本税桥--反例.md'],
    20: ['archives/customer-attraction/state/引理/合法前缀的静态额外槽预算与条件归约--引理.md', 'archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md'],
    25: ['archives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md', 'archives/customer-attraction/state/引理/单后继去相关恒等式--引理.md'],
    29: ['archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md'],
    31: ['archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/replay/exact-review.json', 'archives/customer-attraction/tools/evidence/fifteen-fractional-floor-cone-records-boss3/replay/complete-exact-ledger.json.gz'],
    33: ['archives/customer-attraction/state/障碍/自适应后继与真实菜单安全值--障碍.md'],
    37: ['archives/customer-attraction/tools/evidence/boss5-parent-resume-primary/original/f7c463370d24081cd537/audit_share_deletion.py', 'archives/customer-attraction/tools/evidence/boss5-parent-resume-primary/original/8df67c3df81f28a815b5/audit_share_deletion.json', 'archives/customer-attraction/tools/evidence/boss5-parent-resume-primary/replay-tree/examples/customer_attraction/individual_security_failure.json', 'archives/customer-attraction/state/审查/五人前缀账本与父审程序的恢复核对--审查.md'],
}
for n, paths in extra.items():
    for o in objects:
        if o['body']['path'] != materials[n-1]['path']: continue
        have = {x['path'] for x in o['evidence']}
        for path in paths:
            if path not in have: o['evidence'].append(ref(path)); have.add(path)

(HOME / 'owner-routes.json').write_text(json.dumps({'task_id': TASK, 'routes': routes}, ensure_ascii=False, indent=2) + '\n')
rows = []
for n, m in enumerate(materials, 1):
    local = list(dict.fromkeys(by_n[n]))
    pending = [x for x in routes if x['material']['path'] == m['path']]
    if local:
        disposition = 'objects' if any(o['body']['path'] == m['path'] for o in objects) else 'attachment'
        reason = '完整读取成熟正文，模型/量词/条件及证明位置按本批独立对象保留；未重新清洗原大文件或重跑成熟程序。'
        if pending: reason += ' 同页另有已定位跨批主owner待实接，准确请求见0068/owner-routes.json；当前object_ids仅列已闭合本批owner，不假称外部evidence已接。'
        ids = local
    else:
        disposition = 'needs-decision'
        ids = [x['object_id'] for x in pending if x['object_id'] in catalog]
        reason = '数学及来源已辨清，待主owner实接本材料精确evidence后改attachment；不是数学open的needs-decision。详见0068/owner-routes.json。' if pending else '完整读取，为既有数学对象补充来源/程序证据；具体主owner仍待准确主记录路由，不为日志/计数新造节点。'
    rows.append({**m, 'disposition': disposition, 'object_ids': ids, 'reason': reason})
batch = {'schema': 2, 'objects': objects, 'materials': rows, 'edge_files': []}
batch_path = f'research/registration/batches/{TASK}.json'
(ROOT / batch_path).write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n')
receipt = {'task_id': TASK, 'batch_file': ref(batch_path), 'assets': [ref(batch_path), ref((HOME/'owner-routes.json').relative_to(ROOT).as_posix()), ref((HOME/'allocated-identities.json').relative_to(ROOT).as_posix())],
           'reading': {'formal_materials': len(materials), 'shared_definition_files': 2, 'scope': '完整实读38篇成熟正式正文的数学陈述、模型量词、条件、解析论证和证据位置；完整读两共享定义。原大JSON/代码/运行证书只定位并复用成熟正文所给范围，本次未重新清洗或重跑，未把它们冒作当前全文重审。', 'mathematical_executions': 0},
           'status': 'draft-mathematics-complete-pending-cross-batch-owner-attachments',
           'counts': {'objects': len(objects), 'materials': len(rows), 'owner_routes': len(routes), 'needs_decision_materials': sum(x['disposition']=='needs-decision' for x in rows)},
           'validation': {'pending': 'Run local exact structure/SHA/body/owner validation after writer; publish/checkpoint/done only by Boss.'}}
(ROOT / f'research/registration/receipts/{TASK}.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt['counts'], ensure_ascii=False))
