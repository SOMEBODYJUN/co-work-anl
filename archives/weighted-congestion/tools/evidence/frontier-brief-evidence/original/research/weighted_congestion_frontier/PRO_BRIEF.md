# 加权原子拥塞：Pro 接题材料与精确方法障碍

本稿是现行数学资产的派生读取稿，不另立真值账本。默认只读本稿与任务正文即可接题；原证明、审查、程序和证书按来源编号定点查阅。本稿没有预设开放路线，也没有新增数学 Claim。

**数学源快照：** `SOMEBODYJUN/co-work-anl` 的 `d5492a5deb217e85f438a38a4809057d8ece1f6e`。下文所有 S 编号均指该提交的原文件和所列具体节，末表连接实际审查。内部已审不等于外部同行评审；未认证全球新颖性。当前唯一全类问题仍 **OPEN**。原历史身份 `WC-TARGET v1` 的宽目标不改写，本次完成条件固定如下。

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

### 2.5 潜在使用森林与保次数挂树归约

WC-INCIDENCE-FOREST-EXACT-v1：以玩家与资源为二部图顶点，边 $i-e$ 当且仅当某个合法策略含 $e$。若此**潜在使用图**是森林，则任意正实权、任意有限值非负非减费用及任意非空有限耦合策略族都有精确PNE。无需多项式、连续性或相同权，允许空策略、零/常数费用、必选资源与任意资源分枝；不推出FIP。[S19]§§1–4。

WC-ONE-PLAYER-TREE-PRIVATE-LIFT-v1 是直接可用的保次数接口。输入保留玩家集 $N_0\ne\varnothing$ 和资源集 $E_0$（可空），要求删除玩家不得潜在使用 $E_0$；由全部非 $E_0$ 资源、全部玩家及相关潜在边组成的附属二部图是森林，且每个连通分量至多含一个保留玩家。根必须是玩家；不能换成核心资源根或同一附属分量接触两个核心玩家。

对每条保留玩家 $i$ 的根边 $i-e$，构造私有资源 $z_{i,e}$，费用为常数 $p_{i,e}\ge0$，策略映射
$\psi_i(s_i)=(s_i\cap E_0)\cup\{z_{i,e}:e\in s_i\setminus E_0\}$。
每条根边分别标记，映射单射；不能只投影到 $E_0$ 而合并策略。保留核心资源与权重，删除附属玩家；资源集为空时添从不使用的零费资源。

输出同一个不依赖 $\alpha$ 的固定lift $L$，使对每个reduced状态 $u$、每个保留玩家原合法偏离 $t_i$，

$$
C_i^G(Lu)=C_i^H(u),\qquad
C_i^G(t_i,(Lu)_{-i})\ge C_i^H(\psi_i(t_i),u_{-i}).
$$

删除玩家在固定延续中精确稳定。故H每个 $\alpha\ge1$ 的均衡均提升为G同倍率均衡，原非负系数次数上限 $d\ge0$ 不升；无反向投影、最优倍率相等或统一core规模保证。[S19]§5。

承重机制是每根资源同时构造报价 $p_e$ 与根bit为0/1的两个内部稳定延续：根使用时真实费恰 $p_e$，不使用时冻结延续后进入费至少 $p_e$。递归中玩家任意耦合策略只按父资源bit取有限最小报价和；可选者按两个条件最小值之差降序，以真实进入费贪心接纳，平局顺序固定。首个不同接纳决定的比较证明所选子玩家总负载随父背景非增，给两侧报价关系。不可行bit单独分类为必用/禁止，不作无穷差；这也覆盖跳跃费用。完整自足递归在[S19]§§2–3，独立先重构和冻结攻击已完成。§1旧candidate标签由§8及规范账本明确更新，不视为仍待审；外审未记录。

**保留原因与范围：** 任意大的所写挂树可在不升次数、不损近似倍率下删去；用这些挂树堆规模不能改变core的存在保证。core仍可有任意环、权谱和交互高度；不提供全类归约到可控core，也不预设如何研究这些core。

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

### 4.1 一般同权cohort奇环的实际阈值已闭合到 $T_d$

