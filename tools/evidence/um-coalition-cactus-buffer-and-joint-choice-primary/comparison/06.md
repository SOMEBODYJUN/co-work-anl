---
id: "unrelated-machines/cactus-configuration-gap-and-bounded-slot-rounding-review"
kind: "review"
type_tag: "审查"
title: "仙人掌配置间隙与有界配置槽舍入双源审查"
status: "exact-conditional-results-integrated"
truth_status: "restricted cactus gap, block-rank exact algorithm, and fixed-K slot-margin theorem retained; general UM target remains open"
review_level: "full-source-read-proof-and-audit-comparison"
scope: "high-girth cactus configuration gap, support-two exact block-rank solving, pseudoforest configuration exactness, and bounded configuration cardinality slots"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/cactus_configuration_gap_and_block_exactness.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md"
---

# 读取范围与两个对象的分离

本审查逐项读取两份 current 正文、其中引用的精确审计/独立 review 入口，并比较定义域、量词和冻结增量。稳定 ID/SHA 为：`c6dd1d5f29678d0d810e`，`cactus_configuration_gap_and_block_exactness.md`，SHA `350a816a8eb003dc214dd016a5f0abb8adda5ee570ff85ed32788b5c6578c78f`；`e2b3620eddc4b8ac56bd`，`bounded_configuration_cardinality_slot_margin.md`，SHA `14c1b00b50a8b87f9aa30e5bbe77300516943a60e68073b123582e074ffe79f4`。两份均有 legacy/main 绑定，按一个冻结路径版本计数。

第一源是 support≤2 的图结构边界：有限给定围长的 cactus 配置 gap、块环秩精确算法和单环连通分量配置 exactness。第二源是固定 (K) 的“每个正权配置至多 K 个任务”槽包络余量与承诺算法。前者强调 LP gap 不等于真实计算困难，后者提供受限正面舍入；不能把二者拼成一般 UM 算法。

## 1. 高围长 cactus 配置间隙与 support≤2 精确算法

对任意 (k\ge2,g\ge3)，第一源构造每个任务恰有两个可用机器、处理时间只取 (1/k,1)、机器图为围长恰 (g) 的简单 cactus，使
\[
OPT=2-1/k,
\qquad T_{CONF}=1+1/k
\]
有显式配置证书，故相对 gap 上确界趋近 2。下界沿两棵 k 叉树把根间任务的单位负载逐层下传；到末层后，每个附着 g 环在 makespan<2 时至少一条端点任务落在末层机器，d=k-1 个环贡献 d/k，达到 (2-1/k)。上界是实际路径调度和每个环的局部安排。配置证书用循环窗口，每行仅 O(k) 配置项，逐任务边际精确为 1/2；根间任务边际达到 1/2 后再拆分配置。

这证明的是受限结构中的锐方法障碍，不是一般 hardness。正文随后给出 support≤2 的带标签机器多重图块参数 (b=max_B(|E_B|-|V_B|+1)) 的精确算法：每个双连通块枚举 (2^{b_B}) 条反馈边去向，剩余森林用叶到根的最小父端负担消息；块割树消息可组合，整体时间 \(2^b\operatorname{poly}(L)\)。任务标签必须保留，不能把平行任务合并，否则会错误地把 Partition 型弱 NP-hard 实例宣称为精确可解。

同一源还给出单环连通分量（总环秩可多，但每个连通分量至多 1）的配置 LP exactness：叶剥离后剩余单环在某端不 fit 时强制删边，否则沿环统一定向，得到实际 T 调度。这个精确性不能放大到任意 cactus：前述 cactus 族在同一连通分量有多个环，仍保持配置 gap 近 2。

复杂度边界明确：若 support≤2 且输出图的 (b=O(\log L))，该算法使近二 hardness 归约落入位多项式精确求解，P≠NP 下归约必须逃出该参数或提高 support；但 (b) 无界并不自动给 hardness，且高围长/深树/大量局部环本身不足。

## 2. 有界配置基数的统一槽余量

第二源固定整数 (K\ge1)，给定合法 UM 输入、(T\ge0) 和显式 CONFIG(T) 点。先把有零边任务独立处理并从配置中删除；只要求每个正权配置至多含 K 个任务，不限制所有本地可选任务或所有最优调度的基数。对每行建立非增处理时间单位槽并用同一全局匹配兑现覆盖，得到
\[
L_i\le E_i\le (2-K^{-(K-1)})T\quad(K\ge2),
\qquad L_i\le E_i\le T\quad(K=1).
\]
K=2、3 的包络界分别为 (3T/2,11T/6)，并给出 K=4 的构造性下界 47/24；K=5 的显式槽包络 (287/144=2-1/144) 反驳了更强但错误的 (1-1/K!) 余量猜想。

证明将每行的正边际槽数压到 (q\le K)，按阈值把任务归为 (d=q-1) 个整数类型。槽交叠的严格正交长度给出所有前缀类型均值 (H_t>t)。在整数类型多面体中，Abel 求和使任意非零顶点满足总坐标和严格小于 1；活约束行列式由 Hadamard 限制为 (K^d)，Cramer 法则给统一缺口 (K^{-d}\ge K^{-(K-1)})。这一步需要严格正交长、最早阈值归类和完整的槽匹配；不能把任意 LP 点或独立局部匹配当作同一个全局覆盖。

该结果给出固定 K 的确定性有理匹配构造，实际输出位多项式；但一般 CONFIG LP 仍不是免费 oracle。另立身份 `UM-BOUNDED-CARDINALITY-PROMISE-APPROX-v1` 只在承诺“存在某个普通 OPT 调度，每机至多 K 个无零边任务”时枚举大小≤K 的行子集和断点阈值，再解显式有理覆盖 LP，得到固定 K 的比例保证。K 随输入增长时，余量和枚举都失去统一多项式性；只限制大任务而另收费 tiny 任务也不能直接套用。

## 与既有存档的关系、处置和缺口

1. **与配置 cover/消元障碍：** cactus gap 说明配置 LP gap 可以在任意指定围长下保持；但 support≤2 的块算法说明同一类可能精确可解。两者共同阻止“gap 大 ⇒ hardness”的跳步。
2. **与上列 +B 舍入：** bounded-K 槽余量是给定 CONFIG 点的全局匹配余量，依赖配置基数和整数类型；它不替代 upper-column 的一般非负列预算，也不提供任意输入的结构承诺。
3. **冻结与审计：** current 正文分别链接 cactus generator/精确 solver、独立 oracle 和 K2–K5 槽审计。有限运行只核列明参数；k≥5 的 cactus 只核参数恒等式，不能写成全实例穷举。

**保留结论：** cactus 围长 gap 族、support≤2 的 (2^boperatorname{poly}(L)) 精确算法、单环连通分量配置 exactness、固定 K 的 (2-K^{-(K-1)}) 槽余量和 K=2/3 锐界。

**未解项：** 一般 support、无 K 承诺的 CONFIG 舍入、跨多个环的全局兼容、选定接线族的 hardness、外部新颖性/同行复核和 `UM-TARGET-v1` 正反面仍开放。不能把高围长 cactus、固定 K 或 block-rank 算法宣称为一般 UM 结论。
