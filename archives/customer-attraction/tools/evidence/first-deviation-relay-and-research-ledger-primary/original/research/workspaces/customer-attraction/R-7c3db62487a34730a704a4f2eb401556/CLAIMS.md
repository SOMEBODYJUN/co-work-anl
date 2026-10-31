# 精确个人研究账本

本页登记本工作区资产，不自动提升共享 canonical 状态。主目标 Q-CAG-HALF
的对象、量词不变，仍 OPEN；外审和新颖性均未认证。

## CA-ANCHOR-PRIVATE-SEAT-SPECTRUM-v1

- **Exact Statement / Objects / Domain：** CAG-MODEL 的每个有限实例、任意 m≥1、
  每个全部有序历史依赖纯 SPE。取实际覆盖 C，所有包含极大主题 B_j，
  P_j=B_j\∪_(l≠j)B_l，Q_j=P_j\C，a_j=|Q_j|。
  在每个实际位置 i 取 r=m−i+1、前缀负载 b_i，令
  β_ij=Σ_(x∈B_j\Q_j)1/(b_i(x)+r)，λ_i 为所有
  a_j/k+β_ij（j全体、1≤k≤m）的第 r 大值。
  则对每个 i 有 u_i≥λ_i，故 W≥Σ_iλ_i。
- **Quantifiers / Assumptions / Definitions：** 对全部实例、人数、完整纯 SPE
  和实际位置全称；保留任意平局、空主题、重复和零客户。比较块从实际终局
  固定后，在离轨树中不更换；β 在每个 anchor 子树中固定。
- **Scope / Conclusion：** 联合私有席位与共享遗漏/已覆盖客户的前缀基线；
  是后验必要预算，不是一般 half，也不是输入端均衡选择算法。
- **Dependencies：** 旧 superset 残余席位归纳、全局私有块、同终局子主题支配、
  单位客户份额与全部历史的真实偏离最优性。
- **Evidence：** 自足任意人数解析归纳；主代理先见公式独立重构；有限精确回归
  30 实例、174 可实现有序路径、548 位置行、30 完整策略证书，仅检查实现。
- **Counterevidence / Objections：** 无已成立的本命题致命异议；下一条明确否定
  仅用此谱加全部分数覆盖行即可闭合一般 half 的接口。
- **Status：** 已有解析证明及内部独立重构；个人资产，未作共享正式整理。
- **Related Files：** [正文](omission/joint_omission_prefix_spectrum.md)、
  [作者复现](omission/audit_joint_omission_spectrum.py)、
  [冻结输出](omission/joint_omission_spectrum_audit.json)、
  [独立审查](parent/joint_spectrum_independent_review.md)。

## CA-JOINT-SPECTRUM-FRACTIONAL-NOSUFF-v1

- **Exact Statement / Domain / Quantifiers：** 对每个整数 m≥13，存在有限单位客户
  共同目录和一条确定有序路径，该路径满足上一条联合谱全部位置行以及
  对每个可覆盖客户集 E、每个分数覆盖总重 τ 的全部真实形式前缀行
  |E|≤P_(i−1)+(m−i+1)τu_i，但有 OPT_m>2W。
- **Objects / Definitions / Assumptions：** L=lcm(1,...,m)，K=(m−1)L。
  m 个 B_j 的每对共享 L 名独有客户，另有 m 个不交银行 A_r，大小 K/r；
  路径 A_m,...,A_1。这里明确不假定该路径为 SPE。
- **Conclusion / Scope：** 必要预算接口不充分；不是主目标反例。
- **Dependencies / Evidence：** λ_i=u_i=K/r，W=KH_m，OPT≥mK/2；
  m>4H_m 对全部 m≥13 的有理基础值与差分证明。
  所有主题大小≤K，直接推出对全部 E、全部覆盖的前缀行。
- **Counterevidence / Objections：** 原路径在倒二节点存在严格盈利偏离，
  且偏离后末位唯一选 A_1；因此已证明不能由任何 SPE 实现。
- **Status：** 解析方法障碍与定义级不可实现性，内部独立重构；不改变 Q-CAG-HALF。
- **Related Files：** 同上正文第 4—5 节及独立审查。

## CA-JOINT-SPECTRUM-FRACTIONAL-NOSUFF-v2

- **Exact Statement / Objects / Quantifiers：** 每个 m≥5 都有原单位客户共同目录
  与一条非 SPE 有序路径，满足 v1 所述全部联合谱和全部比较分数覆盖前缀行，
  但 OPT_m>2W；且每名实际遗漏客户恰在两个不同极大主题中共享，遗漏关联为匹配。
- **Domain / Assumptions / Definitions：** L=lcm(1,...,m)。m 组各有两主题，
  共享 L−1 名遗漏客户并各带一名不同信用客户；这 2m 信用客户都被银行 A_1
  覆盖。银行 A_r 大小 L/r，彼此不交。目录全部 3m 主题均为不同极大覆盖。
  路径为 A_m,...,A_1。
- **Conclusion / Scope：** λ_i=u_i=L/r，W=LH_m，精确 OPT=mL>2W；
  故不能仅以遗漏 degree2、森林或匹配假设修补原必要条件接口。
  不否定这些结构下真实 SPE 的 half。
- **Dependencies / Evidence：** m>2H_m 的基础有理值与正差分；所有主题大小≤L
  给全部分数覆盖行；父代理独立逐客户核对极大性和末位菜单，Fraction 审计 m=5,13。
