# actual 第三位、同一 actual 前四最大 X 的八权锥：精确常数 61/3

Boss1；RUN `six-boss1-20261111`。本包只写 `early3_maxx_cone/` 与本稿；没有修改 Git、RUN、registry、旧 51 行或 Main 的 23625 行准备。

## 1. 结论与准确身份

在下述原模型、固定同一 X 与全部合法 Q 下，普遍成立

\[
\boxed{\frac{61}{3}u_3-\frac{58}{3}\kappa_X
\;\ge\;L_{b,4}(X,Q).}
\tag{NEW}
\]

这把旧任意锚 AP 在该位置的常数 23 降低了 `8/3`。新证明确实使用 X 在 **actual 前四负载 P 下**的全目录 `f_P` 最大性；没有把 X 换成较早背景下的 κ 最大者，也没有从旧 AP 的任意锚量词直接推出新常数。

指定的八个客户无关非负权的逐型锥，精确最优为

\[
\boxed{C_* = 61/3,\qquad
(\alpha_0,s_Y,s_Z,s_T,a_Y,a_Z,a_T,\delta)
=(15,2/3,2/3,4,1,1,0,1).}
\tag{OPT}
\]

一份 8 支撑精确有理对偶证明此锥中不能进一步降低 C。这个下界只针对本稿明确的八权、288 型逐客户支付锥；它不是实际 SPE 的锐性结论，不是六人 half 的闭合，也没有构造达到该常数的真实实例。

发现时仅运行 **一次** `288×8` 本地 LP，优化器时间约 `0.010583` 秒，设置的时间上限为 60 秒。没有读旧点或新 5b1b 点来拟合。随后所有原对偶、旧守卫、288 型、36 型约简及付款恒等式都用精确有理算术核验；最终证明不依赖浮点容差。

## 2. 模型、同一 X 和真实有序历史

客户集 N 有限，每个客户单位价值；共同目录 S 是有限非空的**标签集**，标签映射到客户覆盖子集。允许空覆盖标签、同覆盖异标签、重复行动、零客户与任意历史依赖弱平局。固定任意一份完整有序历史纯 SPE σ；两个负载相同但有序标签历史不同的节点仍可有不同续局。

固定 σ 的 actual 终局 `(A1,A2,A3,A4,A5,A6)`。对客户 j，令

\[
h_2=(A_1,A_2),\qquad
b_j=\mathbf 1_{j\in A_1}+\mathbf 1_{j\in A_2}\in\{0,1,2\},
\]

\[
k_j=\mathbf1_{j\in A_3}+\mathbf1_{j\in A_4}\in\{0,1,2\},
\quad P_j=b_j+k_j,
\quad n_j=b_j+1\in\{1,2,3\}.
\]

取并固定一个目录标签

\[
X\in\arg\max_{R\in\mathcal S}f_P(R),\qquad
f_P(R)=\sum_{j\in R}\frac1{P_j+1},\qquad F=f_P(X).
\]

目录有限非空保证最大标签存在。所有后续不等式共用这个 X；不按客户、Q、负载或历史重新选择 X。

仅强制第三人在原前缀 h₂ 选择 X，其后使用同一 σ 的真实后继：

\[
Y=\sigma_4(A_1,A_2,X),\quad
Z=\sigma_5(A_1,A_2,X,Y),\quad
T=\sigma_6(A_1,A_2,X,Y,Z).
\tag{H}
\]

写 `x,y,z,t,q` 为客户对 `X,Y,Z,T,Q` 的会员位。第三人选择 X 后的真实最终收益与该分支真实末位收益是

\[
v=\sum_j\frac{x_j}{b_j+1+y_j+z_j+t_j},\qquad
w=\sum_j\frac{t_j}{b_j+x_j+y_j+z_j+1}.
\]

这里 `u3` 始终是原 actual 终局第三人的收益。目标中

\[
\kappa_X=\sum_j\frac{x_j}{b_j+4},\qquad
L_{b,4}(X,Q)=\sum_jq_j
\left(\frac{x_j}{b_j+4}+\frac{1-x_j}{b_j+1}\right).
\]

实际 P 与强制 X 分支各有其身份：`P=b+k` 使用原 actual 的 A3、A4；v、w 使用 (H) 的 X、Y、Z、T。新证明没有令 `k=x+y`，也没有冻结偏离后的行动。

