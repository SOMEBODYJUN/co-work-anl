# 两状态残余的多数状态地板

这是两份完整复制障碍的加强版。它允许在复制后任意删除变量和叶，但保留每个状态内部的资源不交。只要有一半变量在某个状态仍保留统一比例的标签束，就能直接选多数状态构造高比例根树；不需要把两状态的资源再做全局着色。

## 精确命题

变量集合为 (X)，根需求为 (q_r)；每个变量 (x) 有状态 (a\in\{0,1\}) 的标签 (e_x^a)，原标签需求为 (K_x^a\ge1)。删叶/删变量后给出残余资源束 (R_x^a\subseteq B_x^a)。假设对每个状态分别有
\[
R_x^a\cap R_y^a=\varnothing\quad(x\ne y).
\tag{A}
\]
令 (Y\subseteq X) 为保留变量集合，对 (delta\in[0,1]) 定义
\[
G_a(\delta)=\{x\in Y:\ |R_x^a|\ge\delta K_x^a\},\qquad
G(\delta)=G_0(\delta)\cup G_1(\delta).
\]

**UM-DUPLICATION-STATE-MAJORITY-FLOOR-v1。** 若 (G(\delta)\ne\varnothing)，则存在确定性总位多项式算法输出真实根树 (H)，满足
\[
 b(H)\ \ge\ \min\left\{\frac{|G(\delta)|}{2q_r},\ \delta\right\}.
\tag{1}
\]
若根需求同步为 (q_r=|Y|)，则
\[
 b(H)\ge\min\{|G(\delta)|/(2|Y|),\delta\};
\]
特别地，当每个保留变量至少有一个状态满足 (|R_x^a|\ge\delta K_x^a) 时，(b(H)\ge\min\{1/2,delta\})。

## 证明

每个 (x\in G(\delta)) 至少属于一个 (G_a(\delta))，因此某状态 (a^*) 满足
\[
|G_{a^*}(\delta)|\ge |G(\delta)|/2.
\]
对每个 (x\in G_{a^*}(\delta)) 选标签 (e_x^{a^*})，并保留全部残余资源 (R_x^{a^*})。由 (A)，这些资源束两两不交，故边集
\[
r\to x\to e_x^{a^*}\to R_x^{a^*}
]
是真实根树。根比例为 (|G_{a^*}(\delta)|/q_r\ge |G(\delta)|/(2q_r))；每个变量出度为1；每个选中标签的出度比例至少 (delta)；资源为零需求终端。取三类比例与截断项1的最小值即得 (1)。算法只需计算束大小、比较有理数、选多数状态并输出显式边，位复杂度为输入总位长多项式。

## 近二归约的必要条件

若一个归约的 NO 实例要求 (b^*<\varepsilon/2)，则对任意固定 (delta>\varepsilon/2) 必有
\[
|G(\delta)|<\varepsilon q_r.
\tag{2}
\]
因此不能只让某一个状态的完整分配失效；两个状态必须在几乎所有变量上同时丢失超过 (1-delta) 的标签束。这个条件适用于任意叶/变量删除，只要删除后仍满足状态内不交；它是对“保留两份完整分配再取多数”路线的逐层 soundness 过滤。

## 行列池：原锐性声称的反例与精确修复

取 (q=2s) 个变量、两状态的标签原需求均为 (K\ge s)。状态0的前 (s) 个变量各保留 (s) 个资源，状态1的后 (s) 个变量各保留 (s) 个资源；这两组好资源形成完全二部冲突：每个状态0变量的 (s) 资源集与每个状态1变量的 (s) 资源集恰有一个交点。其余资源作为私有叶补足每个完整束至 (K)，但在残余实例中删除。

同一状态内部资源束不交，且每个变量至少有一个状态残余比例 (s/K)。原稿在此声称“合法树不能同时选两侧”，继而对所有 (K\ge s) 断言 (b^*=\min\{1/2,s/K\})。该推理错误：标签可以只取部分资源，交资源可以分配给其中一侧。主多数下界(1)不受影响，但此过宽锐性已撤回。

