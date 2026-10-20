# 公共基交换有向图的围长距离界与原子博弈接口

用途：把原子博弈论文末尾的明确猜想压到一个纯拟阵引理，保存完整证明候选、独立攻击和精确审计。不是用有限实验宣布猜想解决，也不宣称全球新颖性。

## 题源、数学身份与目前等级

来源 A：[Hao–Michini, Price of Anarchy in Paving Matroid Congestion Games](https://optimization-online.org/wp-content/uploads/2023/11/TEAC_Matroid.pdf)，§6，印刷页19–20。原文令公共拟阵秩为 k、最小回路大小为 g、δ=k−g，猜对 δ≥0 能以 α=z(D)^{2(δ+1)} 满足 Theorem 3.1 的交换流端点条件。该定理本身适用于一般公共拟阵，而非只限 paving。

本轮派生问题 C 是更强的纯组合合同。下述证明由 atomic_games 独立提出；root 逐步核查并另外枚举全部小抽象拟阵；fair_chores 在未读该证明前，从反向 BFS 独立重构了另一证明。当前状态是**自足证明候选，已有独立重构；新颖性与完整文献覆盖未闭合**。本文件留在选题目录，未进入可靠新定理层。

### SEL-MATROID-EXCHANGE-DISTANCE-v1

- Objects/Domain：有限拟阵 M=(E,I)，秩 k；若 M 有回路，g 是所有回路的最小基数。任意非空有限公共基列表 B_1,…,B_N；允许重复、loop、coloop、平行元和非连通。
- Definitions：D 的顶点为 E；r→s 当且仅当存在 i 使 r∈B_i、s∉B_i 且 B_i−r+s 为基。距离为有向最短路的边数。
- Exact statement/Quantifiers：对每个上述 M、基列表和每个不同的可达 u,v，dist_D(u,v)≤k−g+3。无回路的自由拟阵没有交换弧，另作空断言；空 ground set 亦然。
- Conclusion/Scope：只对完整可行单交换图成立；不能换成任意被删弧的子图。不是基图上两个基之间的距离命题。
- Dependencies：基本回路交换刻画、拟阵闭包与秩。
- Evidence：下面一般证明；独立反向 BFS 重构；全抽象小拟阵审计。
- Objections：尚未排除它是已有交换图引理；任何应用仍须逐项核对输出、成本和原定理合同。
- Related Files：[独立审计](../probes/matroid_exchange_diameter_independent.py)、[冻结输出](../probes/results/matroid_exchange_diameter_independent_20261020.json)。

## 前向距离层证明

固定可达的不同端点 u,v，令 L=dist(u,v)，并固定最短路 x_0=u,…,x_L=v。令 d(e)=dist(u,e)，不可达时 d(e)=∞；对整数 j≥1 令 H_j={e:d(e)≥j}，不可达元素也包括在内。

**闭包包含。** 对每个给定基 B_i 与 j≥1，

H_{j+1} ⊆ cl(B_i∩H_j)。

若 s∈H_{j+1}∩B_i，则结论显然。否则取基本回路 C(s,B_i)。每个 r∈C(s,B_i)−s 都能交换 r→s。如果 d(r)≤j−1，就会有 d(s)≤j，矛盾。因此 C(s,B_i)−s⊆B_i∩H_j，故 s 落在其闭包中。这个论证也覆盖 d(s)=∞；loop 的基本回路为单点，落在 cl(∅)。

**严格秩下降。** 对每个 1≤j≤L，最短路第 j 条边 x_{j−1}→x_j 由某个 B_i 见证。因为 d(x_{j−1})=j−1，该元素不在 H_j；又 d(x_j)=j，所以 x_j∈H_j 且 x_j∉B_i。交换可行性说明

(B_i∩H_j)∪{x_j} ⊆ B_i−x_{j−1}+x_j

是独立集。因此 |B_i∩H_j|≤rk(H_j)−1。结合闭包包含，得到 rk(H_{j+1})≤rk(H_j)−1。

若 L≤1，因有回路时 g≤k+1，结论直接成立。若 L≥2，考虑最后一条边的见证基 B_i。基本回路 C(v,B_i) 中每个非 v 元素 r 都有弧 r→v，故 d(r)≥L−1；v 自身也在 H_{L−1}。于是该回路完全包含于 H_{L−1}，得到 rk(H_{L−1})≥g−1。

将 j=1,…,L−2 的秩下降相加：

g−1 ≤ rk(H_{L−1}) ≤ rk(H_1)−(L−2) ≤ k−L+2。

移项即 L≤k−g+3。所有计算均为有限整数秩，无概率或数值近似。

独立反向闭包证明与审查范围见[独立重建](matroid_exchange_distance_independent_review.md)。此审查只认证其所述组合合同，没有认证新颖性或PoA应用。

## 交换流成本接口：正在核查的推论

固定对称、非加权原子拥塞博弈：每个玩家选同一个 M 的基；非负非减延迟 d_e，纯 Nash 状态 f。记 c_f(e)=d_e(f_e)，c_f^+(e)=d_e(f_e+1)，只在负载范围内定义，必要时将 d_e 在 N 处常数延拓。若存在统一 z≥1，满足所有已使用资源的 c_f^+(e)≤z c_f(e)，则每条交换弧 r→s 有 c_f(r)≤c_f^+(s)。

任意最短 u→v 路的内部顶点都有出弧，故是已使用资源。串联上述不等式给

c_f(u) ≤ z^{L−1} c_f^+(v) ≤ z^{k−g+2}c_f^+(v)。

零延迟用乘法不等式表达，不除以零。终点 v 不必已使用。Hao–Michini Theorem 3.1 的交换流每条路径都在 D 中，因此其端点满足此合同；它**不要求**把真实流路缩短成最短路，故不更改流量或容量。依该定理可导出候选上界 PoA≤ρ(D)z(D)^{δ+2}。δ≥0 时 δ+2≤2δ+2；δ=0 恢复其 paving 指数，δ≥1 严格改善猜想的指数（z>1 时）。

**应用尚待完成的检查：**完整重写原文 z(D)、ρ(D) 的函数域和零成本约定；论文原猜想及后续工作的覆盖；这种界在哪些延迟/δ区间优于已有一般 PoA，而非只是形式上改善。对 affine 或固定 rank 不应凭公式外观称有意义的改进。没有提供 PNE 计算算法或 UM 近似算法。

## 独立有限审计与反算

运行：`python3 research/topic_selection/probes/matroid_exchange_diameter_independent.py --max-n 5 --output <新的输出路径>`。既有冻结输出不可原位覆盖。

程序枚举 n=0,…,5 的每个等基数非空子集族，以完整 basis-exchange axiom 筛出所有带标号抽象拟阵。每个拟阵枚举基的所有非空子集作为 profile；重复基不改变 D。再从每个源逐层 BFS，检查所有可达不同端点。

实际总计：498 个拟阵、28,424 个 profile、18,833 个按每个拟阵分别去重的 D、242,976 个可达有序端点检查，全部通过。root 另从各 n/rank 分层重新求和反算四个总数，并重算 witness 的 δ、距离与界。loop、coloop、零秩、自由拟阵包含在枚举内。数目是本次有限运行的覆盖，不是证明规模或成功概率；n>5 由一般证明承担。

## 选题价值与下一判别

该方向同时属于明确问题、工具和结构参数扩类：不是凭空提出一个更强猜想，承重义务确实落在原文交换流工具内。若查新通过，距离引理及成本推论是可复用的机制。当前不能直接称可发表：须检索 matroid union/partition 的交换图最短路文献、检验界的锐性，以及找出原 PoA 界之外真正非平凡的应用区间。若距离界已有且成本应用为直接推论，则降低新颖性判断，保留重构资产并回到候选比较。
