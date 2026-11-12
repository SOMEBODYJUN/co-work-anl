# λ≥25 的完整域、全部退化射线与整域非负闭合

Boss1；`six-boss1-20261111`；执行席 `/root/high_lambda_closure`。

## 结论与准确范围

对五个真实源 $i=1,\ldots,5$ 及两个基准 $q_0=1/6,1/5$，指定坐标最小帽、全尾111…1零查询锚在 **全部 $\lambda\ge25$** 上的准确域为

\[
\boxed{\lambda\ge25,\qquad \tau_j\ge0,\qquad
\frac45\tau_j+\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)}
\le\frac{\lambda-1}{30}-\frac{q_0}{2}\quad(j=i+1,\ldots,5).}
\tag{H-DOMAIN}
\]

每个基准的五域分别有 **9、7、5、3、1 个真面**，**16、8、4、2、1 个顶点**及同数极端退化射线。所有顶点都在 $\lambda=25$；所有非零射线均可唯一归一为 $\delta\lambda=1$。两套共50面、62顶点、62射线。内部权确会沿射线增长，因而不能仅把固定 $\tau$ 的 $\lambda$ 斜率认作 SAFE 就结束。

不过，本包给出更强的**整域非负身份**：每条退化射线及整个无界域上的每条 pure、ordered 行，都由现有 $\lambda=25$ 同目标端点行、原实际节点对合法标签的 SAFE 行、六个合法查询的 SAFE 平均，以及逐客户非负质量支付。C-only 另准确保留真正最大标签的自由大小等式。该身份在全部512个九位客户型及独立K列上成立，且在全部方向变量上逐多项式系数核验。

所以相对于以上已有预算及客户非负性，**此高 $\lambda$ 路线没有新增不等式信息，完整闭合**。这里“六查询 SAFE 平均”明确是六条真实合法标签 SAFE 的非负平均，随后作 $d\ge o$ 的非负投影；没有将覆盖并O当作合法行动。若某个另设的有限矩阵只保八个指定标签 SAFE、却未保合法查询菜单的 SAFE 平均，则本结论不自动等同于那个较小矩阵的行锥包含。本包主张的是题设“任意合法T的 actual SAFE”所生成的普遍必要锥闭合。

不物化重复巨型矩阵；仅保存准确域、全部顶点/射线、全状态证书、全列身份、旧行对应和独立核验。没有读取全局LP、候选点或最优面，没有优化器，没有改动旧冻结包、正文、Git、RUN、map或registry。

## 1. 模型、真实付款和统一记号

沿用[共同目录完整历史模型](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空带标签共同目录、恰六名单位提供者，任取一份在所有完整有序历史上定义的纯SPE。保留空覆盖、重复选择、同覆盖异标签、查询索引重复、零客户和全部在轨/离轨弱平局。不同有序历史不合并为负载状态。

固定原实际第i源节点；$u_i$ 是原实际收益。强制任意合法T后，只使用同一策略在该真实历史后的后继 $R_{i+1},\ldots,R_6$。分支内部收益是 $v_j$，不换成原路径收益。令

\[
J=\{i+1,\ldots,5\},\quad m=5-i,\quad n=6-i,
\quad p\in\{0,\ldots,i-1\},\quad D=p+7-i.
\]

令 $t=1_T$，中间会员为 $r_j$，末位 $z=r_6$。定义

\[
\beta_j=\frac{q_0}{2}+\tau_j+
\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)},\quad
B=\sum_j\beta_j,\quad S=1+B,\quad
\Theta=\sum_j\tau_j,\quad a=\lambda+\Theta.
\tag{WEIGHTS}
\]

K是全目录最大裸大小，C仅在确实达到 $|C|=K$ 时用于C-only。另取任意六个合法查询 $Q_1,\ldots,Q_6$，其重数为d、覆盖并会员为 $o=1_{d>0}$。O不是一个合成合法行动。

[正式联合引理](../../../../archives/customer-attraction/state/引理/联合内部偏离的完整参数域与同菜单条件投影--引理.md)第2、5、7节给出的真实预算，在本记号下为

