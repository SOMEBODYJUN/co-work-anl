# 加权原子拥塞：Pro 接题材料与精确方法障碍

本稿是现行数学资产的派生读取稿，不另立真值账本。默认只读本稿与任务正文即可接题；原证明、审查、程序和证书按来源编号定点查阅。本稿没有预设开放路线，也没有新增数学 Claim。

**数学源快照：** `SOMEBODYJUN/co-work-anl` 的 `c623edd5f717e5f58151e6ab3363499c7ea2b114`。下文所有 S 编号均指该提交的原文件和所列具体节，末表连接实际审查。内部已审不等于外部同行评审；未认证全球新颖性。当前唯一全类问题仍 **OPEN**。原历史身份 `WC-TARGET v1` 的宽目标不改写，本次完成条件固定如下。

## 1. 完整模型、符号与唯一问题

令整数 $d\ge0$，$\mathcal G_d$ 表示以下全部有限博弈的类。

- $N,E$ 是非空有限玩家集与资源集。每名玩家有任意正实权 $w_i>0$，权重不依资源变化。
- $\mathcal S_i\subseteq2^E$ 是非空有限策略族；允许空策略、不同玩家有不同策略族、多资源策略。不能把一般策略族换成单资源选择、网络路径或所有子集。
- 每资源费用 $c_e(x)=\sum_{k=0}^d a_{e,k}x^k$，$a_{e,k}\ge0$ 为任意实数；允许常数和恒零费用。
- 状态 $s\in\Omega:=\prod_i\mathcal S_i$，用户集 $U_e(s)=\{i:e\in s_i\}$，负载 $x_e(s)=\sum_{i\in U_e(s)}w_i$，成本

$$
C_i(s)=\sum_{e\in s_i}c_e(x_e(s)).
$$

成本**不再乘 $w_i$**；逐玩家整体乘其固定正权不改变近似均衡集合。合法单方偏离 $s'=(t_i,s_{-i})$ 后，所有成本均以 $s'$ 的真实负载重新计算，包含偏离者自身。资源在两策略中保留时，其用户集和负载不变。

实数 $\alpha\ge1$ 的 $\alpha$-近似纯 Nash 均衡（$\alpha$-PNE）指

$$
\forall i\in N\ \forall t_i\in\mathcal S_i:\quad C_i(s)\le\alpha C_i(t_i,s_{-i}).
$$

