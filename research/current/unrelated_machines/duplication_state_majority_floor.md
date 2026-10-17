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

## 尖锐族

取 (q=2s) 个变量、两状态的标签原需求均为 (K\ge s)。状态0的前 (s) 个变量各保留 (s) 个资源，状态1的后 (s) 个变量各保留 (s) 个资源；这两组好资源形成完全二部冲突：每个状态0变量的 (s) 资源集与每个状态1变量的 (s) 资源集恰有一个交点。其余资源作为私有叶补足每个完整束至 (K)，但在残余实例中删除。

同一状态内部资源束不交，且每个变量至少有一个状态残余比例 (s/K)。然而任何合法树不能同时选一个前半变量的状态0束和一个后半变量的状态1束；最多选 (s) 个变量。因此根比例至多 (1/2)，标签比例至多 (s/K)，而选完整一侧达到两者最小值：
\[
 b^*=\min\left\{\frac12,\frac{s}{K}\right\}.
\tag{3}
\]
取 (s=4)、(K=8,16,32) 得精确值 (1/2,1/4,1/8)。该族说明 (1) 的两项不能一般删除。

## 与已有障碍的关系

`UM-DUPLICATION-TWO-COPY-FLOOR-v1` 只对完整束并集给资源二着色；本页进一步使用状态内不交和残余比例，给出多数状态的 (delta) 级地板。它也可看作 `UM-GROUP-DEGREE-LABEL-APPROX-v1` 在两状态、已知残余选择下的 sharpen：先固定状态再取内部不交束，避免把 (delta) 再除以2。该命题不排除跨状态资源重用导致状态内不交失效的高阶一致性构造，也不提供一般 UM 硬度。

**Evidence。** `robust_consistency_state_majority.py` 对 (q\le3,r\le5,K\le r) 的 34,389 个完整状态对和所有非空变量子集用 `Fraction` 核对 (\delta=1) 边界；另对尖锐族直接回算式(3)。这是有限审计，不替代上面的组合证明。

**Status。** complete stated-scope obstruction; finite exact audit; external review and novelty unverified。`UM-TARGET-v1` 仍 OPEN，真正缺口是构造能同时破坏两状态多数地板且仍保留完整 YES 的跨层整数一致性。
