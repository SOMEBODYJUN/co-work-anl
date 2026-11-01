# 真实跨枝重置的二查询账：精确分解与尚未支付的对角储备

2026-10-24。R-6bb0323d87294932af2aa23b47b9d4ad / relay。对象始终为任意人数、任意有限共同目录、每个完整有序历史纯 SPE、单位客户与单位提供者，保留空主题、重复和平局。**Q-CAG-HALF 仍 OPEN；本文没有证明新的全输入福利下界。** 下述逐客户恒等式适用于全部输入；它是重置账的显式表示，不把等价表示列作一般证明突破。

本轮直接尝试把 reused-resource reset 接回真实 successor IC。得到的可核内容是：把二查询的正重置项完全局限到对称差客户，保留共同客户税及真正当前 IC 松弛；在已有八人完整 SPE 中，局部二查询付款确实失败，但同分布二次型由对角税支付。该精确区别会影响后续一般证明选取的义务。

## 1. 对任意实际位置保留真实完成叶

固定任意完整纯 SPE σ，实际终局 z，实际位置 i 的有序前缀 h，旧负载 b_x。强制当前主题 A 后沿同一 σ 完成，得 Z_i(A)；其真后继客户负载记 n_A(x)，所以

\[
c_x(Z_i(A))=b_x+\mathbf1_{x\in A}+n_A(x).
\]

定义真正当前偏离利润与 extra-slot 矩阵

\[
D_i(A)=\sum_{x\in A}\frac1{b_x+1+n_A(x)},\qquad
K_i(T,A)=\sum_{x\in T}\frac1{1+c_x(Z_i(A))}.
\]

令实际当前利润为 u_i，真实 IC 松弛 e_i(A)=u_i-D_i(A)≥0。这些定义没有冻结后继，也没有把两个同负载历史当成相同策略节点。

## 2. 二查询的精确 signed reset 恒等式

对任意两个合法主题 A,T，置

\[
\begin{aligned}
R_i(A,T)
&=\sum_x
\frac{(\mathbf1_{x\in A}-\mathbf1_{x\in T})[n_A(x)-n_T(x)]}
{[b_x+1+n_A(x)][b_x+1+n_T(x)]},\\
J_i(A,T)
&=\sum_{x\in A\cap T}
\left[\frac1{c_x(Z_i(A))[c_x(Z_i(A))+1]}
+\frac1{c_x(Z_i(T))[c_x(Z_i(T))+1]}\right].
\end{aligned}
\]

R 是 signed 量，J≥0。逐客户分类直接得

\[
\boxed{K_i(T,A)+K_i(A,T)-D_i(A)-D_i(T)=R_i(A,T)-J_i(A,T).}\tag{RESET}
\]

证明只需四种 membership：

* x 只在 A：左侧贡献为 `1/[b+1+n_T]−1/[b+1+n_A]`，等于 R 项；
* x 只在 T：对称；
* x 同时在 A,T：两枝分别给 `1/(c+1)−1/c`，合计为 −J 项；
* 两者都不含：贡献为零。

所以真正当前 slack 给另一条精确式

\[
\boxed{2u_i-K_i(T,A)-K_i(A,T)
=e_i(A)+e_i(T)+J_i(A,T)-R_i(A,T).}\tag{PAIR}
\]

**含义边界。** 正重置只能来自 A△T 上根查询触发的后继负载差；共同客户提供 J 税。该差仍读取两份完整真实续局。没有证明 R 由 e+J 局部支付，也不能把 R 直接改成后继利润或当前可取得利润。

## 3. 同分布二次型必须另外保留对角税

设 p 为任意目录分布。已知开放弱桥为

\[
\sum_i G_i^+(p)\le W,\qquad G_i^+(p)=\sum_{A,T}p_Ap_TK_i(T,A).
\tag{GB+?}
\]

该桥的既有归属见
`R-12bf6a96d24c48eca828620d6642e203/menu_minimax/aggregate_extra_slot_empty_dilution.md`。
本文不将它重新命名为新候选。其较强 `ΣGplus≤ΣD` 已被该正文否定。

定义对角 self-tax

\[
q_i(A)=D_i(A)-K_i(A,A)
=\sum_{x\in A}\frac1{c_x(Z_i(A))[c_x(Z_i(A))+1]}\ge0.
\]

展开 `Σ_A p_AD_i(A)` 并应用 RESET，得

\[
\boxed{u_i-G_i^+(p)
=\sum_Ap_Ae_i(A)+\sum_Ap_A^2q_i(A)
+\sum_{A<T}p_Ap_T[J_i(A,T)-R_i(A,T)].}\tag{QUAD}
\]