\[
P=a u_i+SK-\sum_x\Psi_x\ge0,
\]
\[
\Psi=\frac{at-z-\sum_j\tau_jr_j}{p+t+\sum_jr_j+z}
+\sum_j\beta_jr_j+z
+\frac q{p+t+\sum_jr_j+1}
+\sum_j\frac{\tau_jq}{p+t+\sum_{h<j}r_h+7-j}.
\tag{COST}
\]

零负载时首分子亦为零，首项取零。P准确由源IC的权a、真实中间CAP的权 $\beta_j$、末CAP和末BR各权1、同分支内部SAFE各权 $\tau_j$ 相加而成。内部j再次偏离到合法查询时，其后继沿该次新历史继续；SAFE分母使用后续至多 $6-j$ 人覆盖的界，未冻结外层后继。

整个 $\tau\ge0$ 象限均有

\[
m_0(p,0)=0,\qquad
m_0(p,q_0)=Z(p)=q_0\left[\frac1{p+1}+\sum_j\frac{\tau_j}{p+7-j}\right].
\tag{ZERO}
\]

理由是最小帽中的交叉项支付所有内部查询分母损失，常数帽支付末查询损失，余下实际份额为非负的 $(z+\sum\tau_jr_j)(1-1/L)$。本包对每一真实尾另从个人份额重建456个仿射余项；没有重新把旧程序输出当作证明。

当 $\lambda\ge25\ge(D-1)^2$ 时，全中间会员且末位1的零查询锚为

\[
W(p)=B+1+\frac{\lambda-1}{D}=S+\frac{\lambda-1}{D}.
\tag{ANCHOR}
\]

此锚所有内部查询和末BR查询的分母都是D。其他真实尾的查询分母不超过D，因此零查询锚一旦成立，就对所有 $q\ge0$ 有

\[
m_1(p,q)=W(p)+\frac{1+\Theta}{D}\,q.
\tag{POSITIVE-QUERY}
\]

## 2. 全部真实状态推出准确域：多缺态没有遗漏

令 $M\subseteq J$ 为缺失中间集，$k=|M|$，$U=\sum_{j\in M}\tau_j$。每一真实零查询余项是

\[
\rho_{D,M,z}=\frac{\lambda+U-z}{D-1-k+z}+z
-\sum_{j\in M}\beta_j-1-\frac{\lambda-1}{D}.
\tag{RHO}
\]

所有分母正，因为 $D-k\ge p+2\ge2$。以下三个准确身份支付全部状态，而非从单缺猜测完整域。

### 2.1 同一缺集的末位0由末位1支付

\[
\rho_{D,M,0}-\rho_{D,M,1}
=\frac{\lambda+U-(D-k-1)^2}{(D-k)(D-k-1)}\ge0.
\tag{LAST-BIT}
\]

分子准确分为 $(\lambda-25)+U+[25-(D-k-1)^2]$，三项均非负。特别 $D=6,M=\varnothing,z=0$ 给 $(\lambda-25)/30$，所以全尾末1锚本身也迫使 $\lambda\ge25$。

### 2.2 同一缺集的最强前缀是D=6

对末位1，

\[
\rho_{D,M,1}
=\frac{k(\lambda-1)}{D(D-k)}+\frac{U}{D-k}-\sum_{j\in M}\beta_j.
\]

于是

\[
\begin{aligned}
\rho_{D,M,1}-\rho_{6,M,1}
={}&k(\lambda-1)\left[\frac1{D(D-k)}-\frac1{6(6-k)}\right]\\
&+U\left[\frac1{D-k}-\frac1{6-k}\right]\ge0.
\end{aligned}
\tag{PREFIX}
\]

每个源都有实际允许前缀 $p=i-1$ 对应D=6，故这个最强状态并非不真实的外加状态。

### 2.3 D=6的多缺态是单缺和加非负余项

定义每个单缺松弛

\[
g_j=\frac{\lambda-1}{30}+\frac{\tau_j}{5}-\beta_j
=\frac{\lambda-1}{30}-\frac{q_0}{2}-\frac45\tau_j
-\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)}.
\]

对 $k\ge1$，

