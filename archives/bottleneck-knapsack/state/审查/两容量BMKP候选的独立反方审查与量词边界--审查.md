---
id: bottleneck-knapsack/two-capacity-bmkp-independent-adversarial-review
kind: review
type_tag: 审查
title: 两容量BMKP候选的独立反方审查与量词边界
status: candidate-algorithm-modules-rechecked-total-proof-open
truth_status: three-conditional-modules-supported; whole-algorithm-unverified
review_level: full-source-read-final-parameter-alignment-and-scope-audit
scope: "两种容量的预算多重背包（BMKP）(2/3-epsilon) 候选；允许unused，硬容量，不涉及玩家均衡"
summary: "完整实读 bmkp_algorithm_review.md。联合类型critical恢复、嵌套short matching和允许弃置的4pmax LP舍入各有条件证明；最终参数已对齐为 zeta=1/ceil(max(100,20/epsilon))、q_pre=2/3-8zeta、Q=2/3-11zeta、最终下界2/3-16zeta。母Lemma8输入提取、整稿联合覆盖、边界处理、通用实现和新颖性仍未闭合，整体保持候选算法。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/cross_field_battle/bmkp_algorithm_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/cross_field_battle/bmkp_algorithm_review.md"
---

# 两容量BMKP候选的独立反方审查与量词边界

本文完整实读冻结来源 bmkp_algorithm_review.md（11,019 bytes，SHA-256 abc7d53cea8c7b83a9236f4a3f31aff39457c70fa04eda3e92554e3f92c63db0），并与现有[双容量BMKP候选的三模块与完整目标](../资料/双容量BMKP候选的三模块与完整目标--资料.md)、广义指派资源对象和有限 toy 审计比较。原文审查对象是 generalized_assignment/TWO_CAPACITY_LEMMA.md 的最终落盘稿，结论明确是“有希望的候选，非已证定理”。本页保留该状态，不因模块证明或母文献标签改变整个算法的数学身份。

## 1. 模型、量词和模型分离

输入是物品集合 \(E\)，每件物品有公共正有理重量 \(w_e\)、非负有理利润 \(p_e\)，每件物品至多使用一次；包容量属于 \(\{B_1,B_2\}\)，其中 \(0<B_1\le B_2\)，容量比没有上界，物品允许 unused。目标是选择互不交的包集合，使硬容量不超载并最大化各包利润最小值：

\[
\max \min_j p(S_j).
\]

这是中央优化问题，没有玩家、偏离、延迟或 NE。它不能从 weighted-congestion 的近似纯均衡存在界、设施客户模型或其他资源拥塞对象自动继承算法结论。两容量候选也不解决固定容量类型 \(K\ge3\) 的完整目标。

目标是每个固定 \(\varepsilon>0\) 给出确定性、总输入位长多项式时间的 \((2/3-\varepsilon)\)-近似。所谓总算法必须同时给出：未知最优值的有限阈值搜索/单向 oracle、每容量 profile 的结构提取、联合类型和 global-critical 选择、short matching、cheap LP 舍入、所有容量/利润/unused 边界的联合证明，以及可执行实现。单独验证其中一个模块不能推出整个 BMKP 目标。

## 2. 三个条件模块

### 2.1 L1：联合类型与 global-critical 恢复

固定有限联合类型 \(\tau\)，把两容量的标签、适用状态、heavy/light、expensive 标志和同宽利润桶都放进同一类型；同类型在每个容量上有相同的上舍入重量 \(u_\tau\)。每个 long bin 的全部 expensive 物品必须是 critical，且每个 long 至多 \(K\) 件，short 至多两件。对每种 \(\tau\)，按所有 long 的总需求选全局最重的 \(N_\tau\) 物品作 critical，交换被换出的旧 critical 与更重的候选物品：