## 3. 八份预算及其合法来源

下面每份预算都是**跨全部客户求和后**非负，不能当成逐客户非负。逐客户剩余项会单独核验。

### 3.1 原第三人选择 X 的真实激励

完整 SPE 在原有序历史 h₂ 给

\[
D_X:=u_3-v\ge0.
\]

此外 X 分支的每个 X 客户终局分母至多 `b+4`，所以 `v≥κ_X`，从而 `u3≥κ_X`。这条 SAFE 事实也说明降低常数的方向：旧常数 23 的目标左侧减新目标左侧，恰是 `(8/3)(u3−κ_X)≥0`。

### 3.2 三份原 h₂ 的 SAFE 预算

对 `R∈{Y,Z,T}`，定义

\[
S_R:=u_3-\sum_{j\in R}\frac1{b_j+4}\ge0.
\tag{SAFE}
\]

完整付款如下。Y、Z、T 是 (H) 中策略实际返回的标签，故分别属于共同目录 S。把这些标签作为原 h₂ 的候选行动时，对每个 R 单独令

\[
B_4^R=\sigma_4(A_1,A_2,R),\quad
B_5^R=\sigma_5(A_1,A_2,R,B_4^R),\quad
B_6^R=\sigma_6(A_1,A_2,R,B_4^R,B_5^R).
\]

若第三人在这个真实 R 分支的收益是 v_R，则第三人的原节点最优性给 `u3−v_R≥0`；未来只有三名玩家，给

\[
v_R\ge\sum_{j\in R}\frac1{b_j+4},
\quad
S_R=(u_3-v_R)+\left(v_R-\sum_{j\in R}\frac1{b_j+4}\right)\ge0.
\]

这些续局可以与 X 分支完全不同；没有把 X 分支的 Y、Z、T 固定为其他偏离后的行动。重复标签只会使部分预算相同，不妨碍使用固定非负乘子。

### 3.3 同一 actual P 下三份全目录最大性预算

由固定 X 的定义和 Y、Z、T 的合法性，

\[
M_R:=F-f_P(R)=\sum_j\frac{x_j-r_j}{n_j+k_j}\ge0,
\qquad R\in\{Y,Z,T\}.
\tag{MAX}
\]

这是同一个 actual P 下的目录比较，既不要求 X 最大化 κ，也不要求 Y、Z、T 在 P 下由任何玩家实际选择。最优支付使用 `aY=aZ=1,aT=0`；仍保留第三份预算在八权锥中的位置。

### 3.4 X 分支真实末节点的一份 Q 激励

固定任意合法标签 Q。在真实末节点 `(A1,A2,X,Y,Z)`，T 是 σ 的选择；改成 Q 已无未来行动，真实偏离收益为

\[
p_Q=\sum_j\frac{q_j}{n_j+x_j+y_j+z_j}.
\]

因此

\[
B_Q:=w-p_Q=\sum_j\frac{t_j-q_j}{n_j+x_j+y_j+z_j}\ge0.
\tag{LAST}
\]

这些合法标签和历史给出了全部八份预算。没有使用玩家 4、5 的额外激励，没有加入 TP 或其他未写出的前提。

## 4. 完整支付恒等式与原证书

对任意非负八权，令 `C=α0+sY+sZ+sT`。每型

\[
\begin{aligned}
E(n,k,x,y,z,t,q)={}&
\frac{\alpha_0x}{n+y+z+t}
+\frac{s_Yy+s_Zz+s_Tt}{n+3}
-\frac{(C-1)x}{n+3}\\
&-q\left(\frac{x}{n+3}+\frac{1-x}{n}\right)
-\frac{a_Y(x-y)+a_Z(x-z)+a_T(x-t)}{n+k}
-\frac{\delta(t-q)}{n+x+y+z}.
\end{aligned}
\tag{E}
\]

逐项展开恰得

\[
\begin{aligned}
Cu_3-(C-1)\kappa_X-L_{b,4}(X,Q)
={}&\alpha_0D_X+s_YS_Y+s_ZS_Z+s_TS_T\\
&+a_YM_Y+a_ZM_Z+a_TM_T+\delta B_Q
+\sum_{j\in N}E(n_j,k_j,x_j,y_j,z_j,t_j,q_j).
\end{aligned}
\tag{PAY-general}
\]