\[
\boxed{\rho_{6,M,1}
=\sum_{j\in M}g_j+
\frac{k-1}{6-k}\left[\frac{k(\lambda-1)}{30}+\frac U5\right].}
\tag{MULTI-MISSING}
\]

k=0时余项为0。后三项只使用 $\lambda-1\ge24$、非负 $\tau$ 和各 $g_j\ge0$。反向，每个 $g_j$ 就是D=6、仅缺j、末位1的真实余项。故(H-DOMAIN)必要且充分。$a\ge25>0$，各 $\beta_j\ge q_0/2>0$，所有真实预算合法。

`all_state_certificates.json`保存每个p、每个M、两种末位，不删除恒零式、重复式或弱达到态。每一 $\rho$ 都准确展开为若干 $g_j$ 加 $\delta=\lambda-25$、各 $\tau_j$、常数1的非负线性组合。零查询共228式，两套查询斜率差另有228式。

## 3. 全部面、顶点、极端射线及无损参数分解

设

\[
L_0=24-15q_0>0,
\qquad h(\lambda)=\frac{L_0+\lambda-25}{30}.
\]

两基准分别有 $L_0=43/2$ 和21。固定h的截面是上三角多胞体

\[
\tau_j\ge0,\qquad
\frac45\tau_j+\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)}\le h.
\tag{SECTION}
\]

任一可行点有 $\tau_j\le5h/4$。因此任意坐标上界中的交叉项至多为

\[
\frac{5h q_0}{4}\sum_{\ell>j}\frac1{(7-\ell)(8-\ell)}
\le\frac{3h}{40}<h.
\]

每坐标的上下界永不同时活跃。一个顶点需m个独立活跃边界，所以每坐标恰选下界或上界；所选法向为可逆三角阵。全部顶点准确由 $\varepsilon\in\{0,1\}^m$ 递推：

\[
\tau_j^{\varepsilon}(h)=\varepsilon_j\frac54
\left[h-\sum_{\ell>j}\frac{q_0\tau_\ell^{\varepsilon}(h)}{(7-\ell)(8-\ell)}\right],
\qquad j=5,4,\ldots,i+1.
\tag{CORNERS}
\]

整个高段域的顶点均为

\[
\boxed{b_\varepsilon=(25,\ L_0 v_\varepsilon),\quad
v_\varepsilon=\tau^\varepsilon(1/30).}
\]

其退化锥为

\[
\delta\lambda\ge0,\qquad v\ge0,\qquad
\frac45v_j+\sum_{\ell>j}\frac{q_0v_\ell}{(7-\ell)(8-\ell)}\le\frac{\delta\lambda}{30}.
\tag{RECESSION}
\]

$\delta\lambda=0$ 时正对角和非负v迫使v=0，所以所有非零射线可归一 $\delta\lambda=1$。归一截面的全部顶点就是上式的 $v_\varepsilon$，全部极端射线为

\[
\boxed{r_\varepsilon=(1,v_\varepsilon).}
\]

| 源i | 维数 | 每基准真面 | 每基准基顶点 | 每基准极端射线 |
|---:|---:|---:|---:|---:|
| 1 | 5 | 9 | 16 | 16 |
| 2 | 4 | 7 | 8 | 8 |
| 3 | 3 | 5 | 4 | 4 |
| 4 | 2 | 3 | 2 | 2 |
| 5 | 1 | 1 | 1 | 1 |

第五源没有内部变量。各域满维；$\delta=1,\tau_j=1/100$ 是严格内点。每个所列边界的支撑顶点差及面内退化方向张成余维一空间，故没有冗余面。独立检查器枚举全部独立边界组合、另枚举归一退化截面的全部边界组合并核此秩条件。

更直接地，给定任一高段参数，置

\[
\delta=\lambda-25,\qquad
v=\frac{\tau}{L_0+\delta},\qquad \tau^0=L_0v.
\tag{RADIAL}
\]

v属于归一退化截面，$\tau^0$属于 $\lambda=25$ 截面。若 $v=\sum\theta_\varepsilon v_\varepsilon$，其中 $\theta_\varepsilon\ge0,\sum\theta_\varepsilon=1$，则

