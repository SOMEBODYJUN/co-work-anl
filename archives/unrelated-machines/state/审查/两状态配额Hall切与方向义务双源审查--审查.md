---
id: unrelated-machines/two-state-quota-hall-cut-and-orientation-review
kind: review
title: 两状态配额Hall切与方向义务双源审查
status: complete-source-read-integrated
scope: "fixed two-rail quota payment Hall cuts and exact orientation equivalence; no general source decoder"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/two_state_quota_hall_cut_decomposition.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/two_state_quota_hall_cut_decomposition.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/two_state_quota_orientation_obligation.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/two_state_quota_orientation_obligation.md
source_ids:
  - 3d9cd298e80806182e41
  - 4d40e675859f9bd74524
inventory_sha256:
  3d9cd298e80806182e41: f8199b4a34608c344221fa828c464739bf96d08d885d00f8434eadab6923ce3f
  4d40e675859f9bd74524: 2c4d48c474d4910d2436fdec5657caa1014f3cf0f0e6ce28525627c8483bf41d
---

# 阅读范围与对象

本批完整读取两个当前正文，并与 `two_state_quota_orientation_obligation.md`、`duplication_state_majority_floor.md`、`single_layer_quota_hypergraph_obstruction.md` 及已有 Hall/配额审查比较。两源描述同一两状态残余 DAG 的不同层次：第一源在已固定变量子集、标签方向和整数支付需求后给出精确 Hall 切分解；第二源把根树存在性精确重写为 two-rail quota orientation，并明确方向选择、部分支付和源解码仍未解决。它们不是一般 unrelated-machines 近二算法，也没有给出一般 hardness。

稳定身份为 `UM-TWO-STATE-QUOTA-HALL-CUT-v1` 与 `UM-TWO-STATE-QUOTA-ORIENTATION-EQUIV-v1`。所有结论都保留固定方向和资源度至多二的量词，不把一个方向失败升级为原问题 `FAIL⇒OPT>T`。

# 一、固定方向的 Hall 配额支付

## 1. 精确对象和等价条件

固定变量子集 (S)、每个 (xin S) 的已选标签 (ell_x=(x,alpha(x)))，以及整数支付需求 (t_ell\ge0)。标签资源邻域为 (R(ell))，要求为每个标签选 (t_ell) 个资源，所有所选资源两两不同。标签集合为 (L)。

构造二部图：左侧把每个标签复制成 (t_ell) 个需求副本，右侧为容量一的资源节点，副本连接到其标签的全部资源。于是支付存在当且仅当对每个 (U\subseteq L)，
\[
\sum_{ell\in U}t_ell\le |N(U)|,qquad N(U)=\bigcup_{ell\in U}R(\ell).
\]
资源度至多二时，把资源压成标签图，邻域可写为
\[
|N(U)|=p(U)+e(U)+\partial(U),
\]
其中 (p) 是只接到 (U) 的全局度一资源，(e) 是两端都在 (U) 的共享资源，(partial) 是一端在 (U)、另一端在外部或未选标签的共享资源。因而固定方向的不可支付性有显式 Hall 缺口
\[
\Delta(U)=\sum_{ell\in U}t_ell-p(U)-e(U)-\partial(U)>0.
\]
整数最大流直接输出支付，或输出该缺口割；需求按二进制容量处理，不需复制 (t_ell) 个输入对象。

## 2. 完整支付与部分支付的分界

当 (t_ell=|R(ell)|) 且所有变量都必须被选时，一个跨变量共享资源只产生“禁止同时选两标签”的二元子句，完整可行性退化为 2-SAT：资源 (u\in R(x,a)\cap R(y,b)) 给出
\[
(x\ne a)\lor(y\ne b).
\]
同一变量的两标签不会同时被选，因此不产生冲突。这个退化只适用于整束支付。

当 (t_ell<|R(ell)|) 时，资源可在两个选中标签之间重分配，成对冲突不再足够。两个标签、三条共享资源、需求 ((1,1)) 可支付而需求 ((2,2)) 不可支付，后者由两个标签的集合 Hall 缺口见证。多个标签的单个资源冲突也可能被其它边界资源补偿，必须保留所有 (U) 的高阶切条件。把部分支付误改成独立集或只检查 pairwise 冲突会漏掉真实失败。

## 3. 证据范围和准确限制

