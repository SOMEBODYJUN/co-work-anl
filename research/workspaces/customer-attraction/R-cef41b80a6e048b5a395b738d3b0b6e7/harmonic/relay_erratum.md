# 非根福利中继漏项：旧玩家利润必须保留

2026-10-24。身份：对既有个人稿的实质勘误与定义级反证，不是一般半覆盖的正向进展。Q-CAG-HALF 仍 OPEN。

## 1. 被纠正的原文

原稿 `research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md` 的原行10，在任意位置 i 的历史 h 后定义

\[
V(T)=\sum_{\ell>i}u_\ell(z(T)),\qquad W(z(T))=u_i(z(T))+V(T).
\]

第二个等号仅在 i=1 时自动成立。原行23–30由此推出的任意节点福利中继式 R1 漏掉了已经行动玩家的利润变化。不能将“固定行动”误当成“最终利润固定”。

## 2. 正确关系与已有来源

令

\[
P(T)=\sum_{j<i}u_j(z(T)),\quad
\gamma_h(T)=u_i(z(A^*))-u_i(z(T))\ge0.
\]

对同一历史的两个真实叶，精确地有

\[
W(z(T))-W(z(A^*))
=V(T)-V(A^*)+P(T)-P(A^*)-\gamma_h(T).
\]

故通用不等式应为

\[
\boxed{\Delta W\le\Delta V+\Delta P.}
\]

固定 h 的旧负载 b_x，以及两个真实叶从 i 起的新增负载 n_x(T)、n_x(A*)，则

\[
\Delta P=
\sum_{x:b_x>0}b_x
\left[\frac1{b_x+n_x(T)}-
\frac1{b_x+n_x(A^*)}\right].
\]

这不是本区新发现的支付恒等式。已有正确完整来源是
`R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/full_depth_ledger_and_harmonic_obstruction.md` §1(1)–(2)。这里只防止旧稿的较强错误版本继续被引用。

根节点 b=0，\(\Delta P=0\)，原 R1 因而正确。一般节点若另有 \(\Delta P\le0\)，原 R1 也可作为推论；这个符号不能无条件假定。

原稿 R2

\[
\Phi(z(T))-\Phi(z(A^*))
\le\Phi(z(T)^{-i})-\Phi(z(A^*)^{-i})
\]

本身在任意节点仍正确，因为 \(u_i=\Phi(z)-\Phi(z^{-i})\)。但删去当前人的势保留了全部旧玩家，不是仅后继势，不能把 R1 与 R2 视为无条件等价的两个福利中继式。

## 3. 两人三客户的完整 SPE 直接反证旧 R1

客户为 a,b,c，目录 A={a,b}、T={c}，两人。根规定选 A；末位在历史 (A) 后规定选 A，在历史 (T) 后规定选 A。

末位历史 (A)：选 A 得1，选 T 得1，故规定行动最优。末位历史 (T)：选 A 得2，选 T 得1/2，故规定行动最优。根规定 A 后的终局 (A,A) 中收益1；根改 T 后终局 (T,A)，根收益仍1。因此这份三节点、六项含自身比较的策略是全部历史纯 SPE。

在历史 h=(A) 比较末位规定 A 与强制 T：

\[
W(A,T)-W(A,A)=3-2=1,
\qquad \Delta V=0,
\qquad \Delta P=2-1=1,
\qquad\gamma_h(T)=0.
\]

旧 R1 会声称1≤0，严格错误；正确式取等。这个例子只纠正漏项，不是否定半覆盖：实际 W=2，OPT₂=3。

## 4. 建议的适用范围补丁

旧稿第10行增加 P(T)，将 R1 改为上面的 \(\Delta W\le\Delta V+\Delta P\)，并注明根的旧式特例。第30行“完全由后继玩家支付”改成“由后继利润变化及旧玩家份额返还共同支付”。第46行将“后继势差”改成“删去当前角色、仍保留旧玩家和真实后继的势差”。正文继续保留未闭合的跨枝支付义务，不将勘误记为一般福利推进。
