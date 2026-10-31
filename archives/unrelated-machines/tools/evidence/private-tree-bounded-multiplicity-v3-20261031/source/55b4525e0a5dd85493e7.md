# 有界叶资源重数私有树：作者冻结证明

绑定 Exact：`/workspace/scratch/038d9dcc4cac/private_tree_bounded_multiplicity_floor_v3_exact_statement.md`，SHA256 `8fd533805efaf7ab6168d0512dea327e70360065d05b4df2d52a178a49279142`。

Candidate ID：`UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3`。

来源披露：literal 根据 root 提出的 μ 有界重数问题独立推导 rainbow blocker；先向 root 报告主链，后冻结 Exact-only。root 看过该摘要后独立提出相同全 CONFIG(T) 扩展；root 不是该新机制的盲审。本文不交给安排中的 Exact-only 审查者，直到其自行冻结重构稿。已有 v2、q 子可加性、raw 叶 blocker 与 Haxell 为明确前提，下文仍自足重述本次所需部分。无代码或有限测试代替证明。

## 1. raw 叶估值 q 的子可加性

对满 a 叉高 h 树，q(A) 是叶集 A 所含的最大同深完整分叉数。需要的是 raw 叶集合估值，不是对带重复色资源直接套一个已假定单射的 resource-demand theorem。

对任意有限叶集族 A_1,…,A_m，有

\[
 q\left(\bigcup_i A_i\right)\le\sum_iq(A_i).
\tag{1}
\]

独立归纳证明如下。h=1 时 q(A)=|A|，结论是普通并集计数。设 h≥2 且已知孩子树上的结论。令 Q=q(∪A_i)，b_i=q(A_i)。若 Q=0 或 Σb_i≥Q，无需证明。否则存在 Q 个孩子，每个孩子下面 ∪A_i 都含 Q 叉高 h−1 子树。对每 i，根的 q(A_i)=b_i 表明“孩子树 q(A_i∩L_child)>b_i”的孩子至多 b_i 个，否则可在至少 b_i+1 个孩子下各取 b_i+1 叉子树，组合出更大根子树。因为 Σb_i<Q，在上述 Q 个孩子中至少有一个孩子对所有 i 都满足 q_i(child)≤b_i。孩子归纳结论给该处的 union value≤Σb_i<Q，与其含 Q 叉子树矛盾。

此归纳也覆盖 a=1、空 A_i、重复 A_i；h=0 不在主域，不需要给 q 的叶辅助值另设约定。该结论与既存 `UM-PRIVATE-TREE-Q-VALUATION-v1` 的 raw 单树部分一致；没有新增 demand/oracle 合同。

## 2. bounded multiplicity 的 rainbow 与 blocker

令 f 为满 a 叉高 h 树的叶资源映射，每个资源出现至多 μ 次。按每个资源的 occurrence 固定顺序，把它的第 j 次出现放入第 j 个叶类，j=1,…,μ；不足的类留空。于是每个叶类本身 rainbow。这只是有限证明划分，μ 为 binary 大整数也不把 μ 的显式展开当作运行时间结论；实际非空类数不超过显式叶数。

全叶的 q 值为 a。由 (1)，某个类 q≥ceil(a/μ)，其对应子树为 rainbow。这立即给 μ2、a3 的任意高度 binary rainbow 子树，故不存在该参数的局部反例。

现固定 r∈[1,a] 且 t=μ(r−1)<a。设资源 X 命中所有 rainbow 满 r 子树。去掉 X 的全部叶逆像，留下 A=f^{-1}(Z\X)。A 中不含 rainbow 满 r 子树。再按相同 occurrence 方法把 A 划为至多 μ 个 rainbow 叶类 A_j；每个类 q(A_j)≤r−1，否则类内的 r 子树就是避开 X 的 rainbow 候选。由 (1)，q(A)≤μ(r−1)=t。

因此删除集 f^{-1}(X) 命中原满 a 树中的**所有 raw 满 t+1 子树**。满 a 叉高 h 树的这类叶 blocker 最少有

\[
 (a-(t+1)+1)^h=(a-t)^h
\]

个叶：若根处仍有至少 t+1 个孩子各自保留 t+1 子树，则根也保留；故至少 a−t 个孩子必须各自被阻断，按高度递归给下界并可递归达到。于是

\[
 |f^{-1}(X)|\ge[a-\mu(r-1)]^h.
\tag{2}
\]