在 (OPT) 处，这成为新引理的完整非负分解

\[
\boxed{
\begin{aligned}
\frac{61}{3}u_3-\frac{58}{3}\kappa_X-L_{b,4}(X,Q)
={}&15D_X+\frac23(S_Y+S_Z)+4S_T\\
&+M_Y+M_Z+B_Q+\sum_jE_*(j).
\end{aligned}}
\tag{PAY-new}
\]

下一节证明所有 `n∈{1,2,3},k∈{0,1,2},(x,y,z,t,q)∈{0,1}^5` 共 288 型的 `E_*≥0`。结合第 3 节各真实预算非负，即完成 (NEW) 的普遍证明。

## 5. 288 型的自足精确证明：约简为 36 个数

写 `m=y+z∈{0,1,2}`。最优余项对 y、z 对称。若 `x=0`，定义

\[
H_0(n,m,t)=\frac{2m/3+4t}{n+3}
+\frac m{n+2}+\frac{1-t}{n+m}-\frac1n.
\]

直接整理 (E) 给

\[
E_*=H_0(n,m,t)
+m\left(\frac1{n+k}-\frac1{n+2}\right)
+\frac{(1-q)m}{n(n+m)}.
\tag{RED-0}
\]

若 `x=1`，定义

\[
H_1(n,m,t)=\frac{15}{n+m+t}
+\frac{2m+12t-58}{3(n+3)}
-\frac{2-m}{n}-\frac t{n+1+m}.
\]

则

\[
E_*=H_1(n,m,t)
+(2-m)\left(\frac1n-\frac1{n+k}\right)
+\frac{q(2-m)}{(n+1+m)(n+3)}.
\tag{RED-1}
\]

在指定整数范围内，两式 H 后的各项均非负。全部 36 个 H 的精确值为：

| x | n | (m,t)=(0,0) | (0,1) | (1,0) | (1,1) | (2,0) | (2,1) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 | 0 | 1/2 | 1/3 | 1 |
| 0 | 2 | 0 | 3/10 | 13/60 | 41/60 | 31/60 | 16/15 |
| 0 | 3 | 0 | 1/3 | 41/180 | 29/45 | 22/45 | 43/45 |
| 1 | 1 | 49/6 | 7/6 | 11/6 | 0 | 1/2 | 0 |
| 1 | 2 | 79/30 | 3/5 | 23/30 | 1/15 | 3/20 | 0 |
| 1 | 3 | 10/9 | 5/18 | 11/36 | 1/45 | 0 | 0 |

因此所有 288 型均非负；其中 52 型为零，其余型最小正余项为 `1/45`。这是一份有限域的完整有理证明；不是抽样或浮点数值检查。

## 6. 八权锥的精确对偶障碍

将 (E) 写为 `E_i=G_i p−h_i`，其中 `p=(α0,sY,sZ,sT,aY,aZ,aT,δ)`，逐型列顺序为 `(n,k,x,y,z,t,q)`，且

\[
\begin{aligned}
G_i=\bigg(&\frac{x}{n+y+z+t}-\frac{x}{n+3},
\frac{y-x}{n+3},\frac{z-x}{n+3},\frac{t-x}{n+3},\\
&\frac{y-x}{n+k},\frac{z-x}{n+k},\frac{t-x}{n+k},
\frac{q-t}{n+x+y+z}\bigg),
\end{aligned}
\]

\[
h_i=q\left(\frac{x}{n+3}+\frac{1-x}{n}\right)-\frac{x}{n+3}.
\]

局部 LP 是 `min c·p`，`Gp≥h,p≥0`，`c=(1,1,1,1,0,0,0,0)`。以下仅八个 λ 非零；其余 280 个全为零。

| 零基行号 | n | k | x | y | z | t | q | λ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 38/3 |
| 22 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 2 |
| 26 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 2 |
| 34 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 16/3 |
| 66 | 1 | 2 | 0 | 0 | 0 | 1 | 0 | 12 |
| 69 | 1 | 2 | 0 | 0 | 1 | 0 | 1 | 6 |
| 73 | 1 | 2 | 0 | 1 | 0 | 0 | 1 | 6 |
| 220 | 3 | 0 | 1 | 1 | 1 | 0 | 0 | 20 |

逐列精确相加为