主题顺序 A<T 只是任意固定标签顺序。对角税项不可在转到 pair 语言时丢弃。`PAIR≥0` 对所有 pair 是一个很强的充分条件；它失败并不否定 QUAD 对所有 p 非负，更不否定跨位置 GB+。

同一公式也可逐客户写成协方差账。设 `a_A=1_(x∈A)`、`s_A=1/[b_x+1+n_A(x)]`、`p_x=E a_A`。则该客户的普通当前平均利润与独立查询之差为 `Cov_p(a_A,s_A)`；extra-slot 再返还

\[
p_x\,\mathbb E_A\frac{a_A}{c_x(Z_i(A))[c_x(Z_i(A))+1]}.
\]

这仍是等价恒等式，不是把协方差符号变成已证。

## 4. genuine successor IC 能无债接入的尾端

最后位置没有自适应后继，R_m=0，故 PAIR≥0。倒数第二位置恰剩一名后继，设末回复为 B(A)，同背景两人收益为 U(A,B)。末位的两条真正 IC slack 为

\[
L(A,T)=U(B(A),A)-U(B(T),A)\ge0,
\]

及 L(T,A)。共同对称交项相消给

\[
D_i(A)+D_i(T)-f_{B(A)}(T)-f_{B(T)}(A)
=L(A,T)+L(T,A).
\]

额外槽再扣 J，因此

\[
2u_i-K_i(T,A)-K_i(A,T)
=e_i(A)+e_i(T)+L(A,T)+L(T,A)+J_i(A,T)\ge0.
\]

这是现有一后继去相关的显式 pair 形式，未宣称新尾端定理。若有更多后继，交换整组后继不再是一名玩家的单一合法偏离；RESET 中的 R 就是必须另付的真实重置差。

## 5. 现有八人源中局部 pair 失败，而对角税救回同分布式

输入与完整策略来源为
`R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json`。
此处不声称新 SPE 实例，也不把固定八人作新专项；只用它检验上述明确的一般辅助关系。

本侧定义级独立审计展开32名单位客户，检查全部13,872个 DAG 节点、59,496项真正行动比较及每条孩子计数关系。DAG 节点带自己的孩子，不假定同计数节点共享后继；按节点的复制展开对应全部有序历史。

实际路径 `(3,0,2,3,4,4,5,6)`，利润

\[
(13/4,21/4,17/4,13/4,13/4,13/4,17/4,21/4),\quad W=32.
\]

根的查询对 A=3,T=7 的 K 子矩阵为

\[
\begin{pmatrix}137/60&37/10\\37/10&137/60\end{pmatrix}.
\]

根的两次真正偏离利润都为 u_1=13/4，A∩T=∅，因此 e_A=e_T=J=0，而

\[
R_1(3,7)=9/10>0.
\]

所以局部充分条件 `K(T,A)+K(A,T)≤2u_i` 被这一已有完整 SPE 精确否定，负余额为 −9/10。位置5、6的查询对(4,7)也分别有 −2/5。不能把每个位置的 pair 欠账要求为非负。

但对 p=(θ,1−θ) 支撑于(3,7)，每个对角税 q=29/30，故

\[
u_1-G_1^+(p)
=\frac{29}{30}[\theta^2+(1-\theta)^2]-\frac9{10}\theta(1-\theta)
=\frac{29}{30}-\frac{17}{6}\theta(1-\theta)
\ge\frac{31}{120}>0.
\]

因此该二点同分布最大值是 `359/120<13/4`。进一步只针对同一根矩阵做精确有理全 simplex 最大化，得

\[
\max_pG_1^+(p)=\frac{1717}{560}<\frac{13}{4},\qquad
p_{2,3,6,7}=\frac1{28}(5,9,5,9).
\]

这不是一般 QUAD 的证明。该实例全部位置相加后的最小 cross-pair 余额亦为

\[
\min_{A,T}\{2W-\sum_i[K_i(T,A)+K_i(A,T)]\}=299/30>0,
\]

在 pair(4,7)达到。局部 pair 失败没有延伸成 aggregate pair 失败。

## 6. 代码审计与 exact quadratic 最大化的完整性

`audit_two_block_pair.py` 不导入原 solver、原 menu 审计或数值优化器。它独立核验整份 DAG、所有实际位置 RESET/PAIR 恒等式，并输出 `audit_two_block_pair.json`。

二次型只依赖对称部分 Q=(K+Kᵀ)/2。在每个非空支撑 S 上解

\[
Q_{SS}p_S=\lambda\mathbf1,\qquad\mathbf1^Tp_S=1.
\]