WC-ODD-RING-GENERAL-COHORT-ACTUAL-UPPER-v2：整数 $d\ge2$、奇数 $m\ge3$，hub $H_i$ 权 $u_i>0$，cohort $i$ 有整数 $n_i\ge1$ 名共同权 $v_i>0$ 的light，下标模 $m$。互异主资源副本 $A_i^b$ 同费 $F_i$，侧资源 $B_{ij}^b$ 同费 $G_i$（同cohort全部side同费）；$F_i,G_i$ 为任意非负系数次数至多 $d$ 多项式，允许零。hub位 $h$ 用 $\{A_i^h\}\cup\{B_{i-1,j}^h:1\le j\le n_{i-1}\}$；light位 $l$ 用 $\{A_i^l,B_{ij}^{1-l}\}$。

**每个如此游戏都有 $T_d$-PNE，不需要任何统一强迫假设。** 和2.1同拓扑下界合用，其有限实例最优倍率的上确界恰为 $T_d$，不声称某一个有限游戏取得。并有

$$
T_d\le H_d+\frac1{2^d+1}
\le\frac d{1+\ln d}+\frac1{2^d+1}<\frac d{\ln d}.
$$

最后严格性由 $\ln d\le d-1,\ 1+\ln d\le d$ 给
$d/[\ln d(1+\ln d)]\ge1/(d-1)>1/(2^d+1)$。因此本拓扑可取 $C=1,d_0=2$，**不是全类结论**。[S2]§10及 general_cohort_actual_upper_review.md：完整一般证明、先重构与最终冻结攻击；未外审。未规范登记的早期v1草案只给较弱上界，不作为第二项结果。

**可直接核验的有限选态接口。** 固定任意 $\alpha\ge T_d>1$。令 $k_i$ 为aligned light数，aligned意为light位等于自身hub位，anti意为不等；$z_i=h_i\mathbin{\mathrm{xor}}h_{i+1}$。置 $q_i=G_i(v_i)$，$D_i=G_i(v_i+u_{i+1})-q_i\ge0$，

$$
A_{iz}(k)=F_i(u_i+kv_i)+q_i+zD_i,\qquad
B_{iz}(k)=F_i((n_i-k+1)v_i)+q_i+(1-z)D_i.
$$

真实light稳定计数集 $I_i(z)$ 由
$A_{iz}(k)\le\alpha B_{iz}(k)$（$k>0$）和
$B_{iz}(k+1)\le\alpha A_{iz}(k+1)$（$k<n_i$）定义，是非空整数区间。写 $I_i(0)=[a_i,b_i]$，$c_i=\min I_i(1)\le\lfloor n_i/2\rfloor$。
每个缺陷位置 $i$ 取 $z_i=0$、其余 $z_j=1$，奇数 $m$ 保证合法偶parity；任选一组相容hub位，另一组全局互补费用相同。非缺陷群取 $k_j=c_j$；缺陷群只列

$$
k_i=\min\{b_i,\lfloor n_i/2\rfloor\}\quad(a_i\le\lfloor n_i/2\rfloor),\qquad
k_i=\max\{a_i,\lceil n_i/2\rceil\}\quad(b_i\ge\lceil n_i/2\rceil).
$$

去重后至多 $2m$ 个计数候选，每群固定前 $k_j$ 名light aligned 即成为真实状态；其中至少一个是 $\alpha$-PNE。可逐候选用真实偏离验证，无任意实数输入的有效算法或位复杂度承诺。

关键理由不是“正测试失败所以有均衡”：先得到全部light稳定的单缺陷候选，只有缺陷两端可能有坏hub。稳定区间位于半数左/右时记L/R；奇数中心同时可取两中央计数时允许两个标签。相邻L→R会迫同一hub在两个候选 $S,T$ 满足
$C_H(S)>\alpha C_H(T)$、$C_H(T)>\alpha C_H(S)$，与非负性矛盾，故全不稳反设只能全部同向且无双标签。全L通过消去成对light及非负平移，重新导出完整strict正测试，才调用已审包络；全R由下式逐群相乘得到同一矛盾：

$$
x[P(x+y)-\alpha P(x)]\le y[\alpha P(x+y)-P(y)]
\quad(x,y>0,\ \alpha\ge T_d).
$$

此式对单项式 $P(t)=t^k$ 等价于 $\alpha\ge f_k(x/y)$，$k=0$ 亦成立，故逐非负系数求和适用；先从strict边界排除零分母再作全R比值相乘，权比沿环消去。完整推导及奇数中央双标签处理在[S2]§§10.3–10.7。