* 更重物品只能原先在 short 或 unused，不能藏在 long 的“非critical expensive”位置；
* 放入 long 后保持同型标签、容量和利润桶；
* 若物品原在 short，则把更轻旧物放回 short，单槽利润损失小于一个桶宽 \(\delta\)；
* 两容量不能各自独立挑重物再拼接，因为同一物品供给只能使用一次；只能在联合需求上做全局交换。

该模块证明的是：**在已有合法 profile/slack 见证和全局 expensive 标记的前提下**，critical 规范化不损坏两容量结构。它不负责从任意输入生成 profile、证明每个 long 的昂贵项数上界，也不负责短包匹配或 cheap 舍入。

### 2.2 L2：嵌套 short matching

给未占用 critical 的 expensive 池、short 数量 \(m_1,m_2\) 和共同利润阈值 \(Q>0\)，加入 \(m_1+m_2\) 个独立 dummy。两物品组成的边若重量和不超过 \(B_2\)、利润和至少 \(Q\)，则为大容量可行边；若还满足 \(B_1\)，边权记为1，否则记0。singleton 通过不同 dummy 表示。

全部 short 可分配，当且仅当存在大小 \(m_1+m_2\) 且至少 \(m_1\) 条权1边的 matching。方向一把 \(m_1\) 条 small-eligible 边给小容量包，其余给大容量包；反方向由任意 short 分配直接生成这样的 matching。故可用固定基数最大权 matching，不需要一般 Exact Matching。这里 \(Q>0\) 排除 dummy-dummy；empty critical 配置仍须作为合法类型计数，不能直接当 short。

### 2.3 L3：允许 discard 的 \(4p_{\max}\) LP 舍入

给物品 \(e\) 非负重量/利润 \(w_e,p_e\)，包容量 \(B_j\) 和利润下界 \(t_j\)。若

\[
\sum_jx_{ej}\le1,\quad
\sum_e w_ex_{ej}\le B_j,\quad
\sum_e p_ex_{ej}\ge t_j,\quad x\ge0
\]

的 LP 可行，则存在多项式时间整数包 \(T_j\)，允许 unused，容量不增且

\[
p(T_j)\ge t_j-4p_{\max},
\qquad p_{\max}=\max(\{0\}\cup\{p_e\}).
\]

证明取残 LP 极点。固定所有 \(x_{ej}=1\) 的物品并移除；只看真分数变量。若某物品的列和约束紧，则它至少与两个正分数变量相连，故紧列数 \(N\le E/2\)，其中 \(E\) 为真分数边数。极点活跃行数给 \(E\le N+2M\)，\(M\) 为未完成包数，因此 \(E\le4M\)，总有一个包至多四条真分数边。结束该包时舍弃其分数份额，只保留已固定整件，利润损失至多四件的分数利润，即不超过 \(4p_{\max}\)。移除该包但保留其分数物品，其他包的列和约束只会放松；重复至所有包结束。每轮固定物品或结束一个包，步数及有理 LP 位复杂度多项式。

这是允许 unused 的舍入证明。若要求每件物品必须恰分一次，合同会失败：一件重量2的物品、两个容量1包、每边取 \(1/2\) 的 LP 分数可行，但不存在完整整数覆盖。该反例只否定字面全覆盖子合同，不否定允许 discard 的 BMKP 主目标；当前候选已自立 L3，不再依赖母 Lemma22 的全覆盖字面表述。

## 3. 最终参数对齐及旧异议处置

最终版本使用

\[
\zeta=\frac1{\lceil\max\{100,20/\varepsilon\}\rceil},\quad
U=1-\zeta,\quad \gamma=U\zeta,\quad
\delta=U\zeta^2,\quad K=1/\zeta,
\]

\[
q_{\mathrm{pre}}=2/3-8\zeta,\qquad Q=2/3-11\zeta.
\]

阈值 \(T\) 先做利润 cap \(p_e\leftarrow\min(p_e/T,1)\)，使用单向 gap oracle：若 \(OPT\ge T\)，某个枚举轮必须成功；成功只保证输出利润至少 \(qT\)，不能反过来把成功当作 \(T\le OPT\) 的双向判定。未知最优的几何网格公比为 \(1+\zeta\)，最终 cheap 舍入损失至多 \(4\zeta\)，故候选预算下界为

