# 两状态残余树的 two-rail quota orientation 表示

本页把两状态复制路线从“资源交叉反例”提升为一个精确的离散对象。它不做有限枚举，也不声称该对象已有近二困难性；作用是明确任意两状态归约必须解决的数学问题：变量方向选择、部分标签配额和资源单射必须同时成立。

## 1. 两状态残余模型

变量集合为 (X)，每个变量 (x) 有两个标签 (ell=(x,0),(x,1))。标签 (ell) 的原需求为 (K_ell\ge1)，残余资源邻域为 (R_ellsubseteq U)。构造需求 DAG
\[
r\to x\to (x,a)\to uqquad(uin R_{x,a}),
\]
根需求为 (q_r>0)，变量需求为1，资源需求为0。假设每个状态内部资源不交：
\[
R_{x,a}\cap R_{y,a}=\varnothing
\quad(x\ne y, a\in\{0,1\}).
\tag{A}
\]
跨状态可以任意重叠；同一资源至多出现在一个0标签和一个1标签中。

对固定 (deltain(0,1])，令
\[
 t_{x,a}=\lceil delta K_{x,a}\rceil.
\]
定义 **two-rail quota orientation** 为一组 ((S,alpha,phi))：

- (Ssubseteq X) 且 (|S|gelceildelta q_r
ceil)；
- (alpha:S	o{0,1}) 为每个选中变量的 rail；
- 对每个 (xin S)，(phi_x) 是从 (t_{x,alpha(x)}) 个配额槽到 (R_{x,alpha(x)}) 的单射；
- 全部 (phi_x) 的像彼此不交。

不把 (t_{x,a}) 个槽展开成输入对象；它只是一个二进制整数阈值。

## 2. 精确等价

**UM-TWO-STATE-QUOTA-ORIENTATION-EQUIV-v1。** 对任意满足 (A) 的显式两状态残余 DAG 和任意固定 (deltain(0,1])，以下两项等价：

1. 存在根树 (H) 使 (b(H)gedelta)；
2. 存在 two-rail quota orientation ((S,alpha,phi))。

**证明。** 若有 (H) 且 (b(H)gedelta>0)，每个被选变量恰有一个被选标签；记其集合为 (S)，标签状态为 (alpha)。根出度至少 (delta q_r)，故 (|S|gelceildelta q_r
ceil)。每个选中标签的出度是整数且至少 (delta K_{x,alpha(x)})，所以至少 (t_{x,alpha(x)}) 个资源孩子；把这些孩子按任意顺序编号得到 (phi_x)。根树的单父条件保证所有像互不交。

反过来，给定 ((S,alpha,phi))，选根到 (S) 的边、每个 (xin S) 到 ((x,alpha(x))) 的边以及 (phi_x) 的资源边。资源像互不交，所以得到真实根树；根比例至少 (lceildelta q_r
ceil/q_rgedelta)，变量比例为1，标签比例至少 (t_{x,alpha(x)}/K_{x,alpha(x)}gedelta)。故 (b(H)gedelta)。

这个等价是关于**存在性**的精确重写，不调用 Fraction 审计，也不改变原需求或输出语义。若 (q_r=0) 或 (X=\varnothing)，按根终端/根单点边界单独处理。

## 3. 冲突图与两个不同难度层

由 (A)，每个资源 (u) 的出现方式只有三类：只在一个0标签中、只在一个1标签中，或同时出现在一个0标签和一个1标签中。第三类给出一条跨 rail 冲突边；因此残余资源可表示为一个二部多重图，左端是0标签，右端是1标签，边是共享资源，标签的私有资源是端点的挂件。

当 (delta=1) 且 (K_{x,a}=|R_{x,a}|) 时，选中标签必须使用其全部资源。若要求所有变量都被选，完整可行性退化为一个 2-SAT 实例：对共享资源 (uin R_{x,a}cap R_{y,b})，加入禁止同时选 ((x,a)) 与 ((y,b)) 的子句
\[
(x\ne a)\lor(y\ne b).
\]
每个变量的真假值就是其 rail。此时两状态冲突不会产生一般近二困难性；完整可行性只是 2-SAT 可满足性。

当 (0<delta<1) 时，标签只需支付 (t_{x,a}) 个资源，未选资源可以被舍弃。共享资源不再只产生布尔禁止边，而产生带容量的部分支付问题：选中两端时，边资源只能支付一端；选中一端时，它可以支付该端。于是对象从 2-SAT 变为带变量方向约束的 quota packing。多数状态地板给出的
\[
 b\ge\min\left\{\frac{|G_0(\delta)\cup G_1(\delta)|}{2q_r},\delta\right\}
\]
正是该 quota packing 的通用半数保证，而不是完整冲突图的独立集界。

## 4. 对近二归约的最小 soundness 义务

要用两状态接口证明某个固定 (arepsilon>0) 的反面，必须从一个源实例构造一个位多项式 two-rail quota orientation，使：

- YES：存在 (S=X)、某个 rail assignment 和完整配额支付，即 (b^*=1)；
- NO：对每个 (\delta>\varepsilon/2)，所有 orientation 至多选少于 (arepsilon q_r) 个变量，或至少有一个选中标签的可支付资源数低于 (delta K)；
- 任意满足 (b\ge\varepsilon/2) 的根树都能解码源问题，而不是只得到一个部分资源支付。

这比“把冲突资源复制很多次”严格得多：复制只改变边的多重度，不能阻止 quota orientation 在每个标签上选择一部分资源。完全两 rail 的状态内不交也不能自动给出 soundness，因为冲突边可以在两端之间重新分配。

## 5. 当前行列池公式的定位

当前 `UM-TWO-STATE-POOL-EXACT-FRONTIER-v1` 是本对象的一个显式参数族：资源是 (s\times s) 格子，前 (s) 个变量选行、后 (s) 个变量选列，配额支付可在交叉格子中部分分配。其精确前沿
\[
 b^*=\max_{1\le k\le2s}
 \min\left\{\frac{k}{2s},\frac{1}{K}min\left(s,\left\lfloor\frac{s^2}{k}\right\rfloor\right)\right\}
\]
正说明“选标签集合后再支付部分资源”是承重机制；把它误当作整束独立集会得到错误锐性。

该公式只解决一个高度对称的 quota packing 族。一般两状态对象的核心问题仍是：能否把跨 rail 资源冲突编译成源问题的整数一致性，而不让部分支付、删变量或多数状态逃逸恢复 (b\ge\varepsilon/2)。


## 6. 行列池的连续形状与反面含义

令 (K/s	o\kappa\) 且 (k/s	o x\)，忽略取整后，行列池的候选值由
\[
 b(x)=\min\left\{rac{x}{2},rac{1}{\kappa x}ight\},
 \qquad 1\le x\le2,
\]
以及单侧 (x\le1) 分支给出。故 \(K\) 与 \(s\) 同阶时，最优值保持正常数；要把该池值压小，必须令 \(K/s\) 很大，使每个标签的配额相对于可用资源高度稀释。这个机制是 quota 稀释，而不是源问题的一致性 gap；它不能单独支持近二困难性归约。

**Status。** 完整等价证明；无有限枚举依赖；外部审查和新颖性未认证。该表示本身不是一般 UM 算法或困难性；它把下一步从“再造冲突资源”收紧为 two-rail quota orientation 的 gap/soundness 问题。
