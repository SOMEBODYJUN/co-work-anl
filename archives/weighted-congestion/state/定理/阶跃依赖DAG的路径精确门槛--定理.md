---
id: "weighted-congestion/step-DAG-exact-path-threshold"
kind: "theorem"
type_tag: "定理"
title: "阶跃依赖DAG的路径精确门槛"
status: "proved"
summary: "辅助对称阶跃依赖模型的振幅最优全状态门槛由全部有向路径计数精确决定，并在正振幅取得。"
review_status: "independently reconstructed internally; not externally refereed"
scope: "specified symmetric step-cost game, outside finite polynomial latencies"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/step_dag/step_dependency_threshold.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/weighted_congestion/step_dag/independent_review.md"
legacy_ids:
  - "WC-R1-DAG-STEP v1"
---

# 阶跃依赖DAG的路径精确门槛

## 模型与量词

令 $D=(V,E)$ 是有限simple DAG，$m=|V|\ge0$。无自环、平行边，策略是资源集合。
根玩家0权重1；轻玩家正权 $w_v$ 满足

\[
W=\sum_vw_v<1,\qquad t_u=\sum_{u\to v}w_v<w_u\quad(u\in V).\tag{W}
\]

任意拓扑编号 $1,\ldots,m$ 的 $w_v=2^{-v}$ 都合法，所以每个这样的图均可实现。
振幅 $A_0,A_v\ge0$ 任意。资源 $a_0,b_0$ 费用为 $A_0\mathbf1[x\ge1]$；
$a_v,b_v$ 费用为 $A_v\mathbf1[x\ge1+w_v]$，断点取闭端点。
根动作是全部 $a$ 资源或全部 $b$ 资源；轻玩家动作是

\[
S_v^0=\{a_0,b_v\}\cup\{a_u:u\to v\},\qquad
S_v^1=\{b_0,a_v\}\cup\{b_u:u\to v\}.
\]

每人成本是所用资源费用之和，不乘权重；偏离后固定其他动作、重新计算真实负载。
$\alpha$-PNE 的定义是对所有合法单人偏离 $C_i(s)\le\alpha C_i(t_i,s_{-i})$，$\alpha\ge1$；零费用直接用此不等式。
这些非零阶跃费用不是有限次数多项式，本文件只是辅助模型。

令 $P_k$ 为恰有 $k$ 个顶点的有向路径数，单顶点计入，故 $P_1=m$。
若 $m>0$，唯一 $q_D>1$ 满足

\[
q_D=1+\sum_{k=1}^{m}P_kq_D^{-k}.\tag{Q}
\]

$m=0$ 定义 $q_D=1$。对每个满足(W)的权向量及每组非负振幅，存在 $q_D$-PNE。
对固定图和任意合法权，在所有振幅上取“实例最优近似因子”的上确界，恰为 $q_D$，且由正振幅取得。
这是全部状态门槛及弱端点存在；不是改善环证书，亦不导出任何多项式门槛。

## 全状态真实费用化简

稳定子对象ID：`weighted-congestion/step-DAG-literal-cost-reduction`。

固定根选 $a$ 列，令 $Z$ 为自身资源 $a_v$ 被轻玩家 $v$ 使用的点集。
记 $P_v(Z)=A_0+\sum_{u\to v,u\in Z}A_u$。真实当前/另一个动作费用恰为

| 玩家 | 当前 | 偏离后 |
|---|---|---|
| 根 | $A_0+\sum_{v\in Z}A_v$ | $A_0+\sum_{v\notin Z}A_v$ |
| $v\in Z$ | $A_v$ | $P_v(Z)$ |
| $v\notin Z$ | $P_v(Z)$ | $A_v$ |