\[
(\lambda,\tau)=\sum_\varepsilon\theta_\varepsilon b_\varepsilon
+\delta\sum_\varepsilon\theta_\varepsilon r_\varepsilon.
\tag{MINKOWSKI}
\]

这给出完整的有界顶点加退化射线表示，不留下大 $\lambda$ 的未处理窗口。全部准确坐标见[端点表](endpoint_table.md)和[参数域](parameter_domains.json)。

## 4. Pure、ordered及真实SAFE平均的准确行

### 4.1 任意合法T的pure行

取 $q_0=1/6$。用六个合法查询的真实均值d/6，随后按 $d\ge o$ 弱化，定义

\[
\mathcal B_i(T)=\sum_x\frac{t_x}{D_x},\quad
M_i(T)=\sum_x\frac{o_x}{6[p_x+1+n t_x]},\quad
N_{ij}(T)=\sum_x\frac{o_x}{6[p_x+(j-i)t_x+7-j]}.
\]

由真实钱包和(ZERO)、(POSITIVE-QUERY)，

\[
\boxed{R_T(\lambda,\tau)
=(\lambda+\Theta)u_i+S(K-|T|)
-(\lambda-1)\mathcal B_i(T)-M_i(T)-\sum_j\tau_jN_{ij}(T)\ge0.}
\tag{PURE}
\]

它适用于任意合法T，不使用C最大性。真实付款是P、菜单弱化差和每个真实客户尾成本减准确min的非负和。

沿归一退化方向v，记 $\theta=\sum_jv_j$，

\[
b_j=1+\frac{(j-i-1)q_0}{(7-j)(8-j)},\qquad V=\sum_jb_jv_j.
\tag{B-PRIME}
\]

纯射线为

\[
\boxed{\mathcal R_T(v)
=(1+\theta)u_i+V(K-|T|)-\mathcal B_i(T)-\sum_jv_jN_{ij}(T).}
\tag{PURE-RAY}
\]

其真实预算中末CAP/BR权退化为0，源IC权为 $1+\theta$，内部SAFE权为v，内部CAP为 $v_j+\sum_{\ell>j}q_0v_\ell/[(7-\ell)(8-\ell)]$。因此它不能仅被称作固定 $\tau$ 的SAFE斜率。后面给它完整的旧行付款。

### 4.2 外六、内五同菜单ordered

取 $q_0=1/5$。外层分别强制同一六菜单的 $Q_k$，内层只均分五个索引 $\ell\ne k$。排除的是索引，重复标签的其他索引保留。每个客户的条件查询均值准确为 $q=(d-t)/5$。所有分支均沿同一份策略的真实历史，未假设续局可独立选择。

令 $m_t(p,q)$ 为全部真实尾最小值。每个尾成本对q非减。对整个高段，

\[
W-Z\ge\frac{24}{5}+\frac m{10}+\frac9{10}\Theta>0,
\]

因为 $D\le6,\lambda\ge25$，故 $1+(\lambda-1)/D\ge5$，而 $\beta_j\ge1/10+\tau_j$ 和 $Z\le1/5+\Theta/10$。于是

\[
f(p,d)=\frac{(6-d)m_0(p,d/5)+d,m_1(p,(d-1)/5)}6
\]

满足 $f(p,0)=0$，且对每个 $d\ge2$，

\[
f(p,d)-f(p,1)\ge\frac{d-1}{6}(W-Z)>0.
\]

d=0、6只计算实际存在项，未构造不可能的查询均值。因此整个无界域上的唯一最弱正重数是d=1，得到

\[
\boxed{R_{\rm ord}(\lambda,\tau)
=(\lambda+\Theta)u_i+SK
-\sum_x\frac{o_x}{6}\left[S+\frac{\lambda-1}{D_x}+\frac1{p_x+1}
+\sum_j\frac{\tau_j}{p_x+7-j}\right]\ge0.}
\tag{ORDERED}
\]

其付款是六分支P的平均、各分支真实尾成本减min、以及 $f(p,d)-o f(p,1)$ 的非负和。准确退化行为

