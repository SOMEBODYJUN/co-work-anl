# 依游戏选择的资源可分序势：独立重构与攻击

## 审查对象与冻结范围

审查者：boss3 内部 independent attack；本文只读审查，不进行 Git 写入或公共发布。

冻结仓库提交：`ec827a977d6e800073b031959016a04509aca986`。

主审 Claim：`WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER v1`，文件
`research/questions/weighted_congestion/ordinal_potentials/game_specific_separable_ordinal_barrier.md`，
SHA-256 `099fe036a70194c4daaaa66abe176b1c250e1b3cf8f5cf9630f838723cd6fd3d`。

关键依赖：`WC-R1-MULTIPLIER-BARRIER v1`，文件
`research/questions/weighted_congestion/marginal_potentials/arbitrary_multipliers.md`，
SHA-256 `7c1b3046da1da452aa528f8d16f9dfc276fabffc14c262bb0b074e3d628fd7ac`。

辅助比较：`WC-R1-ORDINAL-COPY-BRIDGE v1`，文件
`research/questions/weighted_congestion/ordinal_potentials/universal_additive_ordinal_bridge.md`，
SHA-256 `c11a5edb36b2a93296261a399d456b012ae8195b84a1e494b8a04b4eca155574`。

本次在阅读候选正文前，先从 MODEL、ACCEPTANCE 和专题 README 独立重构了插入路径与相容性瓶颈；随后阅读上述冻结证明，再逐项攻击。

## 精确结论及其边界

令

    rho_d = sup_{t>0} ((d+1)(1+t)^d+t^(d+1))/(d+(1+t)^(d+1)).

对每个整数 d>=2 和每个实数 1<=alpha<rho_d，存在一个有限正权、全部资源费用均为 x^d、所有玩家策略族均为 2^E 的游戏，使任何依整个游戏任意选择的资源函数 F_e:2^N->R 所形成的 Phi(s)=sum_e F_e(S_e(s))，均不能在该游戏的每条严格 alpha 改善边上严格下降。

审查判断：一般证明闭合；在上述冻结字节范围内没有发现仍成立的 fatal objection。此判断是内部数学审查，不是外部评审或新颖性认证。

这个游戏有 all-empty 精确均衡。结论不是 alpha-PNE 不存在，也不否定为每个游戏另选的资源可分目标只要求其全局极小点为近似均衡。唯一主问题仍开放。

## 先行独立重构

资源边际 Delta_i F(S) 若被固定正玩家乘子夹住，则沿任意玩家插入顺序从空集到同一玩家子集的边际和相同。因此任意两个顺序的成本加权路径和之比必须落在 [1/alpha,alpha]。

一个权重 1 的重玩家和 K 个权重 epsilon 的轻玩家，令轻重乘子密度比为 s，给出

    r(s) = ((1+K epsilon)^d+s epsilon sum_{k=1}^K(k epsilon)^d)
           /(1+s epsilon sum_{k=1}^K(1+k epsilon)^d).

此分式对 s 严格下降。单一重轻尺度不能排除任意 s，因为 s 可平衡两条路径；真正需要多尺度相容性：某个 t0 强制每对相邻尺度的乘子密度比大于固定 lambda>1，而另一 t1 强制最远两尺度密度比小于固定 C。有限尺度链 lambda^L>C 即矛盾。独立重构并未假设权重连续、玩家无限或乘子预先固定。

从序势走向夹逼的关键也应是将任意两个边际背景同时放入互不相交的资源束，用束大小比比较成本与势差。普适规则可在不同有限游戏间使用任意大复制数；依游戏规则必须先固定足够大的同一个游戏，不能见到势之后再添资源。冻结证明正好提供了这一必要的量词修补。

## 承重步骤逐项核对

1. 任意乘子依赖的对称化必须同时平均 F 和 h。对每个等权类置换并同时重标记边际不等式，所得类均值严格为正，故 beta_j=hbar_j/a_j 合法。
2. 两插入顺序都从空集到同一选中子集；未选玩家不必出现。除以 hbar_i a_i^d 后，路径和正好是正文 A、B。分式导数分子 b-ac<0，因为 a>1、0<b<c。
3. epsilon->0、K=floor(t/epsilon) 的极限是有限区间右端黎曼和极限。只需在 lambda、C 两个固定 s 值使用；从未对未知 F、h 作紧性或极限假设。
4. 先挑 lambda>1 使 R_lambda(t0)>alpha，再挑 C>lambda 使 R_C(t1)<1/alpha。两个严格间隙给出有限 delta；选固定 q<delta 和有限 L，且 q^L<=q<delta。
5. 第 j 类有 ceil(T/q^j)+1 名玩家，足以同时容纳每个相邻测试及最远测试所需的轻玩家。所有类与人数有限，所有权正。各测试仅取子集，不要求多组测试的选中玩家互不重合。
6. 主审命题先选 alpha<R<rho_d，再由依赖在倍率 R 获得坏权向量。令 eta=(wmin/W)^d>0；所有同一玩家背景的 B/A 均落在 [eta,1/eta]。
7. 先选 L>1/((R-alpha)eta) 并固定 M=L+floor(alpha L/eta)+1。对任意背景比 z=B/A，整数 m=floor(alpha L z)+1 满足 m+L<=M 以及 alpha z<m/L<Rz。即使 alpha Lz 是整数，+1 也保留左端严格不等式；L 的严格选取保留右端。
8. 所有资源同费用、所有策略为完整 2^E，故每个资源置换确是同一个游戏的自同构。任一固定严格改善边在每个置换下仍是严格改善边；有限平均保持严格势下降。
9. 平均后 H(U)=M^(-1)sum_e F_e(U)，无需 F_e 匿名、线性、同构不变或按统一模板产生。
10. 每个玩家可从单资源策略删到空集，所有正负载下 x^d>0，故每个 Delta_i H(S)>0。不存在 0/0 或边际非正问题。
11. 对任意 S、T，互不相交的 m、L 资源束可在已固定游戏内同时实现；属于 S∩T 的他人用两束，均是合法完整子集策略。玩家 i 只用旧束或新束，没有影响倍率的共同资源成本。
12. 该移动的成本是 mA 与 LB，严格 alpha 改善给出 q_i(T)<(m/L)(A/B)q_i(S)<R q_i(S)。有限背景集上的正最小值 h_i 存在，并产生被坏权向量排除的 R-sandwich。