保留 bordered matrix 可逆且 p_S≥0 的有理解，直接计算所有这些可行点的值并取最大。完整性如下：取所有全局最大元中支撑极小的一个，其正支撑上满足驻点式。若 bordered matrix 奇异，则存在非零切向 v 满足 `1ᵀv=0,Qv=μ1`。与 p 内积及驻点式给 μ=0，所以沿 p+tv 的二次型恒定。移到 simplex 边界即得到更小支撑最大元，矛盾。因此极小支撑最大元必被上述可逆系统枚举。这里有限计算恰好认证**该固定矩阵**的全分布最大值，不扩大为任意人数结论。

`audit_pair_reset.py` 对七个既有完整证书逐定义核验全历史 IC 与 RESET。结果 `pair_reset_checks.json`。它们只服务于公式实现检查；没有发现违例不承担任何一般引理。

## 7. 当前准确断点与独立攻击

仍需从 genuine successor IC 证明某个全输入支付，而不是只列账。一条可能义务为 GB+，其精确缺口由 QUAD 给出：signed 跨枝 R 在所有实际位置的加权总和，是否由真正当前 e、对角 q 和共同 J 一次支付。较强逐 cross-pair 版本已失败；逐位置同分布版本仍未由本侧证明或反驳。也可完全绕开这条路线。

对本页的独立攻击结果/限制：

1. RESET/QUAD 只是代数；将它们称为新增一般 welfare 下界会错。
2. 八人例已经杀死用逐节点 pair 非负接入一般归纳的做法。根的失败发生在 disjoint queries，不能声称正重置总由共同客户税支付。
3. 丢掉同分布二次型中的对角项会制造不必要的过强命题；根二点有理计算给出显式证据。
4. e 只能来自原真实 IC。将 off-path 捕获者的利润改为原实际位置利润、把旧主题 cap 推给全部 threat branches，均不被这些公式允许。
5. 公式和精确计算由本侧自检；父研究者已实时收到关键数值，但本稿的新表述尚未完成另一作者独立数学审查。原来源 SPE 是旧资产，本侧另做定义级核验。

下一有价值动作应是构造 QUAD 右端的 genuine successor 运输/单次资源付款，或给该明确候选一个真正完整 SPE 反例；本侧没有得到这一步，也没有将检查规模计为主线突破。

## 8. 后继占用查询的一条一般正关系，以及 derivative 接入断点

父研究者随后提出另一个具体充分机制。固定上述位置 i，令 n=m−i≥1，P(A,·) 为该 A 分支中 n 位真实后继主题的均匀经验分布，q=Pp。考察

\[
G(p)=p^TKp,\qquad d(p)=(q-p)^T(K+K^T)p.
\]

若能由 genuine successor IC 证明 `G(p)>u_i => d(p)>0`，则 G 在 simplex 的一个全局最大元 p 上不可能大于 u_i：q 仍为合法分布，而最大元的一阶方向导数 d 必须≤0。该**条件蕴含**尚未证明；不把充分性的解释当作其证明。

这里确实有一条一般非负 occupation-query reserve。令

\[
\pi_j(Z_i(A))=\sum_{x\in S_j(Z_i(A))}\frac1{1+c_x(Z_i(A))},\qquad
V^+_{\rm tail}=\mathbb E_A\sum_{j>i}\pi_j(Z_i(A)).
\]

则对任意 p、任意完整形式策略（不需要 SPE），

\[
\boxed{n q^TKp=V^+_{\rm tail}+\mathcal I_i(p),\qquad \mathcal I_i(p)\ge0.}\tag{OCC}
\]

其中精确余项为

\[
\mathcal I_i(p)=\frac12\sum_x\mathbb E_{A,T\ iid\ p}
\frac{[n_A(x)-n_T(x)]\{n_A(x)-n_T(x)+\mathbf1_{x\in A}-\mathbf1_{x\in T}\}}
{[1+b_x+\mathbf1_{x\in A}+n_A(x)][1+b_x+\mathbf1_{x\in T}+n_T(x)]}.
\]

证明：对每个 x，写 `f_A=1/[1+b+a_A+n_A]`，有 `nq_x=E n_A`，所以左减尾 extra 利润等于

\[
\mathbb E n_A\,\mathbb E f_A-\mathbb E(n_Af_A)
=\frac12\mathbb E[(n_A-n_T)(f_T-f_A)].
\]

展开倒数差即得到展示式。`n_A−n_T` 是整数、`a_A−a_T∈{−1,0,1}`，故每个乘积 `Δn(Δn+Δa)≥0`。这不是对任意实尾质量成立的论证；单位后继产生的整数负载正是非负性的来源。空主题、重复选择和任意历史平局都不会破坏它。

