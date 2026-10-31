---
id: "unrelated-machines/page-solis-oba-maack-2018-job-intersection-bounded-assignments"
kind: "resource"
type_tag: "文献"
title: "Page–Solis-Oba–Maack 2018：简单任务交叠结构与有界任务分配"
status: "retained-primary-literature-read"
truth_status: "primary-paper-statements-read; cited hardness results not independently reproved"
review_level: "full-pdf-text-read-with-proof-sections"
summary: "冻结作者稿研究 R||Cmax 在任务交叠图和每机可处理任务数有界时的精确边界：无菱形图下 <3/2 不可近似；每机至多 2、3、4 个任务分别有精确、3/2、5/3 算法；三角形自由图精确可解；两任务长度的受限分配给出 2−1/(ℓ−1) 近似。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/page_solis_oba_maack_2018_bounded_job_assignments_author.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/page_solis_oba_maack_2018_bounded_job_assignments_author.pdf"
source_ids:
  - "78aa66503bb113a58485"
source_sha256: "a2fad69bcf3b1e6caed4ce4f29d559e1b0f394695d859f2ca0fd8f05f8296775"
source_size_bytes: 464627
source_title: "Makespan Minimization on Unrelated Parallel Machines with Simple Job-Intersection Structure and Bounded Job Assignments"
authors: "Daniel R. Page, Roberto Solis-Oba, Marten Maack"
source_date: "COCOA 2018 accepted author manuscript; six-page PDF"
scope: "unrelated-machines scheduling; distinct from six-provider customer SPE"
related_objects:
  - "../定义/不相关机器与两个调度松弛--定义.md"
  - "../资源/配置LP在图平衡及不相关机中的间隙--资源.md"
---

# 来源身份与阅读边界

本页对应冻结源 `78aa66503bb113a58485`。`clean show` 导出的 PDF 为 6 页、464,627 字节，SHA-256 为 `a2fad69bcf3b1e6caed4ce4f29d559e1b0f394695d859f2ca0fd8f05f8296775`。我逐页阅读摘要、模型定义、相关工作、两条困难性归约、流算法分析、两种任务长度算法和结论；没有把论文引用的 Lenstra–Shmoys–Tardos、Ebenlendr 等外部定理当作本次独立重证，也没有取得 Springer 最终排版作版本核验。

这是 R||Cmax 的受限调度文献，不属于六提供者、有限共同目录、完整有序历史和均分终局价值的 SPE 模型。文中图是“任务交叠图”：任务作顶点，若同一机器同时有资格处理两任务则连边；它不同于把机器作顶点、任务作边的 graph-balancing 图。文中所有不可用资格用处理时间 `∞` 表示，算法与硬度都依赖机器资格集合的真实输入，不可把图结构当作免费 oracle。

# 模型

有机器集 (M)、任务集 (J)，任务 (j) 在机器 (i) 上处理时间 (p_{i,j}\in\mathbb Z_{>0}\cup\{\infty\})，每项任务必须完整且不可抢占地分配一台有资格机器，目标为
\[
 C_{\max}=\max_i\sum_{j:\sigma(j)=i}p_{i,j}.
\]
任务交叠图 (G_J=(J,E_J)) 在两个任务共享至少一台有资格机器时连边。另一个参数化限制是每台机器的资格集合 (J_i=\{j:p_{i,j}\ne\infty\}) 满足 (|J_i|\le \ell)。

论文明确区分 `diamondless`（不含菱形子图）和 `diamond-free`（无菱形诱导子图）；前者更强。三角形自由图自动使每台机器至多有两个有资格任务，因为三个共同资格任务会在交叠图中形成三角形。

# 主要困难性与精确算法

## 无菱形交叠图的 (3/2) 下界

论文从 At-most-3-SAT(2L) 归约到两长度 graph balancing：变量的正负文字顶点之间放权重 2 的“tautologous”边，子句文字与子句顶点之间放权重 1 的边，长度不足三的子句顶点补权重 1 的自环。满足赋值对应最大负载 2 的定向；不可满足时最优负载至少为 3。归约图每个顶点度数至多 3，任务交叠图只能是孤立点、路径或三角形的组合；逐案排除两个三角形共享两任务的可能，得到交叠图无菱形。因此若存在 (k<3/2) 的多项式近似算法，就能区分负载 2 与至少 3，从而除非 (P=NP) 不可行。

结论是：即使交叠图无菱形，R||Cmax 仍无 (k<3/2) 近似；特别地，每机至多三项任务的限制也继承该下界。这里的 NP-hardness 依赖论文采用的两长度 graph-balancing 构造和 (P\ne NP) 假设，不能表述为一般六人 SPE 的反例。

## 每机至多三项任务的流算法

给定猜测阈值 (T)，把机器 (i) 的资格任务按 (p_{i,j}\le T/2)（small）和 (T/2<p_{i,j}\le T)（big）划分；大于 (T) 的资格边先从该机器资格集合中删除。构造单源单汇整数流：每个任务节点从源获得容量 1；每台机器由 machine node、buffer node 和按机器计划（由 (|J_i|)、大小和总和决定）的容量弧组成。满流给出完整分配；若源弧未饱和，返回 REJECT。

