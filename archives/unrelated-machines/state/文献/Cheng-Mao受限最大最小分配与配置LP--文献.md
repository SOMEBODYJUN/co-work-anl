---
id: "unrelated-machines/cheng-mao-restricted-max-min-allocation-2019"
kind: "literature"
type_tag: "文献"
title: "Cheng–Mao 受限最大最小分配与配置 LP"
status: "source-read-retained"
summary: "Cheng–Mao 2019 对 restricted max-min allocation（受限 Santa Claus）给出相对于配置 LP 最优值的 (4+δ)-近似多项式时间算法，并用改进的 AFS 局部搜索把配置 LP 积分间隙上界收紧为 99/26；两项结论的算法/证明边界不同。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/cheng_mao_2019_restricted_max_min_allocation_v1.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/cheng_mao_2019_restricted_max_min_allocation_v1.pdf"
source_sha256: "ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a"
legacy_id: "arXiv:1905.06084v1"
external_status: "published-paper-resource; not independently re-proved here"
---

# Cheng–Mao 受限最大最小分配与配置 LP

## 来源和对象身份

冻结来源是 Cheng 与 Mao 的 *Restricted Max-Min Allocation: Approximation and Integrality Gap*，arXiv:1905.06084v1，PDF 28 页、768,864 字节，SHA-256 为 `ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a`。本次逐页读取摘要、引言、§2–§4、Appendix A/B/C 和参考文献；本页保存论文中的受限分配对象和作者定理，不把它改写成六人客户—提供者 SPE，也不把外部算法当作本仓库已实现程序。

论文研究的是给定玩家集合 (P) 与不可分资源集合 (R) 的 max-min allocation。资源 (r) 有固有值 (v_r\ge0)；玩家 (p) 若想要 (r)，得到 (v_r)，否则得到 0，即 (v_{pr}\in\{v_r,0\})。分配是把每件资源放给至多一个玩家，目标最大化最小玩家总值。该 restricted 模型是 Santa Claus / restricted max-min fair allocation 的算法对象。

## 配置 LP 和基准值

给定目标 (T)，玩家 (p) 的配置是其想要的资源子集 (C) 且
[
  \sum_{r\in C}v_r\ge T.
]
令 (C_p(T)) 为所有此类配置。配置 LP `CLP(T)` 的变量 (x_{p,C}\ge0) 满足
[
\sum_{C\in C_p(T)}x_{p,C}\ge1\quad(p\in P),\qquad
\sum_{p\in P}\sum_{C\ni r}x_{p,C}\le1\quad(r\in R).
]
(T^*) 是 `CLP(T)` 可行的最大目标。论文把 (T^*=1) 归一化；其对偶变量为玩家价格 (y_p\ge0) 与资源价格 (z_r\ge0)，约束为 (y_p\le\sum_{r\in C}z_r) 对全部 (p,C\)。LP 变量数可指数级，但文中沿用配置 LP 的标准近似/二分接口；本来源没有把该接口实现为仓库代码。

论文回顾：一般 max-min allocation 的 assignment LP 积分间隙无界；restricted 情形的配置 LP 间隙至少为 2。此前 AFS 局部搜索给出间隙至多 4 但没有已知多项式时间界；Annamalai–Kalaitzis–Svensson 等工作把时间改善到较差常数，Cheng–Mao 的第一定理在此基础上恢复接近 4 的多项式算法。

## 论文定理 1：(4+\delta) 近似算法

对任意固定常数 (\delta>0)，论文给出一个相对于 (T^*) 的 `(4+δ)`-approximation：输入配置 LP 的最优目标，输出一个实际资源分配，使每位玩家收到至少
[
  \frac{T^*}{4+\delta}
]
的价值。运行时间为
[
  \operatorname{poly}(m,n)\,n^{\operatorname{poly}(1/\delta)},
]
其中 (n=|P|)、(m=|R|)。论文说明可通过二分搜索目标 (T) 避免把 (T^*) 当作免费精确 oracle；二分/目标检查的接口仍是论文算法合同，不是本仓库的生产实现。

证明把目标归一化为 (T^*=1)，令
[
  \lambda=\frac1{4+\delta}.
]
资源分成 fat（(v_r\ge\lambda)）和 thin（(v_r<\lambda)）。fat 资源与玩家构成二分图；维护一个最大匹配 (M)。thin edge 是玩家和一组其所需 thin 资源的超边，若资源值和达到阈值且去掉任何一项后低于阈值，则称为 (w)-minimal。维护与 (M) 兼容的、彼此兼容的 thin edges 集 (E)，使 (M\cup E) 覆盖已经处理的玩家。

最大匹配的有向图 (G_M) 按匹配边由资源指向玩家、非匹配边由玩家指向资源。沿节点不交交替路径翻转 (M) 不改变最大匹配大小。论文的 Appendix A 用最大流/增广路径证明：对于未匹配玩家集合 (S) 和目标玩家集合 (T)，最大节点不交路径数 (f_M(S,T)) 可在多项式时间求出；在现有路径翻转后，若仍非最优，必有从未覆盖源到未覆盖目标的增广路径。

核心 Build/Collapse 框架交替维护层栈。每层 (L_i=(A_i,B_i,d_i,z_i))：(A_i) 是待加入的 blocked/addable thin edges，(B_i) 是当前 (E) 中阻挡它们的 edges；另维护与 (E) 兼容的 unblocked 集 (I)。Build 先加入可直接放入 (I) 的 (\lambda)-minimal edge，再加入被阻挡的 ((1+\gamma)\lambda)-minimal edges，并即时记录阻挡者。资源一旦被早期层、当前层/ (I)，或某阻挡 edge 与当前层重叠超过 (\beta\lambda) 覆盖，就标为 inactive；后续 addable edge 只能使用 active thin resources，形成 limited blocking。