**准确排除范围：** 保持上述cohort内同权、同side费用、同费动作副本、奇环关联的全部游戏，不能给超过 $T_d$ 的实际非存在因子；这比旧 WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1 只限制同时强迫正测试更强，旧证书及下界身份不改。**未被否定：** 不满足此拓扑合同的游戏。不能把该拓扑当全类规范形，也不能把没有统一强迫这一点单独当成逃出本定理的条件。删除本项会遗漏已闭合的实际拓扑边界，重复把其旧OPEN当成未解问题。

### 4.2 共享 side 的最强条件存在界与排序势障碍

**共同拓扑。** $d\ge2$，hub集 $V\ne\varnothing$，hub权 $a_v>0$；每light $l$ 权 $w_l>0$，有唯一main source $o(l)\in V$。主副本 $A_v^0,A_v^1$ 同费 $F_v$；每side $j$ 有同费 $G_j$ 的副本 $B_j^0,B_j^1$、hub子集 $H_j$、light子集 $L_j$，允许跨source多light、多hub及空集。所有副本资源互异，费用均非负系数次数至多 $d$。对 $b\in\{0,1\}$，hub位 $b$ 用 $\{A_v^b\}\cup\{B_j^b:v\in H_j\}$；light位 $b$ 用 $\{A_{o(l)}^b\}\cup\{B_j^{1-b}:l\in L_j\}$。定义
$W_v=\sum_{o(l)=v}w_l,\ T_j=\sum_{l\in L_j}w_l,\ U_j=\sum_{v\in H_j}a_v$。全anti指light位为 $1-h_{o(l)}$。

**可调用定理：WC-HETEROGENEOUS-HUB-SORTED-SIDE-v2。** 仅对 $H_j\ne\varnothing$ 定义 $A_j=\min_{v\in H_j}a_v$，令

$$
R=\max\bigl(\{1\}\cup\{a_v/A_j:H_j\ne\varnothing,\ v\in H_j\}\bigr),\qquad
K=\max\bigl(\{1\}\cup\{a_{o(l)}/A_j:H_j\ne\varnothing,\ l\in L_j\}\bigr).
$$

对任意实数 $\tau\ge1,\alpha\ge1$，若 $\alpha\ge R,\ \alpha\tau\ge Kd$，且每light满足

$$
F_v(a_v+w_l)+\sum_{j:l\in L_j}G_j(w_l)
\ge\tau\left[F_v(W_v)+\sum_{j:l\in L_j}G_j(T_j+U_j)\right],
\quad v=o(l),
\tag{UFtau}
$$

则下面有限势 $E_{\rm het}$ 的**每个**单hub翻位局部最小点配全anti给真实 $\alpha$-PNE。$\tau,\alpha$ 不需排序，含 $\tau=1$，零/常数费用、空集合。全局hub权比可无界，只依局部 $R,K$；source可能不在 $H_j$，故 $K$ 不能只用 $R$ 代替。旧异权v1及同权旧版本身份、证据均保留；最强接口不由旧版未经证明拼接，而由新§11证明。

令 $S_{jb}=\{v\in H_j:h_v=b\}$，$x_{jb}=\sum_{l\in L_j:h_{o(l)}=b}w_l$，

$$
E_{\rm het}(h)=\sum_{j,b}P_j(S_{jb};x_{jb}),\qquad
P_j(S;x)=\sum_{r=1}^{|S|}G_j\left(x+\sum_{t\le r}a_{v_t}\right).
$$

$v_t$ 按hub权非增，同权按固定身份排序，空和零。令 $c$ 为加入后或删除前真实资源费，$\Delta P_j$ 为对应正向势增量或减量，则
$c\le\Delta P_j\le(a_v/A_j)c\le Rc$。这是凸性尾均值边际界，不依严格凸性；$\alpha\ge R$ 使真实side的 $\alpha$ 成本差不超过固定light的势差。

**重置增量与付款的完整短接口。** 令 $\kappa_d(t)=\min\{dt,t+1\}$。给 $A,w>0,x\ge0,T\ge x+w,U\ge0$，非空前缀满足 $A\le p_1<\cdots<p_n\le U$、$p_{r+1}-p_r\ge A$；空列亦允许。对非负系数次数至多 $d$ 的 $G$，$Y=T+U$，有

$$
\sum_{r=1}^n[G(x+w+p_r)-G(x+p_r)]
\le\kappa_d(w/A)[G(Y)-G(w)].
$$

