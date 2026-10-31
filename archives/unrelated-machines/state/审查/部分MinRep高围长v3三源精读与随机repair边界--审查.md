---
id: "unrelated-machines/partial-minrep-high-girth-v3-source-review-20261031"
kind: "review"
type_tag: "审查"
title: "部分 Min-Rep 高围长 v3 三源精读与随机 repair 边界"
status: "complete-source-read-proof-independent-reconstruction-integrated"
truth_status: "scoped-random-high-girth-source-bridge-no-UM-compiler"
review_level: "clean-show-full-read-cross-object-comparison"
scope: "UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3 Exact、frozen Proof、independent PCSP reconstruction"
summary: "三源共同描述固定 G 的随机高围长 regular partial-Min-Rep source：d layers 的独立 fiber permutations、cheap copy-list 同时 soundness、短环 Markov 控制、同 type/layer 远距交换 repair、bounded-bit FAIL 语义。Proof/独立重构闭合了 permutations 的 factorial-moment 上尾与 repair 误差；结论仍只是随机源桥，未提供一般 UM compiler、near-2 hardness 或外部 PCP 新颖性。"
source_refs:
  - "source:1c819f90cbdf32403533:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_exact_source.md"
  - "source:2e5ff24a44855e211d1e:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_frozen_proof_source.md"
  - "source:cc0f0eb857be2b2eef76:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_independent_pcsp_source.md"
related_objects:
  - "../审查/部分MinRep费用桥与pDM阈值双源审查--审查.md"
  - "../审查/部分MinRep度数质量v4-v5陈述与域修复补充--审查.md"
  - "../审查/坐标切片v4双独立重构与阈值增补接续审查--审查.md"
  - "../审查/高围长来源与随机lift量词边界--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/partial-minrep-high-girth-v3-sources-20261031/"
---

# 1. 来源身份与全量阅读

三源均先 `clean claim`，再 `clean show --out` 全文读取。两冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`、`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 内容相同。

| ID | 路径 | 字节 | SHA-256 |
|---|---|---:|---|
| `1c819f90cbdf32403533` | `partial_minrep_regular_high_girth_v3_exact_source.md` | 4,408 | `0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61` |
| `2e5ff24a44855e211d1e` | `partial_minrep_regular_high_girth_v3_frozen_proof_source.md` | 7,496 | `f43e32fa61899de87121c161e3ca51ac76dbaa47daccef5fce7a02ba8609e646` |
| `cc0f0eb857be2b2eef76` | `partial_minrep_regular_high_girth_v3_independent_pcsp_source.md` | 10,631 | `f9c965c6a8b608ba088e135444c4cc8f19c7ed36798b5259c397b84b09b26396` |

现有 `部分MinRep费用桥与pDM阈值双源审查--审查.md` 已整合同一 v3 结构和域边界；本批新增 history/source 的 Exact/Proof/independent provenance，不新建第二个 source bridge。

# 2. v3 Exact 的对象、参数和随机算法

输入是显式无权平衡 (D)-regular 二部全投影游戏，允许平行 edge types；每边投影表显式，字母表 (Sigma) 大小 (Q\ge2)。参数固定 (G\ge2)、(g\ge2)、有理 (0<\rho\le1)、(Q\gamma\ge1)，其中

\[
\ell=\lfloor\log_2g\rfloor,
\quad\lambda=1+\lceil\log_2Q\rceil,
\quad\tau=\rho/(100g^2),
\quad\gamma=\rho^3/(10^9g^8),
\]

\[
d=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
\quad S=\sum_{l=2}^{G}d^l,
\quad B=40NS,
\quad U=\sum_{j=0}^{G+1}d^j,
\quad m_*=dN/2,
\]

并取 (z\) 足够大、(t=Dz)。先建立每个原 edge type 的 canonical template matching，把每条 type 分成 (z) slots；再对每层/每原顶点独立抽 length-(t) uniform permutation，得到 d-layer union，保留 layer/type 标记。

算法枚举长度 (2\ldots G) 的 simple cycles（平行 edge 计 2-cycle）。若短环数超过 B 返回 FAIL；否则每次在同一 `(original edge type, layer)` bucket 中找一条不在短环、且两端距待修边两端都大于 G 的 clean edge，交换两个 matching endpoints，直到没有短环。FAIL、随机位上限、固定 G 的复杂度和 `Qγ≥1` 域均是 Exact 量词的一部分；不能把 FAIL 图伪造为高围长输出。

## 2.1 Exact 四项结论