机器计划保证：

* (|J_i|\le2) 时任意输出负载不超过 (T)；
* (|J_i|=3) 时至多两个任务被放入，同机出现一 big 与一 small 时负载至多 (3T/2)；
* (|J_i|=4) 时通过对前两大任务和、small/big 组合的三种分案，至多得到 (5T/3)。关键分案是：若四项前两大之和 (>T)，机器计划只允许一 big 加一 small；否则在前两大之和不超 (T) 时再区分第二项是否大于 (T/3)，把余下两项的总和压到 (2T/3)，从而总负载不超 (5T/3)。

对 (T) 在 ([0,\sum_{i,j}p_{i,j}]) 上二分，若满流存在则得到阈值比例调度。论文 Theorem 2 给出多项式算法：
\[
\ell=2:\ 1\text{-approximation},\qquad
\ell=3:\ 3/2\text{-approximation},\qquad
\ell=4:\ 5/3\text{-approximation}.
\]
三角形自由交叠图因 (ell\le2) 可精确求解；无菱形交叠图因 (ell\le3) 得 (3/2) 近似；二部交叠图也属于三角形自由情形。算法的承重是资格集合和 (p_{i,j}) 的实际整数比较，未给任意 (ell) 的统一近二改善。

## 两任务长度的 restricted assignment

在更窄的 restricted-assignment 模型 (p_{i,j}\in\{p_j,\infty\})，且任务长度只有 (alpha<\beta) 两种时，论文按 (alpha) 与 (eta) 相对 (T) 的四种位置组合调用已有算法或修改上述机器计划：

1. 若任务无任何 (p_j\le T) 的资格机器，立即 REJECT；
2. 若 (alpha>T/(\ell-1))、(eta\le T)，调用已有两长度算法，保证不超过 (2-\alpha/\beta<2-1/(\ell-1))；
3. 若 (alpha\le T/(\ell-1))、(eta\le T/2)，调用配置 LP 加舍入，负载至多 (3T/2)；
4. 若 (alpha\le T/(\ell-1)<\beta\le T)，按每机 big/small 集合选择机器计划。若只排 small，负载至多 ((\ell-1)\alpha\le T)；若含 big，至多一 big 加 (|S_i|-1) 个 small，负载上界
\[
\beta+(|S_i|-1)\alpha\le \left(2-\frac1{\ell-1}\right)T.
\]

二分阈值后得到 Theorem 3：当每机至多 (ell\ge3) 项且有两种任务长度时，存在多项式 (2-1/(\ell-1)) 近似。该结论仅对 restricted assignment、两长度和明确 (ell) 资格上界成立；不能推广成一般 unrelated-machines 的统一 ((2-\varepsilon)) 算法。

# 交叠图超类的 (3/2) 下界

对含 `∞` 的一般实例，可把不可用处理时间替换为 (np_{\max}+1)（其中 (p_{\max}) 是有限处理时间最大值），在阈值 (T\le np_{\max}) 下保留可行性和最优值，同时所有任务对所有机器有资格，任务交叠图变为完全图 (K_n)。因此完全图、以及 threshold、interval、cograph、split、house-free 等超类都继承 (k<3/2) 不可近似（除非 (P=NP)）。该填充只保持阈值范围内的决策，不是一般算术等价的无界处理时间替换。

论文结论还指出平面任务交叠图的复杂度未解决；它没有把三角形自由/无菱形的正面算法外推到平面图。

# 与本档既有研究的衔接

* 与 `不相关机器与两个调度松弛--定义.md` 的 R||Cmax 目标相同，但本源新增了任务交叠图参数 (|J_i|) 与两长度 restricted-assignment 的具体流构造和硬度边界；它不提供一般共同容量状态、完整 `(2-ε)` 算法或可靠 `FAIL` 证书。
* 与 graph-balancing 资源对象相关，但必须区分机器作顶点的 graph-balancing 图与任务作顶点的交叠图，不能按同名“图”合并量词。
* 对后续研究可复用的条件桥是“资格集合稀疏 ⇒ 流网络可表达完整任务覆盖”；对一般 unrelated-machines，(|J_i|) 无界，本文的机器计划不再封闭。论文的 (3/2) 下界可作为受限模型的障碍记录，不能作为当前六人 SPE 目标的反例。

# 处置

该源按 **integrated/retained-primary-literature-read** 处理：独有的模型、流构造、三项有界资格算法、无菱形/完全图困难性和两长度 restricted-assignment 近似均保存在本页；引用文献的算法和硬度只作为论文内背景，未伪称本次复证。后续若需建图，应从本页稳定 ID 接入 R||Cmax 受限调度对象，并标明“条件/资源/障碍”关系；与六人共同目录 SPE 保持独立。