短证：空列直接成立；否则 $Y-w\ge nA>0$。逐项导数界 $G'(z)\le d[G(Y)-G(w)]/(Y-w)$ 给 $dw/A$ 倍界。另一界令 $c(z)$ 为这些长 $w$ 区间的覆盖密度、$b=1+w/A$。几乎处处 $0\le c\le b$，$\int_0^Yc=nw\le b(Y-w)$。利用 $G'$ 在 $w$ 两侧非减，以 $G'(w)$ 比较低高段，得 $\int cG'\le b\int_w^YG'$，给第二倍界。首前缀下界、总上界及 $x+w\le T$ 均不可删；原区间可能穿过 $w$，不能误用区间包含。常数及零费用直接成立。

应用时前缀是hub权部分和，最小间距 $A_j$、末项至多 $U_j$；空 $H_j$ 的势误差零，不定义或除以其 $A_j$。已有源增量界为

$$
\sum_{o(l)=v}\kappa_d(w_l/a_v)[F_v(a_v+w_l)-\tau F_v(W_v)]
\le d[F_v(a_v+W_v)-F_v(a_v)]\quad(\tau\ge1).
$$

其完整非负系数逐项证明在[S10]§9.9。强迫式给每light全部side的增量预算
$\tau\sum_j[G_j(T_j+U_j)-G_j(w_l)]\le F_v(a_v+w_l)-\tau F_v(W_v)$。
用 $\kappa_d(w_l/A_j)\le K\kappa_d(w_l/a_v)$，先将每light全部side合计、只领取一次主预算，source重置误差满足

$$
B_v\le\frac{Kd}{\tau}\Delta_v\le\alpha\Delta_v
\le\alpha F_v(a_v+W_v)-F_v(a_v),\quad
\Delta_v=F_v(a_v+W_v)-F_v(a_v)\ge0.
$$

这里只有正数 $\tau$ 作除数。hub真实偏离时light保持原动作；重置仅比较势，局部最小性与上式闭合真实 $\alpha$ 成本差。light由强迫式满足 $\tau C_{\rm current}\le C_{\rm deviation}$。一般证明及先重构/冻结攻击见[S10]§11与 heterogeneous_hub_product_budget_review.md；内部已审，未外审。

**同权子域：WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v3。** 所有 $a_v=u>0$ 时 $R=K=1$，条件成为 $\alpha\tau\ge d$，势退化为
$E(h)=\sum_{j,b}\sum_{r=1}^{|S_{jb}|}G_j(x_{jb}+ru)$。特别 $\tau\ge d$ 可取 $\alpha=1$；$d\ge16,\tau=\ln d$ 给 $\alpha=d/\ln d$，均须保留(UFtau)和拓扑合同，非全类结论。该同权身份有自己的§9.14–9.18证明与审查，旧v1/v2未改。

**严格反例：WC-SHARED-SIDE-EXACT-FORCING-THRESHOLD-v1。** 在上述**同权hub子域**中，保证精确PNE的统一强迫阈值恰为 $\tau=d$：上半由同权v3取 $\alpha=1$；对每个实数 $1\le\tau<d$，下面属于该同权子域的两玩家、四资源游戏严格满足(UFtau)，却四态均有严格改善。该精确阈值不覆盖一般异权hub。

令 $\varepsilon=d-\tau>0$，$K_0=\tau(2^d-1)+d(\tau-1)$，
$t=\varepsilon/(2K_0)$，$D=1-(\tau-1)t$，
$A=[\tau(1+t)^d-t^d]/D$，$a=(A+d)/2$。
hub权1、light权 $t$，只有该hub作为source，$F(x)=ax,G(x)=x^d$，策略用共同拓扑中的一主一side。$0<t<1/2,D>1/2$，且

$$
\tau(1+t)^d-t^d-dD\le-\varepsilon+K_0t=-\varepsilon/2<0
\quad\Longrightarrow\quad0<A<a<d.
$$

强迫差为 $a(1+t)+t^d-\tau[at+(1+t)^d]=(a-A)D>0$。两个aligned态由light翻位严格改善；两个anti态由hub翻位，成本减少 $(1+t)^d-1-at\ge(d-a)t>0$，覆盖全部四态。[S10]§9.17及新增冻结攻击。

这严格反驳“在同权子域中，(UFtau)在任意 $\tau\ge1$ 均保证精确PNE”，防止把强迫本身当通用精确均衡工具。**仅否定 $\alpha=1$**；改善幅度可以趋近1，不能升级为固定 $\alpha>1$ 的反例，更没有否定全类目标。它也没有证明v3在 $\alpha>1$ 的充分乘积界是必要界。