\[
Q-4\zeta=2/3-15\zeta,
\]

网格后至少 \(2/3-16\zeta\ge2/3-\varepsilon\)。

反方稿早期的 \(q_{\mathrm{pre}}=2/3-6\zeta\)、\(2/3-13\zeta\) 和 \(\zeta\le\varepsilon/16\) 只属于探索历史，最终对齐已撤回，不能重新作为当前阻断或当前保证。以下旧异议在最终稿中已声明修复，但修复声明仍需整稿联合核验：

1. 未 cap 利润会使 \(\lfloor p/\eta^2\rfloor\) 类型数量随输入数值增长；最终稿先 cap。
2. BMKP 允许 unused，cheap LP 必须使用 \(\sum_jx_{ej}\le1\) 或 discard dummy；不能强迫所有剩余物品进入真实包。
3. 母 Lemma8 的高利润前提与 singleton 预算需一致；最终稿在 q_pre=2/3-8ζ 处分 high singletons，保留 \(Q=2/3-11\zeta\) 的保守阈值。
4. profile 数、joint-type 数、configuration 数必须只依 \(\varepsilon\) 和固定容量类型数，不能随输入数值或容量比指数增长。
5. heavy-cheap 删除、\(K=1/\zeta\) 规范化、两容量物品供给和 cheap/expensive 两池不交，都必须在结构变换后逐条保持。

因此，当前审查不再把这些旧数字异议列作 fatal；但“已修复”不是“已完成总证明”，仍要逐行检查最终稿中的 profile 输入和联合覆盖。

## 4. 仍未闭合的承重义务

整体状态仍为候选算法，原因不是 L1–L3 已发现反例，而是它们尚未被证明可在同一输入上联合调用：

* 母 Lemma8 的输入提取、容量缩放、利润归一、short/profile 符号和 no-heavy-cheap 条件尚未逐行接入；
* 未知 \(OPT\) 下按容量分组、产生 short、对剩余组调用 Lemma8 的结构引理尚未完整写出；
* 所有 labels、无限标记、unusable items、empty critical bins 和无效类型的完整枚举域未给出可执行合同；
* 需要证明命中某轮结构见证后，具体物品能按同型 slots、short matching 和 cheap LP 同时分配，并把每一项利润损失计入最终 \(2/3-\varepsilon\) 预算；
* 需要给出小规模真实实现，枚举容量4–8及两容量中间不变量，审计的不只是最终 OPT，而是每个 profile、matching、critical 交换和舍入步骤；
* 零利润、零 OPT、空类别、\(B_1=B_2\)、无合法 label、重物品删除后的边界尚未形成整稿统一证明；
* 新颖性、发表价值和母文献结论不能由内部候选审查替代。

已有 toy/有限证据（例如 generalized_assignment toy audit 的有限枚举、联合交换和参数网格）只能核验局部合同，不能证明固定 \(\varepsilon\) 对所有输入的总位多项式算法。它们也不能把 discard 舍入引理之外的 profile 提取自动认证。

## 5. 与现有档案的关系和处置

现有资料对象保留三个模块、最终参数和固定 \(K\) 开放目标；本审查正文补充反方来源独有的最终版本对齐、旧异议撤回、L3 完整证明和整稿未闭合义务。两者不能合并成“已证 BMKP 定理”。相关广义指派费用保持和舍入资源对象只提供背景，不承载 BMKP 的联合类型或容量量词。

本源处置为 integrated 到本文。其独有内容去向如下：L1/L2/L3 的条件化证明与 L3 的全覆盖反例保留在本页；最终参数接入现有 BMKP 资料页；旧参数与旧异议明确标为历史；母 Lemma8、联合覆盖、实现和新颖性仍标 open。第三阶段可把本页与三个模块建“条件支撑/边界审查/候选依赖”关系，不能建立“模块合取即总定理”的无条件边。