证明：没有根的一列总负载小于1，所有资源费用为零。有根的一列核心必触发；卫星 $u$ 在其所有者同列时至少负载 $1+w_u$，所有者不在时至多 $1+t_u<1+w_u$。
轻玩家加入或退出前驱卫星，不会使“无所有者”的资源触发，因为其所有outgoing使用者总权仍严格小于所有者权。
切换自身资源恰改变该卫星触发。根偏离则把激活集 $Z$ 与补集交换。这逐项说明表中偏离也是真实费用。
两列对称覆盖另一根动作。

两个严格权条件不可改成等号：$t_u=w_u$ 可让仅有outgoing用户的卫星触发；$W=1$ 可让无根核心触发。
独立代码保存两种literal失败fixture。初期“一侧heavy singleton”转述已由来源审查纠正，本对象不采用那套不同策略。

## 路径递推、任意振幅上界及端点取得

主对象ID：`weighted-congestion/step-DAG-exact-path-threshold`。

对任意 $r>0$，拓扑递推

\[
h_v(r)=\frac{1+\sum_{u\to v}h_u(r)}r
\]

展开为所有以 $v$ 结束路径的 $r^{-\text{顶点数}}$ 之和，故
$\sum_vh_v(r)=\sum_kP_kr^{-k}$。
(Q)右端严格递减，左端严格递增；在1及充分大处变号，故根存在唯一。

为证明上界，固定根在 $a$ 列，拓扑处理点，遇 $v$ 时若
$q_DA_v\le P_v(Z)$ 则收入 $Z$，否则排除。收入者满足
$A_v\le P_v/q_D\le q_DP_v$，排除者满足 $P_v<q_DA_v$，所以全部轻玩家稳定。
对收入者归纳得 $A_v\le A_0h_v(q_D)$，因为其收入前驱也有此界。
因此根当前成本至多

\[
A_0\left(1+\sum_vh_v(q_D)\right)=q_DA_0
\le q_D\left(A_0+\sum_{v\notin Z}A_v\right).
\]

$A_0=0$ 时递推只收入零振幅点，所得全部当前费用为零，是精确PNE；没有任何除零。
$m=0$ 时根两动作均为 $A_0$，同样是精确PNE。

反向取任意 $A_0>0$、$A_v=A_0h_v(q_D)>0$。
每个状态若 $Z=V$，根改善比恰为 $q_D$；否则取拓扑顺序首个不在 $Z$ 的点 $v$，所有前驱已在 $Z$，故其当前成本
$P_v=q_DA_v$，偏离成本 $A_v>0$。
所以每个状态对每个 $1\le\alpha<q_D$ 均有严格改善；这是真实全状态覆盖。
上界同时保证 $q_D$ 端点PNE存在。全入状态本身根比为 $q_D$、轻玩家比为 $1/q_D$；全出状态的每个轻玩家比至多 $q_D$，两者均可见端点存在。

## 有理单参数实例

稳定子对象ID：`weighted-congestion/step-DAG-rational-balanced-factor`。

对任意 $r\ge1$、$A_0>0$ 取 $A_v=A_0h_v(r)$。$m>0$ 时此实例的最优近似因子恰为

\[
\beta_D(r)=\min\left\{r,\ 1+\sum_vh_v(r)\right\}.\tag{B}
\]

首个遗漏点或全入根给每态改善比至少此值。另一方面全入状态的最大改善比恰为第二项，
因为轻玩家当前成本 $A_v$、偏离成本 $rA_v$；全出状态每个轻玩家当前 $A_0$、偏离 $A_v\ge A_0/r$，且存在source满足等号，其最大改善比恰为 $r$，根无改善。
两态分别达到候选两项，证明(B)。$m=0$ 因子另为1。
有理 $1\le r<q_D$ 和有理 $A_0>0$ 给有理振幅；再选拓扑dyadic权 $w_v=2^{-v}$，得到完全有理的精确因子 $r$ 实例，从下方任意逼近 $q_D$。任意原实权不因振幅参数有理而自动变为有理。
没有声称每个图的 $q_D$ 或匹配端点振幅本身有理。