**已证方法障碍：WC-SORTED-SIDE-GLOBAL-MINIMUM-R-BARRIER-v1。** 对每个实 $R>1,1\le\alpha<R$、整数 $d\ge2$、实 $\tau\ge1$，存在上述结构的游戏，(UFtau)真空成立，$K=1$，其排序势 $E_{\rm het}$ 的**全部全局最小点**都不是 $\alpha$-PNE，且均为严格单hub局部最小点。即使另取 $\tau\ge d/\alpha$ 满足乘积预算，也不能删除 $\alpha\ge R$ 后继续依赖该势的最小点。

构造：无light、主费用全零，只有一个side副本对，$G(x)=x$。取 $A>0,a=RA$、整数 $n>\alpha R/(R-\alpha)$，各有 $n$ 名权 $a$ 与权 $A$ 的hub。若副本0有 $x$ 名重hub、$y$ 名轻hub，直接展开降序势得

$$
E(x,y)-E(n,0)=a(n-x-y)^2+(a-A)y(n-y)\ge0.
$$

等号恰在 $(x,y)=(n,0),(0,n)$：所有重hub与所有轻hub分别占一侧。两态中重hub翻位使势增 $a>0$，轻hub翻位使势增 $na-(n-1)A>0$；而任一重hub真实改善比
$na/(a+nA)=nR/(R+n)>\alpha$。因此在全部全局最小点之间择优也无效。[S10]§11.4及独立冻结攻击。

**准确否定范围：** 此排序势局部/全局最小化在 $\alpha<R$ 下的统一均衡保证；包含只在全局最小点之间择优。**未被否定：** 其他势、在非最小态选态或其他机制。该游戏有精确PNE：最小化两侧总负载差绝对值，任一严格改善都会严格缩小该差，矛盾。故障碍不是无均衡反例，也不证明 $\alpha\tau\ge Kd$ 对 $\alpha>1$ 必要。

**存在定理的准确范围：** 满足(UFtau)、$\alpha\ge R,\alpha\tau\ge Kd$ 的游戏，不能成为同倍率的全状态非存在反例。任意实例的 $R,K$ 与强迫假设没有统一控制；单凭条件失败不能判定反例，也不证明其他方法不可能。精确强迫阈值反例与排序势方法反例的主语不同，均不能升级为全类目标否定。

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

### 5.4 已闭合的条件接口：全前沿出口可编译成全状态覆盖

WC-CLASS-FRONT-ALLSTATE-COMPILER-v1：输入MODEL游戏 $G$，旧费用次数至多整数 $p\ge0$，实数 $\alpha\ge1$，每人恰两个互异资源子集动作0/1；允许旧空动作、零和常数费用。全体玩家划分为非空有序类 $a$，类宽 $n_a\ge1$、类内权同为 $w_a>0$；不同类权可相同，跨类权比任意。类前沿沿固定顺序至多一次bit变化，$\mathcal F$ 为全部类都处于前沿的状态集，$s\oplus i$ 为玩家翻位。定义

$$
B=\max_{s,i}C_i^G(s),\qquad
\eta=\min_{s\in\mathcal F}\max_{i:s\oplus i\in\mathcal F}
\{C_i^G(s)-\alpha C_i^G(s\oplus i)\},\qquad
L=\max_a\binom{n_a-1}{2}.
$$

类宽至多2时该二项式取0；每个前沿有保前沿翻位。**承重前提 $\eta>0$：每个product-front都有保product-front的strict $\alpha$ 出口。** 它不是单个strict sweep环；有限性给 $0<\eta\le B$。若 $L=0$，前沿已经是全状态，原游戏即无 $\alpha$-PNE。

若 $L\ge1$，置 $M=2\alpha B$，取正整数 $D$ 满足

$$
\delta_D=(2/3)^D\le\frac{\eta}{4\alpha^2BL}.
$$

每类每个 $1\le j<k\le n_a-1$，给三人 $(a,0),(a,j),(a,k)$ 添加一对fresh、仅三人使用、两侧同费的互补010/101时钟；费用
$c_a(x)=M[x/(3w_a)]^D$。共添 $2\sum_a\binom{n_a-1}{2}$ 条资源，保持玩家、权重、旧动作和全部旧资源使用；输出次数至多 $q=\max\{p,D\}$，全状态均有strict $\alpha$ 出口，选定出口真实余量至少 $\eta/2$。可取
$D=\lceil\ln(4\alpha^2BL/\eta)/\ln(3/2)\rceil$。它只显示新增次数无独立跨类权比损失，**不证明 $B/\eta$ 与权谱、人数无关**。[S17]“条件编译接口：全部同权类前沿出口到全状态非存在”。