\[
G^{\mathsf T}\lambda=(1,1,1,1,0,0,0,0)=c,
\qquad h^{\mathsf T}\lambda=61/3.
\]

特别是对任意满足 288 条 `E_i≥0` 的八权，有恒等式

\[
\boxed{
3C-61=
38E_1+6E_{22}+6E_{26}+16E_{34}
+36E_{66}+18E_{69}+18E_{73}+60E_{220}\ge0.}
\tag{DUAL}
\]

所以 `C≥61/3`。最优原证书满足所有 λ 支撑行恰为零；原对偶目标精确相等、八个 reduced cost 全零。这证明本八权锥的最优值，而不把这些抽象逐型对偶权解释成一份可实现的全历史 SPE 客户构造。

## 7. 旧 23 守卫、边界与来源

在运行唯一一次优化之前，先把

\[
(\alpha_0,s_Y,s_Z,s_T,a_Y,a_Z,a_T,\delta)
=(15,2,2,4,0,0,0,1),\qquad C=23
\]

代入全部 288 型 (E)，精确结果最小值 0、零项 54，全部非负。这核对了付款中的 SAFE、MAX、末位 IC 符号和方向。旧守卫对应原 AP 在 `r=4,M=6` 下的显式付款；新证书在同一真实历史预算上另外调用两份 MAX，因而有独立来源。

本证明没有除以收益、κ、slack、客户数或 X 的大小。零客户时全式为零；空 X 也直接适用，且当它是 f_P 最大者时，正权和非负覆盖已迫使所有合法标签为空覆盖。弱平局保留为非严格不等式。覆盖相同但标签不同的所有有序历史均按原标签使用，不能商成同一个节点。不同预算中的标签若恰好相等，各份非负预算仍可以相加。

实读承重来源：

- [共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：标签目录、全有序历史 SPE、真实续局、空覆盖及零客户边界。
- [旧 AP 原主稿](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md)：任意锚 AP、原节点 SAFE 来源及真实末位付款。
- [原 CLAIMS](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/CLAIMS.md) 与 [原 README](../../../archives/customer-attraction/tools/evidence/background-bns-and-ap-primary/original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/README.md)：旧结果的精确范围和有限审计边界。
- [现行 early X 原查询包第 3 节](early_x_anchor_queries.md)：M=6 下旧 AP 的完整显式付款；本包没有用其旧点评价文件。

来源字节 SHA、局部数学证书、完整表和独立核验输出一起冻结。没有查询外部文献或做新颖性认证。

## 8. 工件与复核入口

| 文件 | 内容 |
|---|---|
| [exact_certificate.json](early3_maxx_cone/exact_certificate.json) | 精确原权、8 支撑对偶、全零 reduced cost、互补条件与旧守卫 |
| [local_table_288.json](early3_maxx_cone/local_table_288.json) | 全部 288 型、8 个精确系数、h、旧/新余项 |
| [local_table_288.csv](early3_maxx_cone/local_table_288.csv) | 同一完整局部表的可直接阅读版本 |
| [reduced_36_table.json](early3_maxx_cone/reduced_36_table.json) | 第 5 节的全部 36 个精确基础值 |
| [discover_once.py](early3_maxx_cone/discover_once.py) | 唯一一次、60 秒上限的 LP 发现程序；不要为复核重复优化 |
| [numerical_input.json](early3_maxx_cone/numerical_input.json) / [numerical_result.json](early3_maxx_cone/numerical_result.json) | 原数值输入数组、完整 SciPy 返回数组及实际优化时间 |
| [verify_independent.py](early3_maxx_cone/verify_independent.py) | 仅标准库 Fraction；不导入生成器、不调用优化器、不读任何游戏点；由原式的仿射基向量重建全部系数 |
| [independent_verification.json](early3_maxx_cone/independent_verification.json) | 288 型、2304 系数、288 付款系数、288 约简恒等式、36 基础型及精确对偶全部 PASS |

复核命令，在仓库根执行：

```sh
python research/workspaces/six-boss1-20261111/early3_maxx_cone/verify_independent.py
```

独立核验的“独立”准确指重新从显示原式构建系数、无生成器导入、无求解器与无旧点读取；不是另一个人或外部审查机构的认证。本数学包冻结后，Main 可再决定是否将常数更新转成已有列的必要行；本稿的普遍结论本身不依赖任何固定支持点评价。
