---
id: "unrelated-machines/long-path-sublinear-coalition-review-20261030"
kind: "review"
type_tag: "审查"
title: "长链联合投影与子线性联盟高围长双源审查"
status: "complete-source-read-integrated"
truth_status: "configuration-and-CC-projection-gap-families-proved-in-stated-machine-count-scope"
review_level: "full-source-read-cross-review-and-quantifier-check"
scope: "two-endpoint unrelated-machines long-path gap, fixed-r coalition projections, and r(M)=o(M) high-girth extension"
source_refs:
  - "source:7d8533e6d4a2dfeb379d:research/current/unrelated_machines/long_path_coalition_gap.md"
  - "source:d3e65f8b7c7cfbfffcb5:research/current/unrelated_machines/sublinear_coalition_projection_high_girth_gap.md"
  - "frozen-commit:68fad804ec5946cb296f77dc5b336308a66abf12"
  - "frozen-commit:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
source_blob_ids:
  - "7d8533e6d4a2dfeb379d -> f97bf92e5b55f7fdf74fa45ed6ad0869525afbc4"
  - "d3e65f8b7c7cfbfffcb5 -> 4e563ec2fed548cb0201084c71c0864ae83e1ef1"
inventory_sha256:
  "7d8533e6d4a2dfeb379d": "71694578be6a110ad993fd0039c039edfeca2f5c509e1049ca204e4fe42b8aa6"
  "d3e65f8b7c7cfbfffcb5": "a5c4e5c36641a1722585935b3b70827d733e5e4859fc82136fb4a4cee84e61d5"
related_reviews:
  - "research/reviews/unrelated_machines/long_path_coalition_review.md"
  - "archives/unrelated-machines/state/审查/长链联合投影与最优凸包边际障碍有限审查--审查.md"
reproduction_sources:
  - "tests/audits/unrelated_machines/long_path_coalition_gap.py"
  - "tests/audits/unrelated_machines/sublinear_coalition_projection_gap.py"
---

# 1. 处置范围与对象身份

本批包含两个正文来源。7d8533e6d4a2dfeb379d（UM-LONG-PATH-GAP-v1 与 UM-COALITION-PROJECTION-GAP-v1）先建立长链族：在每个任务恰有两个可用机器、机器图简单的 unrelated-machines 实例中，把原来可能出现的平行终端任务替换成很长的两端路径。它同时证明固定大小的联合/联盟投影约束不能把配置阈值和整数最优值的比率压到 2 以下。d3e65f8b7c7cfbfffcb5 再把固定的联合大小参数换成随机器数变化的任意函数 r(M)=o(M)，并把围长选到超过该函数。

两源属于同一数学对象，但量词层级不同，不能只保留后一个结论而删除前一个的固定 r 证明。前者提供森林耦合和长链构造的核心推导，后者是对同一族的对角化参数选择。二者都只处理 configuration/coalition projection 阈值相对于整数 OPT 的间隙；没有给出 UM-TARGET-v1 的一般算法、NP-hardness、文献新颖性或相对 OPT 的算法下界。涉及比值时默认排除 OPT=0，空任务、零处理时间、任意平局、空主题和未覆盖边界仍按原模型保留。

完整读取了两份正文中关于定义、森林递归、长链替换、收缩下界、配置证书、围长和树宽的段落，并与相关长链 coalition review、冻结审计脚本名称和当前 unrelated-machines 存档中的《长链联合投影与最优凸包边际障碍有限审查》比较。旧审查中的有限取向枚举只作为交叉核对；本文件不把有限脚本输出升级为一般证明。

# 2. 联合投影对象与森林耦合

## 2.1 配置解和 CC_r(T) 的精确定义

对每台机器 i，令 \(\mathcal C_i(T)\) 是总处理时间不超过 T 的可行配置。配置解 y 给每个任务恰好一次的覆盖边际，并以 y_i 表示机器 i 上的完整配置分布。配置阈值记为 T_CONF。

CC_r(T) 的要求比单纯的二元投影强：对每一个机器集合 U，其中
\[
  1\le |U|\le \min(r,m),
\]
都要存在 U 上两两不相交配置的联合分布 \(\mu_U\)，使每一台 i∈U 的**完整配置边际**恰好是 y_i。这些 \(\mu_U\) 之间只在单机器边际上相交；定义本身不要求两个不同 U 在多机器交集上给出同一联合分布。因此：

