# 六查询均值锥追加真实末两人 PAIR：精确最优仍为 19

Boss1；RUN `six-boss1-20261111`；执行席 `/root/averaged_menu_pair_cone`；2026-11-11。

## 1. 已闭合的数学义务

对六个合法查询的均值预算，固定本次局部系数参数为 `θ=1/6`。在第三位原节点的八预算后，追加同一真实末两人前缀上的三份预算

\[
\overline{TP(Q,X)},\qquad \overline{TP(Q,Q)},\qquad TP(X,X),
\]

并各赋全客户固定的非负乘子。指定的 **144 个有序局部型、11 个非负乘子锥** 的精确最优值是

\[
\boxed{C_*=19.}
\tag{1}
\]

一份最优原始点为

\[
\boxed{
(\alpha,s_Y,s_Z,s_T,a_Y,a_Z,a_T,\delta,\eta_1,\eta_2,\eta_3)
=\left(15,0,0,4,\frac76,\frac76,0,1,0,0,0\right).
}
\tag{2}
\]

下界由四个类型的精确恒等式闭合：

\[
\boxed{
\begin{aligned}
C-19={}&160E_0+36E_{15}+24E_{33}+30E_{110}\\
&+s_Y+s_Z+2a_T+\eta_1+\frac23\eta_2+20\eta_3\ge0.
\end{aligned}}
\tag{3}
\]

行号是第 5 节的零基字典积编号。因此，所有最优证书均满足

\[
\boxed{\eta_1=\eta_2=\eta_3=0.}
\tag{4}
\]

另外，每份可行证书都已有 `η2=0` 与 `δ+η1=1`；最优证书还必须有 `sY=sZ=aT=0, α=15, sT=4, δ=1`。不声称 `aY,aZ` 唯一。

**优化器调用次数为 0。** 四支撑对偶直接由代数获得，获准的一次小型本地 LP 无需启动；没有重跑旧优化器。

这闭合的是指定逐型证书锥，**不是实际 SPE 的锐界**，没有把对偶客户类型解释成可实现博弈，也没有证明六人福利 half 目标或一般查询重数下的无惩罚结论。

## 2. 模型、同一 X 与均值范围

