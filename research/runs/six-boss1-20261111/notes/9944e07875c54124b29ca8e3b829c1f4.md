# 第三位八预算锥追加三份真实倒二 PAIR：精确最优仍为 61/3

Boss1；RUN `six-boss1-20261111`；执行席 `/root/early3_pair_cone`；2026-11-11。

## 1. 结论与闭合范围

在 [原第三位八权锥](early3_maxx_cone.md) 的八份预算后，仅追加真实前缀

\[
h=(A_1,A_2,X,Y)
\]

上的三份倒二预算 `TP(Q,X), TP(Q,Q), TP(X,X)`，赋予三个全客户固定的非负权 `η1,η2,η3`。指定的 **288 型、11 个非负权逐型证书锥** 的精确最优值仍为

\[
\boxed{C_* = \frac{61}{3}.}
\tag{1}
\]

原证书追加三个零即为一份最优原始证书：

\[
\boxed{
(\alpha_0,s_Y,s_Z,s_T,a_Y,a_Z,a_T,\delta,\eta_1,\eta_2,\eta_3)
=\left(15,\frac23,\frac23,4,1,1,0,1,0,0,0\right).
}
\tag{2}
\]

先直接延伸原有 8 支撑对偶，新增三列的精确约化成本为

\[
\boxed{\left(6,\frac13,\frac{139}{6}\right)>0.}
\tag{3}
\]

因此未启动条件允许的数值发现：**本次真正的优化器调用次数为 0**。下界由一个显式恒等式直接闭合：

\[
\boxed{
\begin{aligned}
6C-122={}&76E_1+12E_{22}+12E_{26}+32E_{34}\\
&+72E_{66}+36E_{69}+36E_{73}+120E_{220}\\
&+36\eta_1+2\eta_2+139\eta_3\ge0.
\end{aligned}}
\tag{4}
\]

行号为第 5 节指定枚举顺序的零基行号。所有最优证书都必须满足

\[
\boxed{\eta_1=\eta_2=\eta_3=0.}
\tag{5}
\]

这没有声称原八权最优向量唯一，也没有把抽象逐型对偶解释成可实现的 SPE。结论仅是这次明确指定的 11 权锥不能降低常数；不是实际 SPE 锐性，不是六人 half 的闭合，也不排除其他真实预算或保留更多客户间信息的证明。

## 2. 完整模型、同一 X 与正确真实历史

