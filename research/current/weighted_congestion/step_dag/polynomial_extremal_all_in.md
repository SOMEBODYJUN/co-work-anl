# 阶跃有向无环源极值幅度的多项式全入状态

Claim ID：**WC-DAG-EXTREMAL-AMPLITUDE-ALL-IN-v1**。

本文给出完整一般证明；[独立重构和冻结攻击](../../../reviews/weighted_congestion/step_dag/polynomial_extremal_all_in_review.md)与配套精确审计分开记录。它是具有精确幅度正规化的多项式 DAG 子类存在定理，不是 WC-TARGET 的全类上界。与端点低泄漏检测不同，这里不要求任何模拟精度或高平台保真，直接核对一个真实纯状态的每个偏离。

## 1. 精确对象与结论

给定每个有限 simple DAG `D=(V,A)`，`m=|V|≥1`，索引采用任意拓扑顺序。每个 `d≥1` 为整数。根玩家 `0` 的权重为 `1`，每个轻玩家 `v` 的权重为任意正实数 `w_v`，满足

\[
 W=\sum_v w_v<1,\qquad
 t_v=\sum_{v\to u}w_u<w_v.
\]

资源为成对的 `a_0,b_0` 及 `a_v,b_v`。每对两个资源使用相同费用 `p_0` 或 `p_v`，均为非零、非负系数、次数至多 `d` 的多项式。根的两个策略是所有 `a` 资源和所有 `b` 资源。轻玩家 `v` 的两个策略为

\[
 S_v^0=\{a_0,b_v\}\cup\{a_u:u\to v\},\qquad
 S_v^1=\{b_0,a_v\}\cup\{b_u:u\to v\}.
\]

策略是资源集合，没有重复边，权重不随资源改变，玩家成本为所用资源费用之和。

令 `P_k` 为 `D` 的 `k` 顶点有向路径数，`q=q_D>1` 是唯一满足

\[
 q=1+\sum_{k=1}^mP_kq^{-k}
\]

的数。令

\[
 h_v=\frac{1+\sum_{u\to v}h_u}{q},\qquad
 \sum_vh_v=q-1.
\]

**实际幅度假设。** 存在 `A>0`，使

\[
 p_0(1)=A,\qquad p_v(1+w_v)=A h_v\quad(v\in V). \tag{N}
\]

这不是任意费用幅度：它精确保留已知阶跃源极值幅度在最小触发负载上的值。改变这个假设即改变结论适用的子类。

定义实际全入状态 `s*`：根采用所有 `a` 资源的策略，每个轻玩家采用 `S_v^1`，所以每个 `a_v` 都恰有根和其所有者 `v`，每个 `b_v` 恰有 `v` 的 outgoing 邻居。令

\[
 B_d(q)=\frac{q}{1+(q-1)(1+1/[q(q-1)])^{-d}},\qquad
 \alpha_d(q)=\max\{1+1/q,B_d(q)\}. \tag{1}
\]

**结论。** 对每个上述 `D,d,w,p`，状态 `s*` 是真实多项式游戏的 `α_d(q)`-PNE。特别地，对每个整数 `d≥16`，它是

\[
 \boxed{4\sqrt{d/\ln d}\text{-PNE}.} \tag{2}
\]

该因子与图大小、权重、系数及 `q` 无关，但只覆盖假设 `(N)` 的 DAG 子类。它不证明一般 DAG 多项式游戏具有相同界，不证明全类上界，不给新下界。所有检查均是偏离后重新计算真实负载；下文各偏离成本严格为正，无零比值问题。

依赖：非负系数次数界、DAG 路径递推、凸性 Jensen。路径门槛和极值幅度的来源是已独立证明的 `WC-R1-DAG-STEP v1`；这里的实际状态证明重新写出，不迁入阶跃非存在结论。外部评审及新颖性未认证。

## 2. 总权重的路径恒等式

记

\[
 \delta_v=w_v-t_v>0.
\]