OCC 是新写出的、适用于全部输入的 occupation-query 比较组件，但**没有使用 successor IC，尚未接通一般 half**。它只支付 derivative 的一侧：

\[
d(p)=\frac{V^+_{\rm tail}+\mathcal I_i(p)}n+p^TKq-2G(p).
\]

另一侧 `p^TKq` 读取“在当前根强制一个真实后继主题，再独立查询 p”的重置分支。真正后继在其原历史的单行动 IC 不自动比较这些重置根分支。这是本轮结构尝试留下的准确 successor obligation。

父研究者提出的更强全分布 quantitative 候选

\[
d(p)\ge\frac{2[G(p)-u_i]}n
\]

在同一八人来源已失败：根取 p 均匀于(2,3,6,7)，精确有

\[
G=733/240<u_1=13/4,\quad d=-1/4,
\quad 2(G-u_1)/7=-47/840,
\]

差为 −163/840。这个反驳发生在 G<u，所以**不否定**更弱的 `G>u=>d>0`。同点 OCC 的三项为

\[
q^TKp=286/105,\quad V^+_{\rm tail}=92/5,\quad\mathcal I=2/3,
\]

可直接检查 `7(286/105)=92/5+2/3`。这些值及逐客户 OCC 非负项已加入 `audit_two_block_pair.py/.json`。没有对新特殊人数类展开研究。

## 9. 占用储备确实能支付当前独立查询缺口，但尚未支付全部导数

在 OCC 的相同一般输入上，令 D(p)=E_AD_i(A)。可以进一步证明一条**非恒等重述的全输入不等式**：

\[
\boxed{\mathcal I_i(p)\ge G_i^+(p)-D_i(p).}\tag{IC-RES}
\]

结合 OCC 得

\[
\boxed{G_i^+(p)+V^+_{\rm tail}\le D_i(p)+nq^TKp
\le u_i+nq^TKp.}\tag{OCC-CURRENT}
\]

第一步对任意完整形式策略成立，第二步才用真实当前 IC。没有把它称为 successor IC 定理；它尚未推出 `G≤u`。

给出逐客户可核的正分解。固定 x，缩写 a_A∈{0,1}、n_A、`d_A=1+b+a_A+n_A`，并记

\[
p_{0,k}=\Pr_{T\sim p}[a_T=0,n_T=k].
\]

令 `q_self=E[a_A/(c_A(c_A+1))]`。独立查询差满足

\[
G_x-D_x=\frac12\mathbb E\frac{\Delta a(\Delta a+\Delta n)}{d_Ad_T}-q_{\rm self}.
\]

从 OCC 的余项相减，即

\[
\begin{aligned}
\mathcal I_x-(G_x-D_x)
&=q_{\rm self}+\frac12\mathbb E\frac{\Delta n^2-\Delta a^2}{d_Ad_T}\\
&=\sum_{A:a_A=1}\frac{p_A[1-p_{0,n_A}]}{(b+1+n_A)(b+2+n_A)}\\
&\quad+\frac12\mathbb E\left[\mathbf1_{\Delta n\ne0}
\frac{\Delta n^2-\Delta a^2}{d_Ad_T}\right]\ge0.
\end{aligned}
\]

最后一式的理由有两个：`p_{0,n_A}≤1`；以及当非零 Δn 是整数时 `Δn²≥1≥Δa²`。被移入第一行 self-tax 的负项恰好是 Δn=0、Δa=±1 的两种有序配对，其总质量为 `Σ_(A:a=1) p_A p_(0,n_A)`，没有额外倍数。这份分解避免将相同 self-tax 支付两次。

因此在假设 `G>u` 的导数论证中，确实已有 `I≥G−D≥G−u>0`。然而只知道 I 正仍不控制 `pᵀKq`；当前的精确剩余式为

\[
d=\frac{V^+_{\rm tail}+\mathcal I}{n}+p^TKq-2G.
\]

本侧尚未从 genuine successor IC 给出使这个值在 G>u 时为正的联合下界。将 OCC-CURRENT 当作已经解决导数或 half 会错。所增加的实际一般关系是 IC-RES / OCC-CURRENT，在证明图中只到这里。

八人源中 p 均匀(2,3,6,7)时，`D=13/4`、`I=2/3`、`G=733/240`，正分解总额为 `I−G+D=69/80`。定义级 Fraction 审计同时核验逐项非负和等式。一般证明由上面的明确分解承担，有限输入不承担量词。