- 完整数调度的点质量分布给出 \(T_{\mathrm{CONF}}\le T_{CC,r}\le\mathrm{OPT}\)；
- CC_r 强于只检查 x_ij 等成对任务边际；
- 它仍弱于所有交集都一致的全局联合分布，也不能不加证明地称为完整 Sherali–Adams 层级。

这个量词边界是本批结论能否成立的关键。后面的森林递归只为每个给定 U 构造一个见证，不试图把所有 U 的见证拼成一个全局调度。

## 2.2 森林上的完整配置耦合

把每个任务看作连接其两个可用机器的边。由于源假设每个任务恰有两个端点，且图简单，同一对机器之间不存在两条不同任务边。若 G[U] 是森林，则对每个树分量定根。先按根机器的 y_i 抽取一个完整配置。随后沿树向下处理父子边：若任务 e 是父 u 与子 v 的共享边，则在给定父配置后，从 y_v 条件抽取子配置，只保留
\[
  {\bf 1}_{e\in S_v}=1-{\bf 1}_{e\in S_u}
\]
的状态；父端未选 e 时，子端选 e，反之亦然。任务恰有一次覆盖的边际守恒确保条件事件的总概率等于父端触发概率，故子机器的完整边际仍为 y_v。

树中每个节点只有一个父约束，递归过程中不会出现两个祖先同时规定同一子状态的冲突。内部任务被恰好一个端点选择；只有一个端点在 U 内的边作为边界任务，按单机配置边际处理。由此得到 U 上两两不相交的配置联合分布，完成森林耦合。该步骤是一般数学证明，字段完整性或脚本枚举不能代替它。

若图的围长大于 r，任何 |U|≤r 的诱导子图都不可能含环：简单图中的环至少有其环长个不同顶点。于是任一配置解在这种高围长图上自动满足 CC_r。注意结论只使用“每个小 U 的诱导图为森林”；它没有提供跨不同 U 的高阶交集一致性，也没有说 CC_r 本身等价于一个全局配置分布。

# 3. 长链族：构造、阈值和整数值

## 3.1 原始两树族与参数

正文从经典的两树族出发，固定 \(k\ge4\)，令
\[
 q=\frac{k}{k-1},
 \qquad
 h=\min\left\{t:\frac{q^{t-1}}{k-1}\ge\frac12\right\}.
\]
原族的整数最优值和配置阈值分别为
\[
 c_k=2-\frac1k,
 \qquad
 T_k=1+\frac1k.
\]
终端父点 v 与终端点 t 之间原有 k 个平行任务。平行边会妨碍简单图和高围长条件，因此每一个终端任务都被替换为一条独立长度为 \(\ell\) 的路径
\[
  v-w_1-w_2-\cdots-w_{\ell-1}-t,
  \qquad \ell\ge2.
\]
不同路径的内部机器互不相同。路径第一条边在 v 上的处理时间为 1/k，在 w_1 上为 1；之后每条边的两个端点处理时间均为 1。每条新边仍代表一个恰有两个端点的任务。

两条不同路径组成的最短环正好长 \(2\ell\)，故机器图简单、围长为 \(2\ell\)，并且该串联平行路径结构的树宽为 2。选 \(\ell\) 足够大即可同时满足任意预先给定的围长下限和固定 r 的森林条件。

## 3.2 整数下界：路径不能在内部“回头”

设新实例存在 makespan \(C<c_k<2\) 的整数调度。对一条替代路径，若第一条任务由 w_1 承担，则 w_1 已承受一个单位任务；第二条任务不能再放在 w_1，只能向右。继续沿路径归纳，整条路径只能保持向右传播，末边归于 t。若第一条任务由 v 承担，同样的单位负载约束迫使路径向左传播并归于 v。因此每条路径都可以收缩为原来的一个任务，并且收缩不会增加原终端机器负载。这样得到原两树族一个 makespan <c_k 的调度，矛盾于原族整数最优值 c_k。

反向方向也成立：取原族的最优调度，把一条原任务若分配给 v 就沿路径向左延伸，若分配给 t 就向右延伸。所有新内部机器只承受一个单位任务，终端负载不变，故新实例的整数最优值仍为
\[
  \mathrm{OPT}=c_k=2-\frac1k.
\]
这一步是完整的参数族论证，而非单个小实例的可行排程。

## 3.3 配置证书沿路径延伸

原配置证书中每个终端任务在 v 端出现的质量为 1/k，在 t 端出现的质量为 1-1/k。替换成路径后，首边承担原任务在 v 端的角色，末边承担其在 t 端的角色。每个内部机器只需在其左边任务和右边任务之间抽取：以概率 1/k 选左边，以概率 1-1/k 选右边。由此所有内部机器的配置边际满足容量 1+1/k，且每个新任务覆盖边际仍为 1。于是
\[
  T_{\mathrm{CONF}}\le T_k=1+\frac1k,
\]
而正文给出的配置证书取到该阈值。