## 边界、尝试的反驳与剩余限制

- alpha=1 被证明覆盖，且有限复制取整仍成立；alpha=rho_d 的端点没有被覆盖，也没有被偷偷升级。
- 游戏规模可极大，但存在量词只要求有限；M、玩家人数依 d、alpha、R、坏权向量而定，均在 F_e 选择之前固定。
- MODEL 允许空策略，且使用空策略是正性测试的实质组成。此证明没有自动覆盖禁止空策略的不同模型。
- d>=2；d=0、1 无需本结论。资源是合法非负系数 monomial，不需要从一般多项式外推。
- 极端小权使 eta 很小只放大有限 M，不产生无限游戏。
- all-empty 精确均衡与禁止可分序势相容；必须继续区分“每条改善边下降”和“某些边下降”或“全局极小点可选”。
- 将任意乘子障碍当作无均衡证明，或用此游戏否定任意非可分序势，均不被论证支持。
- 正文 Related Files 中若干旧 `assets/R1/...`、`proof.md` 链接是历史路径，应由主研究者维护现行导航；这不构成已核正文的数学反驳。

## 计算核验及其真实范围

实际重放：

    python3 tests/audits/weighted_congestion/marginal_potentials/verify_multipliers.py --output /workspace/scratch/c8b252147513/potential_multiplier_replay.json

四组冻结式输入 d=2,4,8,16 的任意乘子有限压缩证书全部通过，计算为 Fraction 精确有理数。没有展开巨型玩家表或声称枚举了游戏状态。

独立脚本：`tests/audits/weighted_congestion/ordinal_potentials/verify_finite_bundle_bridge.py`。可在仓库根运行（`--repo` 默认为当前目录）；本次实际命令为：

    python3 /workspace/scratch/c8b252147513/potential_independent_audit.py --repo /workspace/scratch/c8b252147513/co-work-anl-boss3

实际运行结果：`PASS 298 independent exact finite checks: insertion ratios, finite copies, resource averaging.`

脚本用直接有限幂和复核压缩 recurrence；检查 K=1、不同 d 与 epsilon、s 的严格单调性；检查 alpha=1、R-alpha=1/1000、eta=1 及很小 eta、上下端背景比和取整整点；并用非匿名任意有理 F_e 对所有两玩家三资源背景逐项核对资源平均公式。这些计算只核实现，不替代上述一般证明。

## 外部定理与出处范围

下障碍证明不依赖任何外部均衡存在定理。rho_d>d^((d-1)/(d+1)) 是取 1+t=d^(2/(d+1)) 的直接代入；rho_d<=d 可由正文对 H_d 的逐项二项式边际夹逼直接核验。因此 rho_d/d->1 的本次使用不需要额外论文假设。

本次实际打开 ICALP 2019 Caragiannis--Fanelli 主文，核对模型采用不乘 w_i 的玩家成本及严格改善定义。论文的原始形式主要写 monomial 资源；本审查下障碍本身也只使用 x^d 资源，不受零费用或一般多项式推广问题影响。没有作全球文献优先权认证。

## 对研究状态的影响

本次增量是对已有 game-specific 分离势障碍及承重任意乘子引理的独立逐步攻击与精确实现核验。未发现反例或一般证明缺口；没有产生全类 O(d/ln d) 存在性证明，也没有产生排除该存在性的新下界。可安全复用的结论是：若寻找所问匹配上界，不能仅靠每个游戏任意选择一个资源可分、并对全部 alpha 改善严格下降的序势完成。

父研究者逐式复核 (M2)–(M9)、(G3)–(G15) 及现行重构；未改变原 Claim 量词。当前重构见 `research/current/weighted_congestion/separable_ordinal_obstruction.md`。

现行自足重构的附加核对：审查者再次逐式检查资源数先固定、类人数充分和由dH_d推ρ_d≤d。初稿SHA-256为`1c295ce4da8d22bbaf478de34b197d069873b834d7198d0f7d1c1a8930d247bf`；父研究者随后将q的选取显式收紧为q<min{δ,t_0,t_1,1}，保障所有floor测试人数≥1，不改变命题范围或其他推导。
