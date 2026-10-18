# Degree-two bounded-menu joint rounding v2：Exact-first 独立审查

审查者：general_query_response_review。2026-10-18。

冻结前只读新 Exact 及获准的 primary PDF：Verschae–Wiese 2010 arXiv v1 §5.1，printed pp.9–10 / PDF pp.10–11。已提取原文并实际渲染、查看这两页。未读取新作者 Proof、未向其他审查者索取证明、未修改 repo/Work/Git。

冻结输入 SHA-256：

- Exact：`7435885c698e741f0dc762cd1fc79be270ad7de164859477645b37affbd9a298`
- primary PDF：`2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`

**独立结论：Exact v2 的联合算法、相对 OPT 界、bonus 保 OPT 及二状态 2SAT 结论成立，未发现 fatal。外部 additive 定理的真实条件与本归约吻合。**

## 1. 原始实例的无条件范围

每组非空菜单且至少一个组，故至少一枚 selector，所有 selector 的每个合法端时间为1。因此任何完整原调度的 makespan≥1。

任取每组一状态放 selector，全部 incidence jobs 保留各自私有状态机；每个无 selector 的状态机负载≤1，有 selector 的状态机负载≤2，资源机空。因此全部域内输入有

\[
1\le\operatorname{OPT}(P)\le2.
\]

此构造只用显式原端。跨组私有机共享、预载、拒绝 job 或其它 side constraints 都不在域中，证明不偷偷容许这些变化。

## 2. Normalized 恒等式：OPT=2−V

以下先设每个状态私有总量 W_gs=1。各 clause a_gs 总量为1、非负，故 `0≤V≤1`。

### Allocation → 完整实际调度

给任意两两不交 B_g，对每组选择使 a_gs(B_g) 最大的一枚原状态 s_g。selector 放 M_g,s_g；只把选中状态内 `u∈B_g∩S_g,s_g` 的 incidence jobs 放 R_u，所有其它 incidence jobs 放各自私有原状态机。

资源机最多一枚 unit job：B_g 跨组不交，且单个状态内无资源 multiplicity。选中状态机的负载为

\[
1+1-a_{g,s_g}(B_g)=2-f_g(B_g).
\]

未选状态机负载为1，资源机负载≤1。因 f_g(B_g)≤1，完整 makespan≤`2−min_g f_g(B_g)`。取最优 allocation 得

\[
\operatorname{OPT}(P)\le2-V.
\]

选择后原 jobs 全部恰分配一次，没有把同组多个状态同时实现，也未把 allocation 中的 resource 直接当额外执行 job。

### 实际调度 → Allocation；必须区分 OPT=2 边界

若有完整调度 makespan C<2，每个资源机至多一枚 unit incidence job。把所有未放 selector 的状态之 incidence jobs 全部拉回其私有机，不增加 makespan：这些状态的私有总量恰1≤C。然后每组只剩 selector 所选状态可能有 exports。

令 B_g 为该组选中状态已 export 的资源。资源机独占给 B_g 跨组不交；选中状态负载≤C 给其 export 质量≥2−C，所以 `V≥2−C`。若 OPT<2，把 C 取实际最优值，得到 `OPT≥2−V`。

若 OPT=2，不能使用资源机独占论证：此时一台资源机可能接两枚 unit jobs。但先前 allocation→schedule 已给 `2=OPT≤2−V`，结合 V≥0 立即得 V=0，因此同一恒等式仍成立。这里没有把严格 C<2 的性质错误延伸到等号。

## 3. Group 级平均与 published additive degree-two 接口

每组仅建一个 additive agent，

\[
v_g(u)=\frac1{K_g}\sum_{s:\,u\in S_{gs}}p_{gsu}.
\]

对任意 B，`v_g(B)` 恰是该组所有 clause 在 B 上的平均。因此

\[
\frac{f_g(B)}K\le\frac{f_g(B)}{K_g}\le v_g(B)\le f_g(B).
\]

第一步用 K_g≤K，第二步用非负性及“平均≥最大项/K_g”，末步用“平均≤最大项”。重要的是没有把 states 拆成 agents。

把每个显式 resource 当一个 item。资源属于至多两组，故 v_g(u)>0 的 agent 至多两个；同组多状态反复出现只改变这一个 agent 的加总值。zero-value incidences 可删，不影响 additive optimum；全零 item 可丢弃。

若 A 为该 additive instance 的 max-min optimum，将 V 的最优 allocation 原样用于平均 valuations，得 A≥V/K。

### Primary 条件实核

已读 primary §5.1 的完整定义、preassignment、两类边配对及 Theorem12/证明；原文明确允许一个 item 在至多两个 eligible agents 上具有不同数值。其算法为组合式确定性 factor2：阈值测试、强制预分配、排序配对与二部二着色，再二分阈值；原文也明确把运行时按 binary input length 计。

本归约的 items 正是资源，agents 正是原 groups，非“2K 个 state agents 再压缩”。private bonus items 若有仅 degree1。该引用是 additive MaxMin-balancing 定理，不是 makespan configuration-LP gap 论证。

## 4. 联合算法与 relative-OPT 界

调用该 published additive 算法，输出两两不交的 B_g，满足

