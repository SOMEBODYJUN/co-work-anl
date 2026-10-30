# 最末后继的跨客户剥离：只剩中间背景漂移

2026-10-24，个人推导稿，未独立审查。对象是任意有限共同目录、任意人数、任意合法有序前缀与一份完整历史纯 SPE；重复主题、空主题、零客户与任意平局均保留。**Q-CAG-HALF、Mfull、Mpath 仍 OPEN。** 本文的新内容是一个在全输入类成立的精确剥离关系；它支付末位真实 BR 松弛，尚未给余下漂移的符号。

## 1. 对象与唯一的随机源

固定一个还剩 r>=2 人的真实有序历史，旧负载为 b。强制当前主题 A 后，沿同一原策略得到的真实后缀写为

    (A, Y_A, B_A),

其中 Y_A 有 r-2 个中间主题，B_A 是末位主题。令 h_A=b+c(Y_A)。h_A 允许依赖整条有序历史；这里没有把后继匿名化或冻结。

对任意非负整数背景 h 和两主题 P,Q 定义

\[
U_h(P,Q)=\sum_{x\in P}\frac1{h_x+1+\mathbf1_{x\in Q}},\quad
F_h(P)=\sum_{x\in P}\frac1{h_x+1},
\]

\[
\Phi_h(P,Q)=\sum_x\sum_{j=1}^{\mathbf1_{x\in P}+\mathbf1_{x\in Q}}\frac1{h_x+j}
=U_h(P,Q)+F_h(Q).
\tag{1}
\]

最后等式逐客户成立；Phi 是给定背景后两主题的调和势增量。

固定任意目录分布 p，令 A,T 独立同分布 p。定义

\[
D=\mathbb E_A U_{h_A}(A,B_A),\qquad
F=\mathbb E_{A,T}U_{h_A}(T,B_A),
\]

\[
C=\mathbb E_{A,T}\sum_{x\in T}
\frac1{h_A(x)+\mathbf1_{x\in A}+\mathbf1_{x\in B_A}+1}.
\tag{2}
\]

D 是强制当前人的真实平均收益；F 是删去该当前槽后独立查询；C 是保留完整终局的 extra-slot 同分布查询。三者都使用同一个 p，不能为不同客户分别另选源。

## 2. 已经支付的末位项与剩余漂移

在真实末位节点 `(h,A,Y_A)`，比较规定末位行动 B_A 与另一源分支规定的合法主题 B_T：

\[
L(A,T)=U_{h_A}(B_A,A)-U_{h_A}(B_T,A)\ge0.
\tag{3}
\]

这是末位的真实单方面比较。只把 B_T 当一个合法主题使用，没有让中间元组 Y_T 作为联合偏离。

定义中间背景漂移与额外槽碰撞税

\[
\Delta=\mathbb E_{A,T}\left[\Phi_{h_A}(A,B_T)-\Phi_{h_T}(A,B_T)\right],
\tag{4}
\]

\[
J=\mathbb E_{A,T}\sum_{x\in A\cap T}
\frac1{(h_A(x)+\mathbf1_{x\in B_A}+1)
(h_A(x)+\mathbf1_{x\in B_A}+2)}\ge0.
\tag{5}
\]

则有精确的全输入关系

\[
\boxed{D-F=\mathbb E L+\Delta,\qquad
D-C=\mathbb E L+\Delta+J.}
\tag{PEEL}
\]

若当前实际收益为 u，e=u-D>=0，则

\[
\boxed{u-C=e+\mathbb E L+J+\Delta.}
\tag{PAY}
\]

前三项是本完整 SPE 已付的跨客户信用；唯一未给符号的项为中间 r-2 人在两源分支间造成的 Delta。r=2 时 h_A=h_T=b，所以 Delta=0，准确恢复任意背景的末两人去相关并再加 extra-slot 碰撞税。任意 r 下若不同源恰给相同中间负载，也有 Delta=0；这里不为这种结构另开正面范围扩张。

## 3. 证明

由两主题身份 `U_h(P,Q)-U_h(Q,P)=F_h(P)-F_h(Q)`，逐对 A,T 有

\[
U_{h_A}(A,B_A)-U_{h_A}(A,B_T)
=L(A,T)+F_{h_A}(B_T)-F_{h_A}(B_A).
\tag{6}
\]

A,T 交换后仍同分布，故

\[
F=\mathbb E_{A,T}U_{h_T}(A,B_T),\quad
\mathbb E F_{h_A}(B_A)=\mathbb E F_{h_T}(B_T).
\]

向 D-F 加减 `E U_{h_A}(A,B_T)`，再用 (6)，得到

\[
\begin{aligned}
D-F
&=\mathbb E L+
\mathbb E\{U_{h_A}(A,B_T)-U_{h_T}(A,B_T)
+F_{h_A}(B_T)-F_{h_T}(B_T)\}\\
&=\mathbb E L+\Delta.
\end{aligned}
\]

再逐客户减去完整终局中多出的源槽，即 F-C=J，得到 PEEL。加上真实当前 SPE 的 e 即得 PAY。所有分母至少为一。

## 4. 漂移的可计算形式与全路径账

令 `k_x(A,T)=1_{x in A}+1_{x in B_T}`，则

\[
\Delta=\mathbb E_{A,T}\sum_x(h_T(x)-h_A(x))
\sum_{j=1}^{k_x(A,T)}\frac1{(h_A(x)+j)(h_T(x)+j)}.
\tag{7}
\]

该式明确：旧前缀 b 本身没有随机源；漂移全来自中间真实后继负载，且所有客户由同一 A,T 耦合。交换 A,T 还能写成

\[
2\Delta=\mathbb E_{A,T}\{[\Phi_{h_A}(A,B_T)-\Phi_{h_A}(T,B_A)]
-[\Phi_{h_T}(A,B_T)-\Phi_{h_T}(T,B_A)]\}.
\tag{8}
\]

在根实际路径的每个 i<m 运用本式，并令 i=m 时 `Delta=L=0`、J 为当次自身碰撞税。记自由列增益 `G_i=C_i-psi_i(p)>=0`，则有精确账

\[
\boxed{W-\sum_i\psi_i(p)
=\sum_i[e_i+\mathbb E L_i+J_i+G_i]+\sum_i\Delta_i.}
\tag{PATH-PEEL}
\]

末位分支的真实 BR 已从旧的无符号协方差中被显式剥离。若要用此接上一般 Mpath，需要支付负的总中间漂移，例如证明

\[
-\sum_i\Delta_i\le\sum_i[e_i+\mathbb E L_i+J_i+G_i].
\tag{9?}
\]

(9?) 尚未证明。逐枝中间负载对应互斥有序子树，不能将它们改为一个可联合选择的尾元组，也不能把各节点重新抽源误当作同一过滤的条件分布。本式没有绕过这两个真实缺口。

## 5. 与既有协方差身份的关系

boss20 的 DI/PATH 和自由源 FQ/FM 将同一个 `C-D` 留作源会员与倒数剩余负载协方差。本式继续使用原策略的真实末位 IC，从该总量中剥离 `E L>=0`，余项改成两主题势对中间负载的漂移。它不是纯代数上声称 Delta 非负，也不是已完成多后继去相关。

相关源：`boss20/route_mpath/dynamic_query_debt_identity.md`；`R-79a883d99127437ebe4f0423a181f01b/covariance/customerwise_covariance_boundary.md`；`R-d22a706a03c5499d941a6a97f94128a8/round5_coupling/common_customer_covariance_and_stationary_obstruction.md`。本文无外部文献或新颖性声明。