正文配套的独立穷举覆盖至多三个标签、四个资源、需求 (0,1,2) 的全部资源关联模式，共 279,936 个固定方向实例，并逐项核对 Hall 判据；这是有限一致性证据，不替代 Hall 定理本身，也不证明方向选择容易。`FAIL` 的适用范围是一个已经固定的 (S,alpha)；若另一个方向可支付，当前方向的缺口不能推出原调度阈值失败。

# 二、two-rail quota orientation 的精确等价

## 4. 残余模型和 orientation

每个变量 (x) 有两个标签 ((x,0),(x,1))，标签资源邻域 (R_{x,a}) 的原需求为 (K_{x,a}\ge1)。同一状态内部资源不交：若 (x\ne y)，则 (R_{x,a}\cap R_{y,a}=\varnothing)；跨状态可任意重叠，但每个资源至多出现在一个 0 标签和一个 1 标签。根树为 (r\to x\to(x,a)\to u)，根需求 (q_r>0)。给 (\delta\in(0,1])，定义 (t_{x,a}=\lceil\delta K_{x,a}\rceil)。

`two-rail quota orientation` 是 ((S,alpha,phi))：选中变量集合 (S\subseteq X)，满足 (|S|\ge\lceil\delta q_r\rceil)；每个 (x\in S) 选一条 rail (alpha(x)\in\{0,1})；并为选中标签从 (R_{x,alpha(x)}) 中注入 (t_{x,alpha(x)}) 个资源，所有注入像两两不交。

## 5. 根树存在性当且仅当 orientation

完整身份 `UM-TWO-STATE-QUOTA-ORIENTATION-EQUIV-v1` 说明：存在 (b(H)\ge\delta) 的根树，当且仅当存在上述 orientation。正向从根树读取被选变量、rail 和每个标签至少 (\delta K) 个资源孩子；根出度给 (|S|\ge\lceil\delta q_r\rceil)，根树单父性质给资源注入不交。反向把根连接到 (S)、变量连接到选中标签，再按 (phi_x) 接资源；根比例至少 (delta)，变量比例为 1，标签比例至少 (t/K\gedelta)，因此得到根树。

这是存在性等价，不是方向或支付的算法。(q_r=0)、(X=\varnothing) 等边界需单独处理；orientation 的配额槽不作为输入任务展开。它把原问题准确拆成“方向选择 + Hall/配额支付”，而不是用一份局部冲突图替代全局结构。

## 6. 2-SAT、部分配额与近二义务

在 (delta=1)、(t_{x,a}=|R_{x,a}|) 且所有变量都必须选时，orientation 的支付退化为前述 2-SAT。对 (0<delta<1)，资源只需部分支付，跨 rail 共享资源形成带容量的 quota packing；多数状态地板可给半数保证，但不能把它当作完整冲突图独立集界。正文行列池族的精确前沿进一步说明稀释配额是承重机制：对 (s\times s) 格子、前 (s) 个变量选行、后 (s) 个选列，
\[
b^*=\max_{1\le k\le2s}\min\left\{\frac{k}{2s},\frac1K\min\left(s,\left\lfloor\frac{s^2}{k}\right\rfloor\right)\right\}.
\]
当 (K/s) 与 (s) 同阶时该值仍是正常数；要压低它，必须让配额相对资源高度稀释。这不是源一致性 gap 的自动证明。

若要用两状态接口给出固定 (\varepsilon>0) 的反面，至少需证明：YES 有 (S=X) 的一致 rail assignment 和完整支付；NO 对所有允许的 (\delta>\varepsilon/2)，orientation 只能选少于 (\varepsilon q_r) 的变量，或某个选中标签支付不足；并且任意 (b\ge\varepsilon/2) 的根树都能反解源问题。简单复制共享资源只改变 Hall 数值，不会阻止部分支付、删变量或多数状态逃逸。

# 三、关系与接续

1. Hall 切源给固定方向的多项式支付判据和整数流；orientation 源给根树与方向/支付的全称等价。二者合起来把未知义务清楚地分解为方向选择、全局 quota 和源解码。
2. 完整支付时可用 2-SAT；部分支付时必须保留高阶 Hall 子集。不能把后一问题误称独立集、也不能用一个局部缺口代替所有方向的联合证书。
3. 有限穷举只验证小规模模式；不存在一般方向优化器、统一近二保证、hardness 或六人 SPE 结果。资源复制或增加多重度不自动消除量词。
4. 后续若继续该路线，应先给出能生成候选方向/子集的位多项式过程，再对每个候选调用 Hall flow，并在所有方向失败时构造联合可验证证书。当前两源都已准确归档，`UM-TARGET-v1` 保持开放。
