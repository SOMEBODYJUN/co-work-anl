# 七态原星的 AND 端点压缩：作者证明与次数核对

2026-10-18，scratch 作者 Proof，对应 `UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1`。

对应 Exact-only：`sol_seven_state_and_gate_localizer_obstruction_exact_v1.md`，SHA256 `8ca3b942276658319808f3c32d5057b53611555d76bfbf6f4c5f94ea18e511ab`。不得在只据 Exact 独立重构前向该审查者提供本文。

## 1. 参数与唯一所需行

d、s 是正偶数，2≤s≤d/2；η=s/d、h=s/2、T=1+η。基础 P 是 Exact 全列的七态 law，p=η³/1000、u0=4p(1−η)、e=4/5−p−u0。

0<η≤1/2，1≤h≤d/4，p>0；p≤1/8000、u0≤4p 给 e>0.79，故全部质量合法。基础原行 v 的负载保持 C+H/d，slack 为

\[
g=1+\eta-C-H/d.
\]

本证明不改变该行负载，不把给新变量的 AND 矩关系作为普通 UM 的逻辑侧约束。

## 2. 先用 Boolean，再用共同 M3 的二次零向量

固定 i∈[d]，Z 是新增 degree-one 原 endpoint 或明确定义的 Boolean 坐标。设

\[
G=Z-CY_i,\qquad \widehat L(G^2)=0.
\]

G 的原次数至多二，所以是共同 M3 的一个零向量。PSD 使它与每个次数≤3 多项式 Q 正交，即 Lhat(GQ)=0。

取允许的原变量二次多项式 q=Z(H−h)，并记

\[
Q=g(H-h)^2,\qquad\deg Q\le3.
\]

按这个顺序作两个步骤：

\[
\begin{aligned}
\widehat L(gq^2)
 &=\widehat L\big(gZ^2(H-h)^2\big)\\
 &=\widehat L(QZ)\\
 &=\widehat L(QCY_i).\tag{1}
\end{aligned}
\]

第二行使用原 Boolean Z²=Z，乘子 Q 次数三，总次数五；第三行使用二次零向量 G 与次数三 Q 的正交，总次数仍五。所有步骤都在已给 degree-six functional 内，不需要 M4，也不先把 q 中的 Z 当成 degree-two 多项式后偷降次数。

最终表达式 QCY_i 只含基础坐标，次数≤5。因此仅由 base≤5 与真实 P 一致就得到

\[
\widehat L(gq^2)=\mathbb E_P[gCY_i(H-h)^2].\tag{2}
\]

这里没有以 base≤4 代替第五次矩。

## 3. 七态支持上的精确负值

对 C=0 的全部四个类别，被积式中 C=0。对 C=1,H=0 的类别，Y_i=0；对 C=1,H=h 的类别，(H−h)²=0。所以六个非坏类别全部贡献零，且不用平均来抵消。

唯一剩余类别是 C=1,H=d，概率为 p。此时所有 Y_i=1、g=η−1、H−h=d−h。故

\[
\widehat L(gq^2)=p(\eta-1)(d-h)^2
=-p(1-\eta)(d-h)^2<0.\tag{3}
\]

严格性来自 p>0、1−η≥1/2、d−h≥3d/4>0；包括 d=4,s=2、h=1、h=d/4 的全部合法边界。只要负载检验允许所有全局原次数≤2 的 q，它就必须包含这个 q，故发生矛盾。

## 4. 新原 job 的物理读法及范围

可在基础普通星外加入一枚原 unit job K，仅有两个新的 private 机器 a、b，处理时间都为一。令候选完整 assignment law 保留原 P，并在 CY_i=1 时把 K 放 a，否则放 b。Z 是其真实原端点 X_(K,a)，而不是多项式的记号替换。

这个候选 law 完整执行全部原 jobs、保留基础所有矩，产生真实共同 M3，原 Boolean/one-hot identities 自动成立，且 G 点态为零。新增机器负载≤1；唯一被本 Proof 切掉的是要求保留的 v 行全局二次负载检验。这说明该矩关系确实可以有 ordinary original-job 语义，但它不是 UM 物理规则强制的 AND。

原星另有峰一完整调度，新增 K 也可放任一 private 端，所以这里没有 actual near-two gap。结论只是否定“保留这份 base≤5 矩、忠实 AND Gram 关系、原 v 负载公式，并同时通过全局二次检验”的点延拓。其他非线性接线、其他基础矩或近似 AND 需另证；不作一般不可能性宣称。

未运行程序，未改旧文件，未进行 repo/Git 操作。Proof 与 Exact 分开冻结，后续作者读后或独立审查应另记。