短证：所有锚定三元都不触发恰等价于各类是前沿。前沿保前沿出口的clock新成本至多 $LM\delta_D$，故余量至少 $\eta-\alpha LM\delta_D\ge\eta/2$。非前沿类取最早反于首位的玩家；其后有同首位者，因此至少一项旧clock成本 $M$，翻位后全部incident三元不满载。真实基体新成本至多 $B$，余量至少
$M-\alpha B-\alpha LM\delta_D\ge\eta/2$。没有同时重置其他玩家。

更精确地，每条保前沿边的参与clock前后均为真实用户数 $2\to2$，成本完全相同；若mover参与 $r_i\le L$ 对，clock $\alpha$-margin恰为 $-(\alpha-1)r_iM\delta_D$。故也可用分离预算

$$
\delta_D\le\frac1{4\alpha L},\qquad
(\alpha-1)LM\delta_D\le\eta/2.
$$

$\alpha=1$ 时第二式自动成立，不能除以 $\alpha-1$；此时所需新增次数不依 $\eta$。一般实参数证明和两套预算均由独立重构及冻结攻击覆盖，未外审；有理数据及有理 $\alpha$ 可用有理幂比较选择 $D$，不靠浮点舍入证书。

**与已证障碍的关系：** 5.3中的严格稳定前沿不满足 $\eta>0$，故新定理没有推翻旧反例；5.2的真实余量依赖也未被删除。已闭合的是此精确合同下从全部前沿出口到全部状态出口的步骤。**OPEN：** 尚无满足全类严格否定增长量词的输入族与实际输出次数估计；须按输出的实际次数核对第1节增长证书，不能把基体次数上限 $p$ 当输出实际次数。固定输入非存在不补齐增长量词。删除本项会把已经成立的编译步骤继续误写成缺口，或误把旧sweep反例扩大到具有全前沿出口的新合同。

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

本题的一般肯定或严格否定证明仍缺。上述子类界没有全类归约；真实改善环没有自动给全状态非存在量词；条件编译器已有明确全覆盖和次数预算，但尚无满足严格否定增长量词的输入族；有限签名替代没有统一于所有权、人数、动作和selector的倍率估计。这些是缺失义务，**不表示未排除的路线不可能**，也不列推荐路线或答案猜测。

本稿没有采用承重未决候选。源中旧 pending、旧节号或原审查hash，均按后续实际审查与规范diff确定覆盖范围；S表记录实际层级。源三玩家稿所引缺失审查、非分离frontier缺失原稿，以及未审完整轨道/保守端点推广，不作为可调用事实。有限搜索未果、固定次数扫描和工具失败不进默认正文。全类题开放不抹去2节的可靠成果。

## 附录 A：可直接调用的补充接口

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

### A.3 无UF的固定hub精确light响应

WC-FIXED-HUB-LIGHT-THRESHOLD-RESPONSE-v1。采用4.2二元同费、唯一source结构，但进一步要求**每条side只有唯一light**，可含任意hub子集；费用次数允许 $d=0$，权任意正实。输入任意固定的全部hub位 $h$，只允许light移动，不需UF。输出精确light响应，全部strict light改善路径终止；下述序势对每条light偏离保留全符号和平局，单light局部最小点恰为精确响应。[S20]。

各source独立。把其hub副本重标为0、权为 $a>0$，light集合 $I$、总权 $W=\sum_{i\in I}w_i$；固定hub后每light的全部side成本 $q_i^0,q_i^1$ 都为常数。若其他light在0的总权为 $x$，真实成本差为

$$
D_i(x)=F(a+x+w_i)+q_i^0-F(W-x)-q_i^1.
$$

$W-x$ 包含偏离者自身，不能改成 $W-w_i-x$。$F$ 非常数时 $D_i$ 严格递增；在有限可达集
$X_i=\{\sum_{j\in T}w_j:T\subseteq I\setminus\{i\}\}$ 上选 $t_i$ 使
$\operatorname{sgn}(x-t_i)=\operatorname{sgn}D_i(x)$，可达零点必须精确取为阈值。对0侧集合 $S$、负载 $L(S)$，