令 `c_v` 为以 `v` 结束的全部有向路径数（含单顶点路径），故拓扑递推为

\[
 c_v=1+\sum_{u\to v}c_u.
\]

若 `A_D` 为 adjacency matrix，`w=(I-A_D)^{-1}\delta`，因为 DAG 的邻接矩阵幂零，求所有坐标之和得到

\[
 W=\sum_vc_v\delta_v. \tag{3}
\]

另一方面 `h_v` 是以 `v` 结束的全部路径的 `q^{-长度}` 权重和，所以

\[
 qh_v=\sum_{\gamma\text{ ends at }v}q^{1-|\gamma|}\le c_v.
\]

结合 `(3)` 和 `W<1`，

\[
 \boxed{\sum_vh_v\delta_v<1/q.} \tag{4}
\]

无需对每个 `δ_v` 施加统一下界，也没有统一泄漏率假设。

## 3. 全入状态中所有轻玩家稳定

把所有费用同时除以 `A>0`，可先设 `A=1`。根全入状态的成本为

\[
 C_0(s^*)=p_0(1)+\sum_vp_v(1+w_v)=1+\sum_vh_v=q. \tag{5}
\]

轻玩家 `v` 的真实当前成本为

\[
 C_v(s^*)=p_0(W)+\sum_{u\to v}p_u(t_u)+p_v(1+w_v). \tag{6}
\]

由 `W<1`、`t_u<w_u<1+w_u` 和单调性，

\[
 C_v(s^*)\le1+\sum_{u\to v}h_u+h_v=(q+1)h_v. \tag{7}
\]

其唯一另一策略偏离后，根核心资源 `a_0` 的负载为 `1+w_v`；每个 incoming 前驱资源 `a_u` 的负载为 `1+w_u+w_v`；所有者 `v` 新加入自身 `b_v`，负载为 `w_v+t_v`。因此完整偏离成本为

\[
 C_v(S_v^0,s^*_{-v})=
 p_0(1+w_v)+\sum_{u\to v}p_u(1+w_u+w_v)+p_v(w_v+t_v)
 \ge1+\sum_{u\to v}h_u=qh_v>0. \tag{8}
\]

最后一项只被下界为零，没有删掉真实成本。由 `(7)`–`(8)`，每个轻玩家的全部合法偏离均满足倍率 `1+1/q`。

## 4. 根偏离的精确有理包络

根切换到全部 `b` 资源后，真实成本为

\[
 C_0(S_0^1,s^*_{-0})=p_0(1+W)+\sum_vp_v(1+t_v)
 \ge1+\sum_vp_v(1+t_v). \tag{9}
\]

非零、非负系数、次数至多 `d` 的多项式，满足 `p(L)/p(H)≥(L/H)^d`，`0<L<H`。取 `L=1+t_v`、`H=1+w_v=L+δ_v`，并用 `(N)`，得

\[
 p_v(1+t_v)\ge h_v\left(1+\frac{\delta_v}{1+t_v}\right)^{-d}
             \ge h_v(1+\delta_v)^{-d}. \tag{10}
\]

函数 `g(x)=(1+x)^{-d}` 在 `x≥0` 严格递减且凸，因为

\[
 g'(x)=-d(1+x)^{-d-1}<0,
 \qquad g''(x)=d(d+1)(1+x)^{-d-2}>0.
\]

令 `T=Σ_vh_v=q−1>0`。Jensen 与 `(4)` 给

\[
 \sum_vh_v(1+\delta_v)^{-d}
 \ge T\left(1+\frac{\sum_vh_v\delta_v}{T}\right)^{-d}
 >T\left(1+\frac1{qT}\right)^{-d}. \tag{11}
\]

根偏离成本因此严格大于 `(1)` 分母；结合根当前成本 `(5)`，其改善倍率严格小于 `B_d(q)`。实际均衡使用弱不等式，故根与所有轻玩家共同给出 `α_d(q)`-PNE。