\[
\min_g v_g(B_g)\ge A/2\ge V/(2K).
\]

对每组扫描显式菜单，取 s_g 最大化 a_gs(B_g)。因为 f_g(B_g)≥v_g(B_g)，第2节的实际调度恢复给

\[
C_{\max}\le2-\frac V{2K}
=2-\frac{2-\operatorname{OPT}(P)}{2K}.
\]

辅助算法不需要知道 V、A 或原 OPT；这些量只用于分析其近似保证。选择状态发生于这一个共同 allocation 之后，不预先锁定 heavy state 或拆开 diffuse states。

令 x=OPT(P)∈[1,2]。所需 ratio 不等式的右减左为

\[
\left(2-\frac1{2K}\right)x-left[2-\frac{2-x}{2K}\right]
=\left(2-\frac1K\right)(x-1)\ge0.
\]

因此 ratio 为 `2−1/(2K)`。OPT=2 时只保证 makespan≤2，而不错误声称任意输入均达到绝对阈值 `2−1/(2K)`。

## 5. Bonus normalization 精确保留 OPT

每个 W_gs<1 状态只加一枚独有 resource z_gs 和一枚 bonus job，私有时间1−W_gs、资源时间1。该 indexed state 总量恰1；selector、原 incidence jobs 及全部原时间都不改变。每个新 resource 只属于一组，故 degree≤2 保留，K 也不变。

任一 augmented 调度删除 bonus jobs 就是原实例完整调度，负载不增，所以 `OPT(P)≤OPT(N(P))`。

反过来，任一原完整调度 makespan C≥1，可将所有 bonus jobs——包括未选状态的 bonus——各自 export 到其独有的新资源机。每个新机负载1≤C，不动任何原 job，故 `OPT(N(P))≤OPT(P)`。所以两者相等。

对 N(P) 运行 normalized 算法，再删除 bonus jobs；所得原调度的 makespan 不增，以上 relative-OPT 和 ratio 界原封不动适用原 P。

空状态 W=0 加一枚私有时间1的 bonus，仍满足上述双向论证。W=1 状态不加。零时间原 jobs 始终可以放私有端，无须 export 或当成正支撑。

## 6. 零最优 allocation、empty S 与 bit complexity

- G 非空、每菜单非空保证实际 OPT≥1；states 可以为空、重复或有全零 p，均由第5节 normalization 原生处理。
- normalized 情形若 additive optimum A=0，factor2 所需保证只是≥0；输出任意 disjoint allocation 即可，第2节恢复使 makespan≤2。若 V>0 则 A≥V/K>0，所以此退化不会误损相对界。
- 可把所有正辅助权统一乘以共同分母 D 得整数。D 的二进制位长是显式辅助权分母位长的总和，后者为原输入位长的多项式；不复制 D 份物品。阈值二分次数按 log D/编码长度而非 D。
- published 正整数阈值算法的 optimum=0 情形可单独测试整数阈值1；若拒绝，则整数 optimum<1，即为0，直接采用零值 allocation；无需正最优假设。
- averaging、row-sum、bonus 时间1−W、argmax state 及实际负载均为有理精确加减乘除，位长多项式。所有组、state、item 和原 jobs 显式给出，K可大但≤显式状态总数，不依赖 succinct expansion。
- 算法输出每个原 selector 的某一原 state 机及每个原 incidence 的两原端之一。bonus 投影只删除新增 jobs，没有删掉原 zero job 或其它原任务。

## 7. Promise、cube 与两状态 2SAT

严格 unit YES 下 OPT=1，算法实际返回 makespan≤`2−1/(2K)`。NO 若 OPT 严格大于此阈值，则任何完整实际调度都超过阈值。因此检查算法返回的完整调度即能决定该 promise；gap 外不作其它断言。K≤7 时 factor 正是27/14。

F 的 tagged cube 结论在其明确的 injective incidence-index 假设下正确：一个 resource 只可能属于其 Q 个坐标值命中的 groups，故 distinct groups≤min(d,Q)，Q=2 满足本度数合同。该点不是对任意未定义分组的无条件结论。其它既有 unweighted/DGR 上界仅作对照，并非本新算法的依赖；本次未重新审查那些旧定理。

若 K_g≤2，严格 unit 可行等价于每组选一个状态，且所选状态的正权 resource supports 两两不交：

- 必要：selector 时间1已经吃满该 state 机，因此其所有 p>0 incidence jobs 都必须 export；资源机负载≤1，故同一 resource 不能供两组所选正 jobs 使用。p=0 可以与 selector 同机，不应禁止。
- 充分：所选状态全部正 jobs export，zero jobs留 private；其余状态全部 incidence jobs 留各自私有机，其 row sum≤1。正 supports 不交给资源机负载≤1，所有 selector机负载1。

每个两状态组一个 Boolean choice，单状态组固定；每个跨组冲突的状态对给一个禁止同时选它们的2CNF clause。重复状态、空 support、零权和 singleton menus 都合法。该2SAT只解 makespan≤1，不推出其它 makespan 的精确最优算法。

**最终独立判断：新 Exact 的实质算法与定量结论成立，primary 适用条件已实际核对；未声明实现、新颖性或一般 UM below-2 结论。冻结本文件后方可读取新作者 Proof。**