$$
\Psi(S)=\frac12L(S)^2-\sum_{i\in S}w_i(t_i+w_i/2),\qquad
\Psi(S\cup\{i\})-\Psi(S)=w_i(L(S)-t_i)\quad(i\notin S).
$$

势差与加入0的真实成本差同号，反向删除符号相反。$F$ 恒定时改取
$\Psi(S)=\sum_{i\in S}(q_i^0-q_i^1)$，不可强套二次式伪造平局。各source势相加，有限状态给FIP及精确响应。

可直接选态：从本source全部light在0开始，按 $t_i$ 非降扫描，当前0侧总权为 $L$；仅当 $L>t_i+w_i$ 才将 $i$ 删除到1。保留者以后 $L$ 只降，不想离开；删除者当时新 $L>t_i$，后续删除 $j$ 时新 $L>t_j\ge t_i$，所以不想回返。每名light至多一次strict移动；常数 $F$ 时独立取较小side成本即可。阈值的直接构造可能枚举指数多子集，不承诺输入位复杂度。

存在/FIP本身是Milchtaich(1996) §4 Theorem1与§8正权扩展的**已知推论**：每source是共同两策略、player-specific singleton加权游戏，成本函数 $F(a+z)+q_i^0,F(z)+q_i^1$ 非减。当前价值是显式阈值势及删除接口；一般证明、文献适用性、冻结攻击和独立literal审计齐备，不认证这些表示的新颖性。[S20]与同快照LITERATURE的“Milchtaich(1996)”条目。

**准确范围与错误lift：** 不覆盖多light共享side，不给跨不同 $h$ 的共同势。更不能把“先重置light，再判断hub是否改善”当真实hub偏离：4.2的两玩家 $\tau<d$ 无精确PNE例，每个固定hub都有精确light响应，整体互补使重选响应后的hub成本相同，真实冻结light的hub翻位却严格改善。故固定hub精确响应/重置后稳定不能自动提升为原游戏均衡；缺少的是这种跨 $h$ 使用时的兼容预算，仍为OPEN。本接口保留是为准确闭合固定外场响应义务，同时防止把它误升为共同选态定理。

## 来源、精确版本与实际审查层级

所有原数学状态另见同快照的 `research/weighted_congestion_frontier/CLAIMS.md`、`research/review_status.json`；本表不取代它们。各正文的具体 Claim ID 已写在对应节。表中“独立”指仓库内部真实先重构关键义务、随后冻结攻击；是否先自行发现整套构造由实际审查明写，均不是外审。路径均相对于仓库根，S链接固定同一数学源提交。