## 图极值、度界、树特化与浅DAG反例

稳定子对象ID：`weighted-congestion/step-DAG-path-extrema-and-degree`。

拓扑序中每个 $k$ 顶点子集至多有一条按该序通过全部点的路径，所以
$P_k\le\binom mk$。$m\ge1$ 时

\[
q_{\rm empty}=\frac{1+\sqrt{1+4m}}2\le q_D\le\Phi_m,
\qquad \Phi_m=(1+1/\Phi_m)^m.
\]

两端分别是无边图和完整传递DAG。$m>1$ 时有任何边即严格提高下界，缺任何边即由 $P_2<\binom m2$ 严格降低上界。
最大incoming度为 $\Delta$ 时，$P_k\le m\Delta^{k-1}$，对 $R>\Delta$ 有
$\sum_vh_v(R)\le m/(R-\Delta)$。
取 $(R-1)(R-\Delta)=m$ 的较大根，$m>0$ 时它大于 $\max\{1,\Delta\}$，故

\[
q_D\le\frac{\Delta+1+\sqrt{(\Delta-1)^2+4m}}2.
\]

因此 $m\to\infty$、$\Delta=o(\sqrt m)$ 时，与无边下界夹逼得 $q_D/\sqrt m\to1$。

稳定子对象ID：`weighted-congestion/transitive-tree-step-specialization`。

若有根树在轻顶点间放入每一对严格祖先到后代的边，而非只放父子边，深度以根0为0，则

\[
h_v(r)=r^{-1}(1+1/r)^{\operatorname{depth}(v)-1},\qquad
q_T=1+q_T^{-1}\sum_v(1+1/q_T)^{\operatorname{depth}(v)-1}.
\]

因深度按非降序排列后 $1\le d_{(j)}\le j$，深度和在星与链之间；代入严格单调根方程得到相同星/链极值。$m>1$ 时等号分别恰为星、链。
若最大轻深度 $H_m=o(\sqrt m)$，则
$m\le q_T^2-q_T\le m\exp((H_m-1)/q_T)\le m\exp(H_m/\sqrt m)=m(1+o(1))$，故 $q_T\sim\sqrt m$。

稳定子对象ID：`weighted-congestion/shallow-DAG-height-transfer-counterexample`。

此树高度结论不能换成一般DAG最长路径：两层各 $s$ 点的完全二部DAG只有二顶点长路径，却有
$P_1=2s,P_2=s^2$，根满足 $q^3-q^2-2sq-s^2=0$，从而 $q\sim s^{2/3}$。
例如令 $q=s^{2/3}x$，除 $s^2$ 后方程为
$x^3-s^{-2/3}x^2-2s^{-1/3}x-1=0$；唯一正阈值根在任意固定 $1\pm\eta$ 之间，故 $x\to1$。
它大于 $\sqrt m$ 量级；最大incoming度是 $s$，并不满足前述小度假设。

## 证据、后续用途和边界

完整证明由以上真实载荷表、拓扑归纳和首个遗漏点承担；
作者有限审计覆盖76个小图及12824个平衡状态、81256次偏离，独立审计覆盖103图及105050个振幅状态，另有树与严格边界检查，见[计算对象](../计算/曲率与阶跃DAG的精确有限核验--计算.md)。
来源审查提供树公式、浅DAG反例以及曾有错误转述的纠正，均在此保留，不仅留下PASS标签。

该 $q/h$ 递推是[端点低泄漏预算](有向无环端点低泄漏的精确次数预算--定理.md)及[极值幅度全入均衡](阶跃极值幅度的多项式全入均衡--定理.md)的公共输入；它本身没有多项式桥。
后续全状态线性次数族已否定原全类 $Cd/\ln d$ 目标，见同提交 `research/current/weighted_congestion/linear_degree_allstate_lower_bound.md`；那是另一构造的全部状态证明，不能由本阶跃定理或任何改善环替代。外部评审与全球优先权均未认证。