长链族的比率为
\[
 \frac{\mathrm{OPT}}{T_{\mathrm{CONF}}}
 \ge
 \frac{2-1/k}{1+1/k}
 =2-\frac{3}{k+1}.
\]
当 k→∞ 时该比率趋于 2。另一方面，已有 UM-ST-ROUND-v1 型舍入给出配置阈值到整数调度的通用上界 2，因此在该输入类上配置 LP 的上确界恰为 2。这里“恰为”由下界族和独立上界共同得到，不能只从有限脚本输出推断。

# 4. 固定 r 的高围长 coalition gap

给定任意围长下限 \(g\ge3\) 和任意固定 \(r\ge1\)，选 \(\ell\) 使
\[
  2\ell\ge g,\qquad 2\ell>r.
\]
长链图的每个机器集合 U（|U|≤r）诱导森林，因而第 2 节的耦合把同一个配置解提升为 CC_r 见证。于是同一族满足
\[
  \sup_{P:\,\mathrm{girth}(P)\ge g}
  \frac{\mathrm{OPT}(P)}{T_{CC,r}(P)}=2,
\]
其中仅在 OPT>0 的实例上取比值。下界由 2−3/(k+1) 随 k 逼近 2 给出；上界来自 \(T_{CC,r}\ge T_{\mathrm{CONF}}\) 以及配置舍入的 2 上界。

因此 UM-LONG-PATH-GAP-v1 的具体处置是：即使限制为简单二端点实例，并要求围长至少任意给定 g，配置 LP 与整数 OPT 的间隙仍可任意逼近 2。UM-COALITION-PROJECTION-GAP-v1 的具体处置是：固定的任意 r 层 coalition projection 也不能改善这个上确界。它只排除“固定有限联合规模、相对 CC_r 阈值统一得到严格优于 2 的保证”这一条路线。

正文给出的正面边界必须同时保留：若不只要求每个 U 有一个独立见证，而是要求所有至多三台机器的联合分布在全部交集上的**完整配置边际一致**，则树宽为 2 的长链族可沿宽度为 2 的树分解，通过 separator 条件耦合成全局分布，并从该全局分布取出真实 makespan-T 调度。这个正面结论说明负结果严格依赖于 CC_r 的“跨 U 不一致”量词；它不是对所有高阶一致性方法的否定，也不推广到任意树宽或任意图。

# 5. r(M)=o(M) 的子线性提升

## 5.1 参数和机器计数

第二份正文取任意函数 \(r:\mathbb N\to\mathbb N\)，满足
\[
  \frac{r(s)}s\longrightarrow0\qquad(s\to\infty).
\]
它以机器总数 M(P) 为参数，而不是以二进制输入长度为参数。对上一节长链族，固定 k 后，正文给出的机器数为
\[
  M_{k,\ell}=A_k+B_k\ell,
  \qquad
  A_k=\frac{2(k^h-1)}{k-1},
  \qquad
  B_k=2k^h.
\]
围长仍为 2\ell。于是对固定 k，有 M_{k,\ell}/\ell→B_k，从而
\[
  \frac{r(M_{k,\ell})}{\ell}
  =\frac{r(M_{k,\ell})}{M_{k,\ell}}\,
    \frac{M_{k,\ell}}{\ell}
  \longrightarrow0.
\]
最终存在足够大的 \ell 使 r(M_{k,\ell})<2\ell，即围长严格超过该实例的 coalition 大小上限。

## 5.2 量词顺序和结论

给定 \(\varepsilon>0\)，先选 k 使
\[
  \frac{3}{k+1}<\varepsilon.
\]
再固定此 k，利用 r(M_{k,\ell})/\ell→0 选足够大的 \ell，使得 2\ell>r(M_{k,\ell})。该实例于是同时满足：任务各有两个端点、机器图简单、girth(P)>r(M(P))，并且
\[
  \frac{\mathrm{OPT}(P)}{T_{CC_{r(M(P))}}(P)}
  \ge 2-\frac{3}{k+1}>2-\varepsilon.
\]
这就是 UM-SUBLINEAR-CC-PROJECTION-GAP-v1 的完整量词：对任意 o(M) 的联合规模函数以及任意正 \varepsilon，存在一个合法实例把该 projection 层的间隙推到 2−\varepsilon。它比“每个固定 r 都有一族反例”强，因为 r 可以随实例机器数增长；证明仍然只需同一个森林耦合和先选 k、后选 \ell 的对角化。