| 来源 | 原数学正文与具体节 | 实际审查或承重状态 |
| --- | --- | --- |
| [S0] | MODEL.md 全文；ACCEPTANCE.md「本次题目与唯一完成标准」 | 定义/任务，不是新定理；WC-TARGET v1保持OPEN |
| [S1] | CLAIMS.md「WC-LIT-UPPER-D v1」；LITERATURE.md「数学基线」 | Paper Fact；外部一手文献陈述，本项目未独立重建全文 |
| [S2] | odd_ring/cohort_lower_bound_and_envelope.md §§1–6、8、10 | odd_ring_independent/REVIEW.md、EXACT_ENVELOPE_REVIEW.md、odd_ring_parameters/polynomial_envelope_review.md、general_cohort_actual_upper_review.md；下界、正测试及一般同权cohort实际阈值各按对应冻结覆盖，非全类上界 |
| [S3] | resource_support.md 全文 | 完整直接短证明；独立冻结审查未记录，未外审 |
| [S4] | weight_bands/finite_weight_class_potentials.md §§1–8、11–13 | weight_types/finite_weight_classes_reconstruction_review.md；interaction_height_review.md，完整证明与内部独立攻击（高度审查已知旧机制） |
| [S5] | high_degree_share.md「精确陈述」至「固定正权向量」 | high_degree_share_review.md 最终逐资源版复核；原独立计算简式与一般证明覆盖分开 |
| [S6] | cyclic_clone_improvement_cycles.md「定理」及§§1–4 | ordinal_potentials/cyclic_clone_improvement_cycles_review.md，独立重构实现瓶颈后攻击，未冒称先发现lifting |
| [S7] | template_certificates/stationary_selector_obstruction.md §§2–4、7 | template_certificates/stationary_selector_obstruction_review.md，追加仿射引理/回返等价有单独冻结攻击，非高次仿射推广 |
| [S8] | common_power_mixture_obstruction.md §§1–4 | ordinal_potentials/common_power_mixture_review.md，所有实幂/非负连续混合/全部最小点均独立攻击 |
| [S9] | separable_ordinal_obstruction.md §4 | ordinal_potentials/minimizer_scope_review.md；直接范围引理与内部复核，不提供新存在界 |
| [S10] | shared_side_truncated_potential.md §§9.9、9.14–9.18、10.1、10.3、11 | multisource_force_increment_review.md、heterogeneous_hub_sorted_side_review.md、heterogeneous_hub_product_budget_review.md；同权v3、异权v2与两个不同主语的反例各有实际独立重构/冻结攻击，旧身份不改 |
| [S11] | polynomial_curvature/three_load_curvature_bound.md §§1–4 | polynomial_curvature/review.md；曲率原稿有独立冻结攻击。精确相邻次数扩展账本仍candidate，不调用 |
| [S12] | template_certificates/integer_counterexample_normal_form.md §§1–4、7–8 | integer_counterexample_normal_form_review.md 与 antichain_core_normal_form_review.md（均在 reviews/weighted_congestion/template_certificates/） |
| [S13] | template_certificates/selector_local_moments.md §§11–12、14–15 | 同审查目录 approximate_support_review.md、selector_mover_support_review.md；合入改节号有diff复核，未改变数学 |
| [S14] | anchored_cycle_lock.md「精确身份」及全状态证明 | ordinal_potentials/anchored_cycle_lock_review.md；一般编译完整，输出次数依实例 |
| [S15] | uniform_clock_budget_barrier.md §§1–4 | ordinal_potentials/uniform_clock_budget_barrier_review.md；实际输出次数强化与最终diff已核，不把充分预算说成必要 |
| [S16] | anchored_clock_actual_margins.md §§1–6、9 | ordinal_potentials/actual_clock_margins_review.md；接口与新增余量反例分别冻结攻击，曾pending处已由后续冻结攻击/空core追加核查闭合 |
| [S17] | class_front_phase_quotient.md §8.1–8.4及“条件编译接口”整节 | ordinal_potentials/class_internal_clock_compiler_review.md、class_front_allstate_compiler_review.md；旧通用编译障碍与新全前沿出口条件编译分别冻结攻击，合同不同 |
| [S18] | template_certificates/finite_action_duality.md §§1–4 | template_certificates/finite_action_duality_review.md；一般替代内部独立重构与精确核验 |
| [S19] | incidence_forest_private_reduction.md §§1–6、8 | incidence_forest_private_reduction_review.md；森林存在/单根挂树lift完整证明与独立冻结攻击，初稿candidate由最终状态明确更新；不调用固定单环例 |
| [S20] | fixed_hub_light_threshold_response.md 全文 | fixed_hub_light_threshold_review.md；已知FIP/存在推论的完整重构与独立冻结攻击，显式势/删除接口，非原游戏共同均衡 |

上表数学正文（[S2]–[S20]）均位于 `research/current/weighted_congestion/`；审查均位于 `research/reviews/weighted_congestion/`，特别标明者除外。[S0]/[S1] 位于 `research/weighted_congestion_frontier/`。

[S0]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/weighted_congestion_frontier/MODEL.md
[S1]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/weighted_congestion_frontier/LITERATURE.md
[S2]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md
[S3]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/resource_support.md
[S4]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md
[S5]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/high_degree_share.md
[S6]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/cyclic_clone_improvement_cycles.md
[S7]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md
[S8]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/common_power_mixture_obstruction.md
[S9]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/separable_ordinal_obstruction.md
[S10]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/shared_side_truncated_potential.md
[S11]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/polynomial_curvature/three_load_curvature_bound.md
[S12]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md
[S13]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/template_certificates/selector_local_moments.md
[S14]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/anchored_cycle_lock.md
[S15]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/uniform_clock_budget_barrier.md
[S16]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/anchored_clock_actual_margins.md
[S17]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/class_front_phase_quotient.md
[S18]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/template_certificates/finite_action_duality.md

[S19]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/incidence_forest_private_reduction.md

[S20]: https://github.com/SOMEBODYJUN/co-work-anl/blob/d5492a5deb217e85f438a38a4809057d8ece1f6e/research/current/weighted_congestion/fixed_hub_light_threshold_response.md