这里没有把 raw 子树误当 rainbow 超边；(1) 和 occurrence 划分正是两者之间的额外桥。(2) 计数 raw 叶逆像，后续要与原共同 λ 的 multiplicity 容量相接，不应先除以 μ。

## 3. 共同 full-state λ 的 rainbow Haxell 匹配

先证明 Exact A 的纯选择部分，令树分叉数为 d。对每 root u、每真实 state s，枚举全部 rainbow 满 r 叉高 h 子树，取其真实资源集。每集恰 k=r^h 个不同外机。加上 root tag u，得到有限二部超图，总超边大小 k+1。重复超边可去重但保留一个真实 state／子树 witness。

对任意非空 I⊆U，设资源集合 X 命中所有 I-root 的候选边。按 (2)，每个 (u∈I,s) 都满足

\[
 |f_{us}^{-1}(X)|\ge B,
 \qquad B=[d-\mu(r-1)]^h.
\]

使用同一共同 λ 及其 multiplicity 容量，交换有限求和：

\[
\begin{aligned}
 B|I|
 &\le\sum_{u\in I,s}\lambda_{us}|f_{us}^{-1}(X)|\\
 &=\sum_{z\in X}\sum_{u\in I,s}
      \lambda_{us}|f_{us}^{-1}(z)|\\
 &\le|X|.
\end{aligned}
\tag{3}
\]

所以资源 transversal number 至少 B|I|。若 B≥2k−1，则它严格大于 `(2k−1)(|I|−1)`。对总超边大小 k+1，Haxell 条件恰为该常数 2(k+1)−3；因此有覆盖所有 root 的匹配。每条匹配边带一个真实状态和 rainbow r 子树，全部 root 的所有末资源互不相同。μ(r−1)<d 还保证每 state 至少有一个 rainbow r 候选，亦可直接由第 2 节局部结论看出。空 I 的严格条件自动满足。

本次外部定理实际亲核来源沿用已审 v1/v2：Annamalai, *Finding Perfect Matchings in Bipartite Hypergraphs*, arXiv:1509.07007v2，PDF 第2页／印第1页 Theorem1.1 及定义。该文 r-uniform 的 r 是**总边大小**，资源 hitting set 限于 B 侧；本次所有边恰 k+1，完全符合。原 PDF SHA256 `f6294a3b497e98d870ab47ceecb4a94a7e80457e9777114f59d88f321bc7dcce`。未取得／冒称重证 Haxell1995 原全文。

## 4. CONFIG(T) 的 a-tree 支配桥不要求单射

给 1≤T<2 的完整 CONFIG，写 s=⌊d(T−1)⌋、a=d−s。取一份有理可行边际点；v2 小型系统是有理系数，故可无损这样选择。

每内部机器有唯一 incoming unit job，边际 q_v；每 outgoing job 的 unit 下端边际为 t_e。含 incoming 的配置至多 s 枚父置 small，所以边际行满足

\[
 \sum_e(q_v-t_e)_+\le s q_v
 \quad\Longleftrightarrow\quad
 \sum_e\min(q_v,t_e)\ge a q_v.
\tag{4}
\]

外机至多放一枚 unit，故 Σ_leaf e:f(e)=z t_e≤1。这两个条件不需要 f 单射；同一 state 的不同 leaf jobs 若同外机，也逐 job 计入和。

每 root 按各状态根 selector 边际 y_us（和为1）选真实 state。按 v2 递归令根活跃质量 b=y_us。对已定义的 0<b≤q_v，逐项有 `min(b,t_e)≥(b/q_v)min(q_v,t_e)`，故总容量≥ab。可取有理 b_e≤min(b,t_e)、Σb_e=ab，分解 b_e/b 这一 uniform-matroid base vector 成恰 a 个孩子的随机子集；b=0 时后继全零。递归后，每 root 形成一个真实状态内满 a 叉高 h 子树的有限分布，每原叶活跃概率≤t_leaf。

各生成 a-tree 的叶资源映射可能重复，但仍每色≤μ，因为只是原完整 state 的叶子集。将每个正权生成树作为辅助 state，保留其原真实 state witness，取其每 root 分布权重为共同 λ_aux。每外机的期望请求按 multiplicity 为

