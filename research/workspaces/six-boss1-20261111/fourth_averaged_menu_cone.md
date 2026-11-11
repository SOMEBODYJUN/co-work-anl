# 第四源六查询平均锥：六权与十一权的精确最优值均为 10

Boss1；RUN `six-boss1-20261111`。本稿只新增本页及 `fourth_averaged_menu_cone/`；不改既有输入、RUN 或登记。

**结论。** 在下述完整六个非负预算权、逐客户 `θ=1/6` 的 64 型锥中，最优系数恰为 **10**，没有优于既有 H3 的第四源平均常数。再加入同一真实分支的末位查询 X、Y，以及 `PAIR(avgQ,X)`、同标签对角平均 `PAIR(avgQ,avgQ)`、`PAIR(X,X)`，所得十一权锥的最优值仍为 **10**。两个结论都有有理可行权、完整逐型核验和精确对偶恒等式；没有第二次优化器调用。

原 H3 权 `(α,sY,sT,aY,aT,δ)=(10,0,0,1,2,1)` 对全部 `0≤θ≤1` 可行。因此同一系数也适用于六标签平均、六标签并集的 `θ=o/6∈{0,1/6}`，包括任意最优覆盖菜单；不增加并集标签行动。这里的最优性只属于明列的逐客户证书锥，不是完整 SPE 锐性或全局松弛最优值。

## 1. 原模型、同一 X 和真实历史