Collapse 为 (I) 计算 canonical decomposition 和对应的节点不交路径，将可释放的 blocking edges 从 (E) 中删除，把 unblocked edges 加入 (E)，并清理被释放后可直接加入 (I) 的层内 edges。层在某一 canonical 分块中满足 (|I_i|>\mu|B_i|) 时可 collapse。关键不变量包括
[
 f_M(B_{\le\ell-1},I)=|I|,\quad
 f_M(B_{\le i},A_{i+1}\cup I)\ge d_{i+1},\quad
 |A_i|\le z_i,\quad d_i\ge z_i.
]

分析中选择
[
  \beta=\gamma^2,\qquad \mu=\gamma^3,
]
并令 (\gamma) 足够小，使由对偶可行性得到的严格正目标成立；论文说明 (1/\gamma=O(1/\delta))。若没有层可 collapse，Lemma 17 给出从底到顶阻挡边数的几何增长（例如 (|B_{i+1}|\ge \gamma^3|B_{\le i}|/(1+\gamma)) 的形式），并用签名向量的字典序下降限制状态数。Lemma 18 因而保证在
\(
\operatorname{poly}(m,n)n^{\operatorname{poly}(1/\delta)}
\)
时间内至少再覆盖一名玩家，反复进行直到全体玩家覆盖。

这项证明同时标出边界：令 (\beta=\gamma=\mu=0) 时退化为 AFS 的 4-近似局部搜索（时间未证多项式）；参数取大则接近更快但常数较差的既有策略。Cheng–Mao 的贡献是在两个极端之间只移动很小量，靠 layer-level node-disjoint paths、lazy update 和 limited blocking 取得任意 (4+\delta) 及多项式次数。

## 论文定理 2：配置 LP 积分间隙 (99/26)

论文另外改进 AFS 局部搜索的分析，取
[
  \lambda=\frac{26}{99},
]
从而由 (T^*=1) 得到一个实际分配，使每位玩家至少得到 (26/99)，即配置 LP 的积分间隙上界
[
  \frac{99}{26}=3+\frac{21}{26}\u2248 3.808.
]
该部分使用 Appendix C 的局部搜索 Build/Contract 方案；论文没有给出与定理 1 同等级的多项式运行时间界，故不能把定理 2 自动称为多项式算法。

其关键不“把所有 thin resource 价格设为 (v_r)”（该旧分析只覆盖 (\lambda\le1/4)），而是在当前交替栈 \(\Sigma) 中按 thin 值分段定义对偶资源价格：对 (v_r\in(0,\lambda/2))，
[
 z_r=\frac{3\lambda}{2\lambda+v_r}v_r;
]
对 (v_r\in[\lambda/2,3\lambda/4))，
[
 z_r=\frac{3\lambda}{3\lambda-v_r}v_r;
]
对 (v_r\in[3\lambda/4,\lambda))，取 (z_r=\lambda)。可达 fat resources 与可达 players 使用同一常数 (1-\tfrac{21}{26}\lambda)。对偶可行性按配置是否含 fat item、以及剩余 thin 资源的四种值区间分析；最关键的两项是：每个 thin edge 的总价格由最小资源价格控制，且逐层 charge 给 blocking edges 的总额不超过 (3\lambda|B_i|)。当所有层都阻塞时，reachable players、fat resource 和层中 thin resource 的价格总和给出严格正的对偶目标，故配置 LP 不可能仍可行；于是局部搜索必能推进。

该局部搜索以签名向量 ((|B_1|,\ldots,|B_\ell|,\infty)) 的字典序下降证明终止；终止调用次数至多 (n^n) 级别的上界（有限但不宣称多项式）。因此本定理保留两层状态：**完整结论**是积分间隙 (\le99/26)；**算法复杂度**仅有限终止，不能从它推出定理 1 的高效实现。

## 证据、复用和边界

- 本文是外部文献事实；本文实际读取了冻结 PDF 的全部 28 个 PDF 页，而不是只看摘要或仓库旧摘要。
- Cheng–Mao 的玩家、资源、配置、fat/thin、交替路径与受限分配均与 Santa Claus / hypergraph matching 资源对象同类，但论文没有提供客户—提供者历史、终局均分、六人 SPE 的量词，也没有给一般 unrelated-machines 的调度输出。
- 仓库已有的“逐资源正权畸变与 (\kappa) 边界”定理把 Cheng–Mao 定理 1 作为外部 restricted-Santa 后端；本页补充论文自身的完整算法结构和定理 2 的积分间隙分析。该引用关系是“外部算法合同/来源”，不是从论文直接得到六人半覆盖结论。
- 论文只处理每个资源对玩家是 (0) 或统一 intrinsic value 的 restricted 资格。不能将 `4+δ` 自动迁移到每个玩家对同一资源都有不同正值的一般 max-min allocation，也不能把 (99/26) 当作一般不相关机近似比。
- 本页不声称已实现配置 LP oracle、Build/Collapse 后端或独立复证论文全部证明；后续若把算法接入仓库，应另建 `tools/evidence` 实现并记录输入位长、目标搜索、失败证书与完整任务解码。