零成本直接用此式：旧正、新零违反每个有限倍率；旧新均零满足。绝不计算 $0/0$。严格改善边指 $C_i(s)>\alpha C_i(s')$；有限改善性质（FIP）指其有向图无环，等价于每条严格改善序列终止。

**唯一待判命题：** 是否存在绝对实数 $C\ge1$ 和整数 $d_0\ge2$，使

$$
\forall d\in\mathbb Z_{\ge d_0}\ \forall G\in\mathcal G_d\ \exists s\in\Omega:
\quad s\text{ 是 }(Cd/\ln d)\text{-PNE}?
$$

$\ln$ 为自然对数。肯定证明须给可核验的 $C,d_0$，覆盖上述全模型，常数不依人数、资源数、策略数、权比、系数或其他实例参数；只要求存在性。

**严格否定的完整量词：**

$$
\forall C\ge1\ \forall d_0\in\mathbb Z_{\ge2}\ \exists d\in\mathbb Z_{\ge d_0}
\ \exists G\in\mathcal G_d\ \forall s\in\Omega\ \exists i\in N\ \exists t_i\in\mathcal S_i:
\quad C_i(s)>\frac{Cd}{\ln d}C_i(t_i,s_{-i}).
$$

这里的 $i$ 必须是玩家，$t_i$ 是其合法策略。构造一个改善环、固定次数的较好下界或只限制一种证明工具，均没有完成这些量词。

全类阈值沿用

$$
a_*(d)=\inf\{\alpha\ge1:\forall G\in\mathcal G_d,\ G\text{ 有 }\alpha\text{-PNE}\}.
$$

`WC-UNIVERSAL-THRESHOLD-ENDPOINT-v1` 已另证可行倍率集为 $[a_*(d),\infty)$，即每个游戏在全类端点分别有均衡；不意味着某一个有限游戏取得全类最坏值（[S12]）。**本题的充分强否定证书**可以是次数 $q_j\to\infty$ 的全状态无 $\alpha_j$-PNE 族，且 $\alpha_j\ln q_j/q_j\to\infty$。原输入次数与输出实际次数不得混同。来源：[S0]、[S12]。

## 2. 可直接使用的已知边界

### 2.1 全类上下界：对数缺口是真实缺口

**文献导入的模型桥：** 原文正式模型先写正系数、正次单项式并用正成本。非负多项式先按正系数项拆成同关联资源；每个常数项 $a_{e,0}>0$ 可对每个潜在用户 $i$ 用独享资源 $c_{e,i}(x)=a_{e,0}x/w_i$ 精确保成本。删去零费资源后，给每个原动作标签加一条仅该玩家该动作使用、成本恰为 $\varepsilon>0$ 的一次资源，区分标签并使空策略也成为正成本策略。对每个 $\varepsilon$ 调用下述文献定理；有限原状态中取 $\varepsilon\downarrow0$ 的恒定状态子列，$C_i(s)+\varepsilon\le d[C_i(s')+\varepsilon]$ 的极限给全模型弱不等式。这只补齐导入条件，不冒称完整重证原定理。

**Paper Fact — `WC-LIT-UPPER-D v1`：** 每个 $d\ge1$、每个 $G\in\mathcal G_d$ 有 $d$-PNE；不承诺多项式时间，不宣称最强 finite-$d$ 界。来源为 Caragiannis–Fanelli, arXiv:1902.07173v5, Theorem 2（亦由摘要取 $\delta=0$ 可核陈述）；项目未独立重建全文；全模型退化输入的适用性由上述短归约补齐。[S1]。

**团队一般定理 — `WC-R3-ODD-RING-LOWER-v1`：** 对每个整数 $d\ge2$、每个实数 $1\le\alpha<T_d$，存在正有理权、正有理系数、所有资源费用均为正系数 $x^d$ 的有限博弈，没有 $\alpha$-PNE，其中

$$
f_d(R)=\frac{R(1+R)^d+1}{(1+R)^d+R^{d+1}},\qquad
T_d=\max_{R>1}f_d(R)\sim\frac d{\ln d}.
$$

每个倍率可选择不同的有限实例；不声称一个实例同时达到上确界端点。配套 `WC-R3-ODD-RING-ENVELOPE-v1` 给

$$
H_d=\frac d{(d+1)d^{1/(d+1)}-d},\qquad
H_d<T_d\le H_d+\frac1{2^d+1}.
$$

故 $T_d\le a_*(d)\le d$。一般全状态证明、同次数有理构造及内部独立审查齐备；未经外审。线性重置实现与此同次数实现属于同一奇环机制，不能计成互不相关的两项突破。[S2]。

**保留原因：** 删掉本节会把已经达到 $d/\ln d$ 的增长下界误作无成果，或重复仅达到该量级的下界而声称否定本题。

### 2.2 有界用户支持与固定人数

`WC-R1-RESOURCE-SUPPORT v1`：若每资源的潜在用户集
$P_e:=\{i:\exists a\in\mathcal S_i,e\in a\}$ 至多有 $r\ge1$ 人，则任意非负非减费用下都有 $r$-PNE。取无权总成本 $\Phi=\sum_i C_i$，约定 $\Delta\Phi=\Phi(s')-\Phi(s)$、$C_{\rm keep}=\sum_{e\in s_i\cap t_i}c_e(x_e(s))$（保留资源费用）；后文沿用。一次偏离删去/加入/保留资源分别贡献

$$
\Delta\Phi\le rC_i(s')-C_i(s)-(r-1)C_{\rm keep}
\le rC_i(s')-C_i(s).
$$

删除者原费用被消去且其他人费用不增；新资源加入后至多 $r$ 个用户，各付同一资源费用；保留资源完全相消。有限最小点即所需均衡。所有潜在用户集皆空时任意状态精确。此为完整直接证明与精确核验；源页未记录独立冻结审查，不用泛称“全部内部独立审过”。[S3]。

取 $r\le|N|$ 即得固定人数上界。无论堆叠多少小构件，只要每资源潜在用户支持仍统一有界，就不能给随次数无界的非存在因子。此结论不限制用户支持和人数均增长的构造。

### 2.3 少量可动权类与共占高度已经有统一结构界

令整数 $d\ge2,k\ge1$，$A_{d,k}\in[1,d)$ 是唯一正根

$$
A=\sum_{j=0}^{k-1}\left(\frac{d-1}{A}\right)^j.
$$

`WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1`：全局权值至多 $k$ 种时有 $A_{d,k}$-PNE，并有对每条严格该倍率改善下降的资源可加势。`WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1` 只要求**可动玩家**（策略族不止一个元素）的权值至多 $k$ 种；固定玩家按 $c_e(B_e+x)$ 非负系数展开精确吸收。不动者任意多种权值不增加 $k$。

更强的 `WC-WEIGHT-INTERACTION-HEIGHT-POTENTIAL-v1`：先吸收固定玩家，在可动玩家上置弧 $i\to j$，当且仅当 $w_i>w_j$ 且两人是某资源的潜在用户；令 $k$ 为该降权 DAG 的最长路径顶点数，孤点计一。仍有 $A_{d,k}$-PNE/FIP；全局不同权值数可以无界。这里用**同一个跨资源图的高度**，不能换成各资源分别的权种数或某个状态的高度。

可用简式为

$$
A_{d,k}\le\frac{d-1}{d^{1/k}-1},\quad
A_{d,1}=1,\quad A_{d,2}=\frac{1+\sqrt{4d-3}}2.
$$

固定 $k$ 时 $A_{d,k}\sim d^{1-1/k}$；$d\ge16, k\le\ln d/\ln\ln d$ 时 $A_{d,k}\le2d/\ln d$。固定 $d$、$k\to\infty$ 时则 $A_{d,k}\uparrow d$，没有全类高度控制。

`WC-WEIGHT-CLASS-CLUSTER-ROUNDING-v1`：给定实数 $R\ge1$ 和正代表权 $v_1,\ldots,v_k>0$，若每可动者可赋固定标签，使 $v_{\tau(i)}\le w_i\le Rv_{\tau(i)}$，共有至多 $k$ 个代表权，则有 $R^dA_{d,k}$-PNE。其理由是所有相同状态和真实偏离下 $x'\le x\le Rx'$，从而 $C_i'\le C_i\le R^dC_i'$。这是单向均衡提升，未证任意权谱可用少量窄簇覆盖。

全部上述新 ID 有完整一般证明和内部独立攻击；高度扩展的审查者已知旧三角势，独立重构的是新高度接口，不夸称独立发现旧机制。[S4]。

**关键边际，供直接复用：** 一致层秩满足 $1\le r_i\le k$，同资源潜在可动用户若 $w_i>w_j$ 则 $r_i<r_j$；取上述DAG的终点最长路秩即可，同层共用户必等权。取 $A=A_{d,k}$、$t=(d-1)/A$、$\lambda_b=t^{b-1}/A$、$S_r=\sum_{b\le r}\lambda_b$。对一致层秩 $r_i$，对当前用户集 $U$ 按层序 $(k,k-1,\ldots,b+1,1,\ldots,b)$ 排列，同层用固定身份次序；定义 $P_{b,e}(U)=\sum_{j\text{ 按该序}}w_j c_e(\sum_{\ell\text{ 不晚于 }j}w_\ell)$、$F_e(U)=\sum_b\lambda_bP_{b,e}(U)$，插入玩家 $i$ 的资源势边际满足

$$
h_i c_e(Y)\le\Delta_iF_e\le A h_i c_e(Y),\qquad h_i=w_iS_{r_i}>0.
$$

$Y$ 是加入后的真实总负载；$h_i$ 跨全部资源一致。相同推导给任意严格改善闭词的**端点实际共占图**高度 $k$ 必须满足 $\alpha<A_{d,k}$（`WC-REALIZED-INTERACTION-CHAIN-CYCLE-v1`）。各弧可在不同端点出现；长链不是无均衡充分条件。逐步重排层秩会改变势，尚缺同一势的累计控制，此义务 **OPEN**。

**保留原因：** 两权任意人数与权比、有限可动权类和小交互高度都已有结论；不能继续把它们当全类尚未闭合的特殊情形，也不能把它们扩写成全类界。

### 2.4 仅升高固定权谱的全部正次数不会放大反例

`WC-HIGH-DEGREE-SHARE-v1`。对有潜在用户且有正次收费项的资源，令

$$
q_e=\frac{\min_{i\in P_e}w_i}{\sum_{j\in P_e}w_j},\quad
k_e=\min\{j\ge1:a_{e,j}>0\},\quad
\lambda_e=1-(1-q_e)^{k_e}.
$$

其余资源取 $\lambda_e=1$。令 $\lambda=\min_e\lambda_e$，则

$$
\Phi(s)=\sum_e\left[a_{e,0}|U_e(s)|+\sum_{j\ge1}a_{e,j}x_e(s)^j\right],
\qquad
\Delta\Phi\le C_i(s')-\lambda C_i(s)-(1-\lambda)C_{\rm keep}.
$$

所以任一单方局部最小点是 $\lambda^{-1}$-PNE。删除资源时
$x^j-(x-w_i)^j\ge\lambda_e x^j$；加入资源增量至多新费用，常数项必须用**人数**计数。

若有限正权向量固定，则 $q_e\ge q_*:=\min_iw_i/\sum_iw_i>0$。全部正次项的最低次数 $k\to\infty$ 时，保证统一不超过 $[1-(1-q_*)^k]^{-1}\to1$，即使拓扑和系数变化。固定人数但权随次数变化、只升最高次而保留低次项，都不在此限制内。纯 $d$ 次加常数的游戏若无 $\alpha>1$-PNE，必有正次收费资源的潜在用户份额严格小于 $1-(1-1/\alpha)^{1/d}$；这是必要条件，不是坏状态或偏离者的证书。完整证明、独立冻结攻击；有限独立审计原先只覆盖共同 $q/k$ 简式，逐资源扩展由审查中的一般推导覆盖。[S5]。

## 3. 已证方法障碍：全边下降、概率限制与选态

### 3.1 近 $d$ 的真实改善环排除任意全边下降势

`WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1`。对每个 $d\ge2$、每个 $1\le\alpha<\rho_d$，其中

$$
\rho_d=\sup_{t>0}\frac{(d+1)(1+t)^d+t^{d+1}}{d+(1+t)^{d+1}},\qquad \rho_d/d\longrightarrow1,
$$

存在正有理权、每资源费用恰为 $x^d$、人人策略族为 $2^E$ 的有限游戏，真实偏离图有严格 $\alpha$ 改善环，**同时全空是精确 PNE**。完整一般证明与独立攻击已经闭合非负对偶零坐标、逐玩家循环实现、两轮返回及有理化；不再只是局部配置循环候选。[S6]。

**阻止的论证：** 对所有实例、所有严格 $\alpha$ 改善边，某实值全局函数严格下降，或任意改善序列终止。因为沿真实闭环会有
$\Phi(s_0)>\cdots>\Phi(s_L)=\Phi(s_0)$。此处包括非资源可分势，故旧仅资源可分全边下降障碍不再单列。

**不排除：** 均衡存在、选择部分改善边、只要求某些局部/全局最小点为均衡的目标。任意固定 $C$ 下最终 $Cd/\ln d<\rho_d$，所以本题不能靠一个对全类全部该倍率改善边下降的势来证明。此结论仍不是本题的否定。

### 3.2 dual 不能无证增加平稳、回返或固定人数限制

本节矩阵与 selector 的完整定义在附录 A；selector 是给**每个**状态指定一项合法偏离的函数，不要求它对某个既定游戏处处改善。所有下列方法结论均有一般证明、内部独立重构/攻击，未外审。[S7]、[S13]。

**单位速度平稳。** `WC-SELECTOR-UNIT-SPEED-STATIONARY-BARRIER-v1` 排除把 dual $\lambda$ 额外限制为确定性 selector 链的单位速度平稳概率。取 $K$ 名权 $K^{-2}$ 的 light 和一名权1者；唯一环依次让 lights 入1、重者入1、lights 出1、重者出1，环外按1位数下降路由至该环。唯一平稳概率是环上均匀分布；全员仅动作1使用的仿射资源列给

$$
(B_h(\alpha)^\top\lambda^{\rm st})_{\sigma,1}
=\frac{2K+1-3\alpha}{4K}>0\quad\text{若 }K>(3\alpha-1)/2.
$$

因此对任意固定有限倍率都失败，尽管同一仿射模板有精确均衡。`WC-AFFINE-SELECTOR-CYCLE-DUAL-v1` 给仿射环可取 $\lambda_s\propto w_{i(s)}$ 得到非平稳 dual；这只保证次数0、1列。允许自选状态相关持留率不在单位速度障碍内。

**仅回返状态。** `WC-RECURRENT-SUPPORT-FIP-EQUIVALENCE-v1`：固定模板、权、次数、倍率及任意非空列子锥 $J$，

$$
[\forall a\ge0:\text{严格 }\alpha\text{ 改善图无环}]
\iff[\forall h\ \exists\text{ dual 支持于 }\operatorname{Rec}(h)].
$$

左到右对所选环行子矩阵使用线性替代；反向把一个坏改善环外的状态按 Hamming 距离路由至它，令它成为唯一回返环，严格正环 margin 排除任何环上概率 dual。结合3.1，这个附加限制已比本题需要的存在性强。一般 dual 可给暂态质量，不需要平稳性；不能从“有改善环”推出“一般 dual 不存在”。

**固定移动者或状态数截断。** `WC-SELECTOR-UNBOUNDED-MOVER-SUPPORT-v1`：任意奇数 $n\ge3$、等权二动作、$d\ge1$，每状态任选一个满足 $s_i=s_{i+1}$ 的 $i$ 翻位（下标模 $n$）。对每个这种 selector，complete/proper 两锥都存在 dual；但 $1\le\alpha<2^d$ 时，任一 dual 必须给每名移动者的两个方向正质量，最小状态支持恰 $2n$。

简证：设 $\mu_i$ 为选择 $i$ 的总质量，邻边同动作0/同动作1两条 $x^d$ 列给

$$
(2^d-\alpha)\mu_i\le(\alpha2^d-1)\mu_{i+1}.
$$

左系数正，闭环与总质量1迫所有 $\mu_i>0$。私人成本常数列再给
$\mu_{i,0}\le\alpha\mu_{i,1}$ 及反向式，故两个方向均正。恰一个相等邻边的 $2n$ 状态成环，其均匀概率由等权离散资源势望远镜给 dual，达到下界。此例**本来可行**，失败只是固定人数截断；依模板维数的支持界不受排除。这里未把只对特定最小下标 selector 成立的 $\alpha\ge2^d$ 二点端点结论推广到所有 selector。

**保留原因：** 删除本节会把线性替代中允许的任意概率，误换成过强的动力学条件或统一小局部补偿。

### 3.3 共同非负幂混合的全部最小点确实会失败

`WC-COMMON-POWER-MIXTURE-MINIMIZER-OBSTRUCTION-v1`：每个 $d\ge32$ 有同一个四玩家四资源纯 $d$ 次游戏，对每个定义在 $(0,\infty)$ 上的非零非负 Borel 测度 $\mu$（所有状态目标有限），

$$
P_\mu(s)=\sum_e a_e\int_{p>0}x_e(s)^p\,d\mu(p)
$$

的每个全局最小点都不是 $\alpha$-PNE，对全部 $1\le\alpha<d/16$ 成立；但该游戏有精确 PNE。保留原费用系数 $a_e$、所有资源共用同一 $\mu\ge0$、$0^p=0$ 是承重条件，$\mu$ 可依完整游戏。[S8]。

关键机制是在一个游戏中有两个相互独立的可动者，坏选项真实成本均为 $R=d/16$，好选项为1；另两人固定背景。令 $A=d^2+1,K=d(d+1),W=K^{4d},r=p-d$，坏相对好选项的幂目标差为

$$
D_H=W^r[R-A^r(1-(1-1/A)^p)],\quad
D_L=RW^r[1-(1-1/W)^p]-1.
$$

同一个正有理数 $\kappa=4/[dK^{4d-2}]$ 对**所有实数 $p>0$**满足
$\kappa D_H+D_L\le-11/16$。按 $r\le1-1/(2d)$、中间段及大 $r$ 分段的完整证明在源§3。积分得至少一个坏选项在每个最小点强制出现；不是把“每个单幂各有坏例”交换成“同一实例击败全部混合”。

**准确否定范围：** 此原系数共同非负幂混合选态族。资源分别归一化、先消去固定背景再按展开费用重选规则、任意集合函数或非可分目标，均未排除。

相反，`WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1` 说明任意给定合法状态 $s^*$ 可由
$F_e(U)=|U\triangle U_e(s^*)|$ 唯一选出：$\sum_eF_e(U_e(s))=\sum_i|s_i\triangle s_i^*|$。因此“存在任意依完整游戏选择的可分目标，其全部最小点为均衡”与均衡存在本身等价，不是3.1或本节的普遍不可能结论；也不给找 $s^*$ 的方法。[S9]。

## 4. 已证结构限制：强迫反馈与多项式替换

### 4.1 奇环正测试的精确 ceiling，不是整个拓扑的存在界

`WC-R3-ODD-RING-CERTIFICATE-v1` 与 `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1`。奇数 $m\ge3$，hub $H_i$ 权 $u_i>0$，cohort $i$ 有整数 $n_i\ge1$ 名共同权 $v_i>0$ light，下标模 $m$。主资源两副本 $A_i^b$ 同费 $a_iF_i$，侧资源 $B_{ij}^b$（$j=1,\ldots,n_i,\ b\in\{0,1\}$）同费 $b_iG_i$，$a_i,b_i>0$，$F_i,G_i$ 为非零非负系数次数至多 $d$ 多项式。hub 位 $h$ 用 $A_i^h$ 及所有 incoming $B_{i-1,j}^h$；light 位 $l$ 用 $A_i^l,B_{ij}^{1-l}$。

对 $\alpha>1$，令

$$
\begin{aligned}
N_i&=F_i(u_i+v_i)-\alpha F_i(n_iv_i),&
M_i&=\alpha F_i(u_i+n_iv_i)-F_i(u_i),\\
P_i&=\alpha G_i(u_{i+1}+v_i)-G_i(v_i),&
Q_i&=G_i(u_{i+1}+v_i)-\alpha G_i(u_{i+1}).
\end{aligned}
$$

称 light 位等于自身 hub 位为 aligned，不等为 anti。所限制的证书要求**每名 aligned light 在所有配置中都严格改善**，再用奇性覆盖全 anti 状态的 hub；其正系数可行性恰为

$$
N_i,Q_i>0\ (\forall i),\qquad
\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1.
$$

在允许自由选择上述奇环参数和 shapes 的整个证书族内，**存在**通过这些正测试的参数，当且仅当 $\alpha<T_d$；固定参数须用前面的正性/乘积判据，不保证每组固定参数在阈值以下都通过。关键必要性：$x_i=v_i/u_i,t_i=v_i/u_{i+1}$ 必有 $\prod x_i=\prod t_i$。每个单项式的归一化因子

$$
\mathcal F_{k,n}(x)=nx\frac{(1+x)^k-\alpha(nx)^k}{\alpha(1+nx)^k-1}
\le\mathcal F_{k,1}(nx)
$$

在 $\alpha\ge T_d$ 均不超过1；$k=0$ 时为 $-nx$。混合多项式时 $xnN/M$、$Q/(tP)$ 分别是这些因子的正分母加权凸组合；总 $N,Q>0$ 使两总因子为正。沿环相乘并用权闭合，乘积至多1，矛盾。[S2]§§3–5、8及其独立包络审查。

**否定的是** 任意环长、cohort 数、正权和上述 group shapes 内的这套同时强迫正测试越过 $T_d$。允许多项式混合也不救此证书。**没有证明** 一般 cohort 的实际游戏都存在 $T_d$-PNE；测试失败时，反位 light 仍可能通过重新对齐改善。整个拓扑的存在问题不能由正测试不可行推出，当前此义务 **OPEN**。

### 4.2 跨源共享 side 的实际存在界及其承重条件

**共同拓扑。** $d\ge2$，hub集 $V\ne\varnothing$，每light $l$ 权 $w_l>0$，有唯一 main source $o(l)\in V$。主副本 $A_v^0,A_v^1$ 同费 $F_v$；每side $j$ 有同费 $G_j$ 两副本、hub子集 $H_j$、light子集 $L_j$，允许跨source多light、多hub及空集。所有副本资源互异，费用均非负系数次数至多 $d$。对 $b\in\{0,1\}$，hub位 $b$ 用 $\{A_v^b\}\cup\{B_j^b:v\in H_j\}$；light位 $b$ 用 $\{A_{o(l)}^b\}\cup\{B_j^{1-b}:l\in L_j\}$。定义 $W_v=\sum_{o(l)=v}w_l,T_j=\sum_{l\in L_j}w_l$。全anti指light位为 $1-h_{o(l)}$。

**同权hub，保留最强已审版本：WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v3。** 所有hub权为 $u>0$，$m_j=|H_j|$。给任意实数 $\tau\ge1,\alpha\ge1$，若

$$
\alpha\tau\ge d,\qquad
F_v(u+w_l)+\sum_{j:l\in L_j}G_j(w_l)
\ge\tau\left[F_v(W_v)+\sum_{j:l\in L_j}G_j(T_j+m_ju)\right],
\quad v=o(l),
\tag{UFtau}
$$

则有全anti的 $\alpha$-PNE；$\tau,\alpha$ 不需大小排序。特别 $\tau\ge d$ 可取 $\alpha=1$；$d\ge16,\tau=\ln d$ 可取 $\alpha=d/\ln d$，都是明确强迫子类，非全类结论。旧v1/v2原身份和冻结证据保留；本稿只调用已扩大的v3充分域，不宣称 $\alpha>1$ 的乘积条件必要或最优。

关键支付机制是固定light时的真实Rosenthal边际，以及仅用于比较势的source light重置。令 $\kappa_d(t)=\min\{dt,t+1\}$。对非负系数次数至多 $d$ 的 $G$、$u,w>0,S\ge0,T\ge S+w$、整数 $0\le n\le m$ 及 $Y=T+mu$，新重置增量界为

$$
\sum_{r=1}^n[G(S+w+ru)-G(S+ru)]
\le\kappa_d(w/u)[G(Y)-G(w)].
$$

短证：$n=0$ 直接成立；否则 $Y-w\ge nu>0$。逐项导数界 $G'(x)\le d[G(Y)-G(w)]/(Y-w)$ 对 $0\le x\le Y$ 成立，积分得 $d(w/u)$ 倍界。另一界令 $c(x)$ 为这 $n$ 个长 $w$ 区间的覆盖密度、$a=w/u+1$。几乎处处 $0\le c\le a$，$\int c=nw\le a(Y-w)$。因 $G'$ 非减，以 $G'(w)$ 分割低高段，得 $\int cG'\le a\int_w^YG'$，即 $(w/u+1)$ 倍界。原积分区间可以穿过 $w$，不能误用区间包含代替这步凸性容量论证；常数与零费用亦成立。

对每source写 $W=\sum_lw_l$，已证源增量界为

$$
\sum_l\kappa_d(w_l/u)[F(u+w_l)-\tau F(W)]
\le d[F(u+W)-F(u)]\qquad(\tau\ge1).
$$

空列两边零，非负系数逐项证明在[S10]§9.9。令 $Y_j=T_j+m_ju$，$\tau G_j(Y_j)-G_j(w_l)\ge\tau[G_j(Y_j)-G_j(w_l)]\ge0$。将强迫式中每light的全部side先合计，再共用一次源预算，故重置增量
$R_v\le d\Delta_v/\tau\le\alpha\Delta_v\le\alpha F_v(u+W_v)-F_v(u)$，
其中 $\Delta_v=F_v(u+W_v)-F_v(u)\ge0$。这里只除以 $\tau>0$，同时覆盖 $\tau=1$ 与 $\alpha=1$。

可实际选态的有限势为
$E(h)=\sum_{j,b}\sum_{r=1}^{n_{jb}(h)}G_j(x_{jb}(h)+ru)$，
$n_{jb}=|\{v\in H_j:h_v=b\}|$，
$x_{jb}=\sum_{l\in L_j:h_{o(l)}=b}w_l$。
其任一单hub翻位局部最小点配全anti给所需均衡。真实hub偏离时light保持原动作，重置不是联合偏离。light由强迫式满足更强的 $\tau C_{\rm current}\le C_{\rm deviation}$。[S10]§§8.1–8.3、9.9、9.14–9.18。实际审查是旧v2证明者先仅据新引理与精确陈述重构，再攻击原审查者提出的v3冻结稿，并非同一作者自审；双方已有旧机制知识，未外审。

**严格反例：WC-SHARED-SIDE-EXACT-FORCING-THRESHOLD-v1。** 同一结构类保证**精确**PNE的统一强迫阈值恰为 $\tau=d$：上半由v3取 $\alpha=1$；对每个实数 $1\le\tau<d$，下面两玩家、四资源游戏严格满足(UFtau)，却四态均有严格改善。

令 $\varepsilon=d-\tau>0$，$K_0=\tau(2^d-1)+d(\tau-1)$，
$t=\varepsilon/(2K_0)$，$D=1-(\tau-1)t$，
$A=[\tau(1+t)^d-t^d]/D$，$a=(A+d)/2$。
hub权1、light权 $t$，只有该hub作为source，$F(x)=ax,G(x)=x^d$，策略用共同拓扑中的一主一side。$0<t<1/2,D>1/2$，且

$$
\tau(1+t)^d-t^d-dD\le-\varepsilon+K_0t=-\varepsilon/2<0
\quad\Longrightarrow\quad0<A<a<d.
$$

强迫差为 $a(1+t)+t^d-\tau[at+(1+t)^d]=(a-A)D>0$。两个aligned态由light翻位严格改善；两个anti态由hub翻位，成本减少 $(1+t)^d-1-at\ge(d-a)t>0$，覆盖全部四态。[S10]§9.17及新增冻结攻击。

这严格反驳“(UFtau)在任意 $\tau\ge1$ 均保证精确PNE”，防止把强迫本身当通用精确均衡工具。**仅否定 $\alpha=1$**；改善幅度可以趋近1，不能升级为固定 $\alpha>1$ 的反例，更没有否定全类目标。它也没有证明v3在 $\alpha>1$ 的充分乘积界是必要界。

**局部异权hub：WC-HETEROGENEOUS-HUB-SORTED-SIDE-v1。** 同一拓扑，改hub权为任意 $a_v>0$，令 $U_j=\sum_{v\in H_j}a_v$。仅对 $H_j\ne\varnothing$ 定义 $A_j=\min_{v\in H_j}a_v$，并令

$$
R=\max\bigl(\{1\}\cup\{a_v/A_j:H_j\ne\varnothing,\ v\in H_j\}\bigr),\qquad
K=\max\bigl(\{1\}\cup\{a_{o(l)}/A_j:H_j\ne\varnothing,\ l\in L_j\}\bigr).
$$

若实数 $\alpha$ 满足 $\alpha\ge R,\ (\alpha-1)^2\ge Kd$，且每light满足

$$
F_v(a_v+w_l)+\sum_{j:l\in L_j}G_j(w_l)
\ge\alpha\left[F_v(W_v)+\sum_{j:l\in L_j}G_j(T_j+U_j)\right],
\quad v=o(l),
\tag{UFhet}
$$

则有全anti的 $\alpha$-PNE。全局hub权比可无界，只需上述**局部** $R,K$；$K$ 必须包含source到side最小hub权的比例，source可能不在 $H_j$，不能只用 $R$。

其可用势为 $E_{\rm het}(h)=\sum_{j,b}P_j(S_{jb};x_{jb})$，
$S_{jb}=\{v\in H_j:h_v=b\}$，
$P_j(S;x)=\sum_{r=1}^{|S|}G_j(x+\sum_{t\le r}a_{v_t})$，
其中 $v_t$ 按hub权非增、同权按固定身份排序，空和为0。令 $c$ 为加入后或删除前的真实资源费用，$\Delta P_j$ 为相应正向势增量或势减量，插入/删除边际满足
$c\le\Delta P_j\le(a_v/A_j)c\le Rc$；
light重置满足 $\kappa_d(w_l/A_j)\le K\kappa_d(w_l/a_v)$ 的预算。由条件支付主资源余量，任一单hub局部最小点即给上述均衡。完整证明和两名审查者的冻结攻击在[S10]§10及对应审查；凸性加强从 $1+a_v/A_j$ 到 $a_v/A_j$ 已重新核对，没有沿用较弱冻结覆盖。

**准确排除范围：** 满足各自强迫式及倍率条件的上述二元同费、唯一主源拓扑，不能成为同一倍率的全状态非存在反例；仅增加跨源共享side，或局部 $R,K$ 受控的异权hub，不解除这些条件界。**没有排除：** 不满足条件的游戏。一般实例的 $R,K$ 和强迫假设没有统一控制；单凭条件失败不能判定反例，也不证明其他选态方法不可能。同权v3与异权排序势这两个均衡定理，不能未经新证明拼成“异权hub也有同样的双倍率v3界”。

### 4.3 三负载曲率约束只限制保形模拟

`WC-R1-PREFIX-SMOOTHING v1` 的一般三负载接口：给 $0<L<H<U$，非零非负系数有限多项式 $p$，令 $\gamma=\ln(U/H)/\ln(H/L)>0$，则

$$
\frac{p(U)}{p(H)}\ge\left[\frac{p(H)}{p(L)}\right]^\gamma.
$$

若 $0<\varepsilon<1, p(L)\le\varepsilon p(H)$，便有

$$
\frac{p(U)}{p(H)}\ge\varepsilon^{-\gamma},\qquad
\deg p\ge\frac{\ln(1/\varepsilon)}{\ln(H/L)}.
$$

完整短证：$q_k=a_kH^k/p(H)$ 是有限支撑概率，$r=L/H\in(0,1)$，有 $p(L)/p(H)=\mathbb E r^K$、$p(U)/p(H)=\mathbb E[(r^K)^{-\gamma}]$。对凸函数 $z^{-\gamma}$ 用 Jensen；次数界来自 $\mathbb E r^K\ge r^{\deg p}$。非零性与正负载保证分母和对数均合法。[S11]§1、内部先重构后冻结攻击。

因此不能在这**同一三个正负载**上同时任意低漏、保持有界高平台而无视代价。源 prefix 特化 $m\ge3, L=3/2-2^{-m},H=3/2,U=2-2^{-m}$ 给 $\gamma>2^{m-2}$：$\ln(U/H)\ge3/16, \ln(H/L)\le8\cdot2^{-m}/11$，故 $\gamma\ge33\cdot2^m/128>2^{m-2}$。删去 $m\ge3$ 的延伸已有严格反例：$m=2,p(x)=x,\varepsilon=5/6$，其高低比不满足粗指数1的结论。改变权重、可达负载、允许过冲、重配资源尺度或重证全状态偏离都不由此排除；这不是实际游戏均衡阈值。

相邻次数的**精确**三点包络扩展 `WC-R1-THREELOAD-ENVELOPE v1` 不作为本稿可调用事实：源页称完整证明与知情复核，但规范五轴表和全仓精确账本仍登记 candidate / extension review pending，现有冻结独立审查明确覆盖的是上述曲率原稿。这一状态冲突没有由整理静默升级；这里只调用无该欠账的一般 Jensen 界。

## 5. 已证时钟障碍与尚缺的次数义务

这里的输入限于每人两个动作。fresh资源对指两资源与旧资源及其他新增资源对均不相交；每对仅由指定三元使用。按玩家的固定线性顺序编号 $0,1,\ldots,n-1$。把从全0依次翻至全1、再同序翻回的 $2n$ 条严格 $\alpha$ 改善叫双轮环；合法态恰为该环访问的 $2n$ 个状态，即位串至多变位一次。限制回这两个动作后，与3.1最后扩充 $2^E$ 策略的有全空均衡游戏，是不同的输入合同。

### 5.1 全状态编译已能做；统一预算的次数效率已被封闭

`WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1`：任 $n\ge3$、输入次数至多 $p$、双轮严格 $\alpha\ge1$ 环，以首位为anchor 0，令

$$
B\ge\max_{s,i}C_i^G(s),\quad
\eta=\min_{\text{全部环边}}(C_i^G(s)-\alpha C_i^G(s'))>0,\quad
L=\binom{n-1}{2},
$$

$$
\delta=\max_{1\le i<j<n}\left(1-\frac{\min(w_0,w_i,w_j)}{w_0+w_i+w_j}\right)<1.
$$

加入全部 $(0,i,j)$ 的 fresh 同费互补资源对：两资源仅由该三元使用，玩家0、i、j分别选择侧 $s_0,1-s_i,s_j$（侧编号为0、1），费用为
$M[x/(w_0+w_i+w_j)]^D$，$M=2\alpha B$。若整数 $D\ge1$ 满足

$$
\delta^D\le\frac\eta{4\alpha^2BL},\tag{U}
$$

则输出的**全部状态**无 $\alpha$-PNE，次数 $q=\max\{p,D\}$。合法态保留环；非法态互补到 $s_0=0$ 后，首个1后必还有0，对该玩家翻回0有完整触发的高费出口。完整证明与独立审查已覆盖全状态，问题不再是仅有环。[S14]。

`WC-UNIFORM-CLOCK-BUDGET-BARRIER-v1` 则对**所有输入、顺序、anchor及所有满足$U$的整数D**证明

$$
D>2(\alpha+1)\ln(2\alpha),\qquad
\frac{\alpha\ln q}{q}<\frac\alpha{\alpha+1}<1.
$$

关键推导：`WC-R3-DENSE-LOCAL-v1` 的局部窄权比严格 $R$-FIP 给全局权比 $R=\max w/\min w>\alpha$，此处用的是 FIP，不能只从 $R$-PNE存在推无环。任意anchor的三元族总有含全局最大/最小的三元，故
$\delta\ge(R+1)/(R+2)$。又 $0<\eta\le B,L\ge1$，从$U$

$$
D\ge\frac{\ln(4\alpha^2BL/\eta)}{\ln(1/\delta)}
>(R+1)\ln(4\alpha^2L)>2(\alpha+1)\ln(2\alpha).
$$

置 $t=2(\alpha+1)\ln(2\alpha)$；$t>\alpha+1, \ln t<2\ln(2\alpha)$，且 $x-(\alpha+1)\ln x$ 在 $x>\alpha+1$ 严增，得 $q>(\alpha+1)\ln q$。此链直接包括 $\alpha=1$，并适用任何实际输出次数 $q\ge D$。[S15]（其审查明确重建了窄权比FIP依赖）。

**排除范围：** 仅优化$U$中的输入环、anchor、人数、$B/\eta$ 不能靠这个 $\alpha$ 证书否定本题。**未排除：** 同一架构用实际时钟差在不满足$U$的次数成功；$U$只是充分条件，不是必要条件。源已有不满足$U$而实际成功的固定全三元统一幅度证书，只用来防止把预算障碍升级为架构障碍，不在此搬入有限次数扫描。没有证明输出游戏必有 $q/\ln q$-PNE，也不排其另有更强非存在证书。

### 5.2 实际非统一时钟也不能无条件删掉真实余量

`WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1`：保留上述互补三元，但每对可用不同的任意非负系数多项式 $f_T$。写 $T=(0,i,j)$，三种pair负载费用之和

$$
S_T=f_T(w_0+w_i)+f_T(w_0+w_j)+f_T(w_i+w_j).
$$

该三元在合法半环三名玩家上的 margin 恰为

$$
(z-\alpha x,\ x-\alpha y,\ y-\alpha z),\quad
x=f_T(w_0+w_i),\ y=f_T(w_i+w_j),\ z=f_T(w_0+w_j).
$$

若 $g_i$ 是全部时钟合法 margin，$\gamma_i>0$ 是基体玩家 $i$ 两条环边余量的较小者，则保全部严格环边必要有

$$
\sum_i g_i=-(\alpha-1)\sum_T S_T,\qquad
(\alpha-1)\sum_T S_T<\Gamma:=\sum_i\gamma_i.
$$

这是必要预算，**不是充分全状态覆盖条件**；$\alpha=1$ 时不能除以 $\alpha-1$。[S16]§§1–6。

更强的严格反例 `WC-ANCHORED-MARGIN-DEPENDENCE-OBSTRUCTION-v1`：固定四人、权 $(1,1/2,1/4,1/8)$、$\alpha=21/20$、纯三次两动作基体，对每个预给整数次数上限 $D\ge0$，有有理游戏 $G_D$，保有严格双轮环；任何次数至多 $D$ 的 anchor0、010/101同费互补三元时钟，只要保全部环边，就仍保留0101/1010为 $\alpha$-PNE。可逐三元不同次数和幅度，任意多对、可省略三元；每名玩家自己的两个动作非空且相交为空，不同玩家可共享资源。[S16]§9。

调用[S16]§9的显式有理基体后，下列余量压缩推导自足：该基体在环上两半余量 $\gamma_i>0$，在 $b=0101$ 全玩家稳定gap $K_i=\alpha C_i(b^{\oplus i})-C_i(b)>0$，其互补1010同样稳定。给每个动作 $b\in\{0,1\}$ 增加仅由玩家 $i$ 的该动作使用的private资源，费用 $c_{i,b}(x)=t_i(x/w_i)^3$，其中
$t_i=(\gamma_i-\varepsilon)/(\alpha-1)>0$；使用时负载恒为 $w_i$、成本恰为 $t_i$，可把环余量全部压为 $\varepsilon$，同时稳定gap变成 $K_i'=K_i+\gamma_i-\varepsilon>K_i$。每位两动作分别用两条不同private资源，所以不依赖必选资源。

保环迫 $\sum_T S_T<4\varepsilon/(\alpha-1)$。任三元总权 $W_T$ 的最大pair权至少 $2W_T/3$，所以任整数 $0\le k\le D$ 的真实clock margin逐列至多 $(3/2)^D S_{T,k}$，其中 $S_{T,k}=(w_0+w_i)^k+(w_0+w_j)^k+(w_i+w_j)^k$ 是三个pair权和的幂之和。取

$$
0<\varepsilon\le\min\{\tfrac12\min_i\gamma_i,
(\alpha-1)\min_iK_i/[8(3/2)^D]\}
$$

令 $K_{\min}=\min_i K_i>0$，上述选择使任意保环clock对 $b$ 每玩家的增益小于 $K_{\min}/2$，故所有偏离仍稳定。固定基体存在及完整有理数据在源§9，由两份独立literal审计和冻结攻击核验；此推导没有把某个 LP 搜索失败当证明。

**准确否定范围：** 不依真实余量或其他实例数据、只依输入次数/人数/权谱/倍率的通用有限保环次数上界。
**未被否定：** 有额外余量条件的特选增长族、改变相位/两侧费用/arity/辅助玩家、放弃保原环。量词是 $\forall D\exists G_D\forall$允许clock，不能换成一个固定 $G$ 对所有次数均失败。一般增长族的 $\alpha\ln q/q$ 控制仍 **OPEN**。

### 5.3 类内同权时钟的通用编译器有不受次数影响的反例

`WC-CLASS-INTERNAL-CLOCK-COMPILER-OBSTRUCTION-v1`：有显式12人、64资源、基体次数8、三类权 $(1,1/4,1/16)$ 各4人、两动作游戏，具有严格 $21/20$ 双轮环，同时有严格精确PNE的类前沿 $b$：仅最轻类的index0取1，其余人取0。[S17]§8；完整有理fixture和独立审查齐备。

每权类index取固定线性顺序，类前沿意为各类沿此顺序的位串至多改变一次。任意同类递增三元在前沿都不是010或101。若只追加fresh、仅该三人使用、两侧同费的互补010/101资源对，则参与者翻位的负载只能是

$$
(\text{旧},\text{真实新})=(2w,2w)\quad\text{或}\quad(w,3w).
$$

任意非负非减费用使该clock旧成本不超过新成本，包括离开前沿的偏离。有限多对任意叠加也如此，故 $b$ 的全部严格精确稳定不等式保留。结论允许任意次数、幅度和数量，甚至不要求保原环。

**反驳的断言：** 对所有严格双轮输入，仅追加这些类内有序三元clock即可得到无同倍率PNE。此通用断言为假。
**没有反驳：** 只处理更高增长倍率或附额外输入条件的编译器、跨类/非递增相位、两侧异费、共享clock资源、其他arity、辅助玩家。固定 $21/20$ 反例没有无界量词；旧仅端点无出口而仍有内部改善的反例已被这一更强同机制版本替代，不另列。

## 6. 完整成本归约不能自动缩成小用户支持

`WC-APPROXIMATE-SUPPORT-DISTORTION-v1`。$m\ge1,\varepsilon>0$，原权为 $(1,\varepsilon,\ldots,\varepsilon)$，二标签成本表

$$
V_i(s)=s_i\left(s_0+\varepsilon\sum_{\ell=1}^m s_\ell\right).
$$

一个全用户线性资源（加零费动作标记）即实现此表，全0是精确PNE。表示方保留同一玩家/两标签，可任意改正权、升到任意有限次数、增加资源，但每条正费资源潜在用户至多 $r\ge1$。若所有玩家和状态满足

$$
V_i(s)\le\widehat C_i(s)\le\beta V_i(s),\quad\beta\ge1,
$$

则必要有

$$
\beta\ge\max\left\{1,
\frac{m(1+\varepsilon)}{(r-1)(1+m\varepsilon)+m\varepsilon}\right\}.
$$

证明：动作0成本为零，完整乘性上界迫所有正费资源只能在动作1使用。每 light 从singleton到heavy/light pair的成本增加 $D_l\ge1+\varepsilon-\beta\varepsilon$；每条heavy资源至多被 $r-1$ 名light重复收费，单调性给

$$
\sum_lD_l\le(r-1)\widehat C_0(\mathbf1)
\le(r-1)\beta(1+m\varepsilon).
$$

合并即所述界。固定有限 $r,\beta$，先取 $m>\beta(r-1)$，再取足够小的正有理 $\varepsilon$ 即违反；$r=\beta=1$ 时任何 $\varepsilon>0$ 已失败。对称成本失真 $V/A\le\widehat C\le AV$ 对应 $\beta=A^2$。[S13]§§11–12，独立冻结攻击已处理边界。

**排除：** 同玩家同标签、完整逐状态成本、统一有限用户支持和统一有限失真的归约，即使改权和提高次数；原次数已经为1。
**未排除：** 辅助玩家、仅保均衡或单向lift、选择性成本保持。资源**数量**可压缩与资源**用户支持**可缩小不同；附录A的有限表示没有绕过此障碍。不能把此有精确PNE的线性游戏当全类非存在证据。

## 7. OPEN 与证据边界

本题的一般肯定或严格否定证明仍缺。上述子类界没有全类归约；真实改善环没有全状态非存在量词；全状态时钟编译没有所需增长次数效率；有限签名替代没有统一于所有权、人数、动作和selector的倍率估计。这些是缺失义务，**不表示未排除的路线不可能**，也不列推荐路线或答案猜测。

本稿没有采用承重未决候选。源中旧 pending、旧节号或原审查hash，均按后续实际审查与规范diff确定覆盖范围；S表记录实际层级。源三玩家稿所引缺失审查、非分离frontier缺失原稿，以及未审完整轨道/保守端点推广，不作为可调用事实。有限搜索未果、固定次数扫描和工具失败不进默认正文。全类题开放不抹去2节的可靠成果。

## 附录 A：可直接调用的有限签名与严格反例规范接口

### A.1 全状态 selector 的精确线性替代

`WC-ACTION-SIGNATURE-COMPRESSION-v1`、`WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1`。固定正实权 $w_i$、有限动作标签集 $A_i$（大小 $m_i\ge1$）、$d\ge0,\alpha\ge1$。令 $M=\sum_i m_i,\Omega=\prod_iA_i$。每个非空动作签名 $\sigma\subseteq\{(i,a):a\in A_i\}$ 是一种资源，

$$
L_\sigma(s)=\sum_jw_j\mathbf1_{(j,s_j)\in\sigma}.
$$

相同签名的多项式系数可合并，故全部真实状态/偏离成本能以至多 $2^M-1$ 个签名资源精确表示。零费用singleton签名标记区分动作；原空策略可能变成零费非空集合，不改变成本身份。

对全状态selector $h(s)=(i(s),t_i(s))$，允许选当前动作，写 $s'=(t_i,s_{-i})$。$\operatorname{Rec}(h)$ 是确定性映射 $s\mapsto s'$ 的所有周期状态之并，含自环。列 $(\sigma,k),0\le k\le d$ 定义

$$
B_h[s,(\sigma,k)]
=\mathbf1_{(i,s_i)\in\sigma}L_\sigma(s)^k
-\alpha\mathbf1_{(i,t_i)\in\sigma}L_\sigma(s')^k.
$$

$k=0$ 以 $x^0=1$ 计算常数项，再乘使用指示量；不作 $0/0$。对非负系数向量 $a$，$(B_ha)_s=C_i(s)-\alpha C_i(s')$。恰有以下一项成立：

$$
\exists a\ge0:\ B_ha>0\text{ 逐行};\qquad
\exists\lambda\ge0:\ \sum_s\lambda_s=1,\ B_h^\top\lambda\le0\text{ 逐列}.
$$

前者给**同一系数游戏的全部状态**严格偏离，后者排除该selector在任一系数游戏中处处严格改善。因而固定 $w,m,d$ 的所有游戏有 $\alpha$-PNE，等价于 **每个 $h$ 各自存在一个 dual**；不能换成共同 $\lambda$、只检查某个selector或只检查环。若仅允许非空列指标集 $J$，则系数 $a$ 仅在 $J$ 上取非负值，dual只检查这些列；此为固定列子锥，不能无证明将它等同complete列集。上述有限矩阵替代同样成立。

有理 $w,\alpha$ 时存在有理证书；实输入不承诺有效算法。一般线性替代和两套精确审计、内部先重构冻结攻击齐备。[S18]。

### A.2 反例的整数与空交反链核心规范形

`WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1`：每个固定 $d\ge0$、固定实 $\alpha\ge1$，全模型存在无 $\alpha$-PNE 游戏，当且仅当正整数权、每资源费用恰 $x^k\ (0\le k\le d)$、每策略非空的有限反例存在。可保人数，不保规模、成本表或精确最佳因子。有限严格余量先允许有理扰动；取 $W_i=Qw_i\in\mathbb Z_{>0}$，选 $L$ 使 $m_{e,k}=La_{e,k}/Q^k\in\mathbb Z_{\ge0}$，复制这些个单位单项式资源后，所有真实成本精确乘 $L$。动作取商和非空化需保strict margin；不是把任意实参数逐字整数化。

`WC-ANTICHAIN-CORE-NORMAL-FORM-v1` 另给**不依倍率的单向lift**：保留每玩家包含极小动作，令 $F_i$ 为这些动作的交集，将必选权吸收到 $c'_e(x)=c_e(B_e+x)$，$B_e=\sum_{i:e\in F_i}w_i$，删去仅有一个极小动作的玩家。若全删则得到原精确PNE；否则得人人至少两种非空、互无包含、交集为空的core。补回必选资源并恢复固定玩家，core每个 $\alpha\ge1$ 均衡都提升原游戏，因为

$$
C_i^G(\operatorname{lift}u)=C_i^H(u)+K_i(u_{-i}),\quad K_i\ge0,
\qquad r\le\alpha r'\Rightarrow r+K_i\le\alpha(r'+K_i).
$$

对所有原动作的偏离，由其包含一个极小动作且费用非负完成。不能反投影原均衡，不保人数或最优倍率。结合整数展开，严格反例可限制到整数单位单项式core；没有人数、动作数、权重、次数输入精度或资源数的统一搜索截止。[S12]，core有单独独立审查，不能用旧整数化审查替代。

complete 签名允许某玩家的块 $\sigma_i=A_i$；proper/core 签名要求每块 $\sigma_i\subsetneq A_i$，允许空块，仅排全空签名。二动作proper每人块为 $\varnothing,\{0\},\{1\}$，共 $3^{|N|}-1$ 个非空签名。人人至少两动作时保留全部proper字典与零费singleton标记可得到合法core。必须先用上述单向lift说明为什么能限制core，不能随手删complete列就宣称仍刻画原所有游戏。

## 来源、精确版本与实际审查层级

所有原数学状态另见同快照的 `research/weighted_congestion_frontier/CLAIMS.md`、`research/review_status.json`；本表不取代它们。各正文的具体 Claim ID 已写在对应节。表中“独立”指仓库内部真实先重构关键义务、随后冻结攻击；是否先自行发现整套构造由实际审查明写，均不是外审。路径均相对于仓库根，S链接固定同一数学源提交。

| 来源 | 原数学正文与具体节 | 实际审查或承重状态 |
| --- | --- | --- |
| [S0] | MODEL.md 全文；ACCEPTANCE.md「本次题目与唯一完成标准」 | 定义/任务，不是新定理；WC-TARGET v1保持OPEN |
| [S1] | CLAIMS.md「WC-LIT-UPPER-D v1」；LITERATURE.md「数学基线」 | Paper Fact；外部一手文献陈述，本项目未独立重建全文 |
| [S2] | odd_ring/cohort_lower_bound_and_envelope.md §§1–6、8 | odd_ring_independent/REVIEW.md、EXACT_ENVELOPE_REVIEW.md；odd_ring_parameters/polynomial_envelope_review.md，一般证明与内部独立审查；非整个拓扑阈值 |
| [S3] | resource_support.md 全文 | 完整直接短证明；独立冻结审查未记录，未外审 |
| [S4] | weight_bands/finite_weight_class_potentials.md §§1–8、11–13 | weight_types/finite_weight_classes_reconstruction_review.md；interaction_height_review.md，完整证明与内部独立攻击（高度审查已知旧机制） |
| [S5] | high_degree_share.md「精确陈述」至「固定正权向量」 | high_degree_share_review.md 最终逐资源版复核；原独立计算简式与一般证明覆盖分开 |
| [S6] | cyclic_clone_improvement_cycles.md「定理」及§§1–4 | ordinal_potentials/cyclic_clone_improvement_cycles_review.md，独立重构实现瓶颈后攻击，未冒称先发现lifting |
| [S7] | template_certificates/stationary_selector_obstruction.md §§2–4、7 | template_certificates/stationary_selector_obstruction_review.md，追加仿射引理/回返等价有单独冻结攻击，非高次仿射推广 |
| [S8] | common_power_mixture_obstruction.md §§1–4 | ordinal_potentials/common_power_mixture_review.md，所有实幂/非负连续混合/全部最小点均独立攻击 |
| [S9] | separable_ordinal_obstruction.md §4 | ordinal_potentials/minimizer_scope_review.md；直接范围引理与内部复核，不提供新存在界 |
| [S10] | shared_side_truncated_potential.md §§8.1–8.3、9.9、9.14–9.18、10 | multisource_force_increment_review.md、heterogeneous_hub_sorted_side_review.md；v3、精确强迫阈值与异权ID各按实际独立重构/冻结攻击；v3审查角色互换，旧v1/v2身份不改 |
| [S11] | polynomial_curvature/three_load_curvature_bound.md §§1–4 | polynomial_curvature/review.md；曲率原稿有独立冻结攻击。精确相邻次数扩展账本仍candidate，不调用 |
| [S12] | template_certificates/integer_counterexample_normal_form.md §§1–4、7–8 | integer_counterexample_normal_form_review.md 与 antichain_core_normal_form_review.md（均在 reviews/weighted_congestion/template_certificates/） |
| [S13] | template_certificates/selector_local_moments.md §§11–12、14–15 | 同审查目录 approximate_support_review.md、selector_mover_support_review.md；合入改节号有diff复核，未改变数学 |
| [S14] | anchored_cycle_lock.md「精确身份」及全状态证明 | ordinal_potentials/anchored_cycle_lock_review.md；一般编译完整，输出次数依实例 |
| [S15] | uniform_clock_budget_barrier.md §§1–4 | ordinal_potentials/uniform_clock_budget_barrier_review.md；实际输出次数强化与最终diff已核，不把充分预算说成必要 |
| [S16] | anchored_clock_actual_margins.md §§1–6、9 | ordinal_potentials/actual_clock_margins_review.md；接口与新增余量反例分别冻结攻击，曾pending处已由后续冻结攻击/空core追加核查闭合 |
| [S17] | class_front_phase_quotient.md §8.1–8.4 | ordinal_potentials/class_internal_clock_compiler_review.md；仅审新§8，旧端点例不是同一反例 |
| [S18] | template_certificates/finite_action_duality.md §§1–4 | template_certificates/finite_action_duality_review.md；一般替代内部独立重构与精确核验 |

上表数学正文（[S2]–[S18]）均位于 `research/current/weighted_congestion/`；审查均位于 `research/reviews/weighted_congestion/`，特别标明者除外。[S0]/[S1] 位于 `research/weighted_congestion_frontier/`。

[S0]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/weighted_congestion_frontier/MODEL.md
[S1]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/weighted_congestion_frontier/LITERATURE.md
[S2]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md
[S3]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/resource_support.md
[S4]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md
[S5]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/high_degree_share.md
[S6]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/cyclic_clone_improvement_cycles.md
[S7]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md
[S8]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/common_power_mixture_obstruction.md
[S9]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/separable_ordinal_obstruction.md
[S10]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/shared_side_truncated_potential.md
[S11]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md
[S12]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md
[S13]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/template_certificates/selector_local_moments.md
[S14]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/anchored_cycle_lock.md
[S15]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/uniform_clock_budget_barrier.md
[S16]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/anchored_clock_actual_margins.md
[S17]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/class_front_phase_quotient.md
[S18]: https://github.com/SOMEBODYJUN/co-work-anl/blob/c623edd5f717e5f58151e6ab3363499c7ea2b114/research/current/weighted_congestion/template_certificates/finite_action_duality.md