注意：该证明直接容纳任意低端泄漏和高负载过冲。过冲可使偏离成本增加，只会帮助所构状态稳定；低端泄漏由真实总权预算和凸性给出必要总量。它没有假设整张多项式曲线接近阶跃。

## 5. 一个核验得动的统一常数

由 `ln(1+x)≤x`，

\[
 B_d(q)\le F_d(q):=
 \frac q{1+(q-1)\exp\{-d/[q(q-1)]\}}. \tag{12}
\]

固定整数 `d≥16`，令 `L=ln d`、`K=4√(d/L)`。此时 `L<√d`：在 `d=16` 有 `ln16<4`，且 `√d−ln d` 在 `d≥16` 严格增加。因此 `K>4d^{1/4}>2`。

若 `q≤K`，则 `B_d(q)≤q≤K`。

若 `q>K`，则 `q>2`，从而 `q(q−1)>q²/2>K²/2=8d/L`。于是

\[
 F_d(q)\le\frac q{q-1}\exp\{d/[q(q-1)]\}
          <2d^{1/8}\le4d^{1/4}<K. \tag{13}
\]

所有轻玩家的因子 `1+1/q<2<K`。这证明 `(2)`，给出了显式绝对常数和起始次数。它们仅用于所写子类，不能交付为本题一般肯定结论。

## 6. 有限核验与尚未解决的范围

配套程序使用精确 `Fraction` 避免数值根：从小 DAG 中筛出整数 `q_D`，再用这些 `q` 计算精确 `h_v`；另测无边图 `m=q(q−1)`。卫星的多项式形状可任取非零非负系数形状，再按 `(N)` 归一化。逐资源重建全入状态和每个真实单方偏离，核验 `(3)`、`(4)`、`(5)`–`(11)` 的分数不等式。Jensen 一般证明不由这些有限案例代替。

还没有证明任意卫星幅度都能化成 `(N)`。也没有证明任何一般加权拥塞博弈可无损还原为本 DAG。若希望用这个机制推进全类唯一题，下一步必须处理这些实际缺口，而不是只增大 `q_D`、DAG 深度、路径数或提高费用次数。

## 身份、审计合同与继续研究

Objects、Domain、Quantifiers、Assumptions、Definitions、Scope 和 Conclusion 完整固定在第1节，均为任意有限图及合法正实权，实际幅度条件(N)不可删。Dependencies 为 MODEL 的实际成本、已证 WC-R1-DAG-STEP 的 q/h 定义与路径展开、非负单项式比较、有限 Jensen；本界不依赖端点低泄漏预算。Evidence 为正文一般证明、先依据精确陈述独立推导后读取冻结正文攻击，以及两套不互相导入的 Fraction 逐资源核验。Counterevidence / Objections：任意费用幅度、一般DAG之外策略族、零费用和异列费用均不在这个结构类内；仍未证明向这些类的归约。Status：complete restricted proof; independently reconstructed and exactly audited; unrefereed。Truth 为所写实际子类状态界；Value 为排除固定阶跃极值幅度下仅调多项式形状的放大；Novelty 未认证；Mechanism 为总权的缺口矩、Jensen和全入状态；Ambition 仍为全类 O(d/ln d) 题，尚未完成。

规范作者审计：`tests/audits/weighted_congestion/step_dag/verify_polynomial_extremal_all_in.py`；独立实现：`tests/audits/weighted_congestion/step_dag/independent_polynomial_all_in.py`。结果为 `evidence/runs/weighted_congestion/step_dag/polynomial_extremal_all_in.json` 与同目录 `polynomial_extremal_all_in_independent.json`。从仓库根运行 `--check RECORD_PATH` 只读复验；`--output NEW_PATH` 独占创建，默认输出 JSON。输入生成网格、seed（若适用）、代码 hash、算术与环境版本由记录给出。精确有理 q 的有限输入不替代任意实数 q_D 的正文证明。