\[
 \sum_{u,\mathrm{aux}}\lambda_{u,\mathrm{aux}}
  |f_{u,\mathrm{aux}}^{-1}(z)|
 \le\sum_{\mathrm{all\ original\ leaf\ }e:f(e)=z}t_e\le1.
\tag{5}
\]

辅助 state 的支持可为指数大小，但有限。不同 root 尚未互斥；这里只建立 (5)，没有把 LP 自身当整数调度联合分布。

将第 3 节纯组合选择论证应用于分叉数 a 的这些辅助树：候选只取其中的 rainbow r 子树，blocker 为 `[a−μ(r−1)]^h`。若满足 Exact B 的数值条件，Haxell 给出全 root 不交选择。该选择返回原真实 state 内的一棵 r 子树。辅助 a-tree 不是新物理输入，最终负载仍按原 d 个 outgoing jobs 及原时间 1/d 计算。

## 5. 完整原 P 的实际调度

selector 放在匹配选出的原状态根；选中 r 子树内的原 jobs 全下送到 unit 端，所有其它原 jobs 全父置，包括所有未选／零权 states 和同一原 d 树中未选分枝。

活跃内部机器恰一枚 incoming unit（根为 selector，非根为父 job）及 d−r 枚 small，负载 2−r/d。非活跃内部机器没有 incoming unit，其 d 枚 outgoing jobs 父置，总负载1。匹配边为 rainbow，且跨 root 不交，故每外机至多一枚选中 unit leaf。每原 job 恰排一次，所有端是原 P 合法端，完整 Cmax≤2−r/d。

这一步既不要求未选 state 注入，也不对辅助树之外的原 jobs 作删除；私有内部机器是承重条件。

## 6. 默认 r 与全配置整数间隙

令 `r=ceil[a/(μ+2)]`，则 `a≥(μ+2)(r−1)+1`，所以

\[
 a-\mu(r-1)\ge2r-1\ge1.
\]

对 h≥1、r≥1，凸性给 `(2r−1)^h+1≥2r^h`，于是 B≥2r^h−1，且 μ(r−1)<a。默认参数始终合法。

记 β=1/(μ+2)、α_μ=2−β、x=a/d∈(0,1]，T0=1+s/d=2−x。因为 r≥βa，

\[
 C\le2-\beta x\le(2-\beta)(2-x)=\alpha_\mu T_0
 \le\alpha_\mu T.
\]

中间差为 `2(1−β)(1−x)≥0`。T≥2 时原 P 的全部 port 父置且每 selector 任选状态根给实际 C≤2，亦符合 α_μT。非空 selector 排除 T<1。因而对配置阈值取下确界可得 OPT/T_conf≤α_μ；不要求无限阈值或概率极限操作。

μ1 恢复状态注入和 v2 的同一数值条件，α1=5/3；μ2 给 α2=7/4。这里不声称这两个界锐利。

## 7. 退化、复杂度与准确否定范围

- a1、r1 时超图总大小2，条件退化为 Hall；d1 的实际调度为1，允许任意给定 μ 上界只使 stated α_μ 松一些。
- h1 的 q 是叶数、blocker 为 a−μ(r−1)，全部推导成立。h0 不在模型。
- μ≥1 可以 binary 输入且远大于实际重数；无需按 μ 构造生产算法。资源实际重数从显式 leaf list 可数清；选择较松的 μ 只弱化数值保证。
- 空 U 是单独空任务情况，最优0；主链用非空 selector 下界1。
- Haxell 候选边族及辅助 a-tree 分布可能指数多，本 proof 只给有限实际见证的存在。没有把外部 fixed-rank、fixed-slack 算法套为变参位多项式 σ 构造。
- 均匀 private 结构的 CONFIG 小型系统与可行性算法不受本次 multiplicity 改动影响，但它们只计算分数阈值／作承诺判定，不替代实际 σ 输出。
- 固定 μ 得到常数 α_μ<2；一般 UM 的任意输入、共享内部机器、非均匀时间或 μ 随输入无界不被统一常数结论覆盖。
- 全部已用的 q 子可加、raw blocker、Haxell 与分数求和都明确扣除已有技术。本次新范围是 rainbow 候选与 bounded multiplicity 之间的桥及其全 CONFIG(T) 应用；全球新颖性和独立成文价值未认证。

Status：作者一般证明完成，待真正 Exact-first 独立重构与实际全文读后攻击；没有代码／有限运行证据；UM-TARGET-v1 正反面保持 OPEN。
