"""0055 exact registration draft. No registry, task-state or Git writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HOME = ROOT / 'research/registration/Boss2/0055'
TASK = json.loads((ROOT / 'research/operations/p25-register-v2/tasks/register-ab98f323ad-0055.json').read_text())['definition']
M = TASK['materials']
IDS = json.loads((HOME / 'id-allocation.json').read_text())['allocation']
MODEL = '有限不同单位客户、有限非空共同标签目录及任意覆盖映射，单位提供者按全部有序历史各行动一次；终局每客户在覆盖者间均分。完整纯SPE含全部离轨历史、真实改变后续局与任意弱平局，允许空覆盖、同覆盖异标签、重复选择及零客户。'
READ = '本次分段实读全部33正式正文和两共享定义，核精确陈述、模型量词、条件、纠错与完整理由位置；成熟证明按正文复用，未重跑原程序、扫描、LP或SPE审计。'
OBJS = []

def ref(x, section=None):
    p = M[x-1]['path'] if isinstance(x, int) else x
    z = {'path': p, 'sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
    if section:
        hs = [s.lstrip('#').strip() for s in (ROOT / p).read_text().splitlines() if s.startswith('#')]
        assert hs.count(section) == 1, (p, section)
        z['section'] = section
    return z

DEF = TASK['context_plan']['shared_read_refs'][0]

def add(key, title, kind, status, body, statement, quantifiers, assumptions, scope, objections, evidence=(), model=MODEL):
    br = ref(body)
    ev = [DEF] + [ref(x) if not isinstance(x, dict) else x for x in evidence]
    ev = list({json.dumps(x, sort_keys=True): x for x in ev if x != br}.values())
    OBJS.append({'object_id': IDS[key], 'version': 1, 'title': title, 'kind': kind,
                 'truth_status': status, 'model': model, 'statement': statement,
                 'quantifiers': quantifiers, 'assumptions': assumptions, 'scope': scope,
                 'objections': objections + ' ' + READ, 'body': br, 'evidence': ev,
                 'sources': [br['path']]})

add('static_lb', '安全最优两独立查询的共同静态首对下界P≥2v', 'lemma', 'proved', 1,
    '合法整数背景b、余r≥2，v_r(b)=max_p min_C E_p f_{b,C}，M_r(b)为全部安全最优查询。对p∈M，令A,A′独立抽p，P_r(b;p)=min_{B∈S^(r−2)}E[f_{b,B+A′}(A)+f_{b,B+A}(A′)]，则P_r(b;p)≥2v_r(b)。固定B、A′后B+A′是合法静态竞争元组，两项分别用安全最优性。',
    '任意有限实例、任意合法沉没整数前缀、每个r≥2及每个安全最优p；B可依p但不可观察两查询实现。',
    ['两查询独立同分布；共同B为固定静态r−2槽，r2为空元组。'],
    '精确静态接口，不是原SPE实际首两收益的付款证明。',
    '若B观察查询而适应反应已换量词。任意合法背景的动态存在付款已被PB反例否定；实际前缀与零根弱化另开放。')

add('p_concavity', '首对iid查询P的逐客户凹式与安全最优面极点最低点', 'lemma', 'proved', 1,
    '固定B，令t_x=Σ_(A∋x)p_A、d_x=b_x+c_x(B)+1，则客户x的两查询总贡献为2t_x/d_x−2t_x²/[d_x(d_x+1)]。故每个P_B(p)凹，P=min_B P_B连续且凹；在非空紧多面体M_r(b)上，min P由某个极点达到。',
    '任意合法背景与r≥2、全部p∈Δ(S)；极点最低点针对整个恰安全最优面。',
    ['非负单位客户；有限目录与有限静态背景集合。'],
    '允许穷尽最优面顶点检验存在付款，未给多项式时间或有限随机采样充分性。',
    '一加四个随机方向解只采容差放松面，非全部恰极点；浮点采样正gap不足反存在量词。', [2, 9])

add('arbitrary_optimal_p_no', '两人不交L2与S1反每个安全最优p均支付P', 'counterexample', 'proved', 1,
    '两人、互不交L含2客户及S含1客户；根L，L后末L、S后末L为完整纯SPE，W=u1+u2=2。v2=1，安全最优面p(L)=α∈[1/3,1]，P2=1+4α−3α²；α=2/3给7/3>2，严格否定每个安全最优p可由实际首对支付。两个端点α=1/3、1均给P2=2。',
    '存在该明示三客户完整两人SPE及安全最优p；不是对所有安全最优p的失败。',
    ['目录恰L、S；所给完整三个决策节点保弱平局。'],
    '每个安全最优p的付款全称失败；同例仍存在可支付p，保留存在/任意差别。',
    '不否定两人存在付款、W≥2v2或half。精确最优面和P多项式均在正文解析给出。', [2])

add('actual_prefix_p_open', '实际前缀首对收益存在安全最优iid查询付款的开放接口', 'obligation', 'open', 1,
    '给零根一份完整纯SPEσ，在其任一实际合法前缀h后余r≥2，b为真实沉没负载，s为同一σ真实首两位最终收益和；要求存在p∈M_r(b)使s≥P_r(b;p)。零根版本是子域，两人零根等价min_(p∈M2)P2(p)≤min_σW(σ)。若实际各前缀均付款，静态P≥2v及安全值嵌入沿相邻对给W≥m v_m(0)。',
    '候选为每个零根完整SPE、每个实际前缀，存在可依该前缀与σ的安全最优p；非任意合法离轨背景。',
    ['s来自同一份完整策略的真实相邻首两位；p的安全最优面针对该r,b。'],
    '清楚的数学open，正常登记；两人/零根弱化未由有限扫描解决。',
    '全合法背景的更强版本已由PB-extra严格反驳且该特定PB背景实际不可达，不能把它当本候选反例。两人任意最优p版本另有精确失败。1798仅最后已处理非零样本索引加一，非成功最优面实例数；9000为六配置顺序条目，无全称推断。', [2, 3, 4])

add('first_pair_menu', '精确可信终局集合中锁定同一策略首两动作的兼容判据', 'algorithm', 'proved', 3,
    '固定计数过去k、余r≥2，用整数收益pay=L U及全部子SPE可实现终局集合R_z，H_z=max_a min_(i∈R_(z+e_a))pay(q_i,a)。存在一份完整子SPE以有序a,b开头并到q_i，当且仅当i∈R0∩R_ea∩R_(ea+eb)、pay(q_i,a)≥H0、pay(q_i,b)≥H_ea。先在两行动孩子实现目标，再逐层以离轨可信最小收益孩子拼合；全部满足判据者首对和取最小即全部完整子SPE的真实首对最小值。',
    '每个有限整数输入与合法过去、每个有序a,b（允许相等）及每个终局索引i；精确算术且R为全部可信终局集。',
    ['L=lcm(1,…,m)；实现若用int64须遵守正文m≤6、p≤6、w≤100无溢出界，任意规模需任意精度。'],
    '缓存可实现集合不限制同计数有序历史共用行动；不等于报告已经存完整有序策略。',
    'R递推复用CA-EXACT-PURE-SPE-ALL，独有内容是同一策略指定前两动作的两层兼容及首对精确最小化。原六float安全LP与ratio仍仅有限探索。', [2,
       'archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md',
       'archives/customer-attraction/state/算法/可信续局菜单与完整策略重构--算法.md'])

add('pair_cone_method', '固定完整策略全类型锥的真实首对安全值精确接受合同', 'method', 'conditional', 8,
    '固定全有序形式策略σ，Γ为每节点规定动作减真实偏离续局收益行，c为实际覆盖、d为同一实际叶首两收益行。对固定查询q及全部静态r−1竞争背景，求w≥0、Γw≥0、c·w=1、0≤t≤β_B(q)w，目标min(d·w−2t)。任一精确有理可行负目标给同σ的首对s<2t≤2v_r(w)，清分母即单位客户严格反例；不需q安全最优。合法整数过去可同样加在分母；背景pair归一为1的实现使用相应齐次比值。',
    '任意固定有限完整σ、合法背景、固定概率q与满足全部行的精确可行点；原71结果只为n3/4/5零背景。',
    ['所有有序真实IC；全部合法静态竞争元组；概率q与非负有理质量精确验收。'],
    '条件在于精确可行验收，推导完整；局部交替方法无全局最优或全σ支持保证。',
    '原71浮点margin近零不构成精确下界；五查询起点各最多八轮，security_floor仅锥步t。全兴趣零点只给最优目标≤0。原默认极小续局采样遗漏合法非极小完整策略；不证一般pair、聚合或half。', [4, 3,
       'archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md'])

add('p_fixed_saddle_method', '固定首对形式策略及指定pQ安全鞍点的P线性攻击', 'method', 'conditional', 9,
    '三人六标签完整034形式策略，63非空类型质量w≥0、Γw≥0、首对收益=1；固定p=(10,10,21,10,10,21)/82与Q在01/02/12/34/35/45取(23,9,9,23,9,9)/82。所有21竞争对给β_B(p)w≥v，六纯query给cap_a(Q)w≤v，故精确可行时pQ为新质量的真安全鞍点。再对六个共同B槽要求P_B(p;w)≥s并max s，是保持该σ,pQ的首对P攻击LP。',
    '针对该固定σ及该指定有理pQ，对全部63非空类型、21安全背景和六查询/六共同B槽。',
    ['全部真实IC、pQ匹配上下界与首对归一；结论仅对精确可行点。'],
    '固定安全鞍点截面的方法；浮点784B报告仅有限探索。',
    '即使s>1也只反指定p，未排整个安全最优面就不反存在p。打印mask63=3/2的解析点使所有p最优、pair=P=1、v=1/2；rank2不继承原34唯一性；缺精确对偶故不证LP精确最优1。', [1])

add('frozen_q_calculus', '全主题冻结匹配查询的修正恒等式与均匀排列期望', 'lemma', 'proved', 5,
    '固定实际m槽S和比较m槽T（保重复出现），负载c_x及比较重数k_x；A=Σ_x k_x/(c_x+1)，D=Σ_(c=0)k_x。冻结删实际槽再插比较题的Q(π)=A+B(π)，修正每次覆盖匹配为1/[c_x(c_x+1)]，均匀π给E B=(A−D)/m，故min Q≤((m+1)A−D)/m。',
    '任意m≥1、任意合法实际/比较元组与全部槽排列，不要求这些元组或策略最优。',
    ['Q冻结其他实际覆盖者，比较出现重复收费；A与D按出现次数计算。'],
    '纯静态恒等式；若特定最优元组A≤W+D/(m+1)则minQ≤(1+1/m)W，只是条件推论。',
    '不将冻结Q改成真实偏离V，未证普遍A≤W或相应客户补账；52客户minQ48>W47且PFR反例不损此恒等式。')

add('partition_r_calculus', '最便宜owner一次收费分区的超几何冻结公式', 'lemma', 'proved', 5,
    '给比较并集O、实际并集C，固定槽排列π后每客户选最便宜eligible比较出现作为owner；其最小分区费R=|O∖C|+Σ_(x∈O∩C){1/(c_x+1)+I[全部k_x个比较出现均落入覆盖x的实际槽]/[c_x(c_x+1)]}。均匀排列将指标换成binom(c_x,k_x)/binom(m,k_x)，k_x>c_x时为0，得精确E R。',
    '所有有限实际/比较m槽及排列，比较客户只计一次；owner块不必是合法目录行动。',
    ['每客户无跨客户容量约束；任意合法分区或分数owner都不低于逐客户最小值。'],
    '冻结一次收费恒等式，与重复收费Q及真实后继V分立。',
    '普遍存在最优元组、匹配与owner使R≤W的PFR已被14客户严格否定。若额外子类确有该前提，仍给OPT≤(2−1/m)W和终局税条件推论，非一般付款。')

add('partition52_dual', '指定52客户策略锥的固定最优比较与分区匹配有理证书', 'certificate', 'proved', 5,
    '固定正文52客户形式策略、target=(0,1,4,5)、actual=(3,3,2,2)，匹配(4,5,0,1)；对所有使该完整策略为SPE并使target弱最优的非负类型重数，R_(4,5,0,1)≤(281295/345586)W。正文以有理非负乘子及全部63类型residual≥0证明该固定锥上界。原52点W47、minQ48、minR263/12。',
    '该固定完整策略、固定target/匹配的全部非负类型质量；原52客户只是其中明示输入。',
    ['全部真实有序IC；target弱最优条件；证书系数/方向按原有理JSON。'],
    '精确固定锥证书，不是所有策略或全目录PFR定理。',
    '63残差检查支撑所列恒等分解；有限阴性策略搜索不扩大证书域。',
    ['archives/customer-attraction/tools/evidence/weak-partitioned-matching/original/4de448732e82990e2003.source',
     'archives/customer-attraction/tools/evidence/weak-partitioned-matching/original/12b564ff9623f5637894.source',
     'archives/customer-attraction/tools/evidence/weak-matching-cone-attack-20261031/source/dependencies/static_matching_counterexample.json',
     'archives/customer-attraction/tools/evidence/strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py',
     'archives/customer-attraction/state/反例/最优组合冻结匹配的一单位缺口--反例.md'])

add('optimal_addition127_no', '127客户唯一最优并集的新增槽查询费72严格超过W71', 'counterexample', 'proved', 6,
    '两人六互异主题0…5，正文15正兴趣型共127单位客户；根0，末位对0…5回复(1,4,4,5,5,4)，全部七节点真实IC成立，实际0,1利润(34,37)、W71。唯一最优无序支持{2,3}且二者不交各44、OPT88；其并集含56实际遗漏及32实际已覆盖客户，实际已覆盖负载皆1，所以不删除实际覆盖者的并集添加查询A=Σ_(x∈T2∪T3)1/(1+c_x)=56+32/2=72>71。',
    '存在该固定127单位客户完整SPE，全部最优两槽组合均是2,3两种顺序并具有相同严格添加费。',
    ['客户类型与完整七节点策略按两规模原审计；比较并集一次收费，不按主题重数重复。'],
    '否定存在某最优并集使新增槽添加查询≤W的普遍桥；不是PFR9>8的同一计价，也不是half反例。',
    '同输入PFR最小费80>71为既有PFR反例主owner的独立较大见证；14客户添加费8=W不反本桥，127有独立必要数学。2W−OPT54、全终局税71/2仍满足相应弱预算。', [7,
      'archives/customer-attraction/tools/evidence/menu-partition-eight-boss3/original/exact_witness.json'])

add('fixed_rank_no_constant', '固定真正离轨次数的全真实偏离截断不支持人数无关福利常数', 'obstruction', 'proved', 12,
    '每固定整数k≥0，M=2^k，任意m取L=lcm(1,…,ceil(m/M))，两两不交A_i大小L/ceil((m−i+1)/M)、B_j大小L。正文完整计划重置策略在所有真正离轨次数Dσ(h)≤k节点满足全部真实当前偏离IC，但actual W=LΣ_(r=1)^m1/ceil(r/M)，OPT=mL，固定k时OPT/W→∞。因此这些截断行及非负客户不能推出任何预先固定有限C的OPT≤CW。',
    '每个先固定k与有限C>0，存在足够大m及全部有序历史上有定义的形式策略；只保证Dσ(h)≤k的节点IC。',
    ['偏离次数按当时原策略规定行动逐步回放；每次再次偏离都重置同一完整形式策略，不冻结尾。'],
    '截断证书障碍；坏福利点明确不是SPE，不反原模型half或固定六人全部行。',
    '本族首次OPT>2W为m0=4M+floor(5M/18)+1；历史B1…B_(k+1)后的省略节点改新B严格盈利，证明非SPE。原8352节点/92500比较与210000循环项仅有限实现，k≥m−1覆盖全树的小例W=OPT。', [11])

add('terminal_envelope_method', '固定完整策略的纯末位税包络线性客户锥合同', 'method', 'proved', 14,
    '固定完整标签策略σ，非负全非空类型质量x，保全部非self真实IC并令actual W(x)=1。末位IC保证每个代表背景指定σ(h)均为BR；因此E(h)=m f_h(σ(h))+τ(h)是线性，E*=min_h E(h)，只需每个m−1计数背景的一份有序代表。自由ε满足ε≤E(h)−2W，max ε精确等于该σ锥的max(E*−2W)/W。非selfIC=p^m−1，包络背景binom(p+m−2,m−1)。全兴趣一客户点使所有IC等号且ε=−1/m，故仅给最优值下界。',
    '任意m,p≥1及每份完整合法标签动作表；精确优化合同适用其非负客户锥正W截面。',
    ['全部有序末位IC保留才能合法压缩静态背景；没有将策略合为计数函数。'],
    '纯E*发现与精确接受方法；OPT≤E_mix≤E*不逆向给half反例。',
    '正精确ε只反纯包络付款；负浮点最优不是全锥精确上界。原12随机/7known/12fresh各批不同；同覆盖退化点依当前标签模型合法，历史旧集合域说明不擅扩大其它结果。', [13, 15, 16])

add('terminal_envelope2_exact', '五标签两人固定策略的纯税包络精确最大值−1/2', 'certificate', 'proved', 16,
    '固定m2/p5完整σ：根2，σ(0…4)=(2,2,1,2,2)。W为主题1、2并集质量，在σ完整IC客户锥中，(2/3)E(1)+(1/3)E(2)=(3/2)W−(1/2)Σ_(s:1∈s,2∉s)x_s≤3W/2，故E*≤3W/2；单客户mask14={1,2,3}使σ全部IC成立、W1、E*=3/2，达到max(E*−2W)/W=−1/2。',
    '这份明示五标签、六决策节点策略的全部非负31类型质量（W>0），不是所有两人或五人策略。',
    ['σ(1)=2、σ(2)=1是整个锥内BR，由完整末位IC承担。'],
    '精确固定标签锥原始/对偶最优；原86客户重构输入仅用于取得该σ。',
    '单客户达到点标签1/2/3同覆盖，0/4同为空；上界亦限制覆盖互异子域，但不声称该子域同σ能达到。原29×32矩阵及1022标量精确核来自一次已有事件，未新求解。', [14,
      'archives/customer-attraction/tools/evidence/terminal-envelope-cone-program/replay/complete-policy.json',
      'archives/customer-attraction/tools/evidence/terminal-envelope-cone-program/exact/exact-small-cone.json'])

add('common_pivot_rows', '五索引共同T枢轴跨三末菜单的十二条对齐与去对角必要行', 'lemma', 'proved', 18,
    '三路径前缀P^r=(ABC,AEU,ABE)，L_i^r为真实(P^r,T_i)末回复。固定客户p为P^r负载，d=Σt_i、ell_r=Σl_i^r、h_r=Σt_i l_i^r。每个r≠s的同索引slack D_rs=(ell_r−ell_s)/(p+1)−(h_r−h_s)/[(p+1)(p+2)]≥0；全积A_rs=5(ell_r−ell_s)/(p+1)+(d ell_s−5h_r)/[(p+1)(p+2)]，异索引E_rs=A_rs−D_rs≥0。非负性各自由固定完整主题真末位IC再求和，六有序(r,s)共十二必要行。',
    '每份五人完整纯SPE、任意五个可重复合法比较T_i、三份指定真实末菜单；slack在所有真实客户上求和。',
    ['共享T位；ell/h为整索引统计；p≥0，分母恒正。'],
    '必要行可在旧十会员位与三族直方图、ell/h坐标上计算，不需未知跨菜单dot。',
    'E不是由两个非负总式相减证明，须独立对i≠j真实比较求和；不能每客户选择不同好索引。只保A会丢D/E，780系数核验是已有有限实现。', [
      'archives/customer-attraction/tools/evidence/common-pivot-sixty-five-primary/related/common_pivot_rows.py'])

add('pivot2408_obstruction', '65候选的2408必要行仍有O>2W精确非负质量点', 'obstruction', 'proved', 18,
    '原65候选上存在38正、27零有理质量x，W1，全部旧2396行加十二common-pivot行同时非负，恰44零。O=544240830471476968327361388331326738442/268090293203751329886827971068655403225，O−2=8060244063974308553705446194015931992/268090293203751329886827971068655403225>0。因此这套2408必要行与非负质量不能推出O≤2W。',
    '存在该完整65有理向量，对所列全部2408行全称成立；不是所有合法原子域的LP最优。',
    ['新质量取精确point/mass，旧mass_numerator仅来源元数据；O只为五比较主题形式并集。'],
    '固定必要系统的精确障碍；非五人完整SPE反例或真实OPT，未恢复精确dual。',
    '与2396点同38支持位置但质量不同；旧D21负分数不排此新点，D21在新点0。完整共同目录/有序历史一致性、根真实四人后继仍未编码。五人half另已证明，不能借本点否定。', [
      'archives/customer-attraction/tools/evidence/common-pivot-sixty-five-primary/new-exact-event/new_exact_2408_point.json'])

add('bank_signed', '完整Cartesian银行联合偏离的有符号余额与κρ振幅预算', 'lemma', 'proved', 22,
    '主/银行客户不交且目录完整Cartesian，任意跨坐标完整SPE实际第i前缀，V_i(a,b)为强制当前联合动作后的真实主收益，r_i余人数、p^i银行过去负载；K_i=max_bΣ_(x∈b)1/(p_x^i+r_i)。R_i=max_a min_b V_i(a,b)−u_i^M≤u_i^B−K_i，K_i≥L/m，故ΣR≤W_B−ΣK≤W_B−L。κ_i=u_i^M−min_bV_i(A_i,b)≥0，Σ(R_i)+≤W_B−ΣK+Σκ；保持实际B的d_i=max_aV_i(a,B_i)−u_i^M≥0，对最佳a中最小ρ_i=V_i(a,B_i)−min_bV_i(a,b)，有Σd≤W_B−ΣK+Σρ。',
    '每个m≥1、每份完整Cartesian SPE及同一条actual路径；R的子集求和式亦成立。',
    ['所有动作对合法；偏离沿同一σ真实完成；不假设两坐标投影SPE或V独立银行动作。'],
    'signed/正部/通常主菜单差是三种不同预算，均保显式振幅。',
    'R可负，正文五客户两人完整20行例R1=−1、κ1=ρ1=1、d1=0；不能丢负R或未证明Σρ/Σκ付款，不得跨互斥离轨树累加银行福利。', [20, 23])

add('bank_capital', '完整Cartesian银行的最低资本与提前遗漏最大主题扣款', 'lemma', 'proved', 22,
    '完整Cartesian SPE银行actual覆盖W_B不小于最大单银行主题L，由末位保持主动作只改银行的真实BR证明。任取最大B*，z_(i−1)(x)=#{j<i:x∉B_j}，Ω=Σ_(x∈B*,i)[1/(m−z_(i−1)(x))−1/m]≥Σ_(j<m)(m−j)|B*∖B_j|/m²≥0；ΣK_i≥L+Ω。因此各joint预算的W_B−L可加强为W_B−L−Ω。若W_B=L且ρ_i全0，则d_i全0、Ω0；m≥2时所有actual银行动作均等于任意预选最大B*，m1只保证动作大小L。',
    '所有m≥1与完整Cartesian SPE；Ω对任意最大银行主题B*成立，最低资本不需早期银行投影为SPE。',
    ['主/银行客户不交、完整Cartesian动作域、后继仍真实依赖两坐标。'],
    '必要银行资本和指定零振幅等号刚性；不排一般正振幅银行构造。',
    'Ω提高必付保底，是扣款不是新可花信用。实际嵌套容量零与全部映射历史饱和投影为另外两个已有主owner命题，不能互换。', [20, 23])

add('qb_compiler', 'QB绝对收益范围奖励的完整历史编译及严格非放大成本', 'construction', 'proved', 24,
    'k≥1、m=k+1，银行X_i两客户、a_i私有及b,d公共，A_i=X_i+a_i、B_i=X_i+b、C_i=X_i、D={b,d}。若每玩家全部主终局收益范围长≤正有理g，银行质量乘g并取完整Cartesian目录，可构造完整SPE，在Q状态按任意指定早期主动作与fresh A_i，末位D；所有联合偏离有可信Q/B或产品SPE尾将当前银行3g压至≤2g，末位2g。actual银行已全覆盖(3m−1)g，故OPT_prod−2W_prod≤−(2m−1)g<0。',
    '所有有限主输入、k≥1、正有理全终局范围上界g，任意逐完整Q状态的早期主处方；m1另为唯一D加主BR边界。',
    ['主/银行客户不交；全终局范围而非只actual regret；有理质量须对整个产品共同清分母。'],
    '真实完整奖励编译器与该架构成本，不是一般低成本编译不可能性。',
    'fresh B即时可达3，须单独B域压到2，不能粗略略去。Q保存多个旧A/C及target换手，所有退出补真尾；尚无只用局部regret的完整廉价版本。', [20,
      'archives/customer-attraction/state/反例/三人碰撞自由族福利障碍--反例.md'])

add('deviation_capacity', '真实偏离查询子集的Cauchy覆盖次数必要容量', 'lemma', 'proved', 25,
    '固定任一完整SPE合法节点h，当前规定最终收益u、过去负载b；强制合法T后沿同σ真实完成，严格后继覆盖次数L_x。对任意非空Q⊆T、q=|Q|，u≥Σ_Q1/(b_x+1+L_x)≥q²/[q+Σ_Qb_x+Σ_QL_x]>0，故Σ_QL_x≥q²/u−q−Σ_Qb_x。遗漏Q在actual前缀b0；若u<q/2则需严格超过q次后继覆盖。',
    '每份完整SPE的每个合法有序节点、每个合法偏离T及每个非空客户子集Q⊆T。',
    ['单位客户、真实偏离后的同一策略后继；q>0，空Q/零收益不作除零。'],
    '覆盖次数下界非福利/利润下界；各客户可不均匀，不能跨互斥分支累成根共同资本。',
    '正文不交core＋共同D重复尾还要求R/t≥x/2+|Y_j|，若另有R/t≤x才得|Y_j|≤x/2；早期改D又需真实拥挤容量。提高储备不免费，未排交叠储备或一般half。')

add('partialcore_subspe', '60单位客户两固定前缀的完整三回应者部分核心处罚', 'construction', 'proved', 27,
    '正文九兴趣型60客户、12互异主题，六人游戏固定前三动作。small前缀(A0,C1,CB)，目标尾(T1_0,T2_0,T3)，终利润(5/3,2,2,50/3,50/3,18)；big前缀(C0,C1,AB)，目标尾(T3,T1_0,T2_1)，终利润(1,1,4,16,19,19)。政策在目标尾前缀继续下一目标，否则永远D，定义全部157节点并满足各1884真实IC；两前缀下D均为任意两回应后的末位弱支配行动。',
    '这两个明示固定三行动背景后的全部三回应者有序历史及全部12合法行动；只存在这些具体子SPE。',
    ['共同客户池与标签顺序按正文完整表；原small证书全部157动作与单位独审small政策同一。'],
    '局部可信处罚组件，不认证给定前三玩家最优、六人根完整SPE或全部可实现尾部。',
    '构造器large_A检查的目标尾T1_0,T2_0,T3与独审big不同，不互借。small W57、big W60、六槽OPT60，均非half反例；T主题交叠共同E池，不适用不交gluing前提。', [28,
      'archives/customer-attraction/tools/evidence/disjoint-gluing-and-partial-core-reviews-boss3/original/time/partial_core_independent_audit.json',
      'archives/customer-attraction/tools/evidence/disjoint-gluing-and-partial-core-reviews-boss3/original/construction/partial_core_tail_certificate.json'])

add('partialcore_root_no', '60客户部分核心指定储备路径的更早D偏离排除', 'obstruction', 'proved', 27,
    '同60客户12主题六人输入，指定根路径C0,C1,CB,D,D,D若保第三人CB最终收益4，则在前缀(C0,C1)改D覆盖42名过去未覆盖客户，严格后继仅3人，不论如何继续每客户总负载≤4，保证偏离收益42/4=21/2>4，严格增益≥13/2。因此保该actual路径及收益的任何后继补全均非完整根SPE。',
    '该指定路径/输入下对所有可能真实后继策略均排除；不只排首次偏离后全D的一个政策。',
    ['D客户与C0,C1不交；六人，第三位置后恰三名玩家。'],
    '具体根候选的无法补全，与两个固定前缀后三人子SPE的正确性相容。',
    '不否定所有partial-core结构、全部六人SPE或half；后续利用局部处罚仍须付早期储备偏离。', [28, 25])

add('aggregate_menu_no', '六child聚合利润达5F/8加根IC仍不足的精确非均衡菜单', 'obstruction', 'proved', 29,
    '同61单位客户六主题输入，F4(0)=61；根T=A…F指定tail分别AAA,AAB,AAC,AAD,AEE,AFF，F3(T)=(36,51,50,51,42,42)，tail利润=(45/2,35,71/2,35,97/3,97/3)，根利润=(15/2,5,11/2,5,17/3,17/3)。所有tail利润≥(5/8)F3(T)，A根严格最佳，却实际AAAA总覆盖30<61/2。因此只保每child数值聚合profit下界和根IC的放松归纳状态不足。',
    '存在这份同单位客户输入上的六个完整三行动tail菜单；全部六根动作覆盖，无child内部SPE假设。',
    ['F是保真实背景负载的最优剩余利润，非零背景总覆盖。'],
    '精确放松合同反模型，甚至强于3F/5门槛；不是原完整SPE half反例。',
    'AAA末位A得15/2而C得11，严格增7/2，因此不能补成SPE。真AAAF另有W38、根局部债7由实际child盈余22支付，说明真局部步界与该聚合放松是不同合同。', [28,
      'archives/customer-attraction/tools/evidence/aggregate-profit-state-and-stationary-refund-boss3/replay/all-1296-ordered-tail-values.json',
      'archives/customer-attraction/tools/evidence/aggregate-profit-state-and-stationary-refund-boss3/replay/six-child-menu-exact-review.json'])

add('overlap_F', '全人数交叠SPE族首A背景的最优剩余利润精确消元', 'lemma', 'proved', 30,
    '每n≥4、x=n−2，正文普通叶/特殊叶单位兴趣型与完整策略actual AB^(n−1)，u_A=n−1/n、W=n²−2、OPT=2n²−2n−2。以剩余利润而非总覆盖补全为F，首A后余n−1槽的精确最优Ftail=2(n−1)(n−2)+(7n−13)/6：b0最优n−1不同叶含特殊，b≥1可换至一B及n−2不同叶含特殊，两域差(n−4)/6。根差Δ=(17n−23)/6，系数二余额=(23−5n)/6−2/n，n4为0、n≥5负；所需局部系数R_n=n(17n−23)/[6(n²−1)]趋17/6。',
    '所有整数n≥4，对全部n−1槽整数多重集精确优化；SPE真实性复用同族全历史证明。',
    ['客户兴趣和特殊叶重数按正文；固定一名A合法背景；比较允许重复。'],
    '该全n族的F精确工具值和局部步界障碍，17/6并非通用系数。',
    'all-big族已否所有人数通用有限α；本交叠族仍有2W−OPT=2(n−1)>0，真实尾信用支付根债。n4…8有限枚举15501条只核实现，不承担全n证明。', [
      'archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md'])

add('shared_credit_no', '只见共同正负载的实例无关可加信用不可能同时满足两条利润合同', 'obstruction', 'proved', 30,
    '不存在同一函数族f_r(b,c)（允许有符号），满足f_r(0,c)=f_r(b,0)=0并对每个完整SPE节点同时有F_r(b)≤2P_h+C_h及Δ_h+C_(hA)−C_h≤2u_h，其中C_h=Σ_x f_r(b_x,c_x)。all-big n族尾(T)迫f_(n−1)(1,n−1)≥(2−h_n)/n，h_n=min_(1≤j≤n)(j+n/j)；交叠族根(L)迫同值≤{(23−5n)/6−2/n}/(n−1)。n≥16时前者>−1/2、后者<−1/2，严格矛盾。',
    '否定对所有有限实例/人数/完整SPE节点通用的同一f族；使用两真实完整SPE族在同r同负载对上冲突。',
    ['f只依该r及单客户两负载，不见实例/总客户数/目录/其它客户或策略；两个轴均为0。'],
    '精确窄信用模板障碍；信用合同是half充分形式，非half必要形式。',
    '不假设非负、连续、单调或凸性；放开c0轴或读取更多信息未由本两族排除，后续B10旧客户完整H障碍另用三组件及产品更强。不能以C=F−2P的循环定义当证明。', [
      'archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md'])

# Material owners are reverse references. Pending external identities remain explicit.
rows = []
for i, m in enumerate(M, 1):
    own = [o['object_id'] for o in OBJS if o['body']['path'] == m['path']]
    attached = [o['object_id'] for o in OBJS if any(x['path'] == m['path'] for x in o['evidence'])]
    rows.append({**m, 'disposition': 'objects' if own else ('attachment' if attached else 'needs-decision'),
                 'object_ids': list(dict.fromkeys(own + attached)),
                 'reason': READ + ' 正文承载独立对象。' if own else READ + ' 证据/来源合同归所列精确数学owner，原有限记录不提升为普遍结果。'})

def route(i, owners, reason, disposition=None):
    row = rows[i-1]
    row['object_ids'] = list(dict.fromkeys(row['object_ids'] + owners))
    row['reason'] = READ + ' ' + reason
    if disposition:
        row['disposition'] = disposition

route(15, ['customer-attraction/full-history-fresh-policies-on-symmetric-nonempty-types'],
      '与0058主owner同精确fresh定理；父Boss已全文实读并实际接“为什么任意逐历史鲜动作策略在种子上都是SPE”唯一节为evidence。税包络合同另归本批方法；12份再生成完整策略的有限IC核不扩大LP最优。', 'attachment')
route(19, ['M-856a84ce52264852b5c6e9be8a37c917'],
      '2396同一38正原子精确点；registry主owner已实际包含本文件完整path/SHA证据。65全向量生成/38正metadata绑定、旧mass_numerator只来源等独有合同保为该owner附件，不另造同一点。', 'attachment')
route(21, ['BANK-PATH-CAPACITY-v1', 'BANK-MONOTONE-PROJECTION-v1'],
      'priority主批已发布这两个精确对象，且主body就是本文件同SHA；本批只反向复用主owner，不复制略异同ID记录。', 'objects')

PENDING = []
def pending(i, owners, reason):
    # An own mathematical body must stay objects; unresolved additional routing is retained here.
    if rows[i-1]['disposition'] != 'objects':
        rows[i-1]['disposition'] = 'needs-decision'
    rows[i-1]['reason'] = READ + ' ' + reason
    PENDING.append({'material_index': i, 'material': M[i-1], 'requested_owners': owners, 'reason': reason})

pending(6, ['cag-fourteen-customer-optimal-partitioned-frozen-query-counterexample'],
        '本页独有127客户添加费72>71已由本批新对象保成熟数学；其14/127两个PFR独立原审计和版本合同仍须0013主owner实际接证，不能因已有同结论主ID就假附件闭合。')
pending(7, ['cag-fourteen-customer-optimal-partitioned-frozen-query-counterexample'],
        '本页独有127添加费反例归本批，新发现器/整数恢复/双规模原审计另是同PFR Claim必要证据；待主owner接完整path/SHA后补路由，不新增PFR同义身份。')
pending(10, ['customer-attraction/credible-policy-cone-true-static-security-multiplicity-alternation-program'],
        '以固定query静态保证归一1最小W的完整策略交替，与0053按actual W1最大静态保证t的齐次聚合搜索为同真实安全攻击接口；20个best=n是未更新哨兵而非精确最优。未取得主owner实际接证回执，保needs-decision而非另造按程序名身份。')
pending(13, ['B2-REPEATED-LAST-ABSENCE-v1'],
        '税包络软件版本合同已在本批方法证据中保全；末覆盖gamma七步内部解析复核须B2主owner实际接本来源。其12随机/7known历史范围不可补成精确一般付款。')
pending(17, ['M-b75d8f7b6a7f4b8cabb2fabf7def95df'],
        '旧64同坐标质量27诊断的8负值含主owner已认证AE末位异X同一负分数；不新造相同固定点不可补全身份。须原owner实际接27全值/原程序字节复现证据。')
pending(20, ['BANK-PATH-CAPACITY-v1', 'BANK-MONOTONE-PROJECTION-v1'],
        '本批signed/振幅资本及QB构造已归自身owner；原作者/独审完整路径容量、非零前缀与饱和投影责任说明尚需priority两主owner接来源ref。前向吸收另有主body，不在本批重造。')
pending(23, ['BANK-PATH-CAPACITY-v1', 'BANK-MONOTONE-PROJECTION-v1'],
        '37案例有限原审计已归本批signed/资本对象证据；时间谱与21全映射饱和投影的有限独立实现仍待priority两主owner实际接该来源，不以代码PASS生成节点。')
pending(26, ['M-ab6350dcf866451bb43d6f3908f42ec0'],
        '与0062主owner同一24单位客户/16主题完整273节点策略及全菜单277/54鞍点。新增未改原程序知情复放、全部48/16上下界、768核项与12耦合记录是同命题完整证据；主record未canonical且未接此ref，保needs-decision，由父Boss路由，不复制同ID。固定query同步差1/12亦由同完整正文保。')
pending(28, ['DISJOINT-POLICY-GLUING-v1', 'CA-R18-DYNAMIC-PROFIT-BOUNDARY-20261031'],
        'partial-core两局/非均衡六菜单已归本批两个成熟owner；另有不交gluing独审的实际先验和61客户full/static报告版本、真局部差25>18证据，须相应原主owner接完整来源ref。若主owner已有相应源可核后定向回写，不假全部已接。')
pending(29, ['CA-R18-DYNAMIC-PROFIT-BOUNDARY-20261031'],
        '本批独立登记非SPE六child聚合菜单反模型；真61客户SPE的F4−F3(A)=25>18及实际child盈余22归已有局部系数障碍的独立精确见证，需要主owner实际接证。两合同不可混为完整SPE half反例。')
pending(30, ['CA-R18-DYNAMIC-PROFIT-BOUNDARY-20261031'],
        '本页全n交叠F精确消元与两轴为零可加信用障碍在本批分立；all-big任意有限α局部台阶失败与既有CA-R18精确同命题，含h_n及tail信用h_n−2、根债h_n−3的差1分析，待该主owner实际接本来源，不复制同ID。')
for i in (31, 32, 33):
    pending(i, ['B10-BACKGROUND-HISTOGRAM-CREDIT-NO-v1'],
            '同三组件/旧客户完整H信用不可能性：两个64人产品同H=4032(1,63)+4032(1,0)，下界−2898、上界−3170、差272；不新增同义定理。独立AB全历史闭式策略、三种原有理程序各自有限覆盖和全部报告，均须该精确主owner实际接证。本地registry及已发布批次未见该owner，保needs-decision；不把一般产品解析证明/有限m2,3回归/64人数值代入混成全树穷举。')

BATCH = {'schema': 2, 'objects': OBJS, 'materials': rows, 'edge_files': []}
OUT = ROOT / TASK['write_paths'][0]
OUT.write_text(json.dumps(BATCH, ensure_ascii=False, indent=2) + '\n')
batch_ref = ref(OUT.relative_to(ROOT).as_posix())
receipt = {'batch_file': batch_ref, 'assets': [batch_ref],
           'summary': {'objects': len(OBJS), 'materials': len(rows), 'edge_files': [],
                       'pending_material_count': sum(x['disposition'] == 'needs-decision' for x in rows),
                       'additional_pending_routes': len(PENDING)},
           'reading_current_execution': {'materials': M, 'shared_definitions': TASK['context_plan']['shared_read_refs'],
              'scope': READ, 'fully_read_material_indices': list(range(1, 34)),
              'source_attachment_boundary': '必要原始JSON/程序等按正式正文的成熟精确证明和既有事件复用；未把所有原附件宣称本次逐字复读。'},
           'pending_cross_owner': PENDING,
           'same_group_dependencies': [ref('research/registration/batches/register-ab98f323ad-0058.json')],
           'id_allocation': ref('research/registration/Boss2/0055/id-allocation.json')}
(ROOT / TASK['write_paths'][1]).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
(HOME / 'reading-checkpoint.json').write_text(json.dumps({'task_id': TASK['task_id'], 'fully_read': M,
    'shared_definitions_read': TASK['context_plan']['shared_read_refs'], 'unread_formal_materials': [],
    'next': '父Boss核跨批owner实际接证；本worker按反馈定向修本批。',
    'no_git_writes': True, 'no_mathematical_program_reexecution': True}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt['summary'], ensure_ascii=False))