采用[共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同标签目录、六位单位权玩家、任意完整有序历史纯 SPE。保留空覆盖、同覆盖异标签、重复行动、零客户和任意历史依赖弱平局。

固定 actual 路径 `(A1,…,A6)`，对客户 c 记

\[
b_c=\sum_{i=1}^3 1_{c\in A_i},\quad k_c=1_{c\in A_4},\quad
n_c=b_c+1\in\{1,2,3,4\},\quad D_c=n_c+2,\quad P_c=b_c+k_c.
\]

只选定一次共同目录标签

\[
X\in\arg\max_{L\in\mathcal S}f_P(L),\qquad
f_P(L)=\sum_{c\in L}\frac1{P_c+1}.
\]

X 与 [H3 前接原文](maxb_h3_bridge.md)是同一个 actual 前四背景最大者，**没有换成** `Σ_X1/(b+3)` 的最大者。令实际前三有序历史为 h3，沿同一完整策略 σ 定义

\[
Y=\sigma_5(h_3,X),\qquad T=\sigma_6(h_3,X,Y).
\]

以 x,y,t 表示客户对 X,Y,T 的会员位；它们可以相等，标签亦可重复。令 u 为原 actual 第四位收益，强制 X 后第四位收益为 v，真实末位收益为 w。特别地

\[
v=\sum_c\frac{x_c}{n_c+y_c+t_c},\qquad
w=\sum_c\frac{t_c}{n_c+x_c+y_c}.
\]

原源 IC 是 `u−v≥0`，不能将 u 与 v 等同。取六个合法查询标签 Q1,…,Q6，允许重复，设

\[
d_c=\sum_{\ell=1}^6 1_{c\in Q_\ell},\qquad
\bar\theta_c=d_c/6,\qquad
\kappa=\sum_c\frac{x_c}{D_c},\qquad
L(\theta)=\sum_c\theta_c\left(\frac{x_c}{D_c}+\frac{1-x_c}{n_c}\right).
\]

六查询平均不是分数行动；它是同一真实末节点六条合法纯查询 IC 的平均。

## 2. 精确六权锥及其真实付款

所有乘子在全部客户上固定且非负，置 `C=α+sY+sT`。

| 权 | 非负预算 | 实际来源 |
|---:|---|---|
| α | `u−v` | h3 上第四位改选 X，沿该分支真实后继 |
| sY | `u−Σ_c y_c/D_c` | 原第四位改选合法 Y，再沿它自己的真实后继；最坏分母最多 b+3 |
| sT | `u−Σ_c t_c/D_c` | 原第四位改选合法 T，再沿它自己的真实后继；最坏分母最多 b+3 |
| aY | `f_P(X)−f_P(Y)` | 同一个 actual P 上的全目录最大性 |
| aT | `f_P(X)−f_P(T)` | 同一个 actual P 上的全目录最大性 |
| δ | `w−Σ_c θ_c/(n_c+x_c+y_c)` | `θ=barθ` 时为真实末位六查询平均；`0≤θ≤barθ` 时为它的合法减弱 |

两条 SAFE 并不冻结强制 X 分支的 Y,T 后继；Y,T 在这里仅是可供原源偏离的合法标签。两条 MAX 只在全客户相加后非负，未被逐客户使用。

目标 `C u−(C−1)κ−L(θ)` 减去上述六个付款的精确逐客户余项为

\[
\begin{aligned}
E={}&\frac{\alpha x}{n+y+t}+\frac{s_Yy+s_Tt}{D}
-\frac{(C-1)x}{D}
-\theta\left(\frac{x}{D}+\frac{1-x}{n}\right)\\
&-\frac{a_Y(x-y)+a_T(x-t)}{n+k}
-\delta\frac{t-\theta}{n+x+y}.
\end{aligned}\tag{1}
\]

本节的精确优化域为 `n∈{1,2,3,4}`、`k∈{0,1}`、`(x,y,t)∈{0,1}³`，共 64 型，先固定 `θ=1/6`。要求这 64 个 E 均非负，最小化 C。隐藏位没有被当成可以任意共同实现的 SPE；逐型非负只是充分证书要求。

## 3. 可行权、与 H3 的逐项核对

既有 H3 正文 §3 的四项权完全对应

\[
(\alpha,s_Y,s_T,a_Y,a_T,\delta)=(10,0,0,1,2,1).
\tag{2}
\]

它使用源 IC、同一 P 的 `MAX_Y`、`2 MAX_T`、真实末位查询。H3 的 Z 在本文记为 T。该正文把 q 取布尔值；其余项对 q 仿射，因此将 q 换成任意 `θ∈[0,1]` 仍逐客户非负。这里另独立用有理数核对 θ=0、1 两端的全部 128 型，故得到

\[
\boxed{10u-9\kappa\ge L(\bar\theta).}\tag{3}
\]

单次 6 变量、64 行局部 LP 提出的较小 MAX_Y 权为

\[
(10,0,0,1/6,2,1).
\tag{4}
\]

式 (4) 在固定 `θ=1/6` 和 `θ=0` 的全部型也有效，但不能据此删掉任意 `d>1` 的修正，见第 7 节。主陈述一律采用具有任意平均重数范围的 H3 权 (2)。

## 4. 六权锥的精确对偶：C 不可能低于 10

用 `E[n,k,x,y,t]` 表示固定 `θ=1/6` 的式 (1)。下面是**对任意六个权的恒等式**，不以可行性为前提：

\[
\begin{aligned}
64E[1,0,0,0,0]
&+3E[1,0,1,1,0]
+\frac{27}{2}E[1,1,0,0,1]\\
&+15E[4,0,1,1,0]
=\alpha+s_T-10.
\end{aligned}\tag{5}
\]

四个系数全非负，因而

\[
C-10=s_Y+\sum_a\lambda_a E[a]\ge0.
\tag{6}
\]

这同时包括两个源 SAFE 权，而 H3 §7 的旧四权下界未允许这两个预算。因此 (6) 是该指定平均六权锥的完整闭合，不能只用旧四权最优性替代。

还能描述全部最优权。等号使 `sY=0`，式 (5) 的四个活跃余项为零。依次得到

\[
\delta=1,\qquad
2s_T+3a_T=6,\qquad
\alpha=2s_T+6a_T-2,\qquad
\alpha=5s_T+\frac{15}{2}a_T-5.
\]

于是 `sT=0,aT=2,α=10`。余下 MAX_Y 权的必要条件来自两型：

\[
E[1,1,0,1,0]=\frac{a_Y}{2}-\frac1{12}\ge0,
\qquad
E[4,0,1,0,1]=\frac{11}{36}-\frac{a_Y}{4}\ge0.
\]

故完整最优集为

\[
\boxed{(\alpha,s_Y,s_T,a_Y,a_T,\delta)
=(10,0,0,a_Y,2,1),\quad \frac16\le a_Y\le\frac{11}{9}.}\tag{7}
\]

两端各 64 型的精确非负检查给出充分性，中间权由仿射性成立。这里没有把 MAX_Y 权说成唯一。

## 5. 加入真实末位 X/Y 查询和三个 PAIR 后仍为 10

### 5.1 五个额外预算的合法定义

真实前缀为 `(h3,X)`，其背景为 `m=b+x`，置 `z=m+1=n+x`。对合法标签 L,R 定义

\[
f(L)=\sum_c\frac{l_c}{z_c},\qquad
g(L,R)=\sum_c\frac{l_cr_c}{z_c(z_c+1)},\qquad
U(L,R)=f(L)-g(L,R).
\]

真实第五和第六位收益为 `s=U(Y,T)`、`w=U(T,Y)`。同一真实末节点可查询合法 X、Y，逐客户预算是

\[
B_X=\frac{t-x}{z+y},\qquad B_Y=\frac{t-y}{z+y}.
\tag{8}
\]

对任意合法 Q,R，真正两尾 PAIR 预算为

\[
TP(Q,R)=s+w+g(Y,Y)-f(Q)-f(R)+g(Q,R)\ge0.
\tag{9}
\]

其来源可独立核对：设 `J_Q=σ6(h3,X,Q)` 为第五位真改 Q 后的真实末位。式 (9) 精确分解成

\[
[s-U(Q,J_Q)]+[U(J_Q,Q)-U(R,Q)]
+[w-U(J_Q,Y)]+[g(Y,Y)-g(Y,J_Q)].
\]

前三项分别是真实第五位偏离 IC、强制 Q 后真实末位 IC、真实 Y 后末位查询合法 J_Q；最后项逐客户为 `y(1−j_Q)/[z(z+1)]≥0`。没有把强制 Q 授为最优，也没有借用别的历史回复。

记

\[
H=\frac y{z+t}+\frac t{z+y}+\frac y{z(z+1)}.
\]

本文只增加以下三个精确预算，不混入所有 Q,R 的完整二重查询系统：

\[
\begin{aligned}
B_{QX}&=H-\frac{\theta+x}{z}+\frac{\theta x}{z(z+1)},\\
B_{QQ}&=H-\frac{2\theta}{z}+\frac{\theta}{z(z+1)},\\
B_{XX}&=H-\frac{2x}{z}+\frac{x}{z(z+1)}.
\end{aligned}\tag{10}
\]

`B_QQ` 是 `(1/6)Σ_ℓ TP(Qℓ,Qℓ)` 的同标签对角平均，故交叠分子为 **θ**，绝非 θ²。`B_QX` 为 `(1/6)Σ_ℓ TP(Qℓ,X)`；`B_XX` 为 `TP(X,X)`。当 `θ≤barθ` 时，前两个预算因右侧查询费用减少而合法减弱；各费用系数分别为 `1/z−x/[z(z+1)]>0` 与 `2/z−1/[z(z+1)]>0`。

让五个额外非负权依次为 `eX,eY,pQX,pQQ,pXX`，定义

\[
E^+=E-e_XB_X-e_YB_Y-p_{QX}B_{QX}-p_{QQ}B_{QQ}-p_{XX}B_{XX}.
\tag{11}
\]

目标仍为 `C=α+sY+sT`；PAIR 所用 s,w 是该分支真实尾位的钱包，不增添原第四位收益系数。

### 5.2 有理对偶闭合

式 (5) 的四型对偶对五项新预算的加权总和为

\[
(10,10,1,-41/24,11).
\]

只有对角 PAIR 的对偶符号需修补。以下非负原子组合对原六权每个系数和常数均为零：

\[
5E[1,0,0,0,0]+3E[1,0,1,1,1]=0.
\tag{12}
\]

它对五个新预算的总和为 `(0,0,0,5/6,0)`。把 `(41/20)` 倍式 (12) 加到旧对偶，得到扩展对偶权

| 原子 `(n,k,x,y,t)` | 扩展对偶权 |
|---|---:|
| `(1,0,0,0,0)` | 297/4 |
| `(1,0,1,1,0)` | 3 |
| `(1,1,0,0,1)` | 27/2 |
| `(4,0,1,1,0)` | 15 |
| `(1,0,1,1,1)` | 123/20 |

于是任意十一权满足精确恒等式

\[
\boxed{
C-10=s_Y+10e_X+10e_Y+p_{QX}+11p_{XX}
+\sum_a\lambda_a^+E^+[a].
}\tag{13}
\]

所有右侧项非负，所以仍有 `C≥10`。取原 H3 权并将五个新权设零达到此值。没有为扩展锥另跑 LP。

还有一个直接结构检查。在 `n=1,k=0` 的全零型、全一型，式 (11) 非负分别要求

\[
\delta+p_{QX}+\frac32p_{QQ}\ge1,
\qquad
\delta+p_{QX}+\frac52p_{QQ}\le1.
\]

非负权使 `pQQ=0`、`δ+pQX=1`。最优时式 (13) 又强制 `sY=eX=eY=pQX=pXX=0`，因此 δ=1；全部五个扩展权均为零。扩展锥的最优权仍恰为式 (7)。这些原子仅是锥的消元障碍，不被声称共同组成任何完整 SPE 实例。

## 6. 六标签并集与任意 OPT6 菜单

设 `o_c=1_{c∈⋃_ℓ Qℓ}`。始终有 `d_c≥o_c`，每个分母为正，故同一真实末节点满足

\[
w-\sum_c\frac{o_c}{6(n_c+x_c+y_c)}
=\left[w-\sum_c\frac{d_c}{6(n_c+x_c+y_c)}\right]
+\sum_c\frac{d_c-o_c}{6(n_c+x_c+y_c)}\ge0.
\tag{14}
\]

这只减弱六个现有合法查询的平均预算，保留全部客户和真实后继；并集没有被当成目录里的合法主题。取 `θ_c=o_c/6`，H3 权 (2) 给出普遍必要式

\[
\boxed{
10u_4-9\sum_c\frac{x_c}{b_c+3}
\ge\frac16\sum_{c\in\cup_\ell Q_\ell}
\left(\frac{x_c}{b_c+3}+\frac{1-x_c}{b_c+1}\right).
}\tag{15}
\]

亦可直接从式 (3) 减弱得到式 (15)。选择六个达到 OPT6 的合法标签即可用于其最优覆盖并集，重叠不限、标签可重复，所有客户仍被保留。

对十一权锥，将逐型域从固定 `θ=1/6` 扩为 `θ∈{0,1/6}`，其最优值也恰为 10：旧对偶仍属于新域，可行 H3 权同时覆盖新域。最优 `aY` 区间缩为 `[1/6,6/5]`，因为 `θ=0,n=4,k=0,x=1,y=0,t=1` 还要求 `aY≤6/5`；两个端点的 128 型已精确验证。不能把仅固定 θ 的上端 `11/9` 未经检查用于并集域。

## 7. 较小 MAX_Y 权的任意 d 修正（辅助记录）

只有当保留 LP 提出的 `aY=1/6` 时，任意 `d∈{0,…,6}` 需补回

\[
\Pi(n,k,d)=\left[\frac{d}{6n(n+1)}-\frac1{6(n+k)}\right]_+.
\]

该固定权的有效式为

\[
10u-9\kappa-L(\bar\theta)+\sum_{c:x_c=0}\Pi(n_c,k_c,d_c)\ge0.
\tag{16}
\]

仅 `x=0,y=1,t=0` 可能给负余项，那里恰为 `1/[6(n+k)]−d/[6n(n+1)]`；其余隐藏型全非负。故 Π 是给定 n,k,x,d 后消去 y,t 的最小非负逐客户修正，共 448 型精确核对。它只依赖实际前三负载、第四位 bit、菜单重数和 X 会员，若这四项在现有 16 hist 内固定，可直接写为已知 H/X 质量的线性系数。

这里没有更小的 C，因而实用主接口应直接选 H3 的 `aY=1`，它对任意 d 本来无罚；式 (16) 只防止将 LP 的低权端点误推广。

## 8. 可复核资产与边界

命令：

```text
python -B research/workspaces/six-boss1-20261111/fourth_averaged_menu_cone/check_exact.py
```

程序只用标准库 `Fraction`，核验原六权与扩展十一权对偶每一列、全部 64 型、H3 的 128 个 θ 端点型、并集域 128 型和低权修正的 448 型；没有调用优化器或读取任何 LP 点。

- [精确检查程序](fourth_averaged_menu_cone/check_exact.py)。
- [完整 64 型有理系数与余项](fourth_averaged_menu_cone/atom_audit_64.json)、[可读表](fourth_averaged_menu_cone/atom_table.md)。
- [精确证书与来源哈希](fourth_averaged_menu_cone/certificate.json)。
- [H3 θ 端点审计](fourth_averaged_menu_cone/theta_endpoint_audit_128.json)、[并集域审计](fourth_averaged_menu_cone/union_domain_audit_128.json)。
- [低权端点的精确修正](fourth_averaged_menu_cone/lower_endpoint_correction.json)、[并集减弱的正系数](fourth_averaged_menu_cone/union_monotonicity.json)。
- [唯一一次小 LP 的发现记录](fourth_averaged_menu_cone/discovery_lp.json)。

本结果与 [Main 前三源 31／25／19](main_averaged_menu_prefix.md)共享同一 actual 前四最大主题 X，补齐的第四源系数是 10，没有制造新的第四源改进。它没有证明六人半覆盖目标，没有完整 SPE 反例，没有修改固定 16 hist 输入或既有行列，也没有宣称有限锥的最优性覆盖所有可能的非负预算与证明方法。
