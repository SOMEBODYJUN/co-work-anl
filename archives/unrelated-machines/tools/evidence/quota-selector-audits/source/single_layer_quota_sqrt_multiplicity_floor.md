# 单层配额超图的平方根重数地板

## 精确合同

给有限变量集合 X, |X|=q>=1，资源宇宙 R，邻域 A_x subseteq R。假设 |A_x|>=K>=1 对全部 x，且每资源的总关联度 deg(u)=|{x:u∈A_x}| <= Delta。令 nu_t 为最大变量数，使每个变量选 t 个邻域资源、所有选出的资源互不相交（1<=t<=K）。令

b = max_{1<=t<=K} min{t/K, nu_t/q}.

这正是根→变量→K配额标签→资源的单层需求DAG的 b*（若标签层每变量唯一且K需求）。

**UM-SQRT-MULTIPLICITY-FLOOR-v1。**

\[b\ge B(K,\Delta):=\max_{1\le t\le K}\min\left\{\frac tK,\frac{K-t+1}{K-t+1+t\Delta}\right\}.\]

若 K≥√Δ+1，取 t₀=⌊K/(√Δ+1)⌋，得到
\[b\ge t_0/K\ge 1/(\sqrt\Delta+1)-1/K.\]

不能把这写成无条件的固定 sqrt 地板而忽略 K 小于 sqrt(Delta)+1；此时上式的右端可能非正，B 的整数最大值应保留。

## 证明

固定 t。取最大 t-束匹配，大小 s=nu_t；其每变量选出的 t-子集并 U 有 |U|=st。对未选变量 x，极大性意味着 |A_x\\U|<=t-1，否则可再加入一个 t-束。因此 |A_x∩U|>=K-t+1。将此不等式对 q-s 个未选变量求和，左端至少 (q-s)(K-t+1)。右端按资源重数上界至多

\[\sum_{u\in U}\deg(u)\le\Delta|U|=\Delta st.\]

所以 q-s <= Delta st/(K-t+1)，即

\[\frac{\nu_t}{q}=\frac{s}{q}\ge\frac{K-t+1}{K-t+1+t\Delta}.\]

和 t/K 取最小、再对 t 取最大即得命题。

令 α=√Δ≥1，实函数 h(t)=(K−t+1)/(K−t+1+tΔ) 随 t 单调下降。实点 t*=K/(α+1) 满足（去掉正的 +1 修正时）h(t*)=1/(α+1)，而 +1 只使 h 更大。t₀=⌊t*⌋ 因而 h(t0)>=1/(α+1)，t0/K>=1/(α+1)-1/K。若 t₀≥1（即 K≥α+1），即得显示式。

## 平方根量级的示例（不声称达到连续下界）

令 q=g Delta。将 X 分成 g 组，每组 Delta 个变量；每组共享同一个私有资源集 R_j 大小 K，组间资源不交。则 max resource degree=Delta。对 t，组内最多 floor(K/t) 个变量能取得互不交的 t-子集，且可实现；故

nu_t = g floor(K/t),  nu_t/q=floor(K/t)/Delta,

b = max_t min{t/K, floor(K/t)/Delta}.

当 K→∞ 且 Delta 固定，令 s=floor(K/t)；对任意固定整数 s≥1 可取 t≈K/s，于是该族的极限值为

max_{s≥1} min{1/s,s/Delta}.

这等于\(\max\{\lfloor\sqrt{\Delta}\rfloor/\Delta,\,1/\lceil\sqrt{\Delta}\rceil\}\)。例如 Delta=2,3,4 时极限分别为1/2,1/2,1/2；Delta=5 时为2/5；Delta=9 时为1/3；Delta=100 时为1/10。因此为 Theta(1/sqrt(Delta))。它说明平方根依赖在数量级上不能从“总资源重数≤Delta”假设改进，但不声称精确达到连续计数下界 B(K,Delta)。

## 与困难性归约的含义

若一个单层共享标签归约的全部邻域满足 |A_x|>=K 和总资源重数 Delta，且目标 NO 值 b<=delta，同时 K>=sqrt(Delta)+1，则必须

Delta >= (1/(delta+1/K)-1)^2

（由 floor 细节可用直接整数检验；渐近为 Delta >= (1/delta-1)^2）。故把碰撞重数只做成 O(1/delta) 不足以压低所有中间 t 层；至少需要平方级重数，或破坏本合同（异质邻域、非单层约束、跨变量状态资源等）。这只是必要条件，不是复杂度困难性；平方级重数仍是固定 epsilon 下常数，未排除 PCP/Label-Cover 构造。

## 独立有限审计

`single_layer_quota_sqrt_multiplicity_floor.py` 以 Fraction 穷举 q=3、K=2,3、资源宇宙至多5的所有邻域族，逐个计算 nu_t 并核验上面的 Delta 计数下界；另对近锐分组族直接反算 nu_t 和 b。其输出 `ok: 23192 exhaustive systems; group formulas checked`；有限核验覆盖 q=3、K∈{2,3}、资源宇宙至多5的全部邻域族（有限 K 受 t=1/K 离散限制）。另以分组族直接计算上述 floor 公式；不把连续平衡点误报为离散精确值。这只是有限审计，不升级一般命题状态。

**状态：无复杂度假设的自足引理；有限审计通过；不含困难性结论。**

## 与整束缺陷势合同的关系

`UM-LARGE-BUNDLE-COLLISION-FLOOR-v1` 对给定完整束使用整束重染色、Cauchy 和 Hall 匹配，给出含根上取整的更强有限参数界及平方池精确锐例。本页只使用最大 t-束的极大性计数，输入合同允许邻域大小至少 K，证明更短但有限常数通常更弱；两者都只约束单层共享标签接口。故本页是可独立复用的计数推论/不同输入合同，不把它与整束势算法或一般困难性混同。

## 多标签输入的适用边界

本文不把同一变量的所有标签邻域取并集；并集会制造原需求树中不存在的虚假 t-束。若每个变量已给出一个完整标签 e_x，|S_{e_x}|≥K，且全部标签资源的总重数至多 Δ，则固定任意一个这样的 e_x 并令 A_x=S_{e_x}，本文引理直接适用。若某变量没有完整标签，只能先使用局部比例 |S_e|/K<1 的上界，不能直接套用 (1)。

## 资源总量上界与数量级夹逼

若资源总数为 \(N=|R|\)，任意 \(t\)-束匹配满足 \(t\nu_t\le N\)。令 \(\rho=N/(qK)\le1\)。则
\[
b\le\max_t\min\{t/K,\rho K/t\}\le\sqrt{\rho},
\]
因为两项的几何平均恒为 \(\sqrt{\rho}\)。在资源总量达到 \(N=qK/\Delta\) 的设计中，任何单层系统都有 \(b\le1/\sqrt{\Delta}\)；结合 (2)，最大度受限的可证下界和容量上界同为平方根量级。这个夹逼仍只说明单层接口的尺度，不能提供源问题的可解码性或复杂度困难性。