模型完全采用[共同目录完整历史定义](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户集 `N`，有限非空共同标签目录 `S`，任意覆盖映射，六名单位玩家，以及全部有序历史上的同一份完整纯 SPE `σ`。空覆盖、同覆盖异标签、重复行动、零客户、弱平局和离轨历史均保留。

固定 actual 终局 `(A1,…,A6)`，对每个客户记

\[
b=\mathbf1_{A_1}+\mathbf1_{A_2},\qquad
k=\mathbf1_{A_3}+\mathbf1_{A_4},\qquad
P=b+k,\qquad n=b+1,\qquad D=n+3.
\tag{5}
\]

故 `n∈{1,2,3}`、`k∈{0,1,2}`。始终固定同一个合法标签

\[
X\in\arg\max_{R\in\mathcal S}f_P(R),\qquad
f_P(R)=\sum_{j\in R}\frac1{P_j+1},\qquad F=f_P(X).
\tag{6}
\]

`P` 是 actual 前四人的背景。X 不在新的分支或背景上重新取最大者。只强制原第三位在 `h2=(A1,A2)` 选 X，再沿同一完整策略取真实续局

\[
Y=\sigma_4(h_2,X),\quad
Z=\sigma_5(h_2,X,Y),\quad
T=\sigma_6(h_2,X,Y,Z).
\tag{7}
\]

每个客户的 `x,y,z,t` 是对 X、Y、Z、T 的会员位；`k` 仍是 actual 第三、四位的会员数，不令 `k=x+y`。`u3` 始终表示 original actual 第三人的收益。该强制 X 分支中第三人和末位收益为

\[
v=\sum_j\frac{x_j}{n_j+y_j+z_j+t_j},\qquad
w=\sum_j\frac{t_j}{n_j+x_j+y_j+z_j}.
\tag{8}
\]

固定六个合法查询标签 `Q1,…,Q6`，记 `qℓj=1{j∈Qℓ}`。本包只审计固定 `θ=1/6` 的 144 型块。其最直接的字面均值解释为

\[
d_j^{\rm menu}:=\sum_{\ell=1}^6q_{\ell j}=1,
\qquad \theta_j:=\frac16\sum_{\ell=1}^6q_{\ell j}=\frac16=:\theta
\quad\text{对全部被建模客户 }j.
\tag{9}
\]

令

\[
\kappa_X=\sum_j\frac{x_j}{D_j},\qquad
\overline L=\frac16\sum_{\ell=1}^6\sum_jq_{\ell j}
\left(\frac{x_j}{D_j}+\frac{1-x_j}{n_j}\right)
=\sum_j\theta\left(\frac{x_j}{D_j}+\frac{1-x_j}{n_j}\right).
\tag{10}
\]

这里的“全部客户”指进入所用全局预算求和的整个客户集。式 (9) 不能解释成：从一般实例中事后只保留 `dmenu=1` 的客户，并继续宣称删去后的 IC 非负。真菜单均值始终是 `dmenu/6`。式 (9) 给出这个固定参数块的一种充分实现条件，**不是一般原实例必须满足的额外假设**。

### 2.1 与保全客户的并集弱化之间的接口

另令 `oj=1{j∈∪ℓQℓ}`。恒有 `dmenu≥o`，无需删客户。一般实例的真实末位均值预算可弱化为

\[
B_{o/6}=B_{d^{\rm menu}/6}
+\sum_j\frac{d_j^{\rm menu}-o_j}{6(n_j+x_j+y_j+z_j)}\ge0.
\tag{9a}
\]

下文第 4 节的两份 PAIR 均值也具有相同的单调弱化：

\[
\begin{aligned}
TP_{1,o/6}&=TP_{1,d^{\rm menu}/6}
+\sum_j\frac{d_j^{\rm menu}-o_j}{6}
\left(\frac1{d_j}-\frac{x_j}{d_j(d_j+1)}\right)\ge0,\\
TP_{2,o/6}&=TP_{2,d^{\rm menu}/6}
+\sum_j\frac{d_j^{\rm menu}-o_j}{6}
\left(\frac2{d_j}-\frac1{d_j(d_j+1)}\right)\ge0.
\end{aligned}
\tag{9b}
\]

其中局部末两人分母 `dj=nj+xj+yj` 与查询重数 `dmenu` 不同。括号内严格为正，第三份 `TP(X,X)` 不变。式 (9a)—(9b) 保全全部原客户、目录和真实 IC，只增加逐客户非负余量；原菜单可有重叠。

因此，并集内客户恰对应本包的 `θ=1/6` 块，并集外客户对应 `θ=0` 块。这解释了本包如何接到 Main 的普遍并集证明；**本包仍只认证指定的 144 型块，未将 `θ=0` 块或两块合并的完整普遍证明纳入本次最优性义务**。后面的字面均值公式在式 (9) 下直接成立；使用并集时应换成这里明确写出的弱化预算。

## 3. 原八份预算均来自真实历史

以下各式只断言跨全客户求和后的预算非负，不断言每名客户的预算项分别非负。

原第三位对 X 的真实偏离给

\[
D_X=u_3-v\ge0.
\tag{11}
\]

对 `R∈{Y,Z,T}`，R 是共同目录中的合法标签。若原第三位改 R，须跟随该偏离历史后的真实三人续局，令其收益为 `vR`。原节点 IC 与未来至多三名覆盖者给

\[
S_R=u_3-\sum_j\frac{r_j}{D_j}
=(u_3-v_R)+\left(v_R-\sum_j\frac{r_j}{D_j}\right)\ge0.
\tag{12}
\]

没有把 X 分支的 Y、Z、T 冻结成 R 偏离后的行动。式 (6) 对同一 actual 背景的最大性给

\[
M_R=F-f_P(R)=\sum_j\frac{x_j-r_j}{n_j+k_j}\ge0.
\tag{13}
\]

最后，在 X、Y、Z 已经选定的真实末节点，T 分别对六个查询的末位最优性取均值，给

\[
\overline B=\frac16\sum_{\ell=1}^6
\left[w-\sum_j\frac{q_{\ell j}}{n_j+x_j+y_j+z_j}\right]
=\sum_j\frac{t_j-\theta}{n_j+x_j+y_j+z_j}\ge0.
\tag{14}
\]

这些预算的次序为 `DX,SY,SZ,ST,MY,MZ,MT,Bbar`。

## 4. 三份新增 PAIR 的真实付款及均值

与[原非均值 PAIR 锥](early3_pair_cone.md)使用同一正确历史：

\[
h=(A_1,A_2,X,Y),\qquad m_j=b_j+x_j+y_j,\qquad d_j=m_j+1=n_j+x_j+y_j.
\tag{15}
\]

因此真实最后两位是 Z、T，背景中包含 Y。定义

\[
f^h(L)=\sum_j\frac{l_j}{d_j},\qquad
g^h(L,R)=\sum_j\frac{l_jr_j}{d_j(d_j+1)},\qquad
U^h(L,R)=f^h(L)-g^h(L,R).
\tag{16}
\]

布尔会员位保证 `U^h(L,R)=Σ l/(d+r)`。令

\[
\Psi_h=U^h(Z,T)+U^h(T,Z)+g^h(Z,Z),\qquad
TP(L,R)=\Psi_h-f^h(L)-f^h(R)+g^h(L,R).
\tag{17}
\]

对任意合法 L、R，令 `JL=σ6(h,L)` 为第五位改 L 后同一策略给出的真实最后回复。依据[共同锚点与运输引理](../../../archives/customer-attraction/state/引理/跨族末两人菜单的共同锚点与运输界--引理.md)的三 IC 付款，直接展开可得

\[
\begin{aligned}
TP(L,R)={}&[U^h(Z,T)-U^h(L,J_L)]\\
&+[U^h(J_L,L)-U^h(R,L)]\\
&+[U^h(T,Z)-U^h(J_L,Z)]\\
&+[g^h(Z,Z)-g^h(Z,J_L)]\ge0.
\end{aligned}
\tag{18}
\]

第一项是第五位在 h 的真实偏离 IC；第二项是偏离历史 `(h,L)` 上末位对 R 的 IC；第三项是在 `(h,Z)` 的真实末节点以合法标签 JL 为候选的 IC。最后一项等于 `Σ z(1−jL)/[d(d+1)]≥0`。完整历史 SPE 保证所有离轨节点也有这些 IC。这里不要求受迫选 X 的第三位在该分支上最优，也不把 JL 冻结成另一历史的策略回复。

三份新增非负预算精确为

\[
\overline{TP(Q,X)}=\frac16\sum_{\ell=1}^6TP(Q_\ell,X),\quad
\overline{TP(Q,Q)}=\frac16\sum_{\ell=1}^6TP(Q_\ell,Q_\ell),\quad
TP(X,X).
\tag{19}
\]

对一个局部型，令 `d=n+x+y`，并写

\[
\Psi=\frac z{d+t}+\frac t{d+z}+\frac z{d(d+1)}.
\]

式 (19) 的逐客户系数为

\[
\begin{aligned}
T_1&=\Psi-\frac{\theta+x}{d}+\frac{\theta x}{d(d+1)},\\
T_2&=\Psi-\frac{2\theta}{d}+\frac{\theta}{d(d+1)},\\
T_3&=\Psi-\frac{2x}{d}+\frac{x}{d(d+1)}.
\end{aligned}
\tag{20}
\]

第二式是同一查询的对角均值：`qℓ²=qℓ`，所以最后分子是 `θ`，不是 `θ²`。整个均值运算未引入独立随机查询或跨查询配对。每个 `Tj` 可以为负；非负的是相应的全客户预算。

## 5. 11 权锥与系数接口

所有权均非负且全客户固定，定义

\[
C=\alpha+s_Y+s_Z+s_T.
\]

对局部型 `τ=(n,k,x,y,z,t)`，定义

\[
\begin{aligned}
E(\tau)={}&\frac{\alpha x}{n+y+z+t}
+\frac{s_Yy+s_Zz+s_Tt}{n+3}
-\frac{(C-1)x}{n+3}\\
&-\theta\left(\frac{x}{n+3}+\frac{1-x}{n}\right)
-\frac{a_Y(x-y)+a_Z(x-z)+a_T(x-t)}{n+k}\\
&-\frac{\delta(t-\theta)}{n+x+y+z}
-\eta_1T_1-\eta_2T_2-\eta_3T_3.
\end{aligned}
\tag{21}
\]

展开所有全局预算即得恒等式

\[
\begin{aligned}
Cu_3-(C-1)\kappa_X-\overline L
={}&\alpha D_X+s_YS_Y+s_ZS_Z+s_TS_T\\
&+a_YM_Y+a_ZM_Z+a_TM_T+\delta\overline B\\
&+\eta_1\overline{TP(Q,X)}+\eta_2\overline{TP(Q,Q)}
+\eta_3TP(X,X)+\sum_jE(\tau_j).
\end{aligned}
\tag{22}
\]

本次优化问题仅为：在

\[
(n,k,x,y,z,t)\in\{1,2,3\}\times\{0,1,2\}\times\{0,1\}^4
\]

的全部 144 型上要求 `E≥0`，最小化 C。编号从 0 起，按 `n,k,x,y,z,t` 的字典积次序，t 最快变化。PAIR 的背景含 Y，故整个锥不按 Y/Z 交换压缩。

令 `p=(α,sY,sZ,sT,aY,aZ,aT,δ,η1,η2,η3)`，则 `Eτ=Gτp−hτ`，其中

\[
\begin{aligned}
G_\tau=\bigg(&\frac{x}{n+y+z+t}-\frac{x}{n+3},
\frac{y-x}{n+3},\frac{z-x}{n+3},\frac{t-x}{n+3},\\
&\frac{y-x}{n+k},\frac{z-x}{n+k},\frac{t-x}{n+k},
\frac{\theta-t}{n+x+y+z},-T_1,-T_2,-T_3\bigg),
\end{aligned}
\]

\[
h_\tau=\theta\left(\frac{x}{n+3}+\frac{1-x}{n}\right)-\frac{x}{n+3}.
\tag{23}
\]

对应原始问题为 `min cᵀp, Gp≥h, p≥0`，`c=(1,1,1,1,0,0,0,0,0,0,0)`。该接口直接保留全部 144 行，不将局部型的形式可行性当作实际策略可实现性。

## 6. 精确四支撑对偶及全最优点结论

取下表的四个非零对偶权，其余 140 个为零。

| 零基行号 | `(n,k,x,y,z,t)` | λ | T1 | T2 | T3 | h |
|---:|---|---:|---:|---:|---:|---:|
| 0 | `(1,0,0,0,0,0)` | `160` | `−1/6` | `−1/4` | `0` | `1/6` |
| 15 | `(1,0,1,1,1,1)` | `36` | `5/24` | `35/72` | `0` | `−5/24` |
| 33 | `(1,2,0,0,0,1)` | `24` | `5/6` | `3/4` | `1` | `1/6` |
| 110 | `(3,0,1,1,1,0)` | `30` | `1/180` | `31/180` | `−2/15` | `−5/36` |

逐列求和得到

\[
G^{\mathsf T}\lambda
=\left(1,0,0,1,0,0,-2,0,-1,-\frac23,-20\right),
\]

\[
c-G^{\mathsf T}\lambda
=\left(0,1,1,0,0,0,2,0,1,\frac23,20\right)\ge0,
\qquad h^{\mathsf T}\lambda=19.
\tag{24}
\]

这给出式 (3)。其中三个 η 的约化成本严格为正，因此所有 C=19 的可行点都满足式 (4)，还必须令 `sY=sZ=aT=0`。这个结论并非只说“存在一个 η=0 的最优点”。

两个极端型还给出一个更强的可行性事实：

\[
E_0=\frac16\left(\delta-1+\eta_1+\frac32\eta_2\right),
\quad
E_{15}=\frac5{24}\left(1-\delta-\eta_1-\frac73\eta_2\right).
\tag{25}
\]

两式非负而 `η2≥0` 强制

\[
\eta_2=0,\qquad\delta+\eta_1=1.
\tag{26}
\]

代回另外两支撑型，有

\[
E_{33}=\frac{s_T}{4}+\frac{a_T}{3}-1-\eta_3,
\]

\[
E_{110}=\frac\alpha{30}-\frac{s_T}{6}+\frac16-\frac{a_T}{3}
-\frac{\eta_1}{30}+\frac{2\eta_3}{15}.
\tag{27}
\]

由这两式又直接得到

\[
C\ge19+s_Y+s_Z+2a_T+\eta_1+20\eta_3.
\tag{28}
\]

当 C=19 时，两支撑余项均为零，继而 `sT=4, α=15, δ=1`。式 (24) 是不用先消元的完整对偶证书，式 (25)—(28) 给出其简单的代数解释。

## 7. 精确原始点的全 144 型非负证明

取式 (2)。只有此处展示的零 η 对称原始点可写 `a=y+z∈{0,1,2}`。对 `x=0`，定义

\[
H_0(n,a,t)=\frac{4t}{n+3}+\frac{7a}{6(n+2)}
-\frac{t}{n+a}-\frac{a}{6n(n+a)}.
\]

此时

\[
E_*=H_0(n,a,t)+\frac{7a}{6}\left(\frac1{n+k}-\frac1{n+2}\right).
\tag{29}
\]

对 `x=1`，定义

\[
H_1(n,a,t)=\frac{15}{n+a+t}+\frac{24t-109}{6(n+3)}
-\frac{7(2-a)}{6n}-\frac{6t-1}{6(n+1+a)}.
\]

此时

\[
E_*=H_1(n,a,t)+\frac{7(2-a)}6\left(\frac1n-\frac1{n+k}\right).
\tag{30}
\]

所有修正项均非负，36 个基础值如下。

| x | n | `(a,t)=(0,0)` | `(0,1)` | `(1,0)` | `(1,1)` | `(2,0)` | `(2,1)` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | `0` | `0` | `11/36` | `29/36` | `2/3` | `4/3` |
| 0 | 2 | `0` | `3/10` | `19/72` | `263/360` | `13/24` | `131/120` |
| 0 | 3 | `0` | `1/3` | `79/360` | `229/360` | `4/9` | `41/45` |
| 1 | 1 | `197/24` | `29/24` | `133/72` | `1/72` | `1/2` | `0` |
| 1 | 2 | `124/45` | `13/18` | `33/40` | `1/8` | `3/20` | `0` |
| 1 | 3 | `89/72` | `29/72` | `11/30` | `1/12` | `0` | `0` |

因此全部 144 型余项非负：24 个零、120 个正、0 个负，最小正余项 `1/72`。四个对偶支撑全在零余项上，所有非零原始权的约化成本均为零，原始与对偶精确相等。

式 (22) 在这个原始点给出真实全局付款

\[
\boxed{
19u_3-18\kappa_X-\overline L
=15D_X+4S_T+\frac76(M_Y+M_Z)+\overline B+\sum_jE_*(\tau_j)\ge0.
}
\tag{31}
\]

在式 (9) 的范围内，也可将同一接口写成

\[
\boxed{
114u_3\ge\sum_j\left(\frac{109x_j}{n_j+3}+\frac{1-x_j}{n_j}\right).
}
\tag{32}
\]

新增三份 PAIR 在此范围内不能改善原八预算的 19；式 (31) 仍只消耗原八预算中的五份。没有生成或改写共享 registry 的接口行。

## 8. 精确核验、边界和冻结资产

本包只用标准库 `fractions.Fraction`。先由[生成器](averaged_menu_pair_cone/build_exact.py)直接构造精确矩阵、原始点和四支撑对偶，再运行[独立核验器](averaged_menu_pair_cone/verify_independent.py)。后者不导入生成器、不调用求解器；它从“目标减去 11 份实际预算”以零向量和 11 个单位向量重建系数，PAIR 则另从 `U=f−g` 的布尔六查询均值求得。

```text
python -B research/workspaces/six-boss1-20261111/averaged_menu_pair_cone/build_exact.py
python -B research/workspaces/six-boss1-20261111/averaged_menu_pair_cone/verify_independent.py
```

两者均 `PASS`。这里的独立性是不同公式重建、无生成器导入和纯有理数运算，并非另一机构或另一人员的认证。

| 核验项目 | 精确结果 |
|---|---:|
| 有序局部类型 | 144 |
| 11 列矩阵系数 | 1584 |
| 右端 | 144 |
| 三份 PAIR 均值系数 | 432 |
| PAIR 四项付款恒等式 | 160 |
| 最后一项 g 差非负 | 160 |
| 原始点目标付款恒等式 | 144 |
| 任意权的仿射预算重建 | 144 |
| 36 基础值约简恒等式 | 144 |
| 下界恒等式系数与常数 | 12 |
| 对偶支撑 | 4 |
| 原始/对偶目标 | `19 / 19` |
| 精确间隙 | 0 |
| 原始余项零/正/负 | `24 / 120 / 0` |
| 优化器调用 | 0 |

目录有限非空使 X 存在；所有分母为正。没有除以客户数、标签大小、收益或正缺额。零客户时所有付款为零。空覆盖和别名标签仍在完整历史中保留；重复标签只可能令一些预算相同或为零。所有 IC 都是弱不等式，允许历史依赖平局。

| 文件 | 内容 |
|---|---|
| [local_table_144.json](averaged_menu_pair_cone/local_table_144.json) | 全部 144×11 精确矩阵、右端、PAIR 系数、最优余项 |
| [local_table_144.csv](averaged_menu_pair_cone/local_table_144.csv) | 同一输入输出的可读分数表 |
| [exact_certificate.json](averaged_menu_pair_cone/exact_certificate.json) | 原始点、四支撑对偶、约化成本、恒等式和范围 |
| [reduced_36_table.json](averaged_menu_pair_cone/reduced_36_table.json) | 仅用于展示原始点的 36 个基础值 |
| [independent_verification.json](averaged_menu_pair_cone/independent_verification.json) | 全部独立核验的 PASS 结果 |
| [optimization_log.json](averaged_menu_pair_cone/optimization_log.json) | 优化器调用为零，旧优化器重跑为零 |
| [source_manifest.json](averaged_menu_pair_cone/source_manifest.json) | 三份实读只读来源的路径、长度和 SHA-256 |
| [freeze_manifest.json](averaged_menu_pair_cone/freeze_manifest.json) / [SHA256SUMS](averaged_menu_pair_cone/SHA256SUMS) | 交付范围与冻结字节 |

本次仅写 `averaged_menu_pair_cone/` 与本稿，没有修改 Git、RUN、registry、原数学包或其他并行工作区；没有进行外部文献或新颖性检索。

**本指定 11 权义务完成，精确结果冻结释放。** 后续若加入别的预算、放开均值重数或保留更多跨客户信息，应另立新的数学义务；本稿不排除那些方向。
