---
id: "unrelated-machines/list-agreement-degree-budget-source-b46"
kind: "review"
type_tag: "审查"
title: "列表 agreement 度数预算独立源的重构与对象归并"
status: "integrated-into-list-agreement-review"
summary: "独立读取 b46 源；完整重构 ticket 地板、全 agreement 流阈值、逐图锐性和 soundness 参数，归入已有列表协议审查，不升级为 UM 困难性或调度编译。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/list_degree_budget_independent_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/list_degree_budget_independent_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/list_agreement_degree_budget_and_decoder.md"
---

# 列表 agreement 度数预算独立源：实读、比较与归并

## 来源身份和读取边界

冻结源 ID 为 `b46c20052598d5d910c3`，路径为
`history/source/notes/unrelated_machines/list_degree_budget_independent_source.md`，两份冻结定位分别是
`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `main` 提交
`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。inventory 中 blob 为
`6f8dd26dc97b5bae697fef5a3e19fe92aa1aa2ec`，文件大小 6419 bytes，SHA-256 为
`155e4fdbebac53b94e74da05ad35cd875445a1bc351d7ee63929f10fc65c9432`。

正文四部分全部读取。它没有程序、有限运行、文献原文或外部新颖性结论；证明只使用显式有限图、ticket 计数和标准整数最大流。当前工作区已有
《大束碰撞地板与列表协议双源审查--审查.md》，以及其对应的列表 agreement 来源
`9b9de5d88249f986a4e8`。本源与既有列表对象逐式比较后，确认数学对象和全部主量词一致；本源是一份较短的独立重构，不能作为第二个不同模型。

## 对象和量词

输入是有限简单正规二部图 (G=(A,B,E))，(B\ne\varnothing)，左度数 (d\ge1)，右度数 (D\ge2)。给有限字母表
(Sigma_A,Sigma_B) 和每条关联的显式总映射
(pi_{ab}:Sigma_A\toSigma_B)。每个右点 (b) 要求局部公共像
(\bigcap_{a\in N(b)}pi_{ab}(Sigma_A)\ne\varnothing)。列表
(Lambda_a\subseteqSigma_A) 的大小至多二进制整数 (L\ge1)；agreement 必须由两个不同左邻居的列表原像映到同一 (Sigma_B) 标签。所有结论量化上述完整对象域，不使用全局满足赋值。

该源只对普通简单图成立；平行边不能冒充“两个不同邻居”。集合大小是“至多”，所以 (L>|\Sigma_A|) 仍是合法输入语义。局部公共像只供每个右点选一个标签和每条边选一个原像，不等于 Label Cover/UM 的 YES 见证。

## 1. Ticket 构造给出的确定性地板

对每个右点固定选择公共像 (z_b)，并为每条关联选 (x_{ab}) 使
(pi_{ab}(x_{ab})=z_b)。把每个选中关联视为 ticket；即使同一左点的两张 ticket 最终使用相同字母，也分别计数，之后列表去重只会缩小输出。

初始化 ticket 计数 (r_a=0) 和已服务右集 (S=\varnothing)。只要有未服务 (b) 的两个不同邻居 (a,a') 同时满足 (r_a,r_{a'}<L)，按固定顺序给两条关联各发一张 ticket，把 (b) 加入 (S)。终止时每个列表大小至多 (L)，且 (S) 中每个右点真实 agreement。

令 (T=\{a:r_a=L\}) 为饱和左点。终止条件给每个 (b\notin S) 至少 (D-1) 个 (T)-邻居，因此
[
(D-1)(|B|-|S|)\le |E(T,B\setminus S)|\le d|T|.
]
总 ticket 数为 (2|S|)，故 (L|T|\le2|S|)。消去 (|T|) 得
[
 \operatorname{agr}(\Lambda)\ge\frac{|S|}{|B|}
 \ge\frac{L(D-1)}{2d+L(D-1)}.
]
算法每步服务一个右点，至多 (|B|) 步；固定顺序扫描图并比较 ticket 计数与二进制 (L)，不按 (L) 数值展开。若 (L>d)，不能有饱和左点，终止即服务全部右点；因此大二进制 (L) 不造成伪多项式循环。

## 2. 全 agreement 的流阈值

构造源到每个 (b) 容量 2、每条 (b\to a) 关联容量 1、每个 (a) 到汇容量
(min(L,d)) 的网络。每条关联送 (2/D) 的分数流：右点流量恰为 2，左点流量为 (2d/D)。当
(L\ge\lceil2d/D\rceil) 时容量合法，且 (D\ge2) 保证关联容量 1 不超；(lceil2d/D\rceil\le d)。整数最大流给每个右点两条不同关联，放入相应 (x_{ab}) 即使全部右点 agreement。网络显式规模多项式，流容量只需截为 (d)，同样不依赖 (L) 的数值大小。

## 3. 固定图的逐图锐性

对任意固定图取
(Sigma_A=\{\ell_b:b\in B\})，(Sigma_B=\{0\}\cup\{p_a:a\in A\})，所有 (p_a) 两两不同且不为 0。每条边定义
[
\pi_{ab}(\ell_c)=
\begin{cases}0,&c=b,\\p_a,&c\ne b.\end{cases}
]
每个邻居的像含 0，故局部公共像成立；两个不同邻居的私有标签不相等。于是 (b) agreement 当且仅当至少两个邻居的列表含 (ell_b)。全部右点 agreement 需要至少 (2|B|) 个不同的左—右符号关联，而左列表总共至多 (|A|L) 个符号，且 (|A|d=|B|D)，所以 (L\ge\lceil2d/D\rceil)。这同一套映射同时排除所有低于阈值的 (L)，其编码大小为图的多项式大小。

锐性只针对第 2 项“所有右点 agreement”的通用整数阈值；不声称第 1 项的分数地板对每张图或每套映射均锐，也不产生困难性。

## 4. Soundness 参数限制和边界

若对象域内某个 NO 源对所有大小至多 (L) 列表有 agreement soundness (alpha<1)，则把 ticket 地板代入得
[
\alpha\ge\frac{L(D-1)}{2d+L(D-1)}>0,
\qquad L<\lceil2d/D\rceil.
]
正数交叉相乘给
[
\frac dL\ge\frac{(D-1)(1-\alpha)}{2\alpha}.
]
例如 (L/d=1/D) 时地板为 ((D-1)/(3D-1))，随 (D\to\infty) 趋近 (1/3)。这些是列表 soundness 的必要参数，不是 Label Cover 困难性、SAT 归约、真实调度编译器或 UM-TARGET-v1 的答案。

## 与既有对象的关系、独有内容和处置

本源与已有 `UM-LIST-AGREEMENT-DEGREE-BUDGET-v1` 的列表协议正文和
《大束碰撞地板与列表协议双源审查--审查.md》保持同一输入域、四项结论和证明路线；旧源还附带文献接口与调度解码缺口，本源没有。可归并的独有细节是：显式说明列表去重只缩小 ticket 上界、(L>d) 时直接全服务、以及幂次/容量截断不依赖二进制 (L) 的伪多项式展开。它们应作为现有审查对象的补充段落，不能新建第二个 list-agreement 定理。

没有有限程序或 JSON 可入 evidence；本源不声称运行。建议处置为 `integrated`，目标为
`archives/unrelated-machines/state/审查/大束碰撞地板与列表协议双源审查--审查.md`，并将本源两个冻结 source refs 加到该对象的 provenance。`UM-TARGET-v1`、六人 SPE 覆盖目标和外部新颖性保持开放。