1. 非 FAIL 输出是 balanced、simple、d-regular、girth (>G) 的显式游戏，所有边继承原 edge type 投影；复制原 perfect assignment 给每个 copy 可保持 YES complete。
2. 所有合法输入 FAIL 概率 (<0.1)。
3. 若 (operatorname{val}(\Pi)\le\gamma)，至少 (0.8) 概率返回 non-FAIL，且所有 cost (le gN') 的 copy lists 同时覆盖严格少于 (
ho M') 条边。
4. 固定 G 时总时间、输出规模、随机位关于显式图/投影和 binary (g,
ho) 多项式；G 变参允许指数依赖，不隐藏在“poly”中。

Exact 明确声明：这是随机 source bridge，不是一般 UM compiler、near-2 hardness 或 PCP 新颖性定理。

# 3. Proof/独立重构的承重步骤

## 3.1 cheap copy-lists 同时平均界

固定任意 total cost (le gNt) 的 copy-list assignment，允许同一原顶点的 copies 完全不同。heavy list 长度 (>H=4g/\tau) 的 copies 只占端点概率 (le\tau/2)。从每原顶点均匀抽一个 copy，再从非空 list 均匀抽 label，若 light-covered 原 edge 的平均 value 达到 (\tau/2)，则得到单标签赋值 value 至少

\[
\tau/(2H^2)=\rho^3/(32\cdot10^6g^8)>\gamma,
\]

矛盾。因此任意 cheap copy-lists 的模板边 covered 边际平均小于 (	au)，没有把平均 copy list 偷换成一个旧 game 的单一列表。

## 3.2 permutations 的联合上尾

真正难点是同一 permutation 内部存在无放回相关，不能把 covered edges 当独立 Bernoulli。Proof v3 用两种等价表达：

- factorial-moment 路线：(r) 个不同 slots 的 permutation images 相对独立 samples 的点态密度至多 (e^r)，给 (k) 边同时 covered 概率上界 (e^{2k}\prod q_e)，再用
  [
  E\binom{Z}{k}\le(e^2\mu)^k/k!
  ]
  做 Chernoff/MGF；
- 独立重构先用 edge-coloring 从覆盖边中抽一个 bounded-degree witness (F)，再逐步暴露两侧未使用 images，每步条件概率至多 (4p_e)，通过 union bound 控制全部 lists。

两种路线都保留左右 fiber permutations 的真实相关性，不假定 matching 指示量独立。结合 lists 数

\[
K\le\exp(gNt\lambda),
\]

以及 (d\ge1000g\lambda/(\rho\ell))、(ln g\ge\ell/2)，得到对所有 cheap copy-lists 的同时坏事件概率 (<0.001)（Exact 只要求 (<0.2)）。

## 3.3 短环期望和 bounded-bit FAIL

每层是 perfect matching；长度 (l) 的实际环必须相邻 layer 不同，(l=2) 正确解释为不同 layer 的 parallel edges。Proof 逐步揭 fresh permutation images，得到

\[
E X_l\le NtS/(t-G)\le2NS,
\]

故 (X>B=40NS) 的概率 (<0.05)。Fisher–Yates 使用固定 (R) 次 fair-bit rejection；总 sampling FAIL (le0.001)。条件于所有 draw 成功，接受值仍是独立 uniform，故最终 FAIL 概率 (<0.1)，NO 侧 good 概率 (>0.9)，强于 Exact 的 (0.8)。

## 3.4 同 type/layer repair

同一 bucket 始终有 (z) 条 matching edges；短环边占用至多 (GB)，端点 G-balls 贡献至多 (4U)，而 (z>GB+4U+1)，故 clean edge 必存在。交换保持每层 matching、bucket 大小、projection type；不生新短环：含一条新边会形成旧短路径，含两条新边则违反远距或 clean edge 非短环条件。每次至少消除一条旧短环，至多 B 次。

每次 repair 改两条边，任意固定 lists 的 covered 数至多增加2。(t\ge8B/(\rho m_*)) 支付 repair 误差，使最终同时覆盖严格小于 (3\rho M'/4<\rho M')。

# 4. 与既有部分 Min-Rep 对象和 UM 边界

现有 `部分MinRep费用桥与pDM阈值双源审查--审查.md` 已吸收 v3 regular/simple/high-girth 的上述核心；本批三源补充：

| 来源 | 独有内容 | 处置 |
|---|---|---|
| `1c819f90cbdf32403533` | v3 Exact 参数、Qγ域、FAIL 量词、G固定/二进制复杂度、repair算法合同 | integrated-exact-v3-statement |
| `2e5ff24a44855e211d1e` | frozen Proof 的 factorial-moment、cycle、repair、bounded-bit 概率证明 | integrated-frozen-proof |
| `cc0f0eb857be2b2eef76` | 独立 PCSP 重构的 bounded-degree witness、真实 permutation 条件概率和高围长核对 | integrated-independent-pcsp-reconstruction |

该 source bridge 不提供：

- 从任意部分 Min-Rep 输入到 ordinary UM 的真实 compiler；
- 在 FAIL 后保留 soundness 的统一判别器以外的调度输出；
- source list 的全局 decoder、标签复制的跨-copy 一致性或费用预算；
- 一般 near-2 UM hardness、PCP 新颖性或 P≠NP 结论。

`Qγ\ge1`、固定 G、显式投影表、binary (g,\rho) 的位长和 random FAIL 语义必须在第三阶段关系边中保留。固定参数 PCP corollary 是外部来源依赖，不由本批重审；本对象与 CAG 六提供者 SPE 覆盖保持独立。

# 5. 处置与真实运行边界

三源均已完整实读、比较并保全。没有运行软件、抽样或外部 PCP 文献；Proof/independent source 都将运行与外部新颖性列为未完成。父 Boss 在 checkpoint/pushed 后逐源 done；本批未执行 clean done、commit 或 push。