\[
\boxed{\mathcal R_{\rm ord}(v)
=(1+\theta)u_i+VK
-\sum_x\frac{o_x}{6}\left[V+\frac1{D_x}+\sum_j\frac{v_j}{p_x+7-j}\right].}
\tag{ORDERED-RAY}
\]

同样可以直接用末CAP/BR权0的真实射线预算重建；其 $W'-Z'\ge1/6+9\theta/10>0$。本包独立保留这些退化预算的全部弱达到尾。

### 4.3 仅使用原实际节点SAFE，不把O当作行动

[全目录真实前缀SAFE](../../../../archives/customer-attraction/state/引理/真实前缀全目录单步偏离行--引理.md)给每个合法T

\[
F_i(T)=u_i-\mathcal B_i(T)\ge0.
\]

对同一六合法查询平均并作并集投影，有

\[
\boxed{\Phi_i(O)=u_i-\sum_x\frac{o_x}{6D_x}
=\frac16\sum_{\ell=1}^6F_i(Q_\ell)
+\sum_x\frac{d_x-o_x}{6D_x}\ge0.}
\tag{ACTUAL-MENU-SAFE}
\]

右端只含真实合法标签SAFE和客户非负余项。这里没有内部收益，更没有把不同历史上的收益当作同一个 $u_i$。960个全部菜单/前缀上下文及5760个排除单索引平均另被逐项核验。

## 5. 全部射线的整域非负付款：核心身份

以下v取归一退化截面的任意点，**不要求v是顶点**。令

\[
S_0=1+\frac{mq_0}{2},\qquad
H=S_0+L_0V,\qquad
A_T=S_0-15q_0V,\qquad A_O=S_0\theta-V.
\tag{CLOSURE-WEIGHTS}
\]

在pure情形令 $E_T(v)=R_T(25,L_0v)$；ordered情形令 $E_{\rm ord}(v)=R_{\rm ord}(25,L_0v)$。两者都是既有 $\lambda=25$ 同族截面行。

### 5.1 全部付款权非负

各归一帽给 $v_j\le1/24$。把帽相加有

\[
\frac45\theta+(V-\theta)\le\frac m{30},
\qquad
V\le\frac m{30}+\frac\theta5\le\frac m{24}.
\]

所以

\[
A_T\ge1-\frac{mq_0}{8}>0,\qquad H>0.
\]

又 $1\le b_j\le S_0\le7/5$，故

\[
A_O=\sum_j(S_0-b_j)v_j\ge0.
\]

V也非负。此处所有界覆盖完整退化截面，未依赖有限射线诊断。

### 5.2 逐客户余项的准确符号

定义

\[
Q_{ij}(p)=\frac{b_j}{p+1}+\frac{S_0-b_j}{D}-\frac{S_0}{p+7-j}.
\tag{Q-BRACKET}
\]

令 $h=7-j$、$n=6-i$，则

\[
\frac{1/(p+h)-1/D}{1/(p+1)-1/D}
=\frac{(j-i)(p+1)}{n(p+h)}\le\frac12.
\tag{HALF-INTERPOLATION}
\]

最后的界准确等价于 $2(j-i)(p+1)\le(6-i)(p+7-j)$。左减右随j递增，最难是j=5；其条件化为 $(4-i)(p+1)\le6-i$，由 $p\le i-1$ 对i=1、2、3、4分别给3≤5、4≤4、3≤3、0≤2。第五源无j。又 $b_j\ge1\ge S_0/2$，故

\[
Q_{ij}(p)
=b_j\left[\frac1{p+1}-\frac1D\right]
-S_0\left[\frac1{p+7-j}-\frac1D\right]\ge0.
\]

定义客户非负付款

\[
\Omega_T(v)=\sum_x\frac{o_x(1-t_x)}6\sum_jv_jQ_{ij}(p_x),
\quad
\Omega_{\rm ord}(v)=\sum_x\frac{o_x}6\sum_jv_jQ_{ij}(p_x).
\tag{SLACK}
\]

这些是在完整客户型上的非负线性组合，K列为0。

### 5.3 Pure射线完整身份