例如 (s=K=4)，选一行与全部四列。行取该行前三格；前三列各取其他三行的格；第四列任选三格。十五个实际资源各用一次，得到五个变量、每标签三个孩子的真实根树，分数为 (\min\{5/8,3/4\}=5/8>1/2)。本例最优值也恰为 (5/8)，不是只检验一个松弛。

**UM-TWO-STATE-POOL-EXACT-FRONTIER-v1。** 对所有整数 (s\ge1,K\ge s)，此处定义的残余行列池、根需求 (2s)、各标签原需求 (K)，其真实树最优值为
\[
 b^*=\max_{1\le k\le2s}
 \min\left\{\frac{k}{2s},\frac{h_k}{K}\right\},
 \qquad h_k=\min\left\{s,\left\lfloor\frac{s^2}{k}\right\rfloor\right\}.
\tag{3-corrected}
\]
该公式可在显式池输入与 (K) 的总位长多项式时间求值，并输出达到值的完整根树，不按需求数值 (K) 展开。

上界：任何正分树都只选非空标签。若有 (k) 个标签，每个至多有 (s) 个孩子，总计至多 (s^2) 个互异资源；故其中最小整数出度至多 (h_k)。根比例为 (k/(2s))，变量比例为1，给式(3-corrected)的上界。

达到：若 (k\le s)，选任意 (k) 行并取其全部 (s) 格。若 (k>s)，选全部 (s) 行和 (h=k-s) 列，令 (t=\lfloor s^2/k\rfloor)。第 (c=0,\ldots,h-1) 列分取行号 (ct,ct+1,\ldots,ct+t-1) 模 (s) 的 (t) 格。因为 (t\le s)，同列无重复；这些 (ht) 格在每行出现至多 (\lceil ht/s\rceil) 次。由 ((s+h)t\le s^2)，有 (\lceil ht/s\rceil\le s-t)，故每行剩余至少 (t) 格，各任选 (t) 格。列与行所用资源不重叠，每个选中标签恰有 (t=h_k) 个孩子。若 (t=0)，它仅给分数0，不影响已有正分最大值。添上根→变量→标签的边即为真实树。

特别地，(K\ge2s) 时每标签比例至多 (s/K)，取全部 (s) 行达到此值，旧稿数例 (s=4,K=8,16,32) 仍精确为 (1/2,1/4,1/8)。结合 (s=1,K=1) 的一半例，这些正确数例足以说明主多数下界的两项都不能一般删除；不再声称整束冲突会禁止部分混合。

反例、完整树资格/父子/需求核验和两种独立最优值重构见[修复审查](../../reviews/unrelated_machines/two_state_pool_partial_resource_review.md)。原证据保持原字节；新增审计与一般证明分开记录。

## 与已有障碍的关系

`UM-DUPLICATION-TWO-COPY-FLOOR-v1` 只对完整束并集给资源二着色；本页进一步使用状态内不交和残余比例，给出多数状态的 (delta) 级地板。它也可看作 `UM-GROUP-DEGREE-LABEL-APPROX-v1` 在两状态、已知残余选择下的 sharpen：先固定状态再取内部不交束，避免把 (delta) 再除以2。该命题不排除跨状态资源重用导致状态内不交失效的高阶一致性构造，也不提供一般 UM 硬度。

**Evidence。** `robust_consistency_state_majority.py` 对 (q\le3,r\le5,K\le r) 的 34,389 个完整状态对和所有非空变量子集用 `Fraction` 核对 (\delta=1) 边界；另对尖锐族直接回算式(3)。这是有限审计，不替代上面的组合证明。

**Status。** complete stated-scope obstruction; finite exact audit; external review and novelty unverified。`UM-TARGET-v1` 仍 OPEN，真正缺口是构造能同时破坏两状态多数地板且仍保留完整 YES 的跨层整数一致性。