正文明确不把该陈述改写为“相对于输入位长的子线性 coalition”。机器端点、任务与处理时间的编码长度含有额外的编号开销；本源只证明机器计数参数 M 下的 o(M) 结论。第三阶段若要讨论 bit-length 版本，必须重新给出编码模型、输入长度和函数关系，不能由本源自动推得。

# 6. 证据层级、比较和未完成缺口

## 6.1 相关冻结材料的去向

research/reviews/unrelated_machines/long_path_coalition_review.md 以及冻结脚本 tests/audits/unrelated_machines/long_path_coalition_gap.py 主要承担有限参数的路径取向、围长、整数值和森林联合状态核验；它们适合作为本源一般推导的回归证据，不是独立的高阶一致性定理。tests/audits/unrelated_machines/sublinear_coalition_projection_gap.py 对机器数、围长和 r(M) 的选择顺序提供复现入口，但脚本字段检查不能代替极限论证。当前存档中的旧《长链联合投影与最优凸包边际障碍有限审查》还包含固定最优凸包点、逐行合同和负相关随机输出等不同对象；那些对象不并入本批的 coalition gap。

两份当前正文各自的稳定 ID、blob ID、冻结提交和 SHA-256 已记录在本文件 front matter。来源的原文路径是 research/current/unrelated_machines/long_path_coalition_gap.md 与 research/current/unrelated_machines/sublinear_coalition_projection_high_girth_gap.md；本批没有用后续可能变动的工作树副本替代冻结身份。

## 6.2 分类

- **已证明的一般结论**：森林上的完整配置耦合；长链替换保持 OPT=2−1/k 和配置阈值 1+1/k；固定 r、固定围长下的 coalition gap 上确界 2；任意 r(M)=o(M) 的机器计数版本仍可达到 2−\varepsilon。
- **条件/正面结论**：若至多三机器的分布在所有交集上完整一致，则树宽 2 长链族可沿 separator 耦合到真实调度。该条件不能删去，也未推广到一般图。
- **有限证据**：脚本给出的具体 (k,\ell) 取向枚举、配置边际核验、拒绝含环 coalition 的程序先决条件。它们支持实现和边界，不替代一般证明。
- **障碍**：固定有限 r 或任意 o(M) 的独立小集合见证，只在各自集合内部耦合，无法传递跨集合的重叠一致性；长链通过高围长把所有小集合变成森林，从而保留近二间隙。
- **反例/非主张**：本源不是 NP-hardness 反例，不是相对 OPT 的 approximation lower bound，也不是所有全局约束或 bounded-treewidth 动态规划的反例。没有证明高阶一致性不可能，也没有声称随机化、全交集 consistency 或重新选择凸包点的算法失败。

## 6.3 第三阶段应保留的开放问题

后续工作需要明确区分三类路线：一是要求跨 U 完整交集一致性的 hierarchy，二是利用树宽、separator 或动态规划直接恢复调度，三是允许相对 OPT 或重新选择分数解的舍入。任何声称“联合规模足够大即可修复”的陈述，都必须写明是按机器数、输入位长还是树宽参数量化，并证明不同小集合之间的兼容性。

当前批没有解决六人 SPE 的目录覆盖目标；客户目录、终局均分和任意平局语义属于独立对象。它只对 unrelated-machines 子存档完成了两份当前来源的精确处置，故不得把本文件作为主线 SPE 结论或全仓清洗完成的替代。

# 7. 逐源处置记录

| 稳定 ID | 实读与比较 | 独有内容写入 | 处置 | 剩余疑点 |
|---|---|---|---|---|
| 7d8533e6d4a2dfeb379d | 全文读取；与长链 coalition 旧审查、有限取向/森林脚本交叉比较 | 森林耦合、路径收缩、配置延伸、固定 r 和围长 gap、树宽 2 正面边界 | integrated；一般证明与量词写入第 2–4 节，有限脚本仅作证据 | 全交集一致 hierarchy 在更宽树宽/一般图上的可扩展性未解决 |
| d3e65f8b7c7cfbfffcb5 | 全文读取；核对 M_{k,\ell}、围长和先选 k 后选 \ell 的极限顺序 | 任意 r(M)=o(M) 的高围长对角化和机器计数/位长边界 | integrated；写入第 5 节 | 没有 bit-length 版本、硬度结论或相对 OPT 下界 |

该处置只表示来源已经有准确落点和明确边界，不表示开放数学问题已经解决。