\[
\boxed{H\mathcal R_T(v)
=V E_T(v)+A_T F_i(T)+A_O\Phi_i(O)+\Omega_T(v).}
\tag{PURE-CLOSURE}
\]

展开即得恒等式。源收益系数两边都是 $H(1+\theta)$，CAP项由 $HV=VH$ 抵消；目标安全项的系数是 $-H+24V=-A_T$。其余查询项为

\[
V M_i(T)-S_0\sum_jv_jN_{ij}(T)+A_O\sum_x\frac{o_x}{6D_x}.
\]

t=1时所有查询分母同为D，恰为0；t=0时它逐客户恰是(SLACK)。右边每个实际不等式的乘子非负，所有剩余客户系数也非负。

### 5.4 Ordered射线需要自己的身份

\[
\boxed{H\mathcal R_{\rm ord}(v)
=V E_{\rm ord}(v)+(A_T+A_O)\Phi_i(O)+\Omega_{\rm ord}(v).}
\tag{ORDERED-CLOSURE}
\]

这是按ordered准确系数重新展开的身份，不是用pure射线替代ordered。K列由 $HV=VH$ 准确相同；查询中的常数帽项亦相同，D项和其余查询项得到所示SAFE平均及客户余项。

当v=0时V、$\theta$、$A_O$、$\Omega$均为0，身份分别退化为 $\mathcal R_T=F_i(T)$ 和 $\mathcal R_{\rm ord}=\Phi_i(O)$。第五源全域正是这两个退化情形。

## 6. 任意高段参数的直接闭合，而非只核极端射线

给定任意(H-DOMAIN)中的参数，用(RADIAL)定义 $\delta,v$。所有行在高段的参数上仿射，准确有

\[
R_T(\lambda,\tau)=E_T(v)+\delta\mathcal R_T(v),
\quad
R_{\rm ord}(\lambda,\tau)=E_{\rm ord}(v)+\delta\mathcal R_{\rm ord}(v).
\]

因此

\[
\boxed{R_T(\lambda,\tau)
=\left(1+\frac{\delta V}{H}\right)E_T(v)
+\frac{\delta A_T}{H}F_i(T)
+\frac{\delta A_O}{H}\Phi_i(O)
+\frac\delta H\Omega_T(v),}
\tag{WHOLE-PURE}
\]

\[
\boxed{R_{\rm ord}(\lambda,\tau)
=\left(1+\frac{\delta V}{H}\right)E_{\rm ord}(v)
+\frac{\delta(A_T+A_O)}H\Phi_i(O)
+\frac\delta H\Omega_{\rm ord}(v).}
\tag{WHOLE-ORDERED}
\]

全部乘子非负；E(v)由第3节的 $\lambda=25$ 全部端点行作同目标凸组合。再把 $\Phi_i(O)$ 按(ACTUAL-MENU-SAFE)展开，就完全得到既有端点行、真实合法T的actual SAFE以及客户非负质量的非负组合。适用于任意实数 $\lambda\ge25$，不留“ sufficiently large ”或未检验的方向。

## 7. C-only必须保真正最大性和自由等式

仅当C为真正最大裸大小标签时，令 $E_C^{size}=|C|-K=0$。高段通用C行可写为

\[
R_C^{only}(\lambda,\tau)=R_C(\lambda,\tau)+(S-1)E_C^{size}.
\tag{C-EQUALITY}
\]

其独立K列是1。射线和端点分别满足

\[
\mathcal R_C^{only}=\mathcal R_C+V E_C^{size},\qquad
E_C^{only}(v)=E_C(v)+(H-1)E_C^{size}.
\]

所以全513列的准确闭合是

\[
\boxed{H\mathcal R_C^{only}(v)
=V E_C^{only}(v)+A_TF_i(C)+A_O\Phi_i(O)
+\Omega_C(v)+V E_C^{size}.}
\tag{C-RAY-CLOSURE}
\]

最后一项为自由等式，不可删去独立K列后假装它不存在。整个高参数行还有同样的系数 $\delta V/H$ 乘该自由等式。也可直接使用(WHOLE-PURE)中的通用C端点，再加(C-EQUALITY)。这些公式不能给任意T直接套用；没有要求自由等式乘子非负才能合法。

