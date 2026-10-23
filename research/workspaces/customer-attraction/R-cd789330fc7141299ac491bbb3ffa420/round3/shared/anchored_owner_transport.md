# 锚定最优查询后的联合运输与 whole-IC 资金

2026-10-23，shared 提出，credible 已独立重构核对。本文加强其[普通利润运输 A](../credible/owner_hybrid_transport.md)：外部利润可避开已锚定查询的全部客户资源，因而与这些客户上的捕获利润同叶共用一份单位资金。任意锚集的结论先是静态资金结论；只有在下述明确的真实续局域才可购买原 IC。一般 half 仍 OPEN。

## 1. 任意锚集的残余运输

沿用固定最优 T、owner 分割 Q_i⊆T_i、并集 O。固定任意合法 B，设 K⊆{1,…,m} 且 B_i=T_i 对所有 i∈K。令

\[
A=\bigcup_{i\in K}T_i.
\]

保持所有 K 槽固定为 T_i，其余槽先用 Q_i，再任选 J⊆K^c 替为 B_i。基线的并仍是 O，因为每个被移去的 Q_i⊆T_i⊆A；每个实现扩张未替换 Q 槽后仍是合法 m 元组，所以覆盖不超过 |O|。

A 内所有客户永远被锚定槽覆盖。因此有更强的全部子集 hybrid 式

\[
\left|\bigcup_{i\in J}(B_i\setminus O)\right|
\le
\left|\{x\in O\setminus A:o(x)\in J,\ C_x\cap J=\varnothing\}\right|.
\tag{AHYB}
\]

这里 C_x={i:x∈B_i}。只在 O\\A 客户上构造 A 图：c_x>0 时从 owner 向其每个非owner覆盖者加容量1/c_x；c_x=0 时从 owner 向终点加单位库存。 source i 仍为该叶 O 外的普通利润

\[
b_i=\sum_{y\in B_i\setminus O}\frac1{c_y}.
\]

对 J⊆K^c，b(J)不超过 AHYB 左端；其右侧每个客户给出割容量恰一，所以所有 source cut 仍足够。有限最大流最小割给全部 source 同时送满。

每个锚定角色 i∈K 的 source 为零。O\\A 客户的 owner 不在 K，且 B_i=T_i⊆A 不覆盖 O\\A，所以这些角色没有任何角色边或终点边，完全隔离。任意全角色割可删掉其 K 部分化成上述 J；没有漏掉割。

因此外部利润运输可**完全排除 A 内全部客户资源和库存**，不只是避开 anchor 自己的 owner-error。

## 2. 与 A 上捕获利润共用一份资金

令 f 为上述任意可行流；out_ℓ 包含该角色到其它角色及终点的全部流出，in_ℓ只计角色流入。自环已删。定义

\[
s_\ell=\sum_{x\in Q_\ell\cap B_\ell\setminus A}\frac1{c_x}.
\]

真实 O\\A 份额给所有入边容量，故

\[
\operatorname{in}_\ell
\le u_\ell(O\setminus A)-s_\ell.
\]

source b_ℓ=u_ℓ(N\\O)，而 A⊆O，所以守恒给

\[
\boxed{\operatorname{out}_\ell
=b_\ell+\operatorname{in}_\ell
\le u_\ell(N\setminus A)-s_\ell.}\tag{FUND-A}
\]

对任何预留资金 0≤h_ℓ≤u_ℓ(A)，特别是对 A∩R 上捕获者的完整真实利润，有

\[
\boxed{h_\ell+\operatorname{out}_\ell\le u_\ell-s_\ell\le u_\ell.}\tag{JOINT-A}
\]

它们使用互不交的客户资源，不是先用一份 u 支付捕获，再用另一份 u 支付运输。若整张图统一缩小为 λf、同时 h_ℓ≤λu_ℓ(A)，则联合资金至多 λu_ℓ。

这仅对普通利润 A 图成立。调和 source 的 B 图不自动是原单位利润资金：例如共同目录为三个不交 singleton {x_1},{x_2},{y}，m=2，最优 T=({x_1},{x_2})、B=({y},{y})。B 图每角色 source 为 H_2/2=3/4，而其原利润只有1/2，尽管库存运输可行。因此不能把 B 的调和库存直接当作 whole-IC 可花利润。

## 3. whole-IC 的合法适用域

如果 B 是强制最优前缀 T_1,…,T_k 后，余下角色沿原完整 σ 的真实 rollout，取 K={1,…,k}。全部运输活跃角色都满足 ℓ>k；B 从它的真实历史 h_ℓ 开始一直跟随 σ，所以 v_ℓ=u_ℓ(B)正是该节点原 IC 的规定收益。

设联合资金 h_ℓ+out_ℓ 被用于任意合法查询，定义

\[
\theta_\ell=(h_\ell+\operatorname{out}_\ell)/v_\ell\le1,
\]

v_ℓ=0 时资金必零并取 θ_ℓ=0。对任何非负查询系数 X_(ℓ,j)，只要 Σ_jX_(ℓ,j)≤θ_ℓ，每条完整原 IC 用同一个标量系数后求和，就有

\[
\sum_{\ell,j}X_{\ell,j}d(h_\ell,T_j)
\le\sum_\ell\theta_\ell v_\ell
=\sum_\ell(h_\ell+\operatorname{out}_\ell).
\tag{WHOLE}
\]

未按客户重加权 IC。统一缩放 λ 的版本给 θ_ℓ≤λ。

**必须保留适用域。** 对任意非前缀锚集 K，FUND-A/JOINT-A 仍是正确的静态单位利润资金，但某些旧角色的 B 利润可能来自后来强制行动后的改枝叶，不是其原 IC 的规定完成叶，不能据此购买 IC。仅在实际位置 i 强制 T_i 时，过去非anchor角色也可能被运输访问；它们不能免费使用改枝利润。完整最优前缀隔离了所有过去角色，才使上述 WHOLE 应用合法。

## 4. 还没有解决的同系数问题

本组件给同一真实前缀续局内联合选择的 θ。它不保证 θ 等于旧 actual-prefix R 捕获流已经由 A_s/D_s 固定的 w_s；后者经常重新读取另一条真实叶。相同 owner、相同 source 或相同角色编号不等于相同有序历史节点。

仍需将 R 流、I 路由及这些前缀资金共同选为一组原完整 IC 的非负常系数，使互斥真实叶不重复花费库存，并只领实际 I/G 一次预算。本文没有作该动态结算。