- **Counterevidence / Objections：** 路径倒二偏离使其在全部末位最优回复下
  从 L/2 升到 L，已证明不能由任何完整 SPE 实现。
- **Status / Related Files：** 已解析证明、内部重构；[正文第6节](omission/joint_omission_prefix_spectrum.md)、
  [v2冻结输出](omission/joint_omission_spectrum_audit_v2.json)、[独审](parent/joint_spectrum_independent_review.md)。
  v1 原范围和冻结报告保留，不悄悄改写为 v2。

## CA-COMMON-CORE-ARBITRARY-TAIL-v2

- **Exact Statement / Objects / Domain / Quantifiers：** 对任意 k,r≥1、不交单位客户块
  X_j,P_j,B,E，目录含 C_j=X_j、A_j=X_j∪P_j、D=B∪E；其他每项是 X∪P 的
  任意子集或 B 加其任意子集。每份实际为 C_1,...,C_k,D^r 的完整纯 SPE
  都满足 |P_k|≤|X_k|/2。均匀 |X_j|=x、|P_j|=a 时有 2OPT≤3W。
- **Assumptions / Definitions：** 除 D 外不触 E；公共主题含全部 B；实际前缀在
  X 上负载恰一。跨任意多组的脚印、任意目录大小、零块、空主题和任意历史平局均允许。
- **Scope / Conclusion：** 限制这种可扩展惩罚家族；非均匀只约束最后 C 组。
  任意纯局部 A⊇C_k 另满足 β(A)=|A∩X|/2+|A∩P|≤|X_k|。
- **Dependencies / Evidence：** 实际末位菜单；D 在整个真实偏离子博弈的无条件保证；
  局部/公共响应分类与逐客户饱和。construction、harmonic 与父代理独立重构。
  一次旧 RT-r 子类的有限三响应者证书只核验实现，不承担 v2 量词。
- **Counterevidence / Objections：** 未见成立的致命异议；部分公共核心、D 外可触 E、
  不同实际尾主题与一般前缀负载未被本命题涵盖。
- **Status / Related Files：** 内部解析已核对，未共享正式整理；
  [v2正文](construction/common_core_arbitrary_catalog_v2.md)、
  [harmonic重构](harmonic/cross_group_tail_extension.md)、
  [父审](parent/common_core_cross_group_review.md)。RT-r 与单组 v1 原范围保留。

## CA-STATIC-WORST-OCCUPANT-NO-v1

- **Exact Statement / Quantifiers：** 每个静态竞争槽数 m≥1 都存在单位客户共同目录、
  真正安全最优查询 p* 及其唯一纯最坏背景 q，使 q 的每位占用者收益为 v_(m+1)−1。
  q 本身也是最优静态对手分布的全部支撑。
- **Objects / Domain / Assumptions / Definitions：** 两核心各 C=m(m+1) 客户；每核心
  h=m+2 个叶，各有 P=m+3 私有客户；另有双核心主题 B。p* 均匀查询全部叶，q=B^m。
  v_(m+1)=max_p min_(|q|=m)Σ_xα_x(p)/(1+c_x(q))。
- **Conclusion / Scope：** v=2m+3、U_B(q)=2m+2；精确自占用返还后仍有净换标债1。
  否定该静态源端无债桥；不否定加入真实 Γ 激励后的中继或弱聚合。
- **Dependencies / Evidence：** 任意 q 的核心成本增量与私有项损失的解析比较，
  匹配原始/对偶证书；父与security独立得到同参数，Fraction全计数核验 m=1,...,6。
- **Counterevidence / Objections：** q 自身末位改叶严格获利2，故不是完整 SPE 终局。
  没有主目标或弱安全聚合反例。
- **Status / Related Files：** 解析辅助桥反例、内部重构；
  [正文及十客户小例](security/occupied_static_minimizer_counterexample.md)、
  [父重构](parent/security_minimizer_obstruction_review.md)、
  [精确审计](security/audit_occupied_static_minimizer.py)。

## CA-PAY-PARAMETER-LEFT-JUMP-v1

- **Exact Statement / Quantifiers / Domain：** 对每个 m≥5，存在全部历史纯 SPE 与唯一
  真正最优 m 元计数组合，沿前缀长度1到2，PAY仍失败而唯一最优参数严格向左跳。
- **Objects / Definitions / Assumptions：** 大主题有 3(m−1) 名客户，另 m−1 个不交
  singleton；全部历史常选大主题。PAY沿用原接口，不改变前缀/最优元组存在量词。
- **Conclusion / Scope：** 两参数为 8m/(3m−2) 与 4m/(2m−3)，后者严格更小。
  否定“未支付时参数只须单调右扫”的规则；不否定一般 PAY。
- **Dependencies / Evidence：** 常量完整 SPE 逐历史保底、精确加权分位数公式，
  两前缀正缺口的正系数多项式证明；m=5 的 781 历史定义级证书。
- **Counterevidence / Objections：** 该族更晚仍可支付，OPT/W=4/3；不作为主目标反例。
- **Status / Related Files：** 作者解析证明及精确程序核验；父核对内层公式与有限路径DAG，
  尚未单列盲人工审查本参数族。[正文](pay/pay_quantile_and_path_cut.md)、
  [作者审计](pay/audit_pay.py)、[父DAG审计](parent/audit_pay_dag.py)。