## 8. 全513列恒等式、旧行对应与独立核验

列0…511为完整词典序九位 $(a_1,\ldots,a_6,x,o,c)$，列512为独立K。原实际收益的客户系数是 $a_i/\sum_{h=1}^6a_h$，零负载取0。保所有零型、o=0型、重复列与弱平局，不按某个候选支持缩减。

核心(PURE-CLOSURE)、(ORDERED-CLOSURE)、(C-RAY-CLOSURE)乘H后是方向v上的至多二次多项式恒等式。生成器和独立检查器用不同数据结构，均在每个完整列核常数、每个一次项及每个二次交叉项；**不是在62条射线上取值相等就外推整域**。

独立程序不导入生成器或其他项目代码；它从各个人份额、大小帽和每个真实查询前缀重建成本，并从活跃边界求交重建几何。对旧端点，另从全部真实尾枚举准确min，再重建旧raw列；未直接相信闭式锚。两个基准的旧 $\lambda=25$ 端点与已冻结 `all_source_minimal_cap_safe`、`ordered_minimal_cap` 的279行逐143127列相同。

| 承重检查 | 准确数量 |
|---|---:|
| 高段完整域 / 真面 | 10 / 50 |
| 全部基顶点 / 极端射线 | 62 / 62 |
| 所有t=1零查询状态证书 | 228 |
| 所有t=0仿射余项 | 456 |
| 全部t=1查询斜率差 | 228 |
| 整域符号行族（40 pure、5 C-only、5 ordered） | 50 |
| 完整符号列身份 | 25650 |
| 逐多项式标量系数身份 | 179550 |
| 既有端点行 / 独立旧列核验 | 279 / 143127 |
| 高段活跃边界组合 / 归一射线边界组合 | 350 / 198 |
| 全部物理条件min表 / 真实隐藏尾成本 | 2964 / 47112 |
| 全弱达到态出现 / ordered重数值 | 7298 / 798 |
| 实际六菜单SAFE投影上下文 | 960 |
| 内五排同索引平均身份 | 5760 |

进一步的独立边界组合数、真实min表数、隐藏尾成本和全部弱达到态数见[literal_checker_output.json](literal_checker_output.json)。这些有限表用于核验实现和保留退化弱态，连续域证明由第2、3、5、6节承担。

## 9. 工件、复现、冻结与停止边界

复现入口仅使用Python标准库和Fraction；冻结后应在重放副本运行：

```bash
python research/workspaces/six-boss1-20261111/high_lambda_closure/derive_high_lambda.py
python research/workspaces/six-boss1-20261111/high_lambda_closure/check_literal.py
```

- [inputs.json](inputs.json)：模型、域、列合同和禁止读取范围。
- [source_pins.json](source_pins.json)：直接数学来源及旧端点文件的固定SHA256，首末核对。
- [parameter_domains.json](parameter_domains.json)、[endpoint_table.md](endpoint_table.md)：全部面、基顶点、退化射线。
- [all_state_certificates.json](all_state_certificates.json)：全部真实状态的整域非负身份。
- [symbolic_column_checks.json](symbolic_column_checks.json)、[literal_symbolic_column_checks.json](literal_symbolic_column_checks.json)：两份独立全列全多项式系数身份。
- [endpoint_correspondence.json](endpoint_correspondence.json)：279条旧端点行的准确来源，未复制巨型raw矩阵。
- [literal_minimum_tables.json](literal_minimum_tables.json)：基顶点及退化预算的全部物理条件min和全部弱达到尾。
- [literal_geometry_checks.json](literal_geometry_checks.json)、[literal_checker_output.json](literal_checker_output.json)：独立几何和字面预算结果。
- `freeze_manifest.json`、`SHA256SUMS`：最终包身份。

零客户、空覆盖、K=0、O=0、目录标签重复及全部弱平局均由同一齐次预算覆盖。此结论只关闭指定最小帽双锚族的 $\lambda\ge25$ 延拓，不证明任意钱包最优、不提供完整SPE反例、不改变六人half开放状态。所有文件冻结并向Main报告后停止写入。