模型采用 [共同目录完整历史定义](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户集 `N`，有限非空共同标签目录 `S`，任意覆盖映射，以及六名单位玩家的完整有序历史纯 SPE `σ`。允许空覆盖、同覆盖异标签、重复行动、零客户与历史依赖的任意弱平局；同负载历史不能据此合并。

固定 actual 终局 `(A1,A2,A3,A4,A5,A6)`。每客户令

\[
h_2=(A_1,A_2),\quad
b_j=\mathbf1_{j\in A_1}+\mathbf1_{j\in A_2}\in\{0,1,2\},
\]

\[
k_j=\mathbf1_{j\in A_3}+\mathbf1_{j\in A_4}\in\{0,1,2\},
\qquad P_j=b_j+k_j,\quad n_j=b_j+1\in\{1,2,3\}.
\]

始终选定同一合法标签

\[
X\in\arg\max_{R\in\mathcal S} f_P(R),\qquad
f_P(R)=\sum_{j\in R}\frac1{P_j+1},\qquad F=f_P(X).
\tag{6}
\]

`P` 是 actual 前四负载。X 不重新选成其他背景下的最大者。

只强制原第三位在 `h2` 选择 X，之后沿同一完整策略取真实后继

\[
Y=\sigma_4(h_2,X),\qquad
Z=\sigma_5(h_2,X,Y),\qquad
T=\sigma_6(h_2,X,Y,Z).
\tag{7}
\]

写 `x,y,z,t,q` 为一个客户对 `X,Y,Z,T,Q` 的会员位。`k` 与这些分支会员位保持不同身份，不令 `k=x+y`。对任意合法 Q，记

\[
\kappa_X=\sum_j\frac{x_j}{b_j+4},\qquad
L_{b,4}(X,Q)=\sum_jq_j\left(\frac{x_j}{b_j+4}+\frac{1-x_j}{b_j+1}\right).
\]

`u3` 始终是原 actual 第三人收益。强制 X 后第三人收益及该分支末位收益分别为

\[
v=\sum_j\frac{x_j}{n_j+y_j+z_j+t_j},\qquad
w=\sum_j\frac{t_j}{n_j+x_j+y_j+z_j}.
\tag{8}
\]

本次 PAIR 使用式 (7) 的 **最后两位 Z、T**，其固定前缀恰为 `h=(h2,X,Y)`。对应背景和分母是

\[
m_j=b_j+x_j+y_j,\qquad d_j=m_j+1=n_j+x_j+y_j.
\tag{9}
\]

这不同于 [三尾 PAIR 前稿](maxb_h3_pair_strength.md) 的背景 `b+x`；本次没有漏掉 Y。

## 3. 原八份真实预算

以下预算都在跨全体客户求和后非负。局部客户项不分别假定非负。

**原第三位真实偏离。** 在有序节点 `h2`，第三人实际选择的收益不低于改 X 并跟随真实续局的收益，因此

\[
D_X=u_3-v\ge0.
\]

**三份原节点 SAFE。** 对 `R∈{Y,Z,T}`，R 是合法目录标签。另取第三人在 `h2` 改 R 后由 `σ` 返回的真实三名后继，并令该分支第三人收益为 `v_R`。原节点 IC 给 `u3−v_R≥0`；每个 R 客户未来最多再有三名玩家覆盖，故

\[
S_R=u_3-\sum_j\frac{r_j}{b_j+4}
=(u_3-v_R)+\left(v_R-\sum_j\frac{r_j}{b_j+4}\right)\ge0.
\tag{10}
\]

这里没有把 X 分支的 Y、Z、T 冻结为 R 偏离后的行动。

**三份同一 actual P 最大性。** 式 (6) 和三个标签的合法性给

\[
M_R=F-f_P(R)=\sum_j\frac{x_j-r_j}{n_j+k_j}\ge0,
\qquad R\in\{Y,Z,T\}.
\tag{11}
\]

**真实末节点对 Q 的 IC。** 在 `h=(h2,X,Y)` 后 Z 已选定的真实末节点，T 对 Q 的最优性给

\[
B_Q=w-\sum_j\frac{q_j}{n_j+x_j+y_j+z_j}
=\sum_j\frac{t_j-q_j}{n_j+x_j+y_j+z_j}\ge0.
\tag{12}
\]

原八权依次为 `α0,sY,sZ,sT,aY,aZ,aT,δ`。本次没有增加第四位其他 IC 或未指定查询。

## 4. 新增三份倒二 PAIR 的完整真实付款

固定式 (9) 的真实前缀 `h=(A1,A2,X,Y)`，定义

\[
f^h(L)=\sum_j\frac{l_j}{m_j+1},\qquad
g^h(L,R)=\sum_j\frac{l_jr_j}{(m_j+1)(m_j+2)},
\]

\[
U^h(L,R)=f^h(L)-g^h(L,R)
=\sum_j\frac{l_j}{m_j+1+r_j}.
\tag{13}
\]

最后一个等式只用了会员位 `r∈{0,1}`。Z 是第五位在 h 的真实选择，T 是 Z 后第六位的真实回复。令

\[
s_h=U^h(Z,T),\qquad t_h=U^h(T,Z).
\]

对合法标签 L、R，定义

\[
TP(L,R)=s_h+t_h+g^h(Z,Z)-f^h(L)-f^h(R)+g^h(L,R).
\tag{14}
\]

第五位改 L 后的真实末位回复为

\[
J_L=\sigma_6(A_1,A_2,X,Y,L)=\sigma_6(h,L).
\]

利用 `g^h` 对称性，完整恒等分解为

\[
\begin{aligned}
TP(L,R)={}&[s_h-U^h(L,J_L)]\\
&+[U^h(J_L,L)-U^h(R,L)]\\
&+[t_h-U^h(J_L,Z)]\\
&+[g^h(Z,Z)-g^h(Z,J_L)]\ge0.
\end{aligned}
\tag{15}
\]

四项的支付来源分别是：

1. 第五位在 h 选择 Z，改 L 后跟随真实 `J_L` 的 IC。
2. 第六位在真实偏离历史 `(h,L)` 选择 `J_L`，对 R 的末位 IC。
3. 第六位在真实历史 `(h,Z)` 选择 T，对合法标签 `J_L` 的末位 IC。
4. 逐客户非负差
   \[
   g^h(Z,Z)-g^h(Z,J_L)
   =\sum_j\frac{z_j(1-j_{L,j})}{d_j(d_j+1)}\ge0.
   \]

完整 SPE 量化所有有序历史，所以第二项即使处在离轨节点仍合法；第三项只是把合法标签 `J_L` 当作末位候选，并未把它冻结成其他历史的策略回复。无需假定受迫的第三位 X 在该分支上最优。

本次只用 `(L,R)=(Q,X),(Q,Q),(X,X)`。前两式共用 `J_Q`，第三式使用 `J_X=σ6(h,X)`。若 X、Q 或任意标签重合，式 (15) 仍逐项成立。

对一个局部型令 `d=n+x+y`，写

\[
H=\frac z{d+t}+\frac t{d+z}+\frac z{d(d+1)}.
\]

三份 TP 的逐客户系数恰为

\[
\begin{aligned}
T_1&=H-\frac{q+x}{d}+\frac{qx}{d(d+1)},\\
T_2&=H-\frac{2q}{d}+\frac q{d(d+1)},\\
T_3&=H-\frac{2x}{d}+\frac x{d(d+1)}.
\end{aligned}
\tag{16}
\]

因而 `TP(Q,X)=ΣT1`，`TP(Q,Q)=ΣT2`，`TP(X,X)=ΣT3`。这里不声称每个 `Tℓ≥0`。

## 5. 指定 11 权锥与完整目标恒等式

令全部权非负且在全客户间固定，并设

\[
C=\alpha_0+s_Y+s_Z+s_T.
\]

三个 η 不进入 C。每个类型 `(n,k,x,y,z,t,q)` 的余项是

\[
\begin{aligned}
E={}&\frac{\alpha_0x}{n+y+z+t}
 +\frac{s_Yy+s_Zz+s_Tt}{n+3}
 -\frac{(C-1)x}{n+3}\\
&-q\left(\frac x{n+3}+\frac{1-x}{n}\right)
 -\frac{a_Y(x-y)+a_Z(x-z)+a_T(x-t)}{n+k}\\
&-\frac{\delta(t-q)}{n+x+y+z}
 -\eta_1T_1-\eta_2T_2-\eta_3T_3.
\end{aligned}
\tag{17}
\]

对任意这样的权，展开即得

\[
\begin{aligned}
Cu_3-(C-1)\kappa_X-L_{b,4}(X,Q)
={}&\alpha_0D_X+s_YS_Y+s_ZS_Z+s_TS_T\\
&+a_YM_Y+a_ZM_Z+a_TM_T+\delta B_Q\\
&+\eta_1TP(Q,X)+\eta_2TP(Q,Q)+\eta_3TP(X,X)\\
&+\sum_jE(n_j,k_j,x_j,y_j,z_j,t_j,q_j).
\end{aligned}
\tag{18}
\]

本次数学问题精确是：在

\[
(n,k,x,y,z,t,q)\in\{1,2,3\}\times\{0,1,2\}\times\{0,1\}^5
\]

的全部 288 型上要求 `E≥0`，最小化 C。没有按客户、历史或 Q 改变所用常数。行号按 `n`、`k`、`x`、`y`、`z`、`t`、`q` 的字典积序，q 最快变化，从 0 开始。

写 `E_i=G_i p−h_i`，其中 p 的顺序为式 (2)，则

\[
\begin{aligned}
G_i=\bigg(&\frac{x}{n+y+z+t}-\frac{x}{n+3},
\frac{y-x}{n+3},\frac{z-x}{n+3},\frac{t-x}{n+3},\\
&\frac{y-x}{n+k},\frac{z-x}{n+k},\frac{t-x}{n+k},
\frac{q-t}{n+x+y+z},-T_1,-T_2,-T_3\bigg),
\end{aligned}
\]

\[
h_i=q\left(\frac{x}{n+3}+\frac{1-x}{n}\right)-\frac{x}{n+3}.
\tag{19}
\]

原始 LP 形式是 `min cᵀp, Gp≥h, p≥0`，`c=(1,1,1,1,0,0,0,0,0,0,0)`。本次直接给出其精确证书，并未调用 LP。

由于 PAIR 的背景包含 Y、两尾为 Z、T，式 (17) 一般不对 Y/Z 交换不变。全锥始终保留全部有序 288 型，没有使用 Y/Z 交换压缩。

## 6. 旧 8 支撑对偶逐列延伸

原 [精确证书](early3_maxx_cone/exact_certificate.json) 的八个非零 λ 原样保留。逐型代入式 (16) 得到：

| 零基行号 | `(n,k,x,y,z,t,q)` | λ | T1 | T2 | T3 |
|---:|---|---:|---:|---:|---:|
| 1 | `(1,0,0,0,0,0,1)` | `38/3` | `−1` | `−3/2` | `0` |
| 22 | `(1,0,1,0,1,1,0)` | `2` | `1/3` | `5/6` | `0` |
| 26 | `(1,0,1,1,0,1,0)` | `2` | `0` | `1/3` | `−1/4` |
| 34 | `(1,1,0,0,0,1,0)` | `16/3` | `1` | `1` | `1` |
| 66 | `(1,2,0,0,0,1,0)` | `12` | `1` | `1` | `1` |
| 69 | `(1,2,0,0,1,0,1)` | `6` | `1/2` | `0` | `3/2` |
| 73 | `(1,2,0,1,0,0,1)` | `6` | `−1/2` | `−5/6` | `0` |
| 220 | `(3,0,1,1,1,0,0)` | `20` | `1/30` | `7/30` | `−2/15` |

其余 280 个 λ 为零。三列的加权 T 和为

\[
\begin{aligned}
\sum_i\lambda_iT_{1,i}
&=-\frac{38}{3}+\frac23+0+\frac{16}{3}+12+3-3+\frac23=6,\\
\sum_i\lambda_iT_{2,i}
&=-19+\frac53+\frac23+\frac{16}{3}+12+0-5+\frac{14}{3}=\frac13,\\
\sum_i\lambda_iT_{3,i}
&=0+0-\frac12+\frac{16}{3}+12+9+0-\frac83=\frac{139}{6}.
\end{aligned}
\tag{20}
\]

注意新增矩阵列是 **−T**，其目标系数为零。因此

\[
G^{\mathsf T}\lambda
=\left(1,1,1,1,0,0,0,0,-6,-\frac13,-\frac{139}{6}\right),
\]

\[
c-G^{\mathsf T}\lambda
=\left(0,0,0,0,0,0,0,0,6,\frac13,\frac{139}{6}\right)\ge0,
\qquad h^{\mathsf T}\lambda=\frac{61}{3}.
\tag{21}
\]

这就是新增三列后仍可行的精确对偶。对任意可行 p，有恒等式

\[
\boxed{
C-\frac{61}{3}
=\sum_i\lambda_iE_i+6\eta_1+\frac13\eta_2+\frac{139}{6}\eta_3.
}
\tag{22}
\]

乘六即式 (4)。所有右侧项非负，所以 C 不低于 `61/3`；三个 η 的系数严格正，所以等号时三者必为零。式 (22) 只使用指定逐型非负条件与非负权，没有把 λ 当作任何实际客户分布。

## 7. 精确原始证书与完整非负余项证明

取式 (2)，此时 `η1=η2=η3=0`，式 (17) 等于原八权的最优余项。为使本稿自足，以下保留完整的 36 个基础值及修正项证明。**仅此展示的零 η 原始点**可写 `a=y+z∈{0,1,2}`；这不是对整个 11 权锥的交换约简。

若 `x=0`，令

\[
H_0(n,a,t)=\frac{2a/3+4t}{n+3}+\frac a{n+2}+\frac{1-t}{n+a}-\frac1n.
\]

直接整理给

\[
E_*=H_0(n,a,t)
+a\left(\frac1{n+k}-\frac1{n+2}\right)
+\frac{(1-q)a}{n(n+a)}.
\tag{23}
\]

若 `x=1`，令

\[
H_1(n,a,t)=\frac{15}{n+a+t}
+\frac{2a+12t-58}{3(n+3)}-\frac{2-a}{n}-\frac t{n+1+a}.
\]

则

\[
E_*=H_1(n,a,t)
+(2-a)\left(\frac1n-\frac1{n+k}\right)
+\frac{q(2-a)}{(n+1+a)(n+3)}.
\tag{24}
\]

在 `1≤n≤3,0≤k≤2,0≤a≤2` 的范围，两式 H 之后的修正项全部非负。全部 36 个基础值如下：

| x | n | `(a,t)=(0,0)` | `(0,1)` | `(1,0)` | `(1,1)` | `(2,0)` | `(2,1)` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | `0` | `0` | `0` | `1/2` | `1/3` | `1` |
| 0 | 2 | `0` | `3/10` | `13/60` | `41/60` | `31/60` | `16/15` |
| 0 | 3 | `0` | `1/3` | `41/180` | `29/45` | `22/45` | `43/45` |
| 1 | 1 | `49/6` | `7/6` | `11/6` | `0` | `1/2` | `0` |
| 1 | 2 | `79/30` | `3/5` | `23/30` | `1/15` | `3/20` | `0` |
| 1 | 3 | `10/9` | `5/18` | `11/36` | `1/45` | `0` | `0` |

所以全部 288 型 `E_*≥0`。精确统计为 52 个零、236 个正、0 个负，最小正余项为 `1/45`。对偶八个支撑型恰都为零；式 (21) 的约化成本与式 (2) 的原始变量逐项乘积也都为零。原始、对偶目标精确相等，无需浮点容差。

将这份原始证书代入式 (18)，得到普遍真付款

\[
\boxed{
\begin{aligned}
\frac{61}{3}u_3-\frac{58}{3}\kappa_X-L_{b,4}(X,Q)
={}&15D_X+\frac23(S_Y+S_Z)+4S_T\\
&+M_Y+M_Z+B_Q+\sum_jE_*(j)\ge0.
\end{aligned}}
\tag{25}
\]

因此原不等式仍对同一 X 和每个合法 Q 成立，但这三份新增 PAIR 无法在指定锥中把常数再降低。

## 8. 边界、量词与计算复核

目录有限非空保证式 (6) 中最大标签存在。所有分母至少为 1；没有除以收益、客户数、标签大小或缺额。零客户时所有项为零；空覆盖及重复标签只使部分预算相同或为零。每份预算仍可用固定非负乘子相加。弱平局全程用非严格 IC，真实回复使用原有序标签历史，保留所有离轨分支。

本次首先完整实读原稿、原 [精确证书](early3_maxx_cone/exact_certificate.json) 和原 [独立核验器](early3_maxx_cone/verify_independent.py)，再按本稿正确历史重写三份 TP。原核验器含原目录写操作，因此本次没有运行它；本包以自己的标准库程序重建并核对全部原 2304 个系数、288 个右端和最优余项。

已执行独立复核命令：

```text
python -B research/workspaces/six-boss1-20261111/early3_pair_cone/verify_independent.py
```

结果 `PASS`。该程序不导入生成器，不调用优化器，也不读取任何固定 LP 点。它从“目标减去 11 份预算”的标量表达式，以零向量及 11 个单位向量重新求出 3168 个系数；三份 TP 另用 `U=f−g` 计算，未照抄生成器的 H 表达式。它还检查了背景 `d=1,…,5`、五个会员位全布尔的 160 个 PAIR 付款恒等式，以及最后 g 差的逐型非负性。

| 独立核验内容 | 精确结果 |
|---|---:|
| 有序局部类型 | 288 |
| 11 列矩阵项 | 3168 |
| 与原八列逐项一致 | 2304 |
| PAIR 局部系数 | 864 |
| PAIR 四项真实付款代数式 | 160 |
| 非负最后 g 差 | 160 |
| 最优目标付款恒等式 | 288 |
| 零 η 余项约简恒等式 | 288 |
| 对偶支持 | 8 |
| 原始/对偶目标 | `61/3` / `61/3` |
| 精确间隙 | 0 |
| 真正优化器调用 | 0 |

这里的独立性指不同表达式重建、标准库精确算术、无生成器导入；不是另一机构或另一人员的认证。恒等式及全部有限域取值已经在正文与资产中给出，程序计数不替代其数学理由。

## 9. 工件、来源与冻结释放

| 文件 | 内容 |
|---|---|
| [build_exact.py](early3_pair_cone/build_exact.py) | 直接延伸旧对偶、重建全 288×11 输入并生成证书；不含优化器 |
| [old_dual_extension.json](early3_pair_cone/old_dual_extension.json) | 本次最先进行的旧对偶延伸结果，包括八行 T、加权 T 与三列余项 |
| [local_table_288.json](early3_pair_cone/local_table_288.json) | 完整精确输入：类型、11 个 G 系数、h、三个 T 和最优余项 |
| [local_table_288.csv](early3_pair_cone/local_table_288.csv) | 同一完整输入及输出的可读分数表 |
| [exact_certificate.json](early3_pair_cone/exact_certificate.json) | 精确原始、对偶、新列约化成本、互补条件和整数下界恒等式 |
| [reduced_36_table.json](early3_pair_cone/reduced_36_table.json) | 仅对展示的零 η 原始点使用的 36 个基础值 |
| [verify_independent.py](early3_pair_cone/verify_independent.py) | 无生成器导入、无求解器、仅标准库有理数的独立核验 |
| [independent_verification.json](early3_pair_cone/independent_verification.json) | 上述检查的完整 PASS 输出 |
| [optimization_log.json](early3_pair_cone/optimization_log.json) | 真正优化器调用为零；条件 LP 无需启动，数值输入/输出不存在 |
| [source_manifest.json](early3_pair_cone/source_manifest.json) | 六份实读承重来源的路径、字节数和 SHA-256 |
| [freeze_manifest.json](early3_pair_cone/freeze_manifest.json) / [SHA256SUMS](early3_pair_cone/SHA256SUMS) | 本次交付的文件范围与字节冻结 |

所有原始模型与预算来源均为本次仓库实读材料；未做外部文献或新颖性查询。本包只写 `early3_pair_cone/` 与本稿，没有修改 Git、RUN、registry、凭据、旧数学包、其他查询接口或正在冻结的 23676 系统。

**本明确 11 权义务已完成，结果冻结释放。** 本次没有新增接口行；原 61/3 常数及其既有接口维持原身份。若 Main 后续另派其他预算或查询，应作为新数学义务处理。
